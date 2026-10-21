"""
Strategies Module for No-Stop-Loss Backtesting Suite
===================================================
Implements institutional strategies exposing a common run_strategy interface:
1. EMA-Cross (9/20) - Fast/Slow Exponential Moving Average crossover.
2. RSI-Momentum - Conventional (Mean-Reversion) and Trend-Following variants.
3. Order-Block + Demand (OB/Demand) - Reuses Vivek Yadav Order Block detection.

All strategies output:
- entry timestamp (ms)
- entry price
- direction ("LONG" or "SHORT")
- optional initial take-profit level (for "strategy" TP rule)
- candle index
"""

from __future__ import annotations
import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

# Ensure repository root is on sys.path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


@dataclass
class Candle:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time_ms: int


@dataclass
class StrategySignal:
    entry_time_ms: int
    entry_price: float
    direction: str          # "LONG" or "SHORT"
    initial_tp: Optional[float] = None
    candle_idx: int = 0
    exit_signal_idx: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def compute_ema(series: np.ndarray, period: int) -> np.ndarray:
    """Computes Exponential Moving Average with smoothing alpha = 2 / (period + 1)."""
    n = len(series)
    ema = np.zeros(n)
    if n == 0:
        return ema
    if n < period:
        ema[:] = series
        return ema

    alpha = 2.0 / (period + 1.0)
    # Initialize with SMA of first `period` bars
    ema[period - 1] = np.mean(series[:period])
    for i in range(period - 1):
        ema[i] = series[i]
        
    for i in range(period, n):
        ema[i] = series[i] * alpha + ema[i - 1] * (1.0 - alpha)
        
    return ema


def compute_atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> np.ndarray:
    """Computes Average True Range (Wilder smoothing)."""
    n = len(closes)
    atr = np.zeros(n)
    if n < 2:
        return atr
        
    tr = np.zeros(n)
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        hl = highs[i] - lows[i]
        hpc = abs(highs[i] - closes[i - 1])
        lpc = abs(lows[i] - closes[i - 1])
        tr[i] = max(hl, hpc, lpc)
        
    if n < period:
        atr[:] = tr
        return atr
        
    atr[period - 1] = np.mean(tr[:period])
    alpha = 1.0 / period
    for i in range(period, n):
        atr[i] = tr[i] * alpha + atr[i - 1] * (1.0 - alpha)
        
    return atr


def compute_rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    """Computes standard Relative Strength Index (RSI)."""
    n = len(closes)
    rsi = np.full(n, 50.0)
    if n <= period:
        return rsi

    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0.0:
        rsi[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi[period] = 100.0 - (100.0 / (1.0 + rs))

    for i in range(period + 1, n):
        gain = gains[i - 1]
        loss = losses[i - 1]
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0.0:
            rsi[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))

    return rsi


# ─────────────────────────────────────────────────────────────
# 1. EMA-Cross (9/20) Strategy
# ─────────────────────────────────────────────────────────────

def run_ema_cross_strategy(
    candles: List[Candle],
    direction: str = "both",
    fast_period: int = 9,
    slow_period: int = 20,
    **kwargs
) -> List[StrategySignal]:
    """
    Generates signals when EMA-9 crosses EMA-20:
    - Golden Cross (EMA9 > EMA20): LONG entry
    - Death Cross (EMA9 < EMA20): SHORT entry
    Initial TP: entry +- 2.0 * ATR14 (or 1.5% if ATR is narrow).
    """
    if len(candles) < slow_period + 2:
        return []

    closes = np.array([c.close for c in candles], dtype=float)
    highs = np.array([c.high for c in candles], dtype=float)
    lows = np.array([c.low for c in candles], dtype=float)

    ema_fast = compute_ema(closes, fast_period)
    ema_slow = compute_ema(closes, slow_period)
    atr = compute_atr(highs, lows, closes, period=14)

    signals: List[StrategySignal] = []
    dir_clean = direction.lower().strip()

    # Track signals chronologically
    for i in range(slow_period, len(candles) - 1):
        prev_diff = ema_fast[i - 1] - ema_slow[i - 1]
        curr_diff = ema_fast[i] - ema_slow[i]
        
        # Golden Cross
        if prev_diff <= 0.0 and curr_diff > 0.0:
            if dir_clean in ("both", "long"):
                entry_px = candles[i + 1].open
                # Initial TP = entry + max(2 * ATR, 1.5%)
                eff_atr = atr[i] if atr[i] > 0 else (entry_px * 0.01)
                initial_tp = entry_px + max(2.0 * eff_atr, entry_px * 0.015)
                sig = StrategySignal(
                    entry_time_ms=candles[i + 1].open_time_ms,
                    entry_price=entry_px,
                    direction="LONG",
                    initial_tp=initial_tp,
                    candle_idx=i + 1,
                    metadata={"ema_fast": ema_fast[i], "ema_slow": ema_slow[i], "atr": eff_atr}
                )
                signals.append(sig)

        # Death Cross
        elif prev_diff >= 0.0 and curr_diff < 0.0:
            if dir_clean in ("both", "short"):
                entry_px = candles[i + 1].open
                eff_atr = atr[i] if atr[i] > 0 else (entry_px * 0.01)
                initial_tp = entry_px - max(2.0 * eff_atr, entry_px * 0.015)
                sig = StrategySignal(
                    entry_time_ms=candles[i + 1].open_time_ms,
                    entry_price=entry_px,
                    direction="SHORT",
                    initial_tp=initial_tp,
                    candle_idx=i + 1,
                    metadata={"ema_fast": ema_fast[i], "ema_slow": ema_slow[i], "atr": eff_atr}
                )
                signals.append(sig)

    return signals


# ─────────────────────────────────────────────────────────────
# 2. RSI-Momentum Strategy (Conventional & Trend-Following)
# ─────────────────────────────────────────────────────────────

def run_rsi_momentum_strategy(
    candles: List[Candle],
    direction: str = "both",
    rsi_variant: str = "conventional",
    period: int = 14,
    trend_ema_period: int = 50,
    **kwargs
) -> List[StrategySignal]:
    """
    Implements two RSI Momentum variants:
    1. conventional:
       - Sell when RSI > 70 (overbought) -> SHORT
       - Buy when RSI < 30 (oversold) -> LONG
    2. trend-following:
       - Buy when RSI >= 70 AND price > EMA-50 (strong bull momentum) -> LONG
       - Sell when RSI <= 30 AND price < EMA-50 (strong bear momentum) -> SHORT
    """
    if len(candles) < max(period, trend_ema_period) + 2:
        return []

    closes = np.array([c.close for c in candles], dtype=float)
    highs = np.array([c.high for c in candles], dtype=float)
    lows = np.array([c.low for c in candles], dtype=float)

    rsi = compute_rsi(closes, period=period)
    ema_trend = compute_ema(closes, trend_ema_period)
    atr = compute_atr(highs, lows, closes, period=14)

    signals: List[StrategySignal] = []
    dir_clean = direction.lower().strip()
    variant = rsi_variant.lower().strip()
    is_trend_following = "trend" in variant

    start_idx = max(period, trend_ema_period)
    
    for i in range(start_idx, len(candles) - 1):
        c_curr = candles[i]
        c_next = candles[i + 1]
        entry_px = c_next.open
        eff_atr = atr[i] if atr[i] > 0 else (entry_px * 0.01)

        if not is_trend_following:
            # Conventional Mean-Reversion:
            # Buy when RSI crosses below 30 or turns up from < 30
            if (rsi[i - 1] >= 30.0 and rsi[i] < 30.0) or (rsi[i - 1] < 30.0 and rsi[i] >= 30.0):
                if dir_clean in ("both", "long"):
                    initial_tp = entry_px + max(2.0 * eff_atr, entry_px * 0.015)
                    sig = StrategySignal(
                        entry_time_ms=c_next.open_time_ms,
                        entry_price=entry_px,
                        direction="LONG",
                        initial_tp=initial_tp,
                        candle_idx=i + 1,
                        metadata={"rsi": rsi[i], "variant": "conventional"}
                    )
                    signals.append(sig)

            # Sell when RSI crosses above 70 or turns down from > 70
            elif (rsi[i - 1] <= 70.0 and rsi[i] > 70.0) or (rsi[i - 1] > 70.0 and rsi[i] <= 70.0):
                if dir_clean in ("both", "short"):
                    initial_tp = entry_px - max(2.0 * eff_atr, entry_px * 0.015)
                    sig = StrategySignal(
                        entry_time_ms=c_next.open_time_ms,
                        entry_price=entry_px,
                        direction="SHORT",
                        initial_tp=initial_tp,
                        candle_idx=i + 1,
                        metadata={"rsi": rsi[i], "variant": "conventional"}
                    )
                    signals.append(sig)

        else:
            # Trend-Following Momentum:
            # Buy when RSI >= 70 and Price > EMA-50 (Strong Up-Trend Momentum)
            if rsi[i] >= 70.0 and rsi[i - 1] < 70.0 and c_curr.close > ema_trend[i]:
                if dir_clean in ("both", "long"):
                    initial_tp = entry_px + max(2.0 * eff_atr, entry_px * 0.020)
                    sig = StrategySignal(
                        entry_time_ms=c_next.open_time_ms,
                        entry_price=entry_px,
                        direction="LONG",
                        initial_tp=initial_tp,
                        candle_idx=i + 1,
                        metadata={"rsi": rsi[i], "trend_ema": ema_trend[i], "variant": "trend_following"}
                    )
                    signals.append(sig)

            # Sell when RSI <= 30 and Price < EMA-50 (Strong Down-Trend Momentum)
            elif rsi[i] <= 30.0 and rsi[i - 1] > 30.0 and c_curr.close < ema_trend[i]:
                if dir_clean in ("both", "short"):
                    initial_tp = entry_px - max(2.0 * eff_atr, entry_px * 0.020)
                    sig = StrategySignal(
                        entry_time_ms=c_next.open_time_ms,
                        entry_price=entry_px,
                        direction="SHORT",
                        initial_tp=initial_tp,
                        candle_idx=i + 1,
                        metadata={"rsi": rsi[i], "trend_ema": ema_trend[i], "variant": "trend_following"}
                    )
                    signals.append(sig)

    return signals


# ─────────────────────────────────────────────────────────────
# 3. Order-Block + Demand (OB/Demand) Strategy
# ─────────────────────────────────────────────────────────────

def run_ob_demand_strategy(
    candles: List[Candle],
    direction: str = "both",
    symbol: str = "BTCUSDT",
    pivot_len: int = 5,
    **kwargs
) -> List[StrategySignal]:
    """
    Reuses existing institutional Order Block & Demand logic from repository:
    Detects Swing Points, Market Structure Break (BOS), Bullish/Bearish Order Blocks,
    and mitigation entry triggers with 1:2 risk-reward take-profit levels.
    """
    if len(candles) < 20:
        return []

    try:
        from strategies.order_block_demand import OrderBlockDemandStrategy
        
        # Mock minimal BacktestMarket for instantiation
        class MinimalMarket:
            def __init__(self, cs: List[Candle]):
                self.cs = cs
            def get_klines(self, s, interval="1h", limit=120):
                return [(c.open_time_ms, c.open, c.high, c.low, c.close, c.volume) for c in self.cs]
            def get_contract_detail(self, s):
                class DummyContract:
                    price_unit = 0.01
                    price_precision = 2
                    taker_fee_rate = 0.00045
                    maker_fee_rate = 0.00015
                return DummyContract()
                
        ob_strat = OrderBlockDemandStrategy(
            market=MinimalMarket(candles),
            symbol=symbol,
            pivot_len=pivot_len,
            risk_reward_ratio=2.0,
            auto_start_feed=False
        )

        timestamps = [c.open_time_ms for c in candles]
        opens = [c.open for c in candles]
        highs = [c.high for c in candles]
        lows = [c.low for c in candles]
        closes = [c.close for c in candles]

        drawn_zones, drawn_trades = ob_strat.calc_indicator_zones_and_trades(
            timestamps=timestamps,
            opens=opens,
            highs=highs,
            lows=lows,
            closes=closes,
            pivot_len=pivot_len
        )

        signals: List[StrategySignal] = []
        dir_clean = direction.lower().strip()

        for t in drawn_trades:
            trade_type = str(t.get("type", "")).upper()
            start_idx = int(t.get("start_idx", 0))
            if start_idx >= len(candles):
                continue
                
            entry_px = float(t.get("entry", candles[start_idx].close))
            tp_px = float(t.get("tp", entry_px * 1.02))

            if trade_type == "LONG" and dir_clean in ("both", "long"):
                sig = StrategySignal(
                    entry_time_ms=candles[start_idx].open_time_ms,
                    entry_price=entry_px,
                    direction="LONG",
                    initial_tp=tp_px,
                    candle_idx=start_idx,
                    metadata={"zone": getattr(t.get("zone"), "zone_id", "OB_BULL")}
                )
                signals.append(sig)
            elif trade_type == "SHORT" and dir_clean in ("both", "short"):
                sig = StrategySignal(
                    entry_time_ms=candles[start_idx].open_time_ms,
                    entry_price=entry_px,
                    direction="SHORT",
                    initial_tp=tp_px,
                    candle_idx=start_idx,
                    metadata={"zone": getattr(t.get("zone"), "zone_id", "OB_BEAR")}
                )
                signals.append(sig)

        return signals

    except Exception as e:
        print(f"[!] Warning in OB/Demand calculation: {e}. Falling back to swing OB logic.")
        # Fallback to local swing structure OB detector if class import fails
        return _fallback_swing_ob_signals(candles, direction, pivot_len)


def _fallback_swing_ob_signals(
    candles: List[Candle],
    direction: str = "both",
    pivot_len: int = 5
) -> List[StrategySignal]:
    """Lightweight pure-python swing pivot order block signal generator."""
    n = len(candles)
    signals: List[StrategySignal] = []
    dir_clean = direction.lower().strip()
    if n < pivot_len * 2 + 5:
        return signals

    highs = np.array([c.high for c in candles])
    lows = np.array([c.low for c in candles])
    closes = np.array([c.close for c in candles])

    for i in range(pivot_len * 2, n - 1):
        # Bullish swing low test
        is_swing_low = True
        for k in range(1, pivot_len + 1):
            if lows[i - pivot_len] >= lows[i - pivot_len - k] or lows[i - pivot_len] >= lows[i - pivot_len + k]:
                is_swing_low = False
                break
        if is_swing_low and dir_clean in ("both", "long"):
            entry_px = candles[i + 1].open
            sig = StrategySignal(
                entry_time_ms=candles[i + 1].open_time_ms,
                entry_price=entry_px,
                direction="LONG",
                initial_tp=entry_px * 1.015,
                candle_idx=i + 1
            )
            signals.append(sig)

    return signals


# ─────────────────────────────────────────────────────────────
# Common Strategy Interface
# ─────────────────────────────────────────────────────────────

def run_strategy(
    strategy_name: str,
    candles: List[Candle],
    direction: str = "both",
    rsi_variant: str = "conventional",
    symbol: str = "BTCUSDT",
    **kwargs
) -> List[StrategySignal]:
    """
    Common entry point for all strategy engines.
    Exposes uniform interface returning List[StrategySignal].
    """
    strat = strategy_name.lower().strip()
    if strat in ("ema_cross", "ema", "ema9_20", "crossover"):
        return run_ema_cross_strategy(candles, direction=direction, **kwargs)
    elif strat in ("rsi_momentum", "rsi", "rsi_conventional", "rsi_trend"):
        eff_variant = "trend_following" if "trend" in strat else rsi_variant
        return run_rsi_momentum_strategy(candles, direction=direction, rsi_variant=eff_variant, **kwargs)
    elif strat in ("ob_demand", "order_block_demand", "order_block", "smc"):
        return run_ob_demand_strategy(candles, direction=direction, symbol=symbol, **kwargs)
    else:
        raise ValueError(f"Unknown strategy: '{strategy_name}'. Expected one of ['ema_cross', 'rsi_momentum', 'ob_demand']")
