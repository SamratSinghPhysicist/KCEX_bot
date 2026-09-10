"""
Triple Barrier & Dynamic Target Labeling Engine
===============================================
Computes forward-looking targets for 1-minute tactical trading:
1. Discrete Signal Label:
   - 1 = BUY  (Upper barrier reached first with favorable risk-reward)
   - 2 = SELL (Lower barrier reached first with favorable risk-reward)
   - 0 = WAIT / HOLD (Noise, flat chop, or time exit without edge)
2. Continuous Targets:
   - Maximum Favorable Excursion (MFE) -> informs optimal dynamic Take Profit
   - Maximum Adverse Excursion (MAE)   -> informs safe dynamic Stop Loss
"""

import numpy as np
import pandas as pd
from typing import Tuple

from .config import ModelConfig, get_tick_spec


def compute_triple_barrier_labels(
    df: pd.DataFrame,
    cfg: ModelConfig
) -> pd.DataFrame:
    """
    Computes triple-barrier labels and continuous excursion targets
    over a forward horizon of H bars.
    """
    df = df.copy()
    n = len(df)
    H = cfg.horizon_bars
    tp_mult = cfg.tp_atr_mult
    sl_mult = cfg.sl_atr_mult
    min_profit = cfg.min_profit_pct

    closes = df["close"].values
    highs = df["high"].values
    lows = df["low"].values
    atrs = df["atr_14"].values

    labels = np.zeros(n, dtype=np.int32)  # 0 = WAIT
    target_mfe_pct = np.zeros(n, dtype=np.float32)
    target_mae_pct = np.zeros(n, dtype=np.float32)
    target_tp_dist = np.zeros(n, dtype=np.float32)
    target_sl_dist = np.zeros(n, dtype=np.float32)

    # We iterate up to n - H bars
    for i in range(n - H):
        curr_close = closes[i]
        curr_atr = atrs[i]

        if np.isnan(curr_close) or np.isnan(curr_atr) or curr_atr <= 0:
            continue

        # Dynamic barriers based on volatility
        tp_dist = tp_mult * curr_atr
        sl_dist = sl_mult * curr_atr

        # Ensure minimum profit threshold
        tp_dist = max(tp_dist, curr_close * min_profit)
        sl_dist = max(sl_dist, curr_close * (min_profit * 0.75))

        upper_barrier = curr_close + tp_dist
        lower_barrier = curr_close - sl_dist

        window_highs = highs[i + 1 : i + 1 + H]
        window_lows = lows[i + 1 : i + 1 + H]

        # Calculate maximum excursions
        max_h = np.max(window_highs)
        min_l = np.min(window_lows)

        mfe_buy = (max_h - curr_close) / curr_close
        mae_buy = (curr_close - min_l) / curr_close

        target_mfe_pct[i] = mfe_buy
        target_mae_pct[i] = mae_buy
        target_tp_dist[i] = tp_dist
        target_sl_dist[i] = sl_dist

        # Check barrier breach order
        hit_tp_idx = -1
        hit_sl_idx = -1

        for step in range(H):
            h_step = window_highs[step]
            l_step = window_lows[step]

            if hit_tp_idx == -1 and h_step >= upper_barrier:
                hit_tp_idx = step
            if hit_sl_idx == -1 and l_step <= lower_barrier:
                hit_sl_idx = step

            # If both hit on same candle or earlier, determine winner
            if hit_tp_idx != -1 and hit_sl_idx != -1:
                break

        # Assign label
        # Long trade logic:
        if hit_tp_idx != -1 and (hit_sl_idx == -1 or hit_tp_idx < hit_sl_idx):
            labels[i] = cfg.CLASS_BUY
        # Short trade logic:
        elif hit_sl_idx != -1 and (hit_tp_idx == -1 or hit_sl_idx < hit_tp_idx):
            labels[i] = cfg.CLASS_SELL
        else:
            labels[i] = cfg.CLASS_WAIT

    df["target_label"] = labels
    df["target_mfe_pct"] = target_mfe_pct
    df["target_mae_pct"] = target_mae_pct
    df["target_tp_dist"] = target_tp_dist
    df["target_sl_dist"] = target_sl_dist

    # Remove the last H bars since they have incomplete forward windows
    df_labeled = df.iloc[:-H].copy().reset_index(drop=True)

    # Log class distribution
    counts = df_labeled["target_label"].value_counts().to_dict()
    total = len(df_labeled)
    wait_pct = (counts.get(cfg.CLASS_WAIT, 0) / total) * 100
    buy_pct = (counts.get(cfg.CLASS_BUY, 0) / total) * 100
    sell_pct = (counts.get(cfg.CLASS_SELL, 0) / total) * 100

    print(f"[Labeler] Target distribution ({total:,} bars): "
          f"BUY={buy_pct:.1f}%, SELL={sell_pct:.1f}%, WAIT/HOLD={wait_pct:.1f}%")

    return df_labeled
