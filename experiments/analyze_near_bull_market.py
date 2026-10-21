#!/usr/bin/env python3
"""
NEAR 100% Capital Simulation in Non-Bear / Bull Regimes
======================================================
Analyzes performance when the market is NOT in a multi-year bear market:
1. The 2020-2021 Macro Bull Market (Oct 2020 to Dec 2021)
2. The 2023-2024 Crypto Bull Market (Oct 2023 to Oct 2024)
3. Normalized Active Trading Regime (Excluding the single 2022 outlier freeze)
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
from experiments.no_stop_loss_experiment import load_candles, simulate_single_leg

def run_near_regime(start_date_str, end_date_str, label):
    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    all_candles = load_candles("NEAR", "1h", crypto_dir, crypto_dir)
    
    t0_ms = int(pd.Timestamp(start_date_str, tz="UTC").timestamp() * 1000)
    t1_ms = int(pd.Timestamp(end_date_str, tz="UTC").timestamp() * 1000)
    
    candles = [c for c in all_candles if c.open_time_ms >= t0_ms and c.close_time_ms <= t1_ms]
    if len(candles) < 50:
        print(f"Insufficient candles for {label}")
        return
        
    span_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)
    print("\n" + "=" * 85)
    print(f"🐂 REGIME ANALYSIS: {label}")
    print(f"Period: {start_date_str} to {end_date_str} ({span_days:.1f} days / {span_days/30.417:.1f} months)")
    print("=" * 85)

    signals = run_strategy("ema_cross", candles, direction="long")
    signals = [s for s in signals if s.entry_time_ms >= t0_ms and s.entry_time_ms <= t1_ms]
    
    capital = 1000.0
    active_until_ms = 0
    executed_trades = []
    skipped = 0
    
    for s in signals:
        s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
        c_entry = candles[s_idx] if s_idx < len(candles) else candles[s.candle_idx]
        if c_entry.open_time_ms < active_until_ms:
            skipped += 1
            continue
            
        entry_px = c_entry.open
        current_margin = capital
        
        tr = simulate_single_leg(
            direction="LONG",
            candles=candles,
            start_idx=s_idx,
            entry_px=entry_px,
            entry_time_ms=c_entry.open_time_ms,
            notional=current_margin,
            margin_used=current_margin,
            tp1_pct=5.0,
            be_buffer_pct=0.06,
            tp2_pct=5.0,
            exit_signal_idx=s.exit_signal_idx,
            resolver=None,
            symbol="NEAR",
            timeframe="1h",
            tp_rule="mode_dynamic",
            fee_maker_pct=0.015,
            fee_taker_pct=0.045,
            exit_on_signal=False
        )
        
        capital += tr.net_pnl
        active_until_ms = tr.exit_time_ms
        dur_h = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0
        
        executed_trades.append({
            "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
            "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
            "entry_price": tr.entry_price,
            "exit_price": tr.exit_price,
            "margin": current_margin,
            "net_pnl": tr.net_pnl,
            "net_ret_pct": tr.net_return_pct,
            "duration_hours": dur_h,
            "capital_after": capital,
            "is_win": tr.is_win,
            "exit_reason": tr.exit_reason
        })
        
    df = pd.DataFrame(executed_trades)
    if df.empty:
        print("No completed trades.")
        return
        
    n_exec = len(df)
    wins = (df["is_win"]).sum()
    final_cap = capital
    gain_pct = (final_cap / 1000.0 - 1.0) * 100.0
    cagr = ((final_cap / 1000.0) ** (1.0 / max(0.1, span_days / 365.25)) - 1.0) * 100.0
    
    print(f"Initial Capital:         $1,000.00")
    print(f"Final Capital:           ${final_cap:,.2f} (+{gain_pct:,.1f}% Net Gain)")
    print(f"Annualized Growth (CAGR):{cagr:.1f}% per year")
    print(f"Total Completed Trades:  {n_exec} (Wins: {wins}, Win Rate: {wins/n_exec*100:.1f}%)")
    print(f"Average Duration:        {df['duration_hours'].mean():.1f} hours ({df['duration_hours'].mean()/24.0:.1f} days)")
    print(f"Median Duration:         {df['duration_hours'].median():.1f} hours ({df['duration_hours'].median()/24.0:.1f} days)")
    print(f"Longest Trade Duration:  {df['duration_hours'].max():.1f} hours ({df['duration_hours'].max()/24.0:.1f} days)")

    # Rolling window expectancies
    start_dt = pd.to_datetime(candles[0].open_time_ms, unit="ms", utc=True).floor("D")
    end_dt = pd.to_datetime(candles[-1].close_time_ms, unit="ms", utc=True).floor("D")
    all_days = pd.date_range(start=start_dt, end=end_dt, freq="D")
    df["exit_day"] = df["exit_dt"].dt.floor("D")
    last_cap = df.groupby("exit_day")["capital_after"].last()
    daily_s = last_cap.reindex(all_days).ffill().fillna(1000.0)
    
    windows = [("1 Day", 1), ("1 Week (7d)", 7), ("1 Month (30d)", 30), ("3 Months (90d)", 90), ("6 Months (180d)", 180), ("1 Year (365d)", 365)]
    res = []
    for w_name, d in windows:
        if len(daily_s) < d:
            continue
        diff = daily_s.diff(d).dropna()
        start = daily_s.shift(d).dropna()
        pct = (diff / start) * 100.0
        res.append({
            "Time Horizon": w_name,
            "Expected Profit ($)": f"+${diff.mean():,.2f}",
            "Expected Gain (%)": f"+{pct.mean():.2f}%",
            "Median Profit ($)": f"+${diff.median():,.2f}",
            "Median Gain (%)": f"+{pct.median():.2f}%",
            "Typical Range (10th-90th Pct)": f"+{pct.quantile(0.10):.1f}% to +{pct.quantile(0.90):.1f}%",
            "Win Prob (%)": f"{(diff > 0).mean()*100:.1f}%"
        })
    print("\n--- EXPECTED EARNINGS BY TIME HORIZON (Non-Bear / Bull Conditions) ---")
    print(pd.DataFrame(res).to_string(index=False))
    return df

if __name__ == "__main__":
    # 1. 2023-2024 Bull Run (Recent 1 Year: Oct 2023 to Oct 2024)
    run_near_regime("2023-10-01", "2024-10-01", "NEAR 2023-2024 Bull Rally (Recent Market)")
    
    # 2. 2020-2021 Macro Bull Run (Launch to Peak: Oct 2020 to Dec 2021)
    run_near_regime("2020-10-14", "2021-12-31", "NEAR 2020-2021 Macro Bull Market")
