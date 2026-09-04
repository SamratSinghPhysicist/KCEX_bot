"""
KCEX Automated Trade Execution Engine - Test Suite
==================================================
Verifies the Masterplan Strategy, sub-strategy cycling, tick-size (pu) min-profit TP,
-10% ROE stop-loss calculation, immediate profit close checks, zero-fee validation,
dual-currency logging, and end-to-end dry-run execution.
"""

import os
import sys
import time
import json
import logging
import tempfile
import shutil
import unittest
from unittest.mock import MagicMock

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kcex.market import ContractInfo
from kcex import (
    KCEXClient,
    KCEXMarket,
    KCEXRiskCalculator,
    KCEXTrader,
    TradeExecutionEngine,
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    ExitReason,
    TradeOutcome,
    MasterplanStrategy,
    DirectionalCycleSubStrategy,
    MicrostructureSubStrategy,
    MicrostructureSignalGenerator,
    SignalConfig,
    SymbolMeta,
    DualCurrencyLogger,
    TradeOutcomeLogger
)



class TestMasterplanStrategy(unittest.TestCase):
    """Tests core Masterplan pricing math, SL, and immediate profit triggers."""

    def setUp(self):
        self.market = KCEXMarket()
        self.strategy = MasterplanStrategy(self.market)

    def test_min_profit_tp_long(self):
        """For Long: Min-Profit TP = Entry Price + pu"""
        entry_price = 2.3450
        pu = 0.001
        expected_tp = 2.3460
        calc_tp = self.strategy.calculate_min_profit_tp(
            direction=OrderDirection.LONG,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=1,
            precision=4
        )
        self.assertAlmostEqual(calc_tp, expected_tp, places=4)

    def test_min_profit_tp_short(self):
        """For Short: Min-Profit TP = Entry Price - pu"""
        entry_price = 2.3450
        pu = 0.001
        expected_tp = 2.3440
        calc_tp = self.strategy.calculate_min_profit_tp(
            direction=OrderDirection.SHORT,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=1,
            precision=4
        )
        self.assertAlmostEqual(calc_tp, expected_tp, places=4)

    def test_stop_loss_roe_long(self):
        """For Long at 75x, -10% ROE SL: Price drop = 10% / 75 = 0.1333%"""
        entry_price = 2.3480
        leverage = 75
        sl_roe_pct = 10.0
        # price_drop = 2.3480 * (0.10 / 75) = 0.00313066
        # sl_price = 2.3480 - 0.00313 = 2.3449 (rounds to 2.345 observed in Codex capture!)
        calc_sl = self.strategy.calculate_stop_loss(
            direction=OrderDirection.LONG,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=sl_roe_pct,
            precision=3
        )
        self.assertEqual(calc_sl, 2.345)

    def test_stop_loss_roe_short(self):
        """For Short at 75x, -10% ROE SL: Price rise = 10% / 75 = 0.1333%"""
        entry_price = 2.3480
        leverage = 75
        sl_roe_pct = 10.0
        calc_sl = self.strategy.calculate_stop_loss(
            direction=OrderDirection.SHORT,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=sl_roe_pct,
            precision=3
        )
        self.assertEqual(calc_sl, 2.351)

    def test_immediate_profit_condition(self):
        """Check immediate profit close condition."""
        tp_long = 2.3460
        # For Long, current >= TP means profit is already at or better than min
        self.assertTrue(self.strategy.is_better_than_min_profit(OrderDirection.LONG, 2.3460, tp_long))
        self.assertTrue(self.strategy.is_better_than_min_profit(OrderDirection.LONG, 2.3470, tp_long))
        self.assertFalse(self.strategy.is_better_than_min_profit(OrderDirection.LONG, 2.3455, tp_long))

        tp_short = 2.3440
        # For Short, current <= TP means profit is already at or better than min
        self.assertTrue(self.strategy.is_better_than_min_profit(OrderDirection.SHORT, 2.3440, tp_short))
        self.assertTrue(self.strategy.is_better_than_min_profit(OrderDirection.SHORT, 2.3430, tp_short))
        self.assertFalse(self.strategy.is_better_than_min_profit(OrderDirection.SHORT, 2.3445, tp_short))

    def test_zero_fee_validation_trump(self):
        """Verify TRUMP_USDT zero-fee validation."""
        info = self.strategy.validate_zero_fee_pair("TRUMP_USDT")
        self.assertEqual(info["symbol"], "TRUMP_USDT")
        self.assertEqual(info["maker_fee"], 0.0)
        self.assertEqual(info["taker_fee"], 0.0)
        self.assertTrue(info["is_zero_fee"])


class TestSubStrategyCycle(unittest.TestCase):
    """Tests sub-strategy cycle transitions and cooldown enforcement."""

    def test_cycle_and_cooldown(self):
        sub = DirectionalCycleSubStrategy(
            direction=OrderDirection.LONG,
            cooldown_seconds=30.0,
            name="TestCycle"
        )
        # 1. Initial state: ready to signal
        now = time.time()
        self.assertTrue(sub.should_generate_signal(now))

        # 2. Signal generated -> trade in progress
        signal = sub.generate_signal("TRUMP_USDT")
        self.assertIsNotNone(signal)
        self.assertEqual(signal.direction, OrderDirection.LONG)
        self.assertTrue(sub.trade_in_progress)

        # 3. Cannot generate another signal while trade is in progress
        self.assertFalse(sub.should_generate_signal(now + 1))
        self.assertIsNone(sub.generate_signal("TRUMP_USDT"))

        # 4. Simulate trade completion
        dummy_outcome = TradeOutcome(
            trade_id=1,
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="TestCycle",
            mode=EngineMode.DRY_RUN,
            leverage=75,
            vol_contracts=1,
            contract_size=0.1,
            underlying_quantity=0.1,
            entry_price=2.345,
            exit_price=2.346,
            min_profit_tp_price=2.346,
            stop_loss_price=2.342,
            price_unit=0.001,
            open_time=now,
            close_time=now + 5,
            duration_seconds=5.0,
            notional_value_usdt=0.2345,
            notional_value_inr=22.15,
            margin_used_usdt=0.0031,
            margin_used_inr=0.295,
            realized_pnl_usdt=0.0001,
            realized_pnl_inr=0.0094,
            pnl_percentage=0.042,
            roe_percentage=3.19,
            exit_reason=ExitReason.MIN_PROFIT_TP_HIT
        )
        sub.on_trade_completed(dummy_outcome)
        self.assertFalse(sub.trade_in_progress)
        self.assertEqual(sub.completed_trades_count, 1)

        # 5. Cooldown: at now + 10s (5s elapsed since close), cooldown is still active
        self.assertFalse(sub.should_generate_signal(now + 10))
        self.assertGreater(sub.get_remaining_cooldown(now + 10), 0.0)

        # 6. Cooldown elapsed at now + 40s (35s elapsed since close >= 30s)
        self.assertTrue(sub.should_generate_signal(now + 40))
        self.assertEqual(sub.get_remaining_cooldown(now + 40), 0.0)


class TestDualCurrencyAndLogging(unittest.TestCase):
    """Tests dual-currency formatters and trade journal generation."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log_dir = self.temp_dir.name
        self.dual_logger = DualCurrencyLogger(
            log_file=os.path.join(self.test_log_dir, "test_realtime.log"),
            inr_rate=94.50
        )
        self.outcome_logger = TradeOutcomeLogger(
            txt_file=os.path.join(self.test_log_dir, "test_outcomes.txt"),
            jsonl_file=os.path.join(self.test_log_dir, "test_outcomes.jsonl")
        )

    def tearDown(self):
        for h in list(self.dual_logger.logger.handlers):
            h.close()
            self.dual_logger.logger.removeHandler(h)
        logging.shutdown()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_dual_formatting(self):
        formatted = self.dual_logger.format_dual(0.001, precision=4)
        self.assertIn("USDT", formatted)
        self.assertIn("INR", formatted)
        # 0.001 * 94.50 = 0.0945 -> INR 0.09
        self.assertIn("0.09", formatted)

    def test_logger_kwargs_and_exc_info(self):
        try:
            raise ValueError("Test simulation error")
        except ValueError as err:
            # Should not raise TypeError: unexpected keyword argument 'exc_info'
            self.dual_logger.error("Caught error: %s", err, exc_info=True)
            self.dual_logger.warning("Warning test: %s", err, extra={})
            self.dual_logger.info("Info test: %s", err)
            self.dual_logger.debug("Debug test: %s", err)
            self.dual_logger.exception("Exception test: %s", err)

    def test_trade_outcome_card_logging(self):
        now = time.time()
        outcome = TradeOutcome(
            trade_id=1,
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="DirectionalCycle(LONG)",
            mode=EngineMode.DRY_RUN,
            leverage=75,
            vol_contracts=1,
            contract_size=0.1,
            underlying_quantity=0.1,
            entry_price=2.3770,
            exit_price=2.3780,
            min_profit_tp_price=2.3780,
            stop_loss_price=2.3738,
            price_unit=0.001,
            open_time=now,
            close_time=now + 2.5,
            duration_seconds=2.5,
            notional_value_usdt=0.2377,
            notional_value_inr=22.46,
            margin_used_usdt=0.00317,
            margin_used_inr=0.30,
            realized_pnl_usdt=0.0001,
            realized_pnl_inr=0.00945,
            pnl_percentage=0.042,
            roe_percentage=3.15,
            inr_rate=94.50,
            exit_reason=ExitReason.MIN_PROFIT_TP_HIT
        )

        card = self.outcome_logger.log_outcome(outcome)
        self.assertIn("TRADE #1 OUTCOME JOURNAL", card)
        self.assertIn("TRUMP_USDT", card)
        self.assertIn("0.000100 USDT", card)
        self.assertIn("INR 0.0095", card)
        self.assertIn("CUMULATIVE STATS", card)

        # Check that files were written
        self.assertTrue(os.path.isfile(self.outcome_logger.txt_file))
        self.assertTrue(os.path.isfile(self.outcome_logger.jsonl_file))

        # Check JSONL record
        with open(self.outcome_logger.jsonl_file, "r", encoding="utf-8") as f:
            line = f.readline()
            data = json.loads(line)
            self.assertEqual(data["trade_id"], 1)
            self.assertEqual(data["symbol"], "TRUMP_USDT")
            self.assertEqual(data["direction"], "LONG")
            self.assertAlmostEqual(data["realized_pnl_usdt"], 0.0001)


class TestEngineExecutionDryRun(unittest.TestCase):
    """Tests complete dry-run engine cycle execution."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log_dir = self.temp_dir.name

    def tearDown(self):
        logging.shutdown()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_single_dry_run_cycle(self):
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            mode=EngineMode.DRY_RUN,
            cooldown_seconds=1.0,
            max_trades=1,
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        # Mock ticker sequence: entry at 2.350, then price reaches 2.352 (TP hit)
        ticker_sequence = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.352, "bid1": 2.352, "ask1": 2.353}
        ]
        seq_idx = [0]
        orig_get_ticker = engine.market.get_ticker
        def mock_ticker(sym):
            if seq_idx[0] < len(ticker_sequence):
                t = ticker_sequence[seq_idx[0]]
                seq_idx[0] += 1
                return t
            return ticker_sequence[-1]

        engine.market.get_ticker = mock_ticker
        outcome = engine.execute_single_trade_cycle(contract)

        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.trade_id, 1)
        self.assertEqual(outcome.symbol, "TRUMP_USDT")
        self.assertEqual(outcome.direction, OrderDirection.LONG)
        self.assertEqual(outcome.vol_contracts, 1)
        self.assertEqual(outcome.exit_reason, ExitReason.MIN_PROFIT_TP_HIT)
        self.assertAlmostEqual(outcome.exit_price - outcome.entry_price, 0.001, places=2)
        self.assertTrue(outcome.is_profit)
        self.assertGreater(outcome.realized_pnl_usdt, 0)
        self.assertGreater(outcome.realized_pnl_inr, 0)

    def test_single_dry_run_cycle_stop_loss(self):
        """Verify that dry run genuinely triggers STOP_LOSS_HIT when price drops."""
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            mode=EngineMode.DRY_RUN,
            cooldown_seconds=1.0,
            max_trades=1,
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        # Mock ticker sequence: entry at 2.350, then price drops to 2.345 (SL hit)
        ticker_sequence = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.344, "bid1": 2.344, "ask1": 2.345}
        ]
        seq_idx = [0]
        def mock_ticker(sym):
            if seq_idx[0] < len(ticker_sequence):
                t = ticker_sequence[seq_idx[0]]
                seq_idx[0] += 1
                return t
            return ticker_sequence[-1]

        engine.market.get_ticker = mock_ticker
        outcome = engine.execute_single_trade_cycle(contract)

        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.trade_id, 1)
        self.assertEqual(outcome.symbol, "TRUMP_USDT")
        self.assertEqual(outcome.direction, OrderDirection.LONG)
        self.assertEqual(outcome.exit_reason, ExitReason.STOP_LOSS_HIT)
        self.assertTrue(outcome.is_loss)
        self.assertLess(outcome.realized_pnl_usdt, 0)

    def test_single_dry_run_cycle_short_take_profit(self):
        """Verify that dry run correctly triggers MIN_PROFIT_TP_HIT for SHORT when price drops."""
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.SHORT,
            mode=EngineMode.DRY_RUN,
            cooldown_seconds=1.0,
            max_trades=1,
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        # For SHORT: Entry at bid1 = 2.350. TP is 2.349 (1 pu = 0.001).
        # Price must NOT exit immediately when cur_ask=2.350, but exit when price drops to 2.348 (<= TP 2.349).
        ticker_sequence = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.348, "bid1": 2.348, "ask1": 2.349}
        ]
        seq_idx = [0]
        def mock_ticker(sym):
            if seq_idx[0] < len(ticker_sequence):
                t = ticker_sequence[seq_idx[0]]
                seq_idx[0] += 1
                return t
            return ticker_sequence[-1]

        engine.market.get_ticker = mock_ticker
        outcome = engine.execute_single_trade_cycle(contract)

        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.trade_id, 1)
        self.assertEqual(outcome.direction, OrderDirection.SHORT)
        self.assertEqual(outcome.exit_reason, ExitReason.MIN_PROFIT_TP_HIT)
        self.assertFalse(outcome.is_loss)
        self.assertGreater(outcome.realized_pnl_usdt, 0)

    def test_single_dry_run_cycle_short_stop_loss(self):
        """Verify that dry run genuinely triggers STOP_LOSS_HIT for SHORT when price rises."""
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.SHORT,
            mode=EngineMode.DRY_RUN,
            cooldown_seconds=1.0,
            max_trades=1,
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        # For SHORT: Entry at bid1 = 2.350. SL is ~2.353 (3 pu away with 10% ROE on 75x).
        # Ticker stays below SL at 2.351 (should NOT trigger SL), then jumps past SL to 2.355.
        ticker_sequence = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.350, "bid1": 2.350, "ask1": 2.350},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.351, "bid1": 2.351, "ask1": 2.351},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.355, "bid1": 2.354, "ask1": 2.355}
        ]
        seq_idx = [0]
        def mock_ticker(sym):
            if seq_idx[0] < len(ticker_sequence):
                t = ticker_sequence[seq_idx[0]]
                seq_idx[0] += 1
                return t
            return ticker_sequence[-1]

        engine.market.get_ticker = mock_ticker
        outcome = engine.execute_single_trade_cycle(contract)

        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.trade_id, 1)
        self.assertEqual(outcome.direction, OrderDirection.SHORT)
        self.assertEqual(outcome.exit_reason, ExitReason.STOP_LOSS_HIT)
        self.assertTrue(outcome.is_loss)
        self.assertLess(outcome.realized_pnl_usdt, 0)


class TestVolumeSizingAndExposure(unittest.TestCase):
    """
    Tests volume sizing configurations (multiplier, absolute contracts)
    and verifies that Trade Quantity (Volume) != Margin.
    Margin = Trade Quantity / Leverage.
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log_dir = self.temp_dir.name

    def tearDown(self):
        logging.shutdown()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_volume_multiplier_execution(self):
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            mode=EngineMode.DRY_RUN,
            volume_mode="MULTIPLIER",
            volume_multiplier=3.0,  # 3x minimum volume
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        ticks = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.500, "bid1": 2.500, "ask1": 2.500},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.500, "bid1": 2.500, "ask1": 2.500},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.520, "bid1": 2.520, "ask1": 2.521}
        ]
        tick_call = [0]
        def mock_ticker(sym):
            idx = min(tick_call[0], len(ticks) - 1)
            tick_call[0] += 1
            return ticks[idx]
        engine.market.get_ticker = mock_ticker

        outcome = engine.execute_single_trade_cycle(contract)
        self.assertIsNotNone(outcome)
        # TRUMP min_volume is 1 contract. 3x multiplier -> 3 contracts
        self.assertEqual(outcome.vol_contracts, 3)
        self.assertAlmostEqual(outcome.underlying_quantity, 3 * contract.contract_size)
        # Verify Trade Quantity (Notional) != Margin
        self.assertNotEqual(outcome.notional_value_usdt, outcome.margin_used_usdt)
        # Margin = Trade Quantity / Leverage
        expected_margin = outcome.notional_value_usdt / outcome.leverage
        self.assertAlmostEqual(outcome.margin_used_usdt, expected_margin, places=4)

    def test_volume_absolute_contracts_execution(self):
        config = ExecutionConfig(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            mode=EngineMode.DRY_RUN,
            volume_mode="CONTRACTS",
            volume_contracts=5,  # Exactly 5 contracts
            logs_dir=self.test_log_dir,
            poll_interval_seconds=0.05
        )
        engine = TradeExecutionEngine(config=config)
        contract = engine.pre_flight_checks()

        ticks = [
            {"symbol": "TRUMP_USDT", "lastPrice": 2.500, "bid1": 2.500, "ask1": 2.500},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.500, "bid1": 2.500, "ask1": 2.500},
            {"symbol": "TRUMP_USDT", "lastPrice": 2.520, "bid1": 2.520, "ask1": 2.521}
        ]
        tick_call = [0]
        def mock_ticker(sym):
            idx = min(tick_call[0], len(ticks) - 1)
            tick_call[0] += 1
            return ticks[idx]
        engine.market.get_ticker = mock_ticker

        outcome = engine.execute_single_trade_cycle(contract)
        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.vol_contracts, 5)
        self.assertAlmostEqual(outcome.underlying_quantity, 5 * contract.contract_size)
        expected_margin = outcome.notional_value_usdt / outcome.leverage
        self.assertAlmostEqual(outcome.margin_used_usdt, expected_margin, places=4)


class TestGeneralizationMultiCoin(unittest.TestCase):
    """Verifies that the bot dynamically adapts to any coin (BTC, DOGE, PEPE, etc.)."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_high_precision_coin_doge(self):
        """Test DOGE_USDT with 5 decimal precision (pu=0.00001, ps=5)."""
        doge_contract = ContractInfo(
            symbol="DOGE_USDT",
            base_coin="DOGE",
            quote_coin="USDT",
            contract_size=10.0,
            price_unit=0.00001,
            volume_unit=1.0,
            price_precision=5,
            volume_precision=0,
            min_volume=1.0,
            max_volume=100000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.0067,
            initial_margin_ratio=0.0133,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["0.00001"],
            raw_data={}
        )
        strat = MasterplanStrategy(market=MagicMock())
        strat.config.symbol = "DOGE_USDT"
        strat.market.get_contract_detail.return_value = doge_contract

        # Entry = 0.12345, TP 2 pu -> 0.12347
        tp = strat.calculate_min_profit_tp(OrderDirection.LONG, 0.12345, doge_contract.price_unit, tp_ticks=2, precision=doge_contract.price_precision)
        self.assertEqual(tp, 0.12347)

        # SL 10 ticks -> 0.12345 - 0.00010 = 0.12335
        sl = strat.calculate_stop_loss(OrderDirection.LONG, 0.12345, 30, sl_ticks=10, price_unit=doge_contract.price_unit, precision=doge_contract.price_precision)
        self.assertEqual(sl, 0.12335)

    def test_low_precision_coin_btc(self):
        """Test BTC_USDT with 1 decimal precision (pu=0.1, ps=1)."""
        btc_contract = ContractInfo(
            symbol="BTC_USDT",
            base_coin="BTC",
            quote_coin="USDT",
            contract_size=0.0001,
            price_unit=0.1,
            volume_unit=1.0,
            price_precision=1,
            volume_precision=0,
            min_volume=1.0,
            max_volume=1000.0,
            min_leverage=1,
            max_leverage=125,
            maintenance_margin_ratio=0.004,
            initial_margin_ratio=0.008,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0001,
            depth_steps=["0.1"],
            raw_data={}
        )
        strat = MasterplanStrategy(market=MagicMock())
        strat.config.symbol = "BTC_USDT"
        strat.market.get_contract_detail.return_value = btc_contract

        # Entry = 64000.0, TP 2 pu -> 64000.2
        tp = strat.calculate_min_profit_tp(OrderDirection.LONG, 64000.0, btc_contract.price_unit, tp_ticks=2, precision=btc_contract.price_precision)
        self.assertEqual(tp, 64000.2)

        # SL 10 ticks -> 64000.0 - 1.0 = 63999.0
        sl = strat.calculate_stop_loss(OrderDirection.LONG, 64000.0, 30, sl_ticks=10, price_unit=btc_contract.price_unit, precision=btc_contract.price_precision)
        self.assertEqual(sl, 63999.0)

    def test_non_zero_fee_simulation_and_badge(self):
        """Test pair with non-zero taker fees in dry run."""
        btc_contract = ContractInfo(
            symbol="BTC_USDT",
            base_coin="BTC",
            quote_coin="USDT",
            contract_size=0.0001,
            price_unit=0.1,
            volume_unit=1.0,
            price_precision=1,
            volume_precision=0,
            min_volume=1.0,
            max_volume=1000.0,
            min_leverage=1,
            max_leverage=125,
            maintenance_margin_ratio=0.004,
            initial_margin_ratio=0.008,
            maker_fee_rate=0.0000,
            taker_fee_rate=0.0001,
            depth_steps=["0.1"],
            raw_data={}
        )
        cfg = ExecutionConfig(
            symbol="BTC_USDT",
            mode=EngineMode.DRY_RUN,
            logs_dir=self.tmp_dir,
            tp_ticks=2,
            leverage=50,
            poll_interval_seconds=0.1
        )
        engine = TradeExecutionEngine(config=cfg)
        engine.market.ping = MagicMock(return_value=True)
        engine.market.get_contract_detail = MagicMock(return_value=btc_contract)
        engine.market.get_inr_rate = MagicMock(return_value=90.0)
        engine.trader.client.config.auth_token = ""

        ticks = [
            {"symbol": "BTC_USDT", "lastPrice": 60000.0, "bid1": 60000.0, "ask1": 60000.0},
            {"symbol": "BTC_USDT", "lastPrice": 60000.0, "bid1": 60000.0, "ask1": 60000.0},
            {"symbol": "BTC_USDT", "lastPrice": 60000.5, "bid1": 60000.5, "ask1": 60000.6}
        ]
        call_idx = [0]
        def mock_ticker(sym):
            i = min(call_idx[0], len(ticks) - 1)
            call_idx[0] += 1
            return ticks[i]
        engine.market.get_ticker = mock_ticker

        outcome = engine.execute_single_trade_cycle(btc_contract)
        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.symbol, "BTC_USDT")
        self.assertEqual(outcome.base_coin, "BTC")
        self.assertEqual(outcome.price_precision, 1)
        self.assertGreater(outcome.fee_total_usdt, 0.0)

        # Check outcome card contains [Trading Fees: ... ] badge and not [Zero-Fee Pair]
        card = engine.outcome_logger.log_outcome(outcome)
        self.assertIn("[Trading Fees:", card)
        self.assertNotIn("[Zero-Fee Pair]", card)


class TestMicrostructureStrategy(unittest.TestCase):
    """Tests Market Microstructure Signal Generator and Sub-Strategy."""

    def test_rolling_z_and_ema(self):
        from kcex.engine.microstructure import RollingZ, EMA
        rz = RollingZ(maxlen=50, min_n=10)
        for i in range(9):
            rz.push(10.0)
        self.assertEqual(rz.z(10.0), 0.0)  # under min_n

        for i in range(20):
            rz.push(10.0 + (i % 3))
        self.assertGreater(rz.std(), 0.0)
        self.assertAlmostEqual(rz.z(rz.mean()), 0.0, places=3)

        ema = EMA(alpha=0.1, initial=10.0)
        val = ema.update(20.0)
        self.assertAlmostEqual(val, 11.0)

    def test_obi_and_spoof_discount(self):
        meta = SymbolMeta(symbol="TEST_USDT", pu=0.01, cs=1.0, minV=1.0)
        gen = MicrostructureSignalGenerator(meta=meta)
        t0 = 1000.0
        # Add depth snapshot
        gen.on_depth(
            bids=[(10.00, 100.0)],
            asks=[(10.01, 10.0)],
            ts=t0
        )
        # Immediately at t0, level weight is 0
        self.assertEqual(gen._level_weight("bid", 10.00, t0), 0.0)
        # After 1.0s, level weight is 1.0
        self.assertEqual(gen._level_weight("bid", 10.00, t0 + 1.0), 1.0)
        obi = gen._compute_obi(t0 + 1.0)
        self.assertGreater(obi, 0.5)

    def test_trade_delta_and_recency_burst(self):
        meta = SymbolMeta(symbol="TEST_USDT", pu=0.01, cs=1.0, minV=1.0)
        gen = MicrostructureSignalGenerator(meta=meta)
        t = 1000.0
        gen.on_deal(10.00, 5.0, "buy", ts=t)
        gen.on_deal(10.00, 5.0, "buy", ts=t + 1.6) # within 0.5s of t+2.0
        slow_sum, recency = gen._compute_delta(t + 2.0)
        self.assertEqual(slow_sum, 10.0)
        self.assertGreaterEqual(recency, 0.4)

    def test_vamp_deviation(self):
        meta = SymbolMeta(symbol="TEST_USDT", pu=0.01, cs=1.0, minV=1.0)
        gen = MicrostructureSignalGenerator(meta=meta)
        gen.bids = [(10.00, 500.0)]
        gen.asks = [(10.01, 10.0)]
        vamp_dev = gen._compute_vamp_deviation()
        self.assertGreater(vamp_dev, 0.0)

    def test_confluence_signal_generation_and_iceberg_veto(self):
        meta = SymbolMeta(symbol="TEST_USDT", pu=0.01, cs=1.0, minV=1.0)
        cfg = SignalConfig(
            stats_lookback=30,
            obi_z_threshold=1.0,
            delta_z_threshold=1.0,
            vamp_z_threshold=1.0,
            min_confluence=2,
            cooldown_s=0.1
        )
        gen = MicrostructureSignalGenerator(meta=meta, config=cfg)
        t = 1000.0
        # Warmup with balanced data
        for i in range(35):
            t += 0.5
            gen.on_depth([(10.00 - j * 0.01, 10.0) for j in range(5)],
                         [(10.01 + j * 0.01, 10.0) for j in range(5)], ts=t)
            gen.on_deal(10.01 if i % 2 == 0 else 10.00, 1.0, "buy" if i % 2 == 0 else "sell", ts=t)
            gen.generate(ts=t)

        # 1. Let warmup settle and establish solid bid wall, aging past 1.0s (not spoof discounted)
        t += 3.0
        gen.on_depth([(10.00, 300.0)], [(10.01, 20.0)], ts=t)
        t += 1.5
        gen.on_depth([(10.00, 300.0)], [(10.01, 20.0)], ts=t)

        # 2. Aggressive buyer trades at ask (10.01), thinning ask from 20 to 5 (1 tick spread, genuine fill)
        gen.on_deal(10.01, 15.0, "buy", ts=t)
        gen.on_depth([(10.00, 300.0)], [(10.01, 5.0)], ts=t)

        res = gen.generate(ts=t)
        self.assertIsNotNone(res)
        direction, target_ticks, metadata = res
        self.assertEqual(direction, "LONG")
        self.assertIn(target_ticks, [1, 2, 3])
        self.assertIn("agreeing_signals", metadata)

        # 3. Now test iceberg veto: if an iceberg defends the ask, LONG signals are vetoed
        gen._defended["ask"].veto_until = t + 5.0
        gen._last_signal_ts = 0.0  # reset cooldown
        vetoed_res = gen.generate(ts=t)
        self.assertIsNone(vetoed_res)  # Vetoed because ask is defended

    def test_microstructure_sub_strategy_execution(self):
        mock_market = MagicMock()
        mock_market.get_contract_detail.return_value = ContractInfo(
            symbol="TEST_USDT",
            base_coin="TEST",
            quote_coin="USDT",
            contract_size=1.0,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=3,
            volume_precision=0,
            min_volume=1.0,
            max_volume=1000.0,
            min_leverage=1,
            max_leverage=50,
            maintenance_margin_ratio=0.01,
            initial_margin_ratio=0.02,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["0.001"],
            raw_data={}
        )
        mock_market.get_order_book.return_value = {"bids": [[1.000, 10]], "asks": [[1.001, 10]]}
        mock_market.get_recent_trades.return_value = []

        sub = MicrostructureSubStrategy(
            market=mock_market,
            symbol="TEST_USDT",
            auto_start_feed=False,
            cooldown_seconds=5.0
        )
        self.assertIsNotNone(sub.generator)
        diag = sub.get_diagnostics()
        self.assertIn("obi", diag)
        sub.stop()


def run_all_tests():
    print("=" * 70)
    print("      RUNNING KCEX EXECUTION ENGINE TEST SUITE")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromNames([
        "test_engine.TestMasterplanStrategy",
        "test_engine.TestSubStrategyCycle",
        "test_engine.TestDualCurrencyAndLogging",
        "test_engine.TestEngineExecutionDryRun",
        "test_engine.TestVolumeSizingAndExposure",
        "test_engine.TestGeneralizationMultiCoin",
        "test_engine.TestMicrostructureStrategy"
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    return res.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


