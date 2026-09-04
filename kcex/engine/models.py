"""
KCEX Trade Execution Engine - Models & Data Structures
======================================================
Defines core data structures for strategies, signals, execution state,
and trade outcomes with dual-currency (USDT & INR) representations.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum
import time
import os


class OrderDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class ExitReason(str, Enum):
    MIN_PROFIT_TP_HIT = "MIN_PROFIT_TP_HIT"
    IMMEDIATE_PROFIT_CLOSE = "IMMEDIATE_PROFIT_CLOSE"
    STOP_LOSS_HIT = "STOP_LOSS_HIT"
    SCRATCH_CLOSE = "SCRATCH_CLOSE"
    MANUAL_CLOSE = "MANUAL_CLOSE"
    TIMEOUT_CLOSE = "TIMEOUT_CLOSE"
    UNKNOWN = "UNKNOWN"


class EngineMode(str, Enum):
    LIVE = "live"
    DRY_RUN = "dry-run"


@dataclass
class TradeSignal:
    """Signal produced by a strategy or sub-strategy."""
    symbol: str
    direction: OrderDirection
    sub_strategy_name: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionConfig:
    """Execution parameters for the automated engine."""
    symbol: str = field(default_factory=lambda: os.getenv("KCEX_SYMBOL", "TRUMP_USDT"))
    direction: OrderDirection = OrderDirection.LONG
    mode: EngineMode = EngineMode.DRY_RUN
    leverage: int = 75
    is_isolated: bool = True
    cooldown_seconds: float = 30.0
    tp_ticks: int = 1               # Number of pu (tick size) away from entry
    dynamic_tp: bool = False        # False = strictly enforce tp_ticks; True = allow dynamic 1..3 pu scaling
    sl_mode: str = "ROE"            # "ROE", "TICKS", or "PRICE_PCT"
    sl_roe_pct: float = 10.0        # -10% ROE (Return on Equity/Margin)
    sl_ticks: Optional[int] = None  # Number of pu ticks away from entry
    sl_price_pct: Optional[float] = None # Price move percentage away from entry
    # Trade Quantity / Volume settings (Note: Trade Quantity is NOT margin. Margin = Trade Quantity / Leverage)
    volume_mode: str = "MULTIPLIER"       # "MIN", "MULTIPLIER", or "CONTRACTS"
    volume_multiplier: float = 1.0        # x times min_volume (e.g. 1.0 = 1x, 2.0 = 2x)
    volume_contracts: Optional[int] = None # Exact number of contracts (e.g. 5)
    max_trades: int = 0                   # 0 = unlimited
    # Strategy selection
    strategy_mode: str = "CYCLE"          # "EMA_CROSSOVER", "STOCH_RSI", "MICROSTRUCTURE", or "CYCLE" (default for bare config is CYCLE)
    bi_directional: bool = True           # True for autonomous Long/Short, False for fixed direction
    ema_preset: str = "5/13"              # "5/13", "9/21", "3/8", or "custom"
    ema_fast: int = 5                     # Fast EMA length
    ema_slow: int = 13                    # Slow EMA length
    ema_interval: str = "Min1"            # Candle timeframe e.g. "Min1", "Min5"
    ema_require_closed_candle: bool = True # Confirm cross on closed candle (prevents false whipsaw repainting)
    # Stochastic RSI Configuration
    stoch_preset: str = "FAST_SCALP"      # "FAST_SCALP", "STANDARD", "MICRO_BURST", "custom"
    stoch_rsi_period: int = 9             # RSI calculation period
    stoch_period: int = 9                 # Stochastic period over RSI
    stoch_k_period: int = 3               # %K smoothing period
    stoch_d_period: int = 3               # %D smoothing period
    stoch_oversold: float = 20.0          # Oversold threshold
    stoch_overbought: float = 80.0        # Overbought threshold
    stoch_interval: str = "Min1"          # Candle timeframe
    stoch_zone_filter: bool = True        # Gate crossovers to extreme zones
    stoch_require_closed_candle: bool = True # Confirm cross on closed candle
    poll_interval_seconds: float = 0.5
    logs_dir: str = "logs"
    realtime_log_file: str = "engine_realtime.log"
    outcomes_log_file: str = "trade_outcomes.txt"
    outcomes_jsonl_file: str = "trade_outcomes.jsonl"



@dataclass
class TradeOutcome:
    """Complete record of an executed and closed trade."""
    trade_id: int
    symbol: str
    direction: OrderDirection
    sub_strategy_name: str
    mode: EngineMode
    
    # Contract details
    leverage: int
    vol_contracts: int
    contract_size: float
    underlying_quantity: float
    
    # Prices
    entry_price: float
    exit_price: float
    min_profit_tp_price: float
    stop_loss_price: float
    price_unit: float              # pu / tick size
    
    # Timing
    open_time: float
    close_time: float
    duration_seconds: float
    
    # Financial metrics in USDT and INR
    notional_value_usdt: float
    notional_value_inr: float
    margin_used_usdt: float
    margin_used_inr: float
    
    realized_pnl_usdt: float
    realized_pnl_inr: float
    pnl_percentage: float          # Price move %
    roe_percentage: float          # ROE % on margin
    
    base_coin: str = ""
    price_precision: int = 4
    
    fee_open_usdt: float = 0.0
    fee_close_usdt: float = 0.0
    fee_total_usdt: float = 0.0
    fee_total_inr: float = 0.0
    
    inr_rate: float = 94.45
    exit_reason: ExitReason = ExitReason.UNKNOWN
    
    # Live wallet balance after this trade
    balance_after_trade_usdt: Optional[float] = None
    balance_after_trade_inr: Optional[float] = None

    # Server references
    order_id: Optional[str] = None
    close_order_id: Optional[str] = None
    position_id: Optional[int] = None

    @property
    def is_profit(self) -> bool:
        return self.realized_pnl_usdt > 0.0

    @property
    def is_loss(self) -> bool:
        return self.realized_pnl_usdt < -1e-8

    @property
    def is_scratch(self) -> bool:
        return abs(self.realized_pnl_usdt) <= 1e-8


@dataclass
class CumulativeStats:
    """Cumulative performance statistics across multiple trades."""
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    scratch_trades: int = 0
    total_pnl_usdt: float = 0.0
    total_pnl_inr: float = 0.0
    total_fees_usdt: float = 0.0
    total_fees_inr: float = 0.0
    best_trade_usdt: float = 0.0
    worst_trade_usdt: float = 0.0

    @property
    def win_rate_pct(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return (self.winning_trades / self.total_trades) * 100.0

    def update(self, outcome: TradeOutcome) -> None:
        self.total_trades += 1
        self.total_pnl_usdt += outcome.realized_pnl_usdt
        self.total_pnl_inr += outcome.realized_pnl_inr
        self.total_fees_usdt += outcome.fee_total_usdt
        self.total_fees_inr += outcome.fee_total_inr

        if outcome.is_scratch:
            self.scratch_trades += 1
        elif outcome.is_profit:
            self.winning_trades += 1
        else:
            self.losing_trades += 1

        if outcome.realized_pnl_usdt > self.best_trade_usdt:
            self.best_trade_usdt = outcome.realized_pnl_usdt
        if outcome.realized_pnl_usdt < self.worst_trade_usdt:
            self.worst_trade_usdt = outcome.realized_pnl_usdt
