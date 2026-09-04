"""
KCEX "Masterplan" Strategy & Sub-Strategy Framework
===================================================
Implements the Masterplan Strategy and its sub-strategy architecture.
Features:
- Pair fee & contract validation (supports zero-fee and standard pairs)
- Guaranteed Min-Profit TP: Entry Price + pu (Long) / Entry Price - pu (Short)
- Stop Loss: -10% Return on Equity (ROE / Margin)
- Immediate Profit Closing evaluation
- Sub-strategy cycling with 30-second cooldown
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple
from kcex.market import KCEXMarket, ContractInfo
from kcex.engine.models import (
    OrderDirection,
    TradeSignal,
    TradeOutcome,
    ExitReason,
    ExecutionConfig
)

logger = logging.getLogger("KCEXStrategy")


class BaseSubStrategy(ABC):
    """Abstract base class for all Masterplan sub-strategies."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def should_generate_signal(self, current_time: float) -> bool:
        """Determines if the sub-strategy is ready to emit a trade signal."""
        pass

    @abstractmethod
    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        """Generates the directional trade signal."""
        pass

    @abstractmethod
    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        """Callback invoked when a trade has fully closed."""
        pass

    @abstractmethod
    def get_remaining_cooldown(self, current_time: float) -> float:
        """Returns remaining cooldown time in seconds."""
        pass


    def start(self) -> None:
        """Starts any background resources (e.g. WebSocket feeds)."""
        pass

    def stop(self) -> None:
        """Stops any background resources."""
        pass

    def get_diagnostics(self) -> Dict[str, Any]:
        """Returns real-time strategy diagnostics if available."""
        return {}


class DirectionalCycleSubStrategy(BaseSubStrategy):
    """
    Sub-strategy 1: Single-direction trade cycles with a 30-second cooldown.
    Executes in a fixed direction (e.g. LONG or SHORT), waits for trade to close,
    waits cooldown_seconds (default 30s), then signals the next trade.
    """

    def __init__(
        self,
        direction: OrderDirection = OrderDirection.LONG,
        cooldown_seconds: float = 30.0,
        name: str = "DirectionalCycle"
    ):
        super().__init__(name=name)
        self.direction = direction
        self.cooldown_seconds = cooldown_seconds
        self.last_trade_closed_at: Optional[float] = None
        self.trade_in_progress: bool = False
        self.completed_trades_count: int = 0

    def should_generate_signal(self, current_time: float) -> bool:
        if self.trade_in_progress:
            return False
        if self.last_trade_closed_at is None:
            # First trade can execute immediately
            return True
        elapsed = current_time - self.last_trade_closed_at
        return elapsed >= self.cooldown_seconds

    def get_remaining_cooldown(self, current_time: float) -> float:
        if self.trade_in_progress or self.last_trade_closed_at is None:
            return 0.0
        elapsed = current_time - self.last_trade_closed_at
        remaining = self.cooldown_seconds - elapsed
        return max(0.0, remaining)

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        self.trade_in_progress = True
        return TradeSignal(
            symbol=symbol.upper(),
            direction=self.direction,
            sub_strategy_name=f"{self.name}({self.direction.value})",
            timestamp=now,
            metadata={"cycle_index": self.completed_trades_count + 1}
        )

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        self.trade_in_progress = False
        self.last_trade_closed_at = outcome.close_time or time.time()
        self.completed_trades_count += 1
        logger.info(
            "Sub-strategy %s completed trade #%d. Cooldown %ds initiated.",
            self.name,
            outcome.trade_id,
            int(self.cooldown_seconds)
        )


class MicrostructureSubStrategy(BaseSubStrategy):
    """
    Sub-strategy 2: High-Frequency Market Microstructure Entry Strategy.
    Connects to live KCEX WebSocket depth and deal streams.
    Fuses:
    1. Decay-weighted, spoof-discounted Order Book Imbalance (OBI)
    2. Trade Delta Bursts with fast/slow recency acceleration gating
    3. Multi-level Micro-Price / VAMP deviation from naive mid
    4. Confluence voting (>= 2 of 3) & adverse selection filters (iceberg veto, spread guard)

    Emits instantaneous entry signals targeting 1 to 3 pu ticks.
    """

    def __init__(
        self,
        market: KCEXMarket,
        symbol: str,
        signal_config: Optional[Any] = None,
        preferred_direction: Optional[OrderDirection] = None,
        cooldown_seconds: float = 10.0,
        auto_start_feed: bool = True,
        tp_ticks: Optional[int] = None,
        dynamic_tp: bool = False,
        name: str = "Microstructure"
    ):
        super().__init__(name=name)
        self.market = market
        self.symbol = symbol.upper()
        self.preferred_direction = preferred_direction
        self.cooldown_seconds = cooldown_seconds
        self.tp_ticks = tp_ticks
        self.dynamic_tp = dynamic_tp

        from kcex.engine.microstructure import (
            SymbolMeta,
            SignalConfig,
            MicrostructureSignalGenerator
        )
        from kcex.feed import KCEXWebSocketFeed

        # Look up contract metadata
        contract = self.market.get_contract_detail(self.symbol)
        meta = SymbolMeta(
            symbol=self.symbol,
            pu=contract.price_unit,
            cs=contract.contract_size,
            minV=contract.min_volume
        )

        if signal_config is None:
            if not dynamic_tp and tp_ticks is not None:
                cfg = SignalConfig(
                    min_target_ticks=tp_ticks,
                    max_target_ticks=tp_ticks,
                    cooldown_s=1.5
                )
            else:
                max_ticks = max(3, tp_ticks) if tp_ticks else 3
                cfg = SignalConfig(
                    min_target_ticks=1,
                    max_target_ticks=max_ticks,
                    cooldown_s=1.5
                )
        else:
            cfg = signal_config

        self.generator = MicrostructureSignalGenerator(meta=meta, config=cfg)

        depth_step = contract.depth_steps[0] if contract.depth_steps else str(contract.price_unit)
        self.feed = KCEXWebSocketFeed(
            symbol=self.symbol,
            depth_step=depth_step,
            on_depth=self._on_depth,
            on_deal=self._on_deal
        )

        self.last_trade_closed_at: Optional[float] = None
        self.trade_in_progress: bool = False
        self.completed_trades_count: int = 0

        # Seed initial orderbook and trades from REST to warm up distributions
        self._warmup_with_rest(depth_step)

        if auto_start_feed:
            self.start()

    def _warmup_with_rest(self, step: str) -> None:
        """Seeds initial distributions using REST snapshots."""
        try:
            book = self.market.get_order_book(self.symbol, step=step)
            bids = [(float(b[0]), float(b[1])) for b in book.get("bids", [])]
            asks = [(float(a[0]), float(a[1])) for a in book.get("asks", [])]
            if bids or asks:
                self.generator.on_depth(bids, asks)

            deals = self.market.get_recent_trades(self.symbol)
            for d in deals[:50]:
                p = float(d.get("p", 0.0))
                v = float(d.get("v", 0.0))
                side = "buy" if d.get("T") == 1 else "sell"
                ts = float(d.get("t", time.time() * 1000)) / 1000.0
                if p > 0:
                    self.generator.on_deal(p, v, side, ts)
            logger.info("Microstructure strategy warmed up with %d book levels and %d trades.", len(bids) + len(asks), len(deals))
        except Exception as e:
            logger.warning("REST warm-up error for %s: %s", self.symbol, e)

    def _on_depth(self, bids: List[Tuple[float, float]], asks: List[Tuple[float, float]], ts: float) -> None:
        self.generator.on_depth(bids, asks, ts)

    def _on_deal(self, price: float, volume: float, side: str, ts: float) -> None:
        self.generator.on_deal(price, volume, side, ts)

    def start(self) -> None:
        if self.feed and not self.feed.is_connected:
            self.feed.start()

    def stop(self) -> None:
        if self.feed:
            self.feed.stop()

    def should_generate_signal(self, current_time: float) -> bool:
        if self.trade_in_progress:
            return False
        if self.last_trade_closed_at is None:
            return True
        elapsed = current_time - self.last_trade_closed_at
        return elapsed >= self.cooldown_seconds

    def get_remaining_cooldown(self, current_time: float) -> float:
        if self.trade_in_progress or self.last_trade_closed_at is None:
            return 0.0
        elapsed = current_time - self.last_trade_closed_at
        remaining = self.cooldown_seconds - elapsed
        return max(0.0, remaining)

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        result = self.generator.generate(ts=now)
        if not result:
            return None

        dir_str, target_ticks, metadata = result
        dir_enum = OrderDirection.LONG if dir_str == "LONG" else OrderDirection.SHORT

        # If user explicitly preferred a single direction, discard opposite signals
        if self.preferred_direction and dir_enum != self.preferred_direction:
            return None

        self.trade_in_progress = True
        return TradeSignal(
            symbol=self.symbol,
            direction=dir_enum,
            sub_strategy_name=f"{self.name}({dir_str})",
            timestamp=now,
            metadata=metadata
        )

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        self.trade_in_progress = False
        self.last_trade_closed_at = outcome.close_time or time.time()
        self.completed_trades_count += 1
        logger.info(
            "Microstructure sub-strategy completed trade #%d. Cooldown %ds initiated.",
            outcome.trade_id,
            int(self.cooldown_seconds)
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        diag = self.generator.get_diagnostics()
        diag["feed"] = self.feed.stats if self.feed else {}
        diag["cooldown_remaining_s"] = round(self.get_remaining_cooldown(time.time()), 1)
        diag["trade_in_progress"] = self.trade_in_progress
        return diag



EMA_PRESETS: Dict[str, Dict[str, Any]] = {
    "5/13": {"fast": 5, "slow": 13, "desc": "Fibonacci Scalp (5 / 13) [Default]"},
    "9/21": {"fast": 9, "slow": 21, "desc": "Momentum / Trend Scalp (9 / 21)"},
    "3/8":  {"fast": 3, "slow": 8,  "desc": "Ultra-Fast Micro-Scalp (3 / 8)"},
}


def compute_ema_series(prices: List[float], period: int) -> List[float]:
    """
    Computes an Exponential Moving Average (EMA) series matching standard formula:
    alpha = 2 / (period + 1)
    Initial seed at index period - 1 is the SMA of the first `period` prices,
    followed by recursive smoothing: EMA[i] = Price[i] * alpha + EMA[i-1] * (1 - alpha).
    Indices 0 to period - 2 are populated with partial running SMA to preserve exact length.
    """
    if not prices:
        return []
    if period <= 1:
        return list(prices)

    n = len(prices)
    alpha = 2.0 / (period + 1.0)
    if n < period:
        res = [prices[0]]
        for p in prices[1:]:
            res.append(p * alpha + res[-1] * (1.0 - alpha))
        return res

    # Running partial averages for warmup
    res: List[float] = []
    running_sum = 0.0
    for i in range(period - 1):
        running_sum += prices[i]
        res.append(running_sum / (i + 1))

    # SMA at index period - 1
    running_sum += prices[period - 1]
    sma = running_sum / period
    res.append(sma)

    # Recursive EMA smoothing
    for p in prices[period:]:
        ema_val = p * alpha + res[-1] * (1.0 - alpha)
        res.append(ema_val)

    return res


class EMACrossoverSubStrategy(BaseSubStrategy):
    """
    Sub-strategy 3: Fast / Slow Exponential Moving Average (EMA) Crossover Strategy.
    Supports standard scalping pairs:
      - 5/13 (Default: Fibonacci Scalp)
      - 9/21 (Momentum / Intraday Trend)
      - 3/8  (Ultra-Fast Micro-Scalp)
      - Custom (Arbitrary user-defined fast/slow periods)

    Generates:
      - LONG on Golden Cross (Fast EMA crosses above Slow EMA)
      - SHORT on Death Cross (Fast EMA crosses below Slow EMA)
    Features:
      - Closed candle confirmation (prevents repainting mid-candle whipsaws)
      - Instant deduplication per bar (ensures exactly one trade per crossover event)
      - Optional background WebSocket price streaming for zero-latency monitoring
      - Real-time diagnostic metrics (Fast EMA, Slow EMA, Spread, Trend, Bar countdown)
    """

    def __init__(
        self,
        market: KCEXMarket,
        symbol: str,
        fast_period: int = 5,
        slow_period: int = 13,
        ema_preset: Optional[str] = "5/13",
        interval: str = "Min1",
        preferred_direction: Optional[OrderDirection] = None,
        cooldown_seconds: float = 10.0,
        require_closed_candle: bool = True,
        lookback_bars: int = 1,
        auto_start_feed: bool = False,
        name: str = "EMACrossover"
    ):
        super().__init__(name=name)
        self.market = market
        self.symbol = symbol.upper()
        self.interval = interval
        self.preferred_direction = preferred_direction
        self.cooldown_seconds = cooldown_seconds
        self.require_closed_candle = require_closed_candle
        self.lookback_bars = max(1, lookback_bars)

        # Resolve preset
        if ema_preset and ema_preset in EMA_PRESETS:
            self.fast_period = EMA_PRESETS[ema_preset]["fast"]
            self.slow_period = EMA_PRESETS[ema_preset]["slow"]
            self.ema_preset = ema_preset
        else:
            self.fast_period = fast_period
            self.slow_period = slow_period
            self.ema_preset = f"{fast_period}/{slow_period}"

        if self.fast_period >= self.slow_period:
            logger.warning(
                "Warning: Fast EMA (%d) >= Slow EMA (%d). Swapping to maintain fast < slow.",
                self.fast_period, self.slow_period
            )
            self.fast_period, self.slow_period = self.slow_period, self.fast_period

        self.last_trade_closed_at: Optional[float] = None
        self.trade_in_progress: bool = False
        self.completed_trades_count: int = 0

        # State tracking
        self.candles: List[Dict[str, Any]] = []
        self.last_kline_fetch_ts: float = 0.0
        self.last_signal_candle_ts: Optional[int] = None
        self.last_crossover_type: Optional[str] = None
        self.latest_deal_price: Optional[float] = None

        # Optional feed for real-time tick streaming
        self.feed = None
        if auto_start_feed:
            try:
                from kcex.feed import KCEXWebSocketFeed
                contract = self.market.get_contract_detail(self.symbol)
                depth_step = contract.depth_steps[0] if contract.depth_steps else str(contract.price_unit)
                self.feed = KCEXWebSocketFeed(
                    symbol=self.symbol,
                    depth_step=depth_step,
                    on_deal=self._on_deal
                )
                self.feed.start()
            except Exception as e:
                logger.warning("Could not start WS feed for EMA strategy: %s", e)

        # Seed initial candles
        self._refresh_klines(force=True)

    def _on_deal(self, price: float, volume: float, side: str, ts: float) -> None:
        self.latest_deal_price = price
        if not self.require_closed_candle and self.candles:
            self.candles[-1]["close"] = price

    def _refresh_klines(self, force: bool = False) -> None:
        now = time.time()
        # Rate-limit kline fetching to at most once per 1.5 seconds unless forced
        if not force and (now - self.last_kline_fetch_ts < 1.5):
            return
        try:
            bars = self.market.get_klines(self.symbol, interval=self.interval, limit=100)
            if bars and len(bars) >= 5:
                self.candles = bars
                self.last_kline_fetch_ts = now
        except Exception as e:
            logger.warning("Failed to refresh klines for %s: %s", self.symbol, e)

    def start(self) -> None:
        if self.feed and not self.feed.is_connected:
            self.feed.start()

    def stop(self) -> None:
        if self.feed:
            self.feed.stop()

    def should_generate_signal(self, current_time: float) -> bool:
        if self.trade_in_progress:
            return False
        if self.last_trade_closed_at is None:
            return True
        elapsed = current_time - self.last_trade_closed_at
        return elapsed >= self.cooldown_seconds

    def get_remaining_cooldown(self, current_time: float) -> float:
        if self.trade_in_progress or self.last_trade_closed_at is None:
            return 0.0
        elapsed = current_time - self.last_trade_closed_at
        remaining = self.cooldown_seconds - elapsed
        return max(0.0, remaining)

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        self._refresh_klines()
        min_required = max(self.slow_period + 3, 10)
        if len(self.candles) < min_required:
            logger.debug("EMA Crossover waiting for candle history (have %d, need %d)", len(self.candles), min_required)
            return None

        closes = [float(c.get("close", 0.0)) for c in self.candles]
        fast_series = compute_ema_series(closes, self.fast_period)
        slow_series = compute_ema_series(closes, self.slow_period)

        # Determine evaluation candle index
        # By default (require_closed_candle=True), candle[-1] is still forming,
        # so the latest closed candle is at index -2.
        eval_idx = len(closes) - 2 if self.require_closed_candle else len(closes) - 1
        if eval_idx < 1:
            return None

        detected_signal_dir: Optional[OrderDirection] = None
        crossover_type: Optional[str] = None
        signal_candle_ts: Optional[int] = None
        candle_close: float = closes[eval_idx]

        # Scan lookback_bars backwards for the most recent crossover
        for offset in range(self.lookback_bars):
            idx = eval_idx - offset
            if idx < 1:
                break

            prev_fast = fast_series[idx - 1]
            prev_slow = slow_series[idx - 1]
            curr_fast = fast_series[idx]
            curr_slow = slow_series[idx]

            # Bullish Golden Cross
            if prev_fast <= prev_slow and curr_fast > curr_slow:
                # Ensure current trend is still bullish at eval_idx
                if fast_series[eval_idx] > slow_series[eval_idx]:
                    detected_signal_dir = OrderDirection.LONG
                    crossover_type = "GOLDEN_CROSS"
                    signal_candle_ts = int(self.candles[idx].get("timestamp", 0))
                    candle_close = closes[idx]
                    break

            # Bearish Death Cross
            elif prev_fast >= prev_slow and curr_fast < curr_slow:
                # Ensure current trend is still bearish at eval_idx
                if fast_series[eval_idx] < slow_series[eval_idx]:
                    detected_signal_dir = OrderDirection.SHORT
                    crossover_type = "DEATH_CROSS"
                    signal_candle_ts = int(self.candles[idx].get("timestamp", 0))
                    candle_close = closes[idx]
                    break

        if not detected_signal_dir or signal_candle_ts is None:
            return None

        # Deduplication: do not trigger multiple times on the same crossover candle
        if self.last_signal_candle_ts is not None and self.last_signal_candle_ts >= signal_candle_ts:
            return None

        # Preferred direction filtering
        if self.preferred_direction and detected_signal_dir != self.preferred_direction:
            logger.debug(
                "EMA %s signal ignored due to preferred direction (%s)",
                detected_signal_dir.value,
                self.preferred_direction.value
            )
            return None

        # Lock signal
        self.last_signal_candle_ts = signal_candle_ts
        self.last_crossover_type = crossover_type
        self.trade_in_progress = True

        cur_f = fast_series[eval_idx]
        cur_s = slow_series[eval_idx]
        diff = cur_f - cur_s
        diff_pct = (diff / cur_s * 100.0) if cur_s != 0 else 0.0

        metadata = {
            "preset": self.ema_preset,
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "interval": self.interval,
            "crossover_type": crossover_type,
            "candle_timestamp": signal_candle_ts,
            "candle_close": candle_close,
            "fast_ema": cur_f,
            "slow_ema": cur_s,
            "ema_diff": diff,
            "ema_diff_pct": diff_pct
        }

        logger.info(
            "🚀 [EMA CROSSOVER SIGNAL] %s (%s) on %s %s | Fast(%d)=%.4f, Slow(%d)=%.4f (Diff: %+.4f / %+.2f%%)",
            detected_signal_dir.value,
            crossover_type,
            self.symbol,
            self.interval,
            self.fast_period,
            cur_f,
            self.slow_period,
            cur_s,
            diff,
            diff_pct
        )

        return TradeSignal(
            symbol=self.symbol,
            direction=detected_signal_dir,
            sub_strategy_name=f"{self.name}({self.ema_preset}-{detected_signal_dir.value})",
            timestamp=now,
            metadata=metadata
        )

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        self.trade_in_progress = False
        self.last_trade_closed_at = outcome.close_time or time.time()
        self.completed_trades_count += 1
        logger.info(
            "EMA sub-strategy completed trade #%d. Cooldown %ds initiated.",
            outcome.trade_id,
            int(self.cooldown_seconds)
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        now = time.time()
        fast_val = 0.0
        slow_val = 0.0
        diff = 0.0
        diff_pct = 0.0
        trend = "NEUTRAL"
        time_to_bar_close = 0.0

        if self.candles and len(self.candles) >= max(self.slow_period, 5):
            closes = [float(c.get("close", 0.0)) for c in self.candles]
            fast_series = compute_ema_series(closes, self.fast_period)
            slow_series = compute_ema_series(closes, self.slow_period)
            fast_val = fast_series[-1]
            slow_val = slow_series[-1]
            diff = fast_val - slow_val
            diff_pct = (diff / slow_val * 100.0) if slow_val != 0 else 0.0
            trend = "BULLISH" if diff > 0 else ("BEARISH" if diff < 0 else "NEUTRAL")

            span_map = {"Min1": 60, "Min5": 300, "Min15": 900, "Min30": 1800, "Min60": 3600}
            bar_span = span_map.get(self.interval, 60)
            last_ts = self.candles[-1].get("timestamp", now)
            elapsed_in_bar = now - last_ts
            time_to_bar_close = max(0.0, bar_span - elapsed_in_bar)

        return {
            "strategy": "EMA_CROSSOVER",
            "preset": self.ema_preset,
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "interval": self.interval,
            "fast_ema": fast_val,
            "slow_ema": slow_val,
            "diff": diff,
            "diff_pct": diff_pct,
            "trend": trend,
            "time_to_bar_close_s": round(time_to_bar_close, 1),
            "last_crossover": self.last_crossover_type,
            "cooldown_remaining_s": round(self.get_remaining_cooldown(now), 1),
            "trade_in_progress": self.trade_in_progress
        }



STOCH_RSI_PRESETS: Dict[str, Dict[str, Any]] = {
    "FAST_SCALP": {
        "rsi_period": 9,
        "stoch_period": 9,
        "k_period": 3,
        "d_period": 3,
        "oversold": 20.0,
        "overbought": 80.0,
        "desc": "Fast Scalp (9, 9, 3, 3) [Recommended for HFT]"
    },
    "STANDARD": {
        "rsi_period": 14,
        "stoch_period": 14,
        "k_period": 3,
        "d_period": 3,
        "oversold": 20.0,
        "overbought": 80.0,
        "desc": "Standard (14, 14, 3, 3) [Classic Swing/Trend]"
    },
    "MICRO_BURST": {
        "rsi_period": 7,
        "stoch_period": 7,
        "k_period": 3,
        "d_period": 3,
        "oversold": 15.0,
        "overbought": 85.0,
        "desc": "Micro Burst (7, 7, 3, 3) [Extreme Reversals]"
    },
}


def compute_rsi_series(prices: List[float], period: int = 14) -> List[float]:
    """
    Computes standard Relative Strength Index (RSI) series with Wilder's smoothing.
    Returns a series with length equal to len(prices).
    """
    n = len(prices)
    if n == 0:
        return []
    if n < period + 1:
        return [50.0] * n

    gains = []
    losses = []
    for i in range(1, n):
        diff = prices[i] - prices[i - 1]
        gains.append(max(0.0, diff))
        losses.append(max(0.0, -diff))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsi = [50.0] * period
    if avg_loss == 0.0:
        rsi.append(100.0 if avg_gain > 0 else 50.0)
    else:
        rs = avg_gain / avg_loss
        rsi.append(100.0 - (100.0 / (1.0 + rs)))

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0.0:
            val = 100.0 if avg_gain > 0 else 50.0
        else:
            rs = avg_gain / avg_loss
            val = 100.0 - (100.0 / (1.0 + rs))
        rsi.append(val)

    return rsi


def compute_stoch_rsi(
    prices: List[float],
    rsi_period: int = 9,
    stoch_period: int = 9,
    k_period: int = 3,
    d_period: int = 3
) -> Tuple[List[float], List[float]]:
    """
    Computes Stochastic RSI (%K and %D lines).
    Formula:
        StochRSI = (RSI - Min(RSI, stoch_period)) / (Max(RSI, stoch_period) - Min(RSI, stoch_period)) * 100
        %K = SMA(StochRSI, k_period)
        %D = SMA(%K, d_period)
    Returns:
        (k_series, d_series) with length matching len(prices).
    """
    n = len(prices)
    if n == 0:
        return [], []
    if n < rsi_period + stoch_period + k_period:
        return [50.0] * n, [50.0] * n

    rsi = compute_rsi_series(prices, rsi_period)

    stoch_raw: List[float] = []
    for i in range(len(rsi)):
        if i < stoch_period - 1:
            stoch_raw.append(50.0)
        else:
            window = rsi[i - stoch_period + 1 : i + 1]
            min_r = min(window)
            max_r = max(window)
            rng = max_r - min_r
            if rng == 0.0:
                stoch_raw.append(50.0)
            else:
                val = 100.0 * (rsi[i] - min_r) / rng
                stoch_raw.append(max(0.0, min(100.0, val)))

    # %K line: SMA of stoch_raw over k_period
    k_line: List[float] = []
    for i in range(len(stoch_raw)):
        if i < k_period - 1:
            k_line.append(sum(stoch_raw[: i + 1]) / (i + 1))
        else:
            k_line.append(sum(stoch_raw[i - k_period + 1 : i + 1]) / k_period)

    # %D line: SMA of %K line over d_period
    d_line: List[float] = []
    for i in range(len(k_line)):
        if i < d_period - 1:
            d_line.append(sum(k_line[: i + 1]) / (i + 1))
        else:
            d_line.append(sum(k_line[i - d_period + 1 : i + 1]) / d_period)

    return k_line, d_line


class StochasticRSISubStrategy(BaseSubStrategy):
    """
    Sub-strategy: Stochastic RSI Momentum & Extreme Reversal Strategy.
    Designed for fast micro-scalping / HFT on KCEX futures.
    
    Generates:
      - LONG on Bullish Cross (%K crosses above %D) originating in/exiting from Oversold (<= 20 or <= 25)
      - SHORT on Bearish Cross (%K crosses below %D) originating in/exiting from Overbought (>= 80 or >= 75)
    Features:
      - Extreme zone gating (filters out noisy whipsaws in neutral territory 30-70)
      - Closed-candle confirmation (prevents repainting mid-bar)
      - Strict per-candle deduplication
      - Real-time diagnostic metrics (%K, %D, Zone, RSI, bar countdown)
    """

    def __init__(
        self,
        market: KCEXMarket,
        symbol: str,
        rsi_period: int = 9,
        stoch_period: int = 9,
        k_period: int = 3,
        d_period: int = 3,
        oversold: float = 20.0,
        overbought: float = 80.0,
        stoch_preset: Optional[str] = "FAST_SCALP",
        interval: str = "Min1",
        preferred_direction: Optional[OrderDirection] = None,
        cooldown_seconds: float = 10.0,
        zone_filter: bool = True,
        require_closed_candle: bool = True,
        lookback_bars: int = 1,
        auto_start_feed: bool = False,
        name: str = "StochasticRSI"
    ):
        super().__init__(name=name)
        self.market = market
        self.symbol = symbol.upper()
        self.interval = interval
        self.preferred_direction = preferred_direction
        self.cooldown_seconds = cooldown_seconds
        self.zone_filter = zone_filter
        self.require_closed_candle = require_closed_candle
        self.lookback_bars = max(1, lookback_bars)

        # Resolve preset
        if stoch_preset and stoch_preset in STOCH_RSI_PRESETS:
            cfg = STOCH_RSI_PRESETS[stoch_preset]
            self.rsi_period = cfg["rsi_period"]
            self.stoch_period = cfg["stoch_period"]
            self.k_period = cfg["k_period"]
            self.d_period = cfg["d_period"]
            self.oversold = cfg["oversold"]
            self.overbought = cfg["overbought"]
            self.stoch_preset = stoch_preset
        else:
            self.rsi_period = rsi_period
            self.stoch_period = stoch_period
            self.k_period = k_period
            self.d_period = d_period
            self.oversold = oversold
            self.overbought = overbought
            self.stoch_preset = f"{rsi_period}/{stoch_period}/{k_period}/{d_period}"

        self.last_trade_closed_at: Optional[float] = None
        self.trade_in_progress: bool = False
        self.completed_trades_count: int = 0

        # State tracking
        self.candles: List[Dict[str, Any]] = []
        self.last_kline_fetch_ts: float = 0.0
        self.last_signal_candle_ts: Optional[int] = None
        self.last_crossover_type: Optional[str] = None
        self.latest_deal_price: Optional[float] = None

        # Optional feed for real-time tick streaming
        self.feed = None
        if auto_start_feed:
            try:
                from kcex.feed import KCEXWebSocketFeed
                contract = self.market.get_contract_detail(self.symbol)
                depth_step = contract.depth_steps[0] if contract.depth_steps else str(contract.price_unit)
                self.feed = KCEXWebSocketFeed(
                    symbol=self.symbol,
                    depth_step=depth_step,
                    on_deal=self._on_deal
                )
                self.feed.start()
            except Exception as e:
                logger.warning("Could not start WS feed for StochRSI strategy: %s", e)

        # Seed initial candles
        self._refresh_klines(force=True)

    def _on_deal(self, price: float, volume: float, side: str, ts: float) -> None:
        self.latest_deal_price = price
        if not self.require_closed_candle and self.candles:
            self.candles[-1]["close"] = price

    def _refresh_klines(self, force: bool = False) -> None:
        now = time.time()
        if not force and (now - self.last_kline_fetch_ts < 1.5):
            return
        try:
            bars = self.market.get_klines(self.symbol, interval=self.interval, limit=100)
            if bars and len(bars) >= 5:
                self.candles = bars
                self.last_kline_fetch_ts = now
        except Exception as e:
            logger.warning("Failed to refresh klines for %s: %s", self.symbol, e)

    def start(self) -> None:
        if self.feed and not self.feed.is_connected:
            self.feed.start()

    def stop(self) -> None:
        if self.feed:
            self.feed.stop()

    def should_generate_signal(self, current_time: float) -> bool:
        if self.trade_in_progress:
            return False
        if self.last_trade_closed_at is None:
            return True
        elapsed = current_time - self.last_trade_closed_at
        return elapsed >= self.cooldown_seconds

    def get_remaining_cooldown(self, current_time: float) -> float:
        if self.trade_in_progress or self.last_trade_closed_at is None:
            return 0.0
        elapsed = current_time - self.last_trade_closed_at
        remaining = self.cooldown_seconds - elapsed
        return max(0.0, remaining)

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        self._refresh_klines()
        min_required = self.rsi_period + self.stoch_period + self.k_period + self.d_period + 2
        if len(self.candles) < min_required:
            logger.debug("StochRSI waiting for candle history (have %d, need %d)", len(self.candles), min_required)
            return None

        closes = [float(c.get("close", 0.0)) for c in self.candles]
        k_series, d_series = compute_stoch_rsi(
            closes,
            rsi_period=self.rsi_period,
            stoch_period=self.stoch_period,
            k_period=self.k_period,
            d_period=self.d_period
        )

        eval_idx = len(closes) - 2 if self.require_closed_candle else len(closes) - 1
        if eval_idx < 1:
            return None

        detected_signal_dir: Optional[OrderDirection] = None
        crossover_type: Optional[str] = None
        signal_candle_ts: Optional[int] = None
        candle_close: float = closes[eval_idx]

        for offset in range(self.lookback_bars):
            idx = eval_idx - offset
            if idx < 1:
                break

            prev_k = k_series[idx - 1]
            prev_d = d_series[idx - 1]
            curr_k = k_series[idx]
            curr_d = d_series[idx]

            # Bullish Cross (%K crosses above %D)
            if prev_k <= prev_d and curr_k > curr_d:
                # Zone filter check: in or exiting oversold
                zone_ok = True
                if self.zone_filter:
                    zone_ok = (curr_k <= (self.oversold + 5.0)) or (curr_d <= (self.oversold + 5.0)) or (prev_k <= self.oversold)
                if zone_ok and k_series[eval_idx] > d_series[eval_idx]:
                    detected_signal_dir = OrderDirection.LONG
                    crossover_type = "BULLISH_STOCH_CROSS"
                    signal_candle_ts = int(self.candles[idx].get("timestamp", 0))
                    candle_close = closes[idx]
                    break

            # Bearish Cross (%K crosses below %D)
            elif prev_k >= prev_d and curr_k < curr_d:
                # Zone filter check: in or exiting overbought
                zone_ok = True
                if self.zone_filter:
                    zone_ok = (curr_k >= (self.overbought - 5.0)) or (curr_d >= (self.overbought - 5.0)) or (prev_k >= self.overbought)
                if zone_ok and k_series[eval_idx] < d_series[eval_idx]:
                    detected_signal_dir = OrderDirection.SHORT
                    crossover_type = "BEARISH_STOCH_CROSS"
                    signal_candle_ts = int(self.candles[idx].get("timestamp", 0))
                    candle_close = closes[idx]
                    break

        if not detected_signal_dir or signal_candle_ts is None:
            return None

        # Deduplication
        if self.last_signal_candle_ts is not None and self.last_signal_candle_ts >= signal_candle_ts:
            return None

        # Preferred direction filtering
        if self.preferred_direction and detected_signal_dir != self.preferred_direction:
            logger.debug(
                "StochRSI %s signal ignored due to preferred direction (%s)",
                detected_signal_dir.value,
                self.preferred_direction.value
            )
            return None

        # Lock signal
        self.last_signal_candle_ts = signal_candle_ts
        self.last_crossover_type = crossover_type
        self.trade_in_progress = True

        cur_k = k_series[eval_idx]
        cur_d = d_series[eval_idx]
        diff = cur_k - cur_d

        metadata = {
            "preset": self.stoch_preset,
            "rsi_period": self.rsi_period,
            "stoch_period": self.stoch_period,
            "k_period": self.k_period,
            "d_period": self.d_period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "interval": self.interval,
            "crossover_type": crossover_type,
            "candle_timestamp": signal_candle_ts,
            "candle_close": candle_close,
            "k_val": cur_k,
            "d_val": cur_d,
            "diff": diff
        }

        logger.info(
            "⚡ [STOCHASTIC RSI SIGNAL] %s (%s) on %s %s | %%K=%.1f, %%D=%.1f (Diff: %+.1f)",
            detected_signal_dir.value,
            crossover_type,
            self.symbol,
            self.interval,
            cur_k,
            cur_d,
            diff
        )

        return TradeSignal(
            symbol=self.symbol,
            direction=detected_signal_dir,
            sub_strategy_name=f"{self.name}({self.stoch_preset}-{detected_signal_dir.value})",
            timestamp=now,
            metadata=metadata
        )

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        self.trade_in_progress = False
        self.last_trade_closed_at = outcome.close_time or time.time()
        self.completed_trades_count += 1
        logger.info(
            "StochRSI sub-strategy completed trade #%d. Cooldown %ds initiated.",
            outcome.trade_id,
            int(self.cooldown_seconds)
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        now = time.time()
        k_val = 50.0
        d_val = 50.0
        diff = 0.0
        zone = "NEUTRAL"
        time_to_bar_close = 0.0

        min_req = self.rsi_period + self.stoch_period + self.k_period + 2
        if self.candles and len(self.candles) >= min_req:
            closes = [float(c.get("close", 0.0)) for c in self.candles]
            k_series, d_series = compute_stoch_rsi(
                closes,
                rsi_period=self.rsi_period,
                stoch_period=self.stoch_period,
                k_period=self.k_period,
                d_period=self.d_period
            )
            k_val = k_series[-1]
            d_val = d_series[-1]
            diff = k_val - d_val
            if k_val <= self.oversold:
                zone = "OVERSOLD"
            elif k_val >= self.overbought:
                zone = "OVERBOUGHT"
            else:
                zone = "NEUTRAL"

            span_map = {"Min1": 60, "Min5": 300, "Min15": 900, "Min30": 1800, "Min60": 3600}
            bar_span = span_map.get(self.interval, 60)
            last_ts = self.candles[-1].get("timestamp", now)
            elapsed_in_bar = now - last_ts
            time_to_bar_close = max(0.0, bar_span - elapsed_in_bar)

        return {
            "strategy": "STOCHASTIC_RSI",
            "preset": self.stoch_preset,
            "interval": self.interval,
            "k": round(k_val, 1),
            "k_val": round(k_val, 1),
            "d": round(d_val, 1),
            "d_val": round(d_val, 1),
            "diff": round(diff, 1),
            "zone": zone,
            "trend": "BULLISH" if k_val > d_val else "BEARISH",
            "oversold": self.oversold,
            "overbought": self.overbought,
            "time_to_bar_close_s": round(time_to_bar_close, 1),
            "last_crossover": self.last_crossover_type,
            "cooldown_remaining_s": round(self.get_remaining_cooldown(now), 1),
            "trade_in_progress": self.trade_in_progress
        }



class MasterplanStrategy:
    """
    Masterplan Trading Strategy.
    
    Responsibilities:
    1. Validates trading pair fee and contract configuration.
    2. Coordinates sub-strategies to generate entry signals.
    3. Calculates exact Min-Profit Take Profit price:
       - Long: Entry Price + pu
       - Short: Entry Price - pu
       where pu is the contract's tick size (price_unit).
    4. Calculates Stop Loss (by ROE, ticks, or price %).
    5. Evaluates immediate-profit conditions: if current market price is already
       better than or equal to min-profit, triggers instant market close.
    """

    def __init__(
        self,
        market: KCEXMarket,
        config: Optional[ExecutionConfig] = None,
        sub_strategy: Optional[BaseSubStrategy] = None
    ):
        self.market = market
        self.config = config or ExecutionConfig()
        if sub_strategy is not None:
            self.sub_strategy = sub_strategy
        else:
            strat_mode = getattr(self.config, "strategy_mode", "EMA_CROSSOVER") or "EMA_CROSSOVER"
            strat_upper = str(strat_mode).upper()
            if strat_upper in ("EMA", "EMA_CROSSOVER", "CROSSOVER"):
                pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction
                self.sub_strategy = EMACrossoverSubStrategy(
                    market=self.market,
                    symbol=self.config.symbol,
                    fast_period=getattr(self.config, "ema_fast", 5),
                    slow_period=getattr(self.config, "ema_slow", 13),
                    ema_preset=getattr(self.config, "ema_preset", "5/13"),
                    interval=getattr(self.config, "ema_interval", "Min1"),
                    preferred_direction=pref_dir,
                    cooldown_seconds=self.config.cooldown_seconds,
                    require_closed_candle=getattr(self.config, "ema_require_closed_candle", True)
                )
            elif strat_upper in ("STOCH_RSI", "STOCHASTIC_RSI", "STOCH"):
                pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction
                self.sub_strategy = StochasticRSISubStrategy(
                    market=self.market,
                    symbol=self.config.symbol,
                    rsi_period=getattr(self.config, "stoch_rsi_period", 9),
                    stoch_period=getattr(self.config, "stoch_period", 9),
                    k_period=getattr(self.config, "stoch_k_period", 3),
                    d_period=getattr(self.config, "stoch_d_period", 3),
                    oversold=getattr(self.config, "stoch_oversold", 20.0),
                    overbought=getattr(self.config, "stoch_overbought", 80.0),
                    stoch_preset=getattr(self.config, "stoch_preset", "FAST_SCALP"),
                    interval=getattr(self.config, "stoch_interval", "Min1"),
                    preferred_direction=pref_dir,
                    cooldown_seconds=self.config.cooldown_seconds,
                    zone_filter=getattr(self.config, "stoch_zone_filter", True),
                    require_closed_candle=getattr(self.config, "stoch_require_closed_candle", True)
                )
            elif strat_upper == "MICROSTRUCTURE":
                pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction
                self.sub_strategy = MicrostructureSubStrategy(
                    market=self.market,
                    symbol=self.config.symbol,
                    preferred_direction=pref_dir,
                    cooldown_seconds=self.config.cooldown_seconds,
                    tp_ticks=self.config.tp_ticks,
                    dynamic_tp=getattr(self.config, "dynamic_tp", False)
                )
            else:
                self.sub_strategy = DirectionalCycleSubStrategy(
                    direction=self.config.direction,
                    cooldown_seconds=self.config.cooldown_seconds
                )
        self.name = "Masterplan"

    def validate_zero_fee_pair(self, symbol: str) -> Dict[str, Any]:
        """
        Checks whether the selected symbol offers zero maker and taker fees,
        or operates under standard exchange fee tiers.
        """
        symbol_upper = symbol.upper()
        contract = self.market.get_contract_detail(symbol_upper)

        maker_fee = contract.maker_fee_rate
        taker_fee = contract.taker_fee_rate
        tier_data = {}

        # If client is authenticated, check account tier fee endpoint
        if self.market.client.config.is_authenticated:
            try:
                tier = self.market.get_account_tier_fees(symbol_upper)
                maker_fee = tier.get("makerFee", maker_fee)
                taker_fee = tier.get("takerFee", taker_fee)
                tier_data = tier
            except Exception as e:
                logger.warning("Could not query tiered_fee_rate for %s: %s", symbol_upper, e)

        is_zero_fee = (maker_fee == 0.0 and taker_fee == 0.0)
        result = {
            "symbol": symbol_upper,
            "maker_fee": maker_fee,
            "taker_fee": taker_fee,
            "is_zero_fee": is_zero_fee,
            "contract_size": contract.contract_size,
            "price_unit": contract.price_unit,
            "min_volume": contract.min_volume,
            "max_leverage": contract.max_leverage,
            "tier_data": tier_data
        }

        if not is_zero_fee:
            logger.warning(
                "Notice: Pair %s reported non-zero fees: maker=%s, taker=%s",
                symbol_upper, maker_fee, taker_fee
            )
        else:
            logger.info("Verified Zero-Fee Pair: %s (Maker: 0%%, Taker: 0%%)", symbol_upper)

        return result

    def calculate_min_profit_tp(
        self,
        direction: OrderDirection,
        entry_price: float,
        price_unit: float,
        tp_ticks: int = 1,
        precision: Optional[int] = None
    ) -> float:
        """
        Calculates the Guaranteed Min-Profit TP Price.
        For Long:  TP = Entry Price + (tp_ticks * pu)
        For Short: TP = Entry Price - (tp_ticks * pu)
        """
        if precision is None:
            try:
                contract = self.market.get_contract_detail(self.config.symbol)
                precision = contract.price_precision
            except Exception:
                precision = 4

        tick_offset = tp_ticks * price_unit
        if direction == OrderDirection.LONG:
            tp_price = entry_price + tick_offset
        else:
            tp_price = entry_price - tick_offset
        return round(tp_price, precision)

    def calculate_stop_loss(
        self,
        direction: OrderDirection,
        entry_price: float,
        leverage: int,
        sl_roe_pct: Optional[float] = None,
        sl_ticks: Optional[int] = None,
        sl_price_pct: Optional[float] = None,
        price_unit: Optional[float] = None,
        precision: Optional[int] = None
    ) -> float:
        """
        Calculates Stop Loss price supporting multiple modes:
        1. sl_ticks: Stop loss offset by integer price units (e.g. 10 ticks = 10 * pu).
        2. sl_price_pct: Stop loss by pure price change % (e.g. 0.5% = 0.005 * entry_price).
        3. sl_roe_pct (default): Stop loss by ROE % (e.g. 10.0% ROE -> price move = ROE / (100 * leverage)).
        Includes liquidation guard to ensure SL is never placed beyond liquidation price.
        """
        mmr = 0.01
        try:
            contract = self.market.get_contract_detail(self.config.symbol)
            if contract:
                if price_unit is None:
                    price_unit = contract.price_unit
                if precision is None:
                    precision = contract.price_precision
                if contract.maintenance_margin_ratio > 0:
                    mmr = contract.maintenance_margin_ratio
        except Exception:
            pass

        if price_unit is None:
            price_unit = 0.001
        if precision is None:
            precision = 4

        # 1. Determine price offset
        if sl_ticks is not None and sl_ticks > 0:
            price_offset = sl_ticks * price_unit
        elif sl_price_pct is not None and sl_price_pct > 0:
            price_offset = entry_price * (sl_price_pct / 100.0)
        else:
            effective_roe = sl_roe_pct if sl_roe_pct is not None else 10.0
            price_drop_fraction = (effective_roe / 100.0) / float(max(1, leverage))
            price_offset = entry_price * price_drop_fraction

        if direction == OrderDirection.LONG:
            sl_price = entry_price - price_offset
            # Liquidation price for Long: Entry * (1 - 1/leverage + mmr)
            approx_liq = entry_price * (1.0 - (1.0 / float(max(1, leverage))) + mmr)
            if sl_price <= approx_liq:
                # Clamp safely within 85% of liquidation distance
                clamped_sl = entry_price - (entry_price - approx_liq) * 0.85
                clamped_sl = min(clamped_sl, entry_price - price_unit)
                clamped_ticks = int(round((entry_price - clamped_sl) / price_unit))
                max_liq_ticks = (entry_price - approx_liq) / price_unit
                logger.warning(
                    f"Liquidation Guard: Requested SL {sl_price:.{precision}f} was past liq price {approx_liq:.{precision}f} "
                    f"(Total liq buffer is only ~{max_liq_ticks:.1f} ticks at {leverage}x). Clamped safely to {clamped_sl:.{precision}f} (~{clamped_ticks} ticks)."
                )
                sl_price = clamped_sl
        else:
            sl_price = entry_price + price_offset
            # Liquidation price for Short: Entry * (1 + 1/leverage - mmr)
            approx_liq = entry_price * (1.0 + (1.0 / float(max(1, leverage))) - mmr)
            if sl_price >= approx_liq:
                # Clamp safely within 85% of liquidation distance
                clamped_sl = entry_price + (approx_liq - entry_price) * 0.85
                clamped_sl = max(clamped_sl, entry_price + price_unit)
                clamped_ticks = int(round((clamped_sl - entry_price) / price_unit))
                max_liq_ticks = (approx_liq - entry_price) / price_unit
                logger.warning(
                    f"Liquidation Guard: Requested SL {sl_price:.{precision}f} was past liq price {approx_liq:.{precision}f} "
                    f"(Total liq buffer is only ~{max_liq_ticks:.1f} ticks at {leverage}x). Clamped safely to {clamped_sl:.{precision}f} (~{clamped_ticks} ticks)."
                )
                sl_price = clamped_sl

        return round(sl_price, precision)

    def is_better_than_min_profit(
        self,
        direction: OrderDirection,
        current_price: float,
        min_profit_tp_price: float,
        entry_price: Optional[float] = None
    ) -> bool:
        """
        Checks if current market/executable price is already at or better than minimum profit TP:
        - For Long:  current_price >= min_profit_tp_price (and strictly > entry_price if given)
        - For Short: current_price <= min_profit_tp_price (and strictly < entry_price if given)
        """
        if direction == OrderDirection.LONG:
            is_hit = current_price >= min_profit_tp_price
            if entry_price is not None:
                is_hit = is_hit and (current_price > entry_price)
            return is_hit
        else:
            is_hit = current_price <= min_profit_tp_price
            if entry_price is not None:
                is_hit = is_hit and (current_price < entry_price)
            return is_hit

    def get_signal(self) -> Optional[TradeSignal]:
        """Polls active sub-strategy for next entry signal."""
        return self.sub_strategy.generate_signal(self.config.symbol)

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        """Notifies sub-strategy when trade completes."""
        self.sub_strategy.on_trade_completed(outcome)

    def start(self) -> None:
        """Starts sub-strategy resources (e.g. WebSocket feeds)."""
        self.sub_strategy.start()

    def stop(self) -> None:
        """Stops sub-strategy resources."""
        self.sub_strategy.stop()

    def get_diagnostics(self) -> Dict[str, Any]:
        """Returns live sub-strategy diagnostics."""
        return self.sub_strategy.get_diagnostics()

