"""
KCEX Trade Execution Engine - Models & Data Structures
======================================================
Defines core data structures for strategies, signals, execution state,
and trade outcomes with dual-currency (USDT & INR) representations.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
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
    DURATION_SCRATCH = "DURATION_SCRATCH"
    # Phase V2.1 & V2.2 Quantitative Trailing Stop and Queue Exit Markers
    RATCHET_TIGHTEN_HIT = "RATCHET_TIGHTEN_HIT"        # Exited at tightened -1 tick stop
    RATCHET_BREAKEVEN_HIT = "RATCHET_BREAKEVEN_HIT"    # Exited at 0.0 tick breakeven scratch
    QUEUE_TIMEOUT_CANCELLED = "QUEUE_TIMEOUT_CANCELLED" # Maker limit entry order timed out
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
    tp_ticks: int = 2               # Number of pu (tick size) away from entry (fixed TP)
    dynamic_tp: bool = False        # False = strictly enforce tp_ticks; True = allow dynamic 1..3 pu scaling
    sl_mode: str = "ROE"            # "ROE", "TICKS", or "PRICE_PCT"
    sl_roe_pct: float = 25.0        # -25.0% ROE (Return on Equity/Margin)
    sl_ticks: Optional[int] = None  # Number of pu ticks away from entry
    sl_price_pct: Optional[float] = None # Price move percentage away from entry
    # Trade Quantity / Volume settings (Note: Trade Quantity is NOT margin. Margin = Trade Quantity / Leverage)
    volume_mode: str = "MULTIPLIER"       # "MIN", "MULTIPLIER", or "CONTRACTS"
    volume_multiplier: float = 2.0        # x times min_volume (e.g. 2.0 = 2x min quantity for TRUMP)
    volume_contracts: Optional[int] = None # Exact number of contracts (e.g. 2)
    max_trades: int = 0                   # 0 = unlimited
    # Strategy selection
    strategy_mode: str = "STOCH_RSI"      # "STOCH_RSI" or "EMA_CROSSOVER"
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
    # Trade Optimization & Regime Filter Configuration (Toggleable)
    duration_filter_enabled: bool = False       # Master toggle for duration monitoring and exits
    duration_deep_monitor_seconds: float = 60.0 # Time in trade after which high-frequency monitoring engages
    duration_max_hold_seconds: float = 90.0     # Maximum allowable trade duration before time-decay action
    duration_action: str = "CLOSE"              # "CLOSE", "SCRATCH_OR_MARKET", or "TIGHTEN_SL"
    adx_filter_enabled: bool = False            # Gate signals when ADX < threshold (chop suppression)
    adx_period: int = 14                        # ADX smoothing period
    adx_threshold: float = 25.0                 # Minimum ADX required to allow signal execution
    htf_trend_filter_enabled: bool = False      # Higher Timeframe Trend Filter (200 EMA baseline)
    htf_timeframe: str = "15m"                  # HTF candle interval
    htf_ema_period: int = 200                   # HTF EMA period
    hourly_filter_enabled: bool = False         # Blacklist low-liquidity UTC hours
    hourly_blacklist_utc: List[int] = field(default_factory=list) # e.g. [2, 3, 4, 5, 17]
    direction_bias: str = "BOTH"                # "BOTH", "LONG_ONLY", or "SHORT_ONLY"
    # Smart Strategy Configuration (Regime-Adaptive Architecture)
    smart_atr_filter_enabled: bool = True       # Suppress entries during sub-ATR compression
    smart_min_atr_ticks: float = 2.5            # Min ATR in ticks required to ensure target feasibility
    smart_chop_ceiling: float = 58.0            # CHOP index above which market is considered dead consolidation
    smart_adx_trend_threshold: float = 26.0     # ADX threshold separating trending from ranging regimes
    smart_use_ema200_filter: bool = False       # Direction lock via 200 EMA (Default OFF per empirical validation)
    smart_ema200_period: int = 200              # 200 EMA period
    smart_climax_filter_enabled: bool = True    # Circuit breaker on volatility spikes
    smart_max_atr_expansion: float = 2.2        # Current ATR / Baseline ATR ceiling
    smart_ema_preset: str = "5/13"              # Momentum sub-strategy preset
    smart_stoch_preset: str = "FAST_SCALP"      # Mean-reversion sub-strategy preset
    smart_interval: str = "Min1"                # Candle interval for Smart Strategy evaluation
    smart_require_closed_candle: bool = True    # Confirm cross on closed candle
    # Order Execution Mode (Zero Slippage Architecture)
    order_type: str = "MARKET"                  # "MARKET" or "LIMIT" (Post-Only Maker)
    limit_order_timeout_seconds: float = 10.0   # Timeout before canceling unfilled maker orders
    # -------------------------------------------------------------------------
    # RESEARCH V2 / V2.1 / V2.2 QUANTITATIVE FEATURE TOGGLES & ENHANCEMENTS
    # -------------------------------------------------------------------------
    # 1. Signal Inversion (Fading Momentum Crosses at Extremes)
    # Researched in Phase V2.1 & V2.2: Fading Stoch RSI overbought/oversold crosses
    # produces +61% to +84% higher Profit Factor in ranging/consolidation regimes.
    invert_signal: bool = False
    dynamic_regime_fading: bool = False  # Auto-fades when ADX < adx_fading_cutoff, direct when trending
    adx_fading_cutoff: float = 28.0

    # 2. Toggleable Order Execution Architecture (Maker vs Taker)
    # "MAKER_HYBRID": Post-only Maker Limit Entry at bid1/ask1 with queue timeout,
    #                 resting limit TP (+0.00 slippage), and Ratchet Market SL.
    # "PURE_MARKET": Legacy standard execution (Taker market entry + polling market exits).
    execution_style: str = "PURE_MARKET"
    maker_queue_timeout_seconds: float = 10.0
    resting_limit_tp: bool = False

    # 3. Phase V2.2 Champion Micro-Excursion Tick Ratchet
    # Dynamic trailing stop protection: locks breakeven at +2.5 ticks and tightens stalled
    # positions at +1.0 tick after 10s to cut stop loss drawdowns.
    ratchet_enabled: bool = False
    ratchet_trigger_ticks: float = 1.0   # Favorable excursion (MFE) required for Tier 1 (+1.0 tick)
    ratchet_stall_seconds: float = 10.0  # Seconds of stall before tightening SL (10.0 seconds)
    ratchet_tighten_ticks: float = 1.0   # Tightened SL distance (-1.0 tick)
    ratchet_breakeven_ticks: float = 2.5 # Favorable excursion required to lock at Breakeven (+2.5 ticks)

    # 4. Realistic Slippage Engine (Synchronized across Local, GitHub Actions & Dry-Run)
    # When enabled, shifts entry fill and market stop exits adversely by slippage_ticks.
    slippage_enabled: bool = False
    slippage_ticks: int = 1              # Integer ticks of adverse friction (e.g. 1t, 2t, 3t)

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
