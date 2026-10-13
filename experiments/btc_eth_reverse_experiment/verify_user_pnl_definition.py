"""
Simulation under User's Exact Specification:
TP and SL are Profit% and Loss% on the Trade (ROE / Return on Margin).
Initial Balance = 1000 USDT
Leverage = 2x
100% Margin used per trade (Position = 2000 USDT)

Configs:
1. TP = +3.0% profit, SL = -3.0% loss (Price moves: TP = +1.50%, SL = -1.50%)
2. TP = +1.5% profit, SL = -1.5% loss (Price moves: TP = +0.75%, SL = -0.75%)
3. TP = +1.5% profit, SL = -3.0% loss (Price moves: TP = +0.75%, SL = -1.50%)
4. TP = +0.75% profit, SL = -1.5% loss (Price moves: TP = +0.375%, SL = -0.75%)

Also tests with the Partial Profit Booking:
Book 50% at +0.30% to +0.60% profit on trade, move SL to breakeven, run rest to TP.
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

def run_user_spec_sim():
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

    leverage = 2.0
    configs = [
        ("Config 1 (TP +3.0% profit, SL -3.0% loss)", 3.0, 3.0),
        ("Config 2 (TP +1.5% profit, SL -1.5% loss)", 1.5, 1.5),
        ("Config 3 (TP +1.5% profit, SL -3.0% loss)", 1.5, 3.0),
        ("Config 4 (TP +0.75% profit, SL -1.5% loss)", 0.75, 1.5),
    ]

    print("=" * 85)
    print("SIMULATION UNDER EXACT USER SPECIFICATION: TP & SL ARE PROFIT% AND LOSS% ON TRADE")
    print(f"Leverage: {leverage}x | 100% Margin ($1000 USDT) | Max DD: 3.0% | Target: +10.0%")
    print("=" * 85)

    tot_len = len(common_times)

    for cfg_name, tp_profit_pct, sl_loss_pct in configs:
        # Since leverage is 2x:
        # Price move TP (%) = tp_profit_pct / leverage
        # Price move SL (%) = sl_loss_pct / leverage
        price_tp_pct = tp_profit_pct / leverage
        price_sl_pct = sl_loss_pct / leverage

        cycles = []
        i = 0
        while i < tot_len - 1:
            entry_ts = common_times[i]
            p_b = btc_dict[entry_ts].open
            p_e = eth_dict[entry_ts].open

            tp_b = p_b * (1.0 + price_tp_pct / 100.0)
            sl_b = p_b * (1.0 - price_sl_pct / 100.0)
            tp_e = p_e * (1.0 - price_tp_pct / 100.0)
            sl_e = p_e * (1.0 + price_sl_pct / 100.0)

            b_exit = None; b_res = None
            e_exit = None; e_res = None

            j = i
            while j < tot_len:
                ts = common_times[j]
                c_b = btc_dict[ts]
                c_e = eth_dict[ts]

                if b_exit is None:
                    r, _ = evaluate_candle_tp_sl("LONG", p_b, tp_b, sl_b, c_b, btc_sub, timeframe)
                    if r: b_exit = j; b_res = r
                if e_exit is None:
                    r, _ = evaluate_candle_tp_sl("SHORT", p_e, tp_e, sl_e, c_e, eth_sub, timeframe)
                    if r: e_exit = j; e_res = r

                if b_exit is not None and e_exit is not None:
                    break
                j += 1

            if b_exit is None or e_exit is None:
                break

            free_idx = max(b_exit, e_exit)
            exit_ts = common_times[free_idx]

            # In user's definition:
            # If win (TP): profit is +tp_profit_pct on balance (+3.0%, +1.5%, etc.)
            # If loss (SL): loss is -sl_loss_pct on balance (-3.0%, -1.5%, etc.)
            pnl_b = tp_profit_pct if b_res == "TP" else -sl_loss_pct
            pnl_e = tp_profit_pct if e_res == "TP" else -sl_loss_pct

            cycles.append((b_res == "TP", e_res == "TP", pnl_b, pnl_e))
            i = free_idx + 1

        # Calculate standard metrics
        n_c = len(cycles)
        b_win_cnt = sum(1 for c in cycles if c[0])
        e_win_cnt = sum(1 for c in cycles if c[1])
        both_w_cnt = sum(1 for c in cycles if c[0] and c[1])
        both_l_cnt = sum(1 for c in cycles if not c[0] and not c[1])
        one_w_cnt = n_c - both_l_cnt

        print(f"\n--- {cfg_name} (Price moves: TP=+{price_tp_pct:.3f}%, SL=-{price_sl_pct:.3f}%) ---")
        print(f"  Total Cycles: {n_c}")
        print(f"  BTC Win Rate: {b_win_cnt/n_c*100:.1f}% | ETH Win Rate: {e_win_cnt/n_c*100:.1f}%")
        print(f"  Both Win: {both_w_cnt/n_c*100:.1f}% | Both Lose: {both_l_cnt/n_c*100:.1f}% | >=1 Win: {one_w_cnt/n_c*100:.1f}%")

        # Now test Prop Challenge Performance:
        # Standard 100% balance trading (no partial TP)
        # Target: +10%, Max DD: 3.0%
        both_p, either_p, a_p, b_p, n_sim = 0, 0, 0, 0, 0
        for s in range(0, max(1, n_c - 20), 2):
            w = cycles[s:]
            ba, pa, sa = 1000.0, 1000.0, "RUNNING"
            bb, pb, sb = 1000.0, 1000.0, "RUNNING"
            for bw, ew, pb_pnl, pe_pnl in w:
                if sa == "RUNNING":
                    ba += ba * (pb_pnl / 100.0)
                    if ba > pa: pa = ba
                    dd_a = (pa - ba) / pa * 100.0
                    if dd_a >= 3.0: sa = "FAILED"
                    elif ((ba - 1000.0) / 1000.0 * 100.0) >= 10.0: sa = "PASSED"

                if sb == "RUNNING":
                    bb += bb * (pe_pnl / 100.0)
                    if bb > pb: pb = bb
                    dd_b = (pb - bb) / pb * 100.0
                    if dd_b >= 3.0: sb = "FAILED"
                    elif ((bb - 1000.0) / 1000.0 * 100.0) >= 10.0: sb = "PASSED"

                if sa != "RUNNING" and sb != "RUNNING": break

            n_sim += 1
            if sa == "PASSED" and sb == "PASSED": both_p += 1
            if sa == "PASSED" or sb == "PASSED": either_p += 1
            if sa == "PASSED": a_p += 1
            if sb == "PASSED": b_p += 1

        print(f"  Prop Challenge Pass Rate (Standard):")
        print(f"    Both Pass: {both_p/n_sim*100:.1f}% | >=1 Pass: {either_p/n_sim*100:.1f}% | A Pass: {a_p/n_sim*100:.1f}% | B Pass: {b_p/n_sim*100:.1f}%")

if __name__ == "__main__":
    run_user_spec_sim()
