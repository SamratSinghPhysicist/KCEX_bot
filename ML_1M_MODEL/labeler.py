"""
Symmetric Triple Barrier & Dynamic Target Labeling Engine
=========================================================
Computes forward-looking targets for 1-minute tactical trading:
1. Discrete Signal Label (Symmetric formulation):
   - 1 = BUY  (Long hits +TP before -SL, Short does not)
   - 2 = SELL (Short hits -TP before +SL, Long does not)
   - 0 = WAIT / HOLD (Noise, flat chop, or neither barrier hit cleanly)
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
    Computes mathematically symmetric triple-barrier labels and continuous excursion targets
    over a forward horizon of H bars. Eliminates artificial class imbalance.
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

    for i in range(n - H):
        curr_close = closes[i]
        curr_atr = atrs[i]

        if np.isnan(curr_close) or np.isnan(curr_atr) or curr_atr <= 0:
            continue

        # Dynamic barriers based on volatility
        tp_dist = max(tp_mult * curr_atr, curr_close * min_profit)
        sl_dist = max(sl_mult * curr_atr, curr_close * (min_profit * 0.5))

        window_highs = highs[i + 1 : i + 1 + H]
        window_lows = lows[i + 1 : i + 1 + H]

        max_h = np.max(window_highs)
        min_l = np.min(window_lows)

        target_mfe_pct[i] = (max_h - curr_close) / curr_close
        target_mae_pct[i] = (curr_close - min_l) / curr_close
        target_tp_dist[i] = tp_dist
        target_sl_dist[i] = sl_dist

        # 1. Evaluate Long Opportunity
        long_tp = curr_close + tp_dist
        long_sl = curr_close - sl_dist
        long_tp_idx = -1
        long_sl_idx = -1

        for step in range(H):
            if long_tp_idx == -1 and window_highs[step] >= long_tp:
                long_tp_idx = step
            if long_sl_idx == -1 and window_lows[step] <= long_sl:
                long_sl_idx = step
            if long_tp_idx != -1 and long_sl_idx != -1:
                break
        long_success = (long_tp_idx != -1) and (long_sl_idx == -1 or long_tp_idx < long_sl_idx)

        # 2. Evaluate Short Opportunity
        short_tp = curr_close - tp_dist
        short_sl = curr_close + sl_dist
        short_tp_idx = -1
        short_sl_idx = -1

        for step in range(H):
            if short_tp_idx == -1 and window_lows[step] <= short_tp:
                short_tp_idx = step
            if short_sl_idx == -1 and window_highs[step] >= short_sl:
                short_sl_idx = step
            if short_tp_idx != -1 and short_sl_idx != -1:
                break
        short_success = (short_tp_idx != -1) and (short_sl_idx == -1 or short_tp_idx < short_sl_idx)

        # 3. Symmetric Decision Logic
        if long_success and not short_success:
            labels[i] = cfg.CLASS_BUY
        elif short_success and not long_success:
            labels[i] = cfg.CLASS_SELL
        elif long_success and short_success:
            labels[i] = cfg.CLASS_BUY if long_tp_idx < short_tp_idx else cfg.CLASS_SELL
        else:
            labels[i] = cfg.CLASS_WAIT

    df["target_label"] = labels
    df["target_mfe_pct"] = target_mfe_pct
    df["target_mae_pct"] = target_mae_pct
    df["target_tp_dist"] = target_tp_dist
    df["target_sl_dist"] = target_sl_dist

    df_labeled = df.iloc[:-H].copy().reset_index(drop=True)

    counts = df_labeled["target_label"].value_counts().to_dict()
    total = len(df_labeled)
    wait_pct = (counts.get(cfg.CLASS_WAIT, 0) / total) * 100
    buy_pct = (counts.get(cfg.CLASS_BUY, 0) / total) * 100
    sell_pct = (counts.get(cfg.CLASS_SELL, 0) / total) * 100

    print(f"[Labeler] Symmetric target distribution ({total:,} bars): "
          f"BUY={buy_pct:.1f}%, SELL={sell_pct:.1f}%, WAIT/HOLD={wait_pct:.1f}%")

    return df_labeled
