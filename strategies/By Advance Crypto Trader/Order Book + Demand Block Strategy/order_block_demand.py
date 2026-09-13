"""
Order Block + Demand/Supply Block Trading Strategy
===================================================
Designed from the Masterclasses of Vivek Yadav (Advance Crypto Trader):
1. 'Order Block Strategy' (SMC: Opposite origin candle, 2-3+ continuous impulse candles,
   full wick-to-wick OB range, retest tap + rejection wick, next-candle confirmation close, 1:2 RR)
2. 'Demand and Supply Trading Strategy' (3-5 consecutive impulse candles, FVG/imbalance, extrema location,
   approach weakness, rejection wick, confirmation candle close, safe zone SL)

Key Architecture & Rules:
- Pure-Python rolling fractal swing & displacement detection.
- Order Block Discovery: Identifies the opposite candle (full wick-to-wick range: body + wick)
  immediately preceding a strong movement of 2-3 or more consecutive impulse candles.
- Deduplication & Anti-Recreation Memory: Tracks resolved origin timestamps so mitigated,
  invalidated, or expired zones are never re-created or repeatedly traded.
- Retest & Rejection Wick Engine (Candle T): Verifies that price returns to touch the zone
  and forms a prominent rejection wick (lower wick for bullish, upper wick for bearish)
  without closing with a solid body beyond the zone boundary.
- Confirmation Candle Close Engine (Candle T+1): Validates that the next candle closes in
  the direction of the trade (Green for bullish, Red for bearish) confirming institutional defense.
- Dynamic 1:2 Risk-to-Reward Geometry: Calculates exact SL ticks behind zone boundary + buffer ticks,
  and projects 1:2 R:R TP ticks (with 1:1 partial exit and Breakeven lock for multi-contract trades).
"""

from __future__ import annotations
import math
import time
import logging
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple, Set, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from kcex.market import KCEXMarket

from kcex.engine.models import OrderDirection, TradeSignal, TradeOutcome
from strategies.base import BaseStrategy

logger = logging.getLogger("OrderBlockDemandStrategy")


class ZoneType(str, Enum):
    BULLISH_ORDER_BLOCK = "BULLISH_ORDER_BLOCK"
    BEARISH_ORDER_BLOCK = "BEARISH_ORDER_BLOCK"
    DEMAND_BLOCK = "DEMAND_BLOCK"
    SUPPLY_BLOCK = "SUPPLY_BLOCK"
    CONFLUENT_DEMAND_OB = "CONFLUENT_DEMAND_OB"
    CONFLUENT_SUPPLY_OB = "CONFLUENT_SUPPLY_OB"


class ZoneStatus(str, Enum):
    ACTIVE = "ACTIVE"              # Created, waiting for retest
    TESTED = "TESTED"              # Tapped zone and formed rejection wick (Candle T)
    CONFIRMED = "CONFIRMED"        # Directional confirmation candle closed (Candle T+1)
    INVALIDATED = "INVALIDATED"    # Broken directly (candle closed beyond zone boundary)
    MITIGATED = "MITIGATED"        # Trade executed or exhausted
    EXPIRED = "EXPIRED"            # Aged out past max lookback


@dataclass
class SmartMoneyZone:
    """Represents an active or historical Order Block or Demand/Supply Zone."""
    zone_id: str
    zone_type: ZoneType
    symbol: str
    high: float                    # Upper boundary (highest wick of origin candle)
    low: float                     # Lower boundary (lowest wick of origin candle)
    body_high: float               # max(open, close) of origin candle
    body_low: float                # min(open, close) of origin candle
    creation_bar_idx: int          # Bar index of origin candle
    creation_ts: int               # Millisecond timestamp
    status: ZoneStatus = ZoneStatus.ACTIVE
    bos_bar_idx: Optional[int] = None
    bos_price: Optional[float] = None
    fvg_size: float = 0.0
    consecutive_candles: int = 0
    is_extrema: bool = False
    retest_bar_idx: Optional[int] = None
    retest_ts: Optional[int] = None
    retest_price: Optional[float] = None
    retest_wick_price: Optional[float] = None
    tested_count: int = 0
    confirmation_bar_idx: Optional[int] = None

    @property
    def is_bullish(self) -> bool:
        return self.zone_type in (
            ZoneType.BULLISH_ORDER_BLOCK,
            ZoneType.DEMAND_BLOCK,
            ZoneType.CONFLUENT_DEMAND_OB
        )

    @property
    def is_bearish(self) -> bool:
        return self.zone_type in (
            ZoneType.BEARISH_ORDER_BLOCK,
            ZoneType.SUPPLY_BLOCK,
            ZoneType.CONFLUENT_SUPPLY_OB
        )

    @property
    def zone_height(self) -> float:
        return max(1e-12, self.high - self.low)


@dataclass
class SwingPoint:
    """Fractal pivot high or low."""
    bar_idx: int
    ts: int
    price: float
    is_high: bool  # True for swing high, False for swing low


class SwingStructureDetector:
    """
    Identifies fractal swing highs and lows and evaluates Break of Structure (BOS).
    Strict Body-Close Rule:
    A high or low is only broken when a candle body closes beyond it.
    Wick-only breaches are considered liquidity sweeps and are rejected.
    """

    @staticmethod
    def find_swings(
        highs: List[float],
        lows: List[float],
        timestamps: List[int],
        left_bars: int = 3,
        right_bars: int = 3
    ) -> List[SwingPoint]:
        n = len(highs)
        swings: List[SwingPoint] = []
        if n < left_bars + right_bars + 1:
            return swings

        for i in range(left_bars, n - right_bars):
            # Check swing high
            curr_h = highs[i]
            is_sh = True
            for j in range(i - left_bars, i + right_bars + 1):
                if j != i and highs[j] >= curr_h:
                    is_sh = False
                    break
            if is_sh:
                swings.append(SwingPoint(bar_idx=i, ts=timestamps[i], price=curr_h, is_high=True))

            # Check swing low
            curr_l = lows[i]
            is_sl = True
            for j in range(i - left_bars, i + right_bars + 1):
                if j != i and lows[j] <= curr_l:
                    is_sl = False
                    break
            if is_sl:
                swings.append(SwingPoint(bar_idx=i, ts=timestamps[i], price=curr_l, is_high=False))

        swings.sort(key=lambda x: x.bar_idx)
        return swings


class OrderBlockDemandStrategy(BaseStrategy):
    """
    Unified Order Block + Demand/Supply Block Strategy.
    Designed to replicate Vivek Yadav's manual trading edge:
    1. Order Block Discovery: Opposite candle (wick-to-wick) preceding 2-3+ continuous impulse candles.
    2. Demand/Supply Blocks: 3-5 consecutive impulse candles + FVG at structural extrema.
    3. Multi-Candle State Sequence:
       - Step 1: Retest Candle T touches zone and prints rejection wick (lower wick for bullish, upper for bearish).
       - Step 2: Next Candle T+1 confirms by closing in trade direction (Green for bullish, Red for bearish).
       - Step 3: Entry executed at the close of Candle T+1.
    4. Anti-Recreation Memory: Origin timestamps of resolved/mitigated zones are permanently remembered.
    5. Dynamic 1:2 R:R targeting with 1:1 partial profit exit and breakeven lock.
    """

    def __init__(
        self,
        market: KCEXMarket,
        symbol: str,
        interval: str = "Min1",
        swing_left_bars: int = 3,
        swing_right_bars: int = 3,
        min_impulse_candles: int = 2,
        max_impulse_candles: int = 5,
        min_rejection_wick_ratio: float = 0.15,
        risk_reward_ratio: float = 2.0,
        buffer_ticks: int = 1,
        min_sl_ticks: int = 3,
        max_sl_ticks: int = 35,
        max_zone_age_bars: int = 120,
        extrema_percentile: float = 0.25,
        trend_filter_enabled: bool = False,
        partial_tp_enabled: bool = True,
        breakeven_buffer_ticks: int = 1,
        preferred_direction: Optional[OrderDirection] = None,
        cooldown_seconds: float = 15.0,
        require_closed_candle: bool = True,
        auto_start_feed: bool = False,
        name: str = "OrderBlockDemand"
    ):
        super().__init__(name=name)
        self.market = market
        self.symbol = symbol.upper()
        self.interval = interval
        self.swing_left_bars = swing_left_bars
        self.swing_right_bars = swing_right_bars
        self.min_impulse_candles = min_impulse_candles
        self.max_impulse_candles = max_impulse_candles
        self.min_rejection_wick_ratio = min_rejection_wick_ratio
        self.risk_reward_ratio = risk_reward_ratio
        self.buffer_ticks = buffer_ticks
        self.min_sl_ticks = min_sl_ticks
        self.max_sl_ticks = max_sl_ticks
        self.max_zone_age_bars = max_zone_age_bars
        self.extrema_percentile = extrema_percentile
        self.trend_filter_enabled = trend_filter_enabled
        self.partial_tp_enabled = partial_tp_enabled
        self.breakeven_buffer_ticks = breakeven_buffer_ticks
        self.preferred_direction = preferred_direction
        self.cooldown_seconds = cooldown_seconds
        self.require_closed_candle = require_closed_candle

        # Execution tracking
        self.last_trade_closed_at: Optional[float] = None
        self.trade_in_progress: bool = False
        self.completed_trades_count: int = 0
        self.last_signal_candle_ts: Optional[int] = None

        # Contract tick specifications
        self._price_unit: float = 0.001
        self._price_precision: int = 4
        self._refresh_contract_spec()

        # Active zones registry: Dict[zone_id, SmartMoneyZone]
        self.active_zones: Dict[str, SmartMoneyZone] = {}
        # Anti-recreation memory: timestamps of origin candles that have been resolved (mitigated, invalidated, expired)
        self.resolved_origin_ts: Set[int] = set()
        self.history_zones: List[SmartMoneyZone] = []
        self.zone_counter: int = 0
        self.last_diagnostics: Dict[str, Any] = {}
        self.last_rejection_reason: str = ""

    def _refresh_contract_spec(self) -> None:
        """Inspects contract specifications for precise tick scaling."""
        try:
            contract = self.market.get_contract_detail(self.symbol)
            if contract:
                self._price_unit = contract.price_unit
                self._price_precision = contract.price_precision
        except Exception:
            pass

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

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        self.trade_in_progress = False
        self.last_trade_closed_at = outcome.close_time or time.time()
        self.completed_trades_count += 1
        logger.info(
            "[%s] Completed trade #%d. Realized PnL: $%.4f. Cooldown %ds initiated.",
            self.name, outcome.trade_id, outcome.realized_pnl_usdt, int(self.cooldown_seconds)
        )

    def on_trade_rejected(self) -> None:
        """Resets trade_in_progress when execution is canceled or rejected."""
        self.trade_in_progress = False

    def _extract_candle_series(self, raw_bars: List[Any]) -> Tuple[List[int], List[float], List[float], List[float], List[float], List[float]]:
        """Normalizes klines into parallel lists: timestamps, opens, highs, lows, closes, volumes."""
        timestamps: List[int] = []
        opens: List[float] = []
        highs: List[float] = []
        lows: List[float] = []
        closes: List[float] = []
        volumes: List[float] = []

        for b in raw_bars:
            if hasattr(b, "timestamp") and hasattr(b, "close"):
                timestamps.append(int(getattr(b, "timestamp", 0)))
                opens.append(float(getattr(b, "open", 0.0)))
                highs.append(float(getattr(b, "high", 0.0)))
                lows.append(float(getattr(b, "low", 0.0)))
                closes.append(float(getattr(b, "close", 0.0)))
                volumes.append(float(getattr(b, "volume", 0.0)))
            elif isinstance(b, dict):
                timestamps.append(int(b.get("timestamp", b.get("time", 0))))
                opens.append(float(b.get("open", 0.0)))
                highs.append(float(b.get("high", 0.0)))
                lows.append(float(b.get("low", 0.0)))
                closes.append(float(b.get("close", 0.0)))
                volumes.append(float(b.get("volume", 0.0)))
            elif isinstance(b, (list, tuple)) and len(b) >= 6:
                timestamps.append(int(b[0]))
                opens.append(float(b[1]))
                highs.append(float(b[2]))
                lows.append(float(b[3]))
                closes.append(float(b[4]))
                volumes.append(float(b[5]))

        return timestamps, opens, highs, lows, closes, volumes

    def scan_for_order_blocks(
        self,
        timestamps: List[int],
        opens: List[float],
        highs: List[float],
        lows: List[float],
        closes: List[float],
        swings: Optional[List[SwingPoint]] = None
    ) -> List[SmartMoneyZone]:
        """
        Discovers Order Blocks based on Vivek Yadav's Rule:
        An Order Block is the opposite candle immediately preceding a strong movement
        of 2-3 or more continuous impulse candles in the desired direction.

        - Bullish Order Block:
          The last RED candle immediately preceding 2-3+ consecutive GREEN candles.
          Full wick-to-wick range (high to low) marked as the Order Block.
          Displacement verified: Green impulse sequence breaks origin candle high / swing high,
          or creates an FVG, or has substantial displacement.

        - Bearish Order Block:
          The last GREEN candle immediately preceding 2-3+ consecutive RED candles.
          Full wick-to-wick range (high to low) marked as the Order Block.
          Displacement verified: Red impulse sequence breaks origin candle low / swing low,
          or creates an FVG, or has substantial displacement.
        """
        discovered: List[SmartMoneyZone] = []
        n = len(closes)
        if n < 4:
            return discovered

        # ATR calculation for displacement scale
        tr_list = [highs[j] - lows[j] for j in range(max(1, n - 20), n)]
        local_atr = sum(tr_list) / len(tr_list) if tr_list else self._price_unit * 5.0

        scan_start = max(0, n - 60)
        # Scan candidate origin candles
        for origin_idx in range(scan_start, n - 2):
            origin_ts = timestamps[origin_idx]
            if origin_ts in self.resolved_origin_ts:
                continue
            if any(z.creation_ts == origin_ts for z in self.active_zones.values()):
                continue

            # -------------------------------------------------------------
            # 1. Bullish Order Block Check
            # Origin must be RED: closes[origin_idx] <= opens[origin_idx]
            # -------------------------------------------------------------
            if closes[origin_idx] <= opens[origin_idx]:
                consec_green = 0
                for k in range(origin_idx + 1, min(n, origin_idx + 1 + self.max_impulse_candles)):
                    if closes[k] > opens[k]:
                        consec_green += 1
                    else:
                        break

                if consec_green >= self.min_impulse_candles:
                    impulse_end = origin_idx + consec_green
                    impulse_max_high = max(highs[origin_idx + 1 : impulse_end + 1])
                    total_disp = closes[impulse_end] - opens[origin_idx + 1]

                    # Displacement & Break of Structure verification
                    has_fvg = (origin_idx + 2 <= impulse_end) and (lows[origin_idx + 2] > highs[origin_idx])
                    fvg_gap = max(0.0, lows[origin_idx + 2] - highs[origin_idx]) if has_fvg else 0.0
                    breaks_origin_high = impulse_max_high > highs[origin_idx] and closes[impulse_end] > highs[origin_idx]
                    has_disp = total_disp >= (0.5 * local_atr)

                    # When swings are provided, strictly enforce Body-Close Break of Structure (BOS)
                    # Wick-only breaches are liquidity sweeps and must be rejected as per Vivek's Rule
                    if swings:
                        prior_shs = [s for s in swings if s.is_high and s.bar_idx < origin_idx]
                        if not prior_shs:
                            continue
                        recent_sh = prior_shs[-1]
                        if impulse_max_high >= recent_sh.price:
                            if closes[impulse_end] <= recent_sh.price:
                                # Wick sweep: rejected
                                continue
                            else:
                                breaks_swing_high = True
                        else:
                            # Did not reach/break prior swing high
                            continue
                    else:
                        breaks_swing_high = breaks_origin_high or has_fvg or has_disp

                    if breaks_swing_high or has_fvg or has_disp:
                        self.zone_counter += 1
                        zid = f"OB_BULL_{self.zone_counter}_{origin_ts}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.BULLISH_ORDER_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_idx],
                            low=lows[origin_idx],
                            body_high=max(opens[origin_idx], closes[origin_idx]),
                            body_low=min(opens[origin_idx], closes[origin_idx]),
                            creation_bar_idx=origin_idx,
                            creation_ts=origin_ts,
                            fvg_size=fvg_gap,
                            consecutive_candles=consec_green,
                            bos_bar_idx=impulse_end,
                            bos_price=closes[impulse_end]
                        )
                        discovered.append(zone)

            # -------------------------------------------------------------
            # 2. Bearish Order Block Check
            # Origin must be GREEN: closes[origin_idx] >= opens[origin_idx]
            # -------------------------------------------------------------
            elif closes[origin_idx] >= opens[origin_idx]:
                consec_red = 0
                for k in range(origin_idx + 1, min(n, origin_idx + 1 + self.max_impulse_candles)):
                    if closes[k] < opens[k]:
                        consec_red += 1
                    else:
                        break

                if consec_red >= self.min_impulse_candles:
                    impulse_end = origin_idx + consec_red
                    impulse_min_low = min(lows[origin_idx + 1 : impulse_end + 1])
                    total_disp = opens[origin_idx + 1] - closes[impulse_end]

                    has_fvg = (origin_idx + 2 <= impulse_end) and (highs[origin_idx + 2] < lows[origin_idx])
                    fvg_gap = max(0.0, lows[origin_idx] - highs[origin_idx + 2]) if has_fvg else 0.0
                    breaks_origin_low = impulse_min_low < lows[origin_idx] and closes[impulse_end] < lows[origin_idx]
                    has_disp = total_disp >= (0.5 * local_atr)

                    if swings:
                        prior_sls = [s for s in swings if not s.is_high and s.bar_idx < origin_idx]
                        if not prior_sls:
                            continue
                        recent_sl = prior_sls[-1]
                        if impulse_min_low <= recent_sl.price:
                            if closes[impulse_end] >= recent_sl.price:
                                # Wick sweep: rejected
                                continue
                            else:
                                breaks_swing_low = True
                        else:
                            continue
                    else:
                        breaks_swing_low = breaks_origin_low or has_fvg or has_disp

                    if breaks_swing_low or has_fvg or has_disp:
                        self.zone_counter += 1
                        zid = f"OB_BEAR_{self.zone_counter}_{origin_ts}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.BEARISH_ORDER_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_idx],
                            low=lows[origin_idx],
                            body_high=max(opens[origin_idx], closes[origin_idx]),
                            body_low=min(opens[origin_idx], closes[origin_idx]),
                            creation_bar_idx=origin_idx,
                            creation_ts=origin_ts,
                            fvg_size=fvg_gap,
                            consecutive_candles=consec_red,
                            bos_bar_idx=impulse_end,
                            bos_price=closes[impulse_end]
                        )
                        discovered.append(zone)

        return discovered

    def scan_for_demand_supply_blocks(
        self,
        timestamps: List[int],
        opens: List[float],
        highs: List[float],
        lows: List[float],
        closes: List[float]
    ) -> List[SmartMoneyZone]:
        """
        Discovers Demand and Supply Blocks based on Vivek Yadav Video 2:
        1. 3 to 5 consecutive strong candles in one direction.
        2. Creation of Imbalance / Fair Value Gap (FVG).
        3. Structural Extrema Location:
           - Demand must be in the lower 25% of recent range (structural bottom).
           - Supply must be in the upper 25% of recent range (structural top).
        4. Marking the entire opposite candle (high to low) immediately before the impulse.
        """
        discovered: List[SmartMoneyZone] = []
        n = len(closes)
        if n < 5:
            return discovered

        lookback_slice = slice(max(0, n - 60), n)
        recent_highest = max(highs[lookback_slice])
        recent_lowest = min(lows[lookback_slice])
        range_span = max(1e-12, recent_highest - recent_lowest)
        demand_ceiling = recent_lowest + range_span * self.extrema_percentile
        supply_floor = recent_highest - range_span * self.extrema_percentile

        scan_start = max(0, n - 50)
        for origin_idx in range(scan_start, n - 3):
            origin_ts = timestamps[origin_idx]
            if origin_ts in self.resolved_origin_ts:
                continue
            if any(z.creation_ts == origin_ts for z in self.active_zones.values()):
                continue

            # Bullish Demand Block (Origin is RED, followed by 3-5 GREEN candles at bottom)
            if closes[origin_idx] <= opens[origin_idx]:
                consec_green = 0
                for k in range(origin_idx + 1, min(n, origin_idx + 1 + self.max_impulse_candles)):
                    if closes[k] > opens[k]:
                        consec_green += 1
                    else:
                        break

                if consec_green >= 3:
                    if lows[origin_idx] <= demand_ceiling:
                        fvg_gap = 0.0
                        if origin_idx + 2 < n:
                            fvg_gap = max(0.0, lows[origin_idx + 2] - highs[origin_idx])

                        self.zone_counter += 1
                        zid = f"DEMAND_{self.zone_counter}_{origin_ts}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.DEMAND_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_idx],
                            low=lows[origin_idx],
                            body_high=max(opens[origin_idx], closes[origin_idx]),
                            body_low=min(opens[origin_idx], closes[origin_idx]),
                            creation_bar_idx=origin_idx,
                            creation_ts=origin_ts,
                            fvg_size=fvg_gap,
                            consecutive_candles=consec_green,
                            is_extrema=True
                        )
                        discovered.append(zone)

            # Bearish Supply Block (Origin is GREEN, followed by 3-5 RED candles at top)
            elif closes[origin_idx] >= opens[origin_idx]:
                consec_red = 0
                for k in range(origin_idx + 1, min(n, origin_idx + 1 + self.max_impulse_candles)):
                    if closes[k] < opens[k]:
                        consec_red += 1
                    else:
                        break

                if consec_red >= 3:
                    if highs[origin_idx] >= supply_floor:
                        fvg_gap = 0.0
                        if origin_idx + 2 < n:
                            fvg_gap = max(0.0, lows[origin_idx] - highs[origin_idx + 2])

                        self.zone_counter += 1
                        zid = f"SUPPLY_{self.zone_counter}_{origin_ts}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.SUPPLY_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_idx],
                            low=lows[origin_idx],
                            body_high=max(opens[origin_idx], closes[origin_idx]),
                            body_low=min(opens[origin_idx], closes[origin_idx]),
                            creation_bar_idx=origin_idx,
                            creation_ts=origin_ts,
                            fvg_size=fvg_gap,
                            consecutive_candles=consec_red,
                            is_extrema=True
                        )
                        discovered.append(zone)

        return discovered

    def update_zone_lifecycle(
        self,
        new_zones: List[SmartMoneyZone],
        current_bar_idx: int,
        opens: List[float],
        highs: List[float],
        lows: List[float],
        closes: List[float]
    ) -> None:
        """
        Maintains the active zones registry, merges overlapping zones into Confluent zones,
        and invalidates zones that are breached.
        """
        # 1. Register new zones (avoid duplicate origin timestamps or already resolved timestamps)
        for nz in new_zones:
            if nz.creation_ts in self.resolved_origin_ts:
                continue

            exists = any(
                z.creation_ts == nz.creation_ts and z.is_bullish == nz.is_bullish
                for z in self.active_zones.values()
            )
            if not exists:
                # Check for confluence between an OB and a Demand/Supply zone
                confluent_found = False
                for existing_id, ez in list(self.active_zones.items()):
                    if ez.status in (ZoneStatus.ACTIVE, ZoneStatus.TESTED) and ez.is_bullish == nz.is_bullish:
                        overlap_min = max(ez.low, nz.low)
                        overlap_max = min(ez.high, nz.high)
                        if overlap_max > overlap_min:
                            # Upgrade to Confluent Zone
                            if ez.is_bullish:
                                ez.zone_type = ZoneType.CONFLUENT_DEMAND_OB
                            else:
                                ez.zone_type = ZoneType.CONFLUENT_SUPPLY_OB
                            ez.high = max(ez.high, nz.high)
                            ez.low = min(ez.low, nz.low)
                            ez.fvg_size = max(ez.fvg_size, nz.fvg_size)
                            confluent_found = True
                            break
                if not confluent_found:
                    self.active_zones[nz.zone_id] = nz

        # 2. Evaluate active zones against current evaluating candle
        c_close = closes[current_bar_idx]

        for zid, zone in list(self.active_zones.items()):
            # Expire stale zones
            if current_bar_idx - zone.creation_bar_idx > self.max_zone_age_bars:
                zone.status = ZoneStatus.EXPIRED
                self.resolved_origin_ts.add(zone.creation_ts)
                self.history_zones.append(zone)
                del self.active_zones[zid]
                continue

            # Invalidation Check:
            # Vivek: "बाय the वे अगर ये ऑर्डर ब्लॉक डायरेक्ट ब्रेक हो जाता है तो आपको ट्रेड नहीं करना है... मान लीजिए कि इसने पूरी रेड कैंडल बना दी तो आपको ट्रेड नहीं करना है"
            if zone.is_bullish:
                if c_close < zone.low:
                    zone.status = ZoneStatus.INVALIDATED
                    self.resolved_origin_ts.add(zone.creation_ts)
                    self.history_zones.append(zone)
                    del self.active_zones[zid]
                    continue
            else:
                if c_close > zone.high:
                    zone.status = ZoneStatus.INVALIDATED
                    self.resolved_origin_ts.add(zone.creation_ts)
                    self.history_zones.append(zone)
                    del self.active_zones[zid]
                    continue

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        now = time.time()
        if not self.should_generate_signal(now):
            return None

        # Fetch latest candlestick history
        bars = self.market.get_klines(self.symbol, interval=self.interval, limit=120)
        if not bars or len(bars) < 30:
            self.last_rejection_reason = "Insufficient candle history (<30 bars)"
            return None

        self._refresh_contract_spec()

        timestamps, opens, highs, lows, closes, volumes = self._extract_candle_series(bars)
        n = len(closes)
        eval_idx = n - 1 if not self.require_closed_candle else n - 2
        if eval_idx < 10:
            return None

        current_candle_ts = timestamps[eval_idx]
        if self.last_signal_candle_ts is not None and self.last_signal_candle_ts >= current_candle_ts:
            return None

        # 1. Detect Fractal Swings
        swings = SwingStructureDetector.find_swings(
            highs=highs[:eval_idx + 1],
            lows=lows[:eval_idx + 1],
            timestamps=timestamps[:eval_idx + 1],
            left_bars=self.swing_left_bars,
            right_bars=self.swing_right_bars
        )

        # Market structure filter if enabled
        structure_bias: Optional[OrderDirection] = None
        if self.trend_filter_enabled and len(swings) >= 4:
            shs = [s for s in swings if s.is_high]
            sls = [s for s in swings if not s.is_high]
            if len(shs) >= 2 and len(sls) >= 2:
                higher_high = shs[-1].price > shs[-2].price
                higher_low = sls[-1].price > sls[-2].price
                lower_high = shs[-1].price < shs[-2].price
                lower_low = sls[-1].price < sls[-2].price
                if higher_high and higher_low:
                    structure_bias = OrderDirection.LONG
                elif lower_high and lower_low:
                    structure_bias = OrderDirection.SHORT

        # 2. Discover Order Blocks & Demand/Supply Blocks
        ob_zones = self.scan_for_order_blocks(timestamps, opens, highs, lows, closes, swings)
        ds_zones = self.scan_for_demand_supply_blocks(timestamps, opens, highs, lows, closes)
        all_new_zones = ob_zones + ds_zones

        # 3. Update Zone Lifecycle & Invalidation
        self.update_zone_lifecycle(all_new_zones, eval_idx, opens, highs, lows, closes)

        # Evaluating candle metrics
        c_open = opens[eval_idx]
        c_high = highs[eval_idx]
        c_low = lows[eval_idx]
        c_close = closes[eval_idx]
        c_range = max(1e-12, c_high - c_low)

        # Local ATR(14) for volatility & approach weakness check
        tr_list = [highs[i] - lows[i] for i in range(max(1, eval_idx - 14), eval_idx + 1)]
        current_atr = sum(tr_list) / len(tr_list) if tr_list else self._price_unit * 5.0

        pu = self._price_unit
        pu_safe = pu if pu > 0 else 0.001

        best_signal: Optional[TradeSignal] = None
        best_score: float = -1.0
        best_zone_id: Optional[str] = None

        # 4. Multi-Candle State Machine: Tap & Rejection Wick (Candle T) -> Confirmation (Candle T+1)
        for zid, zone in list(self.active_zones.items()):
            # Zone must have been created before the evaluating candle
            if zone.creation_bar_idx >= eval_idx:
                continue

            # Approach Weakness Check: Retest should approach smoothly, not climax explosion
            if c_range > 3.0 * current_atr:
                continue

            # -------------------------------------------------------------
            # Stage A: Check for Retest & Rejection Wick (Candle T)
            # -------------------------------------------------------------
            if zone.status == ZoneStatus.ACTIVE:
                # Scan recent bars (from creation up to eval_idx) to find if a bar tapped and rejected
                # We search the recent window: [max(zone.creation_bar_idx + 1, eval_idx - 2), eval_idx]
                for bar_k in range(max(zone.creation_bar_idx + 1, eval_idx - 2), eval_idx + 1):
                    k_open = opens[bar_k]
                    k_high = highs[bar_k]
                    k_low = lows[bar_k]
                    k_close = closes[bar_k]
                    k_range = max(1e-12, k_high - k_low)

                    if zone.is_bullish:
                        # Price tested inside zone
                        tapped = (k_low <= zone.high) and (k_high >= zone.low)
                        if tapped and k_close >= zone.low:
                            lower_wick = min(k_open, k_close) - k_low
                            if (lower_wick / k_range) >= self.min_rejection_wick_ratio:
                                zone.status = ZoneStatus.TESTED
                                zone.retest_bar_idx = bar_k
                                zone.retest_ts = timestamps[bar_k]
                                zone.retest_wick_price = k_low
                                zone.tested_count += 1
                                break
                    elif zone.is_bearish:
                        tapped = (k_high >= zone.low) and (k_low <= zone.high)
                        if tapped and k_close <= zone.high:
                            upper_wick = k_high - max(k_open, k_close)
                            if (upper_wick / k_range) >= self.min_rejection_wick_ratio:
                                zone.status = ZoneStatus.TESTED
                                zone.retest_bar_idx = bar_k
                                zone.retest_ts = timestamps[bar_k]
                                zone.retest_wick_price = k_high
                                zone.tested_count += 1
                                break

            # -------------------------------------------------------------
            # Stage B: Confirmation Candle Close Check (Candle T+1)
            # -------------------------------------------------------------
            if zone.status == ZoneStatus.TESTED and zone.retest_bar_idx is not None:
                retest_k = zone.retest_bar_idx
                bars_since_retest = eval_idx - retest_k

                # Confirmation candle must follow the retest (eval_idx == retest_k + 1, or within 2 bars)
                if bars_since_retest in (1, 2):
                    if zone.is_bullish:
                        if self.preferred_direction is not None and self.preferred_direction != OrderDirection.LONG:
                            continue
                        if structure_bias is not None and structure_bias != OrderDirection.LONG:
                            continue

                        # Confirmation Rule (User Req 3 & Vivek Masterclass):
                        # Next candle MUST be GREEN and close upward without breaching zone low
                        is_green_confirm = (c_close > c_open) and (c_close >= zone.low)
                        if not is_green_confirm:
                            continue

                        # Stop Loss strictly behind the Order Block low & rejection wick + buffer
                        wick_low = zone.retest_wick_price if zone.retest_wick_price is not None else zone.low
                        stop_loss_price = min(zone.low, wick_low) - (self.buffer_ticks * pu_safe)
                        risk_distance = c_close - stop_loss_price
                        risk_ticks = int(math.ceil(risk_distance / pu_safe))

                        if risk_ticks < self.min_sl_ticks or risk_ticks > self.max_sl_ticks:
                            continue

                        # 1:2 Risk to Reward Dynamic Targets
                        target_1to1_ticks = risk_ticks
                        target_1to1_price = round(c_close + (target_1to1_ticks * pu_safe), self._price_precision)
                        target_1to2_ticks = int(round(risk_ticks * self.risk_reward_ratio))
                        target_1to2_price = round(c_close + (target_1to2_ticks * pu_safe), self._price_precision)
                        stop_loss_price = round(stop_loss_price, self._price_precision)

                        score = 1.0
                        if zone.zone_type == ZoneType.CONFLUENT_DEMAND_OB:
                            score = 3.0
                        elif zone.zone_type == ZoneType.DEMAND_BLOCK and zone.fvg_size > 0:
                            score = 2.0

                        if score > best_score:
                            best_score = score
                            best_zone_id = zid
                            metadata = {
                                "strategy_mode": "ORDER_BLOCK_DEMAND",
                                "zone_id": zone.zone_id,
                                "zone_type": zone.zone_type.value,
                                "zone_high": zone.high,
                                "zone_low": zone.low,
                                "entry_price": round(c_close, self._price_precision),
                                "stop_loss_price": stop_loss_price,
                                "take_profit_price": target_1to2_price,
                                "target_ticks": target_1to2_ticks,
                                "target_sl_ticks": risk_ticks,
                                "target_1to1_ticks": target_1to1_ticks,
                                "target_1to1_price": target_1to1_price,
                                "target_1to2_ticks": target_1to2_ticks,
                                "target_1to2_price": target_1to2_price,
                                "risk_reward_ratio": self.risk_reward_ratio,
                                "partial_tp_enabled": self.partial_tp_enabled,
                                "breakeven_buffer_ticks": self.breakeven_buffer_ticks,
                                "consecutive_candles": zone.consecutive_candles,
                                "fvg_size": zone.fvg_size,
                                "candle_timestamp": current_candle_ts,
                                "atr": current_atr,
                                "retest_bar_idx": zone.retest_bar_idx,
                                "confirmation_bar_idx": eval_idx
                            }
                            best_signal = TradeSignal(
                                symbol=self.symbol,
                                direction=OrderDirection.LONG,
                                sub_strategy_name=f"{self.name}({zone.zone_type.value}-LONG)",
                                timestamp=now,
                                metadata=metadata
                            )

                    elif zone.is_bearish:
                        if self.preferred_direction is not None and self.preferred_direction != OrderDirection.SHORT:
                            continue
                        if structure_bias is not None and structure_bias != OrderDirection.SHORT:
                            continue

                        # Confirmation Rule (User Req 3 & Vivek Masterclass):
                        # Next candle MUST be RED and close downward without breaching zone high
                        is_red_confirm = (c_close < c_open) and (c_close <= zone.high)
                        if not is_red_confirm:
                            continue

                        # Stop Loss strictly above the Order Block high & rejection wick + buffer
                        wick_high = zone.retest_wick_price if zone.retest_wick_price is not None else zone.high
                        stop_loss_price = max(zone.high, wick_high) + (self.buffer_ticks * pu_safe)
                        risk_distance = stop_loss_price - c_close
                        risk_ticks = int(math.ceil(risk_distance / pu_safe))

                        if risk_ticks < self.min_sl_ticks or risk_ticks > self.max_sl_ticks:
                            continue

                        # 1:2 Risk to Reward Dynamic Targets
                        target_1to1_ticks = risk_ticks
                        target_1to1_price = round(c_close - (target_1to1_ticks * pu_safe), self._price_precision)
                        target_1to2_ticks = int(round(risk_ticks * self.risk_reward_ratio))
                        target_1to2_price = round(c_close - (target_1to2_ticks * pu_safe), self._price_precision)
                        stop_loss_price = round(stop_loss_price, self._price_precision)

                        score = 1.0
                        if zone.zone_type == ZoneType.CONFLUENT_SUPPLY_OB:
                            score = 3.0
                        elif zone.zone_type == ZoneType.SUPPLY_BLOCK and zone.fvg_size > 0:
                            score = 2.0

                        if score > best_score:
                            best_score = score
                            best_zone_id = zid
                            metadata = {
                                "strategy_mode": "ORDER_BLOCK_DEMAND",
                                "zone_id": zone.zone_id,
                                "zone_type": zone.zone_type.value,
                                "zone_high": zone.high,
                                "zone_low": zone.low,
                                "entry_price": c_close,
                                "stop_loss_price": stop_loss_price,
                                "take_profit_price": target_1to2_price,
                                "target_ticks": target_1to2_ticks,
                                "target_sl_ticks": risk_ticks,
                                "target_1to1_ticks": target_1to1_ticks,
                                "target_1to1_price": target_1to1_price,
                                "target_1to2_ticks": target_1to2_ticks,
                                "target_1to2_price": target_1to2_price,
                                "risk_reward_ratio": self.risk_reward_ratio,
                                "partial_tp_enabled": self.partial_tp_enabled,
                                "breakeven_buffer_ticks": self.breakeven_buffer_ticks,
                                "consecutive_candles": zone.consecutive_candles,
                                "fvg_size": zone.fvg_size,
                                "candle_timestamp": current_candle_ts,
                                "atr": current_atr,
                                "retest_bar_idx": zone.retest_bar_idx,
                                "confirmation_bar_idx": eval_idx
                            }
                            best_signal = TradeSignal(
                                symbol=self.symbol,
                                direction=OrderDirection.SHORT,
                                sub_strategy_name=f"{self.name}({zone.zone_type.value}-SHORT)",
                                timestamp=now,
                                metadata=metadata
                            )

                elif bars_since_retest > 2:
                    # Retest expired without timely confirmation; reset to ACTIVE
                    zone.status = ZoneStatus.ACTIVE
                    zone.retest_bar_idx = None
                    zone.retest_wick_price = None

        # 5. Signal Dispatch & Zone Mitigation Archival
        if best_signal is not None and best_zone_id is not None:
            self.last_signal_candle_ts = current_candle_ts
            self.trade_in_progress = True

            if best_zone_id in self.active_zones:
                used_zone = self.active_zones[best_zone_id]
                used_zone.status = ZoneStatus.MITIGATED
                used_zone.confirmation_bar_idx = eval_idx
                self.resolved_origin_ts.add(used_zone.creation_ts)
                self.history_zones.append(used_zone)
                del self.active_zones[best_zone_id]

            logger.info(
                "⚡ [ORDER BLOCK + DEMAND SIGNAL] %s on %s | Zone: %s [%.4f - %.4f] | TP: +%dt ($%.4f), SL: -%dt ($%.4f) | 1:%.1f RR",
                best_signal.direction.value,
                self.symbol,
                best_signal.metadata.get("zone_type"),
                best_signal.metadata.get("zone_low", 0.0),
                best_signal.metadata.get("zone_high", 0.0),
                best_signal.metadata.get("target_ticks", 0),
                best_signal.metadata.get("take_profit_price", 0.0),
                best_signal.metadata.get("target_sl_ticks", 0),
                best_signal.metadata.get("stop_loss_price", 0.0),
                best_signal.metadata.get("risk_reward_ratio", 2.0)
            )
            return best_signal

        return None

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "strategy": "ORDER_BLOCK_DEMAND",
            "symbol": self.symbol,
            "interval": self.interval,
            "swing_left_bars": self.swing_left_bars,
            "swing_right_bars": self.swing_right_bars,
            "min_impulse_candles": self.min_impulse_candles,
            "max_impulse_candles": self.max_impulse_candles,
            "min_rejection_wick_ratio": self.min_rejection_wick_ratio,
            "risk_reward_ratio": self.risk_reward_ratio,
            "buffer_ticks": self.buffer_ticks,
            "min_sl_ticks": self.min_sl_ticks,
            "max_sl_ticks": self.max_sl_ticks,
            "extrema_percentile": self.extrema_percentile,
            "active_zones_count": len(self.active_zones),
            "resolved_origin_count": len(self.resolved_origin_ts)
        }

    def get_diagnostics(self) -> Dict[str, Any]:
        return {
            "active_zones_count": len(self.active_zones),
            "resolved_origin_count": len(self.resolved_origin_ts),
            "zones": [
                {
                    "id": z.zone_id,
                    "type": z.zone_type.value,
                    "high": z.high,
                    "low": z.low,
                    "status": z.status.value,
                    "fvg": z.fvg_size
                }
                for z in list(self.active_zones.values())[-5:]
            ],
            "last_rejection_reason": self.last_rejection_reason
        }


# Backwards compatibility aliases
OrderBookDemandStrategy = OrderBlockDemandStrategy
OrderBlockDemandSubStrategy = OrderBlockDemandStrategy
