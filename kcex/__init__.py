"""
KCEX Trading Bot Package
========================
A comprehensive Python toolkit for automated futures trading and trade management on KCEX.

Exports:
- KCEXConfig: API endpoints and credentials configuration
- KCEXClient, KCEXAPIError: Core HTTP client with session signing
- KCEXMarket, ContractInfo: Real-time market data, contract specs, depth, klines
- KCEXRiskCalculator, RiskAnalysisReport: Liquidation, fees, TP/SL, and dual currency (USDT & INR)
- KCEXTrader: Order creation, position TP/SL, partial closing, cancellations
- KCEXSigner: Reverse-engineered MD5 request signing
"""

from kcex.config import KCEXConfig
from kcex.signer import KCEXSigner
from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator, RiskAnalysisReport
from kcex.trade import KCEXTrader
from kcex.engine import (
    TradeExecutionEngine,
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    ExitReason,
    TradeSignal,
    TradeOutcome,
    CumulativeStats,
    MasterplanStrategy,
    DirectionalCycleSubStrategy,
    DualCurrencyLogger,
    TradeOutcomeLogger
)

__version__ = "1.1.0"
__all__ = [
    "KCEXConfig",
    "KCEXSigner",
    "KCEXClient",
    "KCEXAPIError",
    "KCEXMarket",
    "ContractInfo",
    "KCEXRiskCalculator",
    "RiskAnalysisReport",
    "KCEXTrader",
    "TradeExecutionEngine",
    "ExecutionConfig",
    "OrderDirection",
    "EngineMode",
    "ExitReason",
    "TradeSignal",
    "TradeOutcome",
    "CumulativeStats",
    "MasterplanStrategy",
    "DirectionalCycleSubStrategy",
    "DualCurrencyLogger",
    "TradeOutcomeLogger",
]
