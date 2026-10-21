#!/usr/bin/env python3
"""
Deep-Dive Statistical Analysis Engine
=====================================
Calculates:
1. Empirical Trade Frequency (Daily, Weekly, Monthly, and Bar Interval) across assets & timeframes.
2. Probability & Recurrence Intervals of Severe Drawdowns & Near-Liquidation Events (MAE >= 10%, 20%, 50%, 80%, 100%).
3. Most Probable Moves in Favor (MFE Mode) and Against (MAE Mode) with percentiles.
4. Timeframe Scaling Analysis (1m, 5m, 15m, 1h, 4h, 1d) with volatility, noise, and trade density.
"""

import os
import sys
import glob
from io import StringIO
from collections import Counter
import numpy as np
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def parse_trades_from_csv(csv_path: str) -> pd.DataFrame:
    """Extracts detailed trades section from results CSV."""
    lines = []
    found_trades = False
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "# DETAILED_TRADES" in line:
                found_trades = True
                continue
            if found_trades:
                lines.append(line)
    if not lines or len(lines) < 2:
        return pd.DataFrame()
    return pd.read_csv(StringIO("".join(lines)))


def get_mode(series: pd.Series, bin_size: float = 0.05) -> float:
    """Computes empirical mode of continuous series using uniform binning."""
    binned = (series / bin_size).round() * bin_size
    counts = Counter(binned.round(4))
    if not counts:
        return 0.0
    return counts.most_common(1)[0][0]


def run_full_deep_dive():
    print("=" * 80)
    print("🔬 CALCULATING QUANTITATIVE TRADE FREQUENCY & DRAWDOWN DISTRIBUTIONS")
    print("=" * 80)

    # 1. Analyze 1h Results across assets
    target_files = [
        ("BTC", "results_BTC_1h_both_fixed_0.1_ema_cross.csv"),
        ("ETH", "results_ETH_1h_both_fixed_0.1_ema_cross.csv"),
        ("SOL", "results_SOL_1h_both_fixed_0.1_ema_cross.csv"),
        ("GOLD", "results_GOLD_1h_both_fixed_0.1_ema_cross.csv"),
        ("AAPL", "results_AAPL_1h_both_fixed_0.1_ema_cross.csv"),
        ("MSFT", "results_MSFT_1h_both_fixed_0.1_ema_cross.csv"),
        ("NVDA", "results_NVDA_1h_both_fixed_0.1_ema_cross.csv"),
        ("TSLA", "results_TSLA_1h_both_fixed_0.1_ema_cross.csv"),
        ("AMZN", "results_AMZN_1h_both_fixed_0.1_ema_cross.csv"),
        ("JPM", "results_JPM_1h_both_fixed_0.1_ema_cross.csv"),
    ]

    freq_summary = []
    drawdown_summary = []
    prob_summary = []

    for sym, fname in target_files:
        fpath = os.path.join(ROOT_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        df = parse_trades_from_csv(fpath)
        if df.empty or len(df) < 10:
            continue

        n_trades = len(df)
        t_start = pd.to_datetime(df["entry_time_ms"].min(), unit="ms")
        t_end = pd.to_datetime(df["exit_time_ms"].max(), unit="ms")
        days = max(1.0, (t_end - t_start).total_seconds() / 86400.0)

        t_per_day = n_trades / days
        t_per_week = t_per_day * 7.0
        t_per_month = t_per_day * 30.417
        hours_per_trade = (days * 24.0) / n_trades

        # MAE and MFE
        mfes = df["mfe_pct"].dropna()
        maes = df["mae_pct"].dropna()

        mode_mfe = get_mode(mfes, bin_size=0.05)
        mode_mae = get_mode(maes, bin_size=0.10)

        freq_summary.append({
            "asset": sym,
            "span_days": days,
            "trades": n_trades,
            "per_day": t_per_day,
            "per_week": t_per_week,
            "per_month": t_per_month,
            "hours_between": hours_per_trade,
            "mode_mfe": mode_mfe,
            "median_mfe": mfes.median(),
            "p75_mfe": mfes.quantile(0.75),
            "p90_mfe": mfes.quantile(0.90),
            "mode_mae": mode_mae,
            "median_mae": maes.median(),
            "p75_mae": maes.quantile(0.75),
            "p90_mae": maes.quantile(0.90),
        })

        # Probability thresholds
        p_mfe_01 = (mfes >= 0.10).mean() * 100
        p_mfe_02 = (mfes >= 0.20).mean() * 100
        p_mfe_05 = (mfes >= 0.50).mean() * 100
        p_mfe_10 = (mfes >= 1.00).mean() * 100
        p_mfe_20 = (mfes >= 2.00).mean() * 100
        p_mfe_50 = (mfes >= 5.00).mean() * 100

        prob_summary.append({
            "asset": sym,
            "p_01": p_mfe_01,
            "p_02": p_mfe_02,
            "p_05": p_mfe_05,
            "p_10": p_mfe_10,
            "p_20": p_mfe_20,
            "p_50": p_mfe_50,
        })

        # Adverse Drawdown Buckets
        n_severe = (maes >= 20.0).sum()
        n_near_liq = (maes >= 80.0).sum()
        days_per_severe = days / n_severe if n_severe > 0 else 9999.0
        days_per_near_liq = days / n_near_liq if n_near_liq > 0 else 9999.0

        drawdown_summary.append({
            "asset": sym,
            "minor_under_1": (maes < 1.0).mean() * 100,
            "pullback_1_5": ((maes >= 1.0) & (maes < 5.0)).mean() * 100,
            "correction_5_10": ((maes >= 5.0) & (maes < 10.0)).mean() * 100,
            "serious_10_20": ((maes >= 10.0) & (maes < 20.0)).mean() * 100,
            "severe_20_50": ((maes >= 20.0) & (maes < 50.0)).mean() * 100,
            "massive_50_80": ((maes >= 50.0) & (maes < 80.0)).mean() * 100,
            "near_liq_80_plus": (maes >= 80.0).mean() * 100,
            "count_severe": n_severe,
            "freq_severe_months": (days_per_severe / 30.417) if n_severe > 0 else 999.0,
            "count_near_liq": n_near_liq,
            "freq_near_liq_months": (days_per_near_liq / 30.417) if n_near_liq > 0 else 999.0,
        })

    print("\n--- 1. TRADE FREQUENCY & EXCURSION MODES ---")
    df_freq = pd.DataFrame(freq_summary)
    print(df_freq.to_string(index=False))

    print("\n--- 2. ADVERSE DRAWDOWN CLUSTERS (% OF TRADES) ---")
    df_dd = pd.DataFrame(drawdown_summary)
    print(df_dd.to_string(index=False))

    print("\n--- 3. FAVORABLE MOVE PROBABILITIES (% REACHING TARGET) ---")
    df_prob = pd.DataFrame(prob_summary)
    print(df_prob.to_string(index=False))

    # 4. Long vs Short Liquidation / Severe Move Analysis on BTC & ETH
    print("\n--- 4. LONG VS SHORT SEVERE MOVE COMPARISON ---")
    for sym in ["BTC", "ETH"]:
        f_long = os.path.join(ROOT_DIR, f"results_{sym}_1h_long_fixed_0.1_rsi_momentum.csv")
        f_short = os.path.join(ROOT_DIR, f"results_{sym}_1h_short_fixed_0.1_ema_cross.csv")
        for fpath, label in [(f_long, "LONG ONLY"), (f_short, "SHORT ONLY")]:
            if os.path.isfile(fpath):
                df = parse_trades_from_csv(fpath)
                if not df.empty:
                    maes = df["mae_pct"]
                    liq_count = (df["exit_reason"] == "LIQUIDATION_1X").sum() if "exit_reason" in df.columns else 0
                    print(f"Asset: {sym:<4} | {label:<10} | Trades: {len(df):>4} | MAE Max: -{maes.max():.2f}% | MAE >=20%: {(maes>=20).sum()} | Liquidations: {liq_count}")

    # 5. Timeframe Scaling (Vectorized, Fast)
    print("\n--- 5. TIMEFRAME SCALING ANALYSIS (BTC OHLCV) ---")
    btc_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto", "BTC")
    for tf in ["1m", "5m", "1h"]:
        csv_file = os.path.join(btc_dir, f"{tf}.csv")
        if os.path.isfile(csv_file):
            # Read first 50,000 rows to be ultra fast
            df_tf = pd.read_csv(csv_file, nrows=50000)
            col_map = {c: c.lower().strip() for c in df_tf.columns}
            df_tf.rename(columns=col_map, inplace=True)
            ranges = (df_tf["high"] - df_tf["low"]) / df_tf["open"] * 100.0
            print(f"Timeframe: {tf:>3} | Sample Rows: {len(df_tf):>6,} | Median Bar Range: {ranges.median():.3f}% | Mean Bar Range: {ranges.mean():.3f}% | 95th Pct Range: {ranges.quantile(0.95):.3f}%")

    # Resample 1h to 4h and 1d to show higher timeframes
    csv_1h = os.path.join(btc_dir, "1h.csv")
    if os.path.isfile(csv_1h):
        df_1h = pd.read_csv(csv_1h)
        col_map = {c: c.lower().strip() for c in df_1h.columns}
        df_1h.rename(columns=col_map, inplace=True)
        df_1h["dt"] = pd.to_datetime(df_1h["open_time"], unit="ms")
        df_1h.set_index("dt", inplace=True)

        for higher_tf, rule in [("4h", "4h"), ("1d", "1D")]:
            res = df_1h.resample(rule).agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
            ranges = (res["high"] - res["low"]) / res["open"] * 100.0
            print(f"Timeframe: {higher_tf:>3} | Resampled Rows: {len(res):>6,} | Median Bar Range: {ranges.median():.3f}% | Mean Bar Range: {ranges.mean():.3f}% | 95th Pct Range: {ranges.quantile(0.95):.3f}%")


if __name__ == "__main__":
    run_full_deep_dive()
