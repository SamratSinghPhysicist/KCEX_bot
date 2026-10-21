#!/usr/bin/env python3
"""
ETH Long-Only Expectancy and Rolling Return Analyzer
===================================================
Analyzes empirical returns for:
- 1 day
- 1 week
- 1 month (30 days)
- 3 months (90 days)
- 6 months (180 days)
- 1 year (365 days)

Across:
1. ETH Long Fixed 0.1% TP (RSI-Momentum)
2. ETH Long Dynamic TP (EMA-Cross mode_dynamic)
3. ETH Long Fixed 0.1% TP (EMA-Cross)
"""

import os
import sys
from io import StringIO
import numpy as np
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse_trades(csv_path: str) -> pd.DataFrame:
    lines = []
    found = False
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "# DETAILED_TRADES" in line:
                found = True
                continue
            if found:
                lines.append(line)
    if not lines or len(lines) < 2:
        return pd.DataFrame()
    return pd.read_csv(StringIO("".join(lines)))


def analyze_rolling_returns(df_trades: pd.DataFrame, initial_balance: float = 1000.0, label: str = ""):
    print("\n" + "=" * 80)
    print(f"📊 ANALYSIS FOR: {label}")
    print("=" * 80)

    if df_trades.empty:
        print("No trade data found.")
        return

    # Filter to long only if both exist
    if "direction" in df_trades.columns:
        df_trades = df_trades[df_trades["direction"].str.lower() == "long"].copy()

    df_trades["entry_dt"] = pd.to_datetime(df_trades["entry_time_ms"], unit="ms")
    df_trades["exit_dt"] = pd.to_datetime(df_trades["exit_time_ms"], unit="ms")
    df_trades = df_trades.sort_values("entry_dt").reset_index(drop=True)

    t_start = df_trades["entry_dt"].min()
    t_end = df_trades["exit_dt"].max()
    total_days = (t_end - t_start).total_seconds() / 86400.0
    total_years = total_days / 365.25

    total_trades = len(df_trades)
    wins = (df_trades["net_pnl"] > 0).sum()
    losses = (df_trades["net_pnl"] < 0).sum()
    win_rate = (wins / total_trades) * 100.0 if total_trades > 0 else 0.0
    total_net_pnl = df_trades["net_pnl"].sum()
    final_balance = initial_balance + total_net_pnl
    total_gain_pct = (total_net_pnl / initial_balance) * 100.0
    cagr = ((final_balance / initial_balance) ** (1.0 / max(0.1, total_years)) - 1.0) * 100.0 if final_balance > 0 else -100.0

    print(f"Backtest Period: {t_start.strftime('%Y-%m-%d')} to {t_end.strftime('%Y-%m-%d')} ({total_days:.1f} days / {total_years:.1f} years)")
    print(f"Total Long Trades: {total_trades:,} | Wins: {wins:,} | Losses: {losses} | Win Rate: {win_rate:.2f}%")
    print(f"Initial Balance: ${initial_balance:,.2f} | Final Balance: ${final_balance:,.2f} | Net PnL: ${total_net_pnl:,.2f} ({total_gain_pct:+.2f}%)")
    print(f"Compound Annual Growth Rate (CAGR): {cagr:.2f}% / year")
    print(f"Average Profit per Trade: ${df_trades['net_pnl'].mean():.4f} ({df_trades['net_pnl'].mean() / initial_balance * 100:.3f}%)")
    dur_hours = (df_trades["exit_time_ms"] - df_trades["entry_time_ms"]) / 3600000.0
    print(f"Average Holding Duration: {dur_hours.mean():.1f} hours ({dur_hours.median():.1f} hours median)")

    # Build daily equity curve to measure rolling performance
    # Resample daily PnL
    df_trades["exit_day"] = df_trades["exit_dt"].dt.floor("D")
    daily_pnl = df_trades.groupby("exit_day")["net_pnl"].sum()

    # Create full calendar daily index
    all_days = pd.date_range(start=t_start.floor("D"), end=t_end.floor("D"), freq="D")
    daily_df = pd.DataFrame(index=all_days)
    daily_df["daily_pnl"] = daily_pnl.reindex(all_days, fill_value=0.0)
    daily_df["cum_pnl"] = daily_df["daily_pnl"].cumsum()
    daily_df["equity"] = initial_balance + daily_df["cum_pnl"]

    # Rolling window intervals
    windows = {
        "1 Day": 1,
        "1 Week (7d)": 7,
        "1 Month (30d)": 30,
        "3 Months (90d)": 90,
        "6 Months (180d)": 180,
        "1 Year (365d)": 365,
    }

    rolling_results = []
    for w_name, w_days in windows.items():
        if len(daily_df) < w_days:
            continue
        # Rolling difference in equity / cumulative pnl
        rolling_pnl = daily_df["cum_pnl"].diff(w_days).dropna()
        rolling_pct = (rolling_pnl / initial_balance) * 100.0

        p_profit = (rolling_pnl > 0).mean() * 100.0
        p_breakeven = (rolling_pnl >= 0).mean() * 100.0
        avg_ret_pct = rolling_pct.mean()
        median_ret_pct = rolling_pct.median()
        min_ret_pct = rolling_pct.min()
        max_ret_pct = rolling_pct.max()
        p25 = rolling_pct.quantile(0.25)
        p75 = rolling_pct.quantile(0.75)

        avg_dollar = rolling_pnl.mean()
        median_dollar = rolling_pnl.median()
        min_dollar = rolling_pnl.min()
        max_dollar = rolling_pnl.max()

        rolling_results.append({
            "Window": w_name,
            "Days": w_days,
            "Expected ($)": avg_dollar,
            "Expected (%)": avg_ret_pct,
            "Median ($)": median_dollar,
            "Median (%)": median_ret_pct,
            "Range ($) [Min to Max]": f"${min_dollar:+.2f} to ${max_dollar:+.2f}",
            "Range (%) [Min to Max]": f"{min_ret_pct:+.2f}% to {max_ret_pct:+.2f}%",
            "Middle 50% [P25-P75]": f"{p25:+.2f}% to {p75:+.2f}%",
            "Win Prob (%)": p_profit,
            "Loss Prob (%)": 100.0 - p_breakeven,
        })

    res_df = pd.DataFrame(rolling_results)
    print("\n--- EXPECTED PROFIT BY TIME HORIZON ($1,000 Starting Capital, 1x Leverage) ---")
    cols_to_print = ["Window", "Expected ($)", "Expected (%)", "Median ($)", "Median (%)", "Range (%) [Min to Max]", "Win Prob (%)"]
    print(res_df[cols_to_print].to_string(index=False))

    return res_df


if __name__ == "__main__":
    # 1. RSI-Momentum Long Only Fixed 0.1%
    f_rsi_fixed = os.path.join(ROOT_DIR, "results_ETH_1h_long_fixed_0.1_rsi_momentum.csv")
    if os.path.isfile(f_rsi_fixed):
        df_rsi = parse_trades(f_rsi_fixed)
        analyze_rolling_returns(df_rsi, initial_balance=1000.0, label="ETH Long-Only: RSI-Momentum (Fixed 0.1% TP)")

    # 2. EMA-Cross Long Only Dynamic Mode TP
    f_ema_dynamic = os.path.join(ROOT_DIR, "results_ETH_1h_long_mode_dynamic_ema_cross.csv")
    if os.path.isfile(f_ema_dynamic):
        df_dynamic = parse_trades(f_ema_dynamic)
        analyze_rolling_returns(df_dynamic, initial_balance=1000.0, label="ETH Long-Only: EMA-Cross (Mode Dynamic TP ~3.8%)")

    # 3. EMA-Cross Long Only Fixed 0.1% TP (from both results file)
    f_ema_both = os.path.join(ROOT_DIR, "results_ETH_1h_both_fixed_0.1_ema_cross.csv")
    if os.path.isfile(f_ema_both):
        df_ema_both = parse_trades(f_ema_both)
        analyze_rolling_returns(df_ema_both, initial_balance=1000.0, label="ETH Long-Only: EMA-Cross (Fixed 0.1% TP)")
