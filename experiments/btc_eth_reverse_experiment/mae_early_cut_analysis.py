"""
MAE Analysis and Early-Cut Optimization on 7,095 Historical Cycles (2020-2026)
=============================================================================
Analyzes:
1. On profitable/winning trades: How far against entry does price move before winning?
   (Distribution of MAE on winning trades: Median, 75th, 90th, 95th, 99th, Max)
2. Tests the User's hypothesis:
   What if we cut a trade immediately as soon as it crosses the MAE threshold of winners,
   instead of letting it bleed to the full -1.50% Stop Loss?
3. Measures net impact on Total Profit, Win Rate, Max Drawdown, and Expectancy.
"""

import os
import sys
import math
from collections import defaultdict
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

def run_mae_cut_analysis():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2020-01-01")
    end_ms = parse_date_to_ms("2026-09-30") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    leverage = 2.0
    fee_rate = 0.0004
    p_tp = 1.50       # 1.50% price move -> 3.0% profit
    p_sl = 1.50       # default SL
    part_price = 0.20 # partial TP at 0.20% price move

    # Case 1: Long BTC, Short ETH
    b_dir = "LONG"
    e_dir = "SHORT"
    tot_len = len(common_times)

    print("=" * 85)
    print("MAXIMUM ADVERSE EXCURSION (MAE) ANALYSIS ON PROFITABLE TRADES")
    print(f"Dataset: 2020-01-01 to 2026-09-30 ({tot_len} candles, 6.75 years)")
    print("=" * 85)

    # First pass: collect detailed candle-by-candle trajectory of every cycle
    cycles_data = []
    i = 0
    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        tp_b = p_b * (1.0 + p_tp / 100.0)
        sl_b = p_b * (1.0 - p_sl / 100.0)
        tp_e = p_e * (1.0 - p_tp / 100.0)
        sl_e = p_e * (1.0 + p_sl / 100.0)

        b_exit = None; b_res = None; b_mfe = 0.0; b_mae = 0.0
        e_exit = None; e_res = None; e_mfe = 0.0; e_mae = 0.0

        # We track candle-by-candle series for later test of different cut levels
        # b_series: list of (fav_b, adv_b) per candle
        b_series = []
        e_series = []

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]; c_e = eth_dict[ts]

            # BTC Long: fav is (high - p_b), adv is (p_b - low)
            fav_b = (c_b.high - p_b) / p_b * 100.0
            adv_b = (p_b - c_b.low) / p_b * 100.0
            b_series.append((fav_b, adv_b, c_b.open_time_ms))

            if b_exit is None:
                if fav_b > b_mfe: b_mfe = fav_b
                if adv_b > b_mae: b_mae = adv_b
                hit_tp = (c_b.high >= tp_b)
                hit_sl = (c_b.low <= sl_b)
                if hit_tp and not hit_sl: b_exit = j; b_res = "TP"
                elif hit_sl and not hit_tp: b_exit = j; b_res = "SL"
                elif hit_tp and hit_sl: b_exit = j; b_res = "SL"

            # ETH Short: fav is (p_e - low), adv is (high - p_e)
            fav_e = (p_e - c_e.low) / p_e * 100.0
            adv_e = (c_e.high - p_e) / p_e * 100.0
            e_series.append((fav_e, adv_e, c_e.open_time_ms))

            if e_exit is None:
                if fav_e > e_mfe: e_mfe = fav_e
                if adv_e > e_mae: e_mae = adv_e
                hit_tp = (c_e.low <= tp_e)
                hit_sl = (c_e.high >= sl_e)
                if hit_tp and not hit_sl: e_exit = j; e_res = "TP"
                elif hit_sl and not hit_tp: e_exit = j; e_res = "SL"
                elif hit_tp and hit_sl: e_exit = j; e_res = "SL"

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)

        # Did BTC leg win (hit partial TP +0.20%)?
        b_won = (b_mfe >= part_price)
        e_won = (e_mfe >= part_price)

        cycles_data.append({
            "entry_ts": entry_ts,
            "exit_ts": common_times[free_idx],
            "b_series": b_series[:free_idx - i + 1],
            "e_series": e_series[:free_idx - i + 1],
            "b_won": b_won,
            "e_won": e_won,
            "b_mae": b_mae,
            "e_mae": e_mae,
            "b_mfe": b_mfe,
            "e_mfe": e_mfe,
            "b_res": b_res,
            "e_res": e_res
        })
        i = free_idx + 1

    print(f"Total cycles extracted: {len(cycles_data)}")

    # -------------------------------------------------------------
    # 1. MAE DISTRIBUTION ON WINNING TRADES
    # -------------------------------------------------------------
    b_win_maes = [c["b_mae"] for c in cycles_data if c["b_won"]]
    e_win_maes = [c["e_mae"] for c in cycles_data if c["e_won"]]

    def print_mae_stats(name, maes):
        sorted_m = sorted(maes)
        n = len(sorted_m)
        med = sorted_m[n // 2]
        p75 = sorted_m[int(n * 0.75)]
        p90 = sorted_m[int(n * 0.90)]
        p95 = sorted_m[int(n * 0.95)]
        p99 = sorted_m[int(n * 0.99)]
        max_v = sorted_m[-1]

        print(f"\n--- {name} (N = {n} winning trades) ---")
        print(f"  Median Move Against Before Winning: -{med:.2f}%")
        print(f"  75th Percentile:                     -{p75:.2f}%")
        print(f"  90th Percentile:                     -{p90:.2f}%")
        print(f"  95th Percentile:                     -{p95:.2f}%")
        print(f"  99th Percentile:                     -{p99:.2f}%")
        print(f"  Maximum Move Against (Absolute Peak): -{max_v:.2f}%")

        # Distribution bins
        bins = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 1.00, 1.25, 1.50]
        print(f"  Histogram of Adverse Excursion on WINNING trades:")
        for b_i in range(len(bins) - 1):
            cnt = sum(1 for m in sorted_m if bins[b_i] <= m < bins[b_i + 1])
            pct = cnt / n * 100.0
            bar = "#" * int(pct / 2)
            print(f"    [-{bins[b_i]:.2f}% to -{bins[b_i+1]:.2f}%): {cnt:>4} trades ({pct:>5.1f}%) | {bar}")

    print_mae_stats("Account A (BTC Long) MAE on Winners", b_win_maes)
    print_mae_stats("Account B (ETH Short) MAE on Winners", e_win_maes)

    # -------------------------------------------------------------
    # 2. SIMULATE EARLY-CUT AT VARIOUS MAE THRESHOLDS
    # -------------------------------------------------------------
    print(f"\n==========================================================================================")
    print(f"BACKTESTING EARLY-CUT RULE: CLOSE TRADE AS SOON AS MOVE AGAINST EXCEEDS THRESHOLD")
    print(f"==========================================================================================")
    print(f"{'Cut Threshold':>14} | {'Net Profit ($)':>15} | {'Return (%)':>12} | {'Max DD (%)':>11} | {'Pair Win %':>11} | {'Avg/Month':>11}")
    print("-" * 88)

    fee = fee_rate * leverage * 100.0 # 0.08%

    for cut_adv in [1.50, 1.20, 1.00, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30]:
        # For each cycle, evaluate with cut_adv
        tot_profit = 0.0
        wins = 0
        losses = 0
        equity_curve = [2000.0]
        cur_bal = 2000.0
        peak = 2000.0
        max_dd = 0.0

        for c in cycles_data:
            # Evaluate BTC leg with cut_adv
            # Check candle by candle
            b_gain = None
            b_hit_partial = False
            b_peak_fav = 0.0

            for fav, adv, ts in c["b_series"]:
                if fav > b_peak_fav: b_peak_fav = fav
                # Check partial TP
                if b_peak_fav >= part_price and not b_hit_partial:
                    b_hit_partial = True

                # If hit partial TP: SL is at BE (+0.05% price move)
                if b_hit_partial:
                    if fav >= p_tp:
                        b_gain = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage) - 2 * fee
                        break
                    elif adv > 0 and (fav < 0.05): # fell back to BE
                        b_gain = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage) - 2 * fee
                        break
                else:
                    # Not hit partial TP yet
                    # Did it hit cut_adv?
                    if adv >= cut_adv:
                        # Cut early!
                        b_gain = -(cut_adv * leverage) - 2 * fee
                        break
                    elif fav >= p_tp:
                        b_gain = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage) - 2 * fee
                        break

            if b_gain is None:
                # If series finished
                if b_hit_partial:
                    b_gain = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage) - 2 * fee
                elif c["b_mae"] >= cut_adv:
                    b_gain = -(cut_adv * leverage) - 2 * fee
                else:
                    b_gain = -(p_sl * leverage) - 2 * fee

            # Evaluate ETH leg with cut_adv
            e_gain = None
            e_hit_partial = False
            e_peak_fav = 0.0

            for fav, adv, ts in c["e_series"]:
                if fav > e_peak_fav: e_peak_fav = fav
                if e_peak_fav >= part_price and not e_hit_partial:
                    e_hit_partial = True

                if e_hit_partial:
                    if fav >= p_tp:
                        e_gain = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage) - 2 * fee
                        break
                    elif adv > 0 and (fav < 0.05):
                        e_gain = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage) - 2 * fee
                        break
                else:
                    if adv >= cut_adv:
                        e_gain = -(cut_adv * leverage) - 2 * fee
                        break
                    elif fav >= p_tp:
                        e_gain = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage) - 2 * fee
                        break

            if e_gain is None:
                if e_hit_partial:
                    e_gain = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage) - 2 * fee
                elif c["e_mae"] >= cut_adv:
                    e_gain = -(cut_adv * leverage) - 2 * fee
                else:
                    e_gain = -(p_sl * leverage) - 2 * fee

            pnl = (1000.0 * b_gain / 100.0) + (1000.0 * e_gain / 100.0)
            cur_bal += pnl
            equity_curve.append(cur_bal)
            if cur_bal > peak: peak = cur_bal
            dd = (peak - cur_bal) / peak * 100.0
            if dd > max_dd: max_dd = dd

            tot_profit += pnl
            if pnl > 0: wins += 1
            else: losses += 1

        ret_pct = tot_profit / 2000.0 * 100.0
        win_rate = wins / len(cycles_data) * 100.0
        avg_mo = tot_profit / 81.0
        cut_label = f"-{cut_adv:.2f}% (Full SL)" if cut_adv == 1.50 else f"-{cut_adv:.2f}%"
        print(f"{cut_label:>14} | ${tot_profit:>+13,.2f} | {ret_pct:>+10.1f}% | {max_dd:>9.2f}% | {win_rate:>9.1f}% | ${avg_mo:>+9.2f}")

if __name__ == "__main__":
    run_mae_cut_analysis()
