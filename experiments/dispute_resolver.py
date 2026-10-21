"""
High-Performance 1-Minute Dispute Resolver for No-Stop-Loss Backtests
=====================================================================
Resolves intra-candle execution sequence for higher-timeframe candles (>= 5m)
using chronological 1-minute OHLCV bars.

Adversarial Resolution Rules:
1. When checking candidate levels (e.g. TP2 vs BE Stop, or TP1 vs hypothetical SL):
   - Walk minute-by-minute (0 to end of higher timeframe window).
   - If within the SAME 1-minute candle both levels are breached:
     DECLARE STOP / BREAKEVEN! (Conservative pessimistic tie-breaker).
   - If level A is breached in minute m before level B:
     DECLARE level A!
2. Missing data fallback:
   - Conservative fallback: declares STOP / BREAKEVEN.
"""

from __future__ import annotations
import os
import glob
import bisect
import datetime
from collections import OrderedDict
from typing import List, Dict, Tuple, Optional, Any


class OneMinuteDisputeResolver:
    """
    High-Speed LRU-cached 1-minute OHLCV dispute resolver.
    Caches 1m candles by (symbol, year_month) to resolve disputes in microseconds.
    """
    def __init__(self, crypto_dir: str, stocks_dir: str, max_cached_months: int = 24):
        self.crypto_dir = crypto_dir
        self.stocks_dir = stocks_dir
        self.max_cached_months = max_cached_months
        # cache key: (symbol, ym) -> (timestamps_list, candles_list)
        # each candle: (open_time_ms, open, high, low, close)
        self.month_cache: OrderedDict[Tuple[str, str], Tuple[List[int], List[Tuple[int, float, float, float, float]]]] = OrderedDict()
        # Single full-file cache: symbol -> (timestamps_list, candles_list)
        self.full_file_cache: Dict[str, Tuple[List[int], List[Tuple[int, float, float, float, float]]]] = {}
        self.missing_keys: set = set()

    def _load_single_csv(self, filepath: str) -> Tuple[List[int], List[Tuple[int, float, float, float, float]]]:
        timestamps: List[int] = []
        candles: List[Tuple[int, float, float, float, float]] = []
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    p = line.split(",")
                    if len(p) >= 5:
                        try:
                            ot = int(float(p[0]))
                            o = float(p[1])
                            h = float(p[2])
                            l = float(p[3])
                            c = float(p[4])
                            timestamps.append(ot)
                            candles.append((ot, o, h, l, c))
                        except (ValueError, TypeError):
                            continue
        except Exception:
            pass
        return timestamps, candles

    def _get_month_data(self, symbol: str, start_ms: int) -> Tuple[List[int], List[Tuple[int, float, float, float, float]]]:
        sym = symbol.upper().strip()
        dt = datetime.datetime.fromtimestamp(start_ms / 1000.0, tz=datetime.timezone.utc)
        ym = dt.strftime("%Y-%m")
        key = (sym, ym)

        if key in self.month_cache:
            self.month_cache.move_to_end(key)
            return self.month_cache[key]

        if key in self.missing_keys:
            return ([], [])

        # 1. Check if full single 1m.csv exists in crypto or stocks directory
        if sym in self.full_file_cache:
            return self.full_file_cache[sym]

        full_crypto = os.path.join(self.crypto_dir, sym, "1m.csv")
        full_stocks = os.path.join(self.stocks_dir, sym, "1m.csv")
        full_gold = os.path.join(self.stocks_dir, "GOLD", "1m.csv") if sym == "GC=F" else None

        for fp in [full_crypto, full_stocks, full_gold]:
            if fp and os.path.isfile(fp) and os.path.getsize(fp) > 1000:
                ts, cs = self._load_single_csv(fp)
                if ts:
                    self.full_file_cache[sym] = (ts, cs)
                    return (ts, cs)

        # 2. Check monthly Binance Vision archives
        binance_sym = f"{sym}USDT"
        binance_1m_dir = os.path.join(os.path.dirname(self.crypto_dir), "OHLCV_Data_Binance", binance_sym, "1m")
        monthly_file = os.path.join(binance_1m_dir, f"{binance_sym}-1m-{ym}.csv")

        if os.path.isfile(monthly_file) and os.path.getsize(monthly_file) > 100:
            ts, cs = self._load_single_csv(monthly_file)
            if len(self.month_cache) >= self.max_cached_months:
                self.month_cache.popitem(last=False)
            self.month_cache[key] = (ts, cs)
            return (ts, cs)

        # No data found for this month; cache as missing
        self.missing_keys.add(key)
        return ([], [])

    def get_1m_slice(self, symbol: str, start_ms: int, end_ms: int) -> List[Tuple[int, float, float, float, float]]:
        """Returns chronological 1m candles spanning [start_ms, end_ms]."""
        timestamps, candles = self._get_month_data(symbol, start_ms)
        if not timestamps:
            return []

        idx_start = bisect.bisect_left(timestamps, start_ms)
        idx_end = bisect.bisect_right(timestamps, end_ms)
        return candles[idx_start:idx_end]

    def resolve_tp1_vs_hypothetical_sl(
        self,
        symbol: str,
        direction: str,
        start_ms: int,
        end_ms: int,
        tp1_price: float,
        sl_price: float
    ) -> Tuple[str, float, int]:
        """
        Resolves whether TP1 or hypothetical SL was breached first chronologically.
        Returns: (winner, exit_price, timestamp_ms) where winner in ("TP1", "SL")
        """
        sub_candles = self.get_1m_slice(symbol, start_ms, end_ms)
        if not sub_candles:
            return ("SL", sl_price, start_ms)

        for (ot, o, h, l, c) in sub_candles:
            if direction == "LONG":
                hit_tp1 = (h >= tp1_price)
                hit_sl = (l <= sl_price)
            else:
                hit_tp1 = (l <= tp1_price)
                hit_sl = (h >= sl_price)

            if hit_tp1 and hit_sl:
                # Conservative dispute rule: ties declare SL
                return ("SL", sl_price, ot)
            elif hit_sl:
                return ("SL", sl_price, ot)
            elif hit_tp1:
                return ("TP1", tp1_price, ot)

        return ("SL", sl_price, start_ms)

    def resolve_runner_tp2_vs_be(
        self,
        symbol: str,
        direction: str,
        start_ms: int,
        end_ms: int,
        tp2_price: float,
        be_price: float
    ) -> Tuple[str, float, int]:
        """
        Resolves whether TP2 or Breakeven Stop was breached first chronologically.
        Returns: (winner, exit_price, timestamp_ms) where winner in ("TP2", "BE_STOP")
        """
        sub_candles = self.get_1m_slice(symbol, start_ms, end_ms)
        if not sub_candles:
            return ("BE_STOP", be_price, start_ms)

        for (ot, o, h, l, c) in sub_candles:
            if direction == "LONG":
                hit_tp2 = (h >= tp2_price)
                hit_be = (l <= be_price)
            else:
                hit_tp2 = (l <= tp2_price)
                hit_be = (h >= be_price)

            if hit_tp2 and hit_be:
                # Conservative dispute rule: ties declare BE STOP
                return ("BE_STOP", be_price, ot)
            elif hit_be:
                return ("BE_STOP", be_price, ot)
            elif hit_tp2:
                return ("TP2", tp2_price, ot)

        return ("BE_STOP", be_price, start_ms)
