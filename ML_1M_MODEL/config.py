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
    
    # Dataset splitting protocol
    split_mode: str = "calendar"         # "calendar" enforces strict date isolation; "ratio" is fallback
    train_start_date: str = "2026-06-01" # Start of training set
    train_end_date: str = "2026-07-31"   # End of training set (strict zero August leakage)
    val_start_date: str = "2026-07-16"   # Inner validation start date (for hyperparameter tuning)
    val_end_date: str = "2026-07-31"     # Inner validation end date
    test_start_date: str = "2026-08-01"  # Pure unseen out-of-sample test start
    test_end_date: str = "2026-08-31"    # Pure unseen out-of-sample test end
    embargo_bars: int = 30               # 30-bar embargo window between train and test/validation splits
    test_size: float = 0.2               # Fallback ratio if split_mode == "ratio"

    # Prediction horizon & barrier labeling
    horizon_bars: int = 30              # Forward horizon bars
    tp_atr_mult: float = 2.8            # Dynamic Take Profit: ATR multiplier
    sl_atr_mult: float = 1.2            # Dynamic Stop Loss: ATR multiplier
    label_tp_mult: float = 2.8          # Structural Take Profit multiplier for training labels
    label_sl_mult: float = 1.2          # Structural invalidation multiplier for training labels
    min_profit_pct: float = 0.0020      # Minimum profit hurdle to ensure edge exceeds slippage

    # Signal probability thresholds
    confidence_threshold: float = 0.40       # Long calibrated probability threshold
    confidence_threshold_sell: float = 0.48  # Short calibrated probability threshold
    edge_threshold: float = 0.03             # Margin over alternative classes
    order_flow_filter: bool = True          # Require order-flow confirmation
    macro_regime_filter: bool = True        # Directional macro regime gating

    # Execution and Cost Simulation
    maker_fee: float = 0.0             # 0% maker fee on KCEX
    taker_fee: float = 0.0             # 0% taker fee for TRUMP and DOGE on KCEX
    slippage_ticks: float = 2.0        # 2 ticks conservative slippage baseline
    leverage: float = 20.0             # Leverage for margin calculations

    # Model Hyperparameters (Scikit-Learn HistGradientBoosting with L2 Regularization & Early Stopping)
    hgb_params: Dict = field(default_factory=lambda: {
        "max_iter": 250,
        "learning_rate": 0.03,
        "max_leaf_nodes": 31,
        "max_depth": 5,
        "min_samples_leaf": 50,
        "l2_regularization": 3.0,
        "early_stopping": True,
        "validation_fraction": 0.15,
        "n_iter_no_change": 15,
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


def get_model_config(symbol: str, preset: str = "rapid") -> ModelConfig:
    """Returns the empirically verified, hyperparameter-tuned ModelConfig for a given symbol."""
    clean_sym = normalize_symbol_name(symbol)
    if "TRUMP" in clean_sym:
        if preset == "macro":
            return ModelConfig(
                symbol="TRUMPUSDT",
                horizon_bars=45,
                min_profit_pct=0.0080,
                tp_atr_mult=3.5,
                sl_atr_mult=1.8,
                label_tp_mult=3.5,
                label_sl_mult=1.8,
                confidence_threshold=0.45,
                confidence_threshold_sell=0.45,
                edge_threshold=0.03,
                macro_regime_filter=True,
                embargo_bars=45,
                slippage_ticks=2.0
            )
        else:
            # Rapid Scalping Preset (High Frequency: ~80-100 trades/mo, 10-15m horizons, rapid compounding)
            return ModelConfig(
                symbol="TRUMPUSDT",
                horizon_bars=12,
                min_profit_pct=0.0028,
                tp_atr_mult=1.9,
                sl_atr_mult=1.0,
                label_tp_mult=1.9,
                label_sl_mult=1.0,
                confidence_threshold=0.38,
                confidence_threshold_sell=0.38,
                edge_threshold=0.015,
                macro_regime_filter=False,
                embargo_bars=20,
                slippage_ticks=2.0
            )
    elif "DOGE" in clean_sym:
        return ModelConfig(
            symbol="DOGEUSDT",
            horizon_bars=60,
            min_profit_pct=0.0040,
            tp_atr_mult=4.0,
            sl_atr_mult=2.0,
            label_tp_mult=4.0,
            label_sl_mult=2.0,
            confidence_threshold=0.45,
            confidence_threshold_sell=0.45,
            edge_threshold=0.03,
            slippage_ticks=2.0,
            hgb_params={
                "max_iter": 150,
                "learning_rate": 0.04,
                "max_leaf_nodes": 31,
                "max_depth": 5,
                "min_samples_leaf": 50,
                "l2_regularization": 3.0,
                "early_stopping": True,
                "validation_fraction": 0.15,
                "n_iter_no_change": 15,
                "random_state": 42
            }
        )
    else:
        return ModelConfig(symbol=symbol)

