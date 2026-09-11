"""
Live & Offline ML Signal Inference Engine
=========================================
Generates actionable real-time recommendations for 1-minute crypto futures:
- Action: BUY | SELL | WAIT / HOLD
- Dynamic TP price & ticks (pu)
- Dynamic SL price & ticks (pu)
- Risk-to-Reward (R:R) ratio
- Microstructure & Order-Flow market regime context
"""

import os
import sys
import json
import argparse
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import ModelConfig, MODELS_DIR, get_tick_spec
from .model import TradingModel
from .features import extract_features
from .data_loader import load_ohlcv_range
from .orderflow_aggregator import build_orderflow_features_range


class Predictor:
    """
    Inference interface for generating real-time signals from latest 1m candles.
    """
    def __init__(self, symbol: str = "TRUMPUSDT", model_path: Optional[str] = None):
        self.symbol = symbol.upper().replace("-", "").replace("_", "")
        self.tick_spec = get_tick_spec(self.symbol)

        if model_path is None:
            model_path = os.path.join(MODELS_DIR, f"ml_1m_model_{self.symbol.lower()}.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Please train the model first via run_pipeline.py or GitHub Actions."
            )

        print(f"[Predictor] Loading model from {model_path} ...")
        self.model = TradingModel.load(model_path)

    def predict_from_dataframe(
        self,
        df_ohlcv: pd.DataFrame,
        df_orderflow: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Takes recent 1-minute candles (minimum 60 bars for full feature warmup)
        and returns the trade recommendation for the latest bar.
        """
        if len(df_ohlcv) < 200:
            raise ValueError(f"Need at least 200 candles for full feature warmup (received {len(df_ohlcv)}).")

        # Extract features
        df_feats, _ = extract_features(df_ohlcv, df_orderflow)

        # Get latest bar
        latest_idx = len(df_feats) - 1
        latest_row = df_feats.iloc[[latest_idx]]

        curr_price = float(df_ohlcv["close"].iloc[latest_idx])
        curr_atr = float(df_feats["atr_14"].iloc[latest_idx])
        ts = int(df_ohlcv["timestamp"].iloc[latest_idx])
        dt_str = str(pd.to_datetime(ts, unit="ms"))

        # Predict decision
        decisions = self.model.predict_decision(
            X=latest_row,
            current_prices=np.array([curr_price]),
            current_atrs=np.array([curr_atr]),
            symbol=self.symbol
        )
        dec = decisions[0]

        # Context features
        taker_ratio = float(latest_row["of_taker_buy_ratio"].iloc[0])
        imbalance = float(latest_row["of_imbalance_ratio"].iloc[0])
        cvd_slope = float(latest_row["of_cvd_slope"].iloc[0])
        rsi = float(latest_row["rsi_14"].iloc[0])

        if cvd_slope > 0.05:
            cvd_context = "STRONG_BUY_AGGRESSION"
        elif cvd_slope < -0.05:
            cvd_context = "STRONG_SELL_AGGRESSION"
        else:
            cvd_context = "BALANCED"

        if rsi > 70:
            regime = "OVERBOUGHT_MOMENTUM"
        elif rsi < 30:
            regime = "OVERSOLD_MOMENTUM"
        else:
            regime = "NEUTRAL_TRENDING"

        result = {
            "symbol": self.symbol,
            "timestamp": ts,
            "datetime": dt_str,
            "current_price": dec["entry_price"],
            "action": dec["action"],
            "confidence": dec["confidence"],
            "probabilities": {
                "BUY": dec["prob_buy"],
                "SELL": dec["prob_sell"],
                "WAIT_HOLD": dec["prob_wait"]
            },
            "dynamic_risk_management": {
                "suggested_tp_price": dec["suggested_tp"],
                "suggested_sl_price": dec["suggested_sl"],
                "tp_ticks_pu": dec["tp_ticks"],
                "sl_ticks_pu": dec["sl_ticks"],
                "tp_distance_pct": dec["tp_distance_pct"],
                "sl_distance_pct": dec["sl_distance_pct"],
                "risk_reward_ratio": dec["risk_reward_ratio"],
                "tick_size": self.tick_spec["tick_size"]
            },
            "market_microstructure": {
                "taker_buy_ratio": round(taker_ratio, 3),
                "order_flow_imbalance": round(imbalance, 3),
                "cvd_pressure": cvd_context,
                "volatility_regime": regime,
                "atr_14": round(curr_atr, 6)
            }
        }
        return result


def main():
    parser = argparse.ArgumentParser(description="Predict 1m Action & Dynamic TP/SL using ML Trading Model.")
    parser.add_argument("--symbol", type=str, default="TRUMPUSDT", help="Trading Symbol (e.g. TRUMPUSDT, DOGEUSDT)")
    parser.add_argument("--model-path", type=str, default=None, help="Path to saved model bundle")
    parser.add_argument("--start", type=str, default="2026-08-20", help="Recent start date for warmup")
    parser.add_argument("--end", type=str, default="2026-08-31", help="End date for latest candle")
    args = parser.parse_args()

    predictor = Predictor(symbol=args.symbol, model_path=args.model_path)

    # Load recent data for inference
    print(f"[Predictor] Fetching recent candles for {args.symbol} ({args.start} to {args.end})...")
    df_ohlcv = load_ohlcv_range(args.symbol, args.start, args.end)
    df_of = build_orderflow_features_range(args.symbol, args.start, args.end, auto_download=False)

    signal = predictor.predict_from_dataframe(df_ohlcv, df_of)
    print("\n" + "=" * 60)
    print("[SIGNAL] LATEST 1-MINUTE ML TRADING RECOMMENDATION")
    print("=" * 60)
    print(json.dumps(signal, indent=2))
    print("=" * 60)


if __name__ == "__main__":
    main()
