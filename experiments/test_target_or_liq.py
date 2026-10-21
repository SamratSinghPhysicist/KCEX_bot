#!/usr/bin/env python3
"""
Test: Run Until Target or Liquidation (No Indicator Exit)
========================================================
1. Direction 'both' = Allows both Long and Short signals as separate directional trades
   (NOT simultaneous pair trades).
2. Exit rule = Let position run until:
   - TP1 (and runner to TP2 or BE stop)
   - Liquidation:
     * Long: Price drops to 0 (100% loss)
     * Short: Price doubles (+100% price rise, High >= 2.0 * entry_px)
   - End of historical data (mark-to-market at last bar).
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.no_stop_loss_experiment import load_candles, Candle
from experiments.strategies import run_strategy, StrategySignal
from experiments.dispute_resolver import OneMinuteDisputeResolver


def simulate_run_until_target_or_liq(
    direction: str,
    candles: List[Candle],
    start_idx: int,
    entry_px: float,
    entry_time_ms: int,
    notional: float,
    tp1_pct: float,
    be_buffer_pct: float,
    tp2_pct: float,
    resolver: Optional[OneMinuteDisputeResolver],
    symbol: str,
    timeframe: str,
    fee_maker_pct: float = 0.015,
    fee_taker_pct: float = 0.045
) -> Dict[str, Any]:
    n = len(candles)
    entry_fee = notional * (fee_maker_pct / 100.0)
    half_notional = notional / 2.0

    # Targets & Liquidation levels
    if direction == "LONG":
        tp1_px = entry_px * (1.0 + tp1_pct / 100.0)
        be_stop_px = entry_px * (1.0 + be_buffer_pct / 100.0)
        tp2_px = entry_px * (1.0 + tp2_pct / 100.0)
        liq_px = 0.0  # 1x leverage long cannot liquidate unless price hits 0
    else:
        tp1_px = entry_px * (1.0 - tp1_pct / 100.0)
        be_stop_px = entry_px * (1.0 - be_buffer_pct / 100.0)
        tp2_px = entry_px * (1.0 - tp2_pct / 100.0)
        liq_px = entry_px * 2.0  # 1x leverage short liquidates when price doubles (+100%)

    tp1_hit = False
    tp1_gross = 0.0
    tp1_exit_fee = 0.0
    tp1_time_ms = 0
    runner_closed = False
    runner_gross = 0.0
    runner_exit_fee = 0.0
    exit_reason = "END_OF_DATA"
    exit_time_ms = candles[-1].close_time_ms
    exit_px = candles[-1].close

    mfe = 0.0
    mae = 0.0

    for i in range(start_idx, n):
        c = candles[i]

        # Track excursions
        if direction == "LONG":
            c_mfe = (c.high - entry_px) / entry_px * 100.0
            c_mae = (entry_px - c.low) / entry_px * 100.0
        else:
            c_mfe = (entry_px - c.low) / entry_px * 100.0
            c_mae = (c.high - entry_px) / entry_px * 100.0
        mfe = max(mfe, c_mfe)
        mae = max(mae, c_mae)

        # ─── PHASE 1: TP1 NOT HIT YET ───
        if not tp1_hit:
            # Check liquidation first
            is_liquidated = False
            if direction == "LONG":
                if c.low <= liq_px:
                    is_liquidated = True
            else:
                if c.high >= liq_px:
                    is_liquidated = True

            if is_liquidated:
                exit_reason = "LIQUIDATION"
                exit_px = liq_px
                exit_time_ms = c.open_time_ms
                gross = -notional  # 100% loss of collateral
                exit_fee = notional * (fee_taker_pct / 100.0)
                net_pnl = gross - entry_fee - exit_fee
                return {
                    "direction": direction,
                    "entry_time": entry_time_ms,
                    "exit_time": exit_time_ms,
                    "duration_hours": (exit_time_ms - entry_time_ms) / (1000.0 * 3600.0),
                    "entry_px": entry_px,
                    "exit_px": exit_px,
                    "exit_reason": exit_reason,
                    "tp1_hit": False,
                    "mfe_pct": mfe,
                    "mae_pct": mae,
                    "net_pnl": net_pnl,
                    "is_win": False
                }

            # Check TP1
            hit_tp1 = (c.high >= tp1_px) if direction == "LONG" else (c.low <= tp1_px)
            if hit_tp1:
                tp1_hit = True
                tp1_time_ms = c.open_time_ms
                tp1_gross = half_notional * ((tp1_px - entry_px) / entry_px) if direction == "LONG" else half_notional * ((entry_px - tp1_px) / entry_px)
                tp1_exit_fee = half_notional * (fee_taker_pct / 100.0)

                # Check if runner hits TP2 or BE in this same candle
                hit_tp2 = (c.high >= tp2_px) if direction == "LONG" else (c.low <= tp2_px)
                hit_be = (c.low <= be_stop_px) if direction == "LONG" else (c.high >= be_stop_px)
                if hit_tp2 or hit_be:
                    runner_closed = True
                    runner_time_ms = c.open_time_ms
                    if hit_tp2:
                        exit_reason = "TP1_TP2"
                        runner_actual_px = tp2_px
                    else:
                        exit_reason = "TP1_BE"
                        runner_actual_px = be_stop_px
                    runner_gross = half_notional * ((runner_actual_px - entry_px) / entry_px) if direction == "LONG" else half_notional * ((entry_px - runner_actual_px) / entry_px)
                    runner_exit_fee = half_notional * (fee_taker_pct / 100.0)
                    break
                continue

        # ─── PHASE 2: RUNNER ACTIVE (TP1 ALREADY HIT) ───
        else:
            hit_tp2 = (c.high >= tp2_px) if direction == "LONG" else (c.low <= tp2_px)
            hit_be = (c.low <= be_stop_px) if direction == "LONG" else (c.high >= be_stop_px)

            if hit_tp2 or hit_be:
                runner_closed = True
                runner_time_ms = c.open_time_ms
                if hit_tp2:
                    exit_reason = "TP1_TP2"
                    runner_actual_px = tp2_px
                else:
                    exit_reason = "TP1_BE"
                    runner_actual_px = be_stop_px
                runner_gross = half_notional * ((runner_actual_px - entry_px) / entry_px) if direction == "LONG" else half_notional * ((entry_px - runner_actual_px) / entry_px)
                runner_exit_fee = half_notional * (fee_taker_pct / 100.0)
                break

    # If reached end of historical data
    if not tp1_hit:
        exit_reason = "END_OF_DATA_UNRESOLVED"
        exit_px = candles[-1].close
        exit_time_ms = candles[-1].close_time_ms
        gross = notional * ((exit_px - entry_px) / entry_px) if direction == "LONG" else notional * ((entry_px - exit_px) / entry_px)
        exit_fee = notional * (fee_taker_pct / 100.0)
        net_pnl = gross - entry_fee - exit_fee
    else:
        if not runner_closed:
            # Runner still running at end of data
            exit_reason = "TP1_END_OF_DATA"
            runner_actual_px = candles[-1].close
            runner_time_ms = candles[-1].close_time_ms
            runner_gross = half_notional * ((runner_actual_px - entry_px) / entry_px) if direction == "LONG" else half_notional * ((entry_px - runner_actual_px) / entry_px)
            runner_exit_fee = half_notional * (fee_taker_pct / 100.0)

        total_gross = tp1_gross + runner_gross
        total_exit_fee = tp1_exit_fee + runner_exit_fee
        net_pnl = total_gross - entry_fee - total_exit_fee
        exit_time_ms = runner_time_ms

    return {
        "direction": direction,
        "entry_time": entry_time_ms,
        "exit_time": exit_time_ms,
        "duration_hours": (exit_time_ms - entry_time_ms) / (1000.0 * 3600.0),
        "entry_px": entry_px,
        "exit_px": exit_px,
        "exit_reason": exit_reason,
        "tp1_hit": tp1_hit,
        "mfe_pct": mfe,
        "mae_pct": mae,
        "net_pnl": net_pnl,
        "is_win": (net_pnl > 0.0)
    }


def test_asset(asset: str, tf: str = "1h", tp_rule: str = "fixed_0.1", strategy: str = "ema_cross"):
    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    stocks_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Stocks")
    candles = load_candles(asset, tf, crypto_dir, stocks_dir)

    # Run strategy for signals (both long and short signals)
    signals = run_strategy(strategy, candles, direction="both")
    print(f"\n=======================================================")
    print(f"Testing {asset} ({tf}) | Strategy: {strategy} | TP Rule: {tp_rule}")
    print(f"Total Candlesticks: {len(candles):,} | Total Signals Generated: {len(signals):,}")
    print(f"Rule: NEVER EXIT ON INDICATOR SIGNALS -> RUN TO TP OR LIQ (1x leverage)")
    print(f"=======================================================")

    tp1_pct = 0.10 if tp_rule == "fixed_0.1" else 1.0

    results = []
    for sig in signals:
        res = simulate_run_until_target_or_liq(
            direction=sig.direction,
            candles=candles,
            start_idx=sig.candle_idx,
            entry_px=sig.entry_price,
            entry_time_ms=sig.entry_time_ms,
            notional=1000.0,
            tp1_pct=tp1_pct,
            be_buffer_pct=0.06,
            tp2_pct=5.0,
            resolver=None,
            symbol=asset,
            timeframe=tf
        )
        results.append(res)

    df = pd.DataFrame(results)
    total_trades = len(df)
    wins = len(df[df["net_pnl"] > 0])
    losses = len(df[df["net_pnl"] < 0])
    liqs = len(df[df["exit_reason"] == "LIQUIDATION"])
    still_open = len(df[df["exit_reason"] == "END_OF_DATA_UNRESOLVED"])
    tp1_hits = len(df[df["tp1_hit"] == True])
    win_rate = (wins / total_trades * 100.0) if total_trades > 0 else 0.0
    net_pnl = df["net_pnl"].sum()
    avg_dur = df["duration_hours"].mean()
    median_dur = df["duration_hours"].median()
    max_dur = df["duration_hours"].max()

    print(f"RESULTS FOR {asset} (Both Long & Short Signals Allowed):")
    print(f"  Total Trades Taken:       {total_trades:,}")
    print(f"  Trades that Hit TP1:      {tp1_hits:,} ({tp1_hits/total_trades*100:.2f}%)")
    print(f"  Winning Trades:           {wins:,} ({win_rate:.2f}%)")
    print(f"  Losing Trades:            {losses:,} ({losses/total_trades*100:.2f}%)")
    print(f"  Liquidated Trades:        {liqs:,} (Shorts doubling: {liqs})")
    print(f"  Unresolved at End:        {still_open:,}")
    print(f"  Net PnL ($):              ${net_pnl:,.2f}")
    print(f"  Avg Trade Duration:       {avg_dur:.1f} hours ({avg_dur/24:.1f} days)")
    print(f"  Median Trade Duration:    {median_dur:.1f} hours")
    print(f"  Max Trade Duration:       {max_dur:.1f} hours ({max_dur/24:.1f} days)")
    
    # Separate Long vs Short breakdown
    df_long = df[df["direction"] == "LONG"]
    df_short = df[df["direction"] == "SHORT"]
    print(f"\n  --- LONG Trades Breakdown ---")
    print(f"    Trades: {len(df_long):,} | Wins: {len(df_long[df_long['net_pnl'] > 0]):,} | Losses: {len(df_long[df_long['net_pnl'] < 0]):,} | TP1 Hits: {len(df_long[df_long['tp1_hit']]):,}")
    print(f"    Net PnL: ${df_long['net_pnl'].sum():,.2f}")
    
    print(f"\n  --- SHORT Trades Breakdown ---")
    print(f"    Trades: {len(df_short):,} | Wins: {len(df_short[df_short['net_pnl'] > 0]):,} | Losses: {len(df_short[df_short['net_pnl'] < 0]):,} | Liquidations: {len(df_short[df_short['exit_reason'] == 'LIQUIDATION']):,}")
    print(f"    Net PnL: ${df_short['net_pnl'].sum():,.2f}")


if __name__ == "__main__":
    for a in ["BTC", "ETH", "GOLD", "AAPL", "NVDA", "TSLA"]:
        test_asset(a, "1h", tp_rule="fixed_0.1", strategy="ema_cross")
