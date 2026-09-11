"""
ML_1M_MODEL Configuration
=========================
Central configuration for data paths, symbol tick specifics,
feature engineering horizons, barrier labeling, and training hyperparameters.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Primary Local Storage Paths (user's drive)
LOCAL_OHLCV_DIR = r"D:\My_Bots\Trading\BINANCE_DATA\OHLCV_Data\binance_futures_ohlcv"
LOCAL_TRADES_DIR = r"D:\My_Bots\Trading\BINANCE_DATA\Tick_Trades_Data\binance_futures_trades"

# Cloud / CI Fallback Storage Paths (used in GitHub Actions or fallback)
FALLBACK_DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CLOUD_OHLCV_DIR = os.path.join(FALLBACK_DATA_DIR, "binance_futures_ohlcv")
CLOUD_TRADES_DIR = os.path.join(FALLBACK_DATA_DIR, "binance_futures_trades")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data_cache")
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Ensure required directories exist
for d in [PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Symbol metadata: tick size (pu) and min contract specs
SYMBOL_TICK_SPECS: Dict[str, Dict[str, float]] = {
    "TRUMPUSDT": {
        "tick_size": 0.001,
        "price_precision": 3,
        "min_qty": 0.1,
    },
    "TRUMP_USDT": {
        "tick_size": 0.001,
        "price_precision": 3,
        "min_qty": 0.1,
    },
    "DOGEUSDT": {
        "tick_size": 0.00001,
        "price_precision": 5,
        "min_qty": 10.0,
    },
    "DOGE_USDT": {
        "tick_size": 0.00001,
        "price_precision": 5,
        "min_qty": 10.0,
    },
    "BTCUSDT": {
        "tick_size": 0.1,
        "price_precision": 1,
        "min_qty": 0.001,
    },
    "BTC_USDT": {
        "tick_size": 0.1,
        "price_precision": 1,
        "min_qty": 0.001,
    },
}

DEFAULT_TICK_SPEC = {
    "tick_size": 0.0001,
    "price_precision": 4,
    "min_qty": 1.0,
}


def normalize_symbol_name(symbol: str) -> str:
    """Normalizes symbol representations (e.g. 'TRUMP_USDT' -> 'TRUMPUSDT')."""
    return symbol.upper().replace("-", "").replace("_", "")


def get_tick_spec(symbol: str) -> Dict[str, float]:
    """Retrieves tick precision specification for a symbol."""
    clean_sym = normalize_symbol_name(symbol)
    for k, v in SYMBOL_TICK_SPECS.items():
        if normalize_symbol_name(k) == clean_sym:
            return v
    return DEFAULT_TICK_SPEC


def get_fee_schedule(symbol: str) -> Tuple[float, float]:
    """
    Returns (maker_fee, taker_fee).
    Zero fees for TRUMP and DOGE on KCEX.
    0.01% (0.0001) taker fee for other pairs (no maker fee).
    """
    clean_sym = normalize_symbol_name(symbol)
    if "TRUMP" in clean_sym or "DOGE" in clean_sym:
        return 0.0, 0.0
    return 0.0, 0.0001


@dataclass
class ModelConfig:
    # Asset parameters
    symbol: str = "TRUMPUSDT"
    timeframe: str = "1m"
    start_date: str = "2026-06-01"
    end_date: str = "2026-08-31"

    # Prediction horizon & barrier labeling
    horizon_bars: int = 15              # Look forward N bars (15 1m bars = 15 minutes)
    tp_atr_mult: float = 3.0           # Dynamic Take Profit: 3.0x ATR (high reward-to-risk)
    sl_atr_mult: float = 1.5           # Dynamic Stop Loss: 1.5x ATR
    min_profit_pct: float = 0.005      # Minimum profit hurdle (0.5%) to ensure fees/slippage are negligible

    # Signal probability thresholds
    confidence_threshold: float = 0.70  # Empirically verified high-conviction sniper threshold (51.2% WR, PF 2.13)
    edge_threshold: float = 0.05        # Margin over alternative classes
    order_flow_filter: bool = True     # Require order-flow imbalance confirmation

    # Execution and Cost Simulation
    maker_fee: float = 0.0             # 0% maker fee on KCEX
    taker_fee: float = 0.0             # 0% taker fee for TRUMP and DOGE (auto-resolved via get_fee_schedule)
    slippage_ticks: float = 2.0        # 2 ticks conservative slippage baseline
    leverage: float = 20.0             # Leverage for margin calculations

    # Validation and Splitting
    test_size: float = 0.2             # Chronological out-of-sample test fraction
    embargo_bars: int = 30             # Purged embargo gap to eliminate leakage

    # Model Hyperparameters (Scikit-Learn HistGradientBoosting)
    hgb_params: Dict = field(default_factory=lambda: {
        "max_iter": 200,
        "learning_rate": 0.04,
        "class_weight": "balanced",
        "max_leaf_nodes": 31,
        "max_depth": 6,
        "random_state": 42
    })

    # Class ID mapping
    # 0 = WAIT/HOLD, 1 = BUY, 2 = SELL
    CLASS_WAIT: int = 0
    CLASS_BUY: int = 1
    CLASS_SELL: int = 2

    # String mapping
    CLASS_NAMES: Dict[int, str] = field(default_factory=lambda: {
        0: "WAIT / HOLD",
        1: "BUY",
        2: "SELL"
    })
