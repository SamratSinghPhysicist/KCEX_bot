import os
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
import collections

from experiments.btc_eth_reverse_experiment.forensic_audit.master_research_engine import (
    load_1h_candles, parse_date_ms, FastOneMinuteResolver
)

def analyze_mfe_distribution():
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

    # Analyze for baseline SL = 1.5% and SL = 1.0% (with TP = 1.5% and TP = 2.0%)
    scenarios = [
        ("BTC LONG (Base SL 1.5%, TP 1.5%)", "BTCUSDT", "LONG", btc_al, 1.5, 1.5),
        ("BTC SHORT (Base SL 1.5%, TP 1.5%)", "BTCUSDT", "SHORT", btc_al, 1.5, 1.5),
        ("ETH LONG (Base SL 1.5%, TP 1.5%)", "ETHUSDT", "LONG", eth_al, 1.5, 1.5),
        ("ETH SHORT (Base SL 1.5%, TP 1.5%)", "ETHUSDT", "SHORT", eth_al, 1.5, 1.5),
        ("BTC LONG (Base SL 1.0%, TP 2.0%)", "BTCUSDT", "LONG", btc_al, 2.0, 1.0),
        ("ETH SHORT (Base SL 1.0%, TP 2.0%)", "ETHUSDT", "SHORT", eth_al, 2.0, 1.0),
    ]

    for sc_name, sym, direction, candles, tp_pct, sl_pct in scenarios:
        losing_mfes = []
        winning_mfes = []
        all_mfes = []

        i = 0
        while i < n - 1:
            entry_px = candles[i].open
            tp_px = entry_px * (1.0 + tp_pct / 100.0) if direction == "LONG" else entry_px * (1.0 - tp_pct / 100.0)
            sl_px = entry_px * (1.0 - sl_pct / 100.0) if direction == "LONG" else entry_px * (1.0 + sl_pct / 100.0)

            cur_mfe = 0.0
            outcome = None
            exit_idx = i

            for k in range(i, n):
                c = candles[k]
                if direction == "LONG":
                    c_mfe = (c.high - entry_px) / entry_px * 100.0
                    cur_mfe = max(cur_mfe, c_mfe)
                    hit_tp = c.high >= tp_px
                    hit_sl = c.low <= sl_px
                else:
                    c_mfe = (entry_px - c.low) / entry_px * 100.0
                    cur_mfe = max(cur_mfe, c_mfe)
                    hit_tp = c.low <= tp_px
                    hit_sl = c.high >= sl_px

                if hit_tp and hit_sl:
                    # In a dispute, declare SL (pessimistic)
                    outcome = "SL"
                    exit_idx = k
                    break
                elif hit_tp:
                    outcome = "TP"
                    exit_idx = k
                    break
                elif hit_sl:
                    outcome = "SL"
                    exit_idx = k
                    break

            if outcome == "SL":
                losing_mfes.append(cur_mfe)
            elif outcome == "TP":
                winning_mfes.append(cur_mfe)
            all_mfes.append(cur_mfe)

            i = exit_idx + 1

        total_losing = len(losing_mfes)
        arr = np.array(losing_mfes)

        print("\n" + "=" * 80)
        print(f"SCENARIO: {sc_name}")
        print(f"Total Losing Trades: {total_losing} (out of {len(all_mfes)} total, Loss Rate: {total_losing/len(all_mfes)*100:.2f}%)")
        print(f"Mean MFE before loss:   {np.mean(arr):.3f}%")
        print(f"Median MFE before loss: {np.median(arr):.3f}%")
        print(f"25th percentile:        {np.percentile(arr, 25):.3f}%")
        print(f"75th percentile:        {np.percentile(arr, 75):.3f}%")
        print(f"90th percentile:        {np.percentile(arr, 90):.3f}%")

        # Threshold probabilities: P(MFE >= threshold | Trade is a Loss)
        thresholds = [0.10, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.75, 1.00]
        print("\nProbability that a LOSING trade reaches at least X% MFE before stopping out:")
        print("-----------------------------------------------------------------------------")
        for th in thresholds:
            count = np.sum(arr >= th)
            pct = count / total_losing * 100.0
            print(f"  P(MFE >= +{th:.2f}% | Loss) = {pct:5.2f}% ({count}/{total_losing} losing trades)")

        # Histogram distribution in 0.10% bins
        bins = np.arange(0.0, tp_pct + 0.15, 0.10)
        hist, bin_edges = np.histogram(arr, bins=bins)
        print("\nHistogram of Peak MFE for Losing Trades:")
        for idx in range(len(hist)):
            low = bin_edges[idx]
            high = bin_edges[idx + 1]
            pct = hist[idx] / total_losing * 100.0
            bar = "#" * int(pct // 2)
            print(f"  [{low:4.2f}% - {high:4.2f}%): {pct:5.2f}% {bar}")

if __name__ == "__main__":
    analyze_mfe_distribution()
