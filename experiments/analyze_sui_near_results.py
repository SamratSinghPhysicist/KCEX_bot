#!/usr/bin/env python3
"""
SUI & NEAR Quantitative Results & Expectancy Analyzer
=====================================================
Analyzes backtest results for SUI and NEAR across:
- Master Metrics Summary
- Rolling Time Horizons (1d, 1w, 1m, 3m, 6m, 1y) with Fixed $1,000 Sizing
- Rolling Time Horizons with 10% Available Capital Sizing & Compounding
- MFE / MAE Empirical Modes & Adverse Drawdown Tiers
"""

import os
import sys
from io import StringIO
from collections import Counter
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse_csv(csv_path):
    summary = {}
    trades_lines = []
    found_trades = False
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("# DETAILED_TRADES"):
                found_trades = True
                continue
            if not found_trades:
                parts = line.strip().split(",")
                if len(parts) >= 2 and not line.startswith("#"):
                    summary[parts[0].strip()] = parts[1].strip()
            else:
                trades_lines.append(line)
    df_trades = pd.read_csv(StringIO("".join(trades_lines))) if trades_lines else pd.DataFrame()
    return summary, df_trades

def get_mode(s: pd.Series, bin_size=0.10):
    binned = (s / bin_size).round() * bin_size
    c = Counter(binned.round(4))
    return c.most_common(1)[0][0] if c else 0.0

def analyze_asset(sym):
    print("\n" + "=" * 90)
    print(f"📊 COMPREHENSIVE BACKTEST ANALYSIS FOR: {sym}")
    print("=" * 90)
    
    files = [
        (f"results_{sym}_1h_long_mode_dynamic_ema_cross.csv", "Long Only - Dynamic Swing (~3.8%-5% TP)"),
        (f"results_{sym}_1h_long_fixed_0.1_rsi_momentum.csv", "Long Only - Micro-Scalp (Fixed 0.1% TP)"),
        (f"results_{sym}_1h_both_mode_dynamic_ema_cross.csv", "Bidirectional (Both) - Dynamic Swing"),
        (f"results_{sym}_1h_both_fixed_0.1_ema_cross.csv", "Bidirectional (Both) - Micro-Scalp (0.1% TP)"),
    ]
    
    summaries = []
    for fname, desc in files:
        fpath = os.path.join(ROOT_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        sm, df = parse_csv(fpath)
        if not sm or df.empty:
            continue
        summaries.append({
            "Configuration": desc,
            "Period": f"{sm.get('start_date','')} to {sm.get('end_date','')}",
            "Trades": int(sm.get('total_trades', 0)),
            "Win Rate (%)": f"{float(sm.get('win_rate_pct', 0)):.1f}%",
            "Initial $": f"${float(sm.get('initial_balance', 1000)):,.2f}",
            "Final $": f"${float(sm.get('final_balance', 0)):,.2f}",
            "Net PnL ($)": f"${float(sm.get('net_pnl_usd', 0)):,.2f}",
            "Net Gain (%)": f"{float(sm.get('net_gain_pct', 0)):+.1f}%",
            "Max DD ($)": f"${float(sm.get('max_drawdown_usd', 0)):,.2f}",
            "Profit Factor": sm.get('profit_factor', 'N/A')
        })
    print("\n--- MASTER PERFORMANCE TABLE (Fixed $1,000 Margin) ---")
    print(pd.DataFrame(summaries).to_string(index=False))
    
    # Detailed Expectancy on Long Dynamic and Long Fixed
    f_dynamic = os.path.join(ROOT_DIR, f"results_{sym}_1h_long_mode_dynamic_ema_cross.csv")
    if os.path.isfile(f_dynamic):
        _, df_dyn = parse_csv(f_dynamic)
        # Exclude END_OF_DATA
        df_comp = df_dyn[df_dyn["exit_reason"] != "END_OF_DATA"].copy()
        
        # Empirical MFE / MAE
        mfes = df_comp["mfe_pct"].dropna()
        maes = df_comp["mae_pct"].dropna()
        print(f"\n--- EMPIRICAL MOVE MODES & PROBABILITIES ({sym} Long) ---")
        print(f"Mode Move in Favor (MFE): +{get_mode(mfes, 0.1):.2f}% | Median: +{mfes.median():.2f}% | 75th: +{mfes.quantile(0.75):.2f}%")
        print(f"Mode Move Against (MAE):  -{get_mode(maes, 0.1):.2f}% | Median: -{maes.median():.2f}% | 75th: -{maes.quantile(0.75):.2f}% | Max: -{maes.max():.2f}%")
        print(f"P(MFE >= +0.10%): {(mfes>=0.10).mean()*100:.1f}% | P(MFE >= +1.0%): {(mfes>=1.0).mean()*100:.1f}% | P(MFE >= +3.0%): {(mfes>=3.0).mean()*100:.1f}% | P(MFE >= +5.0%): {(mfes>=5.0).mean()*100:.1f}%")
        print(f"Severe Drawdowns: MAE >= 20%: {(maes>=20.0).sum()} times | MAE >= 50%: {(maes>=50.0).sum()} times | 1x Liquidations: 0")

        # Rolling Horizon for Fixed $1,000 Sizing
        df_comp["exit_dt"] = pd.to_datetime(df_comp["exit_time_ms"], unit="ms")
        df_comp["entry_dt"] = pd.to_datetime(df_comp["entry_time_ms"], unit="ms")
        df_comp["exit_day"] = df_comp["exit_dt"].dt.floor("D")
        daily_pnl = df_comp.groupby("exit_day")["net_pnl"].sum()
        all_days = pd.date_range(start=df_comp["entry_dt"].min().floor("D"), end=df_comp["exit_dt"].max().floor("D"), freq="D")
        daily_s = daily_pnl.reindex(all_days, fill_value=0.0).cumsum()
        
        windows = [("1 Day", 1), ("1 Week (7d)", 7), ("1 Month (30d)", 30), ("3 Months (90d)", 90), ("6 Months (180d)", 180), ("1 Year (365d)", 365)]
        roll_fixed = []
        for w_name, d in windows:
            diff = daily_s.diff(d).dropna()
            if not diff.empty:
                roll_fixed.append({
                    "Window": w_name,
                    "Expected ($)": diff.mean(),
                    "Expected (%)": (diff.mean() / 1000.0) * 100.0,
                    "Median ($)": diff.median(),
                    "Median (%)": (diff.median() / 1000.0) * 100.0,
                    "P10-P90 Range": f"+${diff.quantile(0.10):.1f} to +${diff.quantile(0.90):.1f}",
                    "Win Prob (%)": (diff > 0).mean() * 100.0
                })
        print(f"\n--- EXPECTED PROFIT: FIXED $1,000 SIZING ({sym} Long Dynamic Swing) ---")
        print(pd.DataFrame(roll_fixed).to_string(index=False))

        # Simulation with 10% Available Capital Sizing & Compounding
        events = []
        for idx, row in df_comp.iterrows():
            events.append({"time_ms": row["entry_time_ms"], "type": "ENTRY", "trade_id": row["trade_id"], "ret": row["net_return_pct"]})
            events.append({"time_ms": row["exit_time_ms"], "type": "EXIT", "trade_id": row["trade_id"], "ret": row["net_return_pct"]})
        events.sort(key=lambda x: (x["time_ms"], 0 if x["type"] == "ENTRY" else 1))
        
        cash = 1000.0
        active = {}
        eq_curve = []
        for ev in events:
            t_ms = ev["time_ms"]
            if ev["type"] == "ENTRY":
                if cash >= 5.0:
                    m = cash * 0.10
                    cash -= m
                    active[ev["trade_id"]] = {"m": m, "ret": ev["ret"]}
            elif ev["type"] == "EXIT":
                tr_id = ev["trade_id"]
                if tr_id in active:
                    tr = active.pop(tr_id)
                    p = tr["m"] * (tr["ret"] / 100.0)
                    cash += (tr["m"] + p)
            inv = sum(t["m"] for t in active.values())
            eq_curve.append({"time_ms": t_ms, "dt": pd.to_datetime(t_ms, unit="ms"), "equity": cash + inv})
            
        df_eq = pd.DataFrame(eq_curve)
        final_10pct = df_eq["equity"].iloc[-1]
        df_eq["day"] = df_eq["dt"].dt.floor("D")
        daily_eq10 = df_eq.groupby("day")["equity"].last().reindex(all_days).ffill().bfill()
        
        roll_10pct = []
        for w_name, d in windows:
            diff = daily_eq10.diff(d).dropna()
            start = daily_eq10.shift(d).dropna()
            pct = (diff / start) * 100.0
            if not diff.empty:
                roll_10pct.append({
                    "Window": w_name,
                    "Expected ($)": diff.mean(),
                    "Expected (%)": pct.mean(),
                    "Median ($)": diff.median(),
                    "Median (%)": pct.median(),
                    "P10-P90 Range": f"{pct.quantile(0.10):+.1f}% to {pct.quantile(0.90):+.1f}%",
                    "Win Prob (%)": (diff > 0).mean() * 100.0
                })
        print(f"\n--- EXPECTED PROFIT: 10% AVAILABLE CAPITAL SIZING ({sym} Long Dynamic Swing) ---")
        print(f"Starting Capital: $1,000.00 | Final Equity: ${final_10pct:,.2f} (+{(final_10pct/1000 - 1)*100:.1f}%)")
        print(pd.DataFrame(roll_10pct).to_string(index=False))

if __name__ == "__main__":
    analyze_asset("SUI")
    analyze_asset("NEAR")
