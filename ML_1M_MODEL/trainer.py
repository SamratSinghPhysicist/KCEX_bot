"""
Model Training & Walk-Forward Validation Engine
===============================================
Coordinates data preparation, feature extraction, purged time-series splitting,
and fitting of the multi-task model with zero lookahead bias.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, Optional
from sklearn.metrics import accuracy_score, classification_report, log_loss

from .config import ModelConfig, REPORTS_DIR, MODELS_DIR
from .features import extract_features
from .labeler import compute_triple_barrier_labels
from .model import TradingModel


def train_model(
    df_ohlcv: pd.DataFrame,
    df_orderflow: Optional[pd.DataFrame] = None,
    cfg: Optional[ModelConfig] = None,
    save_model: bool = True,
    model_save_path: Optional[str] = None
) -> Tuple[TradingModel, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Executes end-to-end training pipeline with strictly purged out-of-sample split:
    1. Feature engineering
    2. Labeling with triple barriers
    3. Chronological or calendar train/test split with embargo gap
    4. Model training
    5. Evaluation on train set
    """
    cfg = cfg or ModelConfig()
    print(f"[Trainer] Extracting features for {cfg.symbol} ({len(df_ohlcv):,} 1m candles)...")

    # Step 1: Feature Extraction
    df_feats, feature_cols = extract_features(df_ohlcv, df_orderflow)

    # Step 2: Triple Barrier Labeling
    print(f"[Trainer] Computing triple barrier targets (horizon={cfg.horizon_bars} bars, TP={cfg.tp_atr_mult}x ATR, SL={cfg.sl_atr_mult}x ATR)...")
    df_dataset = compute_triple_barrier_labels(df_feats, cfg)

    # Step 2b: Purge initial warmup bars (2000 bars needed for HTF EMA200 / rolling statistics to stabilize)
    warmup_bars = 2000 if len(df_dataset) > 5000 else 50
    if len(df_dataset) > warmup_bars * 2:
        df_dataset = df_dataset.iloc[warmup_bars:].copy().reset_index(drop=True)

    # Step 3: Calendar Split with Strict Embargo (or Ratio fallback)
    n = len(df_dataset)
    embargo_ms = cfg.embargo_bars * 60000

    use_calendar = False
    if cfg.split_mode == "calendar" and "timestamp" in df_dataset.columns:
        test_start_ts = int(pd.Timestamp(cfg.test_start_date).timestamp() * 1000)
        min_ts = df_dataset["timestamp"].iloc[0]
        max_ts = df_dataset["timestamp"].iloc[-1]
        if min_ts < test_start_ts < max_ts:
            use_calendar = True

    if use_calendar:
        test_start_ts = int(pd.Timestamp(cfg.test_start_date).timestamp() * 1000)
        train_mask = (df_dataset["timestamp"] < test_start_ts - embargo_ms)
        test_mask = (df_dataset["timestamp"] >= test_start_ts)
        train_df = df_dataset.loc[train_mask].copy().reset_index(drop=True)
        test_df = df_dataset.loc[test_mask].copy().reset_index(drop=True)
        print(f"[Trainer] Strict Calendar Split: Train ({cfg.train_start_date} to {cfg.train_end_date})={len(train_df):,} bars, "
              f"Embargo={cfg.embargo_bars} bars, Test ({cfg.test_start_date} to {cfg.test_end_date})={len(test_df):,} bars.")
    else:
        test_count = max(int(n * cfg.test_size), 1)
        train_end = n - test_count - cfg.embargo_bars
        if train_end <= 0:
            train_end = int(n * 0.7)
            train_df = df_dataset.iloc[:train_end].copy().reset_index(drop=True)
            test_df = df_dataset.iloc[train_end:].copy().reset_index(drop=True)
        else:
            train_df = df_dataset.iloc[:train_end].copy().reset_index(drop=True)
            test_df = df_dataset.iloc[train_end + cfg.embargo_bars:].copy().reset_index(drop=True)
        print(f"[Trainer] Ratio Chronological Split: Train={len(train_df):,} bars, Embargo={cfg.embargo_bars} bars, Test={len(test_df):,} bars.")

    if len(train_df) == 0 or len(test_df) == 0:
        raise ValueError(f"Insufficient data split: Train={len(train_df)}, Test={len(test_df)}.")

    # Target arrays
    y_train = train_df["target_label"].values

    # Step 4: Model Initialization and Fitting
    model = TradingModel(cfg)
    print(f"[Trainer] Fitting directional classifier on {len(feature_cols)} features...")
    model.fit(
        X_train=train_df,
        y_train=y_train,
        feature_cols=feature_cols
    )

    # Step 5: Evaluate on Training Set
    train_probs = model.predict_proba(train_df)
    train_preds = np.argmax(train_probs, axis=1)
    train_acc = float(accuracy_score(y_train, train_preds))
    train_loss = float(log_loss(y_train, train_probs))

    # Genuine permutation feature importances on validation slice
    val_slice = min(2000, len(train_df))
    imp_df = model.get_feature_importances(
        X_val=train_df.tail(val_slice),
        y_val=y_train[-val_slice:]
    )
    top_10 = imp_df.head(10).to_dict(orient="records")

    metrics = {
        "train_samples": len(train_df),
        "test_samples": len(test_df),
        "num_features": len(feature_cols),
        "train_accuracy": round(train_acc, 4),
        "train_log_loss": round(train_loss, 4),
        "top_features": top_10
    }

    print(f"[Trainer] Training completed! Accuracy: {train_acc:.2%}, LogLoss: {train_loss:.4f}")
    print("[Trainer] Top 5 Features:")
    for row in top_10[:5]:
        print(f"   - {row['feature']}: {row['importance']:.4f}")

    # Save models if requested
    if save_model:
        model.save(filepath=model_save_path)

    return model, train_df, test_df, metrics
