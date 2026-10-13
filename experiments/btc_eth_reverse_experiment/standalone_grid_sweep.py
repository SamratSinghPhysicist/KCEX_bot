"""
Standalone Grid Sweep: BTC-Only and ETH-Only across 77 Leverage x Margin Combinations
=====================================================================================
Evaluates:
- BTC Only (Case 1: Long BTC)
- ETH Only (Case 1: Short ETH)
across all 77 combinations of:
- Leverages: [1x, 2x, 5x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 125x]
- Margins:   [1%, 5%, 10%, 20%, 50%, 75%, 100%]

Dataset: 2020-01-01 to 2026-09-30 (16,381 Trade Cycles, 6.75 Years)
Base Capital: $1,000 USDT per account.
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
    evaluate_candle_tp_sl,
    parse_date_to_ms,
    CandleData
)

def run_standalone_grid():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2020-01-01")
    end_ms = parse_date_to_ms("2026-09-30") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    fee_rate = 0.0004
    p_tp = 1.50
    cut_adv = 0.40
    part_price = 0.20
    tot_len = len(common_times)

    print("=" * 90)
    print("STANDALONE BTC & ETH GRID SWEEP (77 COMBINATIONS EACH)")
    print(f"Data: 2020-01-01 to 2026-09-30 (6.75 Years)")
    print(f"Base Capital: $1,000 USDT Standalone")
    print("=" * 90)

    # Pre-extract trade outcomes for Case 1: Long BTC, Short ETH
    b_dir = "LONG"; e_dir = "SHORT"
    i = 0
    btc_moves = []
    eth_moves = []

    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        tp_b = p_b * (1.0 + p_tp / 100.0)
        sl_b = p_b * (1.0 - cut_adv / 100.0)
        tp_e = p_e * (1.0 - p_tp / 100.0)
        sl_e = p_e * (1.0 + cut_adv / 100.0)

        b_exit = None; b_res = None; b_mfe = 0.0
        e_exit = None; e_res = None; e_mfe = 0.0

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]; c_e = eth_dict[ts]

            if b_exit is None:
                fav_b = (c_b.high - p_b)/p_b * 100.0
                if fav_b > b_mfe: b_mfe = fav_b
                hit_tp = (c_b.high >= tp_b)
                hit_sl = (c_b.low <= sl_b)
                if hit_tp and not hit_sl: b_exit = j; b_res = "TP"
                elif hit_sl and not hit_tp: b_exit = j; b_res = "SL"
                elif hit_tp and hit_sl: b_exit = j; b_res = "SL"

            if e_exit is None:
                fav_e = (p_e - c_e.low)/p_e * 100.0
                if fav_e > e_mfe: e_mfe = fav_e
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

        # BTC price move
        if b_mfe >= part_price:
            leg2_move = p_tp if b_res == "TP" else 0.05
            price_move_b = 0.5 * part_price + 0.5 * leg2_move
        else:
            price_move_b = -cut_adv

        # ETH price move
        if e_mfe >= part_price:
            leg2_move = p_tp if e_res == "TP" else 0.05
            price_move_e = 0.5 * part_price + 0.5 * leg2_move
        else:
            price_move_e = -cut_adv

        btc_moves.append(price_move_b)
        eth_moves.append(price_move_e)
        i = free_idx + 1

    print(f"[*] Pre-extracted {len(btc_moves)} trade cycles.")

    leverages = [1, 2, 5, 10, 15, 20, 25, 50, 75, 100, 125]
    margins = [0.01, 0.05, 0.10, 0.20, 0.50, 0.75, 1.00]

    def evaluate_grid(asset_name, moves):
        grid_ret = {}
        grid_dd = {}
        grid_mo = {}

        for lev in leverages:
            mmr = 0.004 if lev <= 50 else (0.005 if lev <= 100 else 0.006)
            liq_distance_pct = (1.0 / lev - mmr) * 100.0 if lev > 1 else 99.0
            is_liq_before_sl = (liq_distance_pct <= cut_adv)

            for m_frac in margins:
                pos_size = 1000.0 * m_frac * lev
                fee_per_trade = 2.0 * fee_rate * pos_size

                tot_profit = 0.0
                peak = 1000.0
                max_dd = 0.0
                liquidated = is_liq_before_sl

                if not liquidated:
                    for mv in moves:
                        pnl = pos_size * (mv / 100.0) - fee_per_trade
                        tot_profit += pnl

                        cur_total = 1000.0 + tot_profit
                        if cur_total <= 0:
                            liquidated = True
                            break

                        if cur_total > peak: peak = cur_total
                        dd = (peak - cur_total) / peak * 100.0
                        if dd > max_dd: max_dd = dd

                ret_pct = tot_profit / 1000.0 * 100.0 if not liquidated else -100.0
                grid_ret[(lev, m_frac)] = ret_pct if not liquidated else "LIQUIDATED"
                grid_dd[(lev, m_frac)] = max_dd if not liquidated else 100.0
                grid_mo[(lev, m_frac)] = tot_profit / 81.0 if not liquidated else 0.0

        return grid_ret, grid_dd, grid_mo

    btc_ret, btc_dd, btc_mo = evaluate_grid("BTC (Long BTC)", btc_moves)
    eth_ret, eth_dd, eth_mo = evaluate_grid("ETH (Short ETH)", eth_moves)

    headers = [f"Margin {int(m*100)}%" for m in margins]

    def print_matrices(asset_title, g_ret, g_dd, g_mo):
        print(f"\n##########################################################################################")
        print(f"{asset_title}: TOTAL NET RETURN MATRIX (% on $1,000 Base across 6.75 Years)")
        print(f"##########################################################################################")
        print(f"{'Leverage':<10} | " + " | ".join(f"{h:>12}" for h in headers))
        print("-" * 115)
        for lev in leverages:
            row_str = f"{lev:>4}x      | "
            cells = []
            for m in margins:
                v = g_ret[(lev, m)]
                if v == "LIQUIDATED": cells.append(f"{'LIQUIDATED':>12}")
                else: cells.append(f"{v:>+11.1f}%")
            row_str += " | ".join(cells)
            print(row_str)

        print(f"\n--- {asset_title}: MAXIMUM DRAWDOWN MATRIX (%) ---")
        print(f"{'Leverage':<10} | " + " | ".join(f"{h:>12}" for h in headers))
        print("-" * 115)
        for lev in leverages:
            row_str = f"{lev:>4}x      | "
            cells = []
            for m in margins:
                if g_ret[(lev, m)] == "LIQUIDATED": cells.append(f"{'100.0%':>12}")
                else: cells.append(f"{g_dd[(lev, m)]:>11.2f}%")
            row_str += " | ".join(cells)
            print(row_str)

        print(f"\n--- {asset_title}: AVERAGE MONTHLY INCOME MATRIX (USDT / Month on $1,000 Base) ---")
        print(f"{'Leverage':<10} | " + " | ".join(f"{h:>12}" for h in headers))
        print("-" * 115)
        for lev in leverages:
            row_str = f"{lev:>4}x      | "
            cells = []
            for m in margins:
                if g_ret[(lev, m)] == "LIQUIDATED": cells.append(f"{'$0':>12}")
                else: cells.append(f"${g_mo[(lev, m)]:>+10.1f}")
            row_str += " | ".join(cells)
            print(row_str)

    print_matrices("ACCOUNT A ALONE (LONG BTC ONLY)", btc_ret, btc_dd, btc_mo)
    print_matrices("ACCOUNT B ALONE (SHORT ETH ONLY)", eth_ret, eth_dd, eth_mo)

if __name__ == "__main__":
    run_standalone_grid()
