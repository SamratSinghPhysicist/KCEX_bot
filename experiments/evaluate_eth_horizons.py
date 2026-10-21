#!/usr/bin/env python3
"""
ETH Long-Only Expectation Breakdown Script
=========================================
Generates side-by-side comparison of expected dollar profits, percentages,
and probabilities for:
- 1 Day
- 1 Week (7 Days)
- 1 Month (30 Days)
- 3 Months (90 Days)
- 6 Months (180 Days)
- 1 Year (365 Days)
Starting Capital: $1,000 (1x leverage, 100% cash, no stop-loss)
"""

import os
import sys
from io import StringIO
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse_detailed(csv_name):
    path = os.path.join(ROOT_DIR, csv_name)
    lines = []
    found = False
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for l in f:
            if "# DETAILED_TRADES" in l:
                found = True
                continue
            if found:
                lines.append(l)
    df = pd.read_csv(StringIO("".join(lines)))
    # Exclude END_OF_DATA artifact for clean operational expectancy, or analyze both
    return df

df_micro = parse_detailed("results_ETH_1h_long_fixed_0.1_rsi_momentum.csv")
df_swing = parse_detailed("results_ETH_1h_long_mode_dynamic_ema_cross.csv")

def evaluate_windows(df, capital=1000.0, label=""):
    # Filter completed trades
    df_comp = df[df["exit_reason"] != "END_OF_DATA"].copy()
    df_comp["exit_dt"] = pd.to_datetime(df_comp["exit_time_ms"], unit="ms")
    df_comp["entry_dt"] = pd.to_datetime(df_comp["entry_time_ms"], unit="ms")
    df_comp = df_comp.sort_values("exit_dt").reset_index(drop=True)
    
    t_start = df_comp["entry_dt"].min()
    t_end = df_comp["exit_dt"].max()
    
    # Daily aggregation
    df_comp["exit_day"] = df_comp["exit_dt"].dt.floor("D")
    daily_pnl = df_comp.groupby("exit_day")["net_pnl"].sum()
    
    all_days = pd.date_range(start=t_start.floor("D"), end=t_end.floor("D"), freq="D")
    daily_df = pd.DataFrame(index=all_days)
    daily_df["pnl"] = daily_pnl.reindex(all_days, fill_value=0.0)
    daily_df["cum_pnl"] = daily_df["pnl"].cumsum()
    
    windows = [
        ("1 Day", 1),
        ("1 Week (7 Days)", 7),
        ("1 Month (30 Days)", 30),
        ("3 Months (90 Days)", 90),
        ("6 Months (180 Days)", 180),
        ("1 Year (365 Days)", 365),
    ]
    
    records = []
    for w_name, w_days in windows:
        roll = daily_df["cum_pnl"].diff(w_days).dropna()
        avg_usd = roll.mean()
        med_usd = roll.median()
        p10_usd = roll.quantile(0.10)
        p90_usd = roll.quantile(0.90)
        min_usd = roll.min()
        max_usd = roll.max()
        p_pos = (roll > 0).mean() * 100.0
        
        records.append({
            "Time Horizon": w_name,
            "Expected ($)": f"+${avg_usd:.2f}",
            "Expected (%)": f"+{(avg_usd/capital)*100:.2f}%",
            "Median ($)": f"+${med_usd:.2f}",
            "Median (%)": f"+{(med_usd/capital)*100:.2f}%",
            "Typical Range (10th-90th Pct)": f"+${p10_usd:.2f} to +${p90_usd:.2f} (+{(p10_usd/capital)*100:.1f}% to +{(p90_usd/capital)*100:.1f}%)",
            "All-Time Range (Min to Max)": f"+${min_usd:.2f} to +${max_usd:.2f}",
            "Probability of Profit": f"{p_pos:.1f}%"
        })
    print(f"\n========================================================")
    print(f"RESULTS: {label}")
    print(f"Total Completed Trades: {len(df_comp):,} | Total PnL: +${df_comp['net_pnl'].sum():,.2f}")
    print(f"========================================================")
    res_df = pd.DataFrame(records)
    print(res_df.to_string(index=False))

evaluate_windows(df_micro, 1000.0, "OPTION A: ETH Long Micro-Scalp (Fixed 0.1% TP)")
evaluate_windows(df_swing, 1000.0, "OPTION B: ETH Long Dynamic Swing (Mode TP ~3.8%-5.0%)")
