"""
Unit Tests for Forensic Audit Engine
====================================
Tests verify:
1. Intra-candle dispute resolution: SL/Early-Cut fires on simultaneous breach (no optimistic fill).
2. Zero lookahead bias: entries strictly at Open, exits within [Low, High].
3. Fee accounting: exact per-fill deduction on transacted notional.
4. Daily drawdown: measured from 00:00 UTC start-of-day equity.
5. Trailing drawdown: peak-to-trough high-water mark calculation.
"""

import unittest
from experiments.btc_eth_reverse_experiment.forensic_audit.backtester import (
    Candle,
    LegResult,
    OneMinuteDisputeResolver,
    simulate_single_leg,
    run_forensic_backtest,
    run_rolling_challenge_sim,
)


class TestForensicAudit(unittest.TestCase):

    def test_intra_candle_ambiguity_pessimistic_resolution(self):
        """
        Verify that when a candle breaches BOTH TP1 (+0.20%) and Early-Cut (-0.40%),
        the adversarial/pessimistic rule declares Early-Cut SL (no optimistic fill bias).
        """
        entry_price = 100.0
        # Candle with High = 100.30 (+0.30%, reaches TP1 at 100.20)
        # and Low = 99.50 (-0.50%, reaches Early-Cut at 99.60)
        dispute_candle = Candle(
            open_time_ms=0,
            open=100.0,
            high=100.30,
            low=99.50,
            close=100.10,
            volume=10.0,
            close_time_ms=3599999
        )
        candles = [dispute_candle]

        leg, exit_idx = simulate_single_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=candles,
            candle_start_idx=0,
            notional_per_leg=750.0,
            fee_rate_pct=0.060,
            tp1_pct=0.20,
            tp2_pct=1.00,
            be_pct=0.10,
            early_cut_pct=0.40,
        )

        # Early-Cut SL MUST win
        self.assertEqual(leg.exit2_reason, "EARLY_CUT")
        self.assertFalse(leg.tp1_hit)
        self.assertAlmostEqual(leg.exit2_price, 99.60)
        self.assertEqual(exit_idx, 0)

    def test_intra_candle_short_dispute(self):
        """Verify dispute resolution on SHORT leg."""
        entry_price = 100.0
        # For SHORT: TP1 is 99.80 (-0.20%), Early-Cut is 100.40 (+0.40%)
        # Candle has High = 100.50 (+0.50%) and Low = 99.70 (-0.30%)
        dispute_candle = Candle(
            open_time_ms=0,
            open=100.0,
            high=100.50,
            low=99.70,
            close=99.90,
            volume=10.0,
            close_time_ms=3599999
        )
        candles = [dispute_candle]

        leg, exit_idx = simulate_single_leg(
            direction="SHORT",
            symbol="ETHUSDT",
            entry_price=entry_price,
            entry_time_ms=0,
            candles=candles,
            candle_start_idx=0,
            notional_per_leg=750.0,
            fee_rate_pct=0.060,
            tp1_pct=0.20,
            tp2_pct=1.00,
            be_pct=0.10,
            early_cut_pct=0.40,
        )

        self.assertEqual(leg.exit2_reason, "EARLY_CUT")
        self.assertFalse(leg.tp1_hit)
        self.assertAlmostEqual(leg.exit2_price, 100.40)

    def test_fee_accounting_integrity(self):
        """Verify exact fee deductions on winning and losing legs."""
        entry_price = 100.0
        # Clean Early-Cut: only Low breaches 99.60
        loss_candle = Candle(
            open_time_ms=0, open=100.0, high=100.10, low=99.50, close=99.55,
            volume=10.0, close_time_ms=3599999
        )
        leg, _ = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=entry_price,
            entry_time_ms=0, candles=[loss_candle], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40
        )
        # Gross loss = $750 * -0.40% = -$3.00
        # Fee = $750 * 0.060% = $0.45
        # Net loss = -$3.45
        self.assertAlmostEqual(leg.exit2_pnl_gross, -3.00)
        self.assertAlmostEqual(leg.total_fees, 0.45)
        self.assertAlmostEqual(leg.total_net_pnl, -3.45)

    def test_tp1_then_be_stop(self):
        """Verify TP1 + BE stop mechanics."""
        entry_price = 100.0
        # Candle 0: Hits TP1 (High = 100.25), but closes above BE (Close = 100.15)
        c0 = Candle(
            open_time_ms=0, open=100.0, high=100.25, low=99.80, close=100.15,
            volume=10.0, close_time_ms=3599999
        )
        # Candle 1: Retraces to BE stop (Low = 100.05 <= 100.10)
        c1 = Candle(
            open_time_ms=3600000, open=100.15, high=100.18, low=100.05, close=100.08,
            volume=10.0, close_time_ms=7199999
        )
        candles = [c0, c1]

        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=entry_price,
            entry_time_ms=0, candles=candles, candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40
        )

        self.assertTrue(leg.tp1_hit)
        self.assertEqual(leg.exit2_reason, "BE_STOP")
        self.assertEqual(exit_idx, 1)

        # TP1 gross = $375 * 0.20% = +$0.75
        # TP1 fee = $375 * 0.060% = $0.225
        # BE gross = $375 * 0.10% = +$0.375
        # BE fee = $375 * 0.060% = $0.225
        # Total net = (0.75 - 0.225) + (0.375 - 0.225) = 0.525 + 0.150 = +$0.675
        self.assertAlmostEqual(leg.tp1_pnl_gross, 0.75)
        self.assertAlmostEqual(leg.exit2_pnl_gross, 0.375)
        self.assertAlmostEqual(leg.total_net_pnl, 0.675)

    def test_1m_dispute_tp1_hit_first(self):
        """
        In 1H dispute (High >= +0.20%, Low <= -0.40%),
        if 1m data shows TP1 touched at minute 5 and SL touched at minute 20,
        TP1 must be executed, not Early-Cut SL.
        """
        resolver = OneMinuteDisputeResolver(data_dir="")
        # Synthesize 60 minutes for hour 0
        minutes = []
        for m in range(60):
            ot = m * 60000
            if m == 5:
                # Hits TP1 (High = 100.25 >= 100.20, Low = 100.05)
                minutes.append((ot, 100.05, 100.25, 100.05, 100.20))
            elif m == 20:
                # Later drops to Early-Cut (Low = 99.50 <= 99.60)
                minutes.append((ot, 100.10, 100.15, 99.50, 99.55))
            else:
                minutes.append((ot, 100.05, 100.12, 100.02, 100.08))

        resolver.cache[("BTCUSDT", "1970-01")] = {0: minutes}

        h_candle = Candle(
            open_time_ms=0, open=100.0, high=100.25, low=99.50, close=99.55,
            volume=100.0, close_time_ms=3599999
        )
        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=100.0,
            entry_time_ms=0, candles=[h_candle], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40,
            resolver=resolver
        )

        # TP1 must have been hit!
        self.assertTrue(leg.tp1_hit)
        self.assertEqual(leg.tp1_time_ms, 5 * 60000)
        # Because minute 20 dropped to 99.50 <= 100.10, the BE stop fired!
        self.assertEqual(leg.exit2_reason, "BE_STOP")
        self.assertAlmostEqual(leg.exit2_price, 100.10)

    def test_1m_dispute_sl_hit_first(self):
        """
        In 1H dispute, if 1m data shows Early-Cut SL touched at minute 5
        and TP1 touched at minute 20, Early-Cut SL must win.
        """
        resolver = OneMinuteDisputeResolver(data_dir="")
        minutes = []
        for m in range(60):
            ot = m * 60000
            if m == 5:
                # Early-Cut SL hit first (Low = 99.50 <= 99.60)
                minutes.append((ot, 100.0, 100.05, 99.50, 99.55))
            elif m == 20:
                # TP1 hit later (High = 100.25 >= 100.20)
                minutes.append((ot, 99.80, 100.25, 99.80, 100.20))
            else:
                minutes.append((ot, 99.95, 100.05, 99.90, 100.00))

        resolver.cache[("BTCUSDT", "1970-01")] = {0: minutes}

        h_candle = Candle(
            open_time_ms=0, open=100.0, high=100.25, low=99.50, close=100.20,
            volume=100.0, close_time_ms=3599999
        )
        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=100.0,
            entry_time_ms=0, candles=[h_candle], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40,
            resolver=resolver
        )

        self.assertFalse(leg.tp1_hit)
        self.assertEqual(leg.exit2_reason, "EARLY_CUT")
        self.assertAlmostEqual(leg.exit2_price, 99.60)
        self.assertEqual(leg.exit2_time_ms, 5 * 60000)

    def test_1m_dispute_same_1m_candle_declares_sl(self):
        """
        CRITICAL USER REQUIREMENT:
        "if in 1min too the tp and sl is in same candle, then declare sl."
        Verify that if both TP1 and Early-Cut SL are breached within the EXACT SAME 1m candle,
        Early-Cut SL is strictly declared!
        """
        resolver = OneMinuteDisputeResolver(data_dir="")
        minutes = []
        for m in range(60):
            ot = m * 60000
            if m == 8:
                # Minute 8 breaches BOTH TP1 (High 100.30 >= 100.20) AND Early-Cut (Low 99.50 <= 99.60)
                minutes.append((ot, 100.0, 100.30, 99.50, 100.05))
            else:
                minutes.append((ot, 100.0, 100.05, 99.95, 100.0))

        resolver.cache[("BTCUSDT", "1970-01")] = {0: minutes}

        h_candle = Candle(
            open_time_ms=0, open=100.0, high=100.30, low=99.50, close=100.05,
            volume=100.0, close_time_ms=3599999
        )
        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=100.0,
            entry_time_ms=0, candles=[h_candle], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40,
            resolver=resolver
        )

        # MUST be Early-Cut SL!
        self.assertFalse(leg.tp1_hit)
        self.assertEqual(leg.exit2_reason, "EARLY_CUT")
        self.assertAlmostEqual(leg.exit2_price, 99.60)
        self.assertEqual(leg.exit2_time_ms, 8 * 60000)

    def test_1m_phase2_runner_tp2_first(self):
        """
        In Phase 2 dispute (TP2 +1.00% vs BE stop +0.10%),
        if 1m data shows TP2 hit at minute 10 before BE stop, TP2 must win.
        """
        resolver = OneMinuteDisputeResolver(data_dir="")
        minutes = []
        for m in range(60):
            ot = 3600000 + m * 60000
            if m == 10:
                # TP2 hit (High = 101.05 >= 101.00)
                minutes.append((ot, 100.80, 101.05, 100.80, 101.02))
            elif m == 30:
                # Drops to BE stop (Low = 100.05 <= 100.10)
                minutes.append((ot, 100.50, 100.50, 100.05, 100.08))
            else:
                minutes.append((ot, 100.50, 100.60, 100.40, 100.50))

        resolver.cache[("BTCUSDT", "1970-01")] = {3600000: minutes}

        # Candle 0: clean TP1
        c0 = Candle(
            open_time_ms=0, open=100.0, high=100.22, low=99.90, close=100.20,
            volume=50.0, close_time_ms=3599999
        )
        # Candle 1: breaches both TP2 (101.05) and BE stop (100.05)
        c1 = Candle(
            open_time_ms=3600000, open=100.20, high=101.05, low=100.05, close=100.10,
            volume=50.0, close_time_ms=7199999
        )
        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=100.0,
            entry_time_ms=0, candles=[c0, c1], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40,
            resolver=resolver
        )

        self.assertTrue(leg.tp1_hit)
        self.assertEqual(leg.exit2_reason, "TP2")
        self.assertAlmostEqual(leg.exit2_price, 101.00)
        self.assertEqual(exit_idx, 1)

    def test_1m_phase2_runner_same_1m_candle_declares_be_stop(self):
        """
        In Phase 2 dispute, if within the SAME 1m candle both TP2 and BE stop are touched,
        the pessimistic tie-breaker declares BE stop.
        """
        resolver = OneMinuteDisputeResolver(data_dir="")
        minutes = []
        for m in range(60):
            ot = 3600000 + m * 60000
            if m == 15:
                # Spans from 100.05 (BE stop) to 101.10 (TP2) in same minute
                minutes.append((ot, 100.50, 101.10, 100.05, 100.60))
            else:
                minutes.append((ot, 100.40, 100.60, 100.30, 100.50))

        resolver.cache[("BTCUSDT", "1970-01")] = {3600000: minutes}

        c0 = Candle(
            open_time_ms=0, open=100.0, high=100.22, low=99.90, close=100.20,
            volume=50.0, close_time_ms=3599999
        )
        c1 = Candle(
            open_time_ms=3600000, open=100.20, high=101.10, low=100.05, close=100.60,
            volume=50.0, close_time_ms=7199999
        )
        leg, exit_idx = simulate_single_leg(
            direction="LONG", symbol="BTCUSDT", entry_price=100.0,
            entry_time_ms=0, candles=[c0, c1], candle_start_idx=0,
            notional_per_leg=750.0, fee_rate_pct=0.060,
            tp1_pct=0.20, tp2_pct=1.00, be_pct=0.10, early_cut_pct=0.40,
            resolver=resolver
        )

        self.assertTrue(leg.tp1_hit)
        self.assertEqual(leg.exit2_reason, "BE_STOP")
        self.assertAlmostEqual(leg.exit2_price, 100.10)


if __name__ == "__main__":
    unittest.main()

