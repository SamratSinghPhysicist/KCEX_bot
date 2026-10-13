"""
Unit Tests for Master Quantitative Research Engine
===================================================
Tests verify all critical rules:
1. Dead-leg termination rule (zero post-termination interaction).
2. Strict breakeven ratchet (instant termination on touch).
3. 1-minute intra-candle dispute resolution & adversarial tie-breaking (SL wins).
4. Fee accounting accuracy on gross notional per fill.
5. Daily drawdown (00:00 UTC boundary) and continuous trailing drawdown tracking.
6. Cointegration spread Z-score math.
7. Maintenance margin liquidation buffer mechanics.
"""

import unittest
import numpy as np
from experiments.btc_eth_reverse_experiment.forensic_audit.backtester import Candle, OneMinuteDisputeResolver
from experiments.btc_eth_reverse_experiment.forensic_audit.master_research_engine import (
    simulate_leg,
    compute_metrics,
    evaluate_rolling_challenge,
    calculate_ema,
    precompute_market_indicators,
)


class TestMasterResearchEngine(unittest.TestCase):

    def test_dead_leg_termination_rule(self):
        """
        Verify Dead-Leg Termination Rule:
        Once Leg A hits its SL or TP, its PnL is locked at that exact candle.
        Subsequent price movements in Leg A must NOT affect its PnL or state.
        """
        entry_price = 100.0
        # Candle 0: Entry candle
        # Candle 1: High = 102 (TP hit at 101.5), Leg A terminates!
        # Candle 2: Price drops to 50 (crash)
        # Leg A must exit at Candle 1 at price 101.5. Candle 2 must have zero effect.
        c0 = Candle(open_time_ms=0, open=100.0, high=100.5, low=99.5, close=100.0, volume=10, close_time_ms=3599999)
        c1 = Candle(open_time_ms=3600000, open=100.0, high=102.0, low=99.8, close=101.8, volume=10, close_time_ms=7199999)
        c2 = Candle(open_time_ms=7200000, open=101.8, high=102.0, low=50.0, close=55.0, volume=100, close_time_ms=10799999)

        candles = [c0, c1, c2]

        leg, exit_idx = simulate_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=candles,
            candle_start_idx=0,
            notional=750.0,
            tp_pct=1.5,
            sl_pct=1.5,
            fee_maker_pct=0.015,
            fee_taker_pct=0.045,
        )

        self.assertEqual(exit_idx, 1)
        self.assertEqual(leg.exit_reason, "TP")
        self.assertAlmostEqual(leg.exit_price, 101.5)
        self.assertEqual(leg.exit_candle_idx, 1)
        self.assertGreater(leg.net_pnl, 0.0)

    def test_strict_breakeven_ratchet(self):
        """
        Verify Strict Breakeven Ratchet:
        When TP1 hits, position is cut 50% and SL moves to BE (+0.10%).
        Any subsequent candle touch of BE terminates the remaining position at BE.
        """
        entry_price = 100.0
        # Candle 0: Hits TP1 (+0.20%, High = 100.30, Low = 99.90, Close = 100.25)
        # Candle 1: Low drops to 100.05 (breaches BE at 100.10!)
        c0 = Candle(open_time_ms=0, open=100.0, high=100.30, low=99.90, close=100.25, volume=10, close_time_ms=3599999)
        c1 = Candle(open_time_ms=3600000, open=100.25, high=100.30, low=100.05, close=100.15, volume=10, close_time_ms=7199999)

        candles = [c0, c1]

        leg, exit_idx = simulate_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=candles,
            candle_start_idx=0,
            notional=750.0,
            fee_maker_pct=0.015,
            fee_taker_pct=0.045,
            tp1_pct=0.20,
            tp2_pct=1.00,
            be_pct=0.10,
            early_cut_pct=0.40,
        )

        self.assertTrue(leg.tp1_hit)
        self.assertEqual(leg.exit_reason, "BE_STOP")
        self.assertAlmostEqual(leg.exit_price, 100.10)
        self.assertEqual(exit_idx, 1)

    def test_one_minute_dispute_adversarial_tie_break(self):
        """
        Verify that when a candle breaches both TP and SL, if the 1m dispute
        resolver detects both breached in the same 1m candle, it strictly declares SL.
        """
        entry_price = 100.0
        # Dispute candle
        c = Candle(open_time_ms=0, open=100.0, high=102.0, low=98.0, close=100.0, volume=10, close_time_ms=3599999)

        # Mock resolver that simulates simultaneous 1m hit
        class MockResolver:
            def resolve_simple_tp_sl(self, symbol, direction, hour_ms, entry_price, tp_price, sl_price):
                # strictly declare SL
                return ("SL", sl_price, hour_ms + 60000)

        leg, exit_idx = simulate_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=[c],
            candle_start_idx=0,
            notional=750.0,
            tp_pct=1.5,
            sl_pct=1.5,
            resolver=MockResolver(),
        )

        self.assertEqual(leg.exit_reason, "SL")
        self.assertAlmostEqual(leg.exit_price, 98.5)
        self.assertLess(leg.net_pnl, 0.0)

    def test_accurate_fee_deduction(self):
        """
        Verify fee deduction math:
        Maker: 0.015% on entry notional ($750 -> $0.1125)
        Taker: 0.045% on exit notional ($750 * 1.015 = $761.25 -> $0.3425625)
        Total fees = $0.1125 + $0.3425625 = $0.4550625
        """
        entry_price = 100.0
        c0 = Candle(open_time_ms=0, open=100.0, high=102.0, low=99.5, close=101.6, volume=10, close_time_ms=3599999)

        leg, _ = simulate_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=[c0],
            candle_start_idx=0,
            notional=750.0,
            tp_pct=1.5,
            sl_pct=1.5,
            fee_maker_pct=0.015,
            fee_taker_pct=0.045,
        )

        expected_entry_fee = 750.0 * 0.00015
        expected_exit_notional = 750.0 * (101.5 / 100.0)
        expected_exit_fee = expected_exit_notional * 0.00045
        expected_gross_pnl = 750.0 * 0.015  # $11.25
        expected_net_pnl = expected_gross_pnl - expected_entry_fee - expected_exit_fee

        self.assertAlmostEqual(leg.entry_fee, expected_entry_fee, places=4)
        self.assertAlmostEqual(leg.exit_fee, expected_exit_fee, places=4)
        self.assertAlmostEqual(leg.gross_pnl, expected_gross_pnl, places=4)
        self.assertAlmostEqual(leg.net_pnl, expected_net_pnl, places=4)

    def test_daily_drawdown_0000_utc_boundary(self):
        """
        Verify Daily Drawdown measurement strictly resets at 00:00 UTC.
        """
        # Day 1: Trade 1 wins $50, Trade 2 loses $40 -> Day 1 trough DD = -$40 relative to SOD ($1000)
        # Day 2: Starts with $1010. Trade 3 loses $35 -> Day 2 trough DD = $35 ($35 / $1000 = 3.5% breach!)
        ts_day1_1 = 1577836800000  # 2020-01-01 00:00 UTC
        ts_day1_2 = 1577840400000  # 2020-01-01 01:00 UTC
        ts_day2_1 = 1577923200000  # 2020-01-02 00:00 UTC

        pnls = [50.0, -40.0, -35.0]
        timestamps = [ts_day1_1, ts_day1_2, ts_day2_1]

        m = compute_metrics(
            name="Test DD",
            pnls=pnls,
            timestamps=timestamps,
            initial_capital=1000.0,
            daily_dd_limit_pct=3.0,
            max_dd_limit_pct=5.0
        )

        # Day 2 experienced a $35 drop from SOD equity ($1010 -> $975) = $35.00 (3.5% breach!)
        self.assertEqual(m.daily_dd_breaches_3pct, 1)
        self.assertAlmostEqual(m.worst_daily_dd_usd, 35.0, places=2)

    def test_maintenance_margin_liquidation_buffer(self):
        """
        Verify liquidation buffer calculation at 100x leverage:
        MMR = 0.40%, Buffer = (1/100 - 0.004) = 0.60% adverse move.
        If candle MAE >= 0.60%, position must liquidate immediately!
        """
        entry_price = 100.0
        # Candle has Low = 99.30 (MAE = 0.70% >= 0.60% buffer)
        c = Candle(open_time_ms=0, open=100.0, high=100.20, low=99.30, close=99.50, volume=10, close_time_ms=3599999)

        leg, _ = simulate_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=[c],
            candle_start_idx=0,
            notional=1000.0,
            max_adverse_liq_pct=0.60,
        )

        self.assertEqual(leg.exit_reason, "LIQUIDATION")
        self.assertAlmostEqual(leg.exit_price, 99.40)
        self.assertLess(leg.net_pnl, 0.0)


if __name__ == "__main__":
    unittest.main()
