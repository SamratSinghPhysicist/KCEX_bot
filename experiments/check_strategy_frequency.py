#!/usr/bin/env python3
import os, sys
from io import StringIO
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse(path):
    lines = []
    found = False
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for l in f:
            if "# DETAILED_TRADES" in l:
                found = True
                continue
            if found:
                lines.append(l)
    return pd.read_csv(StringIO("".join(lines))) if lines else pd.DataFrame()

strategies = ["ema_cross", "rsi_momentum", "ob_demand"]
for strat in strategies:
    fpath = os.path.join(ROOT_DIR, f"results_BTC_1h_both_fixed_0.1_{strat}.csv")
    if not os.path.isfile(fpath):
        # try long
        fpath = os.path.join(ROOT_DIR, f"results_BTC_1h_long_fixed_0.1_{strat}.csv")
    if not os.path.isfile(fpath):
        fpath = os.path.join(ROOT_DIR, f"results_BTC_1h_both_strategy_{strat}.csv")
    
    if os.path.isfile(fpath):
        df = parse(fpath)
        if not df.empty:
            t_start = pd.to_datetime(df["entry_time_ms"].min(), unit="ms")
            t_end = pd.to_datetime(df["exit_time_ms"].max(), unit="ms")
            days = (t_end - t_start).total_seconds() / 86400.0
            print(f"Strategy: {strat:<15} | File: {os.path.basename(fpath):<45} | Trades: {len(df):>5} | Per Month: {len(df)/days*30.417:>5.1f} | Win Rate: {df['is_win'].mean()*100:.1f}%")
