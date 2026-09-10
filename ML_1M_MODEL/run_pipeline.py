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
import json
import argparse
import datetime

from .config import (
    ModelConfig,
    MODELS_DIR,
    REPORTS_DIR,
    normalize_symbol_name,
)
from .data_loader import load_ohlcv_range
from .orderflow_aggregator import build_orderflow_features_range
from .trainer import train_model
from .evaluator import backtest_out_of_sample
from .predict import Predictor


def run_pipeline(
    symbol: str = "TRUMPUSDT",
    start_date: str = "2026-01-01",
    end_date: str = "2026-08-31",
    horizon_bars: int = 10,
    tp_atr_mult: float = 2.0,
    sl_atr_mult: float = 1.2,
    confidence_thresh: float = 0.55,
    auto_download: bool = True
):
    print("=" * 70)
    print(f"🚀 ML 1-MINUTE ALPHA ENGINE: {symbol.upper()}")
    print(f"   Date Range: {start_date} to {end_date}")
    print(f"   Prediction Horizon: {horizon_bars} bars (1m)")
    print(f"   Dynamic Risk Barriers: TP={tp_atr_mult}x ATR, SL={sl_atr_mult}x ATR")
    print(f"   Confidence Trigger: {confidence_thresh:.0%}")
    print("=" * 70)

    cfg = ModelConfig(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        horizon_bars=horizon_bars,
        tp_atr_mult=tp_atr_mult,
        sl_atr_mult=sl_atr_mult,
        confidence_threshold=confidence_thresh
    )

    # 1. Ingestion: OHLCV 1m
    print("\n[Step 1/5] Ingesting 1-minute OHLCV candles...")
    df_ohlcv = load_ohlcv_range(symbol, start_date, end_date, auto_download=auto_download)

    # 2. Ingestion: Tick Trades Order Flow
    print("\n[Step 2/5] Ingesting & aggregating Tick Trades order-flow microstructure...")
    df_of = build_orderflow_features_range(symbol, start_date, end_date, auto_download=auto_download)
    if not df_of.empty:
        print(f"[+] Successfully integrated {len(df_of):,} 1m order-flow bars (CVD, taker flow, whale ratio).")
    else:
        print("[!] Note: Raw tick trades not found or downloaded; utilizing native OHLCV taker flow as baseline.")

    # 3. Model Training
    print("\n[Step 3/5] Training Multi-Task ML Model (Purged Walk-Forward)...")
    model, train_df, test_df, train_metrics = train_model(df_ohlcv, df_of, cfg)

    # 4. Out-of-Sample Backtesting
    print("\n[Step 4/5] Executing Out-of-Sample Financial Backtest...")
    oos_metrics, df_trades, md_report = backtest_out_of_sample(model, test_df, cfg)

    # Save metrics JSON
    metrics_bundle = {
        "symbol": symbol,
        "config": {
            "horizon_bars": cfg.horizon_bars,
            "tp_atr_mult": cfg.tp_atr_mult,
            "sl_atr_mult": cfg.sl_atr_mult,
            "confidence_threshold": cfg.confidence_threshold,
            "taker_fee": cfg.taker_fee,
            "leverage": cfg.leverage
        },
        "train_metrics": train_metrics,
        "oos_metrics": oos_metrics
    }
    metrics_path = os.path.join(REPORTS_DIR, f"{symbol.lower()}_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_bundle, f, indent=2)

    # 5. Generate Sample Real-Time Signal
    print("\n[Step 5/5] Generating Latest Market Recommendation...")
    predictor = Predictor(symbol=symbol)
    sample_signal = predictor.predict_from_dataframe(df_ohlcv.tail(120), df_of.tail(120) if not df_of.empty else None)

    print("\n" + "=" * 70)
    print("📈 OUT-OF-SAMPLE BACKTEST RESULTS:")
    print("=" * 70)
    print(f"Total Trades Taken  : {oos_metrics['total_trades']:,}")
    print(f"Win Rate            : {oos_metrics['win_rate_pct']}%")
    print(f"Profit Factor       : {oos_metrics['profit_factor']}")
    print(f"Total Net PnL       : {oos_metrics['total_pnl_pct']}%")
    print(f"Max Drawdown        : {oos_metrics['max_drawdown_pct']}%")
    print(f"Sharpe Ratio        : {oos_metrics['sharpe_ratio']}")
    print(f"Sortino Ratio       : {oos_metrics['sortino_ratio']}")
    print(f"Expectancy / Trade  : ${oos_metrics['expectancy_usd']}")
    print(f"Signal Distribution : BUY={oos_metrics['signal_share_buy_pct']}%, SELL={oos_metrics['signal_share_sell_pct']}%, WAIT={oos_metrics['signal_share_wait_pct']}%")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("🎯 LATEST RECOMMENDATION FOR REAL-TIME TRADING:")
    print("=" * 70)
    print(f"Action              : {sample_signal['action']} (Confidence: {sample_signal['confidence']:.1%})")
    print(f"Current Price       : {sample_signal['current_price']}")
    print(f"Suggested TP Price  : {sample_signal['dynamic_risk_management']['suggested_tp_price']} ({sample_signal['dynamic_risk_management']['tp_ticks_pu']} ticks pu)")
    print(f"Suggested SL Price  : {sample_signal['dynamic_risk_management']['suggested_sl_price']} ({sample_signal['dynamic_risk_management']['sl_ticks_pu']} ticks pu)")
    print(f"Risk:Reward Ratio   : {sample_signal['dynamic_risk_management']['risk_reward_ratio']}")
    print(f"Microstructure      : Taker Buy={sample_signal['market_microstructure']['taker_buy_ratio']:.0%}, Regime={sample_signal['market_microstructure']['volatility_regime']}")
    print("=" * 70)
    print(f"\n[+] Full reports and artifacts generated in: {REPORTS_DIR}")

    return metrics_bundle


def main():
    parser = argparse.ArgumentParser(description="Master ML 1-Minute Crypto Futures Pipeline")
    parser.add_argument("--symbol", type=str, default="TRUMPUSDT", help="Trading Symbol (TRUMPUSDT, DOGEUSDT)")
    parser.add_argument("--start", type=str, default="2026-01-01", help="Start Date YYYY-MM-DD")
    parser.add_argument("--end", type=str, default="2026-08-31", help="End Date YYYY-MM-DD")
    parser.add_argument("--horizon", type=int, default=10, help="Forward horizon bars")
    parser.add_argument("--tp-mult", type=float, default=2.0, help="Take-Profit ATR multiplier")
    parser.add_argument("--sl-mult", type=float, default=1.2, help="Stop-Loss ATR multiplier")
    parser.add_argument("--confidence", type=float, default=0.55, help="Confidence threshold")
    parser.add_argument("--no-auto-download", action="store_true", help="Disable automatic download from Binance Vision")

    args = parser.parse_args()

    run_pipeline(
        symbol=args.symbol,
        start_date=args.start,
        end_date=args.end,
        horizon_bars=args.horizon,
        tp_atr_mult=args.tp_mult,
        sl_atr_mult=args.sl_mult,
        confidence_thresh=args.confidence,
        auto_download=not args.no_auto_download
    )


if __name__ == "__main__":
    main()
