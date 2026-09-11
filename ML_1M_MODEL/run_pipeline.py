"""
Master Pipeline Orchestrator for 1-Minute ML Trading Model
==========================================================
Coordinates:
1. Historical 1m OHLCV and Tick Trades data ingestion
2. Streaming order-flow aggregation & parquet caching
3. Deep multi-horizon technical feature engineering
4. Triple-barrier labeling & dynamic TP/SL target creation
5. Purged walk-forward training & model serialization
6. Strict out-of-sample backtesting & performance reporting
7. Sample live signal generation
"""

import os
import sys
import copy
import json
import argparse
import datetime
from typing import Optional, Dict, List, Tuple, Any

# Ensure stdout handles UTF-8 gracefully across all platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import (
    ModelConfig,
    MODELS_DIR,
    REPORTS_DIR,
    normalize_symbol_name,
    get_model_config
)
from .data_loader import load_ohlcv_range
from .orderflow_aggregator import build_orderflow_features_range
from .trainer import train_model
from .evaluator import backtest_out_of_sample
from .predict import Predictor


def run_pipeline(
    symbol: str = "TRUMPUSDT",
    start_date: str = "2026-06-01",
    end_date: str = "2026-08-31",
    horizon_bars: Optional[int] = None,
    tp_atr_mult: Optional[float] = None,
    sl_atr_mult: Optional[float] = None,
    confidence_thresh: Optional[float] = None,
    confidence_thresh_sell: Optional[float] = None,
    auto_download: bool = True,
    run_sweep: bool = True
):
    # Retrieve calibrated symbol configuration baseline
    cfg = get_model_config(symbol)
    cfg.start_date = start_date
    cfg.end_date = end_date

    # Apply overrides if explicitly provided
    if horizon_bars is not None:
        cfg.horizon_bars = horizon_bars
    if tp_atr_mult is not None:
        cfg.tp_atr_mult = tp_atr_mult
        cfg.label_tp_mult = tp_atr_mult
    if sl_atr_mult is not None:
        cfg.sl_atr_mult = sl_atr_mult
        cfg.label_sl_mult = sl_atr_mult
    if confidence_thresh is not None:
        cfg.confidence_threshold = confidence_thresh
    if confidence_thresh_sell is not None:
        cfg.confidence_threshold_sell = confidence_thresh_sell

    print("=" * 80)
    print(f"[ML] 1-MINUTE ALPHA ENGINE: {cfg.symbol}")
    print(f"   Calendar Window      : {start_date} to {end_date} (Train: June–July | Test: August)")
    print(f"   Prediction Horizon   : {cfg.horizon_bars} bars (1m)")
    print(f"   Dynamic Risk Barriers: TP={cfg.tp_atr_mult}x ATR, SL={cfg.sl_atr_mult}x ATR")
    print(f"   Confidence Trigger   : BUY={cfg.confidence_threshold:.0%}, SELL={cfg.confidence_threshold_sell:.0%}")
    print(f"   Embargo Window       : {cfg.embargo_bars} bars (zero calendar leakage)")
    print("=" * 80)

    # 1. Ingestion: OHLCV 1m
    print("\n[Step 1/5] Ingesting 1-minute OHLCV candles...")
    df_ohlcv = load_ohlcv_range(cfg.symbol, start_date, end_date, auto_download=auto_download)

    # 2. Ingestion: Tick Trades Order Flow
    print("\n[Step 2/5] Ingesting & aggregating Tick Trades order-flow microstructure...")
    df_of = build_orderflow_features_range(cfg.symbol, start_date, end_date, auto_download=auto_download)
    if not df_of.empty:
        print(f"[+] Successfully integrated {len(df_of):,} 1m order-flow bars (CVD, taker flow, whale ratio).")
    else:
        print("[!] Note: Raw tick trades not found or downloaded; utilizing native OHLCV taker flow as baseline.")

    # 3. Model Training
    print("\n[Step 3/5] Training Multi-Task ML Model (Strict Purged Calendar Split)...")
    model, train_df, test_df, train_metrics = train_model(df_ohlcv, df_of, cfg)

    # 4. Out-of-Sample Backtesting on Baseline (2 ticks slippage)
    print("\n[Step 4/5] Executing Out-of-Sample Financial Backtest on August 1–31...")
    oos_metrics, df_trades, md_report = backtest_out_of_sample(model, test_df, cfg)

    # Friction matrix sweep if requested
    friction_results = []
    if run_sweep:
        print("\n--- Running Slippage Friction Sensitivity Sweep (1.0, 2.0, 3.0, 5.0 ticks) ---")
        for s_ticks in [1.0, 2.0, 3.0, 5.0]:
            sweep_cfg = copy.copy(cfg)
            sweep_cfg.slippage_ticks = s_ticks
            res_m, _, _ = backtest_out_of_sample(model, test_df, sweep_cfg, write_report=False)
            friction_results.append({
                "slippage_ticks": s_ticks,
                "trades": res_m["total_trades"],
                "win_rate_pct": res_m["win_rate_pct"],
                "profit_factor": res_m["profit_factor"],
                "net_pnl_pct": res_m["total_pnl_pct"],
                "sharpe_daily": res_m["sharpe_ratio_daily"],
                "sortino_daily": res_m["sortino_ratio_daily"],
                "max_dd_pct": res_m["max_drawdown_pct"],
                "t_stat": res_m["t_statistic"],
                "p_val": res_m["p_value_two_tailed"],
                "binom_p": res_m["binom_p_value"]
            })

    # Append Friction Sensitivity Matrix to markdown report
    if friction_results:
        report_path = os.path.join(REPORTS_DIR, f"{cfg.symbol.lower()}_oos_report.md")
        if os.path.exists(report_path):
            with open(report_path, "a", encoding="utf-8") as f:
                f.write("\n\n---\n\n## 🧪 Slippage Friction Sensitivity Matrix\n\n")
                f.write("| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
                for row in friction_results:
                    f.write(f"| **{row['slippage_ticks']:.1f} ticks** | `{row['trades']}` | `{row['win_rate_pct']:.1f}%` | **`{row['profit_factor']:.2f}`** | **`{row['net_pnl_pct']:+.1f}%`** | `{row['sharpe_daily']:.2f}` | `{row['max_dd_pct']:.1f}%` | `{row['t_stat']:.2f} (p={row['p_val']:.3f})` | `{row['binom_p']:.4f}` |\n")

    # Save metrics JSON
    metrics_bundle = {
        "symbol": cfg.symbol,
        "config": {
            "horizon_bars": cfg.horizon_bars,
            "tp_atr_mult": cfg.tp_atr_mult,
            "sl_atr_mult": cfg.sl_atr_mult,
            "confidence_threshold": cfg.confidence_threshold,
            "confidence_threshold_sell": cfg.confidence_threshold_sell,
            "min_profit_pct": cfg.min_profit_pct,
            "taker_fee": cfg.taker_fee,
            "leverage": cfg.leverage,
            "embargo_bars": cfg.embargo_bars
        },
        "train_metrics": train_metrics,
        "oos_metrics": oos_metrics,
        "friction_matrix": friction_results
    }
    metrics_path = os.path.join(REPORTS_DIR, f"{cfg.symbol.lower()}_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_bundle, f, indent=2)

    # 5. Generate Sample Real-Time Signal with Warmup Protection
    print("\n[Step 5/5] Generating Latest Market Recommendation (300 bars warmup)...")
    predictor = Predictor(symbol=cfg.symbol)
    warmup_n = min(300, len(df_ohlcv))
    sample_signal = predictor.predict_from_dataframe(
        df_ohlcv.tail(warmup_n),
        df_of.tail(warmup_n) if not df_of.empty else None
    )

    print("\n" + "=" * 80)
    print(f"[METRICS] OUT-OF-SAMPLE BACKTEST RESULTS: {cfg.symbol} (AUGUST 1–31, 2026)")
    print("=" * 80)
    print(f"Total Trades Taken  : {oos_metrics['total_trades']:,}")
    print(f"Win Rate            : {oos_metrics['win_rate_pct']}% (Breakeven: {oos_metrics['breakeven_win_rate_pct']}%)")
    print(f"Profit Factor       : {oos_metrics['profit_factor']}")
    print(f"Total Net PnL       : {oos_metrics['total_pnl_pct']}%")
    print(f"Max Drawdown        : {oos_metrics['max_drawdown_pct']}%")
    print(f"Daily Sharpe Ratio  : {oos_metrics['sharpe_ratio_daily']}")
    print(f"Daily Sortino Ratio : {oos_metrics['sortino_ratio_daily']}")
    print(f"t-statistic (p-val) : {oos_metrics['t_statistic']} (p={oos_metrics['p_value_two_tailed']})")
    print(f"Binomial p-value    : {oos_metrics['binom_p_value']}")
    print(f"Long Trades         : {oos_metrics['long_trades']} (WR: {oos_metrics['long_win_rate_pct']}%, PnL: ${oos_metrics['long_pnl_usd']:+,.2f})")
    print(f"Short Trades        : {oos_metrics['short_trades']} (WR: {oos_metrics['short_win_rate_pct']}%, PnL: ${oos_metrics['short_pnl_usd']:+,.2f})")
    print("=" * 80)

    if friction_results:
        print("\n" + "=" * 80)
        print(f"[FRICTION MATRIX] SLIPPAGE SENSITIVITY SWEEP: {cfg.symbol}")
        print("=" * 80)
        print(f"{'Slippage':<10} | {'Trades':<8} | {'Win Rate':<10} | {'Profit Factor':<14} | {'Net PnL':<10} | {'Daily Sharpe':<13} | {'Max DD':<10} | {'t-stat (p-val)':<16} | {'Binom p':<8}")
        print("-" * 110)
        for row in friction_results:
            print(f"{row['slippage_ticks']:<4.1f} ticks | {row['trades']:<8d} | {row['win_rate_pct']:<8.1f}% | {row['profit_factor']:<14.2f} | {row['net_pnl_pct']:<+9.1f}% | {row['sharpe_daily']:<13.2f} | {row['max_dd_pct']:<9.1f}% | {row['t_stat']:>5.2f} (p={row['p_val']:.3f}) | {row['binom_p']:<8.4f}")
        print("=" * 80)

    print("\n" + "=" * 80)
    print(f"[SIGNAL] LATEST RECOMMENDATION FOR REAL-TIME TRADING: {cfg.symbol}")
    print("=" * 80)
    print(f"Action              : {sample_signal['action']} (Confidence: {sample_signal['confidence']:.1%})")
    print(f"Current Price       : {sample_signal['current_price']}")
    print(f"Suggested TP Price  : {sample_signal['dynamic_risk_management']['suggested_tp_price']} ({sample_signal['dynamic_risk_management']['tp_ticks_pu']} ticks pu)")
    print(f"Suggested SL Price  : {sample_signal['dynamic_risk_management']['suggested_sl_price']} ({sample_signal['dynamic_risk_management']['sl_ticks_pu']} ticks pu)")
    print(f"Risk:Reward Ratio   : {sample_signal['dynamic_risk_management']['risk_reward_ratio']}")
    print("=" * 80)
    print(f"\n[+] Full reports and artifacts generated in: {REPORTS_DIR}")

    return metrics_bundle


def main():
    parser = argparse.ArgumentParser(description="Master ML 1-Minute Crypto Futures Pipeline")
    parser.add_argument("--symbol", type=str, default="TRUMPUSDT", help="Trading Symbol (TRUMPUSDT, DOGEUSDT)")
    parser.add_argument("--start", type=str, default="2026-06-01", help="Start Date YYYY-MM-DD")
    parser.add_argument("--end", type=str, default="2026-08-31", help="End Date YYYY-MM-DD")
    parser.add_argument("--horizon", type=int, default=None, help="Forward horizon bars")
    parser.add_argument("--tp-mult", type=float, default=None, help="Take-Profit ATR multiplier")
    parser.add_argument("--sl-mult", type=float, default=None, help="Stop-Loss ATR multiplier")
    parser.add_argument("--confidence", type=float, default=None, help="BUY Confidence threshold")
    parser.add_argument("--confidence-sell", type=float, default=None, help="SELL Confidence threshold")
    parser.add_argument("--no-auto-download", action="store_true", help="Disable automatic download from Binance Vision")
    parser.add_argument("--no-sweep", action="store_true", help="Disable slippage sensitivity sweep")

    args = parser.parse_args()

    run_pipeline(
        symbol=args.symbol,
        start_date=args.start,
        end_date=args.end,
        horizon_bars=args.horizon,
        tp_atr_mult=args.tp_mult,
        sl_atr_mult=args.sl_mult,
        confidence_thresh=args.confidence,
        confidence_thresh_sell=args.confidence_sell,
        auto_download=not args.no_auto_download,
        run_sweep=not args.no_sweep
    )


if __name__ == "__main__":
    main()
