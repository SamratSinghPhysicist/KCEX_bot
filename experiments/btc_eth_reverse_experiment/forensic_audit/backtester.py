"""
INDEPENDENT GROUND-TRUTH BACKTESTER (Built From Scratch)
=========================================================
Forensic-grade simulation of the BTC/ETH hedged pairs strategy
with exact prop firm constraints.

Strategy (Locked Production Parameters):
- SINGLE unified account: $1,000 USDC
- Per cycle: Long BTC $750 + Short ETH $750 = $1,500 total notional (1.50x)
- Margin required: $750 at 2x leverage (leaves $250 unencumbered cash)
- TP1: +0.20% -> close 50% ($375 each leg)
- BE Lock: Instantly move SL to +0.10% after TP1
- TP2: +1.00% -> close remaining 50% ($375 each leg)
- Early-Cut SL: -0.40% before TP1 -> close 100% of that leg immediately
- Fees: Limit entry (0.015%) + Market exit (0.045%) = 0.060% round-trip
         OR Market+Market = 0.090% round-trip (stress test)

Forensic Principles:
1. NO lookahead bias - entries at candle Open, exits constrained to H/L range
2. Conservative intra-candle dispute: if TP and SL hit same candle, SL wins
3. Daily drawdown measured from 00:00 UTC equity to intraday trough
4. Trailing max drawdown from peak equity to current trough
5. All fee calculations explicit and auditable per-fill
"""

from __future__ import annotations
import os
import csv
import glob
import datetime
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, OrderedDict


# ─────────────────────────────────────────────────────────────
# Data Structures
# ─────────────────────────────────────────────────────────────

@dataclass
class Candle:
    """Single OHLCV candle."""
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time_ms: int

    @property
    def open_time_utc(self) -> str:
        dt = datetime.datetime.fromtimestamp(
            self.open_time_ms / 1000.0, tz=datetime.timezone.utc
        )
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def date_utc(self) -> str:
        dt = datetime.datetime.fromtimestamp(
            self.open_time_ms / 1000.0, tz=datetime.timezone.utc
        )
        return dt.strftime("%Y-%m-%d")


@dataclass
class LegResult:
    """Result of a single leg (BTC or ETH) within a cycle."""
    symbol: str
    direction: str         # "LONG" or "SHORT"
    entry_price: float
    entry_time_ms: int

    # Partial TP1 (50%)
    tp1_hit: bool
    tp1_price: float
    tp1_time_ms: int
    tp1_pnl_gross: float   # PnL on the 50% partial
    tp1_fee: float

    # Second exit (remaining 50%): either TP2, BE-stop, or Early-Cut
    exit2_reason: str       # "TP2", "BE_STOP", "EARLY_CUT", "END_OF_DATA"
    exit2_price: float
    exit2_time_ms: int
    exit2_pnl_gross: float
    exit2_fee: float

    # Aggregated
    total_net_pnl: float    # After all fees
    total_fees: float

    # Diagnostic
    max_favorable_excursion: float  # % peak favorable move
    max_adverse_excursion: float    # % peak adverse move
    exit_candle_idx: int            # Index in common_times


@dataclass
class CycleResult:
    """Combined result of one BTC+ETH cycle."""
    cycle_id: int
    entry_time_ms: int
    entry_time_utc: str
    exit_time_ms: int
    exit_time_utc: str
    holding_candles: int

    btc_leg: LegResult
    eth_leg: LegResult

    combined_net_pnl: float
    equity_after: float
    is_pair_win: bool


@dataclass
class ForensicMetrics:
    """Complete audit metrics."""
    # Run parameters
    start_date: str
    end_date: str
    fee_model: str
    fee_rate_pct: float
    total_candles_aligned: int

    # Trade statistics
    total_cycles: int
    pair_wins: int
    pair_losses: int
    pair_win_rate_pct: float

    btc_tp1_hit_count: int
    btc_tp2_hit_count: int
    btc_be_stop_count: int
    btc_early_cut_count: int

    eth_tp1_hit_count: int
    eth_tp2_hit_count: int
    eth_be_stop_count: int
    eth_early_cut_count: int

    # Equity curve
    initial_equity: float
    final_equity: float
    net_profit_usd: float
    net_profit_pct: float

    # Drawdown
    max_trailing_drawdown_usd: float
    max_trailing_drawdown_pct: float
    max_trailing_drawdown_date: str

    worst_daily_drawdown_usd: float
    worst_daily_drawdown_pct: float
    worst_daily_drawdown_date: str

    # Prop firm compliance
    daily_dd_breaches: int    # Number of days breaching -$30 (3%)
    max_dd_breached: bool     # Whether -$50 (5%) ever breached
    profit_target_reached: bool
    trade_to_target: Optional[int]
    days_to_target: Optional[float]

    # Intra-candle dispute stats
    same_candle_tp_sl_count_btc: int
    same_candle_tp_sl_count_eth: int

    # Rolling challenge stats
    rolling_windows_tested: int
    rolling_pass_count: int
    rolling_pass_rate_pct: float
    rolling_avg_days_to_pass: float
    rolling_fail_daily_dd: int
    rolling_fail_max_dd: int


# ─────────────────────────────────────────────────────────────
# Data Loading (Independent Implementation)
# ─────────────────────────────────────────────────────────────

def parse_date_ms(date_str: str) -> int:
    """Parse YYYY-MM-DD to epoch milliseconds (UTC)."""
    dt = datetime.datetime.strptime(date_str.strip()[:10], "%Y-%m-%d")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)


def ms_to_utc(ts_ms: int) -> str:
    """Convert epoch ms to ISO UTC string."""
    dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def ms_to_date(ts_ms: int) -> str:
    """Convert epoch ms to YYYY-MM-DD."""
    dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc)
    return dt.strftime("%Y-%m-%d")


def load_1h_candles(
    symbol: str,
    data_dir: str,
    start_ms: int,
    end_ms: int
) -> List[Candle]:
    """
    Load 1-hour OHLCV candles from Binance Vision monthly CSV files.
    Independent implementation - does NOT use engine.py.
    """
    sym = symbol.replace("_", "").upper()
    folder = os.path.join(data_dir, sym, "1h")
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Data directory not found: {folder}")

    pattern = os.path.join(folder, f"{sym}-1h-*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No CSV files matching: {pattern}")

    candles: List[Candle] = []
    seen = set()

    for fpath in files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 7:
                    continue
                try:
                    ot = int(float(row[0]))
                except (ValueError, IndexError):
                    continue  # Skip header rows

                if ot < start_ms or ot > end_ms:
                    continue
                if ot in seen:
                    continue
                seen.add(ot)

                try:
                    candles.append(Candle(
                        open_time_ms=ot,
                        open=float(row[1]),
                        high=float(row[2]),
                        low=float(row[3]),
                        close=float(row[4]),
                        volume=float(row[5]),
                        close_time_ms=int(float(row[6]))
                    ))
                except (ValueError, IndexError):
                    continue

    candles.sort(key=lambda c: c.open_time_ms)
    return candles


# ─────────────────────────────────────────────────────────────
# Core Backtester Logic
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# 1-Minute Dispute Resolver (Eliminating Intra-Candle Ambiguity)
# ─────────────────────────────────────────────────────────────

# Module-level persistent cache across all backtest runs (loaded once per process)
_SHARED_1M_MONTH_CACHE: Dict[Tuple[str, str], Dict[int, List[Tuple[int, float, float, float, float]]]] = {}

class OneMinuteDisputeResolver:
    """
    LRU-cached resolver that loads 1-minute OHLCV candles from Binance Vision CSVs
    to resolve intra-candle sequence and eliminate ambiguity with zero lookahead bias.

    ADVERSARIAL RESOLUTION RULES:
    1. Phase 1 (Entry to TP1/Early-Cut):
       - Walk minute-by-minute (0 to 59).
       - If within the SAME 1-minute candle both TP1 (+0.20%) and Early-Cut (-0.40%) are touched:
         DECLARE EARLY-CUT SL! (Explicit user command)
       - If Early-Cut touched in minute m before TP1: DECLARE EARLY-CUT SL!
       - If TP1 touched in minute m before Early-Cut:
         TP1 fires at tp1_price on 50% ($375).
         Then evaluate the remaining minutes of that hour for the runner (TP2 vs BE stop).
    2. Phase 2 (TP1 already executed, Runner alive):
       - Walk minute-by-minute (0 to 59).
       - If within the SAME 1-minute candle both TP2 (+1.00%) and BE stop (+0.10%) are touched:
         DECLARE BE STOP! (Pessimistic tie-breaker)
       - If BE stop touched in minute m before TP2: DECLARE BE STOP!
       - If TP2 touched in minute m before BE stop: DECLARE TP2!
    3. Missing data or file read failure:
       - Pessimistic fallback: Phase 1 -> Early-Cut SL; Phase 2 -> BE stop.
    """
    def __init__(self, data_dir: str, max_cached_months: int = 4):
        self.data_dir = data_dir
        self.max_cached_months = max_cached_months
        # cache key: (symbol, year_month) -> dict of hour_open_ms -> list of (open_time_ms, open, high, low, close)
        self.cache: OrderedDict[Tuple[str, str], Dict[int, List[Tuple[int, float, float, float, float]]]] = OrderedDict()

        # Diagnostic counters
        self.disputes_p1_total = 0
        self.disputes_p1_sl_first = 0
        self.disputes_p1_tp1_first = 0
        self.disputes_p1_same_1m_sl = 0

        self.disputes_p2_total = 0
        self.disputes_p2_be_first = 0
        self.disputes_p2_tp2_first = 0
        self.disputes_p2_same_1m_be = 0

    def get_1m_candles(self, symbol: str, hour_ms: int) -> List[Tuple[int, float, float, float, float]]:
        """Return chronological 1m candles for given hour timestamp with fast caching."""
        dt = datetime.datetime.fromtimestamp(hour_ms / 1000.0, tz=datetime.timezone.utc)
        ym = dt.strftime("%Y-%m")
        key = (symbol, ym)

        if key in self.cache:
            return self.cache[key].get(hour_ms, [])
        if key in _SHARED_1M_MONTH_CACHE:
            return _SHARED_1M_MONTH_CACHE[key].get(hour_ms, [])

        sym_dir = os.path.join(self.data_dir, symbol, "1m")
        if not os.path.isdir(sym_dir):
            return []
        monthly_file = os.path.join(sym_dir, f"{symbol}-1m-{ym}.csv")
        if os.path.isfile(monthly_file):
            files = [monthly_file]
        else:
            files = sorted(glob.glob(os.path.join(sym_dir, f"{symbol}-1m-{ym}-*.csv")))

        hour_map: Dict[int, List[Tuple[int, float, float, float, float]]] = {}
        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        p = line.split(",")
                        if len(p) >= 5:
                            try:
                                ot = int(float(p[0]))
                                h_key = (ot // 3600000) * 3600000
                                if h_key not in hour_map:
                                    hour_map[h_key] = []
                                hour_map[h_key].append((
                                    ot,
                                    float(p[1]),
                                    float(p[2]),
                                    float(p[3]),
                                    float(p[4])
                                ))
                            except ValueError:
                                continue
            except Exception:
                continue

        for h_k in hour_map:
            hour_map[h_k].sort(key=lambda x: x[0])

        _SHARED_1M_MONTH_CACHE[key] = hour_map
        self.cache[key] = hour_map

        return hour_map.get(hour_ms, [])

    def resolve_phase1_dispute(
        self,
        symbol: str,
        direction: str,
        hour_ms: int,
        tp1_price: float,
        early_cut_price: float,
        tp2_price: float,
        be_price: float,
    ) -> Tuple[str, float, int, Optional[str], float, int]:
        """
        Resolve Phase 1 dispute when 1-hour candle breaches both TP1 and Early-Cut.
        Returns:
            (outcome, p1_price, p1_time_ms, runner_exit_reason, runner_exit_price, runner_exit_time_ms)
        """
        self.disputes_p1_total += 1
        candles = self.get_1m_candles(symbol, hour_ms)
        if not candles:
            # Fallback if no 1m data: declare SL
            self.disputes_p1_sl_first += 1
            return ("EARLY_CUT", early_cut_price, hour_ms, None, 0.0, 0)

        for idx, (ot, o, h, l, c) in enumerate(candles):
            if direction == "LONG":
                m_tp1 = h >= tp1_price
                m_sl = l <= early_cut_price
            else:
                m_tp1 = l <= tp1_price
                m_sl = h >= early_cut_price

            if m_tp1 and m_sl:
                # USER DIRECTIVE: if in 1min too tp and sl are in same candle, declare sl!
                self.disputes_p1_same_1m_sl += 1
                return ("EARLY_CUT", early_cut_price, ot, None, 0.0, 0)

            if m_sl:
                self.disputes_p1_sl_first += 1
                return ("EARLY_CUT", early_cut_price, ot, None, 0.0, 0)

            if m_tp1:
                self.disputes_p1_tp1_first += 1
                tp1_time = ot

                # Check rest of this minute for runner
                if direction == "LONG":
                    m_tp2 = h >= tp2_price
                    m_be = c <= be_price
                else:
                    m_tp2 = l <= tp2_price
                    m_be = c >= be_price

                if m_tp2 and m_be:
                    return ("TP1_DONE", tp1_price, tp1_time, "BE_STOP", be_price, ot)
                if m_tp2:
                    return ("TP1_DONE", tp1_price, tp1_time, "TP2", tp2_price, ot)
                if m_be:
                    return ("TP1_DONE", tp1_price, tp1_time, "BE_STOP", be_price, ot)

                # Check subsequent minutes in the hour
                for rem_ot, rem_o, rem_h, rem_l, rem_c in candles[idx + 1:]:
                    if direction == "LONG":
                        rem_tp2 = rem_h >= tp2_price
                        rem_be = rem_l <= be_price
                    else:
                        rem_tp2 = rem_l <= tp2_price
                        rem_be = rem_h >= be_price

                    if rem_tp2 and rem_be:
                        return ("TP1_DONE", tp1_price, tp1_time, "BE_STOP", be_price, rem_ot)
                    if rem_be:
                        return ("TP1_DONE", tp1_price, tp1_time, "BE_STOP", be_price, rem_ot)
                    if rem_tp2:
                        return ("TP1_DONE", tp1_price, tp1_time, "TP2", tp2_price, rem_ot)

                return ("TP1_DONE", tp1_price, tp1_time, None, 0.0, 0)

        # Fallback
        self.disputes_p1_sl_first += 1
        return ("EARLY_CUT", early_cut_price, hour_ms, None, 0.0, 0)

    def resolve_phase1_tp1_runner(
        self,
        symbol: str,
        direction: str,
        hour_ms: int,
        tp1_price: float,
        tp2_price: float,
        be_price: float,
    ) -> Tuple[int, Optional[str], float, int]:
        """
        When TP1 is hit without SL dispute in 1-hour candle, check 1m candles
        to determine when TP1 hit and if the runner also exited during the same hour.
        """
        candles = self.get_1m_candles(symbol, hour_ms)
        if not candles:
            return (hour_ms, None, 0.0, 0)

        for idx, (ot, o, h, l, c) in enumerate(candles):
            if direction == "LONG":
                m_tp1 = h >= tp1_price
            else:
                m_tp1 = l <= tp1_price

            if m_tp1:
                tp1_time = ot

                if direction == "LONG":
                    m_tp2 = h >= tp2_price
                    m_be = c <= be_price
                else:
                    m_tp2 = l <= tp2_price
                    m_be = c >= be_price

                if m_tp2 and m_be:
                    return (tp1_time, "BE_STOP", be_price, ot)
                if m_tp2:
                    return (tp1_time, "TP2", tp2_price, ot)
                if m_be:
                    return (tp1_time, "BE_STOP", be_price, ot)

                for rem_ot, rem_o, rem_h, rem_l, rem_c in candles[idx + 1:]:
                    if direction == "LONG":
                        rem_tp2 = rem_h >= tp2_price
                        rem_be = rem_l <= be_price
                    else:
                        rem_tp2 = rem_l <= tp2_price
                        rem_be = rem_h >= be_price

                    if rem_tp2 and rem_be:
                        return (tp1_time, "BE_STOP", be_price, rem_ot)
                    if rem_be:
                        return (tp1_time, "BE_STOP", be_price, rem_ot)
                    if rem_tp2:
                        return (tp1_time, "TP2", tp2_price, rem_ot)

                return (tp1_time, None, 0.0, 0)

        return (hour_ms, None, 0.0, 0)

    def resolve_phase2_dispute(
        self,
        symbol: str,
        direction: str,
        hour_ms: int,
        tp2_price: float,
        be_price: float,
    ) -> Tuple[str, float, int]:
        """
        Resolve Phase 2 dispute when 1-hour candle breaches both TP2 and BE stop.
        """
        self.disputes_p2_total += 1
        candles = self.get_1m_candles(symbol, hour_ms)
        if not candles:
            self.disputes_p2_be_first += 1
            return ("BE_STOP", be_price, hour_ms)

        for ot, o, h, l, c in candles:
            if direction == "LONG":
                m_tp2 = h >= tp2_price
                m_be = l <= be_price
            else:
                m_tp2 = l <= tp2_price
                m_be = h >= be_price

            if m_tp2 and m_be:
                # Both hit in same 1m candle -> pessimistic BE stop
                self.disputes_p2_same_1m_be += 1
                return ("BE_STOP", be_price, ot)
            if m_be:
                self.disputes_p2_be_first += 1
                return ("BE_STOP", be_price, ot)
            if m_tp2:
                self.disputes_p2_tp2_first += 1
                return ("TP2", tp2_price, ot)

        self.disputes_p2_be_first += 1
        return ("BE_STOP", be_price, hour_ms)

    def resolve_simple_tp_sl(
        self,
        symbol: str,
        direction: str,
        hour_ms: int,
        entry_price: float,
        tp_price: float,
        sl_price: float,
    ) -> Tuple[str, float, int]:
        """
        Resolve dispute when 1-hour candle breaches both fixed TP and fixed SL.
        Returns: ("TP" | "SL", exit_price, exit_time_ms)
        Adversarial tie-breaker: If both TP and SL are touched in the exact same
        1-minute candle, strictly declare SL (pessimistic fill).
        """
        candles = self.get_1m_candles(symbol, hour_ms)
        if not candles:
            # Fallback if no 1m data: declare SL
            return ("SL", sl_price, hour_ms)

        for ot, o, h, l, c in candles:
            if direction == "LONG":
                m_tp = h >= tp_price
                m_sl = l <= sl_price
            else:
                m_tp = l <= tp_price
                m_sl = h >= sl_price

            if m_tp and m_sl:
                # Both hit in exact same 1m candle -> strictly declare SL
                return ("SL", sl_price, ot)
            if m_sl:
                return ("SL", sl_price, ot)
            if m_tp:
                return ("TP", tp_price, ot)

        # Fallback: declare SL
        return ("SL", sl_price, hour_ms)


# ─────────────────────────────────────────────────────────────
# Core Backtester Logic
# ─────────────────────────────────────────────────────────────

def simulate_single_leg(
    direction: str,            # "LONG" or "SHORT"
    symbol: str,
    entry_price: float,
    entry_time_ms: int,
    candles: List[Candle],     # Candles from entry onward
    candle_start_idx: int,     # Global index for the entry candle
    notional_per_leg: float,   # $750
    fee_rate_pct: float,       # 0.060 or 0.090
    tp1_pct: float = 0.20,    # +0.20%
    tp2_pct: float = 1.00,    # +1.00%
    be_pct: float = 0.10,     # +0.10% BE lock
    early_cut_pct: float = 0.40,  # -0.40%
    tp_pct_original: float = 1.50, # original SL before early-cut
    resolver: Optional[OneMinuteDisputeResolver] = None,
) -> Tuple[LegResult, int]:
    """
    Simulate one leg of the pairs trade.

    Returns (LegResult, exit_candle_global_idx)

    CRITICAL ANTI-BIAS RULES:
    1. Entry at candle Open (already provided as entry_price)
    2. Within each candle, check if TP1/TP2/Early-Cut/BE thresholds are hit
       using only High/Low range
    3. If BOTH TP and SL thresholds are hit in the SAME 1-hour candle:
       Use OneMinuteDisputeResolver (if available) to evaluate chronological 1m candles.
       If both TP and SL hit in the same 1m candle: DECLARE SL! (Explicit user command)
       If resolver is None: conservatively declare SL/Early-Cut fires first (pessimistic).
    4. Fee is applied per fill: entry fill + exit fill(s)
    """
    half_notional = notional_per_leg / 2.0  # $375

    # Calculate price levels
    if direction == "LONG":
        tp1_price = entry_price * (1.0 + tp1_pct / 100.0)
        tp2_price = entry_price * (1.0 + tp2_pct / 100.0)
        be_price = entry_price * (1.0 + be_pct / 100.0)
        early_cut_price = entry_price * (1.0 - early_cut_pct / 100.0)
    else:  # SHORT
        tp1_price = entry_price * (1.0 - tp1_pct / 100.0)
        tp2_price = entry_price * (1.0 - tp2_pct / 100.0)
        be_price = entry_price * (1.0 - be_pct / 100.0)
        early_cut_price = entry_price * (1.0 + early_cut_pct / 100.0)

    fee_per_half = half_notional * fee_rate_pct / 100.0

    tp1_hit = False
    tp1_price_actual = 0.0
    tp1_time_ms = 0
    tp1_pnl_gross = 0.0
    tp1_fee = 0.0

    mfe = 0.0  # Max Favorable Excursion (%)
    mae = 0.0  # Max Adverse Excursion (%)

    for global_idx in range(candle_start_idx, len(candles)):
        candle = candles[global_idx]

        # Calculate excursions for this candle
        if direction == "LONG":
            candle_mfe = (candle.high - entry_price) / entry_price * 100.0
            candle_mae = (entry_price - candle.low) / entry_price * 100.0
        else:
            candle_mfe = (entry_price - candle.low) / entry_price * 100.0
            candle_mae = (candle.high - entry_price) / entry_price * 100.0

        mfe = max(mfe, candle_mfe)
        mae = max(mae, candle_mae)

        if not tp1_hit:
            # Phase 1: Looking for TP1 or Early-Cut
            if direction == "LONG":
                hit_tp1 = candle.high >= tp1_price
                hit_early_cut = candle.low <= early_cut_price
            else:
                hit_tp1 = candle.low <= tp1_price
                hit_early_cut = candle.high >= early_cut_price

            if hit_tp1 and hit_early_cut:
                # ── INTRA-HOUR DISPUTE ──
                if resolver is not None:
                    outcome, p1_p, p1_t, ext2_reason, ext2_p, ext2_t = resolver.resolve_phase1_dispute(
                        symbol=symbol,
                        direction=direction,
                        hour_ms=candle.open_time_ms,
                        tp1_price=tp1_price,
                        early_cut_price=early_cut_price,
                        tp2_price=tp2_price,
                        be_price=be_price,
                    )
                    if outcome == "EARLY_CUT":
                        if direction == "LONG":
                            price_move_pct = (early_cut_price - entry_price) / entry_price * 100.0
                        else:
                            price_move_pct = (entry_price - early_cut_price) / entry_price * 100.0
                        gross_pnl = notional_per_leg * price_move_pct / 100.0
                        total_fee = notional_per_leg * fee_rate_pct / 100.0
                        return LegResult(
                            symbol=symbol, direction=direction,
                            entry_price=entry_price, entry_time_ms=entry_time_ms,
                            tp1_hit=False, tp1_price=0.0, tp1_time_ms=0,
                            tp1_pnl_gross=0.0, tp1_fee=0.0,
                            exit2_reason="EARLY_CUT",
                            exit2_price=early_cut_price,
                            exit2_time_ms=p1_t,
                            exit2_pnl_gross=gross_pnl,
                            exit2_fee=total_fee,
                            total_net_pnl=gross_pnl - total_fee,
                            total_fees=total_fee,
                            max_favorable_excursion=mfe,
                            max_adverse_excursion=mae,
                            exit_candle_idx=global_idx
                        ), global_idx
                    else:  # outcome == "TP1_DONE"
                        tp1_hit = True
                        tp1_price_actual = tp1_price
                        tp1_time_ms = p1_t
                        if direction == "LONG":
                            tp1_move_pct = (tp1_price - entry_price) / entry_price * 100.0
                        else:
                            tp1_move_pct = (entry_price - tp1_price) / entry_price * 100.0
                        tp1_pnl_gross = half_notional * tp1_move_pct / 100.0
                        tp1_fee = fee_per_half

                        if ext2_reason is not None:
                            # Runner exited in same hour
                            if direction == "LONG":
                                exit2_move_pct = (ext2_p - entry_price) / entry_price * 100.0
                            else:
                                exit2_move_pct = (entry_price - ext2_p) / entry_price * 100.0
                            exit2_pnl = half_notional * exit2_move_pct / 100.0
                            return LegResult(
                                symbol=symbol, direction=direction,
                                entry_price=entry_price, entry_time_ms=entry_time_ms,
                                tp1_hit=True, tp1_price=tp1_price_actual,
                                tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                                tp1_fee=tp1_fee,
                                exit2_reason=ext2_reason,
                                exit2_price=ext2_p,
                                exit2_time_ms=ext2_t,
                                exit2_pnl_gross=exit2_pnl,
                                exit2_fee=fee_per_half,
                                total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                                total_fees=tp1_fee + fee_per_half,
                                max_favorable_excursion=mfe,
                                max_adverse_excursion=mae,
                                exit_candle_idx=global_idx
                            ), global_idx
                        else:
                            # Runner still open, continue into Phase 2
                            continue
                else:
                    # Fallback without resolver: pessimistic Early-Cut wins
                    if direction == "LONG":
                        price_move_pct = (early_cut_price - entry_price) / entry_price * 100.0
                    else:
                        price_move_pct = (entry_price - early_cut_price) / entry_price * 100.0
                    gross_pnl = notional_per_leg * price_move_pct / 100.0
                    total_fee = notional_per_leg * fee_rate_pct / 100.0
                    return LegResult(
                        symbol=symbol, direction=direction,
                        entry_price=entry_price, entry_time_ms=entry_time_ms,
                        tp1_hit=False, tp1_price=0.0, tp1_time_ms=0,
                        tp1_pnl_gross=0.0, tp1_fee=0.0,
                        exit2_reason="EARLY_CUT",
                        exit2_price=early_cut_price,
                        exit2_time_ms=candle.open_time_ms,
                        exit2_pnl_gross=gross_pnl,
                        exit2_fee=total_fee,
                        total_net_pnl=gross_pnl - total_fee,
                        total_fees=total_fee,
                        max_favorable_excursion=mfe,
                        max_adverse_excursion=mae,
                        exit_candle_idx=global_idx
                    ), global_idx

            elif hit_early_cut:
                # Early-Cut fires: close 100% at early_cut_price
                if direction == "LONG":
                    price_move_pct = (early_cut_price - entry_price) / entry_price * 100.0
                else:
                    price_move_pct = (entry_price - early_cut_price) / entry_price * 100.0

                gross_pnl = notional_per_leg * price_move_pct / 100.0
                total_fee = notional_per_leg * fee_rate_pct / 100.0

                return LegResult(
                    symbol=symbol,
                    direction=direction,
                    entry_price=entry_price,
                    entry_time_ms=entry_time_ms,
                    tp1_hit=False,
                    tp1_price=0.0,
                    tp1_time_ms=0,
                    tp1_pnl_gross=0.0,
                    tp1_fee=0.0,
                    exit2_reason="EARLY_CUT",
                    exit2_price=early_cut_price,
                    exit2_time_ms=candle.open_time_ms,
                    exit2_pnl_gross=gross_pnl,
                    exit2_fee=total_fee,
                    total_net_pnl=gross_pnl - total_fee,
                    total_fees=total_fee,
                    max_favorable_excursion=mfe,
                    max_adverse_excursion=mae,
                    exit_candle_idx=global_idx
                ), global_idx

            elif hit_tp1:
                # TP1 fires: close 50% at tp1_price
                tp1_hit = True
                tp1_price_actual = tp1_price
                tp1_time_ms = candle.open_time_ms
                if direction == "LONG":
                    tp1_move_pct = (tp1_price - entry_price) / entry_price * 100.0
                else:
                    tp1_move_pct = (entry_price - tp1_price) / entry_price * 100.0
                tp1_pnl_gross = half_notional * tp1_move_pct / 100.0
                tp1_fee = fee_per_half

                if resolver is not None:
                    p1_t, ext2_reason, ext2_p, ext2_t = resolver.resolve_phase1_tp1_runner(
                        symbol=symbol,
                        direction=direction,
                        hour_ms=candle.open_time_ms,
                        tp1_price=tp1_price,
                        tp2_price=tp2_price,
                        be_price=be_price,
                    )
                    tp1_time_ms = p1_t
                    if ext2_reason is not None:
                        if direction == "LONG":
                            exit2_move_pct = (ext2_p - entry_price) / entry_price * 100.0
                        else:
                            exit2_move_pct = (entry_price - ext2_p) / entry_price * 100.0
                        exit2_pnl = half_notional * exit2_move_pct / 100.0
                        return LegResult(
                            symbol=symbol, direction=direction,
                            entry_price=entry_price, entry_time_ms=entry_time_ms,
                            tp1_hit=True, tp1_price=tp1_price_actual,
                            tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                            tp1_fee=tp1_fee,
                            exit2_reason=ext2_reason,
                            exit2_price=ext2_p,
                            exit2_time_ms=ext2_t,
                            exit2_pnl_gross=exit2_pnl,
                            exit2_fee=fee_per_half,
                            total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                            total_fees=tp1_fee + fee_per_half,
                            max_favorable_excursion=mfe,
                            max_adverse_excursion=mae,
                            exit_candle_idx=global_idx
                        ), global_idx
                    else:
                        continue
                else:
                    # Conservative fallback without resolver
                    if direction == "LONG":
                        hit_tp2_same = candle.high >= tp2_price
                        hit_be_stop_same = candle.close <= be_price
                    else:
                        hit_tp2_same = candle.low <= tp2_price
                        hit_be_stop_same = candle.close >= be_price

                    if hit_tp2_same and hit_be_stop_same:
                        if direction == "LONG":
                            exit2_move_pct = (be_price - entry_price) / entry_price * 100.0
                        else:
                            exit2_move_pct = (entry_price - be_price) / entry_price * 100.0
                        exit2_pnl = half_notional * exit2_move_pct / 100.0
                        return LegResult(
                            symbol=symbol, direction=direction,
                            entry_price=entry_price, entry_time_ms=entry_time_ms,
                            tp1_hit=True, tp1_price=tp1_price_actual,
                            tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                            tp1_fee=tp1_fee,
                            exit2_reason="BE_STOP",
                            exit2_price=be_price,
                            exit2_time_ms=candle.open_time_ms,
                            exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                            total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                            total_fees=tp1_fee + fee_per_half,
                            max_favorable_excursion=mfe, max_adverse_excursion=mae,
                            exit_candle_idx=global_idx
                        ), global_idx

                    elif hit_be_stop_same:
                        if direction == "LONG":
                            exit2_move_pct = (be_price - entry_price) / entry_price * 100.0
                        else:
                            exit2_move_pct = (entry_price - be_price) / entry_price * 100.0
                        exit2_pnl = half_notional * exit2_move_pct / 100.0
                        return LegResult(
                            symbol=symbol, direction=direction,
                            entry_price=entry_price, entry_time_ms=entry_time_ms,
                            tp1_hit=True, tp1_price=tp1_price_actual,
                            tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                            tp1_fee=tp1_fee,
                            exit2_reason="BE_STOP",
                            exit2_price=be_price,
                            exit2_time_ms=candle.open_time_ms,
                            exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                            total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                            total_fees=tp1_fee + fee_per_half,
                            max_favorable_excursion=mfe, max_adverse_excursion=mae,
                            exit_candle_idx=global_idx
                        ), global_idx

                    elif hit_tp2_same:
                        if direction == "LONG":
                            exit2_move_pct = (tp2_price - entry_price) / entry_price * 100.0
                        else:
                            exit2_move_pct = (entry_price - tp2_price) / entry_price * 100.0
                        exit2_pnl = half_notional * exit2_move_pct / 100.0
                        return LegResult(
                            symbol=symbol, direction=direction,
                            entry_price=entry_price, entry_time_ms=entry_time_ms,
                            tp1_hit=True, tp1_price=tp1_price_actual,
                            tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                            tp1_fee=tp1_fee,
                            exit2_reason="TP2",
                            exit2_price=tp2_price,
                            exit2_time_ms=candle.open_time_ms,
                            exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                            total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                            total_fees=tp1_fee + fee_per_half,
                            max_favorable_excursion=mfe, max_adverse_excursion=mae,
                            exit_candle_idx=global_idx
                        ), global_idx

                    continue

        else:
            # Phase 2: TP1 already hit. Looking for TP2 or BE-stop on remaining 50%
            if direction == "LONG":
                hit_tp2 = candle.high >= tp2_price
                hit_be_stop = candle.low <= be_price
            else:
                hit_tp2 = candle.low <= tp2_price
                hit_be_stop = candle.high >= be_price

            if hit_tp2 and hit_be_stop:
                # ── INTRA-HOUR DISPUTE ON RUNNER ──
                if resolver is not None:
                    ext2_reason, ext2_p, ext2_t = resolver.resolve_phase2_dispute(
                        symbol=symbol,
                        direction=direction,
                        hour_ms=candle.open_time_ms,
                        tp2_price=tp2_price,
                        be_price=be_price,
                    )
                    if direction == "LONG":
                        exit2_move_pct = (ext2_p - entry_price) / entry_price * 100.0
                    else:
                        exit2_move_pct = (entry_price - ext2_p) / entry_price * 100.0
                    exit2_pnl = half_notional * exit2_move_pct / 100.0
                    return LegResult(
                        symbol=symbol, direction=direction,
                        entry_price=entry_price, entry_time_ms=entry_time_ms,
                        tp1_hit=True, tp1_price=tp1_price_actual,
                        tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                        tp1_fee=tp1_fee,
                        exit2_reason=ext2_reason,
                        exit2_price=ext2_p,
                        exit2_time_ms=ext2_t,
                        exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                        total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                        total_fees=tp1_fee + fee_per_half,
                        max_favorable_excursion=mfe, max_adverse_excursion=mae,
                        exit_candle_idx=global_idx
                    ), global_idx
                else:
                    # Fallback: pessimistic BE-stop
                    if direction == "LONG":
                        exit2_move_pct = (be_price - entry_price) / entry_price * 100.0
                    else:
                        exit2_move_pct = (entry_price - be_price) / entry_price * 100.0
                    exit2_pnl = half_notional * exit2_move_pct / 100.0
                    return LegResult(
                        symbol=symbol, direction=direction,
                        entry_price=entry_price, entry_time_ms=entry_time_ms,
                        tp1_hit=True, tp1_price=tp1_price_actual,
                        tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                        tp1_fee=tp1_fee,
                        exit2_reason="BE_STOP",
                        exit2_price=be_price,
                        exit2_time_ms=candle.open_time_ms,
                        exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                        total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                        total_fees=tp1_fee + fee_per_half,
                        max_favorable_excursion=mfe, max_adverse_excursion=mae,
                        exit_candle_idx=global_idx
                    ), global_idx

            elif hit_be_stop:
                # BE-stop fires
                if direction == "LONG":
                    exit2_move_pct = (be_price - entry_price) / entry_price * 100.0
                else:
                    exit2_move_pct = (entry_price - be_price) / entry_price * 100.0
                exit2_pnl = half_notional * exit2_move_pct / 100.0

                return LegResult(
                    symbol=symbol, direction=direction,
                    entry_price=entry_price, entry_time_ms=entry_time_ms,
                    tp1_hit=True, tp1_price=tp1_price_actual,
                    tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                    tp1_fee=tp1_fee,
                    exit2_reason="BE_STOP",
                    exit2_price=be_price,
                    exit2_time_ms=candle.open_time_ms,
                    exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                    total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                    total_fees=tp1_fee + fee_per_half,
                    max_favorable_excursion=mfe, max_adverse_excursion=mae,
                    exit_candle_idx=global_idx
                ), global_idx

            elif hit_tp2:
                # TP2 fires
                if direction == "LONG":
                    exit2_move_pct = (tp2_price - entry_price) / entry_price * 100.0
                else:
                    exit2_move_pct = (entry_price - tp2_price) / entry_price * 100.0
                exit2_pnl = half_notional * exit2_move_pct / 100.0

                return LegResult(
                    symbol=symbol, direction=direction,
                    entry_price=entry_price, entry_time_ms=entry_time_ms,
                    tp1_hit=True, tp1_price=tp1_price_actual,
                    tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
                    tp1_fee=tp1_fee,
                    exit2_reason="TP2",
                    exit2_price=tp2_price,
                    exit2_time_ms=candle.open_time_ms,
                    exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
                    total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
                    total_fees=tp1_fee + fee_per_half,
                    max_favorable_excursion=mfe, max_adverse_excursion=mae,
                    exit_candle_idx=global_idx
                ), global_idx

    # End of data - close at last candle close
    last_candle = candles[-1]
    last_idx = len(candles) - 1
    if direction == "LONG":
        close_move_pct = (last_candle.close - entry_price) / entry_price * 100.0
    else:
        close_move_pct = (entry_price - last_candle.close) / entry_price * 100.0

    if tp1_hit:
        exit2_pnl = half_notional * close_move_pct / 100.0
        return LegResult(
            symbol=symbol, direction=direction,
            entry_price=entry_price, entry_time_ms=entry_time_ms,
            tp1_hit=True, tp1_price=tp1_price_actual,
            tp1_time_ms=tp1_time_ms, tp1_pnl_gross=tp1_pnl_gross,
            tp1_fee=tp1_fee,
            exit2_reason="END_OF_DATA",
            exit2_price=last_candle.close,
            exit2_time_ms=last_candle.open_time_ms,
            exit2_pnl_gross=exit2_pnl, exit2_fee=fee_per_half,
            total_net_pnl=(tp1_pnl_gross - tp1_fee) + (exit2_pnl - fee_per_half),
            total_fees=tp1_fee + fee_per_half,
            max_favorable_excursion=mfe, max_adverse_excursion=mae,
            exit_candle_idx=last_idx
        ), last_idx
    else:
        gross_pnl = notional_per_leg * close_move_pct / 100.0
        total_fee = notional_per_leg * fee_rate_pct / 100.0
        return LegResult(
            symbol=symbol, direction=direction,
            entry_price=entry_price, entry_time_ms=entry_time_ms,
            tp1_hit=False, tp1_price=0.0, tp1_time_ms=0,
            tp1_pnl_gross=0.0, tp1_fee=0.0,
            exit2_reason="END_OF_DATA",
            exit2_price=last_candle.close,
            exit2_time_ms=last_candle.open_time_ms,
            exit2_pnl_gross=gross_pnl, exit2_fee=total_fee,
            total_net_pnl=gross_pnl - total_fee,
            total_fees=total_fee,
            max_favorable_excursion=mfe, max_adverse_excursion=mae,
            exit_candle_idx=last_idx
        ), last_idx



def run_forensic_backtest(
    data_dir: str,
    start_date: str = "2020-01-01",
    end_date: str = "2026-09-30",
    initial_capital: float = 1000.0,
    notional_per_leg: float = 750.0,
    fee_rate_pct: float = 0.060,
    fee_model_name: str = "LIMIT_ENTRY_MARKET_EXIT",
    tp1_pct: float = 0.20,
    tp2_pct: float = 1.00,
    be_pct: float = 0.10,
    early_cut_pct: float = 0.40,
    daily_dd_limit_pct: float = 3.0,
    max_dd_limit_pct: float = 5.0,
    profit_target_pct: float = 10.0,
    use_1m_resolution: bool = True,
    verbose: bool = True
) -> Tuple[List[CycleResult], ForensicMetrics]:
    """
    Run the complete forensic backtest.

    This is an INDEPENDENT implementation that does NOT use engine.py.
    """
    start_ms = parse_date_ms(start_date)
    end_ms = parse_date_ms(end_date) + (24 * 3600 * 1000 - 1)

    if verbose:
        print(f"[FORENSIC] Loading BTC 1h candles...")
    btc_candles = load_1h_candles("BTCUSDT", data_dir, start_ms, end_ms)
    if verbose:
        print(f"[FORENSIC] Loading ETH 1h candles...")
    eth_candles = load_1h_candles("ETHUSDT", data_dir, start_ms, end_ms)

    if verbose:
        print(f"[FORENSIC] BTC candles: {len(btc_candles)}, ETH candles: {len(eth_candles)}")

    # Build aligned timeline
    btc_dict = {c.open_time_ms: c for c in btc_candles}
    eth_dict = {c.open_time_ms: c for c in eth_candles}
    common_times = sorted(set(btc_dict.keys()) & set(eth_dict.keys()))

    if verbose:
        print(f"[FORENSIC] Aligned candles: {len(common_times)} "
              f"({len(common_times)/24:.1f} days)")

    # Build aligned candle arrays
    btc_aligned = [btc_dict[t] for t in common_times]
    eth_aligned = [eth_dict[t] for t in common_times]

    total_candles = len(common_times)

    # Initialize 1-Minute Dispute Resolver
    resolver = OneMinuteDisputeResolver(data_dir=data_dir) if use_1m_resolution else None
    if verbose and resolver:
        print(f"[FORENSIC] 1-Minute Dispute Resolver ACTIVE (LRU cache initialized)")

    # Track equity, drawdown, daily boundaries
    equity = initial_capital
    peak_equity = initial_capital
    max_trailing_dd_usd = 0.0
    max_trailing_dd_pct = 0.0
    max_trailing_dd_date = ""

    # Daily drawdown tracking
    daily_equity_start: Dict[str, float] = {}  # date -> equity at 00:00 UTC
    daily_equity_trough: Dict[str, float] = {}  # date -> worst equity in that day
    current_date = ""

    # Prop firm limits
    daily_dd_limit_usd = initial_capital * daily_dd_limit_pct / 100.0
    max_dd_limit_usd = initial_capital * max_dd_limit_pct / 100.0
    profit_target_usd = initial_capital * profit_target_pct / 100.0
    target_balance = initial_capital + profit_target_usd

    daily_dd_breaches = 0
    max_dd_breached = False
    profit_target_reached = False
    trade_to_target = None
    days_to_target = None

    # Diagnostic counters
    same_candle_disputes_btc = 0
    same_candle_disputes_eth = 0

    btc_tp1_hits = 0
    btc_tp2_hits = 0
    btc_be_stops = 0
    btc_early_cuts = 0

    eth_tp1_hits = 0
    eth_tp2_hits = 0
    eth_be_stops = 0
    eth_early_cuts = 0

    cycles: List[CycleResult] = []

    i = 0
    cycle_id = 0

    while i < total_candles - 1:
        cycle_id += 1
        entry_ts = common_times[i]
        btc_entry_price = btc_aligned[i].open
        eth_entry_price = eth_aligned[i].open

        # Update daily tracking
        candle_date = ms_to_date(entry_ts)
        if candle_date != current_date:
            current_date = candle_date
            if candle_date not in daily_equity_start:
                daily_equity_start[candle_date] = equity
                daily_equity_trough[candle_date] = equity

        # BTC Leg: LONG from i onward
        btc_leg, btc_exit_idx = simulate_single_leg(
            direction="LONG",
            symbol="BTCUSDT",
            entry_price=btc_entry_price,
            entry_time_ms=entry_ts,
            candles=btc_aligned,
            candle_start_idx=i,
            notional_per_leg=notional_per_leg,
            fee_rate_pct=fee_rate_pct,
            tp1_pct=tp1_pct,
            tp2_pct=tp2_pct,
            be_pct=be_pct,
            early_cut_pct=early_cut_pct,
            resolver=resolver,
        )

        # ETH Leg: SHORT from i onward
        eth_leg, eth_exit_idx = simulate_single_leg(
            direction="SHORT",
            symbol="ETHUSDT",
            entry_price=eth_entry_price,
            entry_time_ms=entry_ts,
            candles=eth_aligned,
            candle_start_idx=i,
            notional_per_leg=notional_per_leg,
            fee_rate_pct=fee_rate_pct,
            tp1_pct=tp1_pct,
            tp2_pct=tp2_pct,
            be_pct=be_pct,
            early_cut_pct=early_cut_pct,
            resolver=resolver,
        )

        # Update counters
        if btc_leg.tp1_hit:
            btc_tp1_hits += 1
        if btc_leg.exit2_reason == "TP2":
            btc_tp2_hits += 1
        elif btc_leg.exit2_reason == "BE_STOP":
            btc_be_stops += 1
        elif btc_leg.exit2_reason == "EARLY_CUT":
            btc_early_cuts += 1

        if eth_leg.tp1_hit:
            eth_tp1_hits += 1
        if eth_leg.exit2_reason == "TP2":
            eth_tp2_hits += 1
        elif eth_leg.exit2_reason == "BE_STOP":
            eth_be_stops += 1
        elif eth_leg.exit2_reason == "EARLY_CUT":
            eth_early_cuts += 1

        # Combined PnL
        combined_pnl = btc_leg.total_net_pnl + eth_leg.total_net_pnl
        equity += combined_pnl

        # Free index: both legs must be done
        free_idx = max(btc_exit_idx, eth_exit_idx)
        exit_ts = common_times[free_idx]

        # Update daily tracking for exit
        exit_date = ms_to_date(exit_ts)
        if exit_date not in daily_equity_start:
            daily_equity_start[exit_date] = equity - combined_pnl  # Approx: was before this trade
            daily_equity_trough[exit_date] = equity
        if equity < daily_equity_trough.get(exit_date, equity):
            daily_equity_trough[exit_date] = equity

        # Trailing drawdown
        if equity > peak_equity:
            peak_equity = equity
        dd_usd = peak_equity - equity
        dd_pct = (dd_usd / peak_equity * 100.0) if peak_equity > 0 else 0.0
        if dd_usd > max_trailing_dd_usd:
            max_trailing_dd_usd = dd_usd
            max_trailing_dd_pct = dd_pct
            max_trailing_dd_date = exit_date

        # Check profit target
        if not profit_target_reached and equity >= target_balance:
            profit_target_reached = True
            trade_to_target = cycle_id
            first_entry_ts = cycles[0].entry_time_ms if cycles else entry_ts
            days_to_target = (exit_ts - first_entry_ts) / (1000.0 * 86400.0)

        cycle = CycleResult(
            cycle_id=cycle_id,
            entry_time_ms=entry_ts,
            entry_time_utc=ms_to_utc(entry_ts),
            exit_time_ms=exit_ts,
            exit_time_utc=ms_to_utc(exit_ts),
            holding_candles=free_idx - i + 1,
            btc_leg=btc_leg,
            eth_leg=eth_leg,
            combined_net_pnl=combined_pnl,
            equity_after=equity,
            is_pair_win=combined_pnl > 0.0
        )
        cycles.append(cycle)

        if verbose and cycle_id % 2000 == 0:
            print(f"  [FORENSIC] Cycle {cycle_id}: equity=${equity:.2f}, "
                  f"trailing DD=${max_trailing_dd_usd:.2f}")

        # Next cycle starts after both legs are free
        i = free_idx + 1

    # ─────────────────────────────────────────────────────────
    # Post-simulation: Daily Drawdown Analysis
    # ─────────────────────────────────────────────────────────
    # Rebuild daily equity curve from trade-by-trade data
    daily_pnl: Dict[str, float] = defaultdict(float)
    for c in cycles:
        exit_date = ms_to_date(c.exit_time_ms)
        daily_pnl[exit_date] += c.combined_net_pnl

    # Build day-by-day equity and compute daily drawdown
    equity_cursor = initial_capital
    worst_daily_dd_usd = 0.0
    worst_daily_dd_pct = 0.0
    worst_daily_dd_date = ""
    daily_dd_breach_count = 0

    # Group cycles by exit date for intraday tracking
    cycles_by_date: Dict[str, List[CycleResult]] = defaultdict(list)
    for c in cycles:
        exit_date = ms_to_date(c.exit_time_ms)
        cycles_by_date[exit_date] += [c]

    all_dates = sorted(set(
        [ms_to_date(c.entry_time_ms) for c in cycles] +
        [ms_to_date(c.exit_time_ms) for c in cycles]
    ))

    equity_at_day_start: Dict[str, float] = {}
    eq_track = initial_capital
    for date in all_dates:
        equity_at_day_start[date] = eq_track
        day_cycles = cycles_by_date.get(date, [])
        for c in day_cycles:
            eq_track += c.combined_net_pnl

    # Now compute intra-day drawdown
    for date in all_dates:
        sod_equity = equity_at_day_start[date]
        day_cycles = cycles_by_date.get(date, [])
        intraday_eq = sod_equity
        intraday_trough = sod_equity

        for c in day_cycles:
            intraday_eq += c.combined_net_pnl
            intraday_trough = min(intraday_trough, intraday_eq)

        daily_dd = sod_equity - intraday_trough
        daily_dd_pct_val = (daily_dd / initial_capital * 100.0)

        if daily_dd > worst_daily_dd_usd:
            worst_daily_dd_usd = daily_dd
            worst_daily_dd_pct = daily_dd_pct_val
            worst_daily_dd_date = date

        if daily_dd >= daily_dd_limit_usd:
            daily_dd_breach_count += 1

    # Check max DD breach
    max_dd_breached = max_trailing_dd_usd >= max_dd_limit_usd

    # ─────────────────────────────────────────────────────────
    # Compile Forensic Metrics
    # ─────────────────────────────────────────────────────────
    pair_wins = sum(1 for c in cycles if c.is_pair_win)
    pair_losses = len(cycles) - pair_wins

    metrics = ForensicMetrics(
        start_date=start_date,
        end_date=end_date,
        fee_model=fee_model_name,
        fee_rate_pct=fee_rate_pct,
        total_candles_aligned=total_candles,
        total_cycles=len(cycles),
        pair_wins=pair_wins,
        pair_losses=pair_losses,
        pair_win_rate_pct=round(pair_wins / len(cycles) * 100.0, 2) if cycles else 0.0,
        btc_tp1_hit_count=btc_tp1_hits,
        btc_tp2_hit_count=btc_tp2_hits,
        btc_be_stop_count=btc_be_stops,
        btc_early_cut_count=btc_early_cuts,
        eth_tp1_hit_count=eth_tp1_hits,
        eth_tp2_hit_count=eth_tp2_hits,
        eth_be_stop_count=eth_be_stops,
        eth_early_cut_count=eth_early_cuts,
        initial_equity=initial_capital,
        final_equity=round(equity, 2),
        net_profit_usd=round(equity - initial_capital, 2),
        net_profit_pct=round((equity - initial_capital) / initial_capital * 100.0, 2),
        max_trailing_drawdown_usd=round(max_trailing_dd_usd, 2),
        max_trailing_drawdown_pct=round(max_trailing_dd_pct, 2),
        max_trailing_drawdown_date=max_trailing_dd_date,
        worst_daily_drawdown_usd=round(worst_daily_dd_usd, 2),
        worst_daily_drawdown_pct=round(worst_daily_dd_pct, 2),
        worst_daily_drawdown_date=worst_daily_dd_date,
        daily_dd_breaches=daily_dd_breach_count,
        max_dd_breached=max_dd_breached,
        profit_target_reached=profit_target_reached,
        trade_to_target=trade_to_target,
        days_to_target=round(days_to_target, 1) if days_to_target else None,
        same_candle_tp_sl_count_btc=same_candle_disputes_btc,
        same_candle_tp_sl_count_eth=same_candle_disputes_eth,
        # Rolling stats filled in separately
        rolling_windows_tested=0,
        rolling_pass_count=0,
        rolling_pass_rate_pct=0.0,
        rolling_avg_days_to_pass=0.0,
        rolling_fail_daily_dd=0,
        rolling_fail_max_dd=0,
    )

    if verbose:
        print(f"\n[FORENSIC] Simulation complete: {len(cycles)} cycles")
        print(f"  Final equity: ${equity:.2f} (net: ${equity - initial_capital:+.2f})")
        print(f"  Win rate: {metrics.pair_win_rate_pct:.1f}%")
        print(f"  Max trailing DD: ${max_trailing_dd_usd:.2f} ({max_trailing_dd_pct:.2f}%)")
        print(f"  Worst daily DD: ${worst_daily_dd_usd:.2f} ({worst_daily_dd_pct:.2f}%)")
        if resolver:
            print(f"\n[FORENSIC] 1-Minute Dispute Resolution Summary:")
            print(f"  Phase 1 Disputes (TP1 vs Early-Cut): {resolver.disputes_p1_total}")
            print(f"    - TP1 hit first: {resolver.disputes_p1_tp1_first}")
            print(f"    - Early-Cut SL hit first: {resolver.disputes_p1_sl_first}")
            print(f"    - Both in same 1m candle (declared SL): {resolver.disputes_p1_same_1m_sl}")
            print(f"  Phase 2 Disputes (TP2 vs BE-Stop): {resolver.disputes_p2_total}")
            print(f"    - TP2 hit first: {resolver.disputes_p2_tp2_first}")
            print(f"    - BE-Stop hit first: {resolver.disputes_p2_be_first}")
            print(f"    - Both in same 1m candle (declared BE-Stop): {resolver.disputes_p2_same_1m_be}")

    return cycles, metrics


def run_rolling_challenge_sim(
    cycles: List[CycleResult],
    initial_capital: float = 1000.0,
    daily_dd_limit_pct: float = 3.0,
    max_dd_limit_pct: float = 5.0,
    profit_target_pct: float = 10.0,
    window_step_days: int = 7,
    verbose: bool = True,
) -> Dict[str, float]:
    """
    Run rolling prop firm challenge windows starting every `window_step_days` days.

    Returns dict with pass_rate, avg_days, fail_daily, fail_max, etc.
    """
    if not cycles:
        return {"pass_rate": 0, "windows": 0}

    step_ms = window_step_days * 24 * 3600 * 1000
    first_ts = cycles[0].entry_time_ms
    last_ts = cycles[-1].entry_time_ms
    min_window_ms = 30 * 24 * 3600 * 1000  # At least 30 days of data ahead

    start_times = []
    curr = first_ts
    while curr < last_ts - min_window_ms:
        start_times.append(curr)
        curr += step_ms

    if verbose:
        print(f"[ROLLING] Testing {len(start_times)} challenge windows "
              f"(every {window_step_days} days)...")

    target_balance = initial_capital * (1.0 + profit_target_pct / 100.0)
    daily_dd_limit = initial_capital * daily_dd_limit_pct / 100.0
    max_dd_limit = initial_capital * max_dd_limit_pct / 100.0

    passed = 0
    failed_daily = 0
    failed_max = 0
    days_to_pass_list = []

    import bisect
    cycle_entry_times = [c.entry_time_ms for c in cycles]

    for st in start_times:
        acct = initial_capital
        peak = initial_capital
        current_day = ""
        day_start_bal = initial_capital
        start_exit_ts = None

        result = "TIMEOUT"  # Default if we run out of cycles

        start_c_idx = bisect.bisect_left(cycle_entry_times, st)
        for c_idx in range(start_c_idx, len(cycles)):
            c = cycles[c_idx]

            exit_date = ms_to_date(c.exit_time_ms)
            if start_exit_ts is None:
                start_exit_ts = c.exit_time_ms

            if exit_date != current_day:
                current_day = exit_date
                day_start_bal = acct

            acct += c.combined_net_pnl

            # Daily DD check
            daily_loss = day_start_bal - acct
            if daily_loss >= daily_dd_limit:
                result = "FAIL_DAILY_DD"
                break

            # Trailing DD check
            if acct > peak:
                peak = acct
            trailing_dd = peak - acct
            if trailing_dd >= max_dd_limit:
                result = "FAIL_MAX_DD"
                break

            # Target check
            if acct >= target_balance:
                result = "PASS"
                days_taken = (c.exit_time_ms - st) / (1000.0 * 86400.0)
                days_to_pass_list.append(days_taken)
                break

        if result == "PASS":
            passed += 1
        elif result == "FAIL_DAILY_DD":
            failed_daily += 1
        elif result == "FAIL_MAX_DD":
            failed_max += 1

    total = len(start_times)
    pass_rate = (passed / total * 100.0) if total > 0 else 0.0
    avg_days = sum(days_to_pass_list) / len(days_to_pass_list) if days_to_pass_list else 0.0

    result = {
        "windows_tested": total,
        "passed": passed,
        "failed_daily_dd": failed_daily,
        "failed_max_dd": failed_max,
        "timed_out": total - passed - failed_daily - failed_max,
        "pass_rate_pct": round(pass_rate, 2),
        "avg_days_to_pass": round(avg_days, 1),
        "median_days_to_pass": round(sorted(days_to_pass_list)[len(days_to_pass_list)//2], 1) if days_to_pass_list else 0.0,
    }

    if verbose:
        print(f"[ROLLING] Results: {passed}/{total} passed ({pass_rate:.1f}%), "
              f"avg {avg_days:.1f} days, "
              f"fail_daily={failed_daily}, fail_max={failed_max}")

    return result
