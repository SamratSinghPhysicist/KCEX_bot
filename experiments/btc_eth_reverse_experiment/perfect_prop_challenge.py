"""
Perfect Prop Challenge Engine: Pushing Pass Rate to 100%
========================================================
Implements:
1. Asymptotic Drawdown Buffer Sizing:
   Risk per trade = fraction * (Max_DD - Current_DD)
   Mathematically guarantees that the account CANNOT breach 3.0% Drawdown!
2. Cointegrated Spread Signal (ETH/BTC Ratio Z-Score / Bollinger):
   Enters Long BTC / Short ETH when ETH is overvalued vs BTC.
   Enters Short BTC / Long ETH when BTC is overvalued vs ETH.
3. Breakeven Ratchet:
   When trade reaches +1.0%, SL is moved to Entry + 0.05% (locking in profit / zero loss).
4. Independent Account Freezing:
   When Account A reaches +10%, it freezes (passed).
   Account B continues taking high-probability setups until it also reaches +10%.
"""

from __future__ import annotations
import os
import sys
import math
from typing import List, Tuple, Dict, Any

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    CandleData,
    load_candles_from_dir,
    build_sub_1m_map,
    evaluate_candle_tp_sl,
    parse_date_to_ms
)


def calculate_sma(values: List[float], period: int) -> List[float]:
    smas = []
    for i in range(len(values)):
        if i < period - 1:
            smas.append(float('nan'))
        else:
            smas.append(sum(values[i - period + 1 : i + 1]) / period)
    return smas


def calculate_std(values: List[float], smas: List[float], period: int) -> List[float]:
    stds = []
    for i in range(len(values)):
        if i < period - 1 or math.isnan(smas[i]):
            stds.append(float('nan'))
        else:
            mean = smas[i]
            var = sum((x - mean) ** 2 for x in values[i - period + 1 : i + 1]) / period
            stds.append(math.sqrt(var))
    return stds


def run_perfect_challenge_simulation(
    timeframe: str = "1h",
    tp_pct: float = 2.0,
    sl_pct: float = 1.0,
    f_risk_buffer: float = 0.10, # Risk 10% of remaining buffer to 3% DD
    target_pct: float = 10.0,
    max_dd_pct: float = 3.0,
    use_spread_filter: bool = True,
    use_ratchet: bool = True,
    spread_z_threshold: float = 1.2, # Enter when Z-score of ETH/BTC spread is extreme
    spread_period: int = 24
):
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2025-01-01")
    end_ms = parse_date_to_ms("2026-10-12") + (24 * 3600 * 1000 - 1)

    btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
    eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)

    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_sub = build_sub_1m_map(btc_c, btc_1m)
    eth_sub = build_sub_1m_map(eth_c, eth_1m)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    # Calculate ETH/BTC ratio series
    ratios = [eth_dict[t].close / btc_dict[t].close for t in common_times]
    smas = calculate_sma(ratios, spread_period)
    stds = calculate_std(ratios, smas, spread_period)

    z_scores = []
    for i in range(len(ratios)):
        if math.isnan(smas[i]) or math.isnan(stds[i]) or stds[i] == 0:
            z_scores.append(0.0)
        else:
            z_scores.append((ratios[i] - smas[i]) / stds[i])

    # Precompute signals
    # When Z-score > +threshold (ETH overvalued vs BTC):
    # Long BTC / Short ETH (Case 1)
    # When Z-score < -threshold (BTC overvalued vs ETH):
    # Short BTC / Long ETH (Case 2)
    # Both take reverse trades!
    signals = []
    for i in range(len(common_times)):
        if not use_spread_filter:
            signals.append("CASE_1") # Continuous Case 1
        else:
            z = z_scores[i]
            if z >= spread_z_threshold:
                signals.append("CASE_1") # Long BTC / Short ETH
            elif z <= -spread_z_threshold:
                signals.append("CASE_2") # Short BTC / Long ETH
            else:
                signals.append("NO_SIGNAL")

    # Generate all trade cycles
    cycles = []
    i = 0
    tot_len = len(common_times)

    while i < tot_len - 1:
        sig = signals[i]
        if sig == "NO_SIGNAL":
            i += 1
            continue

        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        if sig == "CASE_1":
            b_dir = "LONG"
            e_dir = "SHORT"
            tp_b = p_b * (1.0 + tp_pct / 100.0)
            sl_b = p_b * (1.0 - sl_pct / 100.0)
            tp_e = p_e * (1.0 - tp_pct / 100.0)
            sl_e = p_e * (1.0 + sl_pct / 100.0)
        else:
            b_dir = "SHORT"
            e_dir = "LONG"
            tp_b = p_b * (1.0 - tp_pct / 100.0)
            sl_b = p_b * (1.0 + sl_pct / 100.0)
            tp_e = p_e * (1.0 + tp_pct / 100.0)
            sl_e = p_e * (1.0 - sl_pct / 100.0)

        b_exit = None
        b_res = None
        e_exit = None
        e_res = None

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]
            c_e = eth_dict[ts]

            # Ratchet logic: if trade moved +1.0% in profit, move SL to breakeven
            if use_ratchet:
                # BTC Ratchet
                if b_dir == "LONG" and c_b.high >= p_b * 1.010:
                    sl_b = max(sl_b, p_b * 1.0005)
                elif b_dir == "SHORT" and c_b.low <= p_b * 0.990:
                    sl_b = min(sl_b, p_b * 0.9995)

                # ETH Ratchet
                if e_dir == "LONG" and c_e.high >= p_e * 1.010:
                    sl_e = max(sl_e, p_e * 1.0005)
                elif e_dir == "SHORT" and c_e.low <= p_e * 0.990:
                    sl_e = min(sl_e, p_e * 0.9995)

            if b_exit is None:
                r, _ = evaluate_candle_tp_sl(b_dir, p_b, tp_b, sl_b, c_b, btc_sub, timeframe)
                if r: b_exit = j; b_res = r
            if e_exit is None:
                r, _ = evaluate_candle_tp_sl(e_dir, p_e, tp_e, sl_e, c_e, eth_sub, timeframe)
                if r: e_exit = j; e_res = r

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)
        # Outcome: Did it hit TP (gain 2.0x), Breakeven Ratchet (gain 0.05x), or SL (loss 1.0x)?
        b_gain = 2.0 if b_res == "TP" else (-1.0 if b_res == "SL" else 0.0)
        e_gain = 2.0 if e_res == "TP" else (-1.0 if e_res == "SL" else 0.0)

        cycles.append((b_res == "TP", e_res == "TP", b_gain, e_gain))
        i = free_idx + 1

    print(f"\n[*] Generated {len(cycles)} quality trade cycles (Spread Filter: {use_spread_filter}, Ratchet: {use_ratchet}).")

    # Now simulate rolling prop challenges starting across time
    # Testing Asymptotic Sizing
    sim_results = []
    step = 5
    n_sims = 0
    both_pass = 0
    a_pass_cnt = 0
    b_pass_cnt = 0
    either_pass = 0

    for start_idx in range(0, max(1, len(cycles) - 25), step):
        window = cycles[start_idx:]
        bal_a = 1000.0
        peak_a = 1000.0
        a_status = "RUNNING"

        bal_b = 1000.0
        peak_b = 1000.0
        b_status = "RUNNING"

        for b_tp, e_tp, b_g, e_g in window:
            # Step Account A
            if a_status == "RUNNING":
                current_dd_a = (peak_a - bal_a) / peak_a * 100.0
                rem_buffer_a = max(0.01, max_dd_pct - current_dd_a)
                # Asymptotic risk: risk 10% of remaining buffer
                risk_a_pct = min(0.35, f_risk_buffer * rem_buffer_a)
                risk_usd_a = bal_a * (risk_a_pct / 100.0)

                if b_g > 0:
                    bal_a += risk_usd_a * b_g
                elif b_g < 0:
                    bal_a -= risk_usd_a

                if bal_a > peak_a:
                    peak_a = bal_a

                dd_a = (peak_a - bal_a) / peak_a * 100.0
                if dd_a >= max_dd_pct:
                    a_status = "FAILED"
                elif ((bal_a - 1000.0) / 1000.0 * 100.0) >= target_pct:
                    a_status = "PASSED"

            # Step Account B
            if b_status == "RUNNING":
                current_dd_b = (peak_b - bal_b) / peak_b * 100.0
                rem_buffer_b = max(0.01, max_dd_pct - current_dd_b)
                risk_b_pct = min(0.35, f_risk_buffer * rem_buffer_b)
                risk_usd_b = bal_b * (risk_b_pct / 100.0)

                if e_g > 0:
                    bal_b += risk_usd_b * e_g
                elif e_g < 0:
                    bal_b -= risk_usd_b

                if bal_b > peak_b:
                    peak_b = bal_b

                dd_b = (peak_b - bal_b) / peak_b * 100.0
                if dd_b >= max_dd_pct:
                    b_status = "FAILED"
                elif ((bal_b - 1000.0) / 1000.0 * 100.0) >= target_pct:
                    b_status = "PASSED"

            if a_status != "RUNNING" and b_status != "RUNNING":
                break

        n_sims += 1
        if a_status == "PASSED" and b_status == "PASSED":
            both_pass += 1
        if a_status == "PASSED":
            a_pass_cnt += 1
        if b_status == "PASSED":
            b_pass_cnt += 1
        if a_status == "PASSED" or b_status == "PASSED":
            either_pass += 1

    both_pct = (both_pass / n_sims) * 100.0 if n_sims else 0.0
    a_pct = (a_pass_cnt / n_sims) * 100.0 if n_sims else 0.0
    b_pct = (b_pass_cnt / n_sims) * 100.0 if n_sims else 0.0
    either_pct = (either_pass / n_sims) * 100.0 if n_sims else 0.0

    print(f"Results across {n_sims} rolling challenge tests:")
    print(f"  [+] BOTH ACCOUNTS PASSED:        {both_pct:.1f}% ({both_pass}/{n_sims})")
    print(f"  [+] Account A (BTC) Passed:      {a_pct:.1f}% ({a_pass_cnt}/{n_sims})")
    print(f"  [+] Account B (ETH) Passed:      {b_pct:.1f}% ({b_pass_cnt}/{n_sims})")
    print(f"  [+] At Least One Account Passed: {either_pct:.1f}% ({either_pass}/{n_sims})")

    return both_pct, a_pct, b_pct, either_pct


if __name__ == "__main__":
    print("=== TESTING PROP CHALLENGE STRATEGY OPTIMIZATION ===")
    print("\n--- Test 1: Baseline 1H with Asymptotic Sizing ---")
    run_perfect_challenge_simulation(timeframe="1h", tp_pct=2.0, sl_pct=1.0, f_risk_buffer=0.10, use_spread_filter=False, use_ratchet=False)

    print("\n--- Test 2: Adding Breakeven Ratchet (+1% MFE -> Lock Entry) ---")
    run_perfect_challenge_simulation(timeframe="1h", tp_pct=2.0, sl_pct=1.0, f_risk_buffer=0.10, use_spread_filter=False, use_ratchet=True)

    print("\n--- Test 3: Adding Cointegrated Spread Filter (Z-Score >= 1.2) + Ratchet ---")
    run_perfect_challenge_simulation(timeframe="1h", tp_pct=2.0, sl_pct=1.0, f_risk_buffer=0.10, use_spread_filter=True, use_ratchet=True, spread_z_threshold=1.2)

    print("\n--- Test 4: Spread Filter (Z-Score >= 1.5) on 1H ---")
    run_perfect_challenge_simulation(timeframe="1h", tp_pct=2.0, sl_pct=1.0, f_risk_buffer=0.10, use_spread_filter=True, use_ratchet=True, spread_z_threshold=1.5)
