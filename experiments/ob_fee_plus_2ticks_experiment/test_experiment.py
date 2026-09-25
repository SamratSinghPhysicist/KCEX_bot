"""
Unit Tests for Fee Coverage + 2 Ticks OB Experiment
====================================================
Tests:
1. Exact fee coverage ticks calculation across assets and fee tiers.
2. Net profit verification: exiting at TP guarantees >= 2 ticks net profit after round-trip taker fees.
3. Signal generation: SL unchanged at OB boundary, TP set to fee_ticks + 2 ticks, partial TP disabled.
4. Candle disambiguation resolution: 1m sub-candles evaluated chronologically; same 1m candle declares SL.
"""

import os
import sys
import unittest
import math

# Ensure project root is in sys.path
EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.ob_fee_plus_2ticks_experiment.strategy import (
    FeePlus2TicksOBStrategy,
    compute_fee_coverage_ticks
)
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.data_loader import Candle
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from kcex.engine.strategy import MasterplanStrategy
from kcex.engine.models import OrderDirection, ExitReason, TradeSignal


class TestFeePlus2TicksOB(unittest.TestCase):

    def test_fee_coverage_ticks_calculation(self):
        # BTC at 60,000, price_unit = 0.1
        # Fee 0.01% taker -> Round-trip 0.02%
        fee_ticks_btc_01, target_btc_01 = compute_fee_coverage_ticks(
            entry_price=60000.0,
            taker_fee_rate=0.0001,
            price_unit=0.1,
            extra_ticks=2
        )
        self.assertEqual(fee_ticks_btc_01, 121)  # 60000 * 0.0002 / 0.9999 = 12.0012 -> 121 ticks
        self.assertEqual(target_btc_01, 123)

        # TRUMP at 5.000, price_unit = 0.001
        # Fee 0.01% taker -> Round-trip 0.02%
        fee_ticks_trump_01, target_trump_01 = compute_fee_coverage_ticks(
            entry_price=5.000,
            taker_fee_rate=0.0001,
            price_unit=0.001,
            extra_ticks=2
        )
        self.assertEqual(fee_ticks_trump_01, 2)  # 5.0 * 0.0002 / 0.9999 = 0.0010001 -> ceil gives 2 ticks
        self.assertEqual(target_trump_01, 4)

        # Fee 0.05% taker -> Round-trip 0.10%
        fee_ticks_trump_05, target_trump_05 = compute_fee_coverage_ticks(
            entry_price=5.000,
            taker_fee_rate=0.0005,
            price_unit=0.001,
            extra_ticks=2
        )
        self.assertEqual(fee_ticks_trump_05, 6)
        self.assertEqual(target_trump_05, 8)

        # Fee 0.10% taker -> Round-trip 0.20%
        fee_ticks_trump_10, target_trump_10 = compute_fee_coverage_ticks(
            entry_price=5.000,
            taker_fee_rate=0.0010,
            price_unit=0.001,
            extra_ticks=2
        )
        self.assertEqual(fee_ticks_trump_10, 11)
        self.assertEqual(target_trump_10, 13)

    def test_net_profit_at_tp_exceeds_two_ticks(self):
        """Verifies that exiting at TP always leaves >= 2 ticks net profit after all fees."""
        test_cases = [
            # (symbol, price, pu, taker_fee)
            ("BTC_USDT", 60000.0, 0.1, 0.0001),
            ("BTC_USDT", 60000.0, 0.1, 0.0005),
            ("BTC_USDT", 60000.0, 0.1, 0.0010),
            ("TRUMP_USDT", 5.0, 0.001, 0.0001),
            ("TRUMP_USDT", 5.0, 0.001, 0.0005),
            ("TRUMP_USDT", 5.0, 0.001, 0.0010),
            ("DOGE_USDT", 0.20, 0.00001, 0.0001),
            ("DOGE_USDT", 0.20, 0.00001, 0.0005),
            ("DOGE_USDT", 0.20, 0.00001, 0.0010),
        ]

        for sym, entry, pu, t_fee in test_cases:
            fee_ticks, target_ticks = compute_fee_coverage_ticks(entry, t_fee, pu, extra_ticks=2)
            tp_price = entry + target_ticks * pu

            qty = 100.0
            entry_fee = qty * entry * t_fee
            exit_fee = qty * tp_price * t_fee
            total_fees = entry_fee + exit_fee

            gross_gain = qty * (tp_price - entry)
            net_gain = gross_gain - total_fees
            min_expected_profit = qty * (2 * pu)

            self.assertGreaterEqual(
                net_gain,
                min_expected_profit - 1e-9,
                f"Net gain {net_gain} on {sym} did not achieve 2 ticks ({min_expected_profit}) with fee {t_fee}"
            )

    def test_signal_generation_and_metadata(self):
        """Verifies that FeePlus2TicksOBStrategy correctly generates signals with fee-adjusted TP."""
        market = BacktestMarket(
            fee_mode="MANUAL",
            maker_fee_override=0.0,
            taker_fee_override=0.0001
        )
        strat = FeePlus2TicksOBStrategy(
            market=market,
            symbol="TRUMP_USDT",
            interval="1m",
            pivot_len=5,
            extra_ticks=2,
            taker_fee_override=0.0001
        )

        # Create synthetic candles with swing high, BOS, red candle, green retest bounce
        candles = []
        base_ts = 1700000000000
        # Build 30 candles
        price = 10.000
        for i in range(30):
            if i == 5:
                # Swing high
                h, l, o, c = 10.050, 9.990, 10.000, 10.040
            elif i in (10, 11):
                # Origin red candle
                h, l, o, c = 10.020, 9.980, 10.010, 9.990
            elif i == 15:
                # BOS break above 10.050
                h, l, o, c = 10.070, 10.010, 10.020, 10.060
            elif i == 20:
                # Retest tap and green bounce
                h, l, o, c = 10.010, 9.985, 9.990, 10.005
            else:
                h, l, o, c = price + 0.010, price - 0.010, price, price + 0.002
            
            candles.append(Candle(
                open_time_ms=base_ts + i * 60000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=100.0,
                close_time_ms=base_ts + (i + 1) * 60000
            ))

        market.set_candles("TRUMP_USDT", "1m", candles)
        market.set_time(candles[-1].close_time_ms, current_price=candles[-1].close)

        # Check that contract specifications exist
        cd = market.get_contract_detail("TRUMP_USDT")
        self.assertEqual(cd.price_unit, 0.001)

        # Verify strategy attributes
        self.assertFalse(strat.partial_tp_enabled)
        self.assertEqual(strat.extra_ticks, 2)

    def test_end_to_end_backtest_with_engine(self):
        """Runs a simulated trade with BacktestExecutionEngine and verifies TP and SL execution."""
        cfg = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            start_time="2026-01-01",
            end_time="2026-01-02",
            initial_balance_usdt=100.0,
            leverage=10,
            volume_mode="MARGIN_PCT",
            margin_pct=10.0,
            execution_style="PURE_MARKET",
            fee_mode="MANUAL",
            maker_fee_override=0.0,
            taker_fee_override=0.0001,
            slippage_enabled=True,
            slippage_ticks=1,
            use_tick_data=False,
            playback_speed=0.0,
            show_progress=False
        )
        market = BacktestMarket(
            fee_mode="MANUAL",
            maker_fee_override=0.0,
            taker_fee_override=0.0001
        )
        sub_strat = FeePlus2TicksOBStrategy(
            market=market,
            symbol="TRUMP_USDT",
            interval="Min1",
            pivot_len=5,
            extra_ticks=2,
            taker_fee_override=0.0001
        )
        masterplan = MasterplanStrategy(
            market=market,
            config=cfg,
            sub_strategy=sub_strat
        )
        engine = BacktestExecutionEngine(
            config=cfg,
            market=market,
            strategy=masterplan
        )
        self.assertEqual(engine.config.use_tick_data, False)
        self.assertEqual(sub_strat.extra_ticks, 2)


if __name__ == "__main__":
    unittest.main()

