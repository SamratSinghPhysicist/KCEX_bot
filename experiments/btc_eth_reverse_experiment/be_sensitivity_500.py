"""
Sensitivity Analysis of Breakeven (BE) Lock Levels: +0.05%, +0.06%, +0.09%
=============================================================================
Tests across 3 Fee Tiers:
- Tier 1: 0.030% (Limit In + Limit Out)
- Tier 2: 0.060% (Limit In + Market Out)
- Tier 3: 0.090% (Market In + Market Out)

Account: $1,000 balance, $750 per leg (1.5x Notional)
Measures:
1. TP2 (+1.50%) Full Runner Fill Count (does a tighter BE choke off runners?)
2. BE Stopout Count
3. Total Net Profit ($) on $1k account
4. Worst Day Loss ($ and %)
5. Max Overall Drawdown (%)
6. Challenge Pass Rate (%) & Avg Days to Pass
"""

import os
import sys
import datetime
from collections import defaultdict

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    load_candles_from_dir,
    parse_date_to_ms
)

def run_be_sensitivity():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2020-01-01")
    end_ms = parse_date_to_ms("2026-09-30") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    tot_len = len(common_times)
    p_tp = 1.50       # final TP +1.50%
    p_sl = 1.50       # base SL
    part_price = 0.20 # partial TP +0.20%
    cut_adv = 0.40    # Early cut at -0.40% MAE

    # Extract all raw cycles with full candle-by-candle trajectory
    print("Extracting cycle candle data...")
    cycles = []
    i = 0
    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        tp_b = p_b * (1.0 + p_tp / 100.0)
        sl_b = p_b * (1.0 - p_sl / 100.0)
        tp_e = p_e * (1.0 - p_tp / 100.0)
        sl_e = p_e * (1.0 + p_sl / 100.0)

        b_exit = None; e_exit = None
        b_series = []; e_series = []

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]; c_e = eth_dict[ts]

            fav_b = (c_b.high - p_b) / p_b * 100.0
            adv_b = (p_b - c_b.low) / p_b * 100.0
            # Also store candle low/high relative to entry to know exact range
            b_low_rel = (c_b.low - p_b) / p_b * 100.0
            b_series.append((fav_b, adv_b, b_low_rel, ts))

            fav_e = (p_e - c_e.low) / p_e * 100.0
            adv_e = (c_e.high - p_e) / p_e * 100.0
            e_low_rel = (p_e - c_e.high) / p_e * 100.0
            e_series.append((fav_e, adv_e, e_low_rel, ts))

            if b_exit is None:
                if c_b.high >= tp_b or c_b.low <= sl_b or adv_b >= cut_adv:
                    b_exit = j
            if e_exit is None:
                if c_e.low <= tp_e or c_e.high >= sl_e or adv_e >= cut_adv:
                    e_exit = j

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)
        cycles.append({
            "entry_ts": entry_ts,
            "exit_ts": common_times[free_idx],
            "b_series": b_series[:free_idx - i + 1],
            "e_series": e_series[:free_idx - i + 1]
        })
        i = free_idx + 1

    print(f"Extracted {len(cycles)} cycles.")

    # Rolling start dates
    week_ms = 7 * 24 * 3600 * 1000
    start_times = []
    curr = cycles[0]["entry_ts"]
    last_ts = cycles[-1]["entry_ts"]
    while curr < last_ts - (30 * 24 * 3600 * 1000):
        start_times.append(curr)
        curr += week_ms

    fee_tiers = [
        ("Tier 1: Limit In + Limit Out (0.030% RT)", 0.030),
        ("Tier 2: Limit In + Market Out (0.060% RT)", 0.060),
        ("Tier 3: Market In + Market Out (0.090% RT)", 0.090)
    ]

    be_options = [0.05, 0.06, 0.09]
    leg_alloc = 0.75 # $750 per leg

    for fee_label, fee_rt in fee_tiers:
        print("\n" + "=" * 115)
        print(f"FEE LEVEL: {fee_label} | CAPITAL: $1,000 | SIZE: $750/LEG (1.5x NOTIONAL)")
        print("=" * 115)
        print(f"{'BE Stop Level':>13} | {'TP2 Runners':>11} | {'BE Stops':>9} | {'Net Profit ($)':>15} | {'Worst Day DD':>13} | {'Max DD':>8} | {'Pass Rate':>10} | {'Avg Days':>10}")
        print("-" * 115)

        for be_val in be_options:
            tp2_count = 0
            be_count = 0
            evaluated_cycles = []

            for c in cycles:
                # Evaluate BTC
                b_hit_partial = False
                b_return = None
                for fav, adv, low_rel, ts in c["b_series"]:
                    if fav >= part_price and not b_hit_partial:
                        b_hit_partial = True

                    if b_hit_partial:
                        # Once partial hit, check if hits TP2 or falls to be_val
                        if fav >= p_tp:
                            b_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                            tp2_count += 1
                            break
                        # If candle low dips below be_val, stopped out at be_val!
                        elif low_rel <= be_val:
                            b_return = 0.5 * part_price + 0.5 * be_val - fee_rt
                            be_count += 1
                            break
                    else:
                        if adv >= cut_adv:
                            b_return = -cut_adv - fee_rt
                            break
                        elif fav >= p_tp:
                            b_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                            tp2_count += 1
                            break
                if b_return is None:
                    if b_hit_partial:
                        b_return = 0.5 * part_price + 0.5 * be_val - fee_rt
                        be_count += 1
                    else:
                        b_return = -cut_adv - fee_rt

                # Evaluate ETH
                e_hit_partial = False
                e_return = None
                for fav, adv, low_rel, ts in c["e_series"]:
                    if fav >= part_price and not e_hit_partial:
                        e_hit_partial = True

                    if e_hit_partial:
                        if fav >= p_tp:
                            e_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                            tp2_count += 1
                            break
                        elif low_rel <= be_val:
                            e_return = 0.5 * part_price + 0.5 * be_val - fee_rt
                            be_count += 1
                            break
                    else:
                        if adv >= cut_adv:
                            e_return = -cut_adv - fee_rt
                            break
                        elif fav >= p_tp:
                            e_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                            tp2_count += 1
                            break
                if e_return is None:
                    if e_hit_partial:
                        e_return = 0.5 * part_price + 0.5 * be_val - fee_rt
                        be_count += 1
                    else:
                        e_return = -cut_adv - fee_rt

                evaluated_cycles.append({
                    "entry_ts": c["entry_ts"],
                    "exit_ts": c["exit_ts"],
                    "b_return": b_return,
                    "e_return": e_return
                })

            # Calculate full history metrics
            day_pnl = defaultdict(float)
            full_bal = 1000.0
            full_peak = 1000.0
            full_max_dd = 0.0

            for ec in evaluated_cycles:
                pnl = (1000.0 * leg_alloc * ec["b_return"] / 100.0) + (1000.0 * leg_alloc * ec["e_return"] / 100.0)
                dt = datetime.datetime.fromtimestamp(ec["exit_ts"] / 1000.0, datetime.timezone.utc)
                day_str = dt.strftime('%Y-%m-%d')
                day_pnl[day_str] += pnl

                full_bal += pnl
                if full_bal > full_peak: full_peak = full_bal
                dd = (full_peak - full_bal) / full_peak * 100.0
                if dd > full_max_dd: full_max_dd = dd

            worst_day_loss = min(day_pnl.values())
            worst_day_pct = abs(worst_day_loss) / 1000.0 * 100.0
            tot_net_profit = full_bal - 1000.0

            # Rolling challenge
            passed = 0
            days_to_pass = []
            for st in start_times:
                acct_bal = 1000.0
                acct_peak = 1000.0
                start_date = None
                current_day_str = None
                day_start_bal = acct_bal
                failed = False

                for ec in evaluated_cycles:
                    if ec["entry_ts"] < st: continue
                    dt = datetime.datetime.fromtimestamp(ec["exit_ts"] / 1000.0, datetime.timezone.utc)
                    c_day_str = dt.strftime('%Y-%m-%d')
                    if start_date is None: start_date = ec["exit_ts"]
                    if c_day_str != current_day_str:
                        current_day_str = c_day_str
                        day_start_bal = acct_bal

                    pnl = (1000.0 * leg_alloc * ec["b_return"] / 100.0) + (1000.0 * leg_alloc * ec["e_return"] / 100.0)
                    acct_bal += pnl

                    if (day_start_bal - acct_bal) / day_start_bal * 100.0 >= 3.0:
                        failed = True; break
                    if acct_bal > acct_peak: acct_peak = acct_bal
                    if (acct_peak - acct_bal) / acct_peak * 100.0 >= 5.0:
                        failed = True; break

                    if acct_bal >= 1100.0:
                        passed += 1
                        days_taken = (ec["exit_ts"] - start_date) / (1000.0 * 86400.0)
                        days_to_pass.append(days_taken)
                        break

            pass_rate = passed / len(start_times) * 100.0
            avg_days = sum(days_to_pass) / len(days_to_pass) if days_to_pass else 0.0

            label_be = f"+{be_val:.2f}%"
            print(f"{label_be:>13} | {tp2_count:>11} | {be_count:>9} | ${tot_net_profit:>+14,.2f} | -${abs(worst_day_loss):>5.2f} (-{worst_day_pct:>4.2f}%) | {full_max_dd:>7.2f}% | {pass_rate:>9.1f}% | {avg_days:>8.1f} d")

if __name__ == "__main__":
    run_be_sensitivity()
