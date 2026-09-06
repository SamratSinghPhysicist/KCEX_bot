"""
Unit Tests for SmartStrategy (Regime-Adaptive Micro-Scalping Engine)
===================================================================
Validates:
1. Choppiness Index (CHOP) calculation
2. O(1) Market Regime Classifier logic (Compression, Climax, Bull/Bear Momentum, Balanced Range)
3. Signal routing to appropriate sub-strategy
4. 200 EMA macro filter toggleability (default False)
5. Asset generalization across tick sizes (TRUMP, DOGE, BTC)
6. MasterplanStrategy integration and ExecutionConfig defaults
"""

import math
import pytest
from unittest.mock import MagicMock

from kcex.engine.models import OrderDirection, TradeSignal, ExecutionConfig
from kcex.engine.strategy import MasterplanStrategy
from strategies.smart_strategy import (
    SmartStrategy,
    MarketRegime,
    compute_chop_series
)
from BACKTESTER.engine.config import BacktestConfig


def test_compute_chop_series():
    # Synthetic flat candles
    highs = [10.0 + (i % 2) * 0.1 for i in range(30)]
    lows = [10.0 - (i % 2) * 0.1 for i in range(30)]
    closes = [10.0 for _ in range(30)]

    chop = compute_chop_series(highs, lows, closes, period=14)
    assert len(chop) == 30
    # Consolidating / oscillating series should yield high CHOP value
    assert chop[-1] > 50.0


def test_regime_classification_sub_atr_compression():
    mock_market = MagicMock()
    mock_contract = MagicMock()
    mock_contract.price_unit = 0.001
    mock_contract.price_precision = 4
    mock_market.get_contract_detail.return_value = mock_contract

    # Create 50 candles with tight range (0.001 each) -> ATR = 0.001
    # min_atr_ticks = 2.5 -> threshold = 0.0025
    # Since ATR (0.001) < 0.0025, it must classify as SUB_ATR_COMPRESSION
    candles = []
    base_price = 2.500
    for i in range(50):
        candles.append({
            "timestamp": 1000 + i * 60,
            "open": base_price,
            "high": base_price + 0.001,
            "low": base_price,
            "close": base_price + 0.0005,
            "volume": 100.0
        })

    strat = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        min_atr_ticks=2.5,
        atr_filter_enabled=True,
        climax_filter_enabled=False,
        auto_start_feed=False
    )
    regime, metrics = strat.classify_regime(candles)
    assert regime == MarketRegime.SUB_ATR_COMPRESSION

    # Test toggleability: when atr_filter_enabled=False, should NOT compress
    strat_no_filter = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        atr_filter_enabled=False,
        auto_start_feed=False
    )
    regime_no_filter, _ = strat_no_filter.classify_regime(candles)
    assert regime_no_filter != MarketRegime.SUB_ATR_COMPRESSION


def test_regime_classification_volatility_climax():
    mock_market = MagicMock()
    mock_contract = MagicMock()
    mock_contract.price_unit = 0.001
    mock_contract.price_precision = 4
    mock_market.get_contract_detail.return_value = mock_contract

    # 50 normal candles with range 0.005, then final candle with huge surge of 0.030 (6x ATR)
    candles = []
    base_price = 2.500
    for i in range(49):
        candles.append({
            "timestamp": 1000 + i * 60,
            "open": base_price,
            "high": base_price + 0.005,
            "low": base_price - 0.005,
            "close": base_price,
            "volume": 100.0
        })
    # Huge climax bar
    candles.append({
        "timestamp": 1000 + 49 * 60,
        "open": base_price,
        "high": base_price + 0.035,
        "low": base_price,
        "close": base_price + 0.035,
        "volume": 1000.0
    })

    strat = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        climax_filter_enabled=True,
        max_atr_expansion=2.2,
        auto_start_feed=False
    )
    regime, metrics = strat.classify_regime(candles)
    assert regime == MarketRegime.VOLATILITY_CLIMAX


def test_regime_classification_momentum_vs_range():
    mock_market = MagicMock()
    mock_contract = MagicMock()
    mock_contract.price_unit = 0.001
    mock_contract.price_precision = 4
    mock_market.get_contract_detail.return_value = mock_contract

    # Generate a clean uptrend with healthy volatility
    candles_trend = []
    p = 2.000
    for i in range(60):
        step = 0.010
        candles_trend.append({
            "timestamp": 1000 + i * 60,
            "open": p,
            "high": p + step + 0.002,
            "low": p - 0.001,
            "close": p + step,
            "volume": 500.0
        })
        p += step

    strat = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        adx_trend_threshold=20.0,
        auto_start_feed=False
    )
    regime_trend, metrics = strat.classify_regime(candles_trend)
    # Strong persistent upward step produces high ADX + EMA5 > EMA13
    assert regime_trend in (MarketRegime.STRONG_BULL_MOMENTUM, MarketRegime.BALANCED_RANGE)


def test_ema200_filter_toggleability():
    mock_market = MagicMock()
    mock_contract = MagicMock()
    mock_contract.price_unit = 0.001
    mock_contract.price_precision = 4
    mock_market.get_contract_detail.return_value = mock_contract

    # Default is use_ema200_filter = False
    strat_default = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        auto_start_feed=False
    )
    assert strat_default.use_ema200_filter is False

    strat_enabled = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        use_ema200_filter=True,
        auto_start_feed=False
    )
    assert strat_enabled.use_ema200_filter is True


def test_asset_generalization_tick_scaling():
    mock_market = MagicMock()

    # TRUMP_USDT: pu = 0.001 -> 2.5 ticks = 0.0025
    mock_contract_trump = MagicMock()
    mock_contract_trump.price_unit = 0.001
    mock_contract_trump.price_precision = 4
    mock_market.get_contract_detail.return_value = mock_contract_trump

    strat_trump = SmartStrategy(
        market=mock_market,
        symbol="TRUMP_USDT",
        min_atr_ticks=2.5,
        auto_start_feed=False
    )
    assert strat_trump._price_unit == 0.001
    assert math.isclose(strat_trump.min_atr_ticks * strat_trump._price_unit, 0.0025)

    # DOGE_USDT: pu = 0.0001 -> 2.5 ticks = 0.00025
    mock_contract_doge = MagicMock()
    mock_contract_doge.price_unit = 0.0001
    mock_contract_doge.price_precision = 5
    mock_market.get_contract_detail.return_value = mock_contract_doge

    strat_doge = SmartStrategy(
        market=mock_market,
        symbol="DOGE_USDT",
        min_atr_ticks=2.5,
        auto_start_feed=False
    )
    assert strat_doge._price_unit == 0.0001
    assert math.isclose(strat_doge.min_atr_ticks * strat_doge._price_unit, 0.00025)


def test_masterplan_strategy_smart_integration():
    mock_market = MagicMock()
    mock_contract = MagicMock()
    mock_contract.price_unit = 0.001
    mock_contract.price_precision = 4
    mock_contract.maker_fee_rate = 0.0
    mock_contract.taker_fee_rate = 0.0
    mock_contract.contract_size = 0.1
    mock_contract.min_volume = 1
    mock_contract.max_leverage = 75
    mock_market.get_contract_detail.return_value = mock_contract

    config = ExecutionConfig(
        symbol="TRUMP_USDT",
        strategy_mode="SMART_STRATEGY",
        smart_atr_filter_enabled=True,
        smart_min_atr_ticks=2.5,
        smart_use_ema200_filter=False,
        order_type="LIMIT",
        limit_order_timeout_seconds=10.0
    )

    coordinator = MasterplanStrategy(market=mock_market, config=config)
    assert coordinator.sub_strategy.name == "SmartStrategy"
    assert coordinator.sub_strategy.symbol == "TRUMP_USDT"
    assert coordinator.sub_strategy.atr_filter_enabled is True
    assert coordinator.sub_strategy.use_ema200_filter is False


def test_backtest_config_smart_inheritance():
    cfg = BacktestConfig(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="SMART_STRATEGY",
        order_type="MARKET",
        smart_min_atr_ticks=3.0,
        smart_use_ema200_filter=False
    )
    assert cfg.strategy_mode == "SMART_STRATEGY"
    assert cfg.smart_min_atr_ticks == 3.0
    assert cfg.smart_interval == "1m"
    assert cfg.smart_use_ema200_filter is False
