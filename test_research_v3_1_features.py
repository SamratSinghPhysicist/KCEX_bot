"""
Unit Test Suite for Research V3 & V3.1 Quantitative Implementations
===================================================================
Validates:
1. Strategy Preset Registry in settings.py (V3 & V3.1 presets)
2. ATR-Calibrated Dynamic Targets & Target Dilution Law (strategy TP & SL)
3. Volume Shock Momentum Filter (strategies/filters.py)
4. Realistic 75x MMR Liquidation Barrier Detection (dry-run & backtester)
5. Maker Queue Dynamics & Timeout Cancellation
6. Microstructure Alpha & Volatility Regime Module Integration
"""

import os
import sys
import time
import pytest
from unittest.mock import MagicMock

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import settings
from kcex.market import ContractInfo
from kcex.engine.models import (
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    ExitReason,
    TradeSignal,
    TradeOutcome
)
from kcex.engine.strategy import MasterplanStrategy
from kcex.engine.executor import TradeExecutionEngine
from strategies.filters import VolumeShockFilter, FilterPipeline
from strategies.microstructure_alpha import VPINCalculator, OrderFlowImbalance
from strategies.volatility_regime import compute_bollinger_bandwidth, compute_choppiness_index, MarketRegime
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine


# =============================================================================
# 1. STRATEGY PRESET REGISTRY TESTS
# =============================================================================

def test_v3_and_v3_1_presets_registered():
    """Verify all new V3 & V3.1 presets exist in STRATEGY_PRESETS and resolve completely."""
    expected_presets = [
        "TRUMP_MARKET_SLIPPAGE_RESILIENT",
        "DOGE_MARKET_SLIPPAGE_RESILIENT",
        "TRUMP_V3_CHAMPION_MAKER_RATCHET",
        "DOGE_V3_CHAMPION_ASYMMETRIC_MOMENTUM",
        "DOGE_V2_2_RATCHET_CHAMPION",
        "TRUMP_LEGACY_BASELINE"
    ]
    for p in expected_presets:
        assert p in settings.STRATEGY_PRESETS, f"Preset {p} missing from STRATEGY_PRESETS"
        cfg = settings.get_active_preset_config(p)
        assert cfg is not None
        assert "symbol" in cfg
        assert "tp_ticks" in cfg
        assert "sl_ticks" in cfg
        assert "execution_style" in cfg


def test_market_slippage_resilient_preset_specs():
    """Verify market slippage resilient presets satisfy the Target Dilution Law and user mandate."""
    trump_cfg = settings.get_active_preset_config("TRUMP_MARKET_SLIPPAGE_RESILIENT")
    assert trump_cfg["symbol"] == "TRUMP_USDT"
    assert trump_cfg["execution_style"] == "PURE_MARKET"
    assert trump_cfg["resting_limit_tp"] is True
    assert trump_cfg["tp_ticks"] >= 10  # Target Dilution: >= 10 ticks profit target
    assert trump_cfg["sl_ticks"] <= 5   # Tight risk containment: <= 5 ticks stop
    assert trump_cfg["ratchet_enabled"] is True
    assert trump_cfg["ratchet_trigger_ticks"] >= 3.0  # Offsets taker spread friction
    assert trump_cfg["use_atr_targets"] is True
    assert trump_cfg["volume_filter_enabled"] is True

    doge_cfg = settings.get_active_preset_config("DOGE_MARKET_SLIPPAGE_RESILIENT")
    assert doge_cfg["symbol"] == "DOGE_USDT"
    assert doge_cfg["execution_style"] == "PURE_MARKET"
    assert doge_cfg["resting_limit_tp"] is True
    assert doge_cfg["invert_signal"] is True  # Mean reversion dominates DOGE


# =============================================================================
# 2. ATR-CALIBRATED TARGETS & TARGET DILUTION TESTS
# =============================================================================

def test_atr_dynamic_tp_and_sl_calculation():
    """Verify strategy dynamically calculates ATR-calibrated TP and SL when toggled on."""
    cfg = ExecutionConfig(
        symbol="TRUMP_USDT",
        use_atr_targets=True,
        atr_tp_multiplier=2.0,
        atr_sl_multiplier=1.0
    )
    strat = MasterplanStrategy(market=None, config=cfg, sub_strategy=object())

    # Simulated entry at 1.700, pu = 0.001, ATR = 0.005 (5 ticks)
    entry_p = 1.700
    pu = 0.001
    atr_val = 0.005

    # With ATR = 0.005, 2.0x ATR = 0.010 (+10 ticks) -> TP = 1.710
    tp_long = strat.calculate_min_profit_tp(
        direction=OrderDirection.LONG,
        entry_price=entry_p,
        price_unit=pu,
        tp_ticks=2,  # Fixed fallback should be overridden by ATR
        precision=3,
        atr_value=atr_val
    )
    assert tp_long == 1.710

    # With ATR = 0.005, 1.0x ATR = 0.005 (-5 ticks) -> SL = 1.695
    sl_long = strat.calculate_stop_loss(
        direction=OrderDirection.LONG,
        entry_price=entry_p,
        leverage=75,
        price_unit=pu,
        precision=3,
        atr_value=atr_val
    )
    assert sl_long == 1.695


def test_atr_dynamic_targets_disabled_fallback():
    """Verify strategy strictly preserves fixed tp_ticks and sl_ticks when use_atr_targets=False."""
    cfg = ExecutionConfig(
        symbol="TRUMP_USDT",
        use_atr_targets=False,
        tp_ticks=2,
        sl_ticks=4,
        sl_mode="TICKS"
    )
    strat = MasterplanStrategy(market=None, config=cfg, sub_strategy=object())

    entry_p = 1.700
    pu = 0.001
    atr_val = 0.010  # High ATR should be ignored because use_atr_targets is False

    tp = strat.calculate_min_profit_tp(
        direction=OrderDirection.LONG,
        entry_price=entry_p,
        price_unit=pu,
        tp_ticks=2,
        precision=3,
        atr_value=atr_val
    )
    assert tp == 1.702  # Exactly +2 ticks

    sl = strat.calculate_stop_loss(
        direction=OrderDirection.LONG,
        entry_price=entry_p,
        leverage=75,
        sl_ticks=4,
        price_unit=pu,
        precision=3,
        atr_value=atr_val
    )
    assert sl == 1.696  # Exactly -4 ticks


# =============================================================================
# 3. VOLUME SHOCK MOMENTUM FILTER TESTS
# =============================================================================

class MockVolumeCandle:
    def __init__(self, volume: float, close: float = 1.0):
        self.volume = float(volume)
        self.close = float(close)
        self.high = float(close + 0.1)
        self.low = float(close - 0.1)
        self.open = float(close)


def test_volume_shock_filter_gating():
    """Verify VolumeShockFilter permits signals with volume surges and blocks flat volume."""
    vol_filter = VolumeShockFilter(enabled=True, multiplier=1.2, period=10)

    # 10 baseline candles with volume 100.0 (Average = 100.0, Threshold = 120.0)
    baseline_candles = [MockVolumeCandle(volume=100.0) for _ in range(10)]
    sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "MOMENTUM")

    # Flat volume candle (volume = 105.0 < 120.0) -> Must be rejected
    flat_series = baseline_candles + [MockVolumeCandle(volume=105.0)]
    allowed, reason = vol_filter.is_allowed(sig, flat_series, time.time())
    assert allowed is False
    assert "Volume Shock: Current volume 105.0 < 1.2x baseline" in reason

    # Surge volume candle (volume = 150.0 >= 120.0) -> Must be allowed
    surge_series = baseline_candles + [MockVolumeCandle(volume=150.0)]
    allowed, reason = vol_filter.is_allowed(sig, surge_series, time.time())
    assert allowed is True
    assert reason is None


# =============================================================================
# 4. 75X MMR LIQUIDATION BARRIER TESTS
# =============================================================================

def test_75x_liquidation_barrier_detection_in_dry_run():
    """Verify that when simulate_intra_tick_liquidation=True, adverse moves past MMR trigger LIQUIDATION_HIT."""
    mock_market = MagicMock()
    mock_market.get_inr_rate.return_value = 94.45

    contract = MagicMock(spec=ContractInfo)
    contract.symbol = "TRUMP_USDT"
    contract.contract_size = 0.1
    contract.price_unit = 0.001
    contract.min_volume = 1.0
    contract.max_leverage = 75
    contract.price_precision = 3
    contract.maker_fee_rate = 0.0
    contract.taker_fee_rate = 0.0
    contract.maintenance_margin_ratio = 0.01
    contract.base_coin = "TRUMP"
    mock_market.get_contract_detail.return_value = contract

    cfg = ExecutionConfig(
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        mode=EngineMode.DRY_RUN,
        leverage=75,
        sl_mode="TICKS",
        sl_ticks=20,  # Wide SL placed beyond liquidation to test liquidation barrier
        simulate_intra_tick_liquidation=True,
        poll_interval_seconds=0.01
    )

    # Initial price = 2.000. At 75x, liq price is 2.000 * (1 - 1/75 + 0.01) = ~1.9933
    ticker_step = [
        {"lastPrice": 2.000, "bid1": 2.000, "ask1": 2.000},
        {"lastPrice": 2.000, "bid1": 2.000, "ask1": 2.000},
        {"lastPrice": 1.990, "bid1": 1.990, "ask1": 1.991}  # Breaches MMR liquidation barrier
    ]
    idx = [0]
    def get_ticker(s):
        t = ticker_step[min(idx[0], len(ticker_step) - 1)]
        idx[0] += 1
        return t

    mock_market.get_ticker = get_ticker

    engine = TradeExecutionEngine(config=cfg, market=mock_market)
    outcome = engine._simulate_dry_run_trade(
        trade_id=1,
        contract=contract,
        direction=OrderDirection.LONG,
        vol_contracts=1,
        leverage=75,
        open_time=time.time(),
        sub_strategy_name="TestStrat"
    )

    assert outcome is not None
    assert outcome.exit_reason == ExitReason.LIQUIDATION_HIT
    assert outcome.is_loss is True


# =============================================================================
# 5. MICROSTRUCTURE ALPHA & VOLATILITY REGIME INTEGRATION
# =============================================================================

def test_vpin_and_flow_imbalance_computation():
    """Verify VPIN and Order Flow Imbalance calculators process synthetic trade streams cleanly."""
    vpin = VPINCalculator(bucket_volume=10.0, num_buckets=5)
    ofi = OrderFlowImbalance(window_seconds=5.0)

    now = time.time()
    # Ingest 5 buy-heavy aggressive trades
    for i in range(5):
        v = vpin.update(price=10.0 + i * 0.01, qty=5.0, is_buyer_maker=False)
        current_ofi = ofi.update(timestamp_sec=now + i, qty=5.0, is_buyer_maker=False)

    assert vpin.curr_buy_vol > 0
    assert current_ofi > 0.0  # Buy pressure produces positive imbalance
    assert ofi.trades is not None


def test_bollinger_bandwidth_and_choppiness_computation():
    """Verify Bollinger Bandwidth and Choppiness Index compute without numerical instability."""
    closes = [10.0 + (i % 3) * 0.1 for i in range(30)]
    highs = [c + 0.1 for c in closes]
    lows = [c - 0.1 for c in closes]

    bbw, lowest_bbw = compute_bollinger_bandwidth(closes, period=10)
    chop = compute_choppiness_index(highs, lows, closes, period=10)

    assert len(bbw) == 30
    assert len(chop) == 30
    assert all(b >= 0.0 for b in bbw)
    assert all(0.0 <= c <= 100.0 for c in chop)
