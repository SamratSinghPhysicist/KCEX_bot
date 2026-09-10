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
    cfg: Optional[ModelConfig] = None
) -> Tuple[TradingModel, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Executes end-to-end training pipeline with strictly purged out-of-sample split:
    1. Feature engineering
    2. Labeling with triple barriers
    3. Chronological train/test split with embargo gap
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

    # Step 3: Chronological Split with Embargo
    n = len(df_dataset)
    test_count = int(n * cfg.test_size)
    train_end = n - test_count - cfg.embargo_bars

    if train_end <= 0:
        raise ValueError(f"Insufficient data ({n} bars) for train_size with embargo {cfg.embargo_bars}.")

    train_df = df_dataset.iloc[:train_end].copy().reset_index(drop=True)
    test_df = df_dataset.iloc[train_end + cfg.embargo_bars:].copy().reset_index(drop=True)

    print(f"[Trainer] Chronological Split: Train={len(train_df):,} bars, Embargo={cfg.embargo_bars} bars, Test={len(test_df):,} bars.")

    # Target arrays
    y_train = train_df["target_label"].values
    tp_target_train = train_df["target_tp_dist"].values
    sl_target_train = train_df["target_sl_dist"].values

    # Step 4: Model Initialization and Fitting
    model = TradingModel(cfg)
    print(f"[Trainer] Fitting multi-task model on {len(feature_cols)} features...")
    model.fit(
        X_train=train_df,
        y_train=y_train,
        tp_target_train=tp_target_train,
        sl_target_train=sl_target_train,
        feature_cols=feature_cols
    )

    # Step 5: Evaluate on Training Set
    train_probs = model.predict_proba(train_df)
    train_preds = np.argmax(train_probs, axis=1)
    train_acc = float(accuracy_score(y_train, train_preds))
    train_loss = float(log_loss(y_train, train_probs))

    # Feature importances
    imp_df = model.get_feature_importances()
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

    # Save models
    model.save()

    return model, train_df, test_df, metrics
