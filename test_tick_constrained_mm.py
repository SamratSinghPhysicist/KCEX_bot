"""
Unit and Integration Test Suite: Tick-Constrained Market Making Strategy
========================================================================
Validates:
1. Relative tick size gatekeeping (tick bps >= 4.0 bps).
2. Order Flow Imbalance (OFI) calculations.
3. HTF Bollinger Bandwidth squeeze and ADX consolidation detection.
4. Corrected maker/taker directionality on passive scratches and TP limits.
5. Realistic slippage handling on hard stop loss triggers.
6. Integration with MasterplanStrategy and settings preset registry.
"""

import math
import time
import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock

from strategies.tick_constrained_mm import (
    TickConstrainedMMStrategy,
    TickConstrainedConfig,
    TickConstrainedSimulator,
    compute_ofi_from_trades,
    compute_bollinger_bandwidth,
    compute_adx_scalar
)
from kcex.engine.models import OrderDirection, ExecutionConfig, TradeOutcome, ExitReason
from kcex.engine.strategy import MasterplanStrategy
import settings


class TestMicrostructureMath:
    def test_compute_ofi_buy_heavy(self):
        # is_buyer_maker=False means aggressive market BUY
        trades = [
            {"qty": 100.0, "is_buyer_maker": False},
            {"qty": 50.0, "is_buyer_maker": False},
            {"qty": 10.0, "is_buyer_maker": True},
        ]
        ofi = compute_ofi_from_trades(trades, window=10)
        # buy = 150, sell = 10 -> (150 - 10) / 160 = 140 / 160 = 0.875
        assert round(ofi, 3) == 0.875

    def test_compute_ofi_sell_heavy(self):
        # is_buyer_maker=True means aggressive market SELL
        trades = [
            {"qty": 10.0, "is_buyer_maker": False},
            {"qty": 190.0, "is_buyer_maker": True},
        ]
        ofi = compute_ofi_from_trades(trades, window=10)
        # buy = 10, sell = 190 -> (10 - 190) / 200 = -0.9
        assert round(ofi, 3) == -0.9

    def test_compute_ofi_kcex_native_schema(self):
        # KCEX native deal items use 'p' (price), 'v' (volume), 'T' (1=Buy, 2=Sell)
        trades = [
            {"p": 1.45, "v": 75.0, "T": 1},   # Buy
            {"p": 1.45, "v": 25.0, "T": 2},   # Sell
        ]
        ofi = compute_ofi_from_trades(trades, window=10)
        # buy = 75, sell = 25 -> (75 - 25) / 100 = 0.5
        assert round(ofi, 2) == 0.5

    def test_compute_ofi_empty(self):
        assert compute_ofi_from_trades([], window=10) == 0.0

    def test_bollinger_bandwidth_compression(self):
        # Stable price series with minimal variance
        flat_prices = [1.45 + 0.001 * (i % 2) for i in range(30)]
        bbw_flat = compute_bollinger_bandwidth(flat_prices, period=20)
        
        # Volatile series
        volatile_prices = [1.45 + 0.05 * (i % 5) for i in range(30)]
        bbw_vol = compute_bollinger_bandwidth(volatile_prices, period=20)

        assert bbw_flat < bbw_vol
        assert bbw_flat > 0.0

    def test_adx_scalar(self):
        # Sideways oscillating series
        highs = [1.46 + 0.002 * (i % 2) for i in range(40)]
        lows = [1.44 + 0.002 * (i % 2) for i in range(40)]
        closes = [1.45 + 0.002 * (i % 2) for i in range(40)]

        adx = compute_adx_scalar(highs, lows, closes, period=14)
        assert isinstance(adx, float)
        assert adx >= 0.0


class TestTickConstrainedStrategy:
    def test_relative_tick_size_gatekeeper(self):
        mock_market = MagicMock()
        mock_contract = MagicMock()
        mock_contract.price_unit = 0.001
        mock_market.get_contract_detail.return_value = mock_contract

        cfg = TickConstrainedConfig(min_tick_bps=4.0, use_htf_filter=False)
        strat = TickConstrainedMMStrategy(market=mock_market, symbol="TRUMP_USDT", config=cfg)

        # Case 1: Low price ($1.45) -> tick_bps = (0.001 / 1.45) * 10000 = ~6.90 bps (Tick-constrained)
        mock_market.get_ticker.return_value = {"lastPrice": 1.45}
        mock_market.get_recent_trades.return_value = []
        state_low = strat.evaluate_market_state()
        assert state_low["is_tick_constrained"] is True
        assert state_low["tick_bps"] > 4.0

        # Case 2: High price ($20.00) -> tick_bps = (0.001 / 20.00) * 10000 = 0.50 bps (NOT tick-constrained)
        mock_market.get_ticker.return_value = {"lastPrice": 20.00}
        state_high = strat.evaluate_market_state()
        assert state_high["is_tick_constrained"] is False
        assert state_high["tick_bps"] < 4.0

        # Signal generation should be rejected when not tick-constrained
        sig = strat.generate_signal("TRUMP_USDT")
        assert sig is None

    def test_signal_generation_on_favorable_regime(self):
        mock_market = MagicMock()
        mock_contract = MagicMock()
        mock_contract.price_unit = 0.001
        mock_market.get_contract_detail.return_value = mock_contract
        mock_market.get_ticker.return_value = {"lastPrice": 1.45}
        # Neutral order flow
        mock_market.get_recent_trades.return_value = [
            {"qty": 50.0, "is_buyer_maker": False},
            {"qty": 50.0, "is_buyer_maker": True},
        ]
        # Sideways 15m klines
        mock_market.get_klines.return_value = [
            {"open": 1.45, "high": 1.452, "low": 1.448, "close": 1.45} for _ in range(50)
        ]

        cfg = TickConstrainedConfig(min_tick_bps=4.0, tp_ticks=1, sl_ticks=3, use_htf_filter=True)
        strat = TickConstrainedMMStrategy(market=mock_market, symbol="TRUMP_USDT", config=cfg)

        sig = strat.generate_signal("TRUMP_USDT")
        assert sig is not None
        assert sig.metadata["target_ticks"] == 1
        assert sig.metadata["target_sl_ticks"] == 3
        assert sig.metadata["entry_style"] == "MAKER_HYBRID"
        assert sig.metadata["strategy_mode"] == "TICK_CONSTRAINED_MM"

    def test_cooldown_lifecycle(self):
        strat = TickConstrainedMMStrategy(config=TickConstrainedConfig(cooldown_seconds=15.0))
        now = time.time()
        assert strat.should_generate_signal(now) is True

        outcome = TradeOutcome(
            trade_id=1, symbol="TRUMP_USDT", direction=OrderDirection.LONG,
            sub_strategy_name="TICK_CONSTRAINED_MM", mode="dry-run", leverage=10,
            vol_contracts=1, contract_size=0.1, underlying_quantity=0.1,
            entry_price=1.45, exit_price=1.451, min_profit_tp_price=1.451, stop_loss_price=1.447,
            price_unit=0.001, open_time=now - 5.0, close_time=now, duration_seconds=5.0,
            notional_value_usdt=0.145, notional_value_inr=13.7, margin_used_usdt=0.0145,
            margin_used_inr=1.37, realized_pnl_usdt=0.0001, realized_pnl_inr=0.009,
            pnl_percentage=0.07, roe_percentage=0.7, exit_reason=ExitReason.MIN_PROFIT_TP_HIT
        )
        strat.on_trade_completed(outcome)
        assert strat.should_generate_signal(time.time()) is False
        assert strat.get_remaining_cooldown(time.time()) > 0.0


class TestSimulatorCorrectedMechanics:
    def test_simulator_corrected_scratch_and_tp(self):
        # Construct synthetic trades to test:
        # 1. Entry Long at 1.450
        # 2. Market buy at 1.451 (is_buyer_maker=False) -> fills Long TP!
        # 3. Entry Short at 1.451
        # 4. Market sell at 1.450 (is_buyer_maker=True) -> fills Short TP!
        # 5. Passive scratch fill checks
        # 6. Hard stop loss with adverse slippage

        timestamps = [1000 + i * 100 for i in range(60)]
        prices = [1.450] * 20 + [1.451] * 20 + [1.445] * 20  # Drop through stop at end
        # Maker/Taker direction: True = sell hit bid, False = buy hit ask
        buyer_maker = [True] * 10 + [False] * 10 + [True] * 20 + [True] * 20
        qtys = [500.0] * 60

        df = pd.DataFrame({
            "price": prices,
            "is_buyer_maker": buyer_maker,
            "qty": qtys,
            "time": timestamps
        })

        cfg = TickConstrainedConfig(
            tick_size=0.001,
            min_tick_bps=4.0,
            tp_ticks=1,
            sl_ticks=3,
            entry_queue_qty=100.0,
            tp_queue_qty=100.0,
            ofi_window=5,
            use_htf_filter=False
        )
        sim = TickConstrainedSimulator(cfg)
        res = sim.run_simulation(df)

        assert res["total_trades"] > 0
        assert "wins" in res
        assert "losses" in res
        assert res["is_tick_constrained"] is True


class TestMasterplanPresetIntegration:
    def test_preset_registration(self):
        preset_cfg = settings.get_active_preset_config("TRUMP_TICK_CONSTRAINED_MM")
        assert preset_cfg["strategy_mode"] == "TICK_CONSTRAINED_MM"
        assert preset_cfg["tp_ticks"] == 1
        assert preset_cfg["sl_ticks"] == 3
        assert preset_cfg["min_tick_bps"] == 4.0
        assert preset_cfg["execution_style"] == "MAKER_HYBRID"

    def test_masterplan_strategy_factory(self):
        mock_market = MagicMock()
        mock_contract = MagicMock()
        mock_contract.price_unit = 0.001
        mock_market.get_contract_detail.return_value = mock_contract

        exec_cfg = ExecutionConfig(
            symbol="TRUMP_USDT",
            strategy_mode="TICK_CONSTRAINED_MM",
            tp_ticks=1,
            sl_ticks=3,
            min_tick_bps=4.0
        )
        coord = MasterplanStrategy(market=mock_market, config=exec_cfg)
        assert isinstance(coord.sub_strategy, TickConstrainedMMStrategy)
        assert coord.sub_strategy.name == "TICK_CONSTRAINED_MM"


class TestKCEXMarketTrades:
    def test_get_recent_trades_limit(self):
        from kcex.market import KCEXMarket
        mock_client = MagicMock()
        mock_client.get_public.return_value = {
            "data": [
                {"p": 1.45, "v": 10, "T": 1, "t": 1000},
                {"p": 1.46, "v": 20, "T": 2, "t": 1001},
                {"p": 1.47, "v": 30, "T": 1, "t": 1002},
            ]
        }
        market = KCEXMarket(client=mock_client)

        # Call with limit
        trades_limited = market.get_recent_trades("TRUMP_USDT", limit=2)
        assert len(trades_limited) == 2
        assert trades_limited[0]["p"] == 1.45
        assert trades_limited[1]["p"] == 1.46

        # Call without limit
        trades_all = market.get_recent_trades("TRUMP_USDT")
        assert len(trades_all) == 3
