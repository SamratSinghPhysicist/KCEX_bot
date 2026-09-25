"""
High-Performance Batch Backtest Runner for Fee Coverage + 2 Ticks OB Experiment
================================================================================
Executes exhaustive parameter sweeps (Timeframes, Fee Tiers, Slippage) across
multiple cryptocurrency and commodity assets using the Order Block + Demand strategy
with Take Profit set to Fee Coverage + 2 Ticks and Stop Loss anchored to the OB boundary.

Features:
1. Strict OHLCV candle execution without tick data (no ticker/tick streamer).
2. Chronological 1m sub-candle disambiguation for simultaneous TP & SL hits.
   If TP and SL hit within the same 1m candle, declares Stop Loss Hit.
3. Detailed outputs:
   - Batch matrix CSV
   - Detailed trade-by-trade CSV
   - Markdown summary reports with performance analytics
4. Distributed chunk execution and master consolidation for GitHub Actions workers.
"""

from __future__ import annotations
import os
import sys
import glob
import time
import json
import csv
import argparse
import datetime
from typing import List, Dict, Any, Optional, Tuple

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is in sys.path
EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.ob_fee_plus_2ticks_experiment.strategy import (
    FeePlus2TicksOBStrategy,
    compute_fee_coverage_ticks
)
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol, format_ms_to_utc, parse_timestamp_ms
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.data_loader import OHLCVLoader, normalize_timeframe, timeframe_to_kcex_interval
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator, PerformanceSummary
from BACKTESTER.engine.downloader import ensure_market_data
from kcex.engine.strategy import MasterplanStrategy

DEFAULT_ASSETS = [
    "BTC_USDT",
    "TRUMP_USDT",
    "1000000MOG_USDT",
    "DOGE_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XAU_USDT",
    "XAG_USDT",
    "CL_USDT",
    "XRP_USDT"
]

# (Label, maker_rate, taker_rate, maker_pct, taker_pct)
FEE_SCHEDULES = [
    ("Maker 0.00% / Taker 0.01%", 0.0000, 0.0001, 0.00, 0.01),
    ("Maker 0.00% / Taker 0.05%", 0.0000, 0.0005, 0.00, 0.05),
    ("Maker 0.10% / Taker 0.10%", 0.0010, 0.0010, 0.10, 0.10),
]

SLIPPAGE_TICKS = [1, 2, 3, 4, 5, 6, 7]
DEFAULT_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]


def run_experiment_for_symbol(
    symbol: str,
    timeframes: List[str],
    fee_schedules: List[Tuple[str, float, float, float, float]],
    slippage_ticks: List[int],
    extra_ticks: int = 2,
    start_date: str = "2026-01-01",
    end_date: str = "2026-08-31",
    capital: float = 100.0,
    leverage: int = 10,
    margin_pct: float = 10.0,
    reports_dir: str = os.path.join(EXPERIMENT_DIR, "reports"),
    base_dir: str = "BACKTESTER",
    tag: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Runs all combinations for a single asset and returns (matrix_results, trade_results)."""
    canonical = canonicalize_symbol(symbol)
    if "MOG" in canonical:
        canonical = "1000000MOG_USDT"
    elif "XAU" in canonical:
        canonical = "XAU_USDT"
    elif "XAG" in canonical:
        canonical = "XAG_USDT"
    elif "CL" in canonical:
        canonical = "CL_USDT"
    elif "XRP" in canonical:
        canonical = "XRP_USDT"

    # Handle asset listing dates on Binance Futures
    effective_start = start_date
    if "CL" in canonical and start_date < "2026-04-01":
        effective_start = "2026-04-01"
        print(f"[*] Note: {canonical} listed on Binance on 2026-04-01. Using start date: {effective_start}")
    elif "XAG" in canonical and start_date < "2026-01-07":
        effective_start = "2026-01-07"
        print(f"[*] Note: {canonical} listed on Binance on 2026-01-07. Using start date: {effective_start}")

    os.makedirs(reports_dir, exist_ok=True)
    loader = OHLCVLoader(data_dir=os.path.join(base_dir, "OHLCV_Data_Binance"))
    start_ms = parse_timestamp_ms(effective_start)
    end_ms = parse_timestamp_ms(end_date)

    matrix_results: List[Dict[str, Any]] = []
    trade_results: List[Dict[str, Any]] = []

    print("\n" + "=" * 80)
    print(f"🚀 INITIATING EXPERIMENT SWEEP: {canonical}")
    print(f"   Strategy:    Order Block + Demand (Fee Coverage + {extra_ticks} Ticks TP)")
    print(f"   Date Range:  {effective_start} to {end_date}")
    print(f"   Data Mode:   Pure OHLCV (No ticker/ticks, 1m sub-candle disambiguation)")
    print(f"   Capital:     ${capital:.2f} | Leverage: {leverage}x | Margin Sizing: {margin_pct}%")
    print(f"   Timeframes:  {', '.join(timeframes)}")
    print(f"   Fees:        {len(fee_schedules)} schedules | Slippages: {slippage_ticks}")
    print(f"   Combos/TF:   {len(fee_schedules) * len(slippage_ticks)}")
    print("=" * 80)

    # Preload 1m sub-candles once for disambiguation of higher timeframes
    sub_1m_candles = None
    needs_sub_1m = any(normalize_timeframe(tf) != "1m" for tf in timeframes)
    if needs_sub_1m:
        print(f"[*] Ensuring 1m sub-candles for {canonical} disambiguation...")
        ensure_market_data(
            symbol=canonical,
            timeframe="1m",
            start_date=effective_start,
            end_date=end_date,
            download_trades=False,
            base_dir=base_dir
        )
        sub_1m_candles = loader.load_candles(
            symbol=canonical,
            timeframe="1m",
            start_ms=start_ms,
            end_ms=end_ms
        )
        print(f"    Loaded {len(sub_1m_candles) if sub_1m_candles else 0} 1m sub-candles for disambiguation.")

    for tf in timeframes:
        norm_tf = normalize_timeframe(tf)
        print(f"\n📂 [{canonical} - {norm_tf.upper()}] Loading OHLCV...")

        # 1. Download / Verify market data
        ensure_market_data(
            symbol=canonical,
            timeframe=norm_tf,
            start_date=effective_start,
            end_date=end_date,
            download_trades=False,
            base_dir=base_dir
        )

        # 2. Load primary candles into memory
        candles = loader.load_candles(
            symbol=canonical,
            timeframe=norm_tf,
            start_ms=start_ms,
            end_ms=end_ms
        )
        if not candles:
            print(f"⚠️  No candle data found for {canonical} {norm_tf}. Skipping timeframe.")
            continue

        print(f"    Successfully loaded {len(candles)} candles. Executing parameter combinations...")

        for fee_lbl, m_rate, t_rate, m_pct, t_pct in fee_schedules:
            for slip in slippage_ticks:
                cfg = BacktestConfig(
                    symbol=canonical,
                    timeframe=norm_tf,
                    strategy_mode="ORDER_BLOCK_DEMAND_FEE_PLUS_2TICKS",
                    start_time=effective_start,
                    end_time=end_date,
                    initial_balance_usdt=capital,
                    leverage=leverage,
                    volume_mode="MARGIN_PCT",
                    margin_pct=margin_pct,
                    execution_style="PURE_MARKET",
                    fee_mode="MANUAL",
                    maker_fee_override=m_rate,
                    taker_fee_override=t_rate,
                    slippage_enabled=True,
                    slippage_ticks=slip,
                    use_tick_data=False,
                    tick_fallback_to_candle=True,
                    ohlcv_data_dir=os.path.join(base_dir, "OHLCV_Data_Binance"),
                    trades_data_dir=os.path.join(base_dir, "Historical_Trades_Data_Binance"),
                    playback_speed=0.0,
                    show_progress=False,
                    verbose_ticks=False
                )

                market = BacktestMarket(
                    inr_rate=cfg.inr_rate,
                    fee_mode="MANUAL",
                    maker_fee_override=m_rate,
                    taker_fee_override=t_rate
                )

                sub_strat = FeePlus2TicksOBStrategy(
                    market=market,
                    symbol=canonical,
                    interval=timeframe_to_kcex_interval(norm_tf),
                    pivot_len=5,
                    extra_ticks=extra_ticks,
                    taker_fee_override=t_rate,
                    auto_start_feed=False
                )

                masterplan = MasterplanStrategy(
                    market=market,
                    config=cfg,
                    sub_strategy=sub_strat
                )

                engine = BacktestExecutionEngine(
                    config=cfg,
                    market=market,
                    strategy=masterplan,
                    ohlcv_loader=loader
                )

                outcomes = engine.run(
                    preloaded_candles=candles,
                    preloaded_sub_candles_1m=sub_1m_candles if norm_tf != "1m" else None
                )

                summary: PerformanceSummary = PerformanceCalculator.calculate(
                    outcomes=outcomes,
                    initial_balance_usdt=capital,
                    inr_rate=cfg.inr_rate
                )

                res_row = {
                    "symbol": canonical,
                    "timeframe": norm_tf,
                    "fee_schedule": fee_lbl,
                    "maker_fee_pct": m_pct,
                    "taker_fee_pct": t_pct,
                    "slippage_ticks": slip,
                    "extra_ticks": extra_ticks,
                    "total_trades": summary.total_trades,
                    "winning_trades": summary.winning_trades,
                    "losing_trades": summary.losing_trades,
                    "win_rate_pct": round(summary.win_rate_pct, 2),
                    "profit_factor": round(summary.profit_factor, 2) if summary.profit_factor < 999 else 999.0,
                    "net_pnl_usdt": round(summary.net_pnl_usdt, 2),
                    "net_roi_pct": round(summary.net_roi_pct, 2),
                    "max_drawdown_pct": round(summary.max_drawdown_pct, 2),
                    "expectancy_usdt": round(summary.avg_trade_pnl_usdt, 4),
                    "total_fees_usdt": round(summary.total_fees_usdt, 2),
                    "final_balance_usdt": round(summary.final_balance_usdt, 2)
                }
                matrix_results.append(res_row)

                # Record individual trade-by-trade outcomes
                for o in outcomes:
                    trade_results.append({
                        "symbol": canonical,
                        "timeframe": norm_tf,
                        "fee_schedule": fee_lbl,
                        "maker_fee_pct": m_pct,
                        "taker_fee_pct": t_pct,
                        "slippage_ticks": slip,
                        "extra_ticks": extra_ticks,
                        "trade_id": o.trade_id,
                        "direction": o.direction.name if hasattr(o.direction, "name") else str(o.direction),
                        "entry_time_utc": format_ms_to_utc(int(o.open_time * 1000)),
                        "exit_time_utc": format_ms_to_utc(int(o.close_time * 1000)),
                        "duration_seconds": round(o.duration_seconds, 1),
                        "entry_price": o.entry_price,
                        "exit_price": o.exit_price,
                        "min_profit_tp_price": o.min_profit_tp_price,
                        "stop_loss_price": o.stop_loss_price,
                        "underlying_quantity": o.underlying_quantity,
                        "vol_contracts": o.vol_contracts,
                        "margin_used_usdt": round(o.margin_used_usdt, 2),
                        "fee_open_usdt": round(o.fee_open_usdt, 4),
                        "fee_close_usdt": round(o.fee_close_usdt, 4),
                        "fee_total_usdt": round(o.fee_total_usdt, 4),
                        "realized_pnl_usdt": round(o.realized_pnl_usdt, 4),
                        "pnl_percentage": round(o.pnl_percentage, 2),
                        "roe_percentage": round(o.roe_percentage, 2),
                        "exit_reason": o.exit_reason.name if hasattr(o.exit_reason, "name") else str(o.exit_reason),
                        "balance_after_trade_usdt": round(o.balance_after_trade_usdt, 2) if o.balance_after_trade_usdt is not None else None
                    })

    # Save Chunk / Worker Files
    suffix = f"_{tag}" if tag else ""
    prefix = os.path.join(reports_dir, f"{canonical}{suffix}")

    # 1. Matrix CSV
    matrix_csv_path = f"{prefix}_batch_matrix.csv"
    if matrix_results:
        with open(matrix_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(matrix_results[0].keys()))
            writer.writeheader()
            writer.writerows(matrix_results)
        print(f"\n[+] Saved Matrix Results CSV: {matrix_csv_path} ({len(matrix_results)} rows)")

    # 2. Detailed Trades CSV
    trades_csv_path = f"{prefix}_trades.csv"
    if trade_results:
        with open(trades_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(trade_results[0].keys()))
            writer.writeheader()
            writer.writerows(trade_results)
        print(f"[+] Saved Detailed Trades CSV: {trades_csv_path} ({len(trade_results)} trades)")
    else:
        # Create empty trades CSV with headers
        empty_headers = [
            "symbol", "timeframe", "fee_schedule", "maker_fee_pct", "taker_fee_pct",
            "slippage_ticks", "extra_ticks", "trade_id", "direction", "entry_time_utc",
            "exit_time_utc", "duration_seconds", "entry_price", "exit_price",
            "min_profit_tp_price", "stop_loss_price", "underlying_quantity",
            "vol_contracts", "margin_used_usdt", "fee_open_usdt", "fee_close_usdt",
            "fee_total_usdt", "realized_pnl_usdt", "pnl_percentage", "roe_percentage",
            "exit_reason", "balance_after_trade_usdt"
        ]
        with open(trades_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(empty_headers)
        print(f"[+] Saved Empty Trades CSV: {trades_csv_path}")

    # 3. Markdown Report
    md_path = f"{prefix}_batch_matrix.md"
    generate_markdown_report(matrix_results, md_path, canonical, tag)
    print(f"[+] Saved Markdown Report: {md_path}")

    return matrix_results, trade_results


def generate_markdown_report(
    results: List[Dict[str, Any]],
    output_path: str,
    symbol: str,
    tag: Optional[str] = None
) -> None:
    """Generates a structured Markdown report from matrix results."""
    lines = [
        f"# Order Block + Demand Strategy Experiment: Fee Coverage + 2 Ticks TP",
        f"**Asset:** `{symbol}`  ",
        f"**Worker / Tag:** `{tag or 'Single Run'}`  ",
        f"**Execution Mode:** Pure OHLCV (1m Sub-Candle Disambiguation)  ",
        f"**Date Generated:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        "",
        "## 1. Experiment Overview & Rationale",
        "- **Base Strategy:** Order Block + Demand Zone (Vivek Yadav Smart Money Concepts).",
        "- **Stop Loss:** Preserved at exact Order Block boundary (+/- buffer ticks).",
        "- **Take Profit:** Dynamic rapid scalp target set at `Fee Coverage Ticks + 2 Ticks`.",
        "- **Partial TP:** Disabled (100% position exits at the fee+2tick target).",
        "- **Disambiguation Rule:** If candle hits both TP and SL, 1m sub-candles verify precedence. If still on same 1m candle, declares Stop Loss Hit.",
        "",
        "## 2. Top Performing Configurations (by Net ROI %)",
        ""
    ]

    if not results:
        lines.append("*No trades or backtest results generated.*")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return

    # Sort by Net ROI % descending
    sorted_res = sorted(results, key=lambda x: x.get("net_roi_pct", 0.0), reverse=True)
    top_5 = sorted_res[:5]

    lines.append("| Rank | Timeframe | Fee Schedule | Slippage | Win Rate | Profit Factor | Net PnL (USDT) | Net ROI % | Max DD % | Trades |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r, row in enumerate(top_5, 1):
        lines.append(
            f"| {r} | **{row['timeframe']}** | {row['fee_schedule']} | {row['slippage_ticks']}t | "
            f"{row['win_rate_pct']:.1f}% | {row['profit_factor']:.2f} | ${row['net_pnl_usdt']:.2f} | "
            f"**{row['net_roi_pct']:+.2f}%** | {row['max_drawdown_pct']:.2f}% | {row['total_trades']} |"
        )

    lines.extend([
        "",
        "## 3. Comprehensive Parameter Sweep Matrix",
        "",
        "| Timeframe | Fee Schedule | Slip | Trades | Win Rate | PF | Net PnL | Net ROI % | Max DD % | Exp (USDT) | Total Fees | Final Balance |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for row in results:
        lines.append(
            f"| {row['timeframe']} | {row['fee_schedule']} | {row['slippage_ticks']}t | "
            f"{row['total_trades']} | {row['win_rate_pct']:.1f}% | {row['profit_factor']:.2f} | "
            f"${row['net_pnl_usdt']:.2f} | {row['net_roi_pct']:+.2f}% | {row['max_drawdown_pct']:.2f}% | "
            f"${row['expectancy_usdt']:.4f} | ${row['total_fees_usdt']:.2f} | ${row['final_balance_usdt']:.2f} |"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def consolidate_reports(reports_dir: str, symbol: Optional[str] = None) -> None:
    """Consolidates all chunk batch matrix and trades CSV files into master reports."""
    print("\n" + "=" * 80)
    print("🔄 CONSOLIDATING EXPERIMENT WORKER ARTIFACTS")
    print(f"   Directory: {reports_dir}")
    print("=" * 80)

    # Find matrix files
    pattern = os.path.join(reports_dir, f"{symbol or '*'}_*_batch_matrix.csv")
    chunk_files = [f for f in glob.glob(pattern) if not f.endswith("_all_batch_matrix.csv") and not f.endswith("_batch_matrix.csv")]
    if not chunk_files:
        # Check all matrix csv files in reports_dir
        chunk_files = [f for f in glob.glob(os.path.join(reports_dir, "*.csv")) if "matrix" in f and not f.endswith("_consolidated.csv")]

    print(f"[*] Found {len(chunk_files)} chunk matrix files.")

    all_matrix: List[Dict[str, Any]] = []
    seen_combos = set()

    for cf in sorted(chunk_files):
        with open(cf, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row.get("symbol"), row.get("timeframe"), row.get("fee_schedule"), row.get("slippage_ticks"))
                if key not in seen_combos:
                    seen_combos.add(key)
                    # Cast floats
                    for num_col in ["win_rate_pct", "profit_factor", "net_pnl_usdt", "net_roi_pct", "max_drawdown_pct", "expectancy_usdt", "total_fees_usdt", "final_balance_usdt"]:
                        if num_col in row and row[num_col]:
                            try:
                                row[num_col] = float(row[num_col])
                            except ValueError:
                                pass
                    for int_col in ["total_trades", "winning_trades", "losing_trades", "slippage_ticks", "extra_ticks"]:
                        if int_col in row and row[int_col]:
                            try:
                                row[int_col] = int(row[int_col])
                            except ValueError:
                                pass
                    all_matrix.append(row)

    # Master matrix CSV
    master_matrix_path = os.path.join(reports_dir, f"{symbol or 'master'}_batch_matrix.csv")
    if all_matrix:
        with open(master_matrix_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_matrix[0].keys()))
            writer.writeheader()
            writer.writerows(all_matrix)
        print(f"[+] Consolidated Master Matrix CSV: {master_matrix_path} ({len(all_matrix)} rows)")

        # Master matrix Markdown
        master_md_path = os.path.join(reports_dir, f"{symbol or 'master'}_batch_matrix.md")
        generate_markdown_report(all_matrix, master_md_path, symbol or "ALL_COINS", tag="CONSOLIDATED_MASTER")
        print(f"[+] Consolidated Master Markdown: {master_md_path}")

    # Consolidate Trades
    trade_chunk_files = [f for f in glob.glob(os.path.join(reports_dir, f"{symbol or '*'}_*_trades.csv")) if not f.endswith("_all_trades.csv")]
    all_trades: List[Dict[str, Any]] = []
    seen_trades = set()

    for tf in sorted(trade_chunk_files):
        with open(tf, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t_key = (row.get("symbol"), row.get("timeframe"), row.get("fee_schedule"), row.get("slippage_ticks"), row.get("trade_id"))
                if t_key not in seen_trades:
                    seen_trades.add(t_key)
                    all_trades.append(row)

    master_trades_path = os.path.join(reports_dir, f"{symbol or 'master'}_all_trades.csv")
    if all_trades:
        with open(master_trades_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_trades[0].keys()))
            writer.writeheader()
            writer.writerows(all_trades)
        print(f"[+] Consolidated Master Trades CSV: {master_trades_path} ({len(all_trades)} trades)")
    else:
        print("[*] No trades found to consolidate.")


def main():
    parser = argparse.ArgumentParser(description="Fee Coverage + 2 Ticks OB Experiment Runner")
    parser.add_argument("--symbol", type=str, default="BTC_USDT", help="Trading asset (or 'ALL')")
    parser.add_argument("--timeframes", type=str, default="1m,5m,15m,1h,4h,1d", help="Comma-separated timeframes")
    parser.add_argument("--fee-indices", type=str, default="0,1,2", help="Indices of fee schedules (0,1,2)")
    parser.add_argument("--slippage-ticks", type=str, default="1,2,3,4,5,6,7", help="Comma-separated slippage ticks")
    parser.add_argument("--extra-ticks", type=int, default=2, help="Extra profit ticks beyond fee coverage")
    parser.add_argument("--start", type=str, default="2026-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2026-08-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100.0, help="Initial balance in USDT")
    parser.add_argument("--leverage", type=int, default=10, help="Leverage multiplier")
    parser.add_argument("--margin-pct", type=float, default=10.0, help="Margin % per trade")
    parser.add_argument("--reports-dir", type=str, default=os.path.join(EXPERIMENT_DIR, "reports"), help="Output directory")
    parser.add_argument("--base-dir", type=str, default="BACKTESTER", help="Data base directory")
    parser.add_argument("--tag", type=str, default=None, help="Worker chunk tag")
    parser.add_argument("--consolidate", action="store_true", help="Consolidate chunk reports")

    args = parser.parse_args()

    if args.consolidate:
        consolidate_reports(args.reports_dir, args.symbol if args.symbol != "ALL" else None)
        return

    # Parse fee schedules
    selected_fees = []
    for idx_str in args.fee_indices.split(","):
        idx_str = idx_str.strip()
        if idx_str.isdigit():
            idx = int(idx_str)
            if 0 <= idx < len(FEE_SCHEDULES):
                selected_fees.append(FEE_SCHEDULES[idx])
    if not selected_fees:
        selected_fees = FEE_SCHEDULES

    # Parse slippage ticks
    slips = [int(s.strip()) for s in args.slippage_ticks.split(",") if s.strip().isdigit()]
    if not slips:
        slips = SLIPPAGE_TICKS

    # Parse timeframes
    tfs = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    if not tfs:
        tfs = DEFAULT_TIMEFRAMES

    target_symbols = DEFAULT_ASSETS if args.symbol.upper() == "ALL" else [args.symbol]

    for sym in target_symbols:
        run_experiment_for_symbol(
            symbol=sym,
            timeframes=tfs,
            fee_schedules=selected_fees,
            slippage_ticks=slips,
            extra_ticks=args.extra_ticks,
            start_date=args.start,
            end_date=args.end,
            capital=args.capital,
            leverage=args.leverage,
            margin_pct=args.margin_pct,
            reports_dir=args.reports_dir,
            base_dir=args.base_dir,
            tag=args.tag
        )


if __name__ == "__main__":
    main()
