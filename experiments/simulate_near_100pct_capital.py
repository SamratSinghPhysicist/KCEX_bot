#!/usr/bin/env python3
"""
NEAR-Only 100% Capital Backtester & Projector
============================================
Evaluates: What if you ONLY trade NEAR with 100% of your capital?
Rules:
- Long-only, 1x leverage, no stop-loss.
- 100% of capital deployed into each trade (all-in compounding).
- Max 1 trade at a time (if trade is open, all new signals are skipped until exit).
- Evaluates both:
  1. Dynamic Swing (~5.0% TP, BE buffer +0.06%, TP2 +5.0%)
  2. Fixed 0.1% TP (Micro-Scalp)
- Calculates:
  - Final Capital & Net Gain %
  - Peak-to-Trough Unrealized Portfolio Drawdown
  - Maximum Holding Duration (how long you get stuck during bear markets)
  - Rolling returns: 1 Day, 1 Week, 1 Month, 3 Months, 6 Months, 1 Year
"""

import os
import sys
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.strategies import Candle, StrategySignal, run_strategy
from experiments.no_stop_loss_experiment import load_candles, simulate_single_leg, run_baseline_trades, compute_empirical_modes

def run_near_100pct_simulation(
    initial_capital: float = 1000.0,
    strategy_name: str = "ema_cross",
    tp_rule: str = "mode_dynamic",
    fee_maker_pct: float = 0.015,
    fee_taker_pct: float = 0.045,
    be_buffer_pct: float = 0.06
):
    print("=" * 85)
    print(f"🚀 NEAR-ONLY 100% CAPITAL SIMULATION: {tp_rule.upper()}")
    print("=" * 85)

    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    candles = load_candles("NEAR", "1h", crypto_dir, crypto_dir)
    
    t_start = pd.to_datetime(candles[0].open_time_ms, unit="ms", utc=True)
    t_end = pd.to_datetime(candles[-1].close_time_ms, unit="ms", utc=True)
    total_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)
    total_years = total_days / 365.25

    print(f"Asset:               NEAR (NEARUSDT)")
    print(f"Historical Span:     {t_start.strftime('%Y-%m-%d')} to {t_end.strftime('%Y-%m-%d')} ({total_days:.1f} days / {total_years:.2f} years)")
    print(f"Total Candles:       {len(candles):,} 1h bars")
    print(f"Initial Capital:     ${initial_capital:,.2f} Cash (100% Deployed per Trade)")

    # 1. Run Strategy Signals
    signals = run_strategy(strategy_name, candles, direction="long")
    print(f"Total Long Signals:  {len(signals):,}")

    # 2. Determine TP Target
    if tp_rule == "mode_dynamic":
        base_tr = run_baseline_trades(candles, signals, direction_mode="long", fee_maker_pct=fee_maker_pct, fee_taker_pct=fee_taker_pct)
        mode_mfe, mode_mae = compute_empirical_modes(base_tr)
        tp_target = mode_mfe if mode_mfe > 0.10 else 5.0
    elif tp_rule == "fixed_0.1":
        tp_target = 0.10
    else:
        tp_target = 2.0

    print(f"Take-Profit Target:  +{tp_target:.2f}% | BE Buffer: +{be_buffer_pct:.2f}% | Leverage: 1x (No Stop Loss)")

    # 3. Simulate sequential trades (1 trade at a time, 100% capital compounding)
    capital = initial_capital
    active_until_ms = 0
    executed_trades = []
    skipped_signals = 0

    # For mark-to-market equity curve
    daily_equity_map = {}

    for s in signals:
        s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
        c_entry = candles[s_idx] if s_idx < len(candles) else candles[s.candle_idx]
        
        # Check if previous trade is still running
        if c_entry.open_time_ms < active_until_ms:
            skipped_signals += 1
            continue

        entry_px = c_entry.open
        entry_t = c_entry.open_time_ms
        current_margin = capital

        tr = simulate_single_leg(
            direction="LONG",
            candles=candles,
            start_idx=s_idx,
            entry_px=entry_px,
            entry_time_ms=entry_t,
            notional=current_margin,
            margin_used=current_margin,
            tp1_pct=tp_target,
            be_buffer_pct=be_buffer_pct,
            tp2_pct=5.0,
            exit_signal_idx=s.exit_signal_idx,
            resolver=None,
            symbol="NEAR",
            timeframe="1h",
            tp_rule=tp_rule,
            fee_maker_pct=fee_maker_pct,
            fee_taker_pct=fee_taker_pct,
            exit_on_signal=False
        )

        pnl = tr.net_pnl
        capital += pnl
        active_until_ms = tr.exit_time_ms
        dur_hours = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0

        executed_trades.append({
            "entry_time_ms": tr.entry_time_ms,
            "exit_time_ms": tr.exit_time_ms,
            "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
            "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
            "entry_price": tr.entry_price,
            "exit_price": tr.exit_price,
            "margin_deployed": current_margin,
            "net_pnl": pnl,
            "return_pct": tr.net_return_pct,
            "is_win": tr.is_win,
            "exit_reason": tr.exit_reason,
            "mfe_pct": tr.mfe_pct,
            "mae_pct": tr.mae_pct,
            "duration_hours": dur_hours,
            "capital_after": capital
        })

    df_res = pd.DataFrame(executed_trades)
    
    # 4. Master Metrics
    total_executed = len(df_res)
    wins = (df_res["net_pnl"] > 0).sum()
    losses = (df_res["net_pnl"] < 0).sum()
    win_rate = (wins / total_executed * 100.0) if total_executed > 0 else 0.0
    final_capital = capital
    total_gain_usd = final_capital - initial_capital
    total_gain_pct = (total_gain_usd / initial_capital) * 100.0
    cagr = ((final_capital / initial_capital) ** (1.0 / max(0.1, total_years)) - 1.0) * 100.0

    # Max Adverse Excursion & Stuck Durations
    max_mae = df_res["mae_pct"].max()
    longest_stuck_trade = df_res.sort_values("duration_hours", ascending=False).iloc[0]

    print("\n" + "=" * 85)
    print("🏆 PERFORMANCE RESULTS: NEAR ONLY (100% CAPITAL COMPOUNDING)")
    print("=" * 85)
    print(f"Initial Capital:         ${initial_capital:,.2f}")
    print(f"Final Capital:           ${final_capital:,.2f} (Net Gain: +${total_gain_usd:,.2f} / +{total_gain_pct:,.2f}%)")
    print(f"Annualized Growth (CAGR):{cagr:.2f}% per year")
    print(f"Total Completed Trades:  {total_executed:,} | Wins: {wins:,} | Losses: {losses} | Win Rate: {win_rate:.2f}%")
    print(f"Skipped Overlapping Sigs:{skipped_signals:,} (Blocked while waiting for open trade)")
    print(f"Average Trade Duration:  {df_res['duration_hours'].mean():.1f} hours ({df_res['duration_hours'].mean()/24.0:.1f} days)")
    print(f"Median Trade Duration:   {df_res['duration_hours'].median():.1f} hours ({df_res['duration_hours'].median()/24.0:.1f} days)")
    print(f"Longest Trade Duration:  {longest_stuck_trade['duration_hours']:.1f} hours ({longest_stuck_trade['duration_hours']/24.0:.1f} days / {longest_stuck_trade['duration_hours']/(24.0*30.4):.1f} months!)")
    print(f"Longest Stuck Period:    {longest_stuck_trade['entry_dt'].strftime('%Y-%m-%d')} to {longest_stuck_trade['exit_dt'].strftime('%Y-%m-%d')}")
    print(f"Max Unrealized Drawdown: -{max_mae:.2f}% on a single trade (100% account drawdown!)")

    # 5. Build full calendar daily equity curve to measure rolling horizons
    all_days = pd.date_range(start=t_start.floor("D"), end=t_end.floor("D"), freq="D", tz="UTC")
    daily_df = pd.DataFrame(index=all_days)
    
    # Mark closed trade exits
    df_res["exit_day"] = df_res["exit_dt"].dt.floor("D")
    last_cap_per_day = df_res.groupby("exit_day")["capital_after"].last()
    daily_df["closed_equity"] = last_cap_per_day.reindex(all_days).ffill().fillna(initial_capital)

    # Calculate rolling expectancies
    windows = [
        ("1 Day", 1),
        ("1 Week (7d)", 7),
        ("1 Month (30d)", 30),
        ("3 Months (90d)", 90),
        ("6 Months (180d)", 180),
        ("1 Year (365d)", 365),
    ]

    roll_records = []
    for w_name, d in windows:
        diff = daily_df["closed_equity"].diff(d).dropna()
        start = daily_df["closed_equity"].shift(d).dropna()
        pct = (diff / start) * 100.0

        avg_usd = diff.mean()
        med_usd = diff.median()
        avg_pct = pct.mean()
        med_pct = pct.median()
        p10 = pct.quantile(0.10)
        p90 = pct.quantile(0.90)
        p_profit = (diff > 0).mean() * 100.0

        roll_records.append({
            "Time Horizon": w_name,
            "Expected ($)": f"+${avg_usd:,.2f}",
            "Expected (%)": f"+{avg_pct:.2f}%",
            "Median ($)": f"+${med_usd:,.2f}",
            "Median (%)": f"+{med_pct:.2f}%",
            "Typical Range (10th-90th Pct)": f"{p10:+.2f}% to {p90:+.2f}%",
            "Win Prob (%)": f"{p_profit:.1f}%"
        })

    print("\n--- EXPECTED EARNINGS BY TIME HORIZON (NEAR 100% CAPITAL) ---")
    df_roll = pd.DataFrame(roll_records)
    print(df_roll.to_string(index=False))

    return final_capital, df_roll, df_res

if __name__ == "__main__":
    # 1. Dynamic Swing (~5% TP)
    run_near_100pct_simulation(initial_capital=1000.0, tp_rule="mode_dynamic")

    # 2. Fixed 0.1% TP (Micro-Scalp)
    run_near_100pct_simulation(initial_capital=1000.0, tp_rule="fixed_0.1")
