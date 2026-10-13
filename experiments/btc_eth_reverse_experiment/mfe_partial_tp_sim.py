"""
MFE/MAE Analysis on Losing Trades and Partial Profit Booking Strategy
=====================================================================
Analyzes:
1. For losing trades: What is the distribution of Maximum Favorable Excursion (MFE)
   before the trade hits Stop Loss?
   (i.e. how far into profit does price go before reversing and stopping out?)
2. Simulates booking 50% at the optimal MFE, moving SL to breakeven on the rest,
   and letting the remaining 50% run to the target TP.
3. Tests impact on Prop Firm Challenge pass rates (+10% target, 3.0% max drawdown).
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

def run_mfe_and_partial_tp_analysis():
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

    print("=" * 80)
    print("MFE & MAE ANALYSIS ON LOSING TRADES (BTC Long / ETH Short)")
    print(f"Timeframe: {timeframe} | Period: 2025-01-01 to 2026-10-12 ({len(common_times)} candles)")
    print("=" * 80)

    # Let's analyze for Config 3 (TP 1.5%, SL 3.0%) and Config 1 (TP 3.0%, SL 3.0%) and Config 2 (TP 1.5%, SL 1.5%)
    test_configs = [
        ("Config 3 (TP 1.5%, SL 3.0%)", 1.5, 3.0),
        ("Config 2 (TP 1.5%, SL 1.5%)", 1.5, 1.5),
        ("Config 1 (TP 3.0%, SL 3.0%)", 3.0, 3.0),
    ]

    for cfg_title, tp_pct, sl_pct in test_configs:
        print(f"\n############################################################")
        print(f"ANALYZING {cfg_title}")
        print(f"############################################################")

        # Track losing trades
        btc_loss_mfes = [] # peak % move in favor before loss
        eth_loss_mfes = []

        # We step candle by candle
        i = 0
        tot_len = len(common_times)

        # Store trade details for partial TP simulation later
        # Each trade record: (entry_ts, b_res, e_res, b_mfe, e_mfe, b_bars, e_bars)
        trade_records = []

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

                # Update 1m-granular MFE for BTC Long (fav move = high - entry)
                if b_exit is None:
                    # Check 1m candles for precise peak
                    sub_b = btc_sub.get(ts, [])
                    if sub_b:
                        for m_c in sub_b:
                            fav_pct = (m_c.high - p_b) / p_b * 100.0
                            if fav_pct > b_mfe: b_mfe = fav_pct
                            # check if SL hit
                            if m_c.low <= sl_b:
                                b_exit = j; b_res = "SL"; break
                            elif m_c.high >= tp_b:
                                b_exit = j; b_res = "TP"; break
                    else:
                        fav_pct = (c_b.high - p_b) / p_b * 100.0
                        if fav_pct > b_mfe: b_mfe = fav_pct
                        r, _ = evaluate_candle_tp_sl("LONG", p_b, tp_b, sl_b, c_b, btc_sub, timeframe)
                        if r: b_exit = j; b_res = r

                # Update 1m-granular MFE for ETH Short (fav move = entry - low)
                if e_exit is None:
                    sub_e = eth_sub.get(ts, [])
                    if sub_e:
                        for m_c in sub_e:
                            fav_pct = (p_e - m_c.low) / p_e * 100.0
                            if fav_pct > e_mfe: e_mfe = fav_pct
                            # check if SL hit
                            if m_c.high >= sl_e:
                                e_exit = j; e_res = "SL"; break
                            elif m_c.low <= tp_e:
                                e_exit = j; e_res = "TP"; break
                    else:
                        fav_pct = (p_e - c_e.low) / p_e * 100.0
                        if fav_pct > e_mfe: e_mfe = fav_pct
                        r, _ = evaluate_candle_tp_sl("SHORT", p_e, tp_e, sl_e, c_e, eth_sub, timeframe)
                        if r: e_exit = j; e_res = r

                if b_exit is not None and e_exit is not None:
                    break
                j += 1

            if b_exit is None or e_exit is None:
                break

            if b_res == "SL":
                btc_loss_mfes.append(b_mfe)
            if e_res == "SL":
                eth_loss_mfes.append(e_mfe)

            trade_records.append({
                "entry_ts": entry_ts,
                "b_res": b_res,
                "e_res": e_res,
                "b_mfe": b_mfe,
                "e_mfe": e_mfe,
                "p_b": p_b,
                "p_e": p_e,
                "b_exit": b_exit,
                "e_exit": e_exit
            })

            i = max(b_exit, e_exit) + 1

        print(f"Total Completed Trade Cycles: {len(trade_records)}")
        print(f"BTC Losses: {len(btc_loss_mfes)} | ETH Losses: {len(eth_loss_mfes)}")

        # Print MFE statistics for losing trades
        for name, mfes in [("BTC Long Losing Trades", btc_loss_mfes), ("ETH Short Losing Trades", eth_loss_mfes)]:
            if not mfes: continue
            sorted_m = sorted(mfes)
            n = len(sorted_m)
            mean_m = sum(sorted_m) / n
            med_m = sorted_m[n // 2]
            p25 = sorted_m[int(n * 0.25)]
            p75 = sorted_m[int(n * 0.75)]
            p90 = sorted_m[int(n * 0.90)]

            # Histogram bins: [0, 0.25), [0.25, 0.5), [0.5, 0.75), [0.75, 1.0), [1.0, 1.25), [1.25, 1.5)
            bins = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00]
            bin_counts = [0] * (len(bins) - 1)
            for m in sorted_m:
                for b_i in range(len(bins) - 1):
                    if bins[b_i] <= m < bins[b_i + 1]:
                        bin_counts[b_i] += 1
                        break

            print(f"\n--- {name} (Total: {n}) ---")
            print(f"  Mean Move in Favor before SL:   +{mean_m:.2f}%")
            print(f"  Median Move in Favor before SL: +{med_m:.2f}%")
            print(f"  25th Percentile:                +{p25:.2f}%")
            print(f"  75th Percentile:                +{p75:.2f}%")
            print(f"  90th Percentile:                +{p90:.2f}%")
            print(f"  Distribution of Peak Favorable Move Before Stop-Out:")
            for b_i in range(len(bins) - 1):
                cnt = bin_counts[b_i]
                pct = cnt / n * 100.0
                bar = "#" * int(pct / 2)
                print(f"    [{bins[b_i]:.2f}% - {bins[b_i+1]:.2f}%): {cnt:>4} trades ({pct:>5.1f}%) | {bar}")

        # Now test Partial TP + Breakeven Strategy!
        # What if we close 50% at partial_tp (e.g. 0.50%, 0.75%, 1.00%), move SL to BE (+0.05%),
        # and let remaining 50% run to TP?
        print(f"\n>>> PARTIAL PROFIT TAKING (50% Booked + Breakeven Lock) SIMULATION <<<")
        print(f"Original TP = {tp_pct}%, Original SL = {sl_pct}%")
        print(f"{'Partial TP':>12} | {'New BTC Win %':>15} | {'New ETH Win %':>15} | {'Avg PnL/Trade BTC':>18} | {'Avg PnL/Trade ETH':>18} | {'Both Pass (Prop)':>18} | {'>=1 Pass':>10}")
        print("-" * 115)

        for part_tp in [0.30, 0.50, 0.75, 1.00]:
            if part_tp >= tp_pct: continue
            # Simulate each trade with 50% partial TP
            # For each trade:
            # If trade reached part_tp:
            #   50% was closed at +part_tp.
            #   Remaining 50% had SL moved to 0.05% (BE).
            #   If original trade hit full TP: remaining 50% hits +tp_pct. Total gain = 0.5 * part_tp + 0.5 * tp_pct.
            #   If original trade hit SL: remaining 50% stopped at BE (+0.05%). Total gain = 0.5 * part_tp + 0.5 * 0.05%.
            # If trade NEVER reached part_tp:
            #   Trade hit original SL: 100% loss of -sl_pct.
            btc_pnl_list = []
            eth_pnl_list = []
            btc_wins = 0
            eth_wins = 0

            sim_cycles = []
            for tr in trade_records:
                # BTC Trade
                if tr["b_mfe"] >= part_tp:
                    # Partial TP was triggered!
                    if tr["b_res"] == "TP":
                        # Hit full TP
                        gain_b = 0.5 * part_tp + 0.5 * tp_pct
                        btc_wins += 1
                        b_status = "WIN"
                    else:
                        # Hit BE on remaining 50%
                        gain_b = 0.5 * part_tp + 0.5 * 0.05
                        btc_wins += 1 # Ended in net profit!
                        b_status = "PARTIAL_WIN"
                else:
                    # Never reached partial TP, full SL
                    gain_b = -sl_pct
                    b_status = "LOSS"

                # ETH Trade
                if tr["e_mfe"] >= part_tp:
                    if tr["e_res"] == "TP":
                        gain_e = 0.5 * part_tp + 0.5 * tp_pct
                        eth_wins += 1
                        e_status = "WIN"
                    else:
                        gain_e = 0.5 * part_tp + 0.5 * 0.05
                        eth_wins += 1
                        e_status = "PARTIAL_WIN"
                else:
                    gain_e = -sl_pct
                    e_status = "LOSS"

                btc_pnl_list.append(gain_b)
                eth_pnl_list.append(gain_e)
                sim_cycles.append((gain_b, gain_e))

            n_tr = len(trade_records)
            new_b_win = btc_wins / n_tr * 100.0
            new_e_win = eth_wins / n_tr * 100.0
            avg_pnl_b = sum(btc_pnl_list) / n_tr
            avg_pnl_e = sum(eth_pnl_list) / n_tr

            # Now test prop challenge pass rate with this partial booking strategy!
            # Using 20% margin (2x leverage -> 40% effective position)
            # If gain is gain_b %, balance change is: bal * (0.20 * 2.0 * gain_b / 100) = bal * (0.40 * gain_b / 100)
            step = 2
            both_p = 0; either_p = 0; n_sim = 0
            for s_idx in range(0, max(1, n_tr - 20), step):
                w = sim_cycles[s_idx:]
                b_a, p_a, s_a = 1000.0, 1000.0, "RUNNING"
                b_b, p_b, s_b = 1000.0, 1000.0, "RUNNING"
                for gb, ge in w:
                    if s_a == "RUNNING":
                        b_a += b_a * (0.40 * gb / 100.0)
                        if b_a > p_a: p_a = b_a
                        dd_a = (p_a - b_a) / p_a * 100.0
                        if dd_a >= 3.0: s_a = "FAILED"
                        elif ((b_a - 1000.0) / 1000.0 * 100.0) >= 10.0: s_a = "PASSED"

                    if s_b == "RUNNING":
                        b_b += b_b * (0.40 * ge / 100.0)
                        if b_b > p_b: p_b = b_b
                        dd_b = (p_b - b_b) / p_b * 100.0
                        if dd_b >= 3.0: s_b = "FAILED"
                        elif ((b_b - 1000.0) / 1000.0 * 100.0) >= 10.0: s_b = "PASSED"

                    if s_a != "RUNNING" and s_b != "RUNNING": break

                n_sim += 1
                if s_a == "PASSED" and s_b == "PASSED": both_p += 1
                if s_a == "PASSED" or s_b == "PASSED": either_p += 1

            bp_rate = both_p / n_sim * 100.0 if n_sim else 0.0
            ep_rate = either_p / n_sim * 100.0 if n_sim else 0.0

            print(f"{part_tp:>11.2f}% | {new_b_win:>14.1f}% | {new_e_win:>14.1f}% | {avg_pnl_b:>+17.3f}% | {avg_pnl_e:>+17.3f}% | {bp_rate:>17.1f}% | {ep_rate:>9.1f}%")

if __name__ == "__main__":
    run_mfe_and_partial_tp_analysis()
