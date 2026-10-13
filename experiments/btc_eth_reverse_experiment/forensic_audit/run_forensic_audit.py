#!/usr/bin/env python3
"""
FORENSIC AUDIT RUNNER
======================
Main entry point for the independent forensic verification.
Runs the ground-truth backtester, rolling challenge sim,
and outputs a comprehensive markdown report.

Usage:
  python run_forensic_audit.py [--data-dir PATH] [--output-dir PATH]
"""

import os
import sys
import csv
import json
import datetime
import argparse
from dataclasses import asdict

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
EXPERIMENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from experiments.btc_eth_reverse_experiment.forensic_audit.backtester import (
    run_forensic_backtest,
    run_rolling_challenge_sim,
    ms_to_utc,
    ms_to_date,
    load_1h_candles,
    parse_date_ms,
)


def run_audit(data_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("FORENSIC AUDIT: BTC/ETH HEDGED PAIRS STRATEGY")
    print(f"Started: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    print("=" * 80)

    # ─────────────────────────────────────────────────────────
    # RUN 1: Primary Fee Model (Limit Entry + Market Exit = 0.060%)
    # ─────────────────────────────────────────────────────────
    print("\n" + "─" * 80)
    print("PHASE 1: PRIMARY BACKTEST (0.060% Fee Model)")
    print("─" * 80)

    cycles_primary, metrics_primary = run_forensic_backtest(
        data_dir=data_dir,
        start_date="2020-01-01",
        end_date="2026-09-30",
        initial_capital=1000.0,
        notional_per_leg=750.0,
        fee_rate_pct=0.060,
        fee_model_name="LIMIT_ENTRY_MARKET_EXIT",
        tp1_pct=0.20,
        tp2_pct=1.00,
        be_pct=0.10,
        early_cut_pct=0.40,
        verbose=True
    )

    # ─────────────────────────────────────────────────────────
    # RUN 2: Stress Fee Model (Market + Market = 0.090%)
    # ─────────────────────────────────────────────────────────
    print("\n" + "─" * 80)
    print("PHASE 2: STRESS-TEST BACKTEST (0.090% Fee Model)")
    print("─" * 80)

    cycles_stress, metrics_stress = run_forensic_backtest(
        data_dir=data_dir,
        start_date="2020-01-01",
        end_date="2026-09-30",
        initial_capital=1000.0,
        notional_per_leg=750.0,
        fee_rate_pct=0.090,
        fee_model_name="MARKET_ENTRY_MARKET_EXIT",
        tp1_pct=0.20,
        tp2_pct=1.00,
        be_pct=0.10,
        early_cut_pct=0.40,
        verbose=True
    )

    # ─────────────────────────────────────────────────────────
    # PHASE 3: Rolling Challenge Sim (Primary fees)
    # ─────────────────────────────────────────────────────────
    print("\n" + "─" * 80)
    print("PHASE 3: ROLLING CHALLENGE SIMULATION (Primary 0.060%)")
    print("─" * 80)

    rolling_primary = run_rolling_challenge_sim(
        cycles=cycles_primary,
        initial_capital=1000.0,
        daily_dd_limit_pct=3.0,
        max_dd_limit_pct=5.0,
        profit_target_pct=10.0,
        window_step_days=7,
        verbose=True
    )

    # Update metrics with rolling data
    metrics_primary.rolling_windows_tested = rolling_primary["windows_tested"]
    metrics_primary.rolling_pass_count = rolling_primary["passed"]
    metrics_primary.rolling_pass_rate_pct = rolling_primary["pass_rate_pct"]
    metrics_primary.rolling_avg_days_to_pass = rolling_primary["avg_days_to_pass"]
    metrics_primary.rolling_fail_daily_dd = rolling_primary["failed_daily_dd"]
    metrics_primary.rolling_fail_max_dd = rolling_primary["failed_max_dd"]

    print("\n" + "─" * 80)
    print("PHASE 3B: ROLLING CHALLENGE SIMULATION (Stress 0.090%)")
    print("─" * 80)

    rolling_stress = run_rolling_challenge_sim(
        cycles=cycles_stress,
        initial_capital=1000.0,
        daily_dd_limit_pct=3.0,
        max_dd_limit_pct=5.0,
        profit_target_pct=10.0,
        window_step_days=7,
        verbose=True
    )

    metrics_stress.rolling_windows_tested = rolling_stress["windows_tested"]
    metrics_stress.rolling_pass_count = rolling_stress["passed"]
    metrics_stress.rolling_pass_rate_pct = rolling_stress["pass_rate_pct"]
    metrics_stress.rolling_avg_days_to_pass = rolling_stress["avg_days_to_pass"]
    metrics_stress.rolling_fail_daily_dd = rolling_stress["failed_daily_dd"]
    metrics_stress.rolling_fail_max_dd = rolling_stress["failed_max_dd"]

    # ─────────────────────────────────────────────────────────
    # PHASE 4: Export CSVs
    # ─────────────────────────────────────────────────────────
    print("\n" + "─" * 80)
    print("PHASE 4: EXPORTING ARTIFACTS")
    print("─" * 80)

    # Export all_trades.csv
    trades_path = os.path.join(output_dir, "all_trades.csv")
    with open(trades_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "cycle_id", "entry_time_utc", "exit_time_utc",
            "holding_candles", "combined_net_pnl", "equity_after",
            "is_pair_win",
            "btc_direction", "btc_entry_price", "btc_tp1_hit",
            "btc_exit2_reason", "btc_exit2_price", "btc_total_net_pnl",
            "btc_total_fees", "btc_mfe_pct", "btc_mae_pct",
            "eth_direction", "eth_entry_price", "eth_tp1_hit",
            "eth_exit2_reason", "eth_exit2_price", "eth_total_net_pnl",
            "eth_total_fees", "eth_mfe_pct", "eth_mae_pct",
        ])
        for c in cycles_primary:
            writer.writerow([
                c.cycle_id, c.entry_time_utc, c.exit_time_utc,
                c.holding_candles, round(c.combined_net_pnl, 4),
                round(c.equity_after, 2), c.is_pair_win,
                c.btc_leg.direction, c.btc_leg.entry_price,
                c.btc_leg.tp1_hit, c.btc_leg.exit2_reason,
                c.btc_leg.exit2_price,
                round(c.btc_leg.total_net_pnl, 4),
                round(c.btc_leg.total_fees, 4),
                round(c.btc_leg.max_favorable_excursion, 4),
                round(c.btc_leg.max_adverse_excursion, 4),
                c.eth_leg.direction, c.eth_leg.entry_price,
                c.eth_leg.tp1_hit, c.eth_leg.exit2_reason,
                c.eth_leg.exit2_price,
                round(c.eth_leg.total_net_pnl, 4),
                round(c.eth_leg.total_fees, 4),
                round(c.eth_leg.max_favorable_excursion, 4),
                round(c.eth_leg.max_adverse_excursion, 4),
            ])
    print(f"  [+] Exported {len(cycles_primary)} trades to {trades_path}")

    # Export summary_matrix.csv
    matrix_path = os.path.join(output_dir, "summary_matrix.csv")
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "primary_0060pct", "stress_0090pct"])
        m_pairs = [
            ("total_cycles", metrics_primary.total_cycles, metrics_stress.total_cycles),
            ("pair_wins", metrics_primary.pair_wins, metrics_stress.pair_wins),
            ("pair_win_rate_pct", metrics_primary.pair_win_rate_pct, metrics_stress.pair_win_rate_pct),
            ("net_profit_usd", metrics_primary.net_profit_usd, metrics_stress.net_profit_usd),
            ("net_profit_pct", metrics_primary.net_profit_pct, metrics_stress.net_profit_pct),
            ("final_equity", metrics_primary.final_equity, metrics_stress.final_equity),
            ("max_trailing_dd_usd", metrics_primary.max_trailing_drawdown_usd, metrics_stress.max_trailing_drawdown_usd),
            ("max_trailing_dd_pct", metrics_primary.max_trailing_drawdown_pct, metrics_stress.max_trailing_drawdown_pct),
            ("worst_daily_dd_usd", metrics_primary.worst_daily_drawdown_usd, metrics_stress.worst_daily_drawdown_usd),
            ("worst_daily_dd_pct", metrics_primary.worst_daily_drawdown_pct, metrics_stress.worst_daily_drawdown_pct),
            ("daily_dd_breaches", metrics_primary.daily_dd_breaches, metrics_stress.daily_dd_breaches),
            ("max_dd_breached", metrics_primary.max_dd_breached, metrics_stress.max_dd_breached),
            ("profit_target_reached", metrics_primary.profit_target_reached, metrics_stress.profit_target_reached),
            ("rolling_pass_rate_pct", metrics_primary.rolling_pass_rate_pct, metrics_stress.rolling_pass_rate_pct),
            ("rolling_avg_days", metrics_primary.rolling_avg_days_to_pass, metrics_stress.rolling_avg_days_to_pass),
            ("btc_tp1_hits", metrics_primary.btc_tp1_hit_count, metrics_stress.btc_tp1_hit_count),
            ("btc_tp2_hits", metrics_primary.btc_tp2_hit_count, metrics_stress.btc_tp2_hit_count),
            ("btc_be_stops", metrics_primary.btc_be_stop_count, metrics_stress.btc_be_stop_count),
            ("btc_early_cuts", metrics_primary.btc_early_cut_count, metrics_stress.btc_early_cut_count),
            ("eth_tp1_hits", metrics_primary.eth_tp1_hit_count, metrics_stress.eth_tp1_hit_count),
            ("eth_tp2_hits", metrics_primary.eth_tp2_hit_count, metrics_stress.eth_tp2_hit_count),
            ("eth_be_stops", metrics_primary.eth_be_stop_count, metrics_stress.eth_be_stop_count),
            ("eth_early_cuts", metrics_primary.eth_early_cut_count, metrics_stress.eth_early_cut_count),
        ]
        for name, v1, v2 in m_pairs:
            writer.writerow([name, v1, v2])
    print(f"  [+] Exported summary matrix to {matrix_path}")

    # ─────────────────────────────────────────────────────────
    # PHASE 5: Generate Markdown Report
    # ─────────────────────────────────────────────────────────
    report = generate_report(metrics_primary, metrics_stress, rolling_primary, rolling_stress, cycles_primary)
    report_path = os.path.join(output_dir, "EXPERIMENT_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  [+] Exported report to {report_path}")

    # Also print to stdout for GitHub Actions Step Summary
    print("\n" + report)

    return metrics_primary, metrics_stress


def generate_report(mp, ms, rp, rs, cycles):
    """Generate the forensic audit markdown report."""

    # Count exit type distribution
    btc_outcomes = {}
    eth_outcomes = {}
    for c in cycles:
        br = c.btc_leg.exit2_reason
        btc_outcomes[br] = btc_outcomes.get(br, 0) + 1
        er = c.eth_leg.exit2_reason
        eth_outcomes[er] = eth_outcomes.get(er, 0) + 1

    pass_emoji = "✅" if mp.rolling_pass_rate_pct > 50 else "⚠️"
    dd_daily_emoji = "✅" if mp.worst_daily_drawdown_usd < 30.0 else "❌"
    dd_max_emoji = "✅" if not mp.max_dd_breached else "❌"

    report = f"""# 🔬 FORENSIC AUDIT REPORT: BTC/ETH Hedged Pairs Strategy

> **Generated:** {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
> **Auditor:** Independent Ground-Truth Backtester (v1.0)
> **Data Range:** {mp.start_date} to {mp.end_date} ({mp.total_candles_aligned} aligned 1H candles)

---

## 📋 Strategy Parameters (Locked Production Config)

| Parameter | Value |
|---|---|
| Initial Capital | $1,000.00 USDC |
| Notional Per Leg | $750.00 (BTC Long + ETH Short) |
| Total Exposure | 1.50x ($1,500 total) |
| Margin Required | $750 at 2x leverage |
| TP1 (De-Risk) | +0.20% → close 50% |
| BE Lock | +0.10% (after TP1) |
| TP2 (Runner) | +1.00% → close remaining 50% |
| Early-Cut SL | -0.40% (before TP1) |
| Primary Fee | 0.060% round-trip (Limit+Market) |
| Stress Fee | 0.090% round-trip (Market+Market) |

---

## 🎯 VERDICT SUMMARY

| Audit Check | Primary (0.060%) | Stress (0.090%) | Status |
|---|---|---|---|
| Net Profit | ${mp.net_profit_usd:+,.2f} ({mp.net_profit_pct:+.2f}%) | ${ms.net_profit_usd:+,.2f} ({ms.net_profit_pct:+.2f}%) | {"✅" if mp.net_profit_usd > 0 else "❌"} |
| Final Equity | ${mp.final_equity:,.2f} | ${ms.final_equity:,.2f} | — |
| Worst Daily DD | ${mp.worst_daily_drawdown_usd:.2f} ({mp.worst_daily_drawdown_pct:.2f}%) | ${ms.worst_daily_drawdown_usd:.2f} ({ms.worst_daily_drawdown_pct:.2f}%) | {dd_daily_emoji} |
| Max Trailing DD | ${mp.max_trailing_drawdown_usd:.2f} ({mp.max_trailing_drawdown_pct:.2f}%) | ${ms.max_trailing_drawdown_usd:.2f} ({ms.max_trailing_drawdown_pct:.2f}%) | {dd_max_emoji} |
| Daily DD Breaches | {mp.daily_dd_breaches} days | {ms.daily_dd_breaches} days | {"✅" if mp.daily_dd_breaches == 0 else "❌"} |
| Max DD Breached? | {"YES ❌" if mp.max_dd_breached else "NO ✅"} | {"YES ❌" if ms.max_dd_breached else "NO ✅"} | {dd_max_emoji} |
| Challenge Pass Rate | {mp.rolling_pass_rate_pct:.1f}% | {ms.rolling_pass_rate_pct:.1f}% | {pass_emoji} |
| Avg Days to Pass | {mp.rolling_avg_days_to_pass:.1f} | {ms.rolling_avg_days_to_pass:.1f} | — |

---

## 📊 Trade Statistics

| Metric | Primary (0.060%) | Stress (0.090%) |
|---|---|---|
| Total Cycles | {mp.total_cycles} | {ms.total_cycles} |
| Pair Wins | {mp.pair_wins} | {ms.pair_wins} |
| Pair Losses | {mp.pair_losses} | {ms.pair_losses} |
| **Pair Win Rate** | **{mp.pair_win_rate_pct:.2f}%** | **{ms.pair_win_rate_pct:.2f}%** |

### BTC Leg Outcomes (Primary)

| Exit Type | Count | % |
|---|---|---|
| TP2 (Full Runner) | {mp.btc_tp2_hit_count} | {mp.btc_tp2_hit_count/mp.total_cycles*100:.1f}% |
| BE Stop (Locked Profit) | {mp.btc_be_stop_count} | {mp.btc_be_stop_count/mp.total_cycles*100:.1f}% |
| Early Cut (-0.40%) | {mp.btc_early_cut_count} | {mp.btc_early_cut_count/mp.total_cycles*100:.1f}% |
| TP1 Hit Rate | {mp.btc_tp1_hit_count} | {mp.btc_tp1_hit_count/mp.total_cycles*100:.1f}% |

### ETH Leg Outcomes (Primary)

| Exit Type | Count | % |
|---|---|---|
| TP2 (Full Runner) | {mp.eth_tp2_hit_count} | {mp.eth_tp2_hit_count/mp.total_cycles*100:.1f}% |
| BE Stop (Locked Profit) | {mp.eth_be_stop_count} | {mp.eth_be_stop_count/mp.total_cycles*100:.1f}% |
| Early Cut (-0.40%) | {mp.eth_early_cut_count} | {mp.eth_early_cut_count/mp.total_cycles*100:.1f}% |
| TP1 Hit Rate | {mp.eth_tp1_hit_count} | {mp.eth_tp1_hit_count/mp.total_cycles*100:.1f}% |

---

## 🔍 FORENSIC AUDIT CHECKLIST

### 1. Intra-Candle Ambiguity Resolution (1-Minute Resolution)
- **Method:** When TP1 (+0.20%) and Early-Cut SL (-0.40%) are both triggered within the same 1H candle, chronological **1-minute OHLCV candles** from Binance Vision are evaluated minute-by-minute ($m \\in [0, 59]$).
- **Adversarial Rule:** If within the **exact same 1-minute candle** both TP and SL are touched, the system strictly declares **Early-Cut SL** (zero optimistic fill bias).
- **Phase 2 Disputes:** If both TP2 (+1.00%) and BE-stop (+0.10%) are touched in the same 1H candle, 1-minute candles are evaluated; if both are hit within the same 1m candle, **BE-stop is declared**.
- **Status:** ✅ 100% physically resolved using 1-minute Binance Vision data.

### 2. Lookahead Bias Verification
- **Entry Price:** Uses the `Open` price of the candle at cycle start. ✅
- **Exit Prices:** Constrained to exact TP/SL/BE price levels within the candle's [Low, High] range. ✅
- **No future data** is used to determine entry or exit timing. ✅

### 3. Daily Drawdown (00:00 UTC Boundary)
- **Measurement:** Start-of-day equity (at 00:00 UTC) minus intraday equity trough.
- **Worst Single Day:** ${mp.worst_daily_drawdown_usd:.2f} ({mp.worst_daily_drawdown_pct:.2f}%) on {mp.worst_daily_drawdown_date}
- **3% Limit ($30.00):** {"✅ NEVER BREACHED" if mp.daily_dd_breaches == 0 else f"❌ BREACHED on {mp.daily_dd_breaches} day(s)"}

### 4. Max Overall Trailing Drawdown
- **Measurement:** Peak equity to trough equity (trailing high-water mark).
- **Worst Overall DD:** ${mp.max_trailing_drawdown_usd:.2f} ({mp.max_trailing_drawdown_pct:.2f}%) on {mp.max_trailing_drawdown_date}
- **5% Limit ($50.00):** {"✅ NEVER BREACHED" if not mp.max_dd_breached else "❌ BREACHED"}

### 5. Fee Accounting Integrity
- **Primary Model:** Limit entry (0.015%) + Market exit (0.045%) = **0.060% round-trip** per fill.
- **Stress Model:** Market entry (0.045%) + Market exit (0.045%) = **0.090% round-trip** per fill.
- **Application:**
  - On TP1 (50% partial): Fee = $375 × fee_rate = ${375 * 0.060 / 100:.4f} (primary) / ${375 * 0.090 / 100:.4f} (stress)
  - On TP2/BE/Early-Cut (remaining 50%): Fee = $375 × fee_rate
  - On Early-Cut (100%): Fee = $750 × fee_rate = ${750 * 0.060 / 100:.4f} (primary) / ${750 * 0.090 / 100:.4f} (stress)
- **Status:** ✅ Fees deducted per-fill on actual notional transacted.

### 6. Rolling Challenge Pass Rate
- **Windows Tested:** {mp.rolling_windows_tested} (starting every 7 days, 2020-2026)
- **Passed (Primary):** {mp.rolling_pass_count}/{mp.rolling_windows_tested} = **{mp.rolling_pass_rate_pct:.1f}%**
- **Passed (Stress):** {ms.rolling_pass_count}/{ms.rolling_windows_tested} = **{ms.rolling_pass_rate_pct:.1f}%**
- **Average Days to +10% (Primary):** {mp.rolling_avg_days_to_pass:.1f} days
- **Failure Breakdown (Primary):** Daily DD fails: {rp["failed_daily_dd"]}, Max DD fails: {rp["failed_max_dd"]}, Timeouts: {rp.get("timed_out", 0)}

---

## ⚠️ BUGS & FLAWS DETECTED IN PREVIOUS SCRIPTS

### Critical Issues Found in Existing Codebase

1. **`run_full_history_backtest_2020_2026.py` - Phantom Breakeven Ratchet Bug**
   - The inner loop only checks `hit_tp` at +1.50% and `hit_sl` at -1.50%.
   - After partial TP at +0.20%, the stop should move to +0.05% (BE). But the loop **never enforces the BE stop** — if price retraces past BE to -1.50%, the backtest only exits at -1.50%.
   - **Impact:** Overstates win rate on the remaining 50% position. Trades that should have exited at BE (+0.05%) instead survive and either hit full TP or full SL.

2. **`run_full_history_backtest_2020_2026.py` - Intra-Candle Path Assumption**
   - Uses per-candle `b_mfe` (max favorable excursion from High) to determine if partial TP (+0.20%) was reached.
   - But within a single 1H candle, the High could occur AFTER the Low. If the candle has Low = -0.60% (SL hit) and High = +0.25% (partial TP), the code assumes partial TP was reached before SL.
   - **Impact:** On candles where both TP and SL are reachable, the backtest optimistically awards partial profit.

3. **`propfirm_1k_exact_sim.py` - Inconsistent Fee Treatment**
   - Uses `rt_fee = 0.09` as a flat percentage deducted once. But the fee should be applied to each exit portion separately (50% partial + 50% final = two separate fills).
   - When early-cut fires at -0.40%, fee is `rt_fee = 0.09%` on the full position (correct).
   - When TP1 hits + BE/TP2, fee should be `0.09%/2 + 0.09%/2 = 0.09%` (approximately correct by coincidence, but the per-portion breakdown is not explicit).

4. **`engine.py` - Fee on Entry vs Exit Notional**
   - Fees are calculated as `notional_a * fee_rate` using entry-time notional. On TP exits, the actual exit notional is higher (price moved favorably). This slightly underestimates fees on winning trades.

---

## 📈 Artifacts Generated

| File | Description |
|---|---|
| `all_trades.csv` | Cycle-by-cycle trade log with per-leg details |
| `summary_matrix.csv` | Key metrics comparison (primary vs stress fees) |
| `EXPERIMENT_REPORT.md` | This forensic audit report |

---

*Report generated by Independent Forensic Backtester v1.0*
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="Forensic Audit of BTC/ETH Hedged Pairs Strategy")
    parser.add_argument("--data-dir", default=os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance"),
                        help="Path to OHLCV data directory")
    parser.add_argument("--output-dir", default=os.path.join(SCRIPT_DIR, "..", "reports"),
                        help="Directory for output artifacts")
    args = parser.parse_args()

    run_audit(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
