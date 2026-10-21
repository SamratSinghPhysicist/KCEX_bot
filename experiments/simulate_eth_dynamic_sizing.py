#!/usr/bin/env python3
"""
ETH Long-Only 10% Capital Sizing Simulator
=========================================
Evaluates portfolio performance when each trade uses exactly 10% of available cash capital.
Simulates:
1. Sequential / Cash-managed multi-position execution.
2. Compounding equity growth.
3. Portfolio-level peak-to-trough drawdown.
4. Time-horizon rolling expectancies (1d, 1w, 1m, 3m, 6m, 1y).
"""

import os
import sys
from io import StringIO
import numpy as np
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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
    return df

def simulate_10pct_sizing(csv_file, initial_capital=1000.0, max_positions=10, label=""):
    df = parse_trades(csv_file)
    if df.empty:
        print(f"No data for {csv_file}")
        return
    
    # Filter completed trades (or include all)
    df = df[df["exit_reason"] != "END_OF_DATA"].copy()
    df["entry_dt"] = pd.to_datetime(df["entry_time_ms"], unit="ms")
    df["exit_dt"] = pd.to_datetime(df["exit_time_ms"], unit="ms")
    df = df.sort_values("entry_time_ms").reset_index(drop=True)
    
    # We will simulate chronological order:
    # Events: entries and exits
    events = []
    for idx, row in df.iterrows():
        events.append({
            "time_ms": row["entry_time_ms"],
            "type": "ENTRY",
            "trade_id": row["trade_id"],
            "net_return_pct": row["net_return_pct"],
            "mae_pct": row["mae_pct"],
            "row": row
        })
        events.append({
            "time_ms": row["exit_time_ms"],
            "type": "EXIT",
            "trade_id": row["trade_id"],
            "net_return_pct": row["net_return_pct"],
            "mae_pct": row["mae_pct"],
            "row": row
        })
    
    # Sort events by time: at identical timestamps, ENTRY must precede EXIT
    events.sort(key=lambda x: (x["time_ms"], 0 if x["type"] == "ENTRY" else 1))
    
    # State
    cash = initial_capital
    active_trades = {} # trade_id -> dict(margin, net_return_pct, mae_pct, entry_time)
    
    history = [] # list of (time_ms, cash, invested_margin, equity)
    completed_records = []
    
    for ev in events:
        t_ms = ev["time_ms"]
        if ev["type"] == "ENTRY":
            # Check if we can enter: 10% of available cash
            # Minimum margin threshold $1.00
            if cash >= 10.0 and len(active_trades) < max_positions:
                margin_allocated = cash * 0.10
                cash -= margin_allocated
                active_trades[ev["trade_id"]] = {
                    "margin": margin_allocated,
                    "net_return_pct": ev["net_return_pct"],
                    "mae_pct": ev["mae_pct"],
                    "entry_time_ms": t_ms
                }
        elif ev["type"] == "EXIT":
            tr_id = ev["trade_id"]
            if tr_id in active_trades:
                tr = active_trades.pop(tr_id)
                margin = tr["margin"]
                ret_pct = tr["net_return_pct"]
                profit = margin * (ret_pct / 100.0)
                cash += (margin + profit)
                completed_records.append({
                    "trade_id": tr_id,
                    "entry_time_ms": tr["entry_time_ms"],
                    "exit_time_ms": t_ms,
                    "margin": margin,
                    "net_pnl": profit,
                    "return_pct": ret_pct,
                    "cash_after": cash
                })
        
        # Calculate current equity
        invested = sum(t["margin"] for t in active_trades.values())
        equity = cash + invested
        history.append({
            "time_ms": t_ms,
            "dt": pd.to_datetime(t_ms, unit="ms"),
            "cash": cash,
            "invested": invested,
            "equity": equity,
            "open_positions": len(active_trades)
        })
        
    df_hist = pd.DataFrame(history)
    df_res = pd.DataFrame(completed_records)
    
    final_equity = cash + sum(t["margin"] for t in active_trades.values())
    total_gain = final_equity - initial_capital
    total_gain_pct = (total_gain / initial_capital) * 100.0
    
    # Compute max drawdown on total equity
    df_hist["peak_equity"] = df_hist["equity"].cummax()
    df_hist["drawdown_usd"] = df_hist["peak_equity"] - df_hist["equity"]
    df_hist["drawdown_pct"] = (df_hist["drawdown_usd"] / df_hist["peak_equity"]) * 100.0
    max_dd_pct = df_hist["drawdown_pct"].max()
    max_dd_usd = df_hist["drawdown_usd"].max()
    
    t_start = df["entry_dt"].min()
    t_end = df["exit_dt"].max()
    total_days = (t_end - t_start).total_seconds() / 86400.0
    total_years = total_days / 365.25
    cagr = ((final_equity / initial_capital) ** (1.0 / max(0.1, total_years)) - 1.0) * 100.0
    
    print("\n" + "=" * 80)
    print(f"🚀 10% POSITION SIZING SIMULATION: {label}")
    print("=" * 80)
    print(f"Period: {t_start.strftime('%Y-%m-%d')} to {t_end.strftime('%Y-%m-%d')} ({total_days:.1f} days / {total_years:.1f} years)")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Equity:    ${final_equity:,.2f} (Net Profit: +${total_gain:,.2f} / +{total_gain_pct:,.2f}%)")
    print(f"CAGR (Annualized): {cagr:.2f}% per year")
    print(f"Max Portfolio Drawdown: -{max_dd_pct:.2f}% (-${max_dd_usd:,.2f})")
    print(f"Executed Trades: {len(df_res):,} out of {len(df):,} available signals")
    print(f"Average Concurrent Open Positions: {df_hist['open_positions'].mean():.1f} (Max: {df_hist['open_positions'].max()})")
    print(f"Average Deployed Margin: ${df_hist['invested'].mean():,.2f} ({(df_hist['invested'].mean()/df_hist['equity'].mean())*100:.1f}% of equity)")
    print(f"Average Cash Reserve:    ${df_hist['cash'].mean():,.2f} ({(df_hist['cash'].mean()/df_hist['equity'].mean())*100:.1f}% of equity)")

    # Rolling window expectancies
    df_hist["day"] = df_hist["dt"].dt.floor("D")
    daily_equity = df_hist.groupby("day")["equity"].last()
    all_days = pd.date_range(start=t_start.floor("D"), end=t_end.floor("D"), freq="D")
    daily_eq_df = daily_equity.reindex(all_days).ffill().bfill()
    
    windows = [
        ("1 Day", 1),
        ("1 Week (7d)", 7),
        ("1 Month (30d)", 30),
        ("3 Months (90d)", 90),
        ("6 Months (180d)", 180),
        ("1 Year (365d)", 365),
    ]
    
    roll_records = []
    for w_name, w_days in windows:
        roll_pnl = daily_eq_df.diff(w_days).dropna()
        # percentage relative to starting equity of that window
        start_eq = daily_eq_df.shift(w_days).dropna()
        roll_pct = (roll_pnl / start_eq) * 100.0
        
        avg_usd = roll_pnl.mean()
        med_usd = roll_pnl.median()
        avg_pct = roll_pct.mean()
        med_pct = roll_pct.median()
        p10_pct = roll_pct.quantile(0.10)
        p90_pct = roll_pct.quantile(0.90)
        min_pct = roll_pct.min()
        max_pct = roll_pct.max()
        p_profit = (roll_pnl > 0).mean() * 100.0
        
        roll_records.append({
            "Window": w_name,
            "Expected ($)": f"+${avg_usd:,.2f}" if avg_usd >= 0 else f"-${abs(avg_usd):,.2f}",
            "Expected (%)": f"{avg_pct:+.2f}%",
            "Median ($)": f"+${med_usd:,.2f}" if med_usd >= 0 else f"-${abs(med_usd):,.2f}",
            "Median (%)": f"{med_pct:+.2f}%",
            "Typical Range [P10-P90]": f"{p10_pct:+.2f}% to {p90_pct:+.2f}%",
            "All-Time Range [Min to Max]": f"{min_pct:+.2f}% to {max_pct:+.2f}%",
            "Win Prob (%)": f"{p_profit:.1f}%"
        })
        
    print("\n--- ROLLING TIME-HORIZON EXPECTANCIES WITH 10% CAPITAL SIZING & COMPOUNDING ---")
    df_roll = pd.DataFrame(roll_records)
    cols = ["Window", "Expected ($)", "Expected (%)", "Median ($)", "Median (%)", "Typical Range [P10-P90]", "Win Prob (%)"]
    print(df_roll[cols].to_string(index=False))
    return df_roll, df_hist

if __name__ == "__main__":
    # Test Dynamic Swing (EMA Cross mode dynamic)
    simulate_10pct_sizing("results_ETH_1h_long_mode_dynamic_ema_cross.csv", initial_capital=1000.0, max_positions=10, label="Dynamic Swing (~3.8%-5.0% TP)")
    
    # Test Micro-Scalp (Fixed 0.1% TP)
    simulate_10pct_sizing("results_ETH_1h_long_fixed_0.1_rsi_momentum.csv", initial_capital=1000.0, max_positions=10, label="Micro-Scalp (Fixed 0.1% TP)")
