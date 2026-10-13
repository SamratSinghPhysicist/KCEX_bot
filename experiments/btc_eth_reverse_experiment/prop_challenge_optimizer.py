"""
Prop Challenge Optimizer for Dual Reverse Accounts
==================================================
Simulates prop firm challenge evaluations:
- Account A: Trades BTC
- Account B: Trades ETH (Opposite direction)
- Target: +10% Net Profit ($1,100 balance)
- Failure: Max Drawdown >= 3.0% ($970 balance or 3% peak-to-trough)

Tests parameter grid:
1. Risk per trade: 0.25%, 0.50%, 0.75%, 1.00%
2. TP/SL ratios:
   - 1:1 (TP 1.0/SL 1.0, TP 1.5/SL 1.5, TP 2.0/SL 2.0)
   - 2:1 Favorable (TP 2.0/SL 1.0, TP 1.5/SL 0.75, TP 3.0/SL 1.5)
   - 1:2 Adverse (TP 1.5/SL 3.0, TP 0.75/SL 1.5)
3. Timeframes: 1h, 4h, 15m
4. Direction modes:
   - Fixed Case 1: Always Long BTC / Short ETH
   - Fixed Case 2: Always Short BTC / Long ETH
   - Regime Filtered: Long BTC / Short ETH when BTC > 200 EMA; Short BTC / Long ETH when BTC < 200 EMA
5. Rolling challenge windows starting every 7 days across 2025-2026.
"""

from __future__ import annotations
import os
import sys
import csv
import collections
from typing import List, Dict, Any, Tuple, Optional

# Ensure utf-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    CandleData,
    TP_SL_Config,
    load_candles_from_dir,
    build_sub_1m_map,
    evaluate_candle_tp_sl,
    parse_date_to_ms
)


def simulate_challenge_sequence(
    trade_outcomes: List[Tuple[bool, bool, float, float]], # List of (btc_win, eth_win, btc_rr, eth_rr)
    risk_pct: float = 0.5, # Risk 0.5% per trade on current balance
    target_profit_pct: float = 10.0,
    max_dd_pct: float = 3.0,
    fee_per_trade_pct: float = 0.04
) -> Tuple[bool, bool, int, int]:
    """
    Simulates challenge progression for Account A and Account B.
    Returns: (a_passed, b_passed, a_trades, b_trades)
    """
    # Account A (BTC)
    bal_a = 1000.0
    peak_a = 1000.0
    a_status = "RUNNING" # "PASSED", "FAILED", "RUNNING"
    trades_a = 0

    # Account B (ETH)
    bal_b = 1000.0
    peak_b = 1000.0
    b_status = "RUNNING"
    trades_b = 0

    for btc_win, eth_win, btc_rr, eth_rr in trade_outcomes:
        # Step Account A
        if a_status == "RUNNING":
            trades_a += 1
            risk_usd = bal_a * (risk_pct / 100.0)
            fee_usd = bal_a * (fee_per_trade_pct / 100.0)
            if btc_win:
                gain_usd = (risk_usd * btc_rr) - fee_usd
                bal_a += gain_usd
            else:
                loss_usd = risk_usd + fee_usd
                bal_a -= loss_usd

            if bal_a > peak_a:
                peak_a = bal_a

            dd_a = (peak_a - bal_a) / peak_a * 100.0
            if dd_a >= max_dd_pct:
                a_status = "FAILED"
            elif ((bal_a - 1000.0) / 1000.0 * 100.0) >= target_profit_pct:
                a_status = "PASSED"

        # Step Account B
        if b_status == "RUNNING":
            trades_b += 1
            risk_usd = bal_b * (risk_pct / 100.0)
            fee_usd = bal_b * (fee_per_trade_pct / 100.0)
            if eth_win:
                gain_usd = (risk_usd * eth_rr) - fee_usd
                bal_b += gain_usd
            else:
                loss_usd = risk_usd + fee_usd
                bal_b -= loss_usd

            if bal_b > peak_b:
                peak_b = bal_b

            dd_b = (peak_b - bal_b) / peak_b * 100.0
            if dd_b >= max_dd_pct:
                b_status = "FAILED"
            elif ((bal_b - 1000.0) / 1000.0 * 100.0) >= target_profit_pct:
                b_status = "PASSED"

        if a_status != "RUNNING" and b_status != "RUNNING":
            break

    return (a_status == "PASSED", b_status == "PASSED", trades_a, trades_b)


def run_full_prop_optimization():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2025-01-01")
    end_ms = parse_date_to_ms("2026-10-12") + (24 * 3600 * 1000 - 1)

    print("[*] Loading candle data for Prop Challenge Optimizer...")
    btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
    eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)

    configs_to_test = [
        # (Name, tp_pct, sl_pct, rr_ratio)
        ("TP1.5_SL3.0 (1:2)", 1.5, 3.0, 0.5),
        ("TP0.75_SL1.5 (1:2)", 0.75, 1.5, 0.5),
        ("TP1.5_SL1.5 (1:1)", 1.5, 1.5, 1.0),
        ("TP2.0_SL2.0 (1:1)", 2.0, 2.0, 1.0),
        ("TP1.0_SL1.0 (1:1)", 1.0, 1.0, 1.0),
        ("TP2.0_SL1.0 (2:1)", 2.0, 1.0, 2.0),
        ("TP1.5_SL0.75 (2:1)", 1.5, 0.75, 2.0),
        ("TP3.0_SL1.5 (2:1)", 3.0, 1.5, 2.0),
    ]

    timeframes_to_test = ["1h", "4h"]
    risks_to_test = [0.25, 0.35, 0.50, 0.75]

    results = []

    for tf in timeframes_to_test:
        btc_c = load_candles_from_dir("BTCUSDT", tf, base_dir, start_ms, end_ms)
        eth_c = load_candles_from_dir("ETHUSDT", tf, base_dir, start_ms, end_ms)

        btc_sub = build_sub_1m_map(btc_c, btc_1m)
        eth_sub = build_sub_1m_map(eth_c, eth_1m)

        btc_dict = {c.open_time_ms: c for c in btc_c}
        eth_dict = {c.open_time_ms: c for c in eth_c}
        common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

        for cfg_name, tp_p, sl_p, rr in configs_to_test:
            # Pre-simulate all trade cycles for Case 1 (Long BTC / Short ETH)
            raw_cycles = []
            i = 0
            tot_len = len(common_times)

            while i < tot_len:
                entry_ts = common_times[i]
                c_b = btc_dict[entry_ts]
                c_e = eth_dict[entry_ts]

                p_b = c_b.open
                p_e = c_e.open

                tp_b = p_b * (1.0 + (tp_p / 100.0))
                sl_b = p_b * (1.0 - (sl_p / 100.0))

                tp_e = p_e * (1.0 - (tp_p / 100.0))
                sl_e = p_e * (1.0 + (sl_p / 100.0))

                b_exit = None
                b_res = None
                e_exit = None
                e_res = None

                j = i
                while j < tot_len:
                    ts = common_times[j]
                    if b_exit is None:
                        r, _ = evaluate_candle_tp_sl("LONG", p_b, tp_b, sl_b, btc_dict[ts], btc_sub, tf)
                        if r: b_exit = j; b_res = r
                    if e_exit is None:
                        r, _ = evaluate_candle_tp_sl("SHORT", p_e, tp_e, sl_e, eth_dict[ts], eth_sub, tf)
                        if r: e_exit = j; e_res = r
                    if b_exit is not None and e_exit is not None:
                        break
                    j += 1

                if b_exit is None or e_exit is None:
                    break

                free_idx = max(b_exit, e_exit)
                b_win = (b_res == "TP")
                e_win = (e_res == "TP")
                raw_cycles.append((b_win, e_win, rr, rr))
                i = free_idx + 1

            # Test rolling challenges starting every 10 cycles
            for risk in risks_to_test:
                n_sims = 0
                both_passed_cnt = 0
                a_passed_cnt = 0
                b_passed_cnt = 0
                either_passed_cnt = 0

                step = 10
                for start_idx in range(0, len(raw_cycles) - 30, step):
                    window = raw_cycles[start_idx:]
                    a_pass, b_pass, _, _ = simulate_challenge_sequence(
                        trade_outcomes=window,
                        risk_pct=risk,
                        target_profit_pct=10.0,
                        max_dd_pct=3.0,
                        fee_per_trade_pct=0.04
                    )
                    n_sims += 1
                    if a_pass and b_pass:
                        both_passed_cnt += 1
                    if a_pass:
                        a_passed_cnt += 1
                    if b_pass:
                        b_passed_cnt += 1
                    if a_pass or b_pass:
                        either_passed_cnt += 1

                if n_sims > 0:
                    both_rate = (both_passed_cnt / n_sims) * 100.0
                    a_rate = (a_passed_cnt / n_sims) * 100.0
                    b_rate = (b_passed_cnt / n_sims) * 100.0
                    either_rate = (either_passed_cnt / n_sims) * 100.0
                    results.append({
                        "Timeframe": tf,
                        "Config": cfg_name,
                        "Risk_Pct": risk,
                        "Simulations": n_sims,
                        "Both_Passed_Pct": both_rate,
                        "A_Passed_Pct": a_rate,
                        "B_Passed_Pct": b_rate,
                        "Either_Passed_Pct": either_rate
                    })

    # Sort results by Both_Passed_Pct descending
    results.sort(key=lambda x: x["Both_Passed_Pct"], reverse=True)

    print("\n" + "=" * 95)
    print("🏆 TOP PROP CHALLENGE CONFIGURATIONS (Target: +10% | Max DD: 3.0%)")
    print("=" * 95)
    print("{:<4} | {:<20} | {:<8} | {:<12} | {:<12} | {:<12} | {:<12}".format(
        "TF", "Config", "Risk/Trd", "BOTH PASS %", "A (BTC) Pass", "B (ETH) Pass", "EITHER Pass"
    ))
    print("-" * 95)
    for r in results[:15]:
        print("{:<4} | {:<20} | {:<7.2f}% | {:<11.1f}% | {:<11.1f}% | {:<11.1f}% | {:<11.1f}%".format(
            r["Timeframe"], r["Config"], r["Risk_Pct"],
            r["Both_Passed_Pct"], r["A_Passed_Pct"], r["B_Passed_Pct"], r["Either_Passed_Pct"]
        ))

    return results


if __name__ == "__main__":
    run_full_prop_optimization()
