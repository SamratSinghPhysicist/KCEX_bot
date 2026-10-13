"""
TP1 Sweep Analysis: Should We Raise TP1?
========================================
Tests TP1 levels from +0.15% to +0.60%:
- Evaluates the core trade-off:
  - Higher TP1 banks more profit when hit
  - BUT higher TP1 reduces the probability of banking early profit before hitting the -0.40% Early-Cut SL!
  - How does this impact Win Rate, Max Drawdown, Daily Drawdown, and Total Profit?

Tested across 2020-2026 (16,381 cycles):
- $1,000 account, $750/leg (1.5x Notional)
- Fee: 0.060% RT (Limit In + Market Out)
- BE Stop: Set to max(0.10%, TP1 / 2)
- TP2: +1.50%
- SL: -0.40% Early-Cut
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

def run_tp1_sweep():
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
    p_tp2 = 1.50
    cut_adv = 0.40    # Early cut at -0.40% MAE
    fee_rt = 0.060    # 0.060% Limit in + Market out
    leg_alloc = 0.75  # $750

    print("Extracting full cycle trajectories...")
    raw_cycles = []
    i = 0
    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        b_exit = None; e_exit = None
        b_series = []; e_series = []

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]; c_e = eth_dict[ts]

            fav_b = (c_b.high - p_b) / p_b * 100.0
            adv_b = (p_b - c_b.low) / p_b * 100.0
            b_low_rel = (c_b.low - p_b) / p_b * 100.0
            b_series.append((fav_b, adv_b, b_low_rel, ts))

            fav_e = (p_e - c_e.low) / p_e * 100.0
            adv_e = (c_e.high - p_e) / p_e * 100.0
            e_low_rel = (p_e - c_e.high) / p_e * 100.0
            e_series.append((fav_e, adv_e, e_low_rel, ts))

            if b_exit is None:
                if fav_b >= p_tp2 or adv_b >= cut_adv:
                    b_exit = j
            if e_exit is None:
                if fav_e >= p_tp2 or adv_e >= cut_adv:
                    e_exit = j

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)
        raw_cycles.append({
            "entry_ts": entry_ts,
            "exit_ts": common_times[free_idx],
            "b_series": b_series[:free_idx - i + 1],
            "e_series": e_series[:free_idx - i + 1]
        })
        i = free_idx + 1

    print(f"Extracted {len(raw_cycles)} cycles.")

    # Rolling start dates
    week_ms = 7 * 24 * 3600 * 1000
    start_times = []
    curr = raw_cycles[0]["entry_ts"]
    last_ts = raw_cycles[-1]["entry_ts"]
    while curr < last_ts - (30 * 24 * 3600 * 1000):
        start_times.append(curr)
        curr += week_ms

    tp1_options = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]

    print("\n" + "=" * 125)
    print("TP1 SWEEP ANALYSIS: EVALUATING WHETHER RAISING TP1 HELPS OR HURTS ($1,000 Acct, $750/leg, 0.060% fee)")
    print("=" * 125)
    print(f"{'TP1 Level':>10} | {'BE Lock':>8} | {'TP1 Hit Rate':>13} | {'Net Profit ($)':>15} | {'Worst Day Loss':>16} | {'Max Overall DD':>14} | {'Pass Rate':>10} | {'Avg Days':>9}")
    print("-" * 125)

    for tp1_val in tp1_options:
        # BE lock is set to min(0.10%, tp1_val - 0.05%) or 0.10%
        be_val = max(0.06, min(0.12, tp1_val - 0.10)) if tp1_val > 0.20 else 0.10

        tp1_hits = 0
        tot_legs = 0
        evaluated = []

        for c in raw_cycles:
            # BTC leg
            b_hit_tp1 = False
            b_return = None
            for fav, adv, low_rel, ts in c["b_series"]:
                if fav >= tp1_val and not b_hit_tp1:
                    b_hit_tp1 = True
                    tp1_hits += 1

                if b_hit_tp1:
                    if fav >= p_tp2:
                        b_return = 0.5 * tp1_val + 0.5 * p_tp2 - fee_rt
                        break
                    elif low_rel <= be_val:
                        b_return = 0.5 * tp1_val + 0.5 * be_val - fee_rt
                        break
                else:
                    if adv >= cut_adv:
                        b_return = -cut_adv - fee_rt
                        break
                    elif fav >= p_tp2:
                        b_return = 0.5 * tp1_val + 0.5 * p_tp2 - fee_rt
                        b_hit_tp1 = True
                        tp1_hits += 1
                        break
            if b_return is None:
                if b_hit_tp1:
                    b_return = 0.5 * tp1_val + 0.5 * be_val - fee_rt
                else:
                    b_return = -cut_adv - fee_rt
            tot_legs += 1

            # ETH leg
            e_hit_tp1 = False
            e_return = None
            for fav, adv, low_rel, ts in c["e_series"]:
                if fav >= tp1_val and not e_hit_tp1:
                    e_hit_tp1 = True
                    tp1_hits += 1

                if e_hit_tp1:
                    if fav >= p_tp2:
                        e_return = 0.5 * tp1_val + 0.5 * p_tp2 - fee_rt
                        break
                    elif low_rel <= be_val:
                        e_return = 0.5 * tp1_val + 0.5 * be_val - fee_rt
                        break
                else:
                    if adv >= cut_adv:
                        e_return = -cut_adv - fee_rt
                        break
                    elif fav >= p_tp2:
                        e_return = 0.5 * tp1_val + 0.5 * p_tp2 - fee_rt
                        e_hit_tp1 = True
                        tp1_hits += 1
                        break
            if e_return is None:
                if e_hit_tp1:
                    e_return = 0.5 * tp1_val + 0.5 * be_val - fee_rt
                else:
                    e_return = -cut_adv - fee_rt
            tot_legs += 1

            evaluated.append({
                "entry_ts": c["entry_ts"],
                "exit_ts": c["exit_ts"],
                "b_return": b_return,
                "e_return": e_return
            })

        hit_rate_pct = tp1_hits / tot_legs * 100.0

        # Full history metrics
        day_pnl = defaultdict(float)
        full_bal = 1000.0
        full_peak = 1000.0
        full_max_dd = 0.0

        for ec in evaluated:
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
        tot_net = full_bal - 1000.0

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

            for ec in evaluated:
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

        print(f"+{tp1_val:.2f}%{'':<4} | +{be_val:.2f}%{'':<2} | {hit_rate_pct:>12.1f}% | ${tot_net:>+14,.2f} | -${abs(worst_day_loss):>5.2f} (-{worst_day_pct:>4.2f}%) | {full_max_dd:>13.2f}% | {pass_rate:>9.1f}% | {avg_days:>7.1f} d")

if __name__ == "__main__":
    run_tp1_sweep()
