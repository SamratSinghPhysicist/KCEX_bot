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
        self.sub_strategy = sub_strategy or DirectionalCycleSubStrategy(
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
                clamped_sl = approx_liq + (2 * price_unit)
                # Ensure clamped SL is below entry
                if clamped_sl < entry_price:
                    logger.warning(
                        f"Liquidation Guard: Requested SL {sl_price:.{precision}f} was at/past liq price {approx_liq:.{precision}f}. Clamped to {clamped_sl:.{precision}f}."
                    )
                    sl_price = clamped_sl
        else:
            sl_price = entry_price + price_offset
            # Liquidation price for Short: Entry * (1 + 1/leverage - mmr)
            approx_liq = entry_price * (1.0 + (1.0 / float(max(1, leverage))) - mmr)
            if sl_price >= approx_liq:
                clamped_sl = approx_liq - (2 * price_unit)
                # Ensure clamped SL is above entry
                if clamped_sl > entry_price:
                    logger.warning(
                        f"Liquidation Guard: Requested SL {sl_price:.{precision}f} was at/past liq price {approx_liq:.{precision}f}. Clamped to {clamped_sl:.{precision}f}."
                    )
                    sl_price = clamped_sl

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

    def start(self) -> None:
        """Starts sub-strategy resources (e.g. WebSocket feeds)."""
        self.sub_strategy.start()

    def stop(self) -> None:
        """Stops sub-strategy resources."""
        self.sub_strategy.stop()

    def get_diagnostics(self) -> Dict[str, Any]:
        """Returns live sub-strategy diagnostics."""
        return self.sub_strategy.get_diagnostics()

