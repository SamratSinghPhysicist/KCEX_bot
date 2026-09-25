"""
Order Block + Demand Zone Strategy with Fee Coverage + 2 Ticks TP
==================================================================
New Experiment Strategy:
Preserves the exact structural detection, swing pivots, Break of Structure (BOS),
Order Block identification, and Stop Loss placement of the original Vivek Yadav
OB + Demand strategy.

Changes the Take Profit (TP) target:
- Replaces the 1:2 R:R (with 50% partial TP at 1:1) with a rapid-scalp guaranteed
  net profit target placed at exactly:
    TP = Entry ± (Fee Coverage Ticks + 2 Ticks)
- Fully exits the entire position at this TP (partial TP disabled).
- SL remains strictly anchored at the Order Block boundary (low for long, high for short).
"""

from __future__ import annotations
import math
import os
import sys
import logging
from typing import Optional, Dict, Any, List

# Ensure project root is in sys.path
EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from kcex.engine.models import OrderDirection, TradeSignal, TradeOutcome
from strategies.order_block_demand import (
    OrderBlockDemandStrategy,
    SmartMoneyZone,
    ZoneType,
    ZoneStatus,
    SwingPoint
)

logger = logging.getLogger("FeePlus2TicksOBStrategy")


def compute_fee_coverage_ticks(
    entry_price: float,
    taker_fee_rate: float,
    price_unit: float,
    extra_ticks: int = 2
) -> Tuple[int, int]:
    """
    Computes:
    1. fee_ticks: minimum ticks needed to cover 100% round-trip taker fees (entry + exit market orders).
    2. target_ticks: fee_ticks + extra_ticks.

    Mathematical Derivation:
    - Entry notional = Q * entry_price
    - Entry fee = Q * entry_price * taker_fee_rate
    - Exit fee = Q * exit_price * taker_fee_rate
    - Total fees = Q * (entry_price + exit_price) * taker_fee_rate
    - For Long: Gross Gain = Q * (exit_price - entry_price)
      Net Gain = Gross Gain - Total Fees = Q * (exit_price * (1 - taker_fee_rate) - entry_price * (1 + taker_fee_rate))
      To break even (Net Gain = 0):
        exit_price = entry_price * (1 + taker_fee_rate) / (1 - taker_fee_rate)
        delta_p_fees = exit_price - entry_price = entry_price * (2 * taker_fee_rate) / (1 - taker_fee_rate)
    - Ticks to cover fees: ceil(delta_p_fees / price_unit)
    - Target ticks = fee_ticks + extra_ticks
    """
    if price_unit <= 0:
        price_unit = 0.001

    denom = max(1e-9, 1.0 - taker_fee_rate)
    delta_p_fees = entry_price * (2.0 * taker_fee_rate) / denom
    fee_ticks = max(1, int(math.ceil(round(delta_p_fees / price_unit, 8))))
    target_ticks = fee_ticks + extra_ticks
    return fee_ticks, target_ticks


class FeePlus2TicksOBStrategy(OrderBlockDemandStrategy):
    """
    Subclass of OrderBlockDemandStrategy that modifies the Take Profit logic:
    - SL remains identical (anchored to OB boundary + buffer ticks).
    - TP is set to Fee Coverage + 2 Ticks.
    - Partial TP at 1:1 is disabled (100% exit at the fee-plus-2-ticks TP).
    """

    def __init__(
        self,
        market: Any,
        symbol: str,
        interval: str = "Min15",
        pivot_len: int = 5,
        swing_left_bars: Optional[int] = None,
        swing_right_bars: Optional[int] = None,
        min_impulse_candles: int = 2,
        max_impulse_candles: int = 4,
        min_rejection_wick_ratio: float = 0.15,
        buffer_ticks: int = 0,
        min_sl_ticks: int = 1,
        max_sl_ticks: int = 100,
        max_zone_age_bars: int = 120,
        extrema_percentile: float = 0.25,
        trend_filter_enabled: bool = False,
        preferred_direction: Optional[OrderDirection] = None,
        cooldown_seconds: float = 0.0,
        require_closed_candle: bool = True,
        auto_start_feed: bool = False,
        extra_ticks: int = 2,
        taker_fee_override: Optional[float] = None,
        name: str = "OrderBlockDemandFeePlus2Ticks"
    ):
        # Initialize base OrderBlockDemandStrategy with partial_tp_enabled=False
        super().__init__(
            market=market,
            symbol=symbol,
            interval=interval,
            pivot_len=pivot_len,
            swing_left_bars=swing_left_bars,
            swing_right_bars=swing_right_bars,
            min_impulse_candles=min_impulse_candles,
            max_impulse_candles=max_impulse_candles,
            min_rejection_wick_ratio=min_rejection_wick_ratio,
            risk_reward_ratio=1.0,  # Overridden dynamically by fee + extra ticks
            buffer_ticks=buffer_ticks,
            min_sl_ticks=min_sl_ticks,
            max_sl_ticks=max_sl_ticks,
            max_zone_age_bars=max_zone_age_bars,
            extrema_percentile=extrema_percentile,
            trend_filter_enabled=trend_filter_enabled,
            partial_tp_enabled=False,
            breakeven_buffer_ticks=1,
            preferred_direction=preferred_direction,
            cooldown_seconds=cooldown_seconds,
            require_closed_candle=require_closed_candle,
            auto_start_feed=auto_start_feed,
            name=name
        )
        self.extra_ticks = extra_ticks
        self.taker_fee_override = taker_fee_override

    def generate_signal(self, symbol: str) -> Optional[TradeSignal]:
        """
        Runs the exact Vivek Yadav Order Block detection, BOS, retest and confirmation rules.
        When an entry signal is identified, adjusts TP to:
            TP = Entry ± (Fee Coverage Ticks + 2 Ticks)
        Keeps SL at the exact order block boundary.
        """
        signal = super().generate_signal(symbol)
        if signal is None:
            return None

        self._refresh_contract_spec()
        pu = self._price_unit if self._price_unit > 0 else 0.001
        prec = self._price_precision

        contract = self.market.get_contract_detail(self.symbol)
        taker_fee = self.taker_fee_override if self.taker_fee_override is not None else contract.taker_fee_rate

        entry_price = float(signal.metadata.get("entry_price", 0.0))
        if entry_price <= 0:
            return signal

        # Calculate exact fee coverage ticks and extra ticks
        fee_ticks, target_ticks = compute_fee_coverage_ticks(
            entry_price=entry_price,
            taker_fee_rate=taker_fee,
            price_unit=pu,
            extra_ticks=self.extra_ticks
        )

        direction = signal.direction
        if direction == OrderDirection.LONG:
            tp_price = round(entry_price + (target_ticks * pu), prec)
        else:
            tp_price = round(entry_price - (target_ticks * pu), prec)

        # SL is preserved exactly as calculated by super().generate_signal()
        sl_price = float(signal.metadata.get("stop_loss_price", 0.0))
        target_sl_ticks = int(signal.metadata.get("target_sl_ticks", 1))

        # Update metadata to reflect the experiment configuration
        signal.metadata["target_ticks"] = target_ticks
        signal.metadata["take_profit_price"] = tp_price
        signal.metadata["target_1to2_ticks"] = target_ticks
        signal.metadata["target_1to2_price"] = tp_price
        signal.metadata["target_1to1_ticks"] = target_ticks
        signal.metadata["target_1to1_price"] = tp_price
        signal.metadata["fee_coverage_ticks"] = fee_ticks
        signal.metadata["extra_ticks"] = self.extra_ticks
        signal.metadata["round_trip_taker_fee_rate"] = taker_fee * 2.0
        signal.metadata["partial_tp_enabled"] = False
        signal.metadata["strategy_mode"] = "ORDER_BLOCK_DEMAND_FEE_PLUS_2TICKS"
        signal.sub_strategy_name = f"FeePlus2TicksOB({signal.metadata.get('zone_type', 'OB')}-{direction.name})"

        return signal
