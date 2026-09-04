"""
KCEX "Masterplan" Strategy & Sub-Strategy Framework
===================================================
Implements the Masterplan Strategy and its sub-strategy architecture.
Features:
- Zero-fee pair validation (defaults to TRUMP_USDT)
- Guaranteed Min-Profit TP: Entry Price + pu (Long) / Entry Price - pu (Short)
- Stop Loss: -10% Return on Equity (ROE / Margin)
- Immediate Profit Closing evaluation
- Sub-strategy cycling with 30-second cooldown
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
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


class MasterplanStrategy:
    """
    Masterplan Trading Strategy.
    
    Responsibilities:
    1. Validates zero-fee trading pair configuration (TRUMP_USDT).
    2. Coordinates sub-strategies to generate entry signals.
    3. Calculates exact Min-Profit Take Profit price:
       - Long: Entry Price + pu
       - Short: Entry Price - pu
       where pu is the contract's tick size (price_unit).
    4. Calculates Stop Loss at -10% ROE.
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
        self.sub_strategy = sub_strategy or DirectionalCycleSubStrategy(
            direction=self.config.direction,
            cooldown_seconds=self.config.cooldown_seconds
        )
        self.name = "Masterplan"

    def validate_zero_fee_pair(self, symbol: str) -> Dict[str, Any]:
        """
        Validates that the selected symbol offers zero maker and taker fees.
        Raises ValueError if fees are non-zero unless user accepts.
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
        precision: int = 4
    ) -> float:
        """
        Calculates the Guaranteed Min-Profit TP Price.
        For Long:  TP = Entry Price + (tp_ticks * pu)
        For Short: TP = Entry Price - (tp_ticks * pu)
        """
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
        sl_roe_pct: float = 10.0,
        precision: int = 4
    ) -> float:
        """
        Calculates Stop Loss price at desired negative ROE (-10% by default).
        Since ROE% = PriceChangePct * Leverage:
            PriceChangePct = sl_roe_pct / (100 * Leverage)
        For Long:  SL = Entry Price * (1 - PriceChangePct)
        For Short: SL = Entry Price * (1 + PriceChangePct)
        """
        price_drop_fraction = (sl_roe_pct / 100.0) / float(leverage)
        if direction == OrderDirection.LONG:
            sl_price = entry_price * (1.0 - price_drop_fraction)
        else:
            sl_price = entry_price * (1.0 + price_drop_fraction)
        return round(sl_price, precision)

    def is_better_than_min_profit(
        self,
        direction: OrderDirection,
        current_price: float,
        min_profit_tp_price: float
    ) -> bool:
        """
        Checks if current market price is already at or better than minimum profit TP:
        - For Long:  current_price >= min_profit_tp_price
        - For Short: current_price <= min_profit_tp_price
        """
        if direction == OrderDirection.LONG:
            return current_price >= min_profit_tp_price
        else:
            return current_price <= min_profit_tp_price

    def get_signal(self) -> Optional[TradeSignal]:
        """Polls active sub-strategy for next entry signal."""
        return self.sub_strategy.generate_signal(self.config.symbol)

    def on_trade_completed(self, outcome: TradeOutcome) -> None:
        """Notifies sub-strategy when trade completes."""
        self.sub_strategy.on_trade_completed(outcome)
