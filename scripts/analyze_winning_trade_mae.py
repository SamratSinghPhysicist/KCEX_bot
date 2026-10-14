import os
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
import datetime

from experiments.btc_eth_reverse_experiment.forensic_audit.master_research_engine import (
    load_1h_candles, parse_date_ms, FastOneMinuteResolver
)

def run_mae_analysis():
    data_dir = "BACKTESTER/OHLCV_Data_Binance"
    start_ms = parse_date_ms("2020-01-01")
    end_ms = parse_date_ms("2026-09-30") + (86400 * 1000 - 1)

    print("[*] Loading 1H candles...")
    btc_candles = load_1h_candles("BTCUSDT", data_dir, start_ms, end_ms)
    eth_candles = load_1h_candles("ETHUSDT", data_dir, start_ms, end_ms)

    btc_map = {c.open_time_ms: c for c in btc_candles}
    eth_map = {c.open_time_ms: c for c in eth_candles}
    common_ts = sorted(set(btc_map.keys()) & set(eth_map.keys()))
    btc_al = [btc_map[t] for t in common_ts]
    eth_al = [eth_map[t] for t in common_ts]
    n = len(btc_al)
    print(f"[*] Aligned candles: {n}")

    resolver = FastOneMinuteResolver(data_dir=data_dir, max_cached_months=200)

    # Scenarios:
    # 1. Target = TP 1.50% (Base SL 1.50%)
    # 2. Target = TP 1.50% (Wide SL 5.00% to find unconstrained MAE)
    # 3. Target = TP1 +0.50% (Base SL 1.50%) - The primary MFE TP1 level
    # 4. Target = TP1 +0.35% (Base SL 1.50%)
    # 5. Target = TP1 +0.20% (Base SL 1.50%)
    # 6. Target = TP 2.00% (Base SL 1.00%)

    symbols_directions = [
        ("BTCUSDT", "LONG", btc_al),
        ("BTCUSDT", "SHORT", btc_al),
        ("ETHUSDT", "LONG", eth_al),
        ("ETHUSDT", "SHORT", eth_al),
    ]

    tp_targets = [
        (1.50, 1.50, "TP 1.50% (Base SL 1.50%)"),
        (1.50, 5.00, "TP 1.50% (Wide SL 5.00% - Unconstrained)"),
        (0.50, 1.50, "TP1 +0.50% (Base SL 1.50% - MFE-Optimal TP1)"),
        (0.35, 1.50, "TP1 +0.35% (Base SL 1.50%)"),
        (0.20, 1.50, "TP1 +0.20% (Base SL 1.50%)"),
    ]

    for target_tp, base_sl, label in tp_targets:
        print("\n" + "=" * 90)
        print(f"CONFIGURATION: {label}")
        print("=" * 90)

        for sym, direction, candles in symbols_directions:
            winning_maes = []
            losing_maes = []
            all_maes = []

            # Track 1-minute intra-candle disambiguation for accuracy
            i = 0
            while i < n - 1:
                entry_px = candles[i].open
                tp_px = entry_px * (1.0 + target_tp / 100.0) if direction == "LONG" else entry_px * (1.0 - target_tp / 100.0)
                sl_px = entry_px * (1.0 - base_sl / 100.0) if direction == "LONG" else entry_px * (1.0 + base_sl / 100.0)

                cur_mae = 0.0
                outcome = None
                exit_idx = i

                for k in range(i, n):
                    c = candles[k]
                    if direction == "LONG":
                        hit_tp = c.high >= tp_px
                        hit_sl = c.low <= sl_px
                    else:
                        hit_tp = c.low <= tp_px
                        hit_sl = c.high >= sl_px

                    if hit_tp and hit_sl:
                        # 1m dispute
                        res_outcome, _, _ = resolver.resolve_simple_tp_sl(
                            sym, direction, c.open_time_ms, entry_px, tp_px, sl_px
                        )
                        outcome = res_outcome
                        exit_idx = k
                        if outcome == "TP":
                            # In candle k, what was the adverse move before TP?
                            # Get 1m slice
                            slice_arr = resolver.get_hour_slice(sym, c.open_time_ms)
                            if slice_arr is not None:
                                highs = slice_arr[:, 2]
                                lows = slice_arr[:, 3]
                                if direction == "LONG":
                                    m_tp = highs >= tp_px
                                    first_tp_idx = int(np.argmax(m_tp)) if np.any(m_tp) else len(lows)
                                    intra_mae = (entry_px - np.min(lows[:first_tp_idx+1])) / entry_px * 100.0
                                else:
                                    m_tp = lows <= tp_px
                                    first_tp_idx = int(np.argmax(m_tp)) if np.any(m_tp) else len(highs)
                                    intra_mae = (np.max(highs[:first_tp_idx+1]) - entry_px) / entry_px * 100.0
                                cur_mae = max(cur_mae, intra_mae)
                            else:
                                c_mae = (entry_px - c.low) / entry_px * 100.0 if direction == "LONG" else (c.high - entry_px) / entry_px * 100.0
                                cur_mae = max(cur_mae, c_mae)
                        else:
                            c_mae = (entry_px - c.low) / entry_px * 100.0 if direction == "LONG" else (c.high - entry_px) / entry_px * 100.0
                            cur_mae = max(cur_mae, c_mae)
                        break

                    elif hit_tp:
                        outcome = "TP"
                        exit_idx = k
                        # Check intra-candle adverse excursion on winning candle before TP
                        slice_arr = resolver.get_hour_slice(sym, c.open_time_ms)
                        if slice_arr is not None:
                            highs = slice_arr[:, 2]
                            lows = slice_arr[:, 3]
                            if direction == "LONG":
                                m_tp = highs >= tp_px
                                first_tp_idx = int(np.argmax(m_tp)) if np.any(m_tp) else len(lows)
                                intra_mae = (entry_px - np.min(lows[:first_tp_idx+1])) / entry_px * 100.0
                            else:
                                m_tp = lows <= tp_px
                                first_tp_idx = int(np.argmax(m_tp)) if np.any(m_tp) else len(highs)
                                intra_mae = (np.max(highs[:first_tp_idx+1]) - entry_px) / entry_px * 100.0
                            cur_mae = max(cur_mae, intra_mae)
                        else:
                            c_mae = (entry_px - c.low) / entry_px * 100.0 if direction == "LONG" else (c.high - entry_px) / entry_px * 100.0
                            cur_mae = max(cur_mae, c_mae)
                        break

                    elif hit_sl:
                        outcome = "SL"
                        exit_idx = k
                        c_mae = (entry_px - c.low) / entry_px * 100.0 if direction == "LONG" else (c.high - entry_px) / entry_px * 100.0
                        cur_mae = max(cur_mae, c_mae)
                        break
                    else:
                        c_mae = (entry_px - c.low) / entry_px * 100.0 if direction == "LONG" else (c.high - entry_px) / entry_px * 100.0
                        cur_mae = max(cur_mae, c_mae)

                if outcome == "TP":
                    winning_maes.append(max(0.0, cur_mae))
                elif outcome == "SL":
                    losing_maes.append(max(0.0, cur_mae))
                all_maes.append(max(0.0, cur_mae))

                i = exit_idx + 1

            total_winners = len(winning_maes)
            total_trades = len(all_maes)
            w_arr = np.array(winning_maes)

            print(f"\n--- {sym} ({direction}) ---")
            print(f"Total Trades: {total_trades:,} | Winning Trades: {total_winners:,} ({total_winners/total_trades*100:.1f}%)")
            if total_winners > 0:
                print(f"MAE Mean:   {np.mean(w_arr):.3f}%")
                print(f"MAE Median: {np.median(w_arr):.3f}%")
                print(f"MAE P25:    {np.percentile(w_arr, 25):.3f}%")
                print(f"MAE P75:    {np.percentile(w_arr, 75):.3f}%")
                print(f"MAE P90:    {np.percentile(w_arr, 90):.3f}%")
                print(f"MAE P95:    {np.percentile(w_arr, 95):.3f}%")
                print(f"MAE P99:    {np.percentile(w_arr, 99):.3f}%")
                print(f"MAE Max:    {np.max(w_arr):.3f}%")

                thresholds = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00, 1.20, 1.40]
                print("\n  Candidate SL Level | Winning Trades Touching Level (Killed) | Survival Rate (% of Winners that survive)")
                for th in thresholds:
                    if th <= base_sl:
                        killed = np.sum(w_arr >= th)
                        survived = np.sum(w_arr < th)
                        print(f"      SL -{th:.2f}%     | {killed:5d} ({killed/total_winners*100:5.2f}%) touched/killed       | {survived:5d} ({survived/total_winners*100:5.2f}%) survived")

if __name__ == "__main__":
    run_mae_analysis()
