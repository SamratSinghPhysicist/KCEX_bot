#!/usr/bin/env python3
"""
TRUMP Mature Period (Aug 2025 - Sep 2026) & 1-Tick Zero-Fee Scalping Analysis
=============================================================================
1. TRUMP/USDT Mature Period Backtest (2025-08-01 to 2026-09-30)
   - Evaluates whether "maturity" avoids the catastrophic post-launch crash.
   - Compares 100% Capital vs 10% Capital sizing with Zero Fees.
2. 1-Tick Move Chasing on Zero-Fee Pairs (DOGE & TRUMP)
   - Evaluates targeting a 1-tick price change (+1 tick TP).
   - Tests slippages: 0, 1, 2, 3, 4, 5, 6, 7 ticks.
   - Analyzes net expectancy, required win rates, and drawdown recovery math.
"""

import os
import sys
import pandas as pd
import numpy as np
import datetime
from dataclasses import asdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.strategies import Candle, StrategySignal, run_strategy
from experiments.no_stop_loss_experiment import simulate_single_leg
from experiments.analyze_trump_doge_zero_fee import load_local_candles, run_single_asset

CRYPTO_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")


def analyze_trump_mature_period():
    all_candles = load_local_candles("TRUMP", "1h")
    t0 = int(pd.Timestamp("2025-08-01 00:00:00", tz="UTC").timestamp() * 1000)
    t1 = int(pd.Timestamp("2026-09-30 23:59:59", tz="UTC").timestamp() * 1000)
    candles = [c for c in all_candles if c.open_time_ms >= t0 and c.close_time_ms <= t1]

    print("\n" + "=" * 90)
    print("🏛️ PART 1: TRUMP/USDT MATURE REGIME (August 1, 2025 to September 30, 2026)")
    print("=" * 90)
    start_p = candles[0].open
    end_p = candles[-1].close
    high_p = max(c.high for c in candles)
    low_p = min(c.low for c in candles)
    span_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)

    print(f"Candles Count:      {len(candles):,} (1-hour bars)")
    print(f"Duration:           {span_days:.1f} days ({span_days/30.417:.1f} months)")
    print(f"Price Trajectory:   ${start_p:.3f} -> ${end_p:.3f} (Net Change: {((end_p - start_p)/start_p)*100:+.2f}%)")
    print(f"Period High / Low:  High: ${high_p:.3f} | Low: ${low_p:.3f} | Max Drawdown from High: {((low_p - high_p)/high_p)*100:.2f}%")

    # 1. 100% Sizing (No SL, Zero Fees)
    res_100_0f = run_single_asset("TRUMP", candles, 1000.0, zero_fee=True, regime_label="TRUMP Mature 100% (0% Fee)")
    res_100_std = run_single_asset("TRUMP", candles, 1000.0, zero_fee=False, regime_label="TRUMP Mature 100% (Std Fee)")

    print("\n--- 100% CAPITAL ALLOCATION (Zero Fees, No Stop Loss) ---")
    print(f"Initial Capital:    ${res_100_0f['initial_capital']:,.2f}")
    print(f"Final Capital:      ${res_100_0f['final_capital']:,.2f} ({res_100_0f['net_gain_pct']:+.1f}% Net Gain)")
    print(f"Total Trades:       {res_100_0f['trades_count']}")
    
    df100 = res_100_0f["df_trades"]
    if not df100.empty:
        wins = (df100["net_pnl"] > 0).sum()
        print(f"Win Rate:           {wins} / {len(df100)} ({wins/len(df100)*100:.1f}%)")
        print("\nAll Completed Trades:")
        cols = ["entry_dt", "exit_dt", "entry_price", "exit_price", "exit_reason", "duration_hours", "net_pnl", "net_return_pct", "mae_pct"]
        print(df100[cols].to_string(index=False))

    # 2. 10% Sizing (No SL, Zero Fees)
    signals = run_strategy("ema_cross", candles, direction="long")
    cash = 1000.0
    active_until_ms = 0
    trades_10 = []
    for s in signals:
        idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
        c = candles[idx]
        if c.open_time_ms < active_until_ms:
            continue
        pos_size = cash * 0.10
        if pos_size < 1.0:
            continue
        tr = simulate_single_leg(
            direction="LONG", candles=candles, start_idx=idx, entry_px=c.open,
            entry_time_ms=c.open_time_ms, notional=pos_size, margin_used=pos_size,
            tp1_pct=5.0, be_buffer_pct=0.0, tp2_pct=5.0, exit_signal_idx=s.exit_signal_idx,
            resolver=None, symbol="TRUMP", timeframe="1h", tp_rule="mode_dynamic",
            fee_maker_pct=0.0, fee_taker_pct=0.0, exit_on_signal=False
        )
        cash += tr.net_pnl
        active_until_ms = tr.exit_time_ms
        d = asdict(tr)
        d["duration_hours"] = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0
        d["entry_dt"] = pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True)
        d["exit_dt"] = pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True)
        trades_10.append(d)

    df10 = pd.DataFrame(trades_10)
    print("\n--- 10% POSITION SIZING RULE (Zero Fees, No Stop Loss) ---")
    print(f"Initial Capital:    $1,000.00")
    print(f"Final Capital:      ${cash:,.2f} ({((cash-1000)/1000)*100:+.1f}% Net Gain)")
    if not df10.empty:
        wins10 = (df10["net_pnl"] > 0).sum()
        print(f"Win Rate:           {wins10} / {len(df10)} ({wins10/len(df10)*100:.1f}%)")


def analyze_one_tick_microstructure():
    print("\n" + "=" * 90)
    print("⚡ PART 2: 1-TICK MOVE CHASING & SLIPPAGE SENSITIVITY (DOGE & TRUMP)")
    print("=" * 90)

    assets = [
        {"name": "TRUMP/USDT", "typical_price": 2.50, "tick_size": 0.0010, "capital": 1000.0},
        {"name": "DOGE/USDT", "typical_price": 0.12, "tick_size": 0.00001, "capital": 1000.0}
    ]

    slippages = [0, 1, 2, 3, 4, 5, 6, 7]

    for a in assets:
        sym = a["name"]
        px = a["typical_price"]
        ts = a["tick_size"]
        cap = a["capital"]

        tick_bps = (ts / px) * 10000.0
        tick_pct = (ts / px) * 100.0
        dollar_per_1k = cap * (ts / px)

        print(f"\nAsset: {sym} (Benchmark Price: ${px:.4f} | Tick Size: {ts})")
        print(f"  • 1 Tick in Basis Points: {tick_bps:.2f} bps ({tick_pct:.4f}%)")
        print(f"  • Gross Profit on $1,000 Capital for +1 Tick: +${dollar_per_1k:.4f}")
        print("-" * 90)

        rows = []
        for slip in slippages:
            net_ticks = 1 - slip
            net_pct = (net_ticks * ts / px) * 100.0
            net_dollar = cap * (net_pct / 100.0)

            # Scenario 1: Scalping with 3-tick Micro Stop Loss
            # Win = 1 tick - slip. Loss = 3 ticks + slip.
            tp_ticks_realized = 1 - slip
            sl_ticks_realized = 3 + slip
            if tp_ticks_realized > 0:
                req_win_rate = (sl_ticks_realized / (sl_ticks_realized + tp_ticks_realized)) * 100.0
                winrate_str = f"{req_win_rate:.1f}%"
            elif tp_ticks_realized == 0:
                winrate_str = "100.0% (Zero Edge)"
            else:
                winrate_str = "MATHEMATICALLY IMPOSSIBLE (Net Loss on Wins)"

            # Scenario 2: What if 1 adverse trade occurs of -5.0% (-500 bps)?
            # How many 1-tick wins are needed to recover that one drop?
            drop_ticks = int((px * 0.05) / ts)
            if net_ticks > 0:
                recover_wins = int(np.ceil(drop_ticks / net_ticks))
                recovery_str = f"{recover_wins:,} wins"
            else:
                recovery_str = "Never (Negative Expectancy)"

            rows.append({
                "Slippage": f"{slip} tick{'s' if slip != 1 else ''}",
                "Gross Target": "+1 tick",
                "Net Ticks": f"{net_ticks:+d} ticks",
                "Net Return (%)": f"{net_pct:+.4f}%",
                "Dollar PnL ($1,000)": f"${net_dollar:+.3f}",
                "Breakeven Win Rate (3-Tick SL)": winrate_str,
                "Wins to Recover 5% Drop": recovery_str
            })

        df_res = pd.DataFrame(rows)
        print(df_res.to_string(index=False))


if __name__ == "__main__":
    analyze_trump_mature_period()
    analyze_one_tick_microstructure()
