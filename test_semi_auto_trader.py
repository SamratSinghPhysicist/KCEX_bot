"""
Test Suite for KCEX Semi-Autonomous Trade Execution Script (semi_auto_trader.py)
==============================================================================
Verifies:
1. TradePreset initialization and formatting
2. Target TP/SL price calculations for LONG & SHORT across all modes (Ticks, ROE, Price %, Absolute)
3. Position sizing resolution (Contracts, Margin USDT, Notional USDT, Coin Qty)
4. Dry-run single-trade cycle execution and outcome reporting
5. Preset retention for consecutive trade cycles
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from semi_auto_trader import (
    TradePreset,
    init_default_preset,
    compute_target_prices,
    print_pre_trade_report,
    execute_single_trade_cycle,
    OrderDirection,
    EngineMode,
    ExitReason
)
from kcex.config import KCEXConfig
from kcex.client import KCEXClient
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator
from kcex.trade import KCEXTrader


class TestSemiAutoTrader(unittest.TestCase):
    def setUp(self):
        self.config = KCEXConfig()
        self.client = KCEXClient(self.config)
        self.market = KCEXMarket(self.client)
        self.risk = KCEXRiskCalculator(self.market, self.client)
        self.trader = KCEXTrader(self.client, self.market, self.risk)

    def test_preset_initialization(self):
        preset = init_default_preset(self.config)
        self.assertIsNotNone(preset.symbol)
        self.assertGreaterEqual(preset.leverage, 1)
        self.assertIn(preset.qty_mode, ["CONTRACTS", "MARGIN_USDT", "NOTIONAL_USDT", "COIN_QTY"])
        self.assertIn(preset.tp_mode, ["TICKS", "ROE_PCT", "PRICE_PCT", "ABSOLUTE"])

        summary = preset.summary_lines()
        self.assertEqual(len(summary), 5)

    def test_compute_target_prices_long(self):
        # Long entry at 2.0000, pu = 0.001, leverage = 20
        # 1. Ticks
        tp, sl = compute_target_prices(
            direction=OrderDirection.LONG,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="TICKS",
            tp_val=2,
            sl_mode="TICKS",
            sl_val=10
        )
        self.assertEqual(tp, 2.0020)
        self.assertEqual(sl, 1.9900)

        # 2. ROE % (10% ROE at 20x lev = 0.5% price move)
        tp_roe, sl_roe = compute_target_prices(
            direction=OrderDirection.LONG,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="ROE_PCT",
            tp_val=10.0,
            sl_mode="ROE_PCT",
            sl_val=20.0
        )
        self.assertEqual(tp_roe, 2.0100)
        self.assertEqual(sl_roe, 1.9800)

        # 3. Price % (1% move)
        tp_pct, sl_pct = compute_target_prices(
            direction=OrderDirection.LONG,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="PRICE_PCT",
            tp_val=1.0,
            sl_mode="PRICE_PCT",
            sl_val=2.0
        )
        self.assertEqual(tp_pct, 2.0200)
        self.assertEqual(sl_pct, 1.9600)

    def test_compute_target_prices_short(self):
        # Short entry at 2.0000, pu = 0.001, leverage = 20
        # 1. Ticks
        tp, sl = compute_target_prices(
            direction=OrderDirection.SHORT,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="TICKS",
            tp_val=3,
            sl_mode="TICKS",
            sl_val=15
        )
        self.assertEqual(tp, 1.9970)
        self.assertEqual(sl, 2.0150)

        # 2. ROE % (10% ROE at 20x = 0.5% price drop)
        tp_roe, sl_roe = compute_target_prices(
            direction=OrderDirection.SHORT,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="ROE_PCT",
            tp_val=10.0,
            sl_mode="ROE_PCT",
            sl_val=20.0
        )
        self.assertEqual(tp_roe, 1.9900)
        self.assertEqual(sl_roe, 2.0200)

    def test_disabled_stop_loss(self):
        tp, sl = compute_target_prices(
            direction=OrderDirection.LONG,
            entry_price=2.0000,
            pu=0.001,
            precision=4,
            leverage=20,
            tp_mode="TICKS",
            tp_val=2,
            sl_mode="NONE",
            sl_val=None
        )
        self.assertEqual(tp, 2.0020)
        self.assertIsNone(sl)

    def test_quantity_conversions(self):
        # Mock contract TRUMP_USDT (cs=0.1, minV=1, price=2.0)
        contract = ContractInfo(
            symbol="TRUMP_USDT",
            base_coin="TRUMP",
            quote_coin="USDT",
            contract_size=0.1,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=4,
            volume_precision=0,
            min_volume=1.0,
            max_volume=10000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.0067,
            initial_margin_ratio=0.0133,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["1"],
            raw_data={}
        )

        with patch.object(self.market, "get_contract_detail", return_value=contract):
            # 1. By margin: 1 USDT margin at 20x leverage = 20 USDT notional
            # 1 contract = 0.1 TRUMP * 2.0 USDT = 0.2 USDT
            # 20 USDT / 0.2 = 100 contracts
            vol = self.risk.convert_usdt_to_contracts("TRUMP_USDT", target_usdt=20.0, price=2.0)
            self.assertEqual(vol, 100)

            # 2. By coin qty: 50 TRUMP / 0.1 = 500 contracts
            vol_coins = self.risk.convert_coin_qty_to_contracts("TRUMP_USDT", target_coin_qty=50.0)
            self.assertEqual(vol_coins, 500)

    def test_simulated_trade_cycle_execution(self):
        """Simulates full execute_single_trade_cycle in dry-run mode with mocked ticker and inputs."""
        preset = TradePreset(
            symbol="TRUMP_USDT",
            leverage=30,
            is_isolated=True,
            qty_mode="CONTRACTS",
            qty_val=1.0,
            tp_mode="TICKS",
            tp_val=2.0,
            sl_mode="ROE_PCT",
            sl_val=15.0,
            mode=EngineMode.DRY_RUN
        )

        contract = ContractInfo(
            symbol="TRUMP_USDT",
            base_coin="TRUMP",
            quote_coin="USDT",
            contract_size=0.1,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=4,
            volume_precision=0,
            min_volume=1.0,
            max_volume=10000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.0067,
            initial_margin_ratio=0.0133,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["1"],
            raw_data={}
        )

        ticker_data = {"lastPrice": "2.3500", "fairPrice": "2.3500"}

        with patch.object(self.market, "get_contract_detail", return_value=contract), \
             patch.object(self.market, "get_ticker", return_value=ticker_data), \
             patch.object(self.market, "get_inr_rate", return_value=94.50), \
             patch("builtins.input", return_value="y"), \
             patch("semi_auto_trader.monitor_position_until_closed", return_value=(2.3520, ExitReason.MIN_PROFIT_TP_HIT, None)):

            result = execute_single_trade_cycle(
                preset=preset,
                direction=OrderDirection.LONG,
                trade_num=1,
                market=self.market,
                trader=self.trader,
                risk=self.risk
            )
            self.assertTrue(result)

    def test_reconcile_exit_from_kcex(self):
        from semi_auto_trader import reconcile_exit_from_kcex

        # 1. Test TP Hit reconciliation when profit > 0
        mock_orders_win = {
            "data": [
                {"side": 4, "dealVol": 2, "dealAvgPrice": 2.392, "profit": 0.0002, "externalOid": "stoporder_TAKE_PROFIT_123", "positionId": 12345}
            ]
        }
        with patch.object(self.client, "get_private", return_value=mock_orders_win):
            exit_p, pnl, reason = reconcile_exit_from_kcex(
                trader=self.trader,
                symbol="TRUMP_USDT",
                position_id=12345,
                direction=OrderDirection.LONG,
                entry_price=2.390,
                fallback_price=2.392
            )
            self.assertEqual(reason, ExitReason.MIN_PROFIT_TP_HIT)
            self.assertEqual(exit_p, 2.392)
            self.assertEqual(pnl, 0.0002)

        # 2. Test SL Hit reconciliation when profit < 0
        mock_orders_loss = {
            "data": [
                {"side": 2, "dealVol": 2, "dealAvgPrice": 2.403, "profit": -0.0020, "externalOid": "stoporder_STOP_LOSS_456", "positionId": 12345}
            ]
        }
        with patch.object(self.client, "get_private", return_value=mock_orders_loss):
            exit_p, pnl, reason = reconcile_exit_from_kcex(
                trader=self.trader,
                symbol="TRUMP_USDT",
                position_id=12345,
                direction=OrderDirection.SHORT,
                entry_price=2.393,
                fallback_price=2.403
            )
            self.assertEqual(reason, ExitReason.STOP_LOSS_HIT)
            self.assertEqual(exit_p, 2.403)
            self.assertEqual(pnl, -0.0020)

    def test_close_position_taker_price_offset(self):
        """Verifies that trader.close_position offsets prices to cross the spread for taker fill."""
        contract = ContractInfo(
            symbol="TRUMP_USDT",
            base_coin="TRUMP",
            quote_coin="USDT",
            contract_size=0.1,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=3,
            volume_precision=0,
            min_volume=1.0,
            max_volume=10000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.0067,
            initial_margin_ratio=0.0133,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["1"],
            raw_data={}
        )

        with patch.object(self.market, "get_contract_detail", return_value=contract), \
             patch.object(self.client, "post_private", return_value={"success": True, "code": 0, "data": {"orderId": "999"}}) as mock_post:

            # Long close: price must be offset downwards into bids
            self.trader.close_position(
                position_id=1001,
                symbol="TRUMP_USDT",
                side="LONG",
                vol_contracts=2,
                leverage=75,
                is_market=True,
                price=2.390
            )
            call_payload = mock_post.call_args[1]["json_data"]
            sent_price = float(call_payload["price"])
            self.assertLess(sent_price, 2.390)
            self.assertEqual(call_payload["side"], 4)

            # Short close: price must be offset upwards into asks
            self.trader.close_position(
                position_id=1001,
                symbol="TRUMP_USDT",
                side="SHORT",
                vol_contracts=2,
                leverage=75,
                is_market=True,
                price=2.390
            )
            call_payload_short = mock_post.call_args[1]["json_data"]
            self.assertEqual(call_payload["type"], 5)
            self.assertEqual(call_payload_short["type"], 5)

    def test_target_prices_liquidation_clamping(self):
        """Verifies that Stop Loss is clamped safely inside liquidation threshold."""
        # Short with entry 2.393, 75x leverage, 30% ROE loss
        # Without clamping, 30% ROE at 75x is 2.403, which is WORSE than liquidation 2.400!
        tp, sl = compute_target_prices(
            direction=OrderDirection.SHORT,
            entry_price=2.393,
            pu=0.001,
            precision=3,
            leverage=75,
            tp_mode="TICKS",
            tp_val=1,
            sl_mode="ROE_PCT",
            sl_val=30.0,
            liq_price=2.400
        )
        self.assertEqual(tp, 2.392)
        # SL must be strictly below liquidation price 2.400
        self.assertLess(sl, 2.400)
        self.assertGreater(sl, 2.393)

    def test_tp_requires_executable_bid_for_long(self):
        """Verifies that for a LONG position, if lastPrice is at TP but bid1 is below entry/TP, it does NOT trigger TP."""
        from semi_auto_trader import monitor_position_until_closed
        contract = ContractInfo(
            symbol="TRUMP_USDT",
            base_coin="TRUMP",
            quote_coin="USDT",
            contract_size=0.1,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=3,
            volume_precision=0,
            min_volume=1.0,
            max_volume=10000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.0067,
            initial_margin_ratio=0.0133,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0,
            depth_steps=["1"],
            raw_data={}
        )

        # Sequence of tickers:
        # Poll 1: lastPrice touched 2.381, but bid1 is 2.379 (spread!). Should NOT trigger TP!
        # Poll 2: bid1 rises to 2.382 (above TP 2.381 and above entry 2.380). Should trigger TP!
        ticker_1 = {"lastPrice": 2.381, "bid1": 2.379, "ask1": 2.381}
        ticker_2 = {"lastPrice": 2.382, "bid1": 2.382, "ask1": 2.383}

        with patch.object(self.market, "get_ticker", side_effect=[ticker_1, ticker_2]), \
             patch.object(self.market, "get_inr_rate", return_value=94.5), \
             patch("semi_auto_trader.check_manual_close_hotkey", return_value=False):

            exit_p, reason, _ = monitor_position_until_closed(
                trader=self.trader,
                market=self.market,
                symbol="TRUMP_USDT",
                position_id=None,
                direction=OrderDirection.LONG,
                vol_contracts=2,
                leverage=75,
                entry_price=2.380,
                exact_tp=2.381,
                exact_sl=2.374,
                contract=contract,
                is_live=False  # Dry-run
            )
            # Must exit at poll 2 price 2.382 (NOT poll 1 bid 2.379)
            self.assertEqual(exit_p, 2.382)
            self.assertEqual(reason, ExitReason.MIN_PROFIT_TP_HIT)

    def test_reconcile_loss_never_reports_tp_win(self):
        """Verifies that if realized PnL is negative, it is never classified as MIN_PROFIT_TP_HIT."""
        from semi_auto_trader import reconcile_exit_from_kcex

        # Order has externalOid with TAKE_PROFIT, but profit is negative (-0.0002) due to spread slippage
        mock_orders_loss = {
            "data": [
                {"side": 4, "dealVol": 2, "dealAvgPrice": 2.379, "profit": -0.0002, "externalOid": "stoporder_TAKE_PROFIT_999", "positionId": 12345}
            ]
        }
        with patch.object(self.client, "get_private", return_value=mock_orders_loss):
            exit_p, pnl, reason = reconcile_exit_from_kcex(
                trader=self.trader,
                symbol="TRUMP_USDT",
                position_id=12345,
                direction=OrderDirection.LONG,
                entry_price=2.380,
                fallback_price=2.379
            )
            self.assertEqual(reason, ExitReason.STOP_LOSS_HIT)
            self.assertEqual(pnl, -0.0002)
            self.assertEqual(exit_p, 2.379)


if __name__ == "__main__":
    unittest.main()
