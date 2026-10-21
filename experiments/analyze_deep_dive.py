#!/usr/bin/env python3
"""
Deep-Dive Quantitative Analyzer:
1. Trade Frequency Across Timeframes & Assets
2. Frequency & Probability of Severe Drawdown / Near-Liquidation Moves
3. Most Probable Moves in Favor (MFE) and Against (MAE)
4. Timeframe Scaling Analysis (1m, 5m, 15m, 1h, 4h, 1d)
"""

import os
import sys
import glob
import csv
import numpy as np
import pandas as pd
from collections import Counter
from typing import List, Dict, Any, Tuple

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.no_stop_loss_experiment import load_candles, Candle
from experiments.strategies import run_strategy


def parse_trades_from_csv(csv_path: str) -> pd.DataFrame:
    """Extracts the detailed trades table from a results CSV file."""
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

    from io import StringIO
    df = pd.read_csv(StringIO("".join(lines)))
    return df


def analyze_frequency_and_drawdowns(csv_files: List[str]):
    print("=" * 80)
    print("🔬 COMPREHENSIVE FREQUENCY, DRAWDOWN & PROBABILITY ANALYSIS")
    print("=" * 80)

    for csv_file in csv_files:
        df = parse_trades_from_csv(csv_file)
        if df.empty or len(df) < 20:
            continue

        asset = df["asset"].iloc[0]
        tf = df["timeframe"].iloc[0]
        strat = df["strategy"].iloc[0]
        direction = df["direction_mode"].iloc[0]
        tp_rule = df["tp_rule"].iloc[0]

        total_trades = len(df)
        t_start = pd.to_datetime(df["entry_time_ms"].min(), unit="ms")
        t_end = pd.to_datetime(df["exit_time_ms"].max(), unit="ms")
        days = max(1.0, (t_end - t_start).total_seconds() / 86400.0)

        trades_per_day = total_trades / days
        trades_per_week = trades_per_day * 7.0
        trades_per_month = trades_per_day * 30.417

        # MAE and MFE series
        mfes = df["mfe_pct"].dropna()
        maes = df["mae_pct"].dropna()

        # Empirical Modes (binned)
        def _calc_mode(vals: pd.Series, bin_size: float = 0.1) -> float:
            binned = (vals / bin_size).round() * bin_size
            counts = Counter(binned.round(4))
            if not counts:
                return 0.0
            return counts.most_common(1)[0][0]

        mode_mfe = _calc_mode(mfes, bin_size=0.05)
        mode_mae = _calc_mode(maes, bin_size=0.10)

        # MAE Buckets (Severe Drawdown Clusters)
        mae_1 = (maes < 1.0).mean() * 100.0
        mae_1_5 = ((maes >= 1.0) & (maes < 5.0)).mean() * 100.0
        mae_5_10 = ((maes >= 5.0) & (maes < 10.0)).mean() * 100.0
        mae_10_20 = ((maes >= 10.0) & (maes < 20.0)).mean() * 100.0
        mae_20_50 = ((maes >= 20.0) & (maes < 50.0)).mean() * 100.0
        mae_50_80 = ((maes >= 50.0) & (maes < 80.0)).mean() * 100.0
        mae_80_plus = (maes >= 80.0).mean() * 100.0

        # Frequency of severe drawdowns (how often in calendar time)
        severe_count = (maes >= 20.0).sum()
        near_liq_count = (maes >= 80.0).sum()
        days_per_severe = (days / severe_count) if severe_count > 0 else 9999.0
        days_per_near_liq = (days / near_liq_count) if near_liq_count > 0 else 9999.0

        print(f"\n────────────────────────────────────────────────────────────────")
        print(f"📊 ASSET: {asset} ({tf}) | Strategy: {strat} | Dir: {direction} | Rule: {tp_rule}")
        print(f"  Period: {t_start.strftime('%Y-%m-%d')} to {t_end.strftime('%Y-%m-%d')} ({days:.1f} days / {days/365.25:.1f} years)")
        print(f"  Total Trades: {total_trades:,}")
        print(f"  Trade Frequency:")
        print(f"    - Daily:   {trades_per_day:.2f} trades / day (1 trade every {24.0/trades_per_day:.1f} hours)")
        print(f"    - Weekly:  {trades_per_week:.1f} trades / week")
        print(f"    - Monthly: {trades_per_month:.1f} trades / month")
        print(f"  Most Probable Moves (Empirical Modes & Percentiles):")
        print(f"    - In Favor (MFE): Mode: +{mode_mfe:.2f}% | Median: +{mfes.median():.2f}% | 75th: +{mfes.quantile(0.75):.2f}% | 90th: +{mfes.quantile(0.90):.2f}%")
        print(f"    - Against (MAE):  Mode: -{mode_mae:.2f}% | Median: -{maes.median():.2f}% | 75th: -{maes.quantile(0.75):.2f}% | 90th: -{maes.quantile(0.90):.2f}%")
        print(f"  Probability of Favorable Move Reaching:")
        print(f"    - P(MFE >= +0.10%): {(mfes >= 0.10).mean()*100:.2f}%")
        print(f"    - P(MFE >= +0.20%): {(mfes >= 0.20).mean()*100:.2f}%")
        print(f"    - P(MFE >= +0.50%): {(mfes >= 0.50).mean()*100:.2f}%")
        print(f"    - P(MFE >= +1.00%): {(mfes >= 1.00).mean()*100:.2f}%")
        print(f"    - P(MFE >= +2.00%): {(mfes >= 2.00).mean()*100:.2f}%")
        print(f"    - P(MFE >= +5.00%): {(mfes >= 5.00).mean()*100:.2f}%")
        print(f"  Adverse Drawdown Distribution (How Severe Are Losses?):")
        print(f"    - Minor (< 1%):         {mae_1:.2f}% of trades")
        print(f"    - Pullback (1% - 5%):    {mae_1_5:.2f}% of trades")
        print(f"    - Correction (5% - 10%): {mae_5_10:.2f}% of trades")
        print(f"    - Serious (10% - 20%):   {mae_10_20:.2f}% of trades")
        print(f"    - Severe Crash (20%-50%):{mae_20_50:.2f}% of trades ({severe_count} times, occurs once every {days_per_severe:.1f} days / {days_per_severe/30.4:.1f} months)")
        print(f"    - Massive Drawdown (50%-80%): {mae_50_80:.2f}% of trades")
        print(f"    - Near-Liquidation (>=80%):   {mae_80_plus:.2f}% of trades ({near_liq_count} times, occurs once every {days_per_near_liq:.1f} days / {days_per_near_liq/30.4:.1f} months)")


def analyze_timeframe_scaling():
    """Analyzes how trade frequency and move sizes scale across timeframes: 1m, 5m, 15m, 1h, 4h, 1d."""
    print("\n" + "=" * 80)
    print("⏱️ TIMEFRAME SCALING ANALYSIS (1m -> 5m -> 15m -> 1h -> 4h -> 1d)")
    print("=" * 80)

    # Let's inspect BTC across timeframes
    from scripts.download_market_data import download_crypto
    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    tfs = ["1m", "5m", "15m", "1h", "4h", "1d"]

    for tf in tfs:
        try:
            candles = load_candles("BTC", tf, crypto_dir, crypto_dir)
            if len(candles) < 30:
                continue
            sigs = run_strategy("ema_cross", candles, direction="both")
            t_span_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)
            trades_day = len(sigs) / t_span_days if t_span_days > 0 else 0.0

            # Compute average candle range
            ranges = [(c.high - c.low) / c.open * 100.0 for c in candles]
            avg_range = np.mean(ranges)
            median_range = np.median(ranges)

            print(f"Timeframe: {tf:>4} | Bars: {len(candles):>6,} | Span: {t_span_days:>5.1f} days | Signals: {len(sigs):>5,} | Trades/Day: {trades_day:>6.2f} | Avg Candle Range: {avg_range:.2f}% (Median: {median_range:.2f}%)")
        except Exception as e:
            print(f"Timeframe: {tf:>4} | Error: {e}")


if __name__ == "__main__":
    key_csvs = [
        os.path.join(ROOT_DIR, "results_BTC_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_ETH_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_GOLD_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_AAPL_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_NVDA_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_TSLA_1h_both_fixed_0.1_ema_cross.csv"),
        os.path.join(ROOT_DIR, "results_MSFT_1h_both_fixed_0.1_ema_cross.csv"),
    ]
    analyze_frequency_and_drawdowns(key_csvs)
    analyze_timeframe_scaling()
