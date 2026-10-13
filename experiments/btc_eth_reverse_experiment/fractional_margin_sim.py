"""
Fractional Margin Simulation for BTC/ETH Reverse Dual-Account Strategy
Evaluates performance when using fractional margin (e.g. 2%, 5%, 10%, 15%, 20%, 25%, 33%, 50%)
instead of 100% margin per trade under Prop Firm Rules:
- Target: +10% Net Profit
- Max Drawdown: 3.0% (trailing from peak)
- Initial Balance: 1000 USDT on both accounts
- 2x Leverage
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
    parse_date_to_ms
)

def run_fractional_sim():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2025-01-01")
    end_ms = parse_date_to_ms("2026-10-12") + (24 * 3600 * 1000 - 1)

    timeframes = ["1h", "4h"]
    configs = [
        ("Config 1 (TP 3.0%, SL 3.0%)", 3.0, 3.0),
        ("Config 2 (TP 1.5%, SL 1.5%)", 1.5, 1.5),
        ("Config 3 (TP 1.5%, SL 3.0%)", 1.5, 3.0),
        ("Config 4 (TP 0.75%, SL 1.5%)", 0.75, 1.5),
    ]

    margin_fractions = [0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.33, 0.50]
    leverage = 2.0

    print("=" * 80)
    print("FRACTIONAL MARGIN SIMULATION: DUAL ACCOUNTS (BTC & ETH REVERSE)")
    print("Target: +10.0% | Max Drawdown: 3.0% | Initial: 1000 USDT | Leverage: 2x")
    print("=" * 80)

    for tf in timeframes:
        btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
        eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)
        btc_c = load_candles_from_dir("BTCUSDT", tf, base_dir, start_ms, end_ms)
        eth_c = load_candles_from_dir("ETHUSDT", tf, base_dir, start_ms, end_ms)

        btc_sub = build_sub_1m_map(btc_c, btc_1m)
        eth_sub = build_sub_1m_map(eth_c, eth_1m)

        btc_dict = {c.open_time_ms: c for c in btc_c}
        eth_dict = {c.open_time_ms: c for c in eth_c}
        common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

        print(f"\n>>> TIMEFRAME: {tf.upper()} (Total candles: {len(common_times)})")

        for cfg_name, tp_pct, sl_pct in configs:
            # Generate trade cycles
            # Case 1: Long BTC, Short ETH
            cycles = []
            i = 0
            tot_len = len(common_times)
            while i < tot_len - 1:
                entry_ts = common_times[i]
                p_b = btc_dict[entry_ts].open
                p_e = eth_dict[entry_ts].open

                tp_b = p_b * (1.0 + tp_pct / 100.0)
                sl_b = p_b * (1.0 - sl_pct / 100.0)
                tp_e = p_e * (1.0 - tp_pct / 100.0)
                sl_e = p_e * (1.0 + sl_pct / 100.0)

                b_exit, b_res = None, None
                e_exit, e_res = None, None

                j = i
                while j < tot_len:
                    ts = common_times[j]
                    if b_exit is None:
                        r, _ = evaluate_candle_tp_sl("LONG", p_b, tp_b, sl_b, btc_dict[ts], btc_sub, tf)
                        if r: b_exit = j; b_res = r
                    if e_exit is None:
                        r, _ = evaluate_candle_tp_sl("SHORT", p_e, tp_e, sl_e, eth_dict[ts], eth_sub, tf)
                        if r: e_exit = j; e_res = r
                    if b_exit is not None and e_exit is not None:
                        break
                    j += 1

                if b_exit is None or e_exit is None:
                    break

                cycles.append((b_res == "TP", e_res == "TP"))
                i = max(b_exit, e_exit) + 1

            if not cycles:
                continue

            print(f"\n--- {cfg_name} | Cycles: {len(cycles)} ---")
            print(f"{'Margin %':>10} | {'Risk/Loss %':>12} | {'Reward/Win %':>13} | {'Both Pass %':>12} | {'>=1 Pass %':>11} | {'A Pass %':>9} | {'B Pass %':>9}")
            print("-" * 90)

            for m_frac in margin_fractions:
                # With margin fraction m_frac and leverage 2x:
                # Position size = Balance * m_frac * 2.0
                # When SL hit: loss = Position size * (sl_pct / 100) = Balance * (m_frac * 2.0 * sl_pct / 100)
                # When TP hit: gain = Position size * (tp_pct / 100) = Balance * (m_frac * 2.0 * tp_pct / 100)
                loss_per_trade_pct = m_frac * leverage * sl_pct
                gain_per_trade_pct = m_frac * leverage * tp_pct

                # Simulate rolling challenges across cycles
                step = 2
                both_pass = 0
                either_pass = 0
                a_pass = 0
                b_pass = 0
                n_sims = 0

                for s_idx in range(0, max(1, len(cycles) - 20), step):
                    window = cycles[s_idx:]
                    bal_a, peak_a, stat_a = 1000.0, 1000.0, "RUNNING"
                    bal_b, peak_b, stat_b = 1000.0, 1000.0, "RUNNING"

                    for b_tp, e_tp in window:
                        if stat_a == "RUNNING":
                            pos_a = bal_a * m_frac * leverage
                            if b_tp:
                                bal_a += pos_a * (tp_pct / 100.0)
                            else:
                                bal_a -= pos_a * (sl_pct / 100.0)

                            if bal_a > peak_a: peak_a = bal_a
                            dd_a = (peak_a - bal_a) / peak_a * 100.0
                            if dd_a >= 3.0:
                                stat_a = "FAILED"
                            elif ((bal_a - 1000.0) / 1000.0 * 100.0) >= 10.0:
                                stat_a = "PASSED"

                        if stat_b == "RUNNING":
                            pos_b = bal_b * m_frac * leverage
                            if e_tp:
                                bal_b += pos_b * (tp_pct / 100.0)
                            else:
                                bal_b -= pos_b * (sl_pct / 100.0)

                            if bal_b > peak_b: peak_b = bal_b
                            dd_b = (peak_b - bal_b) / peak_b * 100.0
                            if dd_b >= 3.0:
                                stat_b = "FAILED"
                            elif ((bal_b - 1000.0) / 1000.0 * 100.0) >= 10.0:
                                stat_b = "PASSED"

                        if stat_a != "RUNNING" and stat_b != "RUNNING":
                            break

                    n_sims += 1
                    if stat_a == "PASSED" and stat_b == "PASSED": both_pass += 1
                    if stat_a == "PASSED" or stat_b == "PASSED": either_pass += 1
                    if stat_a == "PASSED": a_pass += 1
                    if stat_b == "PASSED": b_pass += 1

                bp_pct = (both_pass / n_sims) * 100.0 if n_sims else 0.0
                ep_pct = (either_pass / n_sims) * 100.0 if n_sims else 0.0
                ap_pct = (a_pass / n_sims) * 100.0 if n_sims else 0.0
                b_pct = (b_pass / n_sims) * 100.0 if n_sims else 0.0

                print(f"{m_frac*100:>9.1f}% | {loss_per_trade_pct:>11.2f}% | {gain_per_trade_pct:>12.2f}% | {bp_pct:>11.1f}% | {ep_pct:>10.1f}% | {ap_pct:>8.1f}% | {b_pct:>8.1f}%")

if __name__ == "__main__":
    run_fractional_sim()
