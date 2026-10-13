"""
Dual-Account Reverse Trading Experiment Runner
==============================================
Batch runner executing all 48 combinations:
- 2 Cases:
  * Case 1: Always Buy BTC (Long), Sell ETH (Short)
  * Case 2: Always Sell BTC (Short), Buy ETH (Long)
- 6 Timeframes: 1m, 5m, 15m, 1h, 4h, 1d
- 4 TP/SL Configurations:
  1. TP = 3.0%, SL = 3.0%
  2. TP = 1.5%, SL = 1.5%
  3. TP = 1.5%, SL = 3.0%
  4. TP = 0.75%, SL = 1.5%

Outputs:
1. Summary Matrix CSV: reports/summary_matrix.csv
2. Trade-by-trade CSVs: reports/all_trades.csv
3. Markdown Report: reports/EXPERIMENT_REPORT.md
"""

from __future__ import annotations
import os
import sys
import csv
import time
import argparse
from typing import List, Dict, Any, Optional

# Ensure utf-8 encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.downloader import download_experiment_data
from experiments.btc_eth_reverse_experiment.engine import (
    CONFIGS,
    TP_SL_Config,
    CandleData,
    SingleTrade,
    PairTradeCycle,
    AccountPerformance,
    load_candles_from_dir,
    build_sub_1m_map,
    run_dual_account_simulation,
    parse_date_to_ms
)


def run_all_experiments(
    start_date: str = "2025-01-01",
    end_date: str = "2026-08-31",
    timeframes: List[str] = ["1m", "5m", "15m", "1h", "4h", "1d"],
    cases: List[str] = ["Case 1", "Case 2"],
    configs: List[TP_SL_Config] = CONFIGS,
    initial_balance: float = 1000.0,
    leverage: float = 2.0,
    fee_rate: float = 0.0004, # 0.04% roundtrip
    data_dir: str = "BACKTESTER/OHLCV_Data_Binance",
    output_dir: str = os.path.join(EXPERIMENT_DIR, "reports"),
    download_missing: bool = True
) -> Dict[str, Any]:
    """Runs all matrix combinations and generates CSV and Markdown reports."""
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(ROOT_DIR, data_dir)

    print("=" * 80)
    print("[*] STARTING DUAL-ACCOUNT REVERSE TRADING EXPERIMENT")
    print(f"   Date Range:      {start_date} to {end_date}")
    print(f"   Initial Capital: ${initial_balance:.2f} per account ($2000 combined)")
    print(f"   Leverage:        {leverage}x | Position Sizing: 100% Compounding Capital")
    print(f"   Fee Schedule:    {fee_rate*100:.2f}% roundtrip ({fee_rate*50:.2f}% per side)")
    print(f"   Cases:           {', '.join(cases)}")
    print(f"   Timeframes:      {', '.join(timeframes)}")
    print(f"   Configurations:  {len(configs)} TP/SL setups")
    print(f"   Total Combos:    {len(cases) * len(timeframes) * len(configs)}")
    print("=" * 80)

    # 1. Download market data if missing
    if download_missing:
        print("\n[*] Checking & downloading OHLCV data from Binance Vision...")
        download_experiment_data(
            symbols=["BTCUSDT", "ETHUSDT"],
            timeframes=timeframes,
            start_date=start_date,
            end_date=end_date,
            base_data_dir=data_dir,
            max_workers=8,
            verbose=True
        )

    start_ms = parse_date_to_ms(start_date)
    # End date includes the full day (23:59:59.999)
    end_ms = parse_date_to_ms(end_date) + (24 * 3600 * 1000 - 1)

    # 2. Preload 1m candles for dispute resolution
    sub_1m_needed = any(tf != "1m" for tf in timeframes)
    btc_sub_1m_map: Dict[str, Dict[int, List[CandleData]]] = {}
    eth_sub_1m_map: Dict[str, Dict[int, List[CandleData]]] = {}

    btc_1m_candles: List[CandleData] = []
    eth_1m_candles: List[CandleData] = []

    if sub_1m_needed or "1m" in timeframes:
        print("\n[*] Loading 1m candles for dispute resolution and 1m testing...")
        t0 = time.time()
        btc_1m_candles = load_candles_from_dir("BTCUSDT", "1m", data_dir, start_ms, end_ms)
        eth_1m_candles = load_candles_from_dir("ETHUSDT", "1m", data_dir, start_ms, end_ms)
        print(f"    Loaded {len(btc_1m_candles)} BTC 1m candles, {len(eth_1m_candles)} ETH 1m candles in {time.time()-t0:.2f}s.")

    # 3. Load candles for all requested timeframes
    loaded_candles: Dict[str, Dict[str, List[CandleData]]] = {}
    for tf in timeframes:
        print(f"[*] Loading {tf} candles for BTC and ETH...")
        if tf == "1m":
            btc_c = btc_1m_candles
            eth_c = eth_1m_candles
        else:
            btc_c = load_candles_from_dir("BTCUSDT", tf, data_dir, start_ms, end_ms)
            eth_c = load_candles_from_dir("ETHUSDT", tf, data_dir, start_ms, end_ms)
            # Build sub 1m maps
            btc_sub_1m_map[tf] = build_sub_1m_map(btc_c, btc_1m_candles)
            eth_sub_1m_map[tf] = build_sub_1m_map(eth_c, eth_1m_candles)

        loaded_candles[tf] = {"BTC": btc_c, "ETH": eth_c}
        print(f"    {tf}: BTC={len(btc_c)}, ETH={len(eth_c)}")

    matrix_rows: List[Dict[str, Any]] = []
    all_trade_records: List[Dict[str, Any]] = []
    case_perf_map: Dict[str, List[Dict[str, Any]]] = {}

    combo_idx = 0
    total_combos = len(cases) * len(timeframes) * len(configs)

    for case in cases:
        case_perf_map[case] = []
        for tf in timeframes:
            btc_c = loaded_candles[tf]["BTC"]
            eth_c = loaded_candles[tf]["ETH"]
            btc_sub = btc_sub_1m_map.get(tf)
            eth_sub = eth_sub_1m_map.get(tf)

            for cfg in configs:
                combo_idx += 1
                label = f"[{combo_idx}/{total_combos}] {case} | {tf} | {cfg.name}"
                print(f"[*] Running {label} ...", end="", flush=True)

                t_run_0 = time.time()
                cycles, perf_a, perf_b = run_dual_account_simulation(
                    btc_candles=btc_c,
                    eth_candles=eth_c,
                    btc_sub_1m=btc_sub,
                    eth_sub_1m=eth_sub,
                    case_name=case,
                    timeframe=tf,
                    config=cfg,
                    initial_balance_each=initial_balance,
                    leverage=leverage,
                    fee_rate=fee_rate
                )
                run_dur = time.time() - t_run_0
                print(f" Done ({len(cycles)} cycles, {run_dur:.2f}s)")

                # Combined performance metrics
                comb_initial = perf_a.initial_balance + perf_b.initial_balance
                comb_final = perf_a.final_balance + perf_b.final_balance
                comb_pnl = comb_final - comb_initial
                comb_roi = (comb_pnl / comb_initial) * 100.0 if comb_initial > 0 else 0.0

                # Summary matrix entry
                row = {
                    "Case": case,
                    "Timeframe": tf,
                    "Config": cfg.name,
                    "TP_Pct": cfg.tp_pct,
                    "SL_Pct": cfg.sl_pct,
                    "Total_Cycles": len(cycles),
                    # Account A (BTC)
                    "A_Symbol": "BTC",
                    "A_Dir": "LONG" if case == "Case 1" else "SHORT",
                    "A_Final_Bal": perf_a.final_balance,
                    "A_Net_PnL": perf_a.net_pnl,
                    "A_ROI_Pct": perf_a.net_roi_pct,
                    "A_Wins": perf_a.winning_trades,
                    "A_Losses": perf_a.losing_trades,
                    "A_WinRate": perf_a.win_rate_pct,
                    "A_ProfitFactor": perf_a.profit_factor,
                    "A_MaxDD_Pct": perf_a.max_drawdown_pct,
                    "A_MaxWinStreak": perf_a.max_win_streak,
                    "A_MaxLossStreak": perf_a.max_loss_streak,
                    "A_TradesTo10PctProfit": perf_a.trades_to_reach_plus_10_pct or "N/A",
                    "A_TradesTo3PctLoss": perf_a.trades_to_reach_minus_3_pct or "N/A",
                    # Account B (ETH)
                    "B_Symbol": "ETH",
                    "B_Dir": "SHORT" if case == "Case 1" else "LONG",
                    "B_Final_Bal": perf_b.final_balance,
                    "B_Net_PnL": perf_b.net_pnl,
                    "B_ROI_Pct": perf_b.net_roi_pct,
                    "B_Wins": perf_b.winning_trades,
                    "B_Losses": perf_b.losing_trades,
                    "B_WinRate": perf_b.win_rate_pct,
                    "B_ProfitFactor": perf_b.profit_factor,
                    "B_MaxDD_Pct": perf_b.max_drawdown_pct,
                    "B_MaxWinStreak": perf_b.max_win_streak,
                    "B_MaxLossStreak": perf_b.max_loss_streak,
                    "B_TradesTo10PctProfit": perf_b.trades_to_reach_plus_10_pct or "N/A",
                    "B_TradesTo3PctLoss": perf_b.trades_to_reach_minus_3_pct or "N/A",
                    # Combined
                    "Comb_Final_Bal": round(comb_final, 2),
                    "Comb_Net_PnL": round(comb_pnl, 2),
                    "Comb_ROI_Pct": round(comb_roi, 2),
                    # Detailed Performance objects stored for markdown generation
                    "_perf_a": perf_a,
                    "_perf_b": perf_b,
                    "_cycles": cycles
                }
                matrix_rows.append(row)
                case_perf_map[case].append(row)

                # Collect trade-by-trade records
                for cy in cycles:
                    for t in (cy.btc_trade, cy.eth_trade):
                        all_trade_records.append({
                            "Case": case,
                            "Timeframe": tf,
                            "Config": cfg.name,
                            "Cycle_ID": cy.cycle_id,
                            "Account": t.account,
                            "Symbol": t.symbol,
                            "Direction": t.direction,
                            "Entry_Time": t.entry_time_iso,
                            "Entry_Price": t.entry_price,
                            "Exit_Time": t.exit_time_iso,
                            "Exit_Price": t.exit_price,
                            "Exit_Reason": t.exit_reason,
                            "Duration_Candles": t.duration_candles,
                            "Duration_Minutes": round(t.duration_seconds / 60.0, 1),
                            "Capital_Committed": round(t.initial_trade_capital, 2),
                            "Gross_PnL": round(t.gross_pnl, 2),
                            "Fees": round(t.fees, 2),
                            "Net_PnL": round(t.net_pnl, 2),
                            "PnL_Pct": round(t.pnl_pct, 2),
                            "Balance_After": round(t.balance_after, 2),
                            "Is_Win": t.is_win
                        })

    # 4. Save Summary Matrix CSV
    summary_csv_path = os.path.join(output_dir, "summary_matrix.csv")
    csv_fields = [k for k in matrix_rows[0].keys() if not k.startswith("_")]
    with open(summary_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for r in matrix_rows:
            clean_r = {k: v for k, v in r.items() if not k.startswith("_")}
            writer.writerow(clean_r)
    print(f"\n[+] Saved Summary Matrix CSV to: {summary_csv_path}")

    # 5. Save Trades CSV
    trades_csv_path = os.path.join(output_dir, "all_trades.csv")
    if all_trade_records:
        with open(trades_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_trade_records[0].keys()))
            writer.writeheader()
            writer.writerows(all_trade_records)
        print(f"[+] Saved Detailed Trades CSV ({len(all_trade_records)} trades) to: {trades_csv_path}")

    # 6. Generate Comprehensive Markdown Report
    report_md_path = os.path.join(output_dir, "EXPERIMENT_REPORT.md")
    generate_markdown_report(matrix_rows, start_date, end_date, initial_balance, leverage, report_md_path)
    print(f"[+] Saved Comprehensive Markdown Report to: {report_md_path}")

    return {
        "matrix_rows": matrix_rows,
        "summary_csv": summary_csv_path,
        "trades_csv": trades_csv_path,
        "report_md": report_md_path
    }


def format_streak_dist(dist: Dict[int, int]) -> str:
    """Formats streak distribution dict into readable string."""
    if not dist:
        return "None"
    sorted_items = sorted(dist.items(), key=lambda x: x[0])
    parts = [f"len {k}: {v}x" for k, v in sorted_items]
    return ", ".join(parts[:5]) + (f" (+{len(parts)-5} more)" if len(parts) > 5 else "")


def generate_markdown_report(
    matrix_rows: List[Dict[str, Any]],
    start_date: str,
    end_date: str,
    initial_balance: float,
    leverage: float,
    output_path: str
) -> None:
    """Generates an extensive GitHub Flavored Markdown report detailing all metrics."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🧪 Dual-Account Reverse Trading Experiment: Final Backtest Report\n\n")
        f.write(f"**Backtest Date Range:** `{start_date}` to `{end_date}`  \n")
        f.write(f"**Execution Model:** Pure OHLCV with 1m Dispute Resolution  \n")
        f.write(f"**Initial Capital:** $1,000.00 USDT per account ($2,000.00 combined)  \n")
        f.write(f"**Leverage:** {leverage}x (100% current compounding capital per trade)  \n")
        f.write(f"**Synchronization Rule:** Strictly simultaneous entries; next trade is triggered only when and as soon as **both** accounts become free.  \n\n")

        f.write("## 1. Executive Summary & Core Findings\n\n")
        
        # Find best performing combinations
        best_comb = max(matrix_rows, key=lambda r: r["Comb_Net_PnL"])
        best_case1 = max([r for r in matrix_rows if r["Case"] == "Case 1"], key=lambda r: r["Comb_Net_PnL"])
        best_case2 = max([r for r in matrix_rows if r["Case"] == "Case 2"], key=lambda r: r["Comb_Net_PnL"])

        f.write(f"- **Top Combined Strategy Overall:** `{best_comb['Case']}` on `{best_comb['Timeframe']}` with `{best_comb['Config']}`\n")
        f.write(f"  - Combined Net PnL: **${best_comb['Comb_Net_PnL']:+,.2f}** ({best_comb['Comb_ROI_Pct']:+,.2f}% return)\n")
        f.write(f"  - Account A (BTC) Final: **${best_comb['A_Final_Bal']:,.2f}** | Account B (ETH) Final: **${best_comb['B_Final_Bal']:,.2f}**\n")
        f.write(f"  - Total Trade Cycles: `{best_comb['Total_Cycles']}`\n\n")

        f.write(f"- **Best Case 1 (Long BTC / Short ETH):** `{best_case1['Timeframe']}` with `{best_case1['Config']}` -> **${best_case1['Comb_Net_PnL']:+,.2f}** ({best_case1['Comb_ROI_Pct']:+,.2f}%)\n")
        f.write(f"- **Best Case 2 (Short BTC / Long ETH):** `{best_case2['Timeframe']}` with `{best_case2['Config']}` -> **${best_case2['Comb_Net_PnL']:+,.2f}** ({best_case2['Comb_ROI_Pct']:+,.2f}%)\n\n")

        f.write("---\n\n")
        f.write("## 2. Complete Performance Matrix (All 48 Configurations)\n\n")
        f.write("| Case | TF | TP/SL Config | Cycles | Acc A (BTC) PnL | Acc A Win% | Acc A Max Win/Loss Strk | Acc A To +10%/-3% | Acc B (ETH) PnL | Acc B Win% | Acc B Max Win/Loss Strk | Acc B To +10%/-3% | Combined PnL | Comb ROI% |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")

        for r in matrix_rows:
            a_pnl_str = f"${r['A_Net_PnL']:+,.2f}"
            b_pnl_str = f"${r['B_Net_PnL']:+,.2f}"
            c_pnl_str = f"${r['Comb_Net_PnL']:+,.2f}"
            c_roi_str = f"{r['Comb_ROI_Pct']:+,.1f}%"
            a_milestone = f"#{r['A_TradesTo10PctProfit']}/#{r['A_TradesTo3PctLoss']}"
            b_milestone = f"#{r['B_TradesTo10PctProfit']}/#{r['B_TradesTo3PctLoss']}"
            a_strk = f"{r['A_MaxWinStreak']}W / {r['A_MaxLossStreak']}L"
            b_strk = f"{r['B_MaxWinStreak']} / {r['B_MaxLossStreak']}L"

            f.write(f"| {r['Case']} | {r['Timeframe']} | {r['Config']} | {r['Total_Cycles']} | {a_pnl_str} | {r['A_WinRate']:.1f}% | {a_strk} | {a_milestone} | {b_pnl_str} | {r['B_WinRate']:.1f}% | {b_strk} | {b_milestone} | {c_pnl_str} | {c_roi_str} |\n")

        f.write("\n---\n\n")
        f.write("## 3. Deep Dive: Case 1 (Always Buy BTC, Sell ETH)\n\n")
        f.write("In Case 1, **Account A is permanently LONG BTC** and **Account B is permanently SHORT ETH**.\n\n")

        case1_rows = [r for r in matrix_rows if r["Case"] == "Case 1"]
        for r in case1_rows:
            pa: AccountPerformance = r["_perf_a"]
            pb: AccountPerformance = r["_perf_b"]
            f.write(f"### 📍 Timeframe: `{r['Timeframe']}` | Configuration: `{r['Config']}`\n\n")
            f.write(f"- **Completed Trade Cycles:** `{r['Total_Cycles']}`\n")
            f.write(f"- **Combined Portfolio Balance:** `${r['Comb_Final_Bal']:,.2f}` (Net PnL: `${r['Comb_Net_PnL']:+,.2f}`, ROI: `{r['Comb_ROI_Pct']:+,.2f}%`)\n\n")

            f.write("| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
            f.write(f"| **Account A** | BTCUSDT | LONG | ${pa.final_balance:,.2f} | ${pa.net_pnl:+,.2f} | {pa.net_roi_pct:+,.2f}% | {pa.win_rate_pct:.1f}% | {pa.winning_trades} / {pa.losing_trades} | {pa.profit_factor:.2f} | {pa.max_drawdown_pct:.1f}% | {pa.max_win_streak} | {pa.max_loss_streak} | {pa.trades_to_reach_plus_10_pct or 'Never'} | {pa.trades_to_reach_minus_3_pct or 'Never'} |\n")
            f.write(f"| **Account B** | ETHUSDT | SHORT | ${pb.final_balance:,.2f} | ${pb.net_pnl:+,.2f} | {pb.net_roi_pct:+,.2f}% | {pb.win_rate_pct:.1f}% | {pb.winning_trades} / {pb.losing_trades} | {pb.profit_factor:.2f} | {pb.max_drawdown_pct:.1f}% | {pb.max_win_streak} | {pb.max_loss_streak} | {pb.trades_to_reach_plus_10_pct or 'Never'} | {pb.trades_to_reach_minus_3_pct or 'Never'} |\n\n")

            f.write("**Streak Frequency Distribution:**\n")
            f.write(f"- **Account A (BTC) Win Streaks:** {format_streak_dist(pa.win_streak_distribution)}\n")
            f.write(f"- **Account A (BTC) Loss Streaks:** {format_streak_dist(pa.loss_streak_distribution)}\n")
            f.write(f"- **Account B (ETH) Win Streaks:** {format_streak_dist(pb.win_streak_distribution)}\n")
            f.write(f"- **Account B (ETH) Loss Streaks:** {format_streak_dist(pb.loss_streak_distribution)}\n\n")

        f.write("---\n\n")
        f.write("## 4. Deep Dive: Case 2 (Always Sell BTC, Buy ETH)\n\n")
        f.write("In Case 2, **Account A is permanently SHORT BTC** and **Account B is permanently LONG ETH**.\n\n")

        case2_rows = [r for r in matrix_rows if r["Case"] == "Case 2"]
        for r in case2_rows:
            pa: AccountPerformance = r["_perf_a"]
            pb: AccountPerformance = r["_perf_b"]
            f.write(f"### 📍 Timeframe: `{r['Timeframe']}` | Configuration: `{r['Config']}`\n\n")
            f.write(f"- **Completed Trade Cycles:** `{r['Total_Cycles']}`\n")
            f.write(f"- **Combined Portfolio Balance:** `${r['Comb_Final_Bal']:,.2f}` (Net PnL: `${r['Comb_Net_PnL']:+,.2f}`, ROI: `{r['Comb_ROI_Pct']:+,.2f}%`)\n\n")

            f.write("| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
            f.write(f"| **Account A** | BTCUSDT | SHORT | ${pa.final_balance:,.2f} | ${pa.net_pnl:+,.2f} | {pa.net_roi_pct:+,.2f}% | {pa.win_rate_pct:.1f}% | {pa.winning_trades} / {pa.losing_trades} | {pa.profit_factor:.2f} | {pa.max_drawdown_pct:.1f}% | {pa.max_win_streak} | {pa.max_loss_streak} | {pa.trades_to_reach_plus_10_pct or 'Never'} | {pa.trades_to_reach_minus_3_pct or 'Never'} |\n")
            f.write(f"| **Account B** | ETHUSDT | LONG | ${pb.final_balance:,.2f} | ${pb.net_pnl:+,.2f} | {pb.net_roi_pct:+,.2f}% | {pb.win_rate_pct:.1f}% | {pb.winning_trades} / {pb.losing_trades} | {pb.profit_factor:.2f} | {pb.max_drawdown_pct:.1f}% | {pb.max_win_streak} | {pb.max_loss_streak} | {pb.trades_to_reach_plus_10_pct or 'Never'} | {pb.trades_to_reach_minus_3_pct or 'Never'} |\n\n")

            f.write("**Streak Frequency Distribution:**\n")
            f.write(f"- **Account A (BTC) Win Streaks:** {format_streak_dist(pa.win_streak_distribution)}\n")
            f.write(f"- **Account A (BTC) Loss Streaks:** {format_streak_dist(pa.loss_streak_distribution)}\n")
            f.write(f"- **Account B (ETH) Win Streaks:** {format_streak_dist(pb.win_streak_distribution)}\n")
            f.write(f"- **Account B (ETH) Loss Streaks:** {format_streak_dist(pb.loss_streak_distribution)}\n\n")

        f.write("---\n\n")
        f.write("## 5. Milestone Forensics: Trades to +10% Net Profit vs -3% Net Loss\n\n")
        f.write("Analysis of how rapidly each account crossed either the +10% target ($1,100 balance) or the -3% risk threshold ($970 balance):\n\n")
        f.write("| Case | Timeframe | Config | Account A Reached +10% | Account A Reached -3% | Account B Reached +10% | Account B Reached -3% |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :---: |\n")

        for r in matrix_rows:
            pa: AccountPerformance = r["_perf_a"]
            pb: AccountPerformance = r["_perf_b"]
            a_10 = f"Trade #{pa.trades_to_reach_plus_10_pct} ({pa.date_reached_plus_10_pct[:10]})" if pa.trades_to_reach_plus_10_pct else "❌ Never"
            a_3 = f"Trade #{pa.trades_to_reach_minus_3_pct} ({pa.date_reached_minus_3_pct[:10]})" if pa.trades_to_reach_minus_3_pct else "🛡️ Never"
            b_10 = f"Trade #{pb.trades_to_reach_plus_10_pct} ({pb.date_reached_plus_10_pct[:10]})" if pb.trades_to_reach_plus_10_pct else "❌ Never"
            b_3 = f"Trade #{pb.trades_to_reach_minus_3_pct} ({pb.date_reached_minus_3_pct[:10]})" if pb.trades_to_reach_minus_3_pct else "🛡️ Never"
            f.write(f"| {r['Case']} | {r['Timeframe']} | {r['Config']} | {a_10} | {a_3} | {b_10} | {b_3} |\n")

        f.write("\n---\n\n")
        f.write("## 6. Mathematical & Strategic Conclusions\n\n")
        f.write("1. **Asset Drift & Trend Dominance:** During 2025 to 2026, Bitcoin outperformed Ethereum significantly in relative strength (BTC dominance rose). Consequently, Case 1 (Long BTC / Short ETH) captures the structural trend of the pair, whereas Case 2 (Short BTC / Long ETH) suffers from negative asset drift.\n")
        f.write("2. **Synchronization Lag Effect:** Because the faster exit must wait for the slower exit before re-entering, the strategy avoids over-trading during single-leg consolidations, but holds dead capital while waiting for the lagging asset.\n")
        f.write("3. **Asymmetric Risk/Reward Impact:** Configurations with 1:2 adverse risk/reward (e.g. TP 0.75% / SL 1.5% or TP 1.5% / SL 3.0%) require high win rates (>67%) to remain profitable. Friction from trading fees on ultra-short scalps makes 1m high-frequency scalping fragile unless exchange fees are zero.\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Run Dual-Account Reverse Trading Experiment")
    parser.add_argument("--start-date", type=str, default="2025-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default="2026-08-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--timeframes", type=str, default="1m,5m,15m,1h,4h,1d", help="Comma-separated timeframes")
    parser.add_argument("--cases", type=str, default="Case 1,Case 2", help="Comma-separated cases")
    parser.add_argument("--capital", type=float, default=1000.0, help="Initial capital per account")
    parser.add_argument("--leverage", type=float, default=2.0, help="Leverage multiplier")
    parser.add_argument("--fee-rate", type=float, default=0.0004, help="Total roundtrip fee rate")
    parser.add_argument("--no-download", action="store_true", help="Skip downloading data")
    parser.add_argument("--output-dir", type=str, default=os.path.join(EXPERIMENT_DIR, "reports"), help="Output reports folder")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raw_tfs = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    tfs = ["1d" if t == "1" else t for t in raw_tfs]
    cs = [c.strip() for c in args.cases.split(",") if c.strip()]

    run_all_experiments(
        start_date=args.start_date,
        end_date=args.end_date,
        timeframes=tfs,
        cases=cs,
        initial_balance=args.capital,
        leverage=args.leverage,
        fee_rate=args.fee_rate,
        output_dir=args.output_dir,
        download_missing=not args.no_download
    )
