"""
1-Minute ML Trading Strategy Adapter for KCEX
==============================================
Bridges the Scikit-Learn HistGradientBoosting Alpha Engine (ML_1M_MODEL)
with the KCEX BaseStrategy interface.

Compatible with:
- Live Automated Trading (run_engine.py --mode live)
- Simulated Dry-Run Execution (run_engine.py --mode dry-run)
- High-Fidelity Backtesting (BACKTESTER/run_backtest.py)
- Semi-Autonomous Terminal Assistant (semi_auto_trader.py)
"""

import os
import sys
import time
import logging
from typing import Optional, Dict, Any, List
import numpy as np
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from strategies.base import BaseStrategy
from kcex.engine.models import OrderDirection, TradeSignal, TradeOutcome
from ML_1M_MODEL.config import MODELS_DIR, normalize_symbol_name, get_model_config, get_tick_spec
from ML_1M_MODEL.model import TradingModel
from ML_1M_MODEL.features import extract_features

logger = logging.getLogger("MLStrategy")


class MLStrategy(BaseStrategy):
    """
    1-Minute Machine Learning Tactical Alpha Strategy.
    
    Generates high-conviction BUY, SELL, or WAIT signals using multi-horizon
    technicals, Carter squeeze expansion, and microstructure order-flow dynamics.
    Outputs volatility-calibrated dynamic Take-Profit and Stop-Loss boundaries.
    """

    def __init__(
        self,
        market: Any,
        symbol: str = "TRUMP_USDT",
        model_path: Optional[str] = None,
        timeframe: str = "1m",
        cooldown_seconds: float = 10.0,
        warmup_candles: int = 150,
        confidence_threshold: Optional[float] = None,
        confidence_threshold_sell: Optional[float] = None,
        edge_threshold: Optional[float] = None,
        preferred_direction: Optional[OrderDirection] = None
    ):
        super().__init__(name="ML_1M_MODEL")
        self.market = market
        self.symbol = symbol
        self.clean_symbol = normalize_symbol_name(symbol)
        self.timeframe = timeframe
        self.cooldown_seconds = cooldown_seconds
        self.warmup_candles = warmup_candles
        self.preferred_direction = preferred_direction

        self.last_trade_time: float = 0.0
        self.trade_in_progress: bool = False
        self.last_prediction: Optional[Dict[str, Any]] = None

        # Resolve model path
        if model_path is None:
            model_path = os.path.join(MODELS_DIR, f"ml_1m_model_{self.clean_symbol.lower()}.pkl")
            if not os.path.exists(model_path):
                alt_path = os.path.join(MODELS_DIR, f"ml_1m_model_{self.symbol.lower()}.pkl")
                if os.path.exists(alt_path):
                    model_path = alt_path

        self.model_path = model_path
        self.model: Optional[TradingModel] = None
        self._load_model()

        # Apply runtime threshold overrides if provided
        if self.model and self.model.cfg:
            if confidence_threshold is not None:
                self.model.cfg.confidence_threshold = confidence_threshold
            if confidence_threshold_sell is not None:
                self.model.cfg.confidence_threshold_sell = confidence_threshold_sell
            if edge_threshold is not None:
                self.model.cfg.edge_threshold = edge_threshold

    def _load_model(self) -> None:
        """Loads serialized model artifact from disk."""
        if os.path.exists(self.model_path):
            try:
                self.model = TradingModel.load(self.model_path)
                logger.info(
                    f"[MLStrategy] Loaded ML model for {self.clean_symbol} from {self.model_path}"
                )
            except Exception as e:
                logger.error(f"[MLStrategy] Error loading model bundle from {self.model_path}: {e}")
                self.model = None
        else:
            logger.warning(
                f"[MLStrategy] Model artifact not found at {self.model_path}. Signals will remain paused until model is trained."
            )
            self.model = None

    def should_generate_signal(self, current_time: float) -> bool:
        """Checks whether the strategy is permitted to emit a signal."""
        if self.trade_in_progress:
            return False
        if (current_time - self.last_trade_time) < self.cooldown_seconds:
            return False
        if self.model is None or not self.model.is_trained:
            return False
        return True

    def get_remaining_cooldown(self, current_time: float) -> float:
        """Returns remaining cooldown time in seconds."""
        elapsed = current_time - self.last_trade_time
        return max(0.0, self.cooldown_seconds - elapsed)

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        """
        Polls recent 1-minute klines from market feed, extracts features,
        evaluates directional probability, and returns a TradeSignal if actionable.
        """
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        # Fetch recent candles for feature warmup
        raw_candles = self.market.get_klines(symbol, interval="Min1", limit=300)
        if not raw_candles or len(raw_candles) < min(self.warmup_candles, 50):
            logger.debug(f"[MLStrategy] Insufficient candles for warmup ({len(raw_candles) if raw_candles else 0}).")
            return None

        # Parse candles to standardized DataFrame
        records = []
        for c in raw_candles:
            if isinstance(c, dict):
                ts = int(c.get("open_time", c.get("timestamp", c.get("time", 0))))
                o = float(c.get("open", 0.0))
                h = float(c.get("high", 0.0))
                l = float(c.get("low", 0.0))
                cl = float(c.get("close", 0.0))
                vol = float(c.get("volume", c.get("vol", 0.0)))
                tbv = float(c.get("taker_buy_volume", c.get("taker_buy_vol", vol * 0.5)))
            else:
                # Support dataclass object (e.g. BACKTESTER Candle)
                ts = int(getattr(c, "open_time_ms", getattr(c, "timestamp", 0)))
                o = float(getattr(c, "open", 0.0))
                h = float(getattr(c, "high", 0.0))
                l = float(getattr(c, "low", 0.0))
                cl = float(getattr(c, "close", 0.0))
                vol = float(getattr(c, "volume", 0.0))
                tbv = float(getattr(c, "taker_buy_volume", vol * 0.5))

            records.append({
                "timestamp": ts,
                "open": o,
                "high": h,
                "low": l,
                "close": cl,
                "volume": vol,
                "taker_buy_volume": tbv
            })

        df_ohlcv = pd.DataFrame(records).drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
        if len(df_ohlcv) < 50:
            return None

        # Feature Extraction using official pipeline
        try:
            df_feats, _ = extract_features(df_ohlcv, df_orderflow=None)
        except Exception as e:
            logger.error(f"[MLStrategy] Error extracting features: {e}")
            return None

        latest_idx = len(df_feats) - 1
        latest_row = df_feats.iloc[[latest_idx]]
        curr_price = float(df_ohlcv["close"].iloc[latest_idx])
        curr_atr = float(df_feats["atr_14"].iloc[latest_idx])

        # Model Inference
        try:
            decisions = self.model.predict_decision(
                X=latest_row,
                current_prices=np.array([curr_price]),
                current_atrs=np.array([curr_atr]),
                symbol=self.clean_symbol
            )
            dec = decisions[0]
            self.last_prediction = dec
        except Exception as e:
            logger.error(f"[MLStrategy] Prediction execution error: {e}")
            return None

        action = dec["action"]
        confidence = dec["confidence"]

        # Periodic ML Radar Telemetry Logging (every 4s when scanning)
        if not hasattr(self, "_last_radar_log_time"):
            self._last_radar_log_time = 0.0
        if now - self._last_radar_log_time >= 4.0:
            self._last_radar_log_time = now
            p_buy = dec["prob_buy"]
            p_sell = dec["prob_sell"]
            p_wait = dec["prob_wait"]
            thresh_buy = getattr(self.model.cfg, "confidence_threshold", 0.38)
            thresh_sell = getattr(self.model.cfg, "confidence_threshold_sell", thresh_buy)
            pu = getattr(self.market, "get_tick_size", lambda s: 0.001)(symbol)
            atr_ticks = (curr_atr / pu) if pu > 0 else 0
            logger.info(
                f"[ML RADAR] {symbol} Price: {curr_price:.4f} USDT | ATR(14): {curr_atr:.4f} ({atr_ticks:.1f}t) | "
                f"P(BUY): {p_buy:.1%} [T:{thresh_buy:.1%}] | P(SELL): {p_sell:.1%} [T:{thresh_sell:.1%}] | "
                f"P(WAIT): {p_wait:.1%} | Action: {action}"
            )

        # Apply preferred direction lock if configured
        if self.preferred_direction is not None:
            if self.preferred_direction == OrderDirection.LONG and action == "SELL":
                return None
            if self.preferred_direction == OrderDirection.SHORT and action == "BUY":
                return None

        if action in ("BUY", "SELL"):
            direction = OrderDirection.LONG if action == "BUY" else OrderDirection.SHORT
            tp_ticks = dec["tp_ticks"]
            sl_ticks = dec["sl_ticks"]
            pu = getattr(self.market, "get_tick_size", lambda s: 0.001)(symbol)

            metadata = {
                "target_ticks": tp_ticks,
                "target_sl_ticks": sl_ticks,
                "suggested_tp": dec["suggested_tp"],
                "suggested_sl": dec["suggested_sl"],
                "tp_price_exact": dec.get("tp_price_exact", dec["suggested_tp"]),
                "sl_price_exact": dec.get("sl_price_exact", dec["suggested_sl"]),
                "confidence": confidence,
                "prob_buy": dec["prob_buy"],
                "prob_sell": dec["prob_sell"],
                "prob_wait": dec["prob_wait"],
                "risk_reward_ratio": dec["risk_reward_ratio"],
                "atr_14": round(curr_atr, 6),
                "entry_price": curr_price,
                "model_action": action,
                "strategy": "ML_1M_MODEL"
            }

            self.trade_in_progress = True
            sig = TradeSignal(
                symbol=symbol,
                direction=direction,
                sub_strategy_name="ML_1M_MODEL",
                timestamp=now,
                metadata=metadata
            )
            logger.info(
                f"==============================================================================\n"
                f"🔥 [ML ALPHA TRIGGER] HIGH-CONVICTION {action} SIGNAL DETECTED 🔥\n"
                f"   • Conviction     : {confidence:.1%} (P({action})={confidence:.1%} vs P(WAIT)={dec['prob_wait']:.1%})\n"
                f"   • Reference Price: {curr_price:.4f} USDT | 1m ATR = {curr_atr:.4f} USDT ({(curr_atr / pu if pu > 0 else 0):.1f} ticks)\n"
                f"   • Dynamic Target : TP = {dec['suggested_tp']} (+{tp_ticks} ticks / ~{getattr(self.model.cfg, 'tp_atr_mult', 1.9):.1f}x ATR)\n"
                f"   • Dynamic Stop   : SL = {dec['suggested_sl']} (-{sl_ticks} ticks / ~{getattr(self.model.cfg, 'sl_atr_mult', 1.0):.1f}x ATR)\n"
                f"   • Reward / Risk  : {dec['risk_reward_ratio']} : 1 | Horizon = {getattr(self.model.cfg, 'horizon_bars', 5)} bars (5m)\n"
                f"=============================================================================="
            )
            return sig

        return None

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        """Callback invoked when position closes."""
        self.trade_in_progress = False
        self.last_trade_time = outcome.close_time if outcome.close_time > 0 else time.time()
        logger.info(
            f"[MLStrategy] Trade #{outcome.trade_id} closed [{outcome.exit_reason.value}]. "
            f"PnL: {outcome.realized_pnl_usdt:+.4f} USDT ({outcome.roe_percentage:+.2f}% ROE). Engaging cooldown ({self.cooldown_seconds}s)."
        )

    def on_trade_rejected(self) -> None:
        """Callback invoked when signal was rejected or suppressed by a filter."""
        self.trade_in_progress = False

    def get_parameters(self) -> Dict[str, Any]:
        """Returns strategy hyperparameters for reporting."""
        params = {
            "strategy": self.name,
            "symbol": self.symbol,
            "clean_symbol": self.clean_symbol,
            "timeframe": self.timeframe,
            "cooldown_seconds": self.cooldown_seconds,
            "warmup_candles": self.warmup_candles,
            "model_path": self.model_path,
            "model_loaded": (self.model is not None and self.model.is_trained)
        }
        if self.model and self.model.cfg:
            params.update({
                "horizon_bars": self.model.cfg.horizon_bars,
                "tp_atr_mult": self.model.cfg.tp_atr_mult,
                "sl_atr_mult": self.model.cfg.sl_atr_mult,
                "confidence_threshold": self.model.cfg.confidence_threshold,
                "confidence_threshold_sell": getattr(self.model.cfg, "confidence_threshold_sell", self.model.cfg.confidence_threshold),
                "edge_threshold": self.model.cfg.edge_threshold
            })
        return params

    def get_diagnostics(self) -> Dict[str, Any]:
        """Returns real-time diagnostics and latest prediction probabilities."""
        diag = {
            "strategy": self.name,
            "symbol": self.symbol,
            "trade_in_progress": self.trade_in_progress,
            "model_loaded": (self.model is not None and self.model.is_trained),
            "remaining_cooldown_sec": round(self.get_remaining_cooldown(time.time()), 1),
            "last_prediction": self.last_prediction
        }
        return diag


# Standard alias
MLSubStrategy = MLStrategy
