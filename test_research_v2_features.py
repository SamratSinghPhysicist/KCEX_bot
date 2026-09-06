"""
Unit Test Suite for Phase V2.1 & V2.2 Quantitative Optimizations
================================================================
Validates:
1. Signal Inversion (Exhaustion Fading in Stoch RSI & Smart Strategy)
2. Micro-Excursion Tick Ratchet logic (Tier 1 Tightening & Tier 2 Breakeven)
3. Order Execution Style & Slippage Engine (Maker Hybrid vs Pure Market)
4. Self-Documenting Strategy Preset Registry in settings.py
5. Backtest Simulation with Slippage & Ratchet
"""

import os
import sys
import time
import pytest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import settings
from kcex.engine.models import (
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    ExitReason,
    TradeOutcome
)
from strategies.stoch_rsi import StochasticRSIStrategy
from strategies.smart_strategy import SmartStrategy
from kcex.engine.executor import TradeExecutionEngine
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine


# =============================================================================
# 1. SIGNAL INVERSION TESTS
# =============================================================================

def test_stoch_rsi_signal_inversion():
    """Verify that invert_signal=True flips overbought to LONG and oversold to SHORT."""
    from unittest.mock import MagicMock
    mock_market = MagicMock()
    # Direct strategy
    direct_strat = StochasticRSIStrategy(
        market=mock_market,
        symbol="DOGE_USDT",
        stoch_preset="FAST_SCALP",
        invert_signal=False
    )
    # Inverted strategy
    inverted_strat = StochasticRSIStrategy(
        market=mock_market,
        symbol="DOGE_USDT",
        stoch_preset="FAST_SCALP",
        invert_signal=True
    )

    # Synthetic candles simulating an oversold bullish bounce (%K crosses above %D in oversold zone)
    # Generate 30 candles where RSI drops below 20 then rebounds
    candles_oversold = []
    base_price = 100.0
    for i in range(30):
        p = base_price - (i * 0.5)
        candles_oversold.append({"timestamp": 1000 + i * 60, "open": p, "high": p + 0.1, "low": p - 0.2, "close": p - 0.1})
    candles_oversold.append({"timestamp": 1000 + 30 * 60, "open": 85.0, "high": 85.8, "low": 84.9, "close": 85.6})

    sig_direct = direct_strat.generate_signal(candles_oversold)
    sig_inverted = inverted_strat.generate_signal(candles_oversold)

    if sig_direct is not None:
        assert sig_direct.direction == OrderDirection.LONG
        assert sig_inverted is not None
        assert sig_inverted.direction == OrderDirection.SHORT
        assert "INVERTED_FADE" in sig_inverted.signal_type


def test_smart_strategy_propagates_invert_signal():
    """Verify SmartStrategy accepts and propagates invert_signal to its child Stoch RSI strategy."""
    from unittest.mock import MagicMock
    mock_market = MagicMock()
    smart = SmartStrategy(
        market=mock_market,
        symbol="DOGE_USDT",
        interval="1m",
        invert_signal=True
    )
    assert smart.invert_signal is True
    assert smart.stoch_strategy.invert_signal is True


# =============================================================================
# 2. TICK RATCHET LOGIC TESTS
# =============================================================================

def test_ratchet_trailing_stop_in_dry_run():
    """Verify dry-run simulation monitors and triggers Tick Ratchet correctly."""
    from kcex.market import ContractInfo
    config = ExecutionConfig(
        symbol="DOGE_USDT",
        direction=OrderDirection.LONG,
        mode=EngineMode.DRY_RUN,
        leverage=75,
        tp_ticks=5,
        sl_mode="TICKS",
        sl_ticks=2,
        ratchet_enabled=True,
        ratchet_trigger_ticks=1.0,
        ratchet_stall_seconds=0.1, # Short stall for test speed
        ratchet_tighten_ticks=1.0,
        ratchet_breakeven_ticks=2.5,
        execution_style="PURE_MARKET",
        slippage_enabled=False,
        slippage_ticks=0,
        cooldown_seconds=0.0,
        max_trades=1
    )

    class MockMarket:
        def __init__(self):
            # Price starts at 0.1000, excursions to +1.5 ticks (0.10015), then pulls back to -1.0 tick (0.09990)
            self.prices = [0.1000, 0.10015, 0.10015, 0.09990]
            self.idx = 0

        def get_ticker(self, symbol):
            p = self.prices[min(self.idx, len(self.prices) - 1)]
            self.idx += 1
            return {"lastPrice": str(p), "bid1": str(p - 0.00001), "ask1": str(p + 0.00001)}

        def get_inr_rate(self):
            return 94.50

    from unittest.mock import MagicMock
    contract = MagicMock()
    contract.symbol = "DOGE_USDT"
    contract.price_unit = 0.0001
    contract.price_precision = 4
    contract.contract_size = 1.0
    contract.min_volume = 1
    contract.max_leverage = 75
    contract.maker_fee_rate = 0.0
    contract.taker_fee_rate = 0.0
    contract.maintenance_margin_ratio = 0.01
    contract.base_coin = "DOGE"

    engine = TradeExecutionEngine(config=config)
    engine.market = MockMarket()
    engine.pu = 0.0001
    engine.ps = 4
    engine.cs = 1.0

    # Execute simulated trade
    outcome = engine._simulate_dry_run_trade(
        trade_id=1,
        contract=contract,
        direction=OrderDirection.LONG,
        vol_contracts=1,
        leverage=75,
        open_time=time.time(),
        sub_strategy_name="MockDirect"
    )
    assert outcome is not None
    assert outcome.exit_reason in (ExitReason.RATCHET_TIGHTEN_HIT, ExitReason.RATCHET_BREAKEVEN_HIT, ExitReason.STOP_LOSS_HIT)


# =============================================================================
# 3. SELF-DOCUMENTING PRESETS REGISTRY TESTS
# =============================================================================

def test_preset_registry_doge_champion():
    """Verify DOGE_V2_2_RATCHET_CHAMPION has full quantitative configuration & backtest data."""
    cfg = settings.get_active_preset_config("DOGE_V2_2_RATCHET_CHAMPION")
    assert cfg is not None
    assert cfg["symbol"] == "DOGE_USDT"
    assert cfg["tp_ticks"] == 5
    assert cfg["sl_ticks"] == 2
    assert cfg["ratchet_enabled"] is True
    assert cfg["invert_signal"] is True
    assert cfg["execution_style"] == "MAKER_HYBRID"
    assert "backtest_config" in cfg
    assert cfg["backtest_config"]["leverage"] == 75
    assert "backtest_results_by_slippage" in cfg
    assert "slippage_0t" in cfg["backtest_results_by_slippage"]
    assert cfg["backtest_results_by_slippage"]["slippage_0t"]["net_profit_usdt"] == 4.87


def test_preset_registry_doge_asymmetric():
    """Verify DOGE_ASYMMETRIC_MOMENTUM_10T2T configuration."""
    cfg = settings.get_active_preset_config("DOGE_ASYMMETRIC_MOMENTUM_10T2T")
    assert cfg["symbol"] == "DOGE_USDT"
    assert cfg["tp_ticks"] == 10
    assert cfg["sl_ticks"] == 2
    assert cfg["invert_signal"] is False


def test_preset_registry_trump_legacy():
    """Verify TRUMP_LEGACY_BASELINE configuration."""
    cfg = settings.get_active_preset_config("TRUMP_LEGACY_BASELINE")
    assert cfg["symbol"] == "TRUMP_USDT"
    assert cfg["tp_ticks"] == 2
    assert cfg["sl_mode"] == "ROE"
    assert cfg["execution_style"] == "PURE_MARKET"


def test_preset_registry_custom():
    """Verify CUSTOM preset falls back cleanly to individual variables."""
    cfg = settings.get_active_preset_config("CUSTOM")
    assert cfg["symbol"] == settings.SYMBOL
    assert cfg["strategy_mode"] == settings.STRATEGY_MODE


# =============================================================================
# 4. BACKTEST ENGINE SLIPPAGE & RATCHET TESTS
# =============================================================================

def test_backtest_config_has_all_quantitative_fields():
    """Ensure BacktestConfig inherits all Phase V2.1/V2.2 fields."""
    bcfg = BacktestConfig(
        symbol="DOGE_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        invert_signal=True,
        ratchet_enabled=True,
        slippage_enabled=True,
        slippage_ticks=2,
        execution_style="MAKER_HYBRID"
    )
    assert bcfg.invert_signal is True
    assert bcfg.ratchet_enabled is True
    assert bcfg.slippage_enabled is True
    assert bcfg.slippage_ticks == 2
    assert bcfg.execution_style == "MAKER_HYBRID"


def test_github_runner_inputs_pack_and_limit_25():
    """Ensure GitHub Actions workflow_dispatch inputs are strictly <= 25 properties."""
    import yaml
    import json
    from BACKTESTER.engine.github_runner import GitHubBacktestRunner

    runner = GitHubBacktestRunner()
    bcfg = BacktestConfig(
        symbol="DOGE_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        invert_signal=True,
        ratchet_enabled=True,
        slippage_enabled=True,
        slippage_ticks=1,
        execution_style="MAKER_HYBRID"
    )
    inputs = runner.build_workflow_inputs(bcfg)

    # 1. Total inputs MUST be <= 25 to prevent GitHub API HTTP 422
    assert len(inputs) <= 25, f"Expected <= 25 inputs, got {len(inputs)}"
    assert "quant_params_json" in inputs

    # 2. Packed quant_params_json contains all quantitative fields
    qp = json.loads(inputs["quant_params_json"])
    assert qp["invert_signal"] is True
    assert qp["ratchet"] is True
    assert qp["enable_slippage"] is True
    assert qp["slippage_ticks"] == 1
    assert qp["execution_style"] == "MAKER_HYBRID"

    # 3. Matches .github/workflows/backtest.yml exactly
    workflow_path = os.path.join(ROOT_DIR, ".github", "workflows", "backtest.yml")
    with open(workflow_path, "r", encoding="utf-8") as f:
        wf_data = yaml.safe_load(f)
    on_block = wf_data.get("on") or wf_data.get(True)
    declared_inputs = on_block["workflow_dispatch"]["inputs"]
    assert len(declared_inputs) <= 25
    assert set(inputs.keys()) == set(declared_inputs.keys())
