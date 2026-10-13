"""
Unit Tests for Dual-Account Reverse Trading Experiment
======================================================
Tests verify:
1. TP and SL price calculation for Long and Short.
2. 1-minute candle dispute resolution (declares SL on simultaneous hit).
3. Sub-candle 1m chronological lookup for higher timeframe disputes.
4. Two-account synchronization (only re-enter when both accounts are free).
5. 2x leverage compounding math.
6. Streak distributions and +10% / -3% milestone detection.
"""

import unittest
from experiments.btc_eth_reverse_experiment.engine import (
    CandleData,
    TP_SL_Config,
    evaluate_candle_tp_sl,
    compute_account_metrics,
    run_dual_account_simulation,
    SingleTrade
)


class TestDualAccountExperiment(unittest.TestCase):

    def test_tp_sl_breach_long(self):
        # Entry 100, TP 3% (103), SL 3% (97)
        c_tp = CandleData(open_time_ms=0, open=100, high=104, low=99, close=102, volume=10, close_time_ms=59999)
        res, px = evaluate_candle_tp_sl("LONG", 100, 103, 97, c_tp, timeframe="1m")
        self.assertEqual(res, "TP")
        self.assertEqual(px, 103)

        c_sl = CandleData(open_time_ms=0, open=100, high=101, low=96, close=98, volume=10, close_time_ms=59999)
        res, px = evaluate_candle_tp_sl("LONG", 100, 103, 97, c_sl, timeframe="1m")
        self.assertEqual(res, "SL")
        self.assertEqual(px, 97)

    def test_tp_sl_breach_short(self):
        # Entry 100, TP 3% (97), SL 3% (103)
        c_tp = CandleData(open_time_ms=0, open=100, high=101, low=96, close=97, volume=10, close_time_ms=59999)
        res, px = evaluate_candle_tp_sl("SHORT", 100, 97, 103, c_tp, timeframe="1m")
        self.assertEqual(res, "TP")
        self.assertEqual(px, 97)

        c_sl = CandleData(open_time_ms=0, open=100, high=104, low=99, close=102, volume=10, close_time_ms=59999)
        res, px = evaluate_candle_tp_sl("SHORT", 100, 97, 103, c_sl, timeframe="1m")
        self.assertEqual(res, "SL")
        self.assertEqual(px, 103)

    def test_dispute_1m_candle_declares_sl(self):
        # In 1m candle, both high >= 103 and low <= 97 hit
        # Per requirement: "if both tp and sl at candle happens in 1min too, then declare sl"
        c_dispute = CandleData(open_time_ms=0, open=100, high=105, low=95, close=100, volume=10, close_time_ms=59999)
        res, px = evaluate_candle_tp_sl("LONG", 100, 103, 97, c_dispute, timeframe="1m")
        self.assertEqual(res, "SL")
        self.assertEqual(px, 97)

        res_s, px_s = evaluate_candle_tp_sl("SHORT", 100, 97, 103, c_dispute, timeframe="1m")
        self.assertEqual(res_s, "SL")
        self.assertEqual(px_s, 103)

    def test_dispute_sub_1m_resolution(self):
        # 5m candle breaches both TP (103) and SL (97)
        c_5m = CandleData(open_time_ms=0, open=100, high=105, low=95, close=100, volume=10, close_time_ms=299999)
        # Sub-candles: minute 0 is neutral, minute 1 hits TP only (high 104, low 99)
        sc0 = CandleData(open_time_ms=0, open=100, high=101, low=99, close=100, volume=2, close_time_ms=59999)
        sc1 = CandleData(open_time_ms=60000, open=100, high=104, low=99, close=103, volume=2, close_time_ms=119999)
        sc2 = CandleData(open_time_ms=120000, open=103, high=103, low=95, close=96, volume=2, close_time_ms=179999)

        sub_map = {0: [sc0, sc1, sc2]}
        res, px = evaluate_candle_tp_sl("LONG", 100, 103, 97, c_5m, sub_1m_map=sub_map, timeframe="5m")
        # Minute 1 hit TP first chronologically!
        self.assertEqual(res, "TP")
        self.assertEqual(px, 103)

    def test_synchronization_rule(self):
        # BTC exits on candle 1, ETH exits on candle 3.
        # Next trade MUST enter at candle 4!
        # BTC candles:
        # Candle 0: Open 100 (Entry)
        # Candle 1: High 104 -> TP hit! BTC free.
        # Candle 2: Holding cash
        # Candle 3: Holding cash
        # Candle 4: Next Entry!
        btc_candles = [
            CandleData(0, 100, 101, 99, 100, 1, 59999),
            CandleData(60000, 100, 105, 99, 104, 1, 119999), # TP hits for BTC
            CandleData(120000, 104, 104, 103, 103, 1, 179999),
            CandleData(180000, 103, 104, 102, 103, 1, 239999),
            CandleData(240000, 103, 104, 102, 103, 1, 299999), # Cycle 2 entry
            CandleData(300000, 103, 108, 102, 107, 1, 359999), # TP hits for BTC
        ]
        # ETH candles (Short): Entry 100, TP 97, SL 103
        # Candle 0: Entry 100
        # Candle 1: 100 -> still open
        # Candle 2: 100 -> still open
        # Candle 3: High 105 -> SL hits! ETH free.
        # Candle 4: Next Entry!
        eth_candles = [
            CandleData(0, 100, 101, 99, 100, 1, 59999),
            CandleData(60000, 100, 101, 99, 100, 1, 119999),
            CandleData(120000, 100, 101, 99, 100, 1, 179999),
            CandleData(180000, 100, 105, 99, 104, 1, 239999), # SL hits for ETH
            CandleData(240000, 104, 104, 103, 103, 1, 299999), # Cycle 2 entry
            CandleData(300000, 103, 103, 95, 96, 1, 359999),  # TP hits for ETH
        ]

        cfg = TP_SL_Config("TP3.0_SL3.0", 3.0, 3.0, "TP 3.0% / SL 3.0%")
        cycles, perf_a, perf_b = run_dual_account_simulation(
            btc_candles, eth_candles, None, None,
            case_name="Case 1", timeframe="1m", config=cfg, fee_rate=0.0
        )

        self.assertEqual(len(cycles), 2)
        # Cycle 1 entered at 0 ms, BTC exited at 60000 ms, ETH exited at 180000 ms.
        # Both became free at 180000 ms.
        self.assertEqual(cycles[0].cycle_exit_time_ms, 180000)
        # Cycle 2 entered at 240000 ms (candle 4)!
        self.assertEqual(cycles[1].entry_time_ms, 240000)

    def test_milestone_and_streaks(self):
        trades = [
            SingleTrade(
                trade_id=1, cycle_id=1, account="A", symbol="BTC", case="C1", direction="LONG",
                config_name="cfg", tp_pct=3.0, sl_pct=3.0, entry_time_ms=0, entry_time_iso="2025-01-01",
                entry_price=100, exit_time_ms=60000, exit_time_iso="2025-01-01 00:01:00", exit_price=103,
                exit_reason="TP", duration_candles=1, duration_seconds=60, initial_trade_capital=1000,
                notional_value=2000, quantity=20, gross_pnl=60, fees=0, net_pnl=60, pnl_pct=6.0,
                balance_after=1060, is_win=True
            ),
            SingleTrade(
                trade_id=2, cycle_id=2, account="A", symbol="BTC", case="C1", direction="LONG",
                config_name="cfg", tp_pct=3.0, sl_pct=3.0, entry_time_ms=120000, entry_time_iso="2025-01-01",
                entry_price=100, exit_time_ms=180000, exit_time_iso="2025-01-01 00:03:00", exit_price=103,
                exit_reason="TP", duration_candles=1, duration_seconds=60, initial_trade_capital=1060,
                notional_value=2120, quantity=21.2, gross_pnl=63.6, fees=0, net_pnl=63.6, pnl_pct=6.0,
                balance_after=1123.6, is_win=True
            ),
            SingleTrade(
                trade_id=3, cycle_id=3, account="A", symbol="BTC", case="C1", direction="LONG",
                config_name="cfg", tp_pct=3.0, sl_pct=3.0, entry_time_ms=240000, entry_time_iso="2025-01-01",
                entry_price=100, exit_time_ms=300000, exit_time_iso="2025-01-01 00:05:00", exit_price=97,
                exit_reason="SL", duration_candles=1, duration_seconds=60, initial_trade_capital=1123.6,
                notional_value=2247.2, quantity=22.472, gross_pnl=-67.4, fees=0, net_pnl=-67.4, pnl_pct=-6.0,
                balance_after=1056.2, is_win=False
            )
        ]

        cfg = TP_SL_Config("TP3.0_SL3.0", 3.0, 3.0, "TP 3.0% / SL 3.0%")
        perf = compute_account_metrics(trades, "A", "BTC", "Case 1", "1m", cfg, initial_balance=1000.0)

        # Reached +10% ($1100) on Trade 2 (balance 1123.6)
        self.assertEqual(perf.trades_to_reach_plus_10_pct, 2)
        # Never reached -3% ($970)
        self.assertIsNone(perf.trades_to_reach_minus_3_pct)
        # Streaks
        self.assertEqual(perf.max_win_streak, 2)
        self.assertEqual(perf.max_loss_streak, 1)
        self.assertEqual(perf.win_streak_distribution, {2: 1})
        self.assertEqual(perf.loss_streak_distribution, {1: 1})


if __name__ == "__main__":
    unittest.main()
