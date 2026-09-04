"""
Market Microstructure Entry Signal Generator
=============================================
Pure order-book / tape-based entry signal generator for ultra-short-horizon
(5-20s) micro-scalping on KCEX perpetual futures.

Three complementary market microstructure dimensions:
1. Decay-weighted, spoof-discounted multi-level Order Book Imbalance (OBI)
2. Sliding-window aggressive trade delta with a fast/slow "burst" (acceleration) gate
3. Multi-level micro-price / Volume-Adjusted Midpoint (VAMP) deviation from naive mid

Adverse-selection & risk filters:
- Wide-spread trap guard (spread/pu threshold)
- New-level spoof discount (time-weighted maturity ramp)
- Iceberg / hidden-replenishment veto on the defended level
- Single-print outlier winsorization against rolling EMA trade size
- Confluence voting (>= 2 of 3 signals must agree)
- Thread-safe state for lock-free parallel WebSocket ingestion
"""

from __future__ import annotations

import math
import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Literal, Optional, Tuple, Any

Direction = Literal["LONG", "SHORT"]
Side = Literal["buy", "sell"]          # aggressor / taker side of a trade
BookSide = Literal["bid", "ask"]


@dataclass(frozen=True)
class SymbolMeta:
    """Symbol specifications needed for microstructure calculations."""
    symbol: str
    pu: float            # tick size / price unit (e.g. 0.001)
    cs: float            # contract multiplier (underlying coins per contract)
    minV: float          # minimum order volume in contracts (e.g. 1)


@dataclass
class SignalConfig:
    # --- structural windows ---
    depth_levels: int = 10                 # top-N book levels used in OBI/VAMP
    delta_window_s: float = 2.0            # slow trade-delta window
    delta_fast_window_s: float = 0.5       # fast sub-window -> burst/recency gate
    stats_lookback: int = 300              # samples kept per rolling z-score

    # --- OBI decay weighting ---
    level_decay: float = 0.75              # weight_i = level_decay ** i

    # --- self-calibrating thresholds (z-scores, NOT raw units) ---
    obi_z_threshold: float = 1.6
    delta_z_threshold: float = 1.8
    vamp_z_threshold: float = 1.5
    min_confluence: int = 2                # how many of the 3 must agree
    min_burst_recency: float = 0.35        # frac of slow-window delta concentrated in fast window

    # --- adverse-selection filters ---
    max_spread_ticks: float = 1.5
    spoof_full_weight_after_s: float = 1.0 # book level ramps to full weight over this duration
    iceberg_replenish_ratio: float = 3.0   # traded_vol / minV at price before flagged as defended
    iceberg_veto_ttl_s: float = 2.0        # duration in seconds of defended-level veto
    outlier_trade_mult: float = 8.0        # vs EMA trade size -> winsorize print

    # --- output sizing ---
    min_target_ticks: int = 1
    max_target_ticks: int = 3

    # --- anti-overtrade ---
    cooldown_s: float = 1.5


class RollingZ:
    """
    O(1)-amortized incremental mean/std over a fixed-length rolling window.
    Turns raw microstructure values into self-calibrating z-scores so
    thresholds scale automatically across any symbol regardless of liquidity.
    """

    __slots__ = ("maxlen", "buf", "sum", "sumsq", "min_n")

    def __init__(self, maxlen: int, min_n: int = 30):
        self.maxlen = maxlen
        self.buf: Deque[float] = deque()
        self.sum = 0.0
        self.sumsq = 0.0
        self.min_n = min_n

    def push(self, x: float) -> None:
        self.buf.append(x)
        self.sum += x
        self.sumsq += x * x
        if len(self.buf) > self.maxlen:
            old = self.buf.popleft()
            self.sum -= old
            self.sumsq -= old * old

    def mean(self) -> float:
        n = len(self.buf)
        return self.sum / n if n else 0.0

    def std(self) -> float:
        n = len(self.buf)
        if n < 2:
            return 0.0
        var = max(self.sumsq / n - self.mean() ** 2, 1e-12)
        return math.sqrt(var)

    def z(self, x: float) -> float:
        if len(self.buf) < self.min_n:
            return 0.0  # insufficient samples to calibrate
        s = self.std()
        if s < 1e-9:
            return 0.0
        return (x - self.mean()) / s


class EMA:
    """Exponential moving average helper."""
    __slots__ = ("alpha", "value")

    def __init__(self, alpha: float, initial: float = 0.0):
        self.alpha = alpha
        self.value = initial

    def update(self, x: float) -> float:
        self.value = self.alpha * x + (1 - self.alpha) * self.value
        return self.value


@dataclass
class _LevelWatch:
    """Tracks how long a price level has been continuously visible."""
    first_seen: float
    size: float


@dataclass
class _DefendedLevel:
    """Tracks aggressive volume traded into best level to detect icebergs."""
    price: float
    traded_since_reset: float = 0.0
    last_size: float = 0.0
    veto_until: float = 0.0


class MicrostructureSignalGenerator:
    """
    Consumes live L2 depth frames and trade deals, maintaining rolling microstructure
    distributions and producing instantaneous (direction, target_ticks, metadata) entries.
    Thread-safe for real-time WebSocket feeds.
    """

    def __init__(self, meta: SymbolMeta, config: Optional[SignalConfig] = None):
        self.meta = meta
        self.cfg = config or SignalConfig()
        self._lock = threading.Lock()

        self.bids: List[Tuple[float, float]] = []
        self.asks: List[Tuple[float, float]] = []
        self._last_depth_ts: float = 0.0

        # rolling calibration distributions
        self._obi_stats = RollingZ(self.cfg.stats_lookback)
        self._delta_stats = RollingZ(self.cfg.stats_lookback)
        self._vamp_stats = RollingZ(self.cfg.stats_lookback)

        # trade tape buffers
        self._trades: Deque[Tuple[float, float]] = deque()   # (ts, signed_vol)
        self._trade_size_ema = EMA(alpha=0.05, initial=max(1.0, meta.minV))

        # spoof & persistence tracking, keyed by (side, price_pu_key)
        self._level_watch: Dict[Tuple[BookSide, int], _LevelWatch] = {}

        # iceberg / defended level tracking
        self._defended: Dict[BookSide, _DefendedLevel] = {
            "bid": _DefendedLevel(price=float("nan")),
            "ask": _DefendedLevel(price=float("nan")),
        }

        self._last_signal_ts: float = 0.0

    # ------------------------------------------------------------------
    # Data Ingestion
    # ------------------------------------------------------------------

    def on_depth(
        self,
        bids: List[Tuple[float, float]],
        asks: List[Tuple[float, float]],
        ts: Optional[float] = None
    ) -> None:
        """
        Ingests order book depth snapshot/delta.
        Ensures bids sorted descending and asks sorted ascending.
        """
        ts = ts if ts is not None else time.time()
        with self._lock:
            # Sort to enforce invariant: bids highest first, asks lowest first
            sorted_bids = sorted(bids, key=lambda x: x[0], reverse=True)[: self.cfg.depth_levels]
            sorted_asks = sorted(asks, key=lambda x: x[0], reverse=False)[: self.cfg.depth_levels]

            self.bids = sorted_bids
            self.asks = sorted_asks
            self._last_depth_ts = ts

            self._update_level_watch("bid", self.bids, ts)
            self._update_level_watch("ask", self.asks, ts)
            self._update_defended_level("bid", self.bids, ts)
            self._update_defended_level("ask", self.asks, ts)

    def on_deal(
        self,
        price: float,
        volume: float,
        side: Side,
        ts: Optional[float] = None
    ) -> None:
        """
        Ingests a public executed trade print.
        `side` is 'buy' (taker buyer) or 'sell' (taker seller).
        """
        ts = ts if ts is not None else time.time()
        with self._lock:
            # Winsorize single outsized prints to prevent whale anomalies from faking bursts
            avg_sz = max(self._trade_size_ema.value, self.meta.minV)
            capped_vol = min(volume, self.cfg.outlier_trade_mult * avg_sz)
            self._trade_size_ema.update(volume)

            signed = capped_vol if side == "buy" else -capped_vol
            self._trades.append((ts, signed))
            self._evict_old_trades(ts)

            # Check if this trade consumed liquidity at the current best level
            # Taker buy consumes ask liquidity; taker sell consumes bid liquidity
            if side == "sell" and self.bids and math.isclose(price, self.bids[0][0], abs_tol=self.meta.pu * 0.49):
                self._defended["bid"].traded_since_reset += capped_vol
            elif side == "buy" and self.asks and math.isclose(price, self.asks[0][0], abs_tol=self.meta.pu * 0.49):
                self._defended["ask"].traded_since_reset += capped_vol

    # ------------------------------------------------------------------
    # Internal Math & Tracking
    # ------------------------------------------------------------------

    def _update_level_watch(self, side: BookSide, levels: List[Tuple[float, float]], ts: float) -> None:
        live_keys = set()
        for price, size in levels:
            key = (side, round(price / self.meta.pu))
            live_keys.add(key)
            watch = self._level_watch.get(key)
            if watch is None:
                self._level_watch[key] = _LevelWatch(first_seen=ts, size=size)
            else:
                watch.size = size
        # Clean up vanished levels
        stale = [k for k in self._level_watch if k[0] == side and k not in live_keys]
        for k in stale:
            del self._level_watch[k]

    def _level_weight(self, side: BookSide, price: float, ts: float) -> float:
        """0..1 ramp: brand-new levels are discounted until survived spoof_full_weight_after_s."""
        key = (side, round(price / self.meta.pu))
        watch = self._level_watch.get(key)
        if watch is None:
            return 0.0
        age = ts - watch.first_seen
        return min(1.0, max(0.0, age / self.cfg.spoof_full_weight_after_s))

    def _update_defended_level(self, side: BookSide, levels: List[Tuple[float, float]], ts: float) -> None:
        d = self._defended[side]
        if not levels:
            return
        price, size = levels[0]
        if not math.isclose(price, d.price, abs_tol=self.meta.pu / 2):
            d.price, d.last_size, d.traded_since_reset, d.veto_until = price, size, 0.0, 0.0
            return

        displayed_drop = max(0.0, d.last_size - size)
        # If substantial volume traded but displayed size barely dropped -> iceberg replenishment
        if d.traded_since_reset > 0 and displayed_drop < d.traded_since_reset * 0.5:
            ratio = d.traded_since_reset / max(self.meta.minV, 1e-9)
            if ratio > self.cfg.iceberg_replenish_ratio:
                d.veto_until = ts + self.cfg.iceberg_veto_ttl_s
                d.traded_since_reset = 0.0  # Reset counter once veto is flagged

        if displayed_drop >= d.traded_since_reset * 0.9:
            d.traded_since_reset = 0.0  # level genuinely thinned out, reset counter
        d.last_size = size

    def _evict_old_trades(self, ts: float) -> None:
        cutoff = ts - self.cfg.delta_window_s
        while self._trades and self._trades[0][0] < cutoff:
            self._trades.popleft()

    def _spread_ticks(self) -> float:
        if not self.bids or not self.asks:
            return float("inf")
        return (self.asks[0][0] - self.bids[0][0]) / self.meta.pu

    def _mid(self) -> float:
        if not self.bids or not self.asks:
            return 0.0
        return (self.bids[0][0] + self.asks[0][0]) / 2.0

    def _compute_obi(self, ts: float) -> float:
        wb = wa = 0.0
        for i, (price, size) in enumerate(self.bids):
            w = (self.cfg.level_decay ** i) * self._level_weight("bid", price, ts)
            wb += w * size
        for i, (price, size) in enumerate(self.asks):
            w = (self.cfg.level_decay ** i) * self._level_weight("ask", price, ts)
            wa += w * size
        denom = wb + wa
        return (wb - wa) / denom if denom > 1e-12 else 0.0

    def _compute_delta(self, ts: float) -> Tuple[float, float]:
        self._evict_old_trades(ts)
        slow_cut = ts - self.cfg.delta_window_s
        fast_cut = ts - self.cfg.delta_fast_window_s
        slow_sum = fast_sum = 0.0
        for t, v in self._trades:
            if t >= slow_cut:
                slow_sum += v
            if t >= fast_cut:
                fast_sum += v
        recency = (abs(fast_sum) / abs(slow_sum)) if abs(slow_sum) > 1e-9 else 0.0
        return slow_sum, recency

    def _compute_vamp_deviation(self) -> float:
        bid_depth = sum(size * (self.cfg.level_decay ** i) for i, (_, size) in enumerate(self.bids))
        ask_depth = sum(size * (self.cfg.level_decay ** i) for i, (_, size) in enumerate(self.asks))
        denom = bid_depth + ask_depth
        if denom < 1e-12:
            return 0.0
        vamp = (self.bids[0][0] * ask_depth + self.asks[0][0] * bid_depth) / denom
        mid = self._mid()
        return (vamp - mid) / self.meta.pu if mid > 0 else 0.0

    # ------------------------------------------------------------------
    # Public Signal Generation & Diagnostics
    # ------------------------------------------------------------------

    def get_diagnostics(self, ts: Optional[float] = None) -> Dict[str, Any]:
        """Returns instantaneous snapshot of all microstructure metrics."""
        ts = ts if ts is not None else time.time()
        with self._lock:
            obi = self._compute_obi(ts)
            delta, recency = self._compute_delta(ts)
            vamp_dev = self._compute_vamp_deviation()
            spread = self._spread_ticks()

            return {
                "ts": ts,
                "spread_ticks": spread,
                "obi": obi,
                "obi_z": self._obi_stats.z(obi),
                "delta": delta,
                "recency": recency,
                "delta_z": self._delta_stats.z(delta),
                "vamp_dev_ticks": vamp_dev,
                "vamp_z": self._vamp_stats.z(vamp_dev),
                "defended_bid": self._defended["bid"].veto_until > ts,
                "defended_ask": self._defended["ask"].veto_until > ts,
                "trade_count_window": len(self._trades),
                "best_bid": self.bids[0][0] if self.bids else None,
                "best_ask": self.asks[0][0] if self.asks else None,
            }

    def generate(self, ts: Optional[float] = None) -> Optional[Tuple[Direction, int, Dict[str, Any]]]:
        """
        Evaluates real-time market microstructure.
        Returns:
            (Direction, target_ticks, metadata_dict) if entry signal fires, else None.
        """
        ts = ts if ts is not None else time.time()

        with self._lock:
            if ts - self._last_signal_ts < self.cfg.cooldown_s:
                return None
            if not self.bids or not self.asks:
                return None
            spread_ticks = self._spread_ticks()
            if spread_ticks > self.cfg.max_spread_ticks:
                return None

            # 1. Order Book Imbalance
            obi = self._compute_obi(ts)
            self._obi_stats.push(obi)
            obi_z = self._obi_stats.z(obi)

            # 2. Trade Delta & Burst Recency Gate
            delta, recency = self._compute_delta(ts)
            self._delta_stats.push(delta)
            delta_z = self._delta_stats.z(delta) if recency >= self.cfg.min_burst_recency else 0.0

            # 3. Micro-Price / VAMP Deviation
            vamp_dev = self._compute_vamp_deviation()
            self._vamp_stats.push(vamp_dev)
            vamp_z = self._vamp_stats.z(vamp_dev)

            # Collect votes with normalized strength
            votes: List[Tuple[str, Direction, float]] = []
            if abs(obi_z) >= self.cfg.obi_z_threshold:
                votes.append(("obi", "LONG" if obi_z > 0 else "SHORT", abs(obi_z) / self.cfg.obi_z_threshold))
            if abs(delta_z) >= self.cfg.delta_z_threshold:
                votes.append(("delta", "LONG" if delta_z > 0 else "SHORT", abs(delta_z) / self.cfg.delta_z_threshold))
            if abs(vamp_z) >= self.cfg.vamp_z_threshold:
                votes.append(("vamp", "LONG" if vamp_z > 0 else "SHORT", abs(vamp_z) / self.cfg.vamp_z_threshold))

            if not votes:
                return None

            long_votes = [v for v in votes if v[1] == "LONG"]
            short_votes = [v for v in votes if v[1] == "SHORT"]

            direction: Optional[Direction] = None
            agreeing: List[Tuple[str, Direction, float]] = []

            if len(long_votes) >= self.cfg.min_confluence and len(long_votes) > len(short_votes):
                direction, agreeing = "LONG", long_votes
            elif len(short_votes) >= self.cfg.min_confluence and len(short_votes) > len(long_votes):
                direction, agreeing = "SHORT", short_votes

            if direction is None:
                return None

            # Iceberg Veto: Don't buy into a defended ask, don't sell into a defended bid
            if direction == "LONG" and self._defended["ask"].veto_until > ts:
                return None
            if direction == "SHORT" and self._defended["bid"].veto_until > ts:
                return None

            # Dynamic Target Sizing (1 to 3 pu ticks based on excess confluence strength)
            excess = (sum(strength for _, _, strength in agreeing) / len(agreeing)) - 1.0
            excess = max(0.0, min(excess, 1.0))
            span = self.cfg.max_target_ticks - self.cfg.min_target_ticks
            target_ticks = int(round(self.cfg.min_target_ticks + span * excess))
            target_ticks = max(self.cfg.min_target_ticks, min(self.cfg.max_target_ticks, target_ticks))

            self._last_signal_ts = ts

            metadata = {
                "agreeing_signals": [k for k, _, _ in agreeing],
                "confluence_count": len(agreeing),
                "obi_z": round(obi_z, 2),
                "delta_z": round(delta_z, 2),
                "delta_recency": round(recency, 2),
                "vamp_z": round(vamp_z, 2),
                "spread_ticks": round(spread_ticks, 2),
                "target_ticks": target_ticks
            }

            return direction, target_ticks, metadata
