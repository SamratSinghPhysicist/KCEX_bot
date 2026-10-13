"""
Challenge Duration and Time-to-Pass Analysis
============================================
Calculates:
1. Number of trades required to reach +10% profit target.
2. Individual trade holding durations (hours).
3. Calendar time (days / weeks) to pass:
   - For Account A (BTC)
   - For Account B (ETH)
   - For BOTH Accounts to pass
4. Distribution: Min, Median, Mean, 75th percentile, Max days.
Tested across all rolling challenge starts in 2025-2026 data.
"""

import os
import sys
import math
from typing import List, Dict, Tuple

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    load_candles_from_dir,
    build_sub_1m_map,
    evaluate_candle_tp_sl,
    parse_date_to_ms,
    CandleData
)

def analyze_time_to_pass():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2025-01-01")
    end_ms = parse_date_to_ms("2026-10-12") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
    eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_sub = build_sub_1m_map(btc_c, btc_1m)
    eth_sub = build_sub_1m_map(eth_c, eth_1m)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    # Config 1: TP 3.0%, SL 3.0%, Partial TP at 0.30%
    tp_pct = 3.0
    sl_pct = 3.0
    part_tp = 0.30
    margin_frac = 0.20
    leverage = 2.0
    pos_mult = margin_frac * leverage # 0.40

    # Build all trade cycles with precise entry and exit timestamps
    cycles = []
    i = 0
    tot_len = len(common_times)

    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        tp_b = p_b * (1.0 + tp_pct / 100.0)
        sl_b = p_b * (1.0 - sl_pct / 100.0)
        tp_e = p_e * (1.0 - tp_pct / 100.0)
        sl_e = p_e * (1.0 + sl_pct / 100.0)

        b_exit = None; b_res = None; b_mfe = 0.0
        e_exit = None; e_res = None; e_mfe = 0.0

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]
            c_e = eth_dict[ts]

            if b_exit is None:
                sub_b = btc_sub.get(ts, [])
                if sub_b:
                    for mc in sub_b:
                        fav = (mc.high - p_b) / p_b * 100.0
                        if fav > b_mfe: b_mfe = fav
                        if mc.low <= sl_b: b_exit = j; b_res = "SL"; break
                        elif mc.high >= tp_b: b_exit = j; b_res = "TP"; break
                else:
                    fav = (c_b.high - p_b) / p_b * 100.0
                    if fav > b_mfe: b_mfe = fav
                    r, _ = evaluate_candle_tp_sl("LONG", p_b, tp_b, sl_b, c_b, btc_sub, timeframe)
                    if r: b_exit = j; b_res = r

            if e_exit is None:
                sub_e = eth_sub.get(ts, [])
                if sub_e:
                    for mc in sub_e:
                        fav = (p_e - mc.low) / p_e * 100.0
                        if fav > e_mfe: e_mfe = fav
                        if mc.high >= sl_e: e_exit = j; e_res = "SL"; break
                        elif mc.low <= tp_e: e_exit = j; e_res = "TP"; break
                else:
                    fav = (p_e - c_e.low) / p_e * 100.0
                    if fav > e_mfe: e_mfe = fav
                    r, _ = evaluate_candle_tp_sl("SHORT", p_e, tp_e, sl_e, c_e, eth_sub, timeframe)
                    if r: e_exit = j; e_res = r

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)
        exit_ts = common_times[free_idx]
        hold_hours = free_idx - i + 1

        # Calculate PnL with partial TP 0.30%
        if b_mfe >= part_tp:
            gain_b = (0.5 * part_tp + 0.5 * tp_pct) if b_res == "TP" else (0.5 * part_tp + 0.5 * 0.05)
        else:
            gain_b = -sl_pct

        if e_mfe >= part_tp:
            gain_e = (0.5 * part_tp + 0.5 * tp_pct) if e_res == "TP" else (0.5 * part_tp + 0.5 * 0.05)
        else:
            gain_e = -sl_pct

        cycles.append({
            "entry_ts": entry_ts,
            "exit_ts": exit_ts,
            "hold_hours": hold_hours,
            "gain_b": gain_b,
            "gain_e": gain_e,
            "b_mfe": b_mfe,
            "e_mfe": e_mfe
        })

        i = free_idx + 1

    print(f"Total Cycles: {len(cycles)}")
    hold_hours_all = [c["hold_hours"] for c in cycles]
    avg_hold = sum(hold_hours_all) / len(hold_hours_all)
    sorted_hold = sorted(hold_hours_all)
    med_hold = sorted_hold[len(sorted_hold) // 2]
    print(f"Single Trade Holding Duration: Avg = {avg_hold:.1f} hours ({avg_hold/24:.1f} days) | Median = {med_hold} hours ({med_hold/24:.1f} days)")

    # Simulate challenges starting across time
    # Track days to pass and trades to pass
    a_pass_days = []
    b_pass_days = []
    both_pass_days = []
    a_trades_cnt = []
    b_trades_cnt = []
    both_trades_cnt = []

    step = 1 # Test starting every single trade cycle
    for s_idx in range(len(cycles)):
        window = cycles[s_idx:]
        start_ts = window[0]["entry_ts"]
        bal_a, peak_a, stat_a, a_pass_ts, a_cnt = 1000.0, 1000.0, "RUNNING", None, 0
        bal_b, peak_b, stat_b, b_pass_ts, b_cnt = 1000.0, 1000.0, "RUNNING", None, 0

        for c in window:
            # Step A
            if stat_a == "RUNNING":
                a_cnt += 1
                bal_a += bal_a * (pos_mult * c["gain_b"] / 100.0)
                if bal_a > peak_a: peak_a = bal_a
                dd_a = (peak_a - bal_a) / peak_a * 100.0
                if dd_a >= 3.0:
                    stat_a = "FAILED"
                elif ((bal_a - 1000.0) / 1000.0 * 100.0) >= 10.0:
                    stat_a = "PASSED"
                    a_pass_ts = c["exit_ts"]

            # Step B
            if stat_b == "RUNNING":
                b_cnt += 1
                bal_b += bal_b * (pos_mult * c["gain_e"] / 100.0)
                if bal_b > peak_b: peak_b = bal_b
                dd_b = (peak_b - bal_b) / peak_b * 100.0
                if dd_b >= 3.0:
                    stat_b = "FAILED"
                elif ((bal_b - 1000.0) / 1000.0 * 100.0) >= 10.0:
                    stat_b = "PASSED"
                    b_pass_ts = c["exit_ts"]

            if stat_a != "RUNNING" and stat_b != "RUNNING":
                break

        if stat_a == "PASSED":
            days_a = (a_pass_ts - start_ts) / (1000 * 3600 * 24)
            a_pass_days.append(days_a)
            a_trades_cnt.append(a_cnt)

        if stat_b == "PASSED":
            days_b = (b_pass_ts - start_ts) / (1000 * 3600 * 24)
            b_pass_days.append(days_b)
            b_trades_cnt.append(b_cnt)

        if stat_a == "PASSED" and stat_b == "PASSED":
            both_ts = max(a_pass_ts, b_pass_ts)
            days_both = (both_ts - start_ts) / (1000 * 3600 * 24)
            both_pass_days.append(days_both)
            both_trades_cnt.append(max(a_cnt, b_cnt))

    def print_dist(name, arr, unit="days"):
        if not arr:
            print(f"{name}: No data")
            return
        sorted_arr = sorted(arr)
        n = len(sorted_arr)
        min_v = sorted_arr[0]
        p25 = sorted_arr[int(n * 0.25)]
        med_v = sorted_arr[n // 2]
        mean_v = sum(sorted_arr) / n
        p75 = sorted_arr[int(n * 0.75)]
        p90 = sorted_arr[int(n * 0.90)]
        max_v = sorted_arr[-1]
        print(f"\n--- {name} (N={n} successful runs) ---")
        print(f"  Fastest (Min):      {min_v:.1f} {unit}")
        print(f"  25th Percentile:    {p25:.1f} {unit}")
        print(f"  Median (Typical):   {med_v:.1f} {unit}")
        print(f"  Average (Mean):     {mean_v:.1f} {unit}")
        print(f"  75th Percentile:    {p75:.1f} {unit}")
        print(f"  90th Percentile:    {p90:.1f} {unit}")
        print(f"  Slowest (Max):      {max_v:.1f} {unit}")

    print_dist("Time to Pass: Account A (BTC)", a_pass_days, "days")
    print_dist("Trades to Pass: Account A (BTC)", a_trades_cnt, "trades")

    print_dist("Time to Pass: Account B (ETH)", b_pass_days, "days")
    print_dist("Trades to Pass: Account B (ETH)", b_trades_cnt, "trades")

    print_dist("Time to Pass: BOTH Accounts", both_pass_days, "days")
    print_dist("Trades to Pass: BOTH Accounts", both_trades_cnt, "trades")

if __name__ == "__main__":
    analyze_time_to_pass()
