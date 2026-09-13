"""
Unit Tests for OrderBlockDemandStrategy (Smart Money Concepts)
=============================================================
Validates:
1. Fractal swing high & low detection.
2. Strict body-close Break of Structure (BOS) rule vs. wick-only rejection.
3. Wick-to-wick Order Block origin candle marking (red candle for bullish, green for bearish).
4. Demand & Supply block detection: 3-5 consecutive impulse candles + FVG + structural extrema.
5. Setup invalidation upon direct blowout through zone boundary.
6. Retest mitigation: tap + rejection wick + directional confirmation candle close.
7. Dynamic 1:2 Risk-to-Reward calculation and SL placement behind the block.
8. Exchange fee schedule verification: 0.0% on TRUMP/DOGE, 0.01% taker on others.
"""

import math
import unittest
from unittest.mock import MagicMock

from kcex.engine.models import OrderDirection, TradeSignal, ExecutionConfig, ExitReason
from strategies.order_block_demand import (
    OrderBlockDemandStrategy,
    SmartMoneyZone,
    ZoneType,
    ZoneStatus,
    SwingPoint,
    SwingStructureDetector
)
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.data_loader import Candle
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine, VirtualClock





class TestOrderBlockDemandStrategy(unittest.TestCase):

    def setUp(self):
        self.mock_market = MagicMock()
        mock_contract = MagicMock()
        mock_contract.price_unit = 0.001
        mock_contract.price_precision = 4
        self.mock_market.get_contract_detail.return_value = mock_contract

        self.strategy = OrderBlockDemandStrategy(
            market=self.mock_market,
            symbol="TRUMP_USDT",
            interval="Min1",
            risk_reward_ratio=2.0,
            buffer_ticks=1,
            min_sl_ticks=3,
            max_sl_ticks=35,
            require_closed_candle=False
        )

    def test_swing_structure_detector(self):
        # 10 candles with a clear peak at index 4 and trough at index 7
        highs = [10.0, 10.2, 10.4, 10.6, 11.0, 10.5, 10.2, 9.8, 10.1, 10.3]
        lows  = [ 9.8, 10.0, 10.2, 10.3, 10.7, 10.1,  9.9, 9.4,  9.7, 10.0]
        ts    = [1000 + i * 60 for i in range(10)]

        swings = SwingStructureDetector.find_swings(highs, lows, ts, left_bars=2, right_bars=2)
        shs = [s for s in swings if s.is_high]
        sls = [s for s in swings if not s.is_high]

        self.assertTrue(any(s.bar_idx == 4 and s.price == 11.0 for s in shs))
        self.assertTrue(any(s.bar_idx == 7 and s.price == 9.4 for s in sls))

    def test_strict_body_close_bos_vs_wick_sweep(self):
        """
        Vivek's Rule:
        If a candle pierces the swing high only with a wick, it is NOT a BOS.
        It must close with its body above the prior swing high to be a valid BOS.
        """
        highs = [10.0, 10.5, 10.1, 10.2, 10.0, 10.6, 10.7]  # Bar 5 has high 10.6, close 10.3
        lows  = [ 9.8, 10.0,  9.9, 10.0,  9.7, 10.1, 10.2]
        opens = [ 9.9, 10.1, 10.4, 10.1,  9.9, 10.2, 10.3]
        closes= [10.1, 10.4, 10.2, 10.0,  9.8, 10.3, 10.65] # Bar 5 close 10.3 <= swing high 10.5 (Wick sweep)
        ts    = [1000 + i * 60 for i in range(7)]

        swings = [
            SwingPoint(bar_idx=1, ts=ts[1], price=10.5, is_high=True),
            SwingPoint(bar_idx=4, ts=ts[4], price=9.7, is_high=False)
        ]

        # Evaluating Bar 5 (Wick sweep: high=10.6 > 10.5, but close=10.3 <= 10.5)
        # Should NOT discover an OB at bar 5
        discovered_sweep = self.strategy.scan_for_order_blocks(
            ts[:6], opens[:6], highs[:6], lows[:6], closes[:6], swings
        )
        self.assertEqual(len(discovered_sweep), 0, "Wick sweep must not trigger an Order Block!")

        # Evaluating Bar 6 (Body close: close=10.65 > 10.5)
        # Should successfully discover an Order Block at the origin red candle (bar 4)
        discovered_bos = self.strategy.scan_for_order_blocks(
            ts, opens, highs, lows, closes, swings
        )
        self.assertGreaterEqual(len(discovered_bos), 1, "Body close above swing high must trigger Bullish OB!")
        ob = discovered_bos[0]
        self.assertEqual(ob.zone_type, ZoneType.BULLISH_ORDER_BLOCK)
        # Full wick-to-wick marking
        self.assertEqual(ob.high, highs[4])
        self.assertEqual(ob.low, lows[4])

    def test_demand_block_consecutive_impulse_and_fvg(self):
        """
        Vivek's Rule:
        Demand requires 3-5 consecutive green candles at structural bottom + FVG creation.
        """
        # Build 35 background candles + 1 red origin candle at bottom + 3 strong green impulse candles
        base = 2.000
        opens, highs, lows, closes, ts = [], [], [], [], []
        for i in range(30):
            ts.append(1000 + i * 60)
            opens.append(base + 0.10 - i * 0.003)
            highs.append(opens[-1] + 0.002)
            lows.append(opens[-1] - 0.002)
            closes.append(opens[-1] - 0.001)

        # Bar 30: Last Red Candle at range bottom (Origin)
        ts.append(1000 + 30 * 60)
        opens.append(1.910)
        highs.append(1.912)
        lows.append(1.905)
        closes.append(1.906) # Red

        # Bar 31, 32, 33: 3 consecutive aggressive green candles creating FVG
        # Candle 1 (Bar 31)
        ts.append(1000 + 31 * 60)
        opens.append(1.908)
        highs.append(1.920)
        lows.append(1.907)
        closes.append(1.919)

        # Candle 2 (Bar 32)
        ts.append(1000 + 32 * 60)
        opens.append(1.920)
        highs.append(1.940)
        lows.append(1.918)
        closes.append(1.938)

        # Candle 3 (Bar 33): low 1.925 > Candle 1 high 1.912 -> Fair Value Gap!
        ts.append(1000 + 33 * 60)
        opens.append(1.939)
        highs.append(1.960)
        lows.append(1.925)
        closes.append(1.958)

        demand_zones = self.strategy.scan_for_demand_supply_blocks(ts, opens, highs, lows, closes)
        self.assertGreaterEqual(len(demand_zones), 1, "Should detect Demand Block from 3 consecutive green bars + FVG at bottom")
        dz = demand_zones[0]
        self.assertEqual(dz.zone_type, ZoneType.DEMAND_BLOCK)
        self.assertEqual(dz.creation_bar_idx, 30)
        self.assertEqual(dz.consecutive_candles, 3)
        self.assertGreater(dz.fvg_size, 0.0, "Displacement must create Fair Value Gap")

    def test_zone_invalidation_on_direct_blowout(self):
        """
        Vivek's Rule:
        If market directly blows through the Order Block with a body close,
        the setup is immediately invalidated.
        """
        zone = SmartMoneyZone(
            zone_id="OB_TEST_1",
            zone_type=ZoneType.BULLISH_ORDER_BLOCK,
            symbol="TRUMP_USDT",
            high=2.500,
            low=2.480,
            body_high=2.495,
            body_low=2.485,
            creation_bar_idx=10,
            creation_ts=1000
        )
        self.strategy.active_zones["OB_TEST_1"] = zone

        # Next candle closes below zone.low (2.480) -> e.g. close = 2.470
        opens = [2.490]
        highs = [2.495]
        lows = [2.465]
        closes = [2.470]

        self.strategy.update_zone_lifecycle([], 0, opens, highs, lows, closes)
        self.assertNotIn("OB_TEST_1", self.strategy.active_zones, "Zone must be invalidated when candle body closes through it")

    def test_rejection_wick_and_green_confirmation_signal(self):
        """
        Vivek's Rule (User Requirements 2, 3, 4):
        Candle T: Retests zone + forms lower rejection wick.
        Candle T+1: Next candle closes GREEN confirming buyers defend the zone.
        Entry at close of Candle T+1 with 1:2 R:R dynamic targets.
        """
        zone = SmartMoneyZone(
            zone_id="OB_BULL_ACTIVE",
            zone_type=ZoneType.BULLISH_ORDER_BLOCK,
            symbol="TRUMP_USDT",
            high=2.500,
            low=2.480,
            body_high=2.495,
            body_low=2.485,
            creation_bar_idx=5,
            creation_ts=1000
        )
        self.strategy.active_zones["OB_BULL_ACTIVE"] = zone

        # Create 40 bars so history >= 30
        mock_bars = []
        for i in range(38):
            mock_bars.append({
                "timestamp": 1000 + i * 60,
                "open": 2.510,
                "high": 2.515,
                "low": 2.505,
                "close": 2.512,
                "volume": 100.0
            })

        # Bar 38 (Candle T): Retests zone with prominent lower rejection wick
        # open = 2.495, high = 2.505, low = 2.482, close = 2.496
        # lower wick = min(2.495, 2.496) - 2.482 = 0.013
        # range = 2.505 - 2.482 = 0.023 -> 56.5% wick ratio >= 15%
        mock_bars.append({
            "timestamp": 1000 + 38 * 60,
            "open": 2.495,
            "high": 2.505,
            "low": 2.482,
            "close": 2.496,
            "volume": 200.0
        })

        # Bar 39 (Candle T+1): Next candle closes GREEN confirming the bounce
        # open = 2.496, high = 2.506, low = 2.494, close = 2.504 (green close)
        mock_bars.append({
            "timestamp": 1000 + 39 * 60,
            "open": 2.496,
            "high": 2.506,
            "low": 2.494,
            "close": 2.504,
            "volume": 250.0
        })
        self.mock_market.get_klines.return_value = mock_bars

        signal = self.strategy.generate_signal("TRUMP_USDT")
        self.assertIsNotNone(signal, "Should generate LONG signal upon Candle T tap+wick followed by Candle T+1 green confirmation close")
        self.assertEqual(signal.direction, OrderDirection.LONG)

        # Check Dynamic 1:2 R:R
        # Stop Loss: min(zone.low 2.480, wick_low 2.482) - buffer (0.001) = 2.479
        # Entry: 2.504
        # Risk: 2.504 - 2.479 = 0.025 -> 25 ticks
        # Target TP: 2 * 25 = 50 ticks
        self.assertEqual(signal.metadata["target_sl_ticks"], 25)
        self.assertEqual(signal.metadata["target_ticks"], 50)
        self.assertEqual(signal.metadata["risk_reward_ratio"], 2.0)
        self.assertEqual(signal.metadata["stop_loss_price"], 2.479)
        self.assertEqual(signal.metadata["take_profit_price"], 2.554)

        # Confirm zone is now MITIGATED and cannot be traded again
        self.assertNotIn("OB_BULL_ACTIVE", self.strategy.active_zones)
        self.assertIn(1000, self.strategy.resolved_origin_ts)

    def test_bearish_order_block_tap_and_red_confirmation(self):
        """
        Vivek's Rule (Bearish):
        Candle T: Retests Bearish OB overhead + forms upper rejection wick.
        Candle T+1: Next candle closes RED confirming sellers defend the zone.
        Entry at close of Candle T+1 with 1:2 R:R dynamic targets.
        """
        zone = SmartMoneyZone(
            zone_id="OB_BEAR_ACTIVE",
            zone_type=ZoneType.BEARISH_ORDER_BLOCK,
            symbol="TRUMP_USDT",
            high=2.520,
            low=2.500,
            body_high=2.515,
            body_low=2.505,
            creation_bar_idx=5,
            creation_ts=2000
        )
        self.strategy.active_zones["OB_BEAR_ACTIVE"] = zone

        mock_bars = []
        for i in range(38):
            mock_bars.append({
                "timestamp": 1000 + i * 60,
                "open": 2.490,
                "high": 2.495,
                "low": 2.485,
                "close": 2.488,
                "volume": 100.0
            })

        # Bar 38 (Candle T): Retests Bearish OB with upper rejection wick
        # open = 2.505, high = 2.518, low = 2.500, close = 2.504
        # upper wick = 2.518 - max(2.505, 2.504) = 0.013
        # range = 2.518 - 2.500 = 0.018 -> 72% upper wick ratio
        mock_bars.append({
            "timestamp": 1000 + 38 * 60,
            "open": 2.505,
            "high": 2.518,
            "low": 2.500,
            "close": 2.504,
            "volume": 200.0
        })

        # Bar 39 (Candle T+1): Next candle closes RED confirming the rejection
        # open = 2.504, high = 2.505, low = 2.492, close = 2.494 (red close)
        mock_bars.append({
            "timestamp": 1000 + 39 * 60,
            "open": 2.504,
            "high": 2.505,
            "low": 2.492,
            "close": 2.494,
            "volume": 250.0
        })
        self.mock_market.get_klines.return_value = mock_bars

        signal = self.strategy.generate_signal("TRUMP_USDT")
        self.assertIsNotNone(signal, "Should generate SHORT signal upon Candle T tap+wick followed by Candle T+1 red confirmation close")
        self.assertEqual(signal.direction, OrderDirection.SHORT)

        # Check Dynamic 1:2 R:R
        # Stop Loss: max(zone.high 2.520, wick_high 2.518) + buffer (0.001) = 2.521
        # Entry: 2.494
        # Risk: 2.521 - 2.494 = 0.027 -> 27 ticks
        # Target TP: 2 * 27 = 54 ticks
        self.assertEqual(signal.metadata["target_sl_ticks"], 27)
        self.assertEqual(signal.metadata["target_ticks"], 54)
        self.assertEqual(signal.metadata["risk_reward_ratio"], 2.0)
        self.assertEqual(signal.metadata["stop_loss_price"], 2.521)
        self.assertEqual(signal.metadata["take_profit_price"], 2.440)

        # Confirm zone is now MITIGATED and cannot be traded again
        self.assertNotIn("OB_BEAR_ACTIVE", self.strategy.active_zones)
        self.assertIn(2000, self.strategy.resolved_origin_ts)

    def test_mitigated_zone_never_recreated(self):
        """
        Anti-Recreation Rule:
        Once an Order Block origin candle is resolved/mitigated, subsequent scans
        must never re-create that zone, preventing overtrading loops.
        """
        # Populate history with an OB origin at bar 2
        ts = [1000 + i * 60 for i in range(10)]
        opens = [2.50, 2.50, 2.49, 2.50, 2.51, 2.52, 2.53, 2.54, 2.55, 2.56]
        highs = [2.51, 2.51, 2.50, 2.51, 2.52, 2.53, 2.54, 2.55, 2.56, 2.57]
        lows  = [2.49, 2.49, 2.48, 2.49, 2.50, 2.51, 2.52, 2.53, 2.54, 2.55]
        closes= [2.50, 2.50, 2.485, 2.505, 2.515, 2.525, 2.535, 2.545, 2.555, 2.565]

        # Scan initially
        zones_first = self.strategy.scan_for_order_blocks(ts, opens, highs, lows, closes)
        self.assertGreaterEqual(len(zones_first), 1)

        # Mark origin timestamp as resolved
        origin_ts = zones_first[0].creation_ts
        self.strategy.resolved_origin_ts.add(origin_ts)

        # Scan again - should NOT re-create the resolved zone
        zones_second = self.strategy.scan_for_order_blocks(ts, opens, highs, lows, closes)
        self.assertFalse(any(z.creation_ts == origin_ts for z in zones_second))

    def test_fee_schedule_zero_on_trump_doge_and_001_on_others(self):
        """
        Exchange Fee Rule:
        TRUMP & DOGE enjoy 0.0% maker and 0.0% taker fees.
        Other coins have 0.0% maker and 0.01% taker fees.
        """
        sim_market = BacktestMarket(fee_mode="LIVE")

        trump_contract = sim_market.get_contract_detail("TRUMP_USDT")
        self.assertEqual(trump_contract.maker_fee_rate, 0.0)
        self.assertEqual(trump_contract.taker_fee_rate, 0.0)

        doge_contract = sim_market.get_contract_detail("DOGE_USDT")
        self.assertEqual(doge_contract.maker_fee_rate, 0.0)
        self.assertEqual(doge_contract.taker_fee_rate, 0.0)

        btc_contract = sim_market.get_contract_detail("BTC_USDT")
        self.assertEqual(btc_contract.maker_fee_rate, 0.0)
        self.assertAlmostEqual(btc_contract.taker_fee_rate, 0.0001, places=6)  # 0.01% taker fee

    def test_smc_execution_multi_contract_full_target(self):
        """
        Multi-contract (>=2) SMC Execution:
        Hits 1:1 TP -> 50% exits at 1:1, SL moved to Breakeven (+1 tick).
        Then hits 1:2 TP -> remaining 50% exits at 1:2.
        Resulting exit price is blended (50% @ 1:1 + 50% @ 1:2).
        """
        config = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            initial_balance_usdt=100.0,
            leverage=25,
            volume_contracts=2,
            fee_mode="LIVE",
            use_tick_data=False,
            tick_fallback_to_candle=True,
            partial_tp_enabled=True,
            breakeven_buffer_ticks=1,
            strategy_mode="ORDER_BLOCK_DEMAND"
        )
        sim_engine = BacktestExecutionEngine(config=config)

        # Entry = 2.500. SL = 2.480 (20 ticks). 1:1 TP = 2.520. 1:2 TP = 2.540 (40 ticks).
        signal = TradeSignal(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="OrderBlockDemandStrategy",
            metadata={
                "strategy_mode": "ORDER_BLOCK_DEMAND",
                "zone_id": "TEST_DB_1",
                "target_sl_ticks": 20,
                "target_ticks": 40,
                "target_1to1_price": 2.520,
                "target_1to2_price": 2.540,
                "partial_tp_enabled": True,
                "breakeven_buffer_ticks": 1
            }
        )

        candles = [
            Candle(open_time_ms=1000, open=2.495, high=2.502, low=2.490, close=2.500, volume=100, close_time_ms=1059999),
            Candle(open_time_ms=1060000, open=2.500, high=2.525, low=2.498, close=2.522, volume=150, close_time_ms=1119999),
            Candle(open_time_ms=1120000, open=2.522, high=2.545, low=2.515, close=2.542, volume=200, close_time_ms=1179999),
        ]

        clock = VirtualClock(initial_time_sec=1000.0)
        outcome, exit_idx = sim_engine._execute_simulated_trade(
            trade_id=1, signal=signal, entry_candle=candles[0], all_candles=candles, entry_idx=0, clock=clock
        )
        self.assertIsNotNone(outcome)
        self.assertTrue(outcome.smc_partial_tp_hit, "SMC partial TP must be recorded as hit")
        # Blended price: (1 * 2.520 + 1 * 2.540) / 2 = 2.530
        self.assertAlmostEqual(outcome.exit_price, 2.530, places=3)
        self.assertGreater(outcome.realized_pnl_usdt, 0.0)
        self.assertEqual(outcome.fee_total_usdt, 0.0)

    def test_smc_execution_multi_contract_breakeven_exit(self):
        """
        Multi-contract (>=2) SMC Execution with pull-back to Breakeven:
        Hits 1:1 TP -> 50% exits at 1:1, SL moved to BE (+1 tick buffer = 2.501).
        Then market reverses and drops through 2.501.
        Runner exits at 2.501. Blended exit price = (2.520 + 2.501) / 2 = 2.511.
        Trade is guaranteed profitable & risk-free!
        """
        config = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            initial_balance_usdt=100.0,
            leverage=25,
            volume_contracts=2,
            fee_mode="LIVE",
            use_tick_data=False,
            tick_fallback_to_candle=True,
            partial_tp_enabled=True,
            breakeven_buffer_ticks=1,
            strategy_mode="ORDER_BLOCK_DEMAND"
        )
        sim_engine = BacktestExecutionEngine(config=config)

        signal = TradeSignal(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="OrderBlockDemandStrategy",
            metadata={
                "strategy_mode": "ORDER_BLOCK_DEMAND",
                "zone_id": "TEST_DB_2",
                "target_sl_ticks": 20,
                "target_ticks": 40,
                "target_1to1_price": 2.520,
                "target_1to2_price": 2.540,
                "partial_tp_enabled": True,
                "breakeven_buffer_ticks": 1
            }
        )

        candles = [
            Candle(open_time_ms=1000, open=2.495, high=2.502, low=2.490, close=2.500, volume=100, close_time_ms=1059999),
            Candle(open_time_ms=1060000, open=2.500, high=2.525, low=2.500, close=2.518, volume=150, close_time_ms=1119999),
            Candle(open_time_ms=1120000, open=2.518, high=2.520, low=2.498, close=2.500, volume=200, close_time_ms=1179999),
        ]

        clock = VirtualClock(initial_time_sec=1000.0)
        outcome, exit_idx = sim_engine._execute_simulated_trade(
            trade_id=1, signal=signal, entry_candle=candles[0], all_candles=candles, entry_idx=0, clock=clock
        )
        self.assertIsNotNone(outcome)
        self.assertTrue(outcome.smc_partial_tp_hit)
        # Blended: (2.520 + 2.501) / 2 = 2.5105 -> round to 3 decimals = 2.510
        self.assertAlmostEqual(outcome.exit_price, 2.510, places=3)
        self.assertGreater(outcome.realized_pnl_usdt, 0.0, "Trade must be net profitable even on BE stop out!")

    def test_smc_execution_1_contract_be_runner(self):
        """
        1-Contract SMC Execution (1TO2_WITH_BE mode):
        Cannot divide 1 contract.
        Hits 1:1 TP -> locks SL at Breakeven (+1 tick buffer: 2.501).
        Then hits 1:2 TP -> full contract exits at 2.540.
        """
        config = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            initial_balance_usdt=100.0,
            leverage=25,
            volume_contracts=1,
            fee_mode="LIVE",
            use_tick_data=False,
            tick_fallback_to_candle=True,
            partial_tp_enabled=True,
            breakeven_buffer_ticks=1,
            smc_1x_exit_mode="1TO2_WITH_BE",
            strategy_mode="ORDER_BLOCK_DEMAND"
        )
        sim_engine = BacktestExecutionEngine(config=config)

        signal = TradeSignal(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="OrderBlockDemandStrategy",
            metadata={
                "strategy_mode": "ORDER_BLOCK_DEMAND",
                "zone_id": "TEST_DB_3",
                "target_sl_ticks": 20,
                "target_ticks": 40,
                "target_1to1_price": 2.520,
                "target_1to2_price": 2.540,
                "partial_tp_enabled": True,
                "breakeven_buffer_ticks": 1
            }
        )

        candles = [
            Candle(open_time_ms=1000, open=2.495, high=2.502, low=2.490, close=2.500, volume=100, close_time_ms=1059999),
            Candle(open_time_ms=1060000, open=2.500, high=2.525, low=2.500, close=2.518, volume=150, close_time_ms=1119999),
            Candle(open_time_ms=1120000, open=2.518, high=2.545, low=2.515, close=2.542, volume=200, close_time_ms=1179999),
        ]

        clock = VirtualClock(initial_time_sec=1000.0)
        outcome, exit_idx = sim_engine._execute_simulated_trade(
            trade_id=1, signal=signal, entry_candle=candles[0], all_candles=candles, entry_idx=0, clock=clock
        )
        self.assertIsNotNone(outcome)
        self.assertTrue(outcome.smc_partial_tp_hit)
        self.assertAlmostEqual(outcome.exit_price, 2.540, places=3)
        self.assertEqual(outcome.exit_reason, ExitReason.MIN_PROFIT_TP_HIT)

    def test_smc_execution_1_contract_1to1_exit_mode(self):
        """
        1-Contract SMC Execution (1TO1_TP mode):
        Hits 1:1 TP -> closes 100% of the position immediately at 1:1.
        """
        config = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            initial_balance_usdt=100.0,
            leverage=25,
            volume_contracts=1,
            fee_mode="LIVE",
            use_tick_data=False,
            tick_fallback_to_candle=True,
            partial_tp_enabled=True,
            breakeven_buffer_ticks=1,
            smc_1x_exit_mode="1TO1_TP",
            strategy_mode="ORDER_BLOCK_DEMAND"
        )
        sim_engine = BacktestExecutionEngine(config=config)

        signal = TradeSignal(
            symbol="TRUMP_USDT",
            direction=OrderDirection.LONG,
            sub_strategy_name="OrderBlockDemandStrategy",
            metadata={
                "strategy_mode": "ORDER_BLOCK_DEMAND",
                "zone_id": "TEST_DB_4",
                "target_sl_ticks": 20,
                "target_ticks": 40,
                "target_1to1_price": 2.520,
                "target_1to2_price": 2.540,
                "partial_tp_enabled": True,
                "breakeven_buffer_ticks": 1
            }
        )

        candles = [
            Candle(open_time_ms=1000, open=2.495, high=2.502, low=2.490, close=2.500, volume=100, close_time_ms=1059999),
            Candle(open_time_ms=1060000, open=2.500, high=2.525, low=2.500, close=2.518, volume=150, close_time_ms=1119999),
        ]

        clock = VirtualClock(initial_time_sec=1000.0)
        outcome, exit_idx = sim_engine._execute_simulated_trade(
            trade_id=1, signal=signal, entry_candle=candles[0], all_candles=candles, entry_idx=0, clock=clock
        )
        self.assertIsNotNone(outcome)
        self.assertAlmostEqual(outcome.exit_price, 2.520, places=3)
        self.assertEqual(outcome.exit_reason, ExitReason.MIN_PROFIT_TP_HIT)


if __name__ == "__main__":
    unittest.main()

