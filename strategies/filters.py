"""
Modular Regime & Trend Filter Pipeline
======================================
Quantitative filters and regime gates to filter out false signals,
low-liquidity chop, counter-trend entries, and adverse sessions.

Components:
- compute_atr_series: Pure-Python Wilder's Average True Range
- compute_adx_series: Pure-Python Wilder's Average Directional Index (ADX)
- BaseFilter: Abstract interface for all signal and regime filters
- HTFTrendFilter: 200 EMA macro-trend baseline gate
- ADXRegimeFilter: Volatility and trend strength chop gate
- HourlySessionFilter: UTC hourly session blacklist (dead-zone filter)
- DirectionalBiasFilter: Long-only / Short-only / Bi-directional gate
- FilterPipeline: Composite pipeline orchestrating all active filters
"""

from __future__ import annotations
import math
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from kcex.engine.models import TradeSignal, OrderDirection

from strategies.ema_crossover import compute_ema_series

logger = logging.getLogger("FilterPipeline")


# =============================================================================
# QUANTITATIVE INDICATOR SERIES CALCULATORS
# =============================================================================

def compute_atr_series(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14
) -> List[float]:
    """
    Computes Wilder's Average True Range (ATR) series:
    TR = max(high - low, abs(high - close_prev), abs(low - close_prev))
    ATR[0] = TR[0]
    ATR[i] = (ATR[i-1] * (period - 1) + TR[i]) / period  for i >= period
    Initial seed at period - 1 is the SMA of the first `period` TRs.
    """
    n = len(closes)
    if n == 0:
        return []
    if n != len(highs) or n != len(lows):
        raise ValueError("highs, lows, and closes series must have identical length")

    # 1. Compute True Range (TR)
    tr_series = [0.0] * n
    tr_series[0] = highs[0] - lows[0]
    for i in range(1, n):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        tr_series[i] = max(hl, hc, lc)

    if n < period:
        # Not enough bars for smoothed ATR; return running average of TR
        atr = [0.0] * n
        running = 0.0
        for i in range(n):
            running += tr_series[i]
            atr[i] = running / (i + 1)
        return atr

    atr_series = [0.0] * n
    # Seed: SMA of first `period` TR values
    seed_atr = sum(tr_series[:period]) / period
    for i in range(period - 1):
        atr_series[i] = sum(tr_series[:i + 1]) / (i + 1)
    atr_series[period - 1] = seed_atr

    # Wilder's smoothing for subsequent bars
    for i in range(period, n):
        atr_series[i] = (atr_series[i - 1] * (period - 1) + tr_series[i]) / period

    return atr_series


def compute_adx_series(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14
) -> Tuple[List[float], List[float], List[float]]:
    """
    Computes Wilder's Average Directional Index (ADX), +DI, and -DI:
    - +DM = (high[i] - high[i-1]) if > (low[i-1] - low[i]) and > 0 else 0
    - -DM = (low[i-1] - low[i]) if > (high[i] - high[i-1]) and > 0 else 0
    - Smooth +DM, -DM, and TR over `period` bars via Wilder's smoothing
    - +DI = 100 * (smoothed +DM / smoothed TR)
    - -DI = 100 * (smoothed -DM / smoothed TR)
    - DX = 100 * (| +DI - -DI | / (+DI + -DI))
    - ADX = Wilder smoothed DX over `period`

    Returns:
        (adx_series, plus_di_series, minus_di_series)
    """
    n = len(closes)
    if n == 0:
        return [], [], []
    if n != len(highs) or n != len(lows):
        raise ValueError("highs, lows, and closes series must have identical length")

    plus_dm = [0.0] * n
    minus_dm = [0.0] * n
    tr = [0.0] * n

    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        up_move = highs[i] - highs[i - 1]
        down_move = lows[i - 1] - lows[i]

        if up_move > down_move and up_move > 0:
            plus_dm[i] = up_move
        else:
            plus_dm[i] = 0.0

        if down_move > up_move and down_move > 0:
            minus_dm[i] = down_move
        else:
            minus_dm[i] = 0.0

        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        tr[i] = max(hl, hc, lc)

    if n < (period * 2):
        # Fallback for short series: approximate with partial sums
        zeros = [0.0] * n
        return zeros, zeros, zeros

    # Smoothed +DM, -DM, and TR using Wilder's smoothing
    smooth_plus = [0.0] * n
    smooth_minus = [0.0] * n
    smooth_tr = [0.0] * n

    smooth_plus[period - 1] = sum(plus_dm[:period])
    smooth_minus[period - 1] = sum(minus_dm[:period])
    smooth_tr[period - 1] = sum(tr[:period])

    for i in range(period, n):
        smooth_plus[i] = smooth_plus[i - 1] - (smooth_plus[i - 1] / period) + plus_dm[i]
        smooth_minus[i] = smooth_minus[i - 1] - (smooth_minus[i - 1] / period) + minus_dm[i]
        smooth_tr[i] = smooth_tr[i - 1] - (smooth_tr[i - 1] / period) + tr[i]

    # Calculate +DI, -DI, and DX
    plus_di = [0.0] * n
    minus_di = [0.0] * n
    dx = [0.0] * n

    for i in range(period - 1, n):
        tr_val = smooth_tr[i]
        if tr_val > 1e-12:
            p_di = 100.0 * (smooth_plus[i] / tr_val)
            m_di = 100.0 * (smooth_minus[i] / tr_val)
        else:
            p_di = 0.0
            m_di = 0.0

        plus_di[i] = p_di
        minus_di[i] = m_di

        di_sum = p_di + m_di
        if di_sum > 1e-12:
            dx[i] = 100.0 * (abs(p_di - m_di) / di_sum)
        else:
            dx[i] = 0.0

    # Smooth DX into ADX
    adx = [0.0] * n
    start_adx_idx = 2 * period - 1
    if n > start_adx_idx:
        seed_adx = sum(dx[period - 1:start_adx_idx + 1]) / period
        adx[start_adx_idx] = seed_adx
        for i in range(start_adx_idx + 1, n):
            adx[i] = (adx[i - 1] * (period - 1) + dx[i]) / period

    return adx, plus_di, minus_di


# =============================================================================
# BASE FILTER INTERFACE
# =============================================================================

class BaseFilter(ABC):
    """Abstract interface for all trade optimization and regime filters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the filter."""
        pass

    @property
    @abstractmethod
    def is_enabled(self) -> bool:
        """Whether the filter is actively enabled."""
        pass

    @abstractmethod
    def is_allowed(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: float
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluates whether a candidate TradeSignal is allowed to execute.

        Args:
            signal: The candidate TradeSignal.
            candles: List of historical Candle objects or dictionaries with open/high/low/close.
            current_time: Current timestamp in seconds (epoch).

        Returns:
            (True, None) if allowed, or (False, rejection_reason) if rejected.
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Exports filter parameters for reporting and analytics."""
        pass


# =============================================================================
# HIGHER TIMEFRAME 200 EMA TREND FILTER
# =============================================================================

class HTFTrendFilter(BaseFilter):
    """
    Higher Timeframe (HTF) Trend Filter (e.g. 200 EMA baseline).
    Enforces that micro-scalp entries align with the macro trend:
    - Long signals permitted ONLY when current_price >= HTF EMA.
    - Short signals permitted ONLY when current_price <= HTF EMA.
    """

    def __init__(
        self,
        enabled: bool = False,
        ema_period: int = 200,
        timeframe: str = "15m"
    ):
        self._enabled = enabled
        self.ema_period = ema_period
        self.timeframe = timeframe

    @property
    def name(self) -> str:
        return "HTFTrendFilter"

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def is_allowed(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: float
    ) -> Tuple[bool, Optional[str]]:
        if not self._enabled:
            return True, None

        if not candles:
            return True, None

        # Extract closing prices
        closes: List[float] = []
        for c in candles:
            if hasattr(c, "close"):
                closes.append(float(c.close))
            elif isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) >= 5:
                closes.append(float(c[4]))

        if len(closes) < 5:
            return True, None

        period = min(self.ema_period, len(closes))
        ema_series = compute_ema_series(closes, period)
        if not ema_series:
            return True, None

        current_price = closes[-1]
        htf_ema = ema_series[-1]

        direction_str = str(getattr(signal, "direction", "")).upper()
        is_long = "LONG" in direction_str or "BUY" in direction_str

        if is_long and current_price < htf_ema:
            return False, f"HTF Trend: Long rejected (Price {current_price:.4f} < {period} EMA {htf_ema:.4f})"

        if not is_long and current_price > htf_ema:
            return False, f"HTF Trend: Short rejected (Price {current_price:.4f} > {period} EMA {htf_ema:.4f})"

        return True, None

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "htf_trend_filter_enabled": self._enabled,
            "htf_ema_period": self.ema_period,
            "htf_timeframe": self.timeframe
        }


# =============================================================================
# ADX VOLATILITY & CHOP REGIME FILTER
# =============================================================================

class ADXRegimeFilter(BaseFilter):
    """
    Average Directional Index (ADX) Regime Filter.
    Suppresses entries during non-directional sideways chop (ADX < threshold).
    """

    def __init__(
        self,
        enabled: bool = False,
        period: int = 14,
        threshold: float = 25.0
    ):
        self._enabled = enabled
        self.period = period
        self.threshold = threshold

    @property
    def name(self) -> str:
        return "ADXRegimeFilter"

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def is_allowed(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: float
    ) -> Tuple[bool, Optional[str]]:
        if not self._enabled:
            return True, None

        if not candles or len(candles) < (self.period * 2):
            return True, None

        highs: List[float] = []
        lows: List[float] = []
        closes: List[float] = []

        for c in candles:
            if hasattr(c, "high") and hasattr(c, "low") and hasattr(c, "close"):
                highs.append(float(c.high))
                lows.append(float(c.low))
                closes.append(float(c.close))
            elif isinstance(c, dict):
                highs.append(float(c.get("high", 0.0)))
                lows.append(float(c.get("low", 0.0)))
                closes.append(float(c.get("close", 0.0)))
            elif isinstance(c, (list, tuple)) and len(c) >= 5:
                highs.append(float(c[2]))
                lows.append(float(c[3]))
                closes.append(float(c[4]))

        adx_series, _, _ = compute_adx_series(highs, lows, closes, period=self.period)
        if not adx_series:
            return True, None

        latest_adx = adx_series[-1]
        if latest_adx < self.threshold:
            return False, f"ADX Regime: Chop detected (ADX {latest_adx:.1f} < threshold {self.threshold:.1f})"

        return True, None

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "adx_filter_enabled": self._enabled,
            "adx_period": self.period,
            "adx_threshold": self.threshold
        }


# =============================================================================
# HOURLY DEAD-ZONE SESSION FILTER
# =============================================================================

class HourlySessionFilter(BaseFilter):
    """
    UTC Hourly Session Blacklist Filter.
    Blocks trade entries during known low-liquidity or erratic transition hours
    (e.g., 02:00, 03:00, 04:00, 05:00, 17:00 UTC).
    """

    def __init__(
        self,
        enabled: bool = False,
        blacklist_utc_hours: Optional[List[int]] = None
    ):
        self._enabled = enabled
        self.blacklist_utc_hours = blacklist_utc_hours or []

    @property
    def name(self) -> str:
        return "HourlySessionFilter"

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def is_allowed(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: float
    ) -> Tuple[bool, Optional[str]]:
        if not self._enabled or not self.blacklist_utc_hours:
            return True, None

        try:
            dt = datetime.fromtimestamp(current_time, tz=timezone.utc)
            hour = dt.hour
            if hour in self.blacklist_utc_hours:
                return False, f"Hourly Filter: Blocked UTC hour {hour:02d}:00 (Blacklist: {self.blacklist_utc_hours})"
        except Exception as e:
            logger.debug("Hourly filter timestamp parsing error: %s", e)

        return True, None

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "hourly_filter_enabled": self._enabled,
            "hourly_blacklist_utc": list(self.blacklist_utc_hours)
        }


# =============================================================================
# DIRECTIONAL BIAS FILTER
# =============================================================================

class DirectionalBiasFilter(BaseFilter):
    """
    Directional Bias Filter.
    Enforces trading strictly in a preferred direction (BOTH, LONG_ONLY, SHORT_ONLY).
    """

    def __init__(
        self,
        enabled: bool = False,
        direction_bias: str = "BOTH"
    ):
        self._enabled = enabled
        self.direction_bias = (direction_bias or "BOTH").upper()

    @property
    def name(self) -> str:
        return "DirectionalBiasFilter"

    @property
    def is_enabled(self) -> bool:
        return self._enabled and self.direction_bias in ("LONG_ONLY", "SHORT_ONLY")

    def is_allowed(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: float
    ) -> Tuple[bool, Optional[str]]:
        if not self.is_enabled:
            return True, None

        direction_str = str(getattr(signal, "direction", "")).upper()
        is_long = "LONG" in direction_str or "BUY" in direction_str

        if self.direction_bias == "LONG_ONLY" and not is_long:
            return False, "Directional Bias: Short rejected (Policy: LONG_ONLY)"

        if self.direction_bias == "SHORT_ONLY" and is_long:
            return False, "Directional Bias: Long rejected (Policy: SHORT_ONLY)"

        return True, None

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "direction_bias": self.direction_bias
        }


# =============================================================================
# COMPOSITE FILTER PIPELINE
# =============================================================================

class FilterPipeline:
    """
    Composite pipeline chaining multiple regime and trend filters together.
    Evaluates candidate signals sequentially and reports aggregated parameters.
    """

    def __init__(self, filters: Optional[List[BaseFilter]] = None):
        self.filters: List[BaseFilter] = filters or []

    def add_filter(self, f: BaseFilter) -> None:
        """Appends a filter to the pipeline."""
        self.filters.append(f)

    def evaluate(
        self,
        signal: TradeSignal,
        candles: List[Any],
        current_time: Optional[float] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluates a candidate signal against all active filters in the pipeline.

        Returns:
            (True, None) if all active filters allow the signal.
            (False, rejection_reason) on the first filter that rejects the signal.
        """
        now = current_time if current_time is not None else getattr(signal, "timestamp", 0.0)
        for f in self.filters:
            if f.is_enabled:
                allowed, reason = f.is_allowed(signal, candles, now)
                if not allowed:
                    return False, reason
        return True, None

    def get_parameters(self) -> Dict[str, Any]:
        """Aggregates parameter dictionaries from all filters."""
        params: Dict[str, Any] = {}
        for f in self.filters:
            params.update(f.get_parameters())
        return params

    @classmethod
    def from_config(cls, config: Any) -> FilterPipeline:
        """Factory constructor instantiating all configured filters from ExecutionConfig or BacktestConfig."""
        pipeline = cls()

        # 1. HTF Trend Filter
        htf_enabled = getattr(config, "htf_trend_filter_enabled", False)
        htf_ema = getattr(config, "htf_ema_period", 200)
        htf_tf = getattr(config, "htf_timeframe", "15m")
        pipeline.add_filter(HTFTrendFilter(enabled=htf_enabled, ema_period=htf_ema, timeframe=htf_tf))

        # 2. ADX Chop Filter
        adx_enabled = getattr(config, "adx_filter_enabled", False)
        adx_period = getattr(config, "adx_period", 14)
        adx_threshold = getattr(config, "adx_threshold", 25.0)
        pipeline.add_filter(ADXRegimeFilter(enabled=adx_enabled, period=adx_period, threshold=adx_threshold))

        # 3. Hourly Session Filter
        hourly_enabled = getattr(config, "hourly_filter_enabled", False)
        blacklist = getattr(config, "hourly_blacklist_utc", []) or []
        pipeline.add_filter(HourlySessionFilter(enabled=hourly_enabled, blacklist_utc_hours=blacklist))

        # 4. Directional Bias Filter
        dir_bias = getattr(config, "direction_bias", "BOTH")
        pipeline.add_filter(DirectionalBiasFilter(enabled=(dir_bias != "BOTH"), direction_bias=dir_bias))

        return pipeline
