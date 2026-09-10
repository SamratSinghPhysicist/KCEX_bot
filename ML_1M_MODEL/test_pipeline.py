"""
Comprehensive Automated Unit & Pipeline Verification Suite
===========================================================
Validates feature extraction, order-flow aggregation, triple-barrier labeling,
model training, dynamic TP/SL generation, and inference.
Runs rapidly using synthetic and sample structures to preserve local resources.
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure package import
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ML_1M_MODEL.config import ModelConfig, get_tick_spec
from ML_1M_MODEL.features import extract_features, calculate_atr, calculate_rsi
from ML_1M_MODEL.labeler import compute_triple_barrier_labels
from ML_1M_MODEL.model import TradingModel
from ML_1M_MODEL.trainer import train_model
from ML_1M_MODEL.evaluator import backtest_out_of_sample


class TestMLPipeline(unittest.TestCase):

    def setUp(self):
        """Generates synthetic 1m candles and tick trades for fast testing."""
        np.random.seed(42)
        n = 300
        base_price = 10.0
        start_ts = 1735689600000  # 2025-01-01 00:00:00

        # Geometric Brownian Motion
        returns = np.random.normal(0.0001, 0.002, n)
        prices = base_price * np.exp(np.cumsum(returns))

        highs = prices * (1.0 + np.abs(np.random.normal(0, 0.001, n)))
        lows = prices * (1.0 - np.abs(np.random.normal(0, 0.001, n)))
        opens = (prices + np.roll(prices, 1)) / 2.0
        opens[0] = base_price
        closes = prices
        volumes = np.random.uniform(1000, 50000, n)
        timestamps = [start_ts + i * 60000 for i in range(n)]

        self.df_ohlcv = pd.DataFrame({
            "timestamp": timestamps,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "trades_count": np.random.randint(50, 1000, n),
            "taker_buy_volume": volumes * np.random.uniform(0.3, 0.7, n)
        })

        # Synthetic order flow
        self.df_orderflow = pd.DataFrame({
            "timestamp": timestamps,
            "of_buy_volume": volumes * 0.52,
            "of_sell_volume": volumes * 0.48,
            "of_delta_volume": volumes * 0.04,
            "of_taker_buy_ratio": 0.52,
            "of_imbalance_ratio": 0.04,
            "of_trades_count": 100,
            "of_buy_trades_count": 55,
            "of_sell_trades_count": 45,
            "of_trade_count_ratio": 0.55,
            "of_vwap": prices * 0.9999,
            "of_avg_trade_size": 250.0,
            "of_whale_ratio": 0.15,
            "of_cvd_slope": 0.02
        })

        self.cfg = ModelConfig(
            symbol="TRUMPUSDT",
            horizon_bars=5,
            tp_atr_mult=1.5,
            sl_atr_mult=1.0,
            test_size=0.25,
            embargo_bars=5,
            confidence_threshold=0.45
        )

    def test_feature_extraction(self):
        """Verifies feature extraction shapes and calculations."""
        df_feats, feature_cols = extract_features(self.df_ohlcv, self.df_orderflow)
        self.assertGreater(len(feature_cols), 25)
        self.assertIn("ret_1m", feature_cols)
        self.assertIn("dist_ema9", feature_cols)
        self.assertIn("parkinson_vol", feature_cols)
        self.assertIn("rsi_14", feature_cols)
        self.assertIn("of_taker_buy_ratio", feature_cols)
        self.assertEqual(len(df_feats), len(self.df_ohlcv))

    def test_triple_barrier_labeling(self):
        """Verifies triple-barrier logic and class generation."""
        df_feats, _ = extract_features(self.df_ohlcv, self.df_orderflow)
        df_labeled = compute_triple_barrier_labels(df_feats, self.cfg)
        self.assertIn("target_label", df_labeled.columns)
        self.assertIn("target_tp_dist", df_labeled.columns)
        self.assertIn("target_sl_dist", df_labeled.columns)

        unique_labels = set(df_labeled["target_label"].unique())
        self.assertTrue(unique_labels.issubset({0, 1, 2}))

    def test_end_to_end_training_and_eval(self):
        """Verifies model training, predictions, and backtest evaluation."""
        model, train_df, test_df, metrics = train_model(self.df_ohlcv, self.df_orderflow, self.cfg)
        self.assertTrue(model.is_trained)
        self.assertGreater(metrics["train_accuracy"], 0.0)

        # Test inference decisions
        decisions = model.predict_decision(
            X=test_df.iloc[:5],
            current_prices=test_df["close"].iloc[:5].values,
            current_atrs=test_df["atr_14"].iloc[:5].values,
            symbol="TRUMPUSDT"
        )
        self.assertEqual(len(decisions), 5)
        for d in decisions:
            self.assertIn(d["action"], ["BUY", "SELL", "WAIT / HOLD"])
            self.assertGreaterEqual(d["confidence"], 0.0)
            self.assertGreater(d["entry_price"], 0.0)
            if d["action"] in ["BUY", "SELL"]:
                self.assertGreater(d["suggested_tp"], 0.0)
                self.assertGreater(d["suggested_sl"], 0.0)
                self.assertGreater(d["tp_ticks"], 0)
                self.assertGreater(d["sl_ticks"], 0)

        # Test Out-Of-Sample Evaluator
        oos_metrics, df_trades, md_report = backtest_out_of_sample(model, test_df, self.cfg)
        self.assertIn("win_rate_pct", oos_metrics)
        self.assertIn("profit_factor", oos_metrics)
        self.assertTrue(len(md_report) > 100)


if __name__ == "__main__":
    unittest.main()
