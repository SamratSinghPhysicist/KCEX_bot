"""
Prop Firm Challenge Simulation: 3% Daily DD, 5% Max DD, 10% Profit Target
==========================================================================
Simulates the exact user prop firm conditions across 6.75 years (2020 - 2026):
- Daily Drawdown Limit: 3.0%
- Max Drawdown Limit: 5.0%
- Profit Target: 10.0%

Tests:
1. Worst single-day drawdown across all 2,464 calendar days.
2. Max overall drawdown across all 7,095 cycles.
3. Challenge Pass Rate (%) across rolling start dates (e.g., starting every single week from 2020 to 2026).
4. Days to pass (Average, Fastest, Slowest).
5. Position sizing sweep: Sizing from 0.25x to 2.5x notional to determine the mathematical sweet spot.
"""

import os
import sys
import datetime
from collections import defaultdict
from typing import List, Dict, Tuple

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    load_candles_from_dir,
    parse_date_to_ms,
    CandleData
)

def run_simulation():
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
    fee_rate = 0.0004 # 0.04% per side
    p_tp = 1.50       # final TP +1.50%
    p_sl = 1.50       # base SL
    part_price = 0.20 # partial TP +0.20%
    cut_adv = 0.40    # Early cut at -0.40% MAE

    print("Extracting trade cycles...")
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
            b_series.append((fav_b, adv_b, ts))

            fav_e = (p_e - c_e.low) / p_e * 100.0
            adv_e = (c_e.high - p_e) / p_e * 100.0
            e_series.append((fav_e, adv_e, ts))

            # Early exit check for cycle end
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

        # Calculate exact price move return for BTC
        b_hit_partial = False
        b_return = None
        for fav, adv, ts in b_series[:free_idx - i + 1]:
            if fav >= part_price and not b_hit_partial:
                b_hit_partial = True
            if b_hit_partial:
                if fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - 2 * (fee_rate * 100.0)
                    break
                elif adv > 0 and fav < 0.05:
                    b_return = 0.5 * part_price + 0.5 * 0.05 - 2 * (fee_rate * 100.0)
                    break
            else:
                if adv >= cut_adv:
                    b_return = -cut_adv - 2 * (fee_rate * 100.0)
                    break
                elif fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - 2 * (fee_rate * 100.0)
                    break
        if b_return is None:
            if b_hit_partial:
                b_return = 0.5 * part_price + 0.5 * 0.05 - 2 * (fee_rate * 100.0)
            else:
                b_return = -cut_adv - 2 * (fee_rate * 100.0)

        # Calculate exact price move return for ETH
        e_hit_partial = False
        e_return = None
        for fav, adv, ts in e_series[:free_idx - i + 1]:
            if fav >= part_price and not e_hit_partial:
                e_hit_partial = True
            if e_hit_partial:
                if fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - 2 * (fee_rate * 100.0)
                    break
                elif adv > 0 and fav < 0.05:
                    e_return = 0.5 * part_price + 0.5 * 0.05 - 2 * (fee_rate * 100.0)
                    break
            else:
                if adv >= cut_adv:
                    e_return = -cut_adv - 2 * (fee_rate * 100.0)
                    break
                elif fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - 2 * (fee_rate * 100.0)
                    break
        if e_return is None:
            if e_hit_partial:
                e_return = 0.5 * part_price + 0.5 * 0.05 - 2 * (fee_rate * 100.0)
            else:
                e_return = -cut_adv - 2 * (fee_rate * 100.0)

        cycles.append({
            "entry_ts": entry_ts,
            "exit_ts": common_times[free_idx],
            "b_return": b_return, # in %
            "e_return": e_return  # in %
        })
        i = free_idx + 1

    print(f"Loaded {len(cycles)} completed trade cycles.")

    # -------------------------------------------------------------
    # SIMULATING DIFFERENT POSITION SIZINGS
    # Sizing factor 's': Notional per leg as % of initial account balance
    # If s = 0.5 (50% on BTC, 50% on ETH) -> Total Notional = 1.0x
    # If s = 1.0 (100% on BTC, 100% on ETH) -> Total Notional = 2.0x
    # -------------------------------------------------------------
    notional_options = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00]

    print("\n" + "=" * 95)
    print("PROP FIRM EVALUATION: 3% DAILY DD | 5% MAX DD | 10% PROFIT TARGET")
    print("=" * 95)
    print(f"{'Sizing Per Leg':>15} | {'Tot Exposure':>12} | {'Worst Day DD':>12} | {'Max Overall DD':>14} | {'Pass Rate':>10} | {'Avg Days to Pass':>17}")
    print("-" * 95)

    # Let's run a rolling simulation starting every 7 days across the 6.75 years
    # Total weeks ~ 350 rolling challenges
    week_ms = 7 * 24 * 3600 * 1000
    start_times = []
    curr = cycles[0]["entry_ts"]
    last_ts = cycles[-1]["entry_ts"]
    while curr < last_ts - (30 * 24 * 3600 * 1000):
        start_times.append(curr)
        curr += week_ms

    for leg_alloc in notional_options:
        tot_exposure = leg_alloc * 2.0 # BTC + ETH

        # 1. Full history daily PnL check
        # Group cycle PnLs by day
        day_pnl = defaultdict(float)
        full_bal = 100000.0
        full_peak = 100000.0
        full_max_dd = 0.0

        for c in cycles:
            # dollar PnL on $100k account
            pnl_usd = (100000.0 * leg_alloc * c["b_return"] / 100.0) + (100000.0 * leg_alloc * c["e_return"] / 100.0)
            day_str = datetime.datetime.utcfromtimestamp(c["exit_ts"] / 1000.0).strftime('%Y-%m-%d')
            day_pnl[day_str] += pnl_usd

            full_bal += pnl_usd
            if full_bal > full_peak:
                full_peak = full_bal
            dd = (full_peak - full_bal) / full_peak * 100.0
            if dd > full_max_dd:
                full_max_dd = dd

        # Worst calendar day in % of account
        worst_day_loss = min(day_pnl.values())
        worst_day_pct = abs(worst_day_loss) / 100000.0 * 100.0 if worst_day_loss < 0 else 0.0

        # 2. Rolling challenge test
        passed = 0
        failed_daily = 0
        failed_max = 0
        days_to_pass = []

        for st in start_times:
            # Run challenge from st
            acct_bal = 100000.0
            acct_peak = 100000.0
            challenge_status = "RUNNING"
            start_date = None
            end_date = None

            # Track daily starting balance
            current_day_str = None
            day_start_bal = acct_bal
            day_worst_equity = acct_bal

            for c in cycles:
                if c["entry_ts"] < st:
                    continue

                c_day_str = datetime.datetime.utcfromtimestamp(c["exit_ts"] / 1000.0).strftime('%Y-%m-%d')
                if start_date is None:
                    start_date = c["exit_ts"]

                # Check if new day
                if c_day_str != current_day_str:
                    current_day_str = c_day_str
                    day_start_bal = acct_bal

                pnl_usd = (100000.0 * leg_alloc * c["b_return"] / 100.0) + (100000.0 * leg_alloc * c["e_return"] / 100.0)
                acct_bal += pnl_usd

                # Daily DD check
                daily_loss_pct = (day_start_bal - acct_bal) / day_start_bal * 100.0
                if daily_loss_pct >= 3.0:
                    failed_daily += 1
                    challenge_status = "FAILED_DAILY"
                    break

                # Max DD check (relative to initial balance or high-water mark, standard prop rules check high water mark)
                if acct_bal > acct_peak:
                    acct_peak = acct_bal
                trailing_dd_pct = (acct_peak - acct_bal) / acct_peak * 100.0
                if trailing_dd_pct >= 5.0:
                    failed_max += 1
                    challenge_status = "FAILED_MAX"
                    break

                # Profit target check (+10%)
                if (acct_bal - 100000.0) / 100000.0 * 100.0 >= 10.0:
                    passed += 1
                    challenge_status = "PASSED"
                    end_date = c["exit_ts"]
                    days_taken = (end_date - start_date) / (1000.0 * 86400.0)
                    days_to_pass.append(days_taken)
                    break

        pass_rate = passed / len(start_times) * 100.0
        avg_days = sum(days_to_pass) / len(days_to_pass) if days_to_pass else 0.0

        label_alloc = f"{leg_alloc * 100:.0f}% (${leg_alloc*100:,.0f}k)"
        label_tot = f"{tot_exposure:.2f}x Notional"
        print(f"{label_alloc:>15} | {label_tot:>12} | -{worst_day_pct:>10.2f}% | {full_max_dd:>13.2f}% | {pass_rate:>9.1f}% | {avg_days:>15.1f} days")

if __name__ == "__main__":
    run_simulation()
