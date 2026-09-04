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
    MasterplanStrategy
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
    "MasterplanStrategy",
    "TradeExecutionEngine",
]
