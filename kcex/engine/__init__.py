"""
KCEX Automated Execution Engine Package
=======================================
Exports:
- TradeExecutionEngine: Core automated trade execution engine
- ExecutionConfig, OrderDirection, EngineMode, ExitReason: Engine models
- MasterplanStrategy, DirectionalCycleSubStrategy, BaseSubStrategy: Strategies
- DualCurrencyLogger, TradeOutcomeLogger: Dual-currency loggers
- TradeOutcome, CumulativeStats: Trade recording and analytics
"""

from kcex.engine.models import (
    OrderDirection,
    ExitReason,
    EngineMode,
    TradeSignal,
    ExecutionConfig,
    TradeOutcome,
    CumulativeStats
)
from kcex.engine.logger import DualCurrencyLogger, TradeOutcomeLogger
from kcex.engine.strategy import (
    BaseSubStrategy,
    DirectionalCycleSubStrategy,
    MicrostructureSubStrategy,
    EMACrossoverSubStrategy,
    EMA_PRESETS,
    compute_ema_series,
    StochasticRSISubStrategy,
    STOCH_RSI_PRESETS,
    compute_stoch_rsi,
    compute_rsi_series,
    MasterplanStrategy
)
from kcex.engine.microstructure import (
    MicrostructureSignalGenerator,
    SignalConfig,
    SymbolMeta,
    RollingZ,
    EMA
)
from kcex.engine.executor import TradeExecutionEngine

__all__ = [
    "OrderDirection",
    "ExitReason",
    "EngineMode",
    "TradeSignal",
    "ExecutionConfig",
    "TradeOutcome",
    "CumulativeStats",
    "DualCurrencyLogger",
    "TradeOutcomeLogger",
    "BaseSubStrategy",
    "DirectionalCycleSubStrategy",
    "MicrostructureSubStrategy",
    "EMACrossoverSubStrategy",
    "EMA_PRESETS",
    "compute_ema_series",
    "StochasticRSISubStrategy",
    "STOCH_RSI_PRESETS",
    "compute_stoch_rsi",
    "compute_rsi_series",
    "MicrostructureSignalGenerator",
    "SignalConfig",
    "SymbolMeta",
    "RollingZ",
    "EMA",
    "MasterplanStrategy",
    "TradeExecutionEngine",
]

