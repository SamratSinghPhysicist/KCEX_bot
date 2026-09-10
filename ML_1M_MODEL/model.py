"""
ML Trading Model Architecture
=============================
Multi-task model architecture combining:
1. Multi-class Gradient Boosting Classifier for Action (BUY, SELL, WAIT/HOLD)
2. Excursion Regressors for Dynamic Take-Profit and Stop-Loss distances
Supports LightGBM with automated Scikit-Learn HistGradientBoosting fallback.
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any

from .config import ModelConfig, MODELS_DIR, get_tick_spec

# Attempt LightGBM import, fallback to scikit-learn HistGradientBoosting
USE_LIGHTGBM = False
try:
    import lightgbm as lgb
    USE_LIGHTGBM = True
except ImportError:
    from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor


class TradingModel:
    """
    Unified 1-Minute ML Trading Model for Directional Classification and Dynamic Risk Management.
    """
    def __init__(self, cfg: Optional[ModelConfig] = None):
        self.cfg = cfg or ModelConfig()
        self.feature_cols: List[str] = []
        self.is_trained: bool = False

        # Models
        self.classifier = None
        self.tp_regressor = None
        self.sl_regressor = None

        self._init_models()

    def _init_models(self):
        """Initializes classifiers and regressors using LightGBM or Scikit-Learn."""
        if USE_LIGHTGBM:
            self.classifier = lgb.LGBMClassifier(
                objective="multiclass",
                num_class=3,
                boosting_type="gbdt",
                learning_rate=self.cfg.lgb_params.get("learning_rate", 0.03),
                num_leaves=self.cfg.lgb_params.get("num_leaves", 31),
                max_depth=self.cfg.lgb_params.get("max_depth", 6),
                n_estimators=self.cfg.lgb_params.get("n_estimators", 350),
                subsample=self.cfg.lgb_params.get("bagging_fraction", 0.8),
                colsample_bytree=self.cfg.lgb_params.get("feature_fraction", 0.8),
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            self.tp_regressor = lgb.LGBMRegressor(
                objective="regression",
                learning_rate=0.03,
                num_leaves=31,
                max_depth=6,
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            self.sl_regressor = lgb.LGBMRegressor(
                objective="regression",
                learning_rate=0.03,
                num_leaves=31,
                max_depth=6,
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
        else:
            # Fallback to Scikit-Learn HistGradientBoosting
            self.classifier = HistGradientBoostingClassifier(
                max_iter=200,
                learning_rate=0.05,
                max_leaf_nodes=31,
                max_depth=6,
                random_state=42
            )
            self.tp_regressor = HistGradientBoostingRegressor(
                max_iter=150,
                learning_rate=0.05,
                max_leaf_nodes=31,
                max_depth=6,
                random_state=42
            )
            self.sl_regressor = HistGradientBoostingRegressor(
                max_iter=150,
                learning_rate=0.05,
                max_leaf_nodes=31,
                max_depth=6,
                random_state=42
            )

    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        tp_target_train: np.ndarray,
        sl_target_train: np.ndarray,
        feature_cols: List[str]
    ):
        """Fits the multi-task model on training data."""
        self.feature_cols = feature_cols
        X_mat = X_train[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).values

        # 1. Fit Multi-Class Directional Classifier
        self.classifier.fit(X_mat, y_train)

        # 2. Fit Excursion Regressors for TP & SL
        self.tp_regressor.fit(X_mat, tp_target_train)
        self.sl_regressor.fit(X_mat, sl_target_train)

        self.is_trained = True

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Returns class probabilities [P(WAIT), P(BUY), P(SELL)]."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before predicting.")
        X_mat = X[self.feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).values
        return self.classifier.predict_proba(X_mat)

    def predict_decision(
        self,
        X: pd.DataFrame,
        current_prices: np.ndarray,
        current_atrs: np.ndarray,
        symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Translates probabilities and excursion forecasts into actionable trading decisions.
        Outputs: action, confidence, suggested TP & SL prices, ticks, and risk-reward ratio.
        """
        probs = self.predict_proba(X)
        X_mat = X[self.feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).values

        pred_tp_dists = self.tp_regressor.predict(X_mat)
        pred_sl_dists = self.sl_regressor.predict(X_mat)

        sym = symbol or self.cfg.symbol
        tick_spec = get_tick_spec(sym)
        tick_size = tick_spec["tick_size"]
        precision = int(tick_spec["price_precision"])

        decisions = []
        conf_thresh = self.cfg.confidence_threshold
        edge_thresh = self.cfg.edge_threshold

        for i in range(len(probs)):
            p_wait = probs[i, self.cfg.CLASS_WAIT]
            p_buy = probs[i, self.cfg.CLASS_BUY]
            p_sell = probs[i, self.cfg.CLASS_SELL]

            curr_price = float(current_prices[i])
            curr_atr = float(current_atrs[i]) if current_atrs[i] > 0 else curr_price * 0.002

            # Determine dynamic distances
            raw_tp = pred_tp_dists[i]
            raw_sl = pred_sl_dists[i]

            # Bounds check with ATR multipliers
            tp_dist = max(float(raw_tp), self.cfg.tp_atr_mult * curr_atr, curr_price * self.cfg.min_profit_pct)
            sl_dist = max(float(raw_sl), self.cfg.sl_atr_mult * curr_atr, curr_price * (self.cfg.min_profit_pct * 0.75))

            action = "WAIT / HOLD"
            confidence = float(p_wait)
            action_code = self.cfg.CLASS_WAIT
            tp_price = 0.0
            sl_price = 0.0
            tp_ticks = 0
            sl_ticks = 0

            # Long Signal Condition
            if p_buy >= conf_thresh and (p_buy - p_sell) >= edge_thresh:
                action = "BUY"
                confidence = float(p_buy)
                action_code = self.cfg.CLASS_BUY
                tp_price = round(curr_price + tp_dist, precision)
                sl_price = round(curr_price - sl_dist, precision)
                tp_ticks = int(round(tp_dist / tick_size))
                sl_ticks = int(round(sl_dist / tick_size))

            # Short Signal Condition
            elif p_sell >= conf_thresh and (p_sell - p_buy) >= edge_thresh:
                action = "SELL"
                confidence = float(p_sell)
                action_code = self.cfg.CLASS_SELL
                tp_price = round(curr_price - tp_dist, precision)
                sl_price = round(curr_price + sl_dist, precision)
                tp_ticks = int(round(tp_dist / tick_size))
                sl_ticks = int(round(sl_dist / tick_size))

            rr_ratio = round(tp_dist / (sl_dist + 1e-9), 2)

            decisions.append({
                "action": action,
                "action_code": action_code,
                "confidence": round(confidence, 4),
                "prob_wait": round(float(p_wait), 4),
                "prob_buy": round(float(p_buy), 4),
                "prob_sell": round(float(p_sell), 4),
                "entry_price": round(curr_price, precision),
                "suggested_tp": tp_price,
                "suggested_sl": sl_price,
                "tp_ticks": tp_ticks,
                "sl_ticks": sl_ticks,
                "tp_distance_pct": round((tp_dist / curr_price) * 100, 3),
                "sl_distance_pct": round((sl_dist / curr_price) * 100, 3),
                "risk_reward_ratio": rr_ratio,
            })

        return decisions

    def get_feature_importances(self) -> pd.DataFrame:
        """Returns sorted feature importances of the directional classifier."""
        if not self.is_trained:
            return pd.DataFrame()

        if hasattr(self.classifier, "feature_importances_"):
            importances = self.classifier.feature_importances_
        else:
            importances = np.ones(len(self.feature_cols))

        df_imp = pd.DataFrame({
            "feature": self.feature_cols,
            "importance": importances
        }).sort_values("importance", ascending=False).reset_index(drop=True)
        return df_imp

    def save(self, filepath: Optional[str] = None):
        """Saves trained model bundle and metadata to disk."""
        path = filepath or os.path.join(MODELS_DIR, f"ml_1m_model_{self.cfg.symbol.lower()}.pkl")
        bundle = {
            "classifier": self.classifier,
            "tp_regressor": self.tp_regressor,
            "sl_regressor": self.sl_regressor,
            "feature_cols": self.feature_cols,
            "config": self.cfg,
            "use_lightgbm": USE_LIGHTGBM,
        }
        with open(path, "wb") as f:
            pickle.dump(bundle, f)
        print(f"[Model] Successfully saved model bundle to {path}")

    @classmethod
    def load(cls, filepath: str) -> "TradingModel":
        """Loads model bundle from disk."""
        with open(filepath, "rb") as f:
            bundle = pickle.load(f)

        instance = cls(bundle.get("config"))
        instance.classifier = bundle["classifier"]
        instance.tp_regressor = bundle["tp_regressor"]
        instance.sl_regressor = bundle["sl_regressor"]
        instance.feature_cols = bundle["feature_cols"]
        instance.is_trained = True
        return instance
