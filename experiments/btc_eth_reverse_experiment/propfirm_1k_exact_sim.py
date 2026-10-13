"""
Prop Firm Simulation for $1,000 Account:
- Balance: $1,000
- Daily Drawdown Limit: 3.0% ($30.00)
- Max Drawdown Limit: 5.0% ($50.00)
- Profit Target: 10.0% ($100.00)
- Round-Trip Fees: 0.09% (Taker 0.045% in + 0.045% out)
- Data: 2020-01-01 to 2026-09-30 (2,464 calendar days, 16,381 cycles)
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

def run_1k_simulation():
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
    rt_fee = 0.09     # 0.09% round-trip fee
    p_tp = 1.50       # final TP +1.50%
    p_sl = 1.50       # base SL
    part_price = 0.20 # partial TP +0.20%
    cut_adv = 0.40    # Early cut at -0.40% MAE

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

        # BTC return calculation
        b_hit_partial = False
        b_return = None
        for fav, adv, ts in b_series[:free_idx - i + 1]:
            if fav >= part_price and not b_hit_partial:
                b_hit_partial = True
            if b_hit_partial:
                if fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - rt_fee
                    break
                elif adv > 0 and fav < 0.05:
                    b_return = 0.5 * part_price + 0.5 * 0.05 - rt_fee
                    break
            else:
                if adv >= cut_adv:
                    b_return = -cut_adv - rt_fee
                    break
                elif fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - rt_fee
                    break
        if b_return is None:
            if b_hit_partial:
                b_return = 0.5 * part_price + 0.5 * 0.05 - rt_fee
            else:
                b_return = -cut_adv - rt_fee

        # ETH return calculation
        e_hit_partial = False
        e_return = None
        for fav, adv, ts in e_series[:free_idx - i + 1]:
            if fav >= part_price and not e_hit_partial:
                e_hit_partial = True
            if e_hit_partial:
                if fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - rt_fee
                    break
                elif adv > 0 and fav < 0.05:
                    e_return = 0.5 * part_price + 0.5 * 0.05 - rt_fee
                    break
            else:
                if adv >= cut_adv:
                    e_return = -cut_adv - rt_fee
                    break
                elif fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - rt_fee
                    break
        if e_return is None:
            if e_hit_partial:
                e_return = 0.5 * part_price + 0.5 * 0.05 - rt_fee
            else:
                e_return = -cut_adv - rt_fee

        cycles.append({
            "entry_ts": entry_ts,
            "exit_ts": common_times[free_idx],
            "b_return": b_return,
            "e_return": e_return
        })
        i = free_idx + 1

    print(f"Extracted {len(cycles)} cycles.")

    # Rolling evaluation starting every 7 days across 2020-2026
    week_ms = 7 * 24 * 3600 * 1000
    start_times = []
    curr = cycles[0]["entry_ts"]
    last_ts = cycles[-1]["entry_ts"]
    while curr < last_ts - (30 * 24 * 3600 * 1000):
        start_times.append(curr)
        curr += week_ms

    notional_options = [
        (0.25, "$250 per leg", "0.50x Notional"),
        (0.35, "$350 per leg", "0.70x Notional"),
        (0.50, "$500 per leg", "1.00x Notional"),
        (0.60, "$600 per leg", "1.20x Notional"),
        (0.75, "$750 per leg", "1.50x Notional"),
        (1.00, "$1,000 per leg", "2.00x Notional"),
        (1.25, "$1,250 per leg", "2.50x Notional"),
        (1.50, "$1,500 per leg", "3.00x Notional")
    ]

    print("\n" + "=" * 105)
    print("SIMULATION RESULTS: $1,000 PROP ACCOUNT (3% DAILY DD / 5% MAX DD / 10% TARGET / 0.09% FEES)")
    print("=" * 105)
    print(f"{'Position Size Per Leg':>22} | {'Total Notional':>14} | {'Worst Day Loss':>16} | {'Max Overall DD':>15} | {'Pass Rate':>10} | {'Avg Days to Pass':>16}")
    print("-" * 105)

    for leg_alloc, label_size, label_tot in notional_options:
        # Check worst calendar day over full 6.75 years
        day_pnl = defaultdict(float)
        full_bal = 1000.0
        full_peak = 1000.0
        full_max_dd = 0.0

        for c in cycles:
            # dollar PnL on $1k base
            pnl_usd = (1000.0 * leg_alloc * c["b_return"] / 100.0) + (1000.0 * leg_alloc * c["e_return"] / 100.0)
            dt = datetime.datetime.fromtimestamp(c["exit_ts"] / 1000.0, datetime.timezone.utc)
            day_str = dt.strftime('%Y-%m-%d')
            day_pnl[day_str] += pnl_usd

            full_bal += pnl_usd
            if full_bal > full_peak:
                full_peak = full_bal
            dd = (full_peak - full_bal) / full_peak * 100.0
            if dd > full_max_dd:
                full_max_dd = dd

        worst_day_loss = min(day_pnl.values())
        worst_day_pct = abs(worst_day_loss) / 1000.0 * 100.0

        # Rolling challenge progression
        passed = 0
        failed_daily = 0
        failed_max = 0
        days_to_pass = []

        for st in start_times:
            acct_bal = 1000.0
            acct_peak = 1000.0
            start_date = None
            current_day_str = None
            day_start_bal = acct_bal

            for c in cycles:
                if c["entry_ts"] < st:
                    continue

                dt = datetime.datetime.fromtimestamp(c["exit_ts"] / 1000.0, datetime.timezone.utc)
                c_day_str = dt.strftime('%Y-%m-%d')
                if start_date is None:
                    start_date = c["exit_ts"]

                if c_day_str != current_day_str:
                    current_day_str = c_day_str
                    day_start_bal = acct_bal

                pnl_usd = (1000.0 * leg_alloc * c["b_return"] / 100.0) + (1000.0 * leg_alloc * c["e_return"] / 100.0)
                acct_bal += pnl_usd

                # Daily DD check (3.0% = $30.00 from day start)
                daily_loss_pct = (day_start_bal - acct_bal) / day_start_bal * 100.0
                if daily_loss_pct >= 3.0:
                    failed_daily += 1
                    break

                # Max DD check (5.0% = $50.00 from peak)
                if acct_bal > acct_peak:
                    acct_peak = acct_bal
                trailing_dd_pct = (acct_peak - acct_bal) / acct_peak * 100.0
                if trailing_dd_pct >= 5.0:
                    failed_max += 1
                    break

                # Target check (+10% = $1,100 balance)
                if acct_bal >= 1100.0:
                    passed += 1
                    days_taken = (c["exit_ts"] - start_date) / (1000.0 * 86400.0)
                    days_to_pass.append(days_taken)
                    break

        pass_rate = passed / len(start_times) * 100.0
        avg_days = sum(days_to_pass) / len(days_to_pass) if days_to_pass else 0.0

        print(f"{label_size:>22} | {label_tot:>14} | -${abs(worst_day_loss):>5.2f} (-{worst_day_pct:>4.2f}%) | {full_max_dd:>14.2f}% | {pass_rate:>9.1f}% | {avg_days:>14.1f} days")

if __name__ == "__main__":
    run_1k_simulation()
