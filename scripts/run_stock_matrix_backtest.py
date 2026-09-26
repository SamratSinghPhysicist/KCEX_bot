"""
Distributed Stock Matrix Backtesting Worker
============================================
Executes institutional Order Book + Demand/Supply Block Strategy backtests
across US Equities (crypto-equivalent pairs) for multiple timeframes,
fee tiers, and adverse tick slippages.

Designed for GitHub Actions parallel runners and local multi-core execution.

Features:
- Automated OHLCV data retrieval from Yahoo Finance with disk caching.
- Handles timeframes: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d.
- Automated timeframe resampling (1m -> 3m, 1h -> 4h).
- Strict US Regular Market Hours gating (09:30 - 16:00 ET Mon-Fri).
- 3 Fee Schedules:
    * Tier 1: 0% maker, 0.01% taker (net 0.02% round-trip)
    * Tier 2: 0.02% maker, 0.05% taker (net 0.10% round-trip)
    * Tier 3: 0.10% maker, 0.10% taker (net 0.20% round-trip)
- 7 Adverse Slippage Settings: 1, 2, 3, 4, 5, 6, 7 ticks.
- Full output artifacts:
    * Detailed Trades CSV for every parameter set
    * Summary JSON for every parameter set
    * Stock Consolidated Matrix CSV and JSON
"""

from __future__ import annotations
import os
import sys
import csv
import json
import time
import math
import argparse
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple

# Reconfigure stdout for utf-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol, format_ms_to_utc
from BACKTESTER.engine.data_loader import Candle, normalize_timeframe
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator, PerformanceSummary
from BACKTESTER.stock_data_downloader import (
    get_cached_or_download_stock_candles,
    resolve_stock_ticker,
    TOP_50_US_STOCKS
)
from kcex.market import ContractInfo


# ---------------------------------------------------------------------------
# Stock Batches for GitHub Actions Parallel Partitioning
# ---------------------------------------------------------------------------

STOCK_BATCHES: Dict[str, List[str]] = {
    "BATCH_1": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL", "ADBE"],
    "BATCH_2": ["BRK-B", "JPM", "V", "MA", "BAC", "WFC", "GS", "BKNG", "CSCO", "TXN"],
    "BATCH_3": ["LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO", "ISRG", "WMT", "PG", "COST"],
    "BATCH_4": ["HD", "NFLX", "CRM", "CVX", "XOM", "KO", "PEP", "DIS", "PM", "CAT"],
    "BATCH_5": ["AMD", "QCOM", "AMAT", "INTC", "IBM", "NOW", "PLTR", "GE", "LIN", "VZ"],
}

ALL_TIMEFRAMES: List[str] = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"]

FEE_TIERS: Dict[str, Dict[str, Any]] = {
    "tier1": {
        "label": "tier1_0m_0.01t",
        "description": "0% Maker / 0.01% Taker (0.02% Net RT)",
        "maker_fee": 0.0,
        "taker_fee": 0.0001,
        "round_trip_fee_pct": 0.02
    },
    "tier2": {
        "label": "tier2_0.02m_0.05t",
        "description": "0.02% Maker / 0.05% Taker (0.10% Net RT)",
        "maker_fee": 0.0002,
        "taker_fee": 0.0005,
        "round_trip_fee_pct": 0.10
    },
    "tier3": {
        "label": "tier3_0.1m_0.1t",
        "description": "0.10% Maker / 0.10% Taker (0.20% Net RT)",
        "maker_fee": 0.0010,
        "taker_fee": 0.0010,
        "round_trip_fee_pct": 0.20
    }
}

SLIPPAGE_TICKS_LIST: List[int] = [1, 2, 3, 4, 5, 6, 7]


def build_stock_contract(ticker: str, sample_price: float = 150.0) -> ContractInfo:
    """
    Constructs faithful KCEX ContractInfo specification for a US equity equivalent pair.
    KCEX stock tokens feature: cs=0.01 (or 0.001 for high priced stocks), pu=0.01 ($0.01 tick),
    min_volume=1, max_leverage=25.
    """
    sym = f"{ticker}_USDT"
    cs = 0.001 if sample_price >= 500.0 else 0.01
    return ContractInfo(
        symbol=sym,
        base_coin=ticker,
        quote_coin="USDT",
        contract_size=cs,
        price_unit=0.01,
        volume_unit=1.0,
        price_precision=2,
        volume_precision=0,
        min_volume=1.0,
        max_volume=100000.0,
        min_leverage=1,
        max_leverage=25,
        maintenance_margin_ratio=0.02,
        initial_margin_ratio=0.04,
        maker_fee_rate=0.0,
        taker_fee_rate=0.0001,
        depth_steps=["0.01"],
        raw_data={}
    )


def run_single_stock_scenario(
    ticker: str,
    timeframe: str,
    candles: List[Candle],
    fee_tier_key: str,
    fee_spec: Dict[str, Any],
    slippage_ticks: int,
    leverage: int = 15,
    margin_pct: float = 10.0,
    capital: float = 100.0,
    output_dir: str = "stock_artifacts",
    export_trades_csv: bool = True
) -> Dict[str, Any]:
    """
    Executes one backtest combination for a pre-loaded list of candles.
    Writes trades CSV and returns structured summary metrics.
    """
    norm_tf = normalize_timeframe(timeframe)
    canonical = f"{ticker}_USDT"
    fee_label = fee_spec["label"]

    maker_fee = fee_spec["maker_fee"]
    taker_fee = fee_spec["taker_fee"]

    # 1. Configure Market
    market = BacktestMarket(
        fee_mode="MANUAL",
        maker_fee_override=maker_fee,
        taker_fee_override=taker_fee
    )
    sample_p = candles[-1].close if candles else 150.0
    contract = build_stock_contract(ticker, sample_price=sample_p)
    market._contracts[canonical] = contract
    market.register_candles(canonical, norm_tf, candles)

    # 2. Configure Backtest Engine
    config = BacktestConfig(
        symbol=canonical,
        timeframe=norm_tf,
        strategy_mode="ORDER_BLOCK_DEMAND",
        volume_mode="MARGIN_PCT",
        margin_pct=margin_pct,
        leverage=leverage,
        initial_balance_usdt=capital,
        fee_mode="MANUAL",
        maker_fee_override=maker_fee,
        taker_fee_override=taker_fee,
        slippage_enabled=True,
        slippage_ticks=slippage_ticks,
        risk_reward_ratio=2.0,
        pivot_len=5,
        use_tick_data=False,
        us_market_hours_filter_enabled=True
    )

    t_start = time.time()
    engine = BacktestExecutionEngine(config=config, market=market)
    outcomes = engine.run(preloaded_candles=candles, preloaded_sub_candles_1m=[])
    runtime_sec = time.time() - t_start

    # 3. Calculate Performance Metrics
    summary: PerformanceSummary = PerformanceCalculator.calculate(
        outcomes=outcomes,
        initial_balance_usdt=capital,
        inr_rate=94.45
    )

    timespan_days = max(1.0, (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000 * 86400))
    monthly_freq = round(len(outcomes) / (timespan_days / 30.4375), 2) if timespan_days > 0 else 0.0

    # 4. Export Detailed Trades CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_filename = f"trades_{ticker}_{norm_tf}_{fee_label}_slip{slippage_ticks}t.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    if export_trades_csv:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "trade_id", "entry_time_utc", "exit_time_utc", "symbol", "direction",
                "entry_price", "exit_price", "contracts", "margin_usdt",
                "gross_pnl_usdt", "fee_open_usdt", "fee_close_usdt", "total_fee_usdt",
                "net_pnl_usdt", "roe_pct", "exit_reason", "duration_seconds", "wallet_balance_usdt"
            ])
            running_bal = capital
            for o in outcomes:
                running_bal += o.realized_pnl_usdt
                open_ts = getattr(o, "open_time", 0.0)
                close_ts = getattr(o, "close_time", 0.0)
                e_str = datetime.fromtimestamp(open_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if open_ts > 0 else ""
                x_str = datetime.fromtimestamp(close_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if close_ts > 0 else ""
                exit_r = o.exit_reason.value if hasattr(o.exit_reason, "value") else str(o.exit_reason)
                f_open = round(getattr(o, "fee_open_usdt", 0.0), 5)
                f_close = round(getattr(o, "fee_close_usdt", 0.0), 5)
                f_total = round(getattr(o, "fee_total_usdt", 0.0), 5)
                net_pnl = round(o.realized_pnl_usdt, 4)
                gross_pnl = round(net_pnl + f_total, 4)
                writer.writerow([
                    o.trade_id, e_str, x_str, o.symbol,
                    o.direction.value if hasattr(o.direction, "value") else str(o.direction),
                    o.entry_price, o.exit_price, getattr(o, "vol_contracts", 1),
                    round(getattr(o, "margin_used_usdt", 0.0), 2),
                    gross_pnl, f_open, f_close, f_total, net_pnl,
                    round(getattr(o, "roe_percentage", 0.0), 2), exit_r,
                    round(o.duration_seconds, 1), round(running_bal, 2)
                ])

    # 5. Build Result Dictionary
    result_data: Dict[str, Any] = {
        "stock": ticker,
        "symbol": canonical,
        "timeframe": norm_tf,
        "fee_tier": fee_tier_key,
        "fee_label": fee_label,
        "maker_fee": maker_fee,
        "taker_fee": taker_fee,
        "round_trip_fee_pct": fee_spec["round_trip_fee_pct"],
        "slippage_ticks": slippage_ticks,
        "leverage": leverage,
        "margin_pct": margin_pct,
        "initial_capital_usdt": capital,
        "final_balance_usdt": round(summary.final_balance_usdt, 2),
        "net_pnl_usdt": round(summary.net_pnl_usdt, 2),
        "net_roi_pct": round(summary.net_roi_pct, 2),
        "total_trades": summary.total_trades,
        "winning_trades": summary.winning_trades,
        "losing_trades": summary.losing_trades,
        "win_rate_pct": round(summary.win_rate_pct, 2),
        "profit_factor": round(summary.profit_factor, 2) if not math.isinf(summary.profit_factor) else 999.0,
        "max_drawdown_pct": round(summary.max_drawdown_pct, 2),
        "max_drawdown_usdt": round(summary.max_drawdown_usdt, 2),
        "sharpe_ratio": round(summary.sharpe_ratio, 2),
        "sortino_ratio": round(summary.sortino_ratio, 2),
        "calmar_ratio": round(summary.calmar_ratio, 2),
        "total_fees_usdt": round(summary.total_fees_usdt, 4),
        "monthly_trades": monthly_freq,
        "candles_count": len(candles),
        "timespan_days": round(timespan_days, 1),
        "runtime_seconds": round(runtime_sec, 2),
        "trades_csv_path": csv_filename
    }

    # Export Individual Summary JSON
    json_filename = f"summary_{ticker}_{norm_tf}_{fee_label}_slip{slippage_ticks}t.json"
    json_path = os.path.join(output_dir, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2)

    return result_data


def run_stock_full_matrix(
    ticker: str,
    timeframes: List[str],
    fee_keys: List[str],
    slippage_ticks_list: List[int],
    leverage: int = 15,
    margin_pct: float = 10.0,
    capital: float = 100.0,
    output_dir: str = "stock_artifacts",
    data_dir: str = "BACKTESTER/OHLCV_Data_Stocks",
    lookback_years: float = 15.0
) -> List[Dict[str, Any]]:
    """
    Executes full matrix for a single stock.
    Pre-downloads / loads each timeframe once, then sweeps across all fee tiers and slippages.
    """
    norm_ticker = resolve_stock_ticker(ticker)
    print(f"\n{'=' * 80}")
    print(f"🏛️ RUNNING STOCK MATRIX WORKER: {norm_ticker}")
    print(f"   Timeframes ({len(timeframes)}): {', '.join(timeframes)}")
    print(f"   Fee Tiers ({len(fee_keys)}):   {', '.join(fee_keys)}")
    print(f"   Slippages ({len(slippage_ticks_list)}):   {slippage_ticks_list} ticks")
    print(f"   Total Combinations:        {len(timeframes) * len(fee_keys) * len(slippage_ticks_list)}")
    print(f"{'=' * 80}\n")

    stock_results: List[Dict[str, Any]] = []

    for tf in timeframes:
        t_load = time.time()
        candles = get_cached_or_download_stock_candles(
            ticker=norm_ticker,
            timeframe=tf,
            data_dir=data_dir,
            lookback_years=lookback_years
        )
        if not candles or len(candles) < 30:
            print(f"[!] Warning: Insufficient candles for {norm_ticker} [{tf}] ({len(candles) if candles else 0} bars). Skipping.")
            continue

        print(f"[+] Loaded {len(candles)} candles for {norm_ticker} [{tf}] in {time.time() - t_load:.2f}s. Sweeping parameter grid...")

        for fee_key in fee_keys:
            fee_spec = FEE_TIERS[fee_key]
            for slip in slippage_ticks_list:
                res = run_single_stock_scenario(
                    ticker=norm_ticker,
                    timeframe=tf,
                    candles=candles,
                    fee_tier_key=fee_key,
                    fee_spec=fee_spec,
                    slippage_ticks=slip,
                    leverage=leverage,
                    margin_pct=margin_pct,
                    capital=capital,
                    output_dir=output_dir,
                    export_trades_csv=True
                )
                stock_results.append(res)

        print(f"    Completed {len(fee_keys) * len(slippage_ticks_list)} backtests for {norm_ticker} [{tf}].")

    # Save Stock Matrix Summary CSV & JSON
    if stock_results:
        matrix_csv = os.path.join(output_dir, f"matrix_{norm_ticker}.csv")
        fieldnames = list(stock_results[0].keys())
        with open(matrix_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in stock_results:
                writer.writerow(r)

        matrix_json = os.path.join(output_dir, f"matrix_{norm_ticker}.json")
        with open(matrix_json, "w", encoding="utf-8") as f:
            json.dump(stock_results, f, indent=2)

        print(f"\n[+] Stock Matrix Finished for {norm_ticker}: {len(stock_results)} scenarios executed.")
        print(f"    Consolidated CSV: {matrix_csv}")
        print(f"    Consolidated JSON: {matrix_json}\n")

    return stock_results


def resolve_stock_list(target: str) -> List[str]:
    """Resolves CLI stock argument into a list of stock tickers."""
    cleaned = target.strip().upper()
    if cleaned == "ALL":
        return list(TOP_50_US_STOCKS)
    if cleaned in STOCK_BATCHES:
        return list(STOCK_BATCHES[cleaned])
    # Check comma-separated list
    items = [resolve_stock_ticker(s.strip()) for s in cleaned.split(",") if s.strip()]
    return items


def main():
    parser = argparse.ArgumentParser(description="Distributed Stock Matrix Backtesting Worker")
    parser.add_argument("--stock", "--stocks", "--ticker", type=str, required=True,
                        help="Target stock(s): 'AAPL', 'AAPL,MSFT,NVDA', 'BATCH_1'..'BATCH_5', or 'ALL'")
    parser.add_argument("--timeframes", "--tf", type=str, default="ALL",
                        help="Timeframes: 'ALL' or comma-separated e.g. '1m,3m,5m,15m,30m,1h,4h,1d'")
    parser.add_argument("--fees", type=str, default="ALL",
                        help="Fee tiers: 'ALL' or comma-separated e.g. 'tier1,tier2,tier3'")
    parser.add_argument("--slippages", type=str, default="ALL",
                        help="Slippages in ticks: 'ALL' (1,2,3,4,5,6,7) or comma-separated e.g. '1,2,3'")
    parser.add_argument("--leverage", type=int, default=15, help="Isolated leverage multiplier (default: 15)")
    parser.add_argument("--margin-pct", type=float, default=10.0, help="Margin compounding percentage (default: 10.0)")
    parser.add_argument("--capital", type=float, default=100.0, help="Initial capital in USDT (default: 100.0)")
    parser.add_argument("--lookback-years", type=float, default=15.0, help="Max lookback years for daily bars (default: 15.0)")
    parser.add_argument("--output-dir", type=str, default="stock_artifacts", help="Output directory for artifacts")
    parser.add_argument("--data-dir", type=str, default="BACKTESTER/OHLCV_Data_Stocks", help="Data directory cache")

    args = parser.parse_args()

    # 1. Resolve stocks
    stocks = resolve_stock_list(args.stock)
    if not stocks:
        print(f"[!] No valid stocks resolved from target: {args.stock}")
        sys.exit(1)

    # 2. Resolve timeframes
    if args.timeframes.upper() == "ALL":
        tfs = ALL_TIMEFRAMES
    else:
        tfs = [t.strip().lower() for t in args.timeframes.split(",") if t.strip()]

    # 3. Resolve fee tiers
    if args.fees.upper() == "ALL":
        fee_keys = list(FEE_TIERS.keys())
    else:
        fee_keys = [f.strip().lower() for f in args.fees.split(",") if f.strip().lower() in FEE_TIERS]

    # 4. Resolve slippages
    if args.slippages.upper() == "ALL":
        slippages = SLIPPAGE_TICKS_LIST
    else:
        slippages = [int(s.strip()) for s in args.slippages.split(",") if s.strip().isdigit()]

    print(f"🚀 Initializing Stock Backtest Worker for {len(stocks)} stocks...")
    print(f"   Stocks:     {', '.join(stocks)}")
    print(f"   Timeframes: {', '.join(tfs)}")
    print(f"   Fees:       {', '.join(fee_keys)}")
    print(f"   Slippages:  {slippages}")

    all_worker_results = []
    t_global_start = time.time()

    for stock in stocks:
        res = run_stock_full_matrix(
            ticker=stock,
            timeframes=tfs,
            fee_keys=fee_keys,
            slippage_ticks_list=slippages,
            leverage=args.leverage,
            margin_pct=args.margin_pct,
            capital=args.capital,
            output_dir=args.output_dir,
            data_dir=args.data_dir,
            lookback_years=args.lookback_years
        )
        all_worker_results.extend(res)

    total_time = time.time() - t_global_start
    print(f"\n🎉 Worker completed all tasks in {total_time:.2f}s! Total backtests: {len(all_worker_results)}")


if __name__ == "__main__":
    main()
