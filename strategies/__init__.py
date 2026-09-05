"""
Modular Strategies Package
==========================
Exports standardized, modular trading strategies and mathematical routines for KCEX:
- BaseStrategy: Strategy lifecycle interface
- EMACrossoverStrategy: Fast/Slow EMA crossover momentum/trend trading
- StochasticRSIStrategy: High-frequency Stochastic RSI mean-reversion & momentum scalping
"""

from strategies.base import BaseStrategy, BaseSubStrategy
from strategies.ema_crossover import (
    EMACrossoverStrategy,
    EMACrossoverSubStrategy,
    EMA_PRESETS,
    compute_ema_series
)
from strategies.stoch_rsi import (
    StochasticRSIStrategy,
    StochasticRSISubStrategy,
    STOCH_RSI_PRESETS,
    compute_rsi_series,
    compute_stoch_rsi
)

from strategies.filters import (
    BaseFilter,
    HTFTrendFilter,
    ADXRegimeFilter,
    HourlySessionFilter,
    DirectionalBiasFilter,
    FilterPipeline,
    compute_atr_series,
    compute_adx_series
)

__all__ = [
    "BaseStrategy",
    "BaseSubStrategy",
    "EMACrossoverStrategy",
    "EMACrossoverSubStrategy",
    "EMA_PRESETS",
    "compute_ema_series",
    "StochasticRSIStrategy",
    "StochasticRSISubStrategy",
    "STOCH_RSI_PRESETS",
    "compute_rsi_series",
    "compute_stoch_rsi",
    "BaseFilter",
    "HTFTrendFilter",
    "ADXRegimeFilter",
    "HourlySessionFilter",
    "DirectionalBiasFilter",
    "FilterPipeline",
    "compute_atr_series",
    "compute_adx_series",
]
