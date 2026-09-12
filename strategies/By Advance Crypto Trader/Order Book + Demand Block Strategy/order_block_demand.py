"""
Order Block + Demand/Supply Block Trading Strategy
===================================================
Designed from the Masterclasses of Vivek Yadav (Advance Crypto Trader):
1. 'Order Block Strategy' (SMC: BOS body-close, wick-to-wick OB origin marking, tap + confirmation, 1:2 RR)
2. 'Demand and Supply Trading Strategy' (3-5 consecutive impulse candles, FVG/imbalance, extrema location,
   approach weakness, rejection wick, confirmation candle close, safe zone SL)

Key Features:
- Pure-Python rolling fractal swing detection (peaks and troughs).
- Strict Body-Close Break of Structure (BOS) rule: Wick-only breaches are rejected as liquidity sweeps.
- Wick-to-wick bounding box marking for Order Blocks and Demand/Supply Blocks.
- Demand/Supply Impulse Engine: Validates 3 to 5 consecutive directional candles and Fair Value Gaps (FVG).
- Extrema Location Filtering: Demand is exclusively identified at structural bottoms; Supply at structural tops.
- Retest & Mitigation Engine: Checks for approach weakness, zone tap, rejection wick (absorption), and confirmation candle close.
- Strict Invalidation Engine: Direct blowout closes beyond the zone immediately disqualify the setup.
- Structure-Calibrated Dynamic 1:2 Risk-to-Reward: Calculates exact SL ticks behind zone boundary and projects 2x R:R TP ticks.
"""

from __future__ import annotations
import math
import time
import logging
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple, TYPE_CHECKING
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
    TESTED = "TESTED"              # Tapped zone and formed rejection wick
    CONFIRMED = "CONFIRMED"        # Directional confirmation candle closed
    INVALIDATED = "INVALIDATED"    # Broken directly (candle closed beyond zone)
    MITIGATED = "MITIGATED"        # Trade executed or exhausted


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
    retest_price: Optional[float] = None
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
    Combines:
    1. Smart Money Order Blocks identified upon validated structural BOS with body close.
    2. Demand and Supply Blocks formed by 3-5 consecutive impulse candles + FVG at structural extrema.
    3. Confluence bonus when Order Block and Demand/Supply zone overlap.
    4. Approach weakness check, rejection wick validation, and confirmation candle trigger.
    5. Dynamic 1:2 R:R tick targeting and stop loss placement behind zone boundaries.
    """

    def __init__(
        self,
        market: KCEXMarket,
        symbol: str,
        interval: str = "Min1",
        swing_left_bars: int = 3,
        swing_right_bars: int = 3,
        min_impulse_candles: int = 3,
        max_impulse_candles: int = 5,
        min_rejection_wick_ratio: float = 0.20,
        risk_reward_ratio: float = 2.0,
        buffer_ticks: int = 1,
        min_sl_ticks: int = 3,
        max_sl_ticks: int = 35,
        max_zone_age_bars: int = 120,
        extrema_percentile: float = 0.25,
        trend_filter_enabled: bool = True,
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
        swings: List[SwingPoint]
    ) -> List[SmartMoneyZone]:
        """
        Discovers Order Blocks based on Break of Structure (BOS).
        Rule:
        - When price closes with its BODY above a previous swing high -> Bullish BOS.
          Locate the swing low before the rally and mark the last red (bearish) candle.
        - When price closes with its BODY below a previous swing low -> Bearish BOS.
          Locate the swing high before the dump and mark the last green (bullish) candle.
        - Wicks exceeding levels without body close are strictly rejected.
        """
        discovered: List[SmartMoneyZone] = []
        n = len(closes)
        if n < 3 or not swings:
            return discovered

        swing_highs = [s for s in swings if s.is_high]
        swing_lows = [s for s in swings if not s.is_high]

        # Scan recent candles for BOS
        for i in range(max(1, n - 40), n):
            c_close = closes[i]
            c_open = opens[i]

            # 1. Check Bullish BOS (Body closes above prior swing high)
            prior_shs = [s for s in swing_highs if s.bar_idx < i]
            if prior_shs:
                recent_sh = prior_shs[-1]
                # Body must close strictly above the swing high
                if c_close > recent_sh.price and closes[i - 1] <= recent_sh.price:
                    # Find origin swing low between recent_sh and current candle
                    intervening_sls = [s for s in swing_lows if recent_sh.bar_idx < s.bar_idx < i]
                    origin_bar = intervening_sls[-1].bar_idx if intervening_sls else recent_sh.bar_idx

                    # In the vicinity of origin_bar, find the last negative (red) candle
                    origin_red_idx = None
                    for b_idx in range(min(n - 1, origin_bar + 2), max(0, origin_bar - 4), -1):
                        if b_idx < i and closes[b_idx] < opens[b_idx]:
                            origin_red_idx = b_idx
                            break

                    if origin_red_idx is not None:
                        self.zone_counter += 1
                        zid = f"OB_BULL_{self.zone_counter}_{timestamps[origin_red_idx]}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.BULLISH_ORDER_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_red_idx],
                            low=lows[origin_red_idx],
                            body_high=max(opens[origin_red_idx], closes[origin_red_idx]),
                            body_low=min(opens[origin_red_idx], closes[origin_red_idx]),
                            creation_bar_idx=origin_red_idx,
                            creation_ts=timestamps[origin_red_idx],
                            bos_bar_idx=i,
                            bos_price=c_close
                        )
                        discovered.append(zone)

            # 2. Check Bearish BOS (Body closes below prior swing low)
            prior_sls = [s for s in swing_lows if s.bar_idx < i]
            if prior_sls:
                recent_sl = prior_sls[-1]
                # Body must close strictly below the swing low
                if c_close < recent_sl.price and closes[i - 1] >= recent_sl.price:
                    # Find origin swing high between recent_sl and current candle
                    intervening_shs = [s for s in swing_highs if recent_sl.bar_idx < s.bar_idx < i]
                    origin_bar = intervening_shs[-1].bar_idx if intervening_shs else recent_sl.bar_idx

                    # In vicinity of origin_bar, find the last positive (green) candle
                    origin_green_idx = None
                    for b_idx in range(min(n - 1, origin_bar + 2), max(0, origin_bar - 4), -1):
                        if b_idx < i and closes[b_idx] > opens[b_idx]:
                            origin_green_idx = b_idx
                            break

                    if origin_green_idx is not None:
                        self.zone_counter += 1
                        zid = f"OB_BEAR_{self.zone_counter}_{timestamps[origin_green_idx]}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.BEARISH_ORDER_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_green_idx],
                            low=lows[origin_green_idx],
                            body_high=max(opens[origin_green_idx], closes[origin_green_idx]),
                            body_low=min(opens[origin_green_idx], closes[origin_green_idx]),
                            creation_bar_idx=origin_green_idx,
                            creation_ts=timestamps[origin_green_idx],
                            bos_bar_idx=i,
                            bos_price=c_close
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
        Discovers Demand and Supply Blocks based on:
        1. 3 to 5 consecutive strong candles in one direction.
        2. Creation of Imbalance / Fair Value Gap (FVG).
        3. Structural Extrema Location:
           - Demand must be in the lower 25% of recent range (structural bottom).
           - Supply must be in the upper 25% of recent range (structural top).
        4. Marking the last opposite candle before the impulse sequence.
        """
        discovered: List[SmartMoneyZone] = []
        n = len(closes)
        if n < 4:
            return discovered

        # Determine recent macro range over last 60 candles
        lookback_slice = slice(max(0, n - 60), n)
        recent_highest = max(highs[lookback_slice])
        recent_lowest = min(lows[lookback_slice])
        range_span = max(1e-12, recent_highest - recent_lowest)
        demand_ceiling = recent_lowest + range_span * self.extrema_percentile
        supply_floor = recent_highest - range_span * self.extrema_percentile

        for i in range(max(5, n - 40), n):
            # Check for Bullish Demand Block (3 to 5 consecutive green candles)
            consec_green = 0
            for k in range(i, max(-1, i - self.max_impulse_candles), -1):
                if closes[k] > opens[k]:
                    consec_green += 1
                else:
                    break

            if consec_green >= self.min_impulse_candles:
                origin_bar = i - consec_green  # The candle immediately prior to impulse
                if origin_bar >= 0 and closes[origin_bar] <= opens[origin_bar]:
                    # Check bottom extrema location
                    if lows[origin_bar] <= demand_ceiling:
                        # Check Fair Value Gap (FVG) across candle 1, 2, 3
                        # Bullish FVG: low of bar 3 > high of bar 1
                        fvg_gap = 0.0
                        if origin_bar + 2 <= i:
                            fvg_gap = max(0.0, lows[origin_bar + 2] - highs[origin_bar])

                        self.zone_counter += 1
                        zid = f"DEMAND_{self.zone_counter}_{timestamps[origin_bar]}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.DEMAND_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_bar],
                            low=lows[origin_bar],
                            body_high=max(opens[origin_bar], closes[origin_bar]),
                            body_low=min(opens[origin_bar], closes[origin_bar]),
                            creation_bar_idx=origin_bar,
                            creation_ts=timestamps[origin_bar],
                            fvg_size=fvg_gap,
                            consecutive_candles=consec_green,
                            is_extrema=True
                        )
                        discovered.append(zone)

            # Check for Bearish Supply Block (3 to 5 consecutive red candles)
            consec_red = 0
            for k in range(i, max(-1, i - self.max_impulse_candles), -1):
                if closes[k] < opens[k]:
                    consec_red += 1
                else:
                    break

            if consec_red >= self.min_impulse_candles:
                origin_bar = i - consec_red
                if origin_bar >= 0 and closes[origin_bar] >= opens[origin_bar]:
                    # Check top extrema location
                    if highs[origin_bar] >= supply_floor:
                        # Bearish FVG: high of bar 3 < low of bar 1
                        fvg_gap = 0.0
                        if origin_bar + 2 <= i:
                            fvg_gap = max(0.0, lows[origin_bar] - highs[origin_bar + 2])

                        self.zone_counter += 1
                        zid = f"SUPPLY_{self.zone_counter}_{timestamps[origin_bar]}"
                        zone = SmartMoneyZone(
                            zone_id=zid,
                            zone_type=ZoneType.SUPPLY_BLOCK,
                            symbol=self.symbol,
                            high=highs[origin_bar],
                            low=lows[origin_bar],
                            body_high=max(opens[origin_bar], closes[origin_bar]),
                            body_low=min(opens[origin_bar], closes[origin_bar]),
                            creation_bar_idx=origin_bar,
                            creation_ts=timestamps[origin_bar],
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
        # 1. Register new zones (avoid duplicate origin timestamps)
        for nz in new_zones:
            exists = any(
                z.creation_ts == nz.creation_ts and z.is_bullish == nz.is_bullish
                for z in self.active_zones.values()
            )
            if not exists:
                # Check for confluence between an OB and a Demand/Supply zone
                confluent_found = False
                for existing_id, ez in list(self.active_zones.items()):
                    if ez.status == ZoneStatus.ACTIVE and ez.is_bullish == nz.is_bullish:
                        # If price boundaries overlap significantly
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

        # 2. Evaluate active zones against current candle
        c_high = highs[current_bar_idx]
        c_low = lows[current_bar_idx]
        c_close = closes[current_bar_idx]
        c_open = opens[current_bar_idx]

        for zid, zone in list(self.active_zones.items()):
            # Expire stale zones
            if current_bar_idx - zone.creation_bar_idx > self.max_zone_age_bars:
                zone.status = ZoneStatus.EXPIRED
                del self.active_zones[zid]
                continue

            # Invalidation Check:
            # Vivek: If market directly breaks through the order block with a body close,
            # do not trade. Cancel setup immediately.
            if zone.is_bullish:
                if c_close < zone.low:
                    zone.status = ZoneStatus.INVALIDATED
                    del self.active_zones[zid]
                    continue
            else:
                if c_close > zone.high:
                    zone.status = ZoneStatus.INVALIDATED
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
        if eval_idx < 15:
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

        # Determine market structure from recent swing points if enabled
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

        # 3. Update Zone Lifecycle & Registries
        self.update_zone_lifecycle(all_new_zones, eval_idx, opens, highs, lows, closes)

        # Current evaluating candle metrics
        c_open = opens[eval_idx]
        c_high = highs[eval_idx]
        c_low = lows[eval_idx]
        c_close = closes[eval_idx]
        c_range = max(1e-12, c_high - c_low)

        # Calculate local ATR(14) for volatility & approach weakness check
        tr_list = [highs[i] - lows[i] for i in range(max(1, eval_idx - 14), eval_idx + 1)]
        current_atr = sum(tr_list) / len(tr_list) if tr_list else self._price_unit * 5.0

        pu = self._price_unit
        pu_safe = pu if pu > 0 else 0.001

        # 4. Check for Retest, Rejection Wick & Confirmation across Active Zones
        best_signal: Optional[TradeSignal] = None
        best_score: float = -1.0

        for zid, zone in list(self.active_zones.items()):
            if zone.status != ZoneStatus.ACTIVE:
                continue
            # Only evaluate zones created prior to the current candle
            if zone.creation_bar_idx >= eval_idx:
                continue

            # Approach Weakness Check:
            # Vivek: Retest should approach with weakness, not runaway climax momentum
            if c_range > 2.8 * current_atr:
                continue

            # -------------------------------------------------------------
            # Case A: Bullish Order Block / Demand Block Entry
            # -------------------------------------------------------------
            if zone.is_bullish:
                if self.preferred_direction is not None and self.preferred_direction != OrderDirection.LONG:
                    continue
                if structure_bias is not None and structure_bias != OrderDirection.LONG:
                    continue

                # 1. Zone Tap: Price tested inside or probed the upper boundary of the zone
                is_tapped = (c_low <= zone.high) and (c_high >= zone.low)
                if not is_tapped:
                    prev_idx = eval_idx - 1
                    if prev_idx >= 0:
                        is_tapped = (lows[prev_idx] <= zone.high) and (highs[prev_idx] >= zone.low)

                if not is_tapped:
                    continue

                # 2. Rejection Wick (Lower Shadow):
                # Vivek: "नीचे से bottom wick होना आवश्यक है, body directly close नहीं होनी चाहिए"
                lower_wick = min(c_open, c_close) - c_low
                has_rejection_wick = (lower_wick / c_range) >= self.min_rejection_wick_ratio

                if not has_rejection_wick:
                    continue

                # 3. Confirmation Candle Close:
                # Vivek: "Level को tap किया. Order block पे एक green candle close हुआ. अब RR लगाओ. अब यहां पे अपनी trade करो."
                is_green_confirmation = c_close > c_open and c_close > zone.low
                if not is_green_confirmation:
                    continue

                # 4. Risk & Target Geometry (1:2 RR)
                # Stop Loss strictly below Order Block low
                stop_loss_price = zone.low - (self.buffer_ticks * pu_safe)
                risk_distance = c_close - stop_loss_price
                risk_ticks = int(math.ceil(risk_distance / pu_safe))

                # Boundary guards
                if risk_ticks < self.min_sl_ticks or risk_ticks > self.max_sl_ticks:
                    continue

                target_1to1_ticks = risk_ticks
                target_1to1_price = c_close + (target_1to1_ticks * pu_safe)
                target_1to2_ticks = int(round(risk_ticks * self.risk_reward_ratio))
                target_1to2_price = c_close + (target_1to2_ticks * pu_safe)

                score = 1.0
                if zone.zone_type == ZoneType.CONFLUENT_DEMAND_OB:
                    score = 3.0
                elif zone.zone_type == ZoneType.DEMAND_BLOCK and zone.fvg_size > 0:
                    score = 2.0

                if score > best_score:
                    best_score = score
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
                        "atr": current_atr
                    }
                    best_signal = TradeSignal(
                        symbol=self.symbol,
                        direction=OrderDirection.LONG,
                        sub_strategy_name=f"{self.name}({zone.zone_type.value}-LONG)",
                        timestamp=now,
                        metadata=metadata
                    )

            # -------------------------------------------------------------
            # Case B: Bearish Order Block / Supply Block Entry
            # -------------------------------------------------------------
            elif zone.is_bearish:
                if self.preferred_direction is not None and self.preferred_direction != OrderDirection.SHORT:
                    continue
                if structure_bias is not None and structure_bias != OrderDirection.SHORT:
                    continue

                # 1. Zone Tap: Price tested inside or probed the lower boundary of the zone
                is_tapped = (c_high >= zone.low) and (c_low <= zone.high)
                if not is_tapped:
                    prev_idx = eval_idx - 1
                    if prev_idx >= 0:
                        is_tapped = (highs[prev_idx] >= zone.low) and (lows[prev_idx] <= zone.high)

                if not is_tapped:
                    continue

                # 2. Rejection Wick (Upper Shadow):
                # Vivek: "ऊपर से top wick होना आवश्यक है, sellers ने reject किया"
                upper_wick = c_high - max(c_open, c_close)
                has_rejection_wick = (upper_wick / c_range) >= self.min_rejection_wick_ratio

                if not has_rejection_wick:
                    continue

                # 3. Confirmation Candle Close:
                # Vivek: "Order block पे जाने के बाद market ने एक red candle का confirmation दिया... हमने short किया."
                is_red_confirmation = c_close < c_open and c_close < zone.high
                if not is_red_confirmation:
                    continue

                # 4. Risk & Target Geometry (1:2 RR)
                # Stop Loss strictly above Order Block high
                stop_loss_price = zone.high + (self.buffer_ticks * pu_safe)
                risk_distance = stop_loss_price - c_close
                risk_ticks = int(math.ceil(risk_distance / pu_safe))

                # Boundary guards
                if risk_ticks < self.min_sl_ticks or risk_ticks > self.max_sl_ticks:
                    continue

                target_1to1_ticks = risk_ticks
                target_1to1_price = c_close - (target_1to1_ticks * pu_safe)
                target_1to2_ticks = int(round(risk_ticks * self.risk_reward_ratio))
                target_1to2_price = c_close - (target_1to2_ticks * pu_safe)

                score = 1.0
                if zone.zone_type == ZoneType.CONFLUENT_SUPPLY_OB:
                    score = 3.0
                elif zone.zone_type == ZoneType.SUPPLY_BLOCK and zone.fvg_size > 0:
                    score = 2.0

                if score > best_score:
                    best_score = score
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
                        "atr": current_atr
                    }
                    best_signal = TradeSignal(
                        symbol=self.symbol,
                        direction=OrderDirection.SHORT,
                        sub_strategy_name=f"{self.name}({zone.zone_type.value}-SHORT)",
                        timestamp=now,
                        metadata=metadata
                    )

        if best_signal is not None:
            self.last_signal_candle_ts = current_candle_ts
            self.trade_in_progress = True
            used_zid = best_signal.metadata.get("zone_id")
            if used_zid and used_zid in self.active_zones:
                self.active_zones[used_zid].status = ZoneStatus.MITIGATED
                del self.active_zones[used_zid]

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
            "risk_reward_ratio": self.risk_reward_ratio,
            "buffer_ticks": self.buffer_ticks,
            "min_sl_ticks": self.min_sl_ticks,
            "max_sl_ticks": self.max_sl_ticks,
            "extrema_percentile": self.extrema_percentile,
            "active_zones_count": len(self.active_zones)
        }

    def get_diagnostics(self) -> Dict[str, Any]:
        return {
            "active_zones_count": len(self.active_zones),
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


# Backwards compatibility alias
OrderBookDemandStrategy = OrderBlockDemandStrategy
OrderBlockDemandSubStrategy = OrderBlockDemandStrategy
