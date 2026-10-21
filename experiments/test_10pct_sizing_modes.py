#!/usr/bin/env python3
"""
Comprehensive Sizing Comparison:
1. Mode A: 10% of Available Cash (Multi-position fractional sizing, no cap)
2. Mode B: 10% of Total Equity (Single position at a time, compounded)
3. Mode C: 100% Capital vs 10% Capital Head-to-Head
"""

import os
import sys
from io import StringIO
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse_trades(csv_name):
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
    return df[df["exit_reason"] != "END_OF_DATA"].copy()

def test_unconstrained_10pct_cash(df, initial_capital=1000.0, label=""):
    df["entry_dt"] = pd.to_datetime(df["entry_time_ms"], unit="ms")
    df["exit_dt"] = pd.to_datetime(df["exit_time_ms"], unit="ms")
    
    events = []
    for idx, row in df.iterrows():
        events.append({"time_ms": row["entry_time_ms"], "type": "ENTRY", "trade_id": row["trade_id"], "ret": row["net_return_pct"]})
        events.append({"time_ms": row["exit_time_ms"], "type": "EXIT", "trade_id": row["trade_id"], "ret": row["net_return_pct"]})
    events.sort(key=lambda x: (x["time_ms"], 0 if x["type"] == "ENTRY" else 1))
    
    cash = initial_capital
    active = {}
    completed = []
    equity_curve = []
    
    for ev in events:
        t_ms = ev["time_ms"]
        if ev["type"] == "ENTRY":
            if cash >= 5.0: # min margin $5
                margin = cash * 0.10
                cash -= margin
                active[ev["trade_id"]] = {"margin": margin, "ret": ev["ret"], "entry_time": t_ms}
        elif ev["type"] == "EXIT":
            tr_id = ev["trade_id"]
            if tr_id in active:
                tr = active.pop(tr_id)
                m = tr["margin"]
                profit = m * (tr["ret"] / 100.0)
                cash += (m + profit)
                completed.append({"trade_id": tr_id, "pnl": profit, "exit_ms": t_ms, "cash": cash})
        
        invested = sum(t["margin"] for t in active.values())
        equity = cash + invested
        equity_curve.append({"time_ms": t_ms, "equity": equity, "cash": cash, "invested": invested, "open": len(active)})
        
    df_eq = pd.DataFrame(equity_curve)
    df_eq["dt"] = pd.to_datetime(df_eq["time_ms"], unit="ms")
    final_eq = df_eq["equity"].iloc[-1]
    
    # Calculate rolling expectancies
    df_eq["day"] = df_eq["dt"].dt.floor("D")
    daily_eq = df_eq.groupby("day")["equity"].last()
    all_days = pd.date_range(start=df["entry_dt"].min().floor("D"), end=df["exit_dt"].max().floor("D"), freq="D")
    daily_s = daily_eq.reindex(all_days).ffill().bfill()
    
    windows = [("1 Day", 1), ("1 Week", 7), ("1 Month", 30), ("3 Months", 90), ("6 Months", 180), ("1 Year", 365)]
    res = []
    for w_name, d in windows:
        diff = daily_s.diff(d).dropna()
        start = daily_s.shift(d).dropna()
        pct = (diff / start) * 100.0
        res.append({
            "Window": w_name,
            "Expected ($)": diff.mean(),
            "Expected (%)": pct.mean(),
            "Median ($)": diff.median(),
            "Median (%)": pct.median(),
            "P10-P90 (%)": f"{pct.quantile(0.10):.1f}% to {pct.quantile(0.90):.1f}%",
            "Win Prob (%)": (diff > 0).mean() * 100.0
        })
    print(f"\n--- {label} ---")
    print(f"Initial: ${initial_capital:,.2f} | Final Equity: ${final_eq:,.2f} (+{(final_eq/initial_capital - 1)*100:.1f}%) | Trades Taken: {len(completed):,}/{len(df):,}")
    print(pd.DataFrame(res).to_string(index=False))

def test_single_position_10pct_equity(df, initial_capital=1000.0, label=""):
    df = df.sort_values("entry_time_ms").reset_index(drop=True)
    equity = initial_capital
    completed = []
    last_exit_ms = 0
    
    for idx, row in df.iterrows():
        # Only enter if previous trade finished
        if row["entry_time_ms"] >= last_exit_ms:
            margin = equity * 0.10
            profit = margin * (row["net_return_pct"] / 100.0)
            equity += profit
            last_exit_ms = row["exit_time_ms"]
            completed.append({"exit_ms": row["exit_time_ms"], "pnl": profit, "equity": equity})
            
    print(f"\n--- {label} (Single-Position at a Time) ---")
    print(f"Initial: ${initial_capital:,.2f} | Final Equity: ${equity:,.2f} (+{(equity/initial_capital - 1)*100:.1f}%) | Trades Executed: {len(completed):,}")

if __name__ == "__main__":
    df_swing = parse_trades("results_ETH_1h_long_mode_dynamic_ema_cross.csv")
    test_unconstrained_10pct_cash(df_swing, label="ETH Long Dynamic Swing: 10% Available Cash (Fractional Multi-Position)")
    test_single_position_10pct_equity(df_swing, label="ETH Long Dynamic Swing: 10% Equity")

    df_micro = parse_trades("results_ETH_1h_long_fixed_0.1_rsi_momentum.csv")
    test_unconstrained_10pct_cash(df_micro, label="ETH Long Micro-Scalp (0.1% TP): 10% Available Cash")
