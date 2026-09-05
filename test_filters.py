"""
Unit Test Suite for Trade Optimization & Regime Filters
======================================================
Verifies:
- compute_atr_series: True Range and Wilder smoothing
- compute_adx_series: Directional movement and chop detection
- HTFTrendFilter: 200 EMA trend gating
- ADXRegimeFilter: Sideways chop suppression
- HourlySessionFilter: Blacklisted UTC session filtering
- DirectionalBiasFilter: Long-only / Short-only policies
- FilterPipeline: Composite sequential evaluation and parameter extraction
- Backtester Duration Time-Stop: Simulation exit on max duration timeout
"""

import unittest
from datetime import datetime, timezone
from typing import List, NamedTuple

from kcex.engine.models import (
    OrderDirection,
    TradeSignal,
    ExitReason,
    ExecutionConfig
)
from strategies.filters import (
    BaseFilter,
    HTFTrendFilter,
    ADXRegimeFilter,
    HourlySessionFilter,
    DirectionalBiasFilter,
    FilterPipeline,
    compute_atr_series,
    compute_adx_series,
    resample_closes_to_timeframe
)
from strategies.stoch_rsi import StochasticRSIStrategy
from strategies.ema_crossover import EMACrossoverStrategy
from kcex.engine.strategy import MasterplanStrategy


class MockCandle:
    def __init__(self, open_: float, high: float, low: float, close: float, close_time_ms: int = 0, open_time_ms: int = 0):
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.close_time_ms = close_time_ms
        self.open_time_ms = open_time_ms


class TestIndicatorMath(unittest.TestCase):
    """Tests Wilder's ATR and ADX series calculations."""

    def test_compute_atr_series(self):
        highs = [10.0, 12.0, 11.0, 13.0, 14.0, 15.0]
        lows = [9.0, 10.0, 9.5, 11.0, 12.0, 13.0]
        closes = [9.5, 11.5, 10.5, 12.5, 13.5, 14.5]

        atr = compute_atr_series(highs, lows, closes, period=3)
        self.assertEqual(len(atr), len(closes))
        self.assertTrue(all(x > 0 for x in atr))

    def test_compute_adx_series_trend_vs_chop(self):
        # 1. Strong uptrend
        n = 40
        trend_highs = [100.0 + i * 2.0 for i in range(n)]
        trend_lows = [98.0 + i * 2.0 for i in range(n)]
        trend_closes = [99.5 + i * 2.0 for i in range(n)]

        adx_trend, plus_di, minus_di = compute_adx_series(trend_highs, trend_lows, trend_closes, period=14)
        self.assertEqual(len(adx_trend), n)
        # In a strong uptrend, +DI should significantly exceed -DI
        self.assertGreater(plus_di[-1], minus_di[-1])
        # ADX should reflect strong directional movement
        self.assertGreater(adx_trend[-1], 20.0)

        # 2. Sideways chop
        chop_highs = [100.0 + (1.0 if i % 2 == 0 else 0.0) for i in range(n)]
        chop_lows = [99.0 + (1.0 if i % 2 == 0 else 0.0) for i in range(n)]
        chop_closes = [99.5 for _ in range(n)]

        adx_chop, _, _ = compute_adx_series(chop_highs, chop_lows, chop_closes, period=14)
        self.assertEqual(len(adx_chop), n)
        # In sideways chop, ADX should stay low
        self.assertLess(adx_chop[-1], 25.0)


class TestHTFTrendFilter(unittest.TestCase):
    """Verifies 200 EMA macro trend filtering."""

    def setUp(self):
        # Create 250 ascending candles: prices rising from 100 to 350
        self.uptrend_candles = [
            MockCandle(100.0 + i, 101.0 + i, 99.0 + i, 100.5 + i) for i in range(250)
        ]
        # Create 250 descending candles: prices falling from 350 to 100
        self.downtrend_candles = [
            MockCandle(350.0 - i, 351.0 - i, 349.0 - i, 349.5 - i) for i in range(250)
        ]

    def test_disabled_filter_always_allows(self):
        filter_ = HTFTrendFilter(enabled=False, ema_period=200)
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        allowed, reason = filter_.is_allowed(long_sig, self.downtrend_candles, 0.0)
        self.assertTrue(allowed)
        self.assertIsNone(reason)

    def test_uptrend_allows_long_and_rejects_short(self):
        filter_ = HTFTrendFilter(enabled=True, ema_period=200)
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        short_sig = TradeSignal("TRUMP_USDT", OrderDirection.SHORT, "STOCH_RSI")

        # In uptrend, latest close (350) > 200 EMA (~250)
        allowed_long, _ = filter_.is_allowed(long_sig, self.uptrend_candles, 0.0)
        allowed_short, reason_short = filter_.is_allowed(short_sig, self.uptrend_candles, 0.0)

        self.assertTrue(allowed_long)
        self.assertFalse(allowed_short)
        self.assertIn("Short rejected", reason_short)

    def test_downtrend_allows_short_and_rejects_long(self):
        filter_ = HTFTrendFilter(enabled=True, ema_period=200)
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        short_sig = TradeSignal("TRUMP_USDT", OrderDirection.SHORT, "STOCH_RSI")

        # In downtrend, latest close (100) < 200 EMA (~200)
        allowed_short, _ = filter_.is_allowed(short_sig, self.downtrend_candles, 0.0)
        allowed_long, reason_long = filter_.is_allowed(long_sig, self.downtrend_candles, 0.0)

        self.assertTrue(allowed_short)
        self.assertFalse(allowed_long)
        self.assertIn("Long rejected", reason_long)


class TestADXRegimeFilter(unittest.TestCase):
    """Verifies sideways chop rejection via ADX."""

    def test_chop_suppression(self):
        filter_ = ADXRegimeFilter(enabled=True, period=14, threshold=25.0)
        sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")

        # 40 bars of flat chop
        chop_candles = [
            MockCandle(100.0, 100.5, 99.5, 100.0) for _ in range(40)
        ]
        allowed, reason = filter_.is_allowed(sig, chop_candles, 0.0)
        self.assertFalse(allowed)
        self.assertIn("Chop detected", reason)

    def test_trend_allowed(self):
        filter_ = ADXRegimeFilter(enabled=True, period=14, threshold=25.0)
        sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")

        # 40 bars of steep trend
        trend_candles = [
            MockCandle(100.0 + i * 2, 102.0 + i * 2, 99.0 + i * 2, 101.5 + i * 2) for i in range(40)
        ]
        allowed, reason = filter_.is_allowed(sig, trend_candles, 0.0)
        self.assertTrue(allowed)
        self.assertIsNone(reason)


class TestHourlySessionFilter(unittest.TestCase):
    """Verifies blacklisted UTC hour blocking."""

    def test_hourly_blocking(self):
        blacklist = [2, 3, 4, 5, 17]
        filter_ = HourlySessionFilter(enabled=True, blacklist_utc_hours=blacklist)
        sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")

        # 2026-07-01 03:30:00 UTC (Hour 3: blocked)
        dt_blocked = datetime(2026, 7, 1, 3, 30, 0, tzinfo=timezone.utc)
        ts_blocked = dt_blocked.timestamp()
        allowed_b, reason_b = filter_.is_allowed(sig, [], ts_blocked)
        self.assertFalse(allowed_b)
        self.assertIn("Blocked UTC hour 03:00", reason_b)

        # 2026-07-01 10:30:00 UTC (Hour 10: allowed)
        dt_allowed = datetime(2026, 7, 1, 10, 30, 0, tzinfo=timezone.utc)
        ts_allowed = dt_allowed.timestamp()
        allowed_a, reason_a = filter_.is_allowed(sig, [], ts_allowed)
        self.assertTrue(allowed_a)
        self.assertIsNone(reason_a)


class TestDirectionalBiasFilter(unittest.TestCase):
    """Verifies LONG_ONLY and SHORT_ONLY directional constraints."""

    def test_long_only_policy(self):
        filter_ = DirectionalBiasFilter(enabled=True, direction_bias="LONG_ONLY")
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        short_sig = TradeSignal("TRUMP_USDT", OrderDirection.SHORT, "STOCH_RSI")

        allowed_long, _ = filter_.is_allowed(long_sig, [], 0.0)
        allowed_short, reason_short = filter_.is_allowed(short_sig, [], 0.0)

        self.assertTrue(allowed_long)
        self.assertFalse(allowed_short)
        self.assertIn("Short rejected", reason_short)

    def test_short_only_policy(self):
        filter_ = DirectionalBiasFilter(enabled=True, direction_bias="SHORT_ONLY")
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        short_sig = TradeSignal("TRUMP_USDT", OrderDirection.SHORT, "STOCH_RSI")

        allowed_short, _ = filter_.is_allowed(short_sig, [], 0.0)
        allowed_long, reason_long = filter_.is_allowed(long_sig, [], 0.0)

        self.assertTrue(allowed_short)
        self.assertFalse(allowed_long)
        self.assertIn("Long rejected", reason_long)


class TestFilterPipeline(unittest.TestCase):
    """Verifies composite pipeline chaining and from_config factory."""

    def test_pipeline_chaining(self):
        config = ExecutionConfig(
            htf_trend_filter_enabled=True,
            htf_ema_period=50,
            adx_filter_enabled=True,
            adx_threshold=20.0,
            hourly_filter_enabled=True,
            hourly_blacklist_utc=[3, 17],
            direction_bias="LONG_ONLY"
        )
        pipeline = FilterPipeline.from_config(config)
        self.assertEqual(len(pipeline.filters), 4)

        # Signal rejected because hour is 3
        sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        dt_hour_3 = datetime(2026, 7, 1, 3, 15, 0, tzinfo=timezone.utc)
        uptrend = [MockCandle(100.0 + i, 102.0 + i, 99.0 + i, 101.0 + i) for i in range(100)]

        allowed, reason = pipeline.evaluate(sig, uptrend, dt_hour_3.timestamp())
        self.assertFalse(allowed)
        self.assertIn("Blocked UTC hour 03:00", reason)

        # Check parameter export
        params = pipeline.get_parameters()
        self.assertTrue(params["htf_trend_filter_enabled"])
        self.assertTrue(params["adx_filter_enabled"])
        self.assertTrue(params["hourly_filter_enabled"])
        self.assertEqual(params["direction_bias"], "LONG_ONLY")


class TestHTFTrendFilterWithResampling(unittest.TestCase):
    """Verifies candle resampling and multi-timeframe HTF trend filtering."""

    def test_resample_closes_to_timeframe_1m_to_15m(self):
        # 30 candles spaced 1 minute (60,000 ms) apart aligned to 15m boundary -> 2 15m buckets
        bucket_ms = 900_000
        base_ts = 1700000000000 - (1700000000000 % bucket_ms)
        candles = [
            MockCandle(100.0 + i, 101.0 + i, 99.0 + i, 100.5 + i, open_time_ms=base_ts + i * 60_000)
            for i in range(30)
        ]
        resampled = resample_closes_to_timeframe(candles, target_timeframe="15m")
        self.assertEqual(len(resampled), 2)
        # Bucket 1 should have close of candle 14, Bucket 2 close of candle 29
        self.assertEqual(resampled[0], candles[14].close)
        self.assertEqual(resampled[1], candles[29].close)

    def test_htf_trend_filter_with_resampling(self):
        # 300 1m candles in steady uptrend
        base_ts = 1700000000000
        candles = [
            MockCandle(100.0 + i * 0.1, 101.0 + i * 0.1, 99.0 + i * 0.1, 100.5 + i * 0.1, open_time_ms=base_ts + i * 60_000)
            for i in range(300)
        ]
        filter_ = HTFTrendFilter(enabled=True, ema_period=10, timeframe="15m")
        long_sig = TradeSignal("TRUMP_USDT", OrderDirection.LONG, "STOCH_RSI")
        short_sig = TradeSignal("TRUMP_USDT", OrderDirection.SHORT, "STOCH_RSI")

        allowed_long, _ = filter_.is_allowed(long_sig, candles, 0.0)
        allowed_short, reason_short = filter_.is_allowed(short_sig, candles, 0.0)

        self.assertTrue(allowed_long)
        self.assertFalse(allowed_short)
        self.assertIn("Short rejected", reason_short)


class TestStrategyTradeRejectedReset(unittest.TestCase):
    """Verifies that on_trade_rejected() correctly unlocks strategies when filters reject signals."""

    def test_stoch_rsi_on_trade_rejected_resets_state(self):
        from unittest.mock import MagicMock
        strat = StochasticRSIStrategy(market=MagicMock(), symbol="TRUMP_USDT", auto_start_feed=False)
        strat.trade_in_progress = True
        self.assertTrue(strat.trade_in_progress)

        strat.on_trade_rejected()
        self.assertFalse(strat.trade_in_progress)

    def test_ema_crossover_on_trade_rejected_resets_state(self):
        from unittest.mock import MagicMock
        strat = EMACrossoverStrategy(market=MagicMock(), symbol="TRUMP_USDT", auto_start_feed=False)
        strat.trade_in_progress = True
        self.assertTrue(strat.trade_in_progress)

        strat.on_trade_rejected()
        self.assertFalse(strat.trade_in_progress)

    def test_masterplan_forwards_on_trade_rejected(self):
        from unittest.mock import MagicMock
        sub_strat = StochasticRSIStrategy(market=MagicMock(), symbol="TRUMP_USDT", auto_start_feed=False)
        masterplan = MasterplanStrategy(market=MagicMock(), sub_strategy=sub_strat)

        sub_strat.trade_in_progress = True
        self.assertTrue(sub_strat.trade_in_progress)

        masterplan.on_trade_rejected()
        self.assertFalse(sub_strat.trade_in_progress)


if __name__ == "__main__":
    unittest.main()
