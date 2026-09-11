"""
ML Trading Model Architecture
=============================
Multi-task model architecture powered 100% by Scikit-Learn:
1. HistGradientBoostingClassifier for Multi-Class Action (BUY, SELL, WAIT/HOLD)
2. HistGradientBoostingRegressor for Dynamic Take-Profit and Stop-Loss distances
Guarantees 100% environment parity between local development and GitHub Actions.
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

from .config import ModelConfig, MODELS_DIR, get_tick_spec


class TradingModel:
    """
    Unified 1-Minute ML Trading Model for Directional Classification and Dynamic Risk Management.
    Eliminates dead compute by focusing on high-conviction directional probabilities
    with volatility-calibrated risk geometry.
    """
    def __init__(self, cfg: Optional[ModelConfig] = None):
        self.cfg = cfg or ModelConfig()
        self.feature_cols: List[str] = []
        self.is_trained: bool = False

        # Directional Classifier
        self.classifier = None
        self._init_models()

    def _init_models(self):
        """Initializes classifier using standard Scikit-Learn with L2 regularization."""
        hgb_params = getattr(self.cfg, "hgb_params", {})
        self.classifier = HistGradientBoostingClassifier(
            max_iter=hgb_params.get("max_iter", 250),
            learning_rate=hgb_params.get("learning_rate", 0.03),
            max_leaf_nodes=hgb_params.get("max_leaf_nodes", 31),
            max_depth=hgb_params.get("max_depth", 5),
            min_samples_leaf=hgb_params.get("min_samples_leaf", 50),
            l2_regularization=hgb_params.get("l2_regularization", 3.0),
            early_stopping=hgb_params.get("early_stopping", True),
            validation_fraction=hgb_params.get("validation_fraction", 0.15),
            n_iter_no_change=hgb_params.get("n_iter_no_change", 15),
            random_state=42
        )

    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        feature_cols: List[str],
        tp_target_train: Optional[np.ndarray] = None,
        sl_target_train: Optional[np.ndarray] = None
    ):
        """Fits the directional classifier on training data."""
        self.feature_cols = feature_cols
        X_mat = X_train[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).values

        # Fit Directional Classifier
        self.classifier.fit(X_mat, y_train)
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
        Translates probabilities and macro regime confluence into actionable trading decisions.
        Outputs: action, confidence, suggested TP & SL prices, ticks, and risk-reward ratio.
        """
        probs = self.predict_proba(X)

        sym = symbol or self.cfg.symbol
        tick_spec = get_tick_spec(sym)
        tick_size = tick_spec["tick_size"]
        precision = int(tick_spec["price_precision"])

        decisions = []
        conf_thresh_buy = self.cfg.confidence_threshold
        conf_thresh_sell = getattr(self.cfg, "confidence_threshold_sell", conf_thresh_buy)
        edge_thresh = self.cfg.edge_threshold

        for i in range(len(probs)):
            p_wait = probs[i, self.cfg.CLASS_WAIT]
            p_buy = probs[i, self.cfg.CLASS_BUY]
            p_sell = probs[i, self.cfg.CLASS_SELL]

            curr_price = float(current_prices[i])
            curr_atr = float(current_atrs[i]) if current_atrs[i] > 0 else curr_price * 0.002

            # Dynamic Take Profit & Stop Loss geometry scaled to asset volatility
            tp_dist = max(self.cfg.tp_atr_mult * curr_atr, curr_price * self.cfg.min_profit_pct)
            sl_dist = max(self.cfg.sl_atr_mult * curr_atr, curr_price * (self.cfg.min_profit_pct * 0.5))

            # Strict risk containment: cap max SL to 2.0% distance to prevent outsized leverage drawdowns
            sl_dist = min(sl_dist, curr_price * 0.020)

            action = "WAIT / HOLD"
            confidence = float(p_wait)
            action_code = self.cfg.CLASS_WAIT
            tp_price = 0.0
            sl_price = 0.0
            tp_ticks = 0
            sl_ticks = 0

            # Macro regime and order flow gating
            macro_bull = bool(X["macro_bull"].iloc[i]) if "macro_bull" in X.columns else False
            macro_bear = bool(X["macro_bear"].iloc[i]) if "macro_bear" in X.columns else False
            trend_htf_val = float(X["trend_htf"].iloc[i]) if "trend_htf" in X.columns else 0.0
            trend_1m_val = float(X["trend_score"].iloc[i]) if "trend_score" in X.columns else 0.0
            
            if "taker_ratio" in X.columns:
                t_ratio = float(X["taker_ratio"].iloc[i])
            elif "of_taker_buy_ratio" in X.columns:
                t_ratio = float(X["of_taker_buy_ratio"].iloc[i])
            else:
                t_ratio = 0.50
                
            bb_exp = float(X["bb_expansion"].iloc[i]) if "bb_expansion" in X.columns else 1.0

            if getattr(self.cfg, "macro_regime_filter", True):
                # Strict Macro Directional Gating:
                # In Bull macro: only Longs allowed. In Bear macro: only Shorts allowed.
                allow_long = (macro_bull or trend_htf_val >= 0.25) and (trend_1m_val >= -0.25) and (t_ratio >= 0.48)
                allow_short = (macro_bear or trend_htf_val <= -0.25) and (trend_1m_val <= 0.25) and (t_ratio <= 0.52)
            else:
                allow_long = (trend_1m_val >= -0.25)
                allow_short = (trend_1m_val <= 0.25)

            squeeze_ok = (bb_exp >= 1.0)

            # Long Signal Condition
            if allow_long and squeeze_ok and p_buy >= conf_thresh_buy and (p_buy - p_sell) >= edge_thresh and p_buy > (p_wait * 0.65):
                action = "BUY"
                confidence = float(p_buy)
                action_code = self.cfg.CLASS_BUY
                tp_price = curr_price + tp_dist
                sl_price = curr_price - sl_dist
                tp_ticks = int(round(tp_dist / tick_size))
                sl_ticks = int(round(sl_dist / tick_size))

            # Short Signal Condition
            elif allow_short and squeeze_ok and p_sell >= conf_thresh_sell and (p_sell - p_buy) >= edge_thresh and p_sell > (p_wait * 0.65):
                action = "SELL"
                confidence = float(p_sell)
                action_code = self.cfg.CLASS_SELL
                tp_price = curr_price - tp_dist
                sl_price = curr_price + sl_dist
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
                "suggested_tp": round(tp_price, precision) if action != "WAIT / HOLD" else 0.0,
                "suggested_sl": round(sl_price, precision) if action != "WAIT / HOLD" else 0.0,
                "tp_price_exact": tp_price if action != "WAIT / HOLD" else 0.0,
                "sl_price_exact": sl_price if action != "WAIT / HOLD" else 0.0,
                "tp_ticks": tp_ticks,
                "sl_ticks": sl_ticks,
                "tp_distance_pct": round((tp_dist / curr_price) * 100, 3),
                "sl_distance_pct": round((sl_dist / curr_price) * 100, 3),
                "risk_reward_ratio": rr_ratio,
            })

        return decisions

    def get_feature_importances(
        self,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[np.ndarray] = None
    ) -> pd.DataFrame:
        """
        Returns sorted feature importances of the directional classifier.
        Computes genuine permutation importance on validation data when provided.
        """
        if not self.is_trained:
            return pd.DataFrame()

        if X_val is not None and y_val is not None and len(X_val) > 0:
            from sklearn.inspection import permutation_importance
            n_sample = min(2000, len(X_val))
            idx = np.random.RandomState(42).choice(len(X_val), n_sample, replace=False)
            X_sample = X_val[self.feature_cols].iloc[idx].replace([np.inf, -np.inf], np.nan).fillna(0.0).values
            y_sample = y_val[idx]
            result = permutation_importance(self.classifier, X_sample, y_sample, n_repeats=3, random_state=42, n_jobs=-1)
            importances = result.importances_mean
        elif hasattr(self.classifier, "feature_importances_"):
            importances = self.classifier.feature_importances_
        else:
            importances = np.zeros(len(self.feature_cols))

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
            "feature_cols": self.feature_cols,
            "config": self.cfg,
            "framework": "scikit-learn",
        }
        with open(path, "wb") as f:
            pickle.dump(bundle, f)
        print(f"[Model] Successfully saved model bundle to {path}")

    @classmethod
    def load(cls, filepath: str) -> "TradingModel":
        """Loads model bundle from disk, supporting legacy bundles gracefully."""
        with open(filepath, "rb") as f:
            bundle = pickle.load(f)

        instance = cls(bundle.get("config"))
        instance.classifier = bundle["classifier"]
        instance.feature_cols = bundle["feature_cols"]
        instance.is_trained = True
        return instance
