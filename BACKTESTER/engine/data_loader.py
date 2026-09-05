"""
High-Performance Dual-Feed Data Loader
======================================
Provides streaming and indexed access to:
1. OHLCV candlestick data across dynamic timeframes (1m, 5m, 1h, 1d, etc.)
2. Millisecond-level historical tick trades with binary-seek fast-forwarding
"""

import os
import csv
import glob
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Generator, Tuple, Union

from BACKTESTER.engine.scanner import canonicalize_symbol, parse_timestamp_ms


# Timeframe mapping between Binance folder names and KCEX interval constants
TIMEFRAME_MAP = {
    "1m": "Min1",
    "min1": "1m",
    "3m": "Min3",
    "min3": "3m",
    "5m": "Min5",
    "min5": "5m",
    "15m": "Min15",
    "min15": "15m",
    "30m": "Min30",
    "min30": "30m",
    "1h": "Min60",
    "60m": "1h",
    "min60": "1h",
    "hour1": "1h",
    "2h": "Hour2",
    "hour2": "2h",
    "4h": "Hour4",
    "hour4": "4h",
    "6h": "Hour6",
    "hour6": "6h",
    "8h": "Hour8",
    "hour8": "8h",
    "12h": "Hour12",
    "hour12": "12h",
    "1d": "Day1",
    "day1": "1d",
    "d1": "1d"
}


def normalize_timeframe(tf: str) -> str:
    """Normalizes timeframe to folder key (e.g. 'Min1' -> '1m', '1M' -> '1m')."""
    s = tf.strip().lower()
    if s in TIMEFRAME_MAP:
        mapped = TIMEFRAME_MAP[s].lower()
        if mapped in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"):
            return mapped
    return s


def timeframe_to_kcex_interval(tf: str) -> str:
    """Converts a timeframe string (e.g. '1m') into KCEX interval constant (e.g. 'Min1')."""
    s = tf.strip().lower()
    return TIMEFRAME_MAP.get(s, "Min1")


@dataclass
class Candle:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time_ms: int
    quote_volume: float = 0.0
    trades_count: int = 0

    @property
    def timestamp_sec(self) -> int:
        return int(self.open_time_ms / 1000)

    def to_kcex_dict(self) -> Dict[str, Any]:
        """Converts to dictionary structure expected by KCEXMarket and strategies."""
        return {
            "timestamp": self.timestamp_sec,
            "timestamp_ms": self.open_time_ms,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "vol": self.volume,
            "volume": self.volume,
            "amount": self.quote_volume,
            "close_time": self.close_time_ms
        }


@dataclass
class TradeTick:
    trade_id: int
    price: float
    qty: float
    quote_qty: float
    timestamp_ms: int
    is_buyer_maker: bool


def find_byte_offset_for_timestamp(file_path: str, target_ms: int, ts_col_idx: int = 4) -> int:
    """
    Performs binary search on file byte offsets to quickly find where target_ms begins.
    Enables jumping directly to a timestamp in 1.5+ GB files in a few milliseconds.
    """
    file_size = os.path.getsize(file_path)
    if file_size < 4096:
        return 0

    low = 0
    high = file_size
    best_offset = 0

    with open(file_path, "rb") as f:
        # Check first record after header
        f.readline() # header
        first_record_pos = f.tell()

        while low < high:
            mid = (low + high) // 2
            f.seek(mid)
            # Discard partial line
            f.readline()
            curr_pos = f.tell()
            line = f.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                high = mid
                continue

            parts = line.split(",")
            if len(parts) <= ts_col_idx:
                high = mid
                continue

            try:
                ts = int(float(parts[ts_col_idx]))
            except ValueError:
                high = mid
                continue

            if ts < target_ms:
                best_offset = curr_pos
                low = mid + 1
            else:
                high = mid

    return max(first_record_pos, best_offset)


class OHLCVLoader:
    """
    Loads and streams candlestick data from BACKTESTER/OHLCV_Data_Binance.
    """

    def __init__(self, data_dir: str = os.path.join("BACKTESTER", "OHLCV_Data_Binance")):
        self.data_dir = data_dir

    def resolve_symbol_path(self, symbol: str) -> Optional[str]:
        """Resolves folder path regardless of underscore variations (TRUMPUSDT or TRUMP_USDT)."""
        clean = symbol.strip().upper()
        no_us = clean.replace("_", "")
        with_us = canonicalize_symbol(clean)

        candidates = [with_us, no_us, clean]
        for c in candidates:
            p = os.path.join(self.data_dir, c)
            if os.path.isdir(p):
                return p
        return None

    def get_candle_files(self, symbol: str, timeframe: str) -> List[str]:
        """Returns sorted list of CSV file paths for the given symbol and timeframe."""
        sym_dir = self.resolve_symbol_path(symbol)
        if not sym_dir:
            return []

        norm_tf = normalize_timeframe(timeframe)
        tf_dir = os.path.join(sym_dir, norm_tf)
        if not os.path.isdir(tf_dir):
            return []

        return sorted(glob.glob(os.path.join(tf_dir, "*.csv")))

    def load_candles(
        self,
        symbol: str,
        timeframe: str,
        start_ms: Optional[int] = None,
        end_ms: Optional[int] = None
    ) -> List[Candle]:
        """Loads candles into memory for the requested interval."""
        files = self.get_candle_files(symbol, timeframe)
        candles: List[Candle] = []

        import re
        import datetime

        for fpath in files:
            # Fast month filtering from filename: e.g. TRUMPUSDT-1m-2025-01.csv
            m = re.search(r'(\d{4})-(\d{2})', os.path.basename(fpath))
            if m and (start_ms or end_ms):
                year, month = int(m.group(1)), int(m.group(2))
                # Start of this month in UTC ms
                file_month_start_dt = datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc)
                file_month_start_ms = int(file_month_start_dt.timestamp() * 1000)
                # Next month start
                next_month = month + 1 if month < 12 else 1
                next_year = year if month < 12 else year + 1
                file_month_end_dt = datetime.datetime(next_year, next_month, 1, tzinfo=datetime.timezone.utc)
                file_month_end_ms = int(file_month_end_dt.timestamp() * 1000)

                if start_ms and file_month_end_ms <= start_ms:
                    continue
                if end_ms and file_month_start_ms > end_ms:
                    continue

            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    continue

                for row in reader:
                    if len(row) < 6:
                        continue
                    try:
                        open_time = int(float(row[0]))
                        if start_ms and open_time < start_ms:
                            continue
                        if end_ms and open_time > end_ms:
                            break

                        o = float(row[1])
                        h = float(row[2])
                        l = float(row[3])
                        c = float(row[4])
                        v = float(row[5])
                        close_time = int(float(row[6])) if len(row) > 6 else (open_time + 59999)
                        qv = float(row[7]) if len(row) > 7 else 0.0
                        tc = int(float(row[8])) if len(row) > 8 else 0

                        candles.append(Candle(
                            open_time_ms=open_time,
                            open=o,
                            high=h,
                            low=l,
                            close=c,
                            volume=v,
                            close_time_ms=close_time,
                            quote_volume=qv,
                            trades_count=tc
                        ))
                    except (ValueError, IndexError):
                        continue

        # Sort just in case of any overlap between monthly files
        candles.sort(key=lambda c: c.open_time_ms)
        return candles


class TickTradeStreamer:
    """
    Streams historical tick-by-tick trades from BACKTESTER/Historical_Trades_Data_Binance.
    Utilizes binary-seek to jump directly to entry timestamps without reading
    millions of past rows.
    """

    def __init__(self, data_dir: str = os.path.join("BACKTESTER", "Historical_Trades_Data_Binance")):
        self.data_dir = data_dir

    def resolve_symbol_path(self, symbol: str) -> Optional[str]:
        """Resolves folder path regardless of underscore variations."""
        clean = symbol.strip().upper()
        no_us = clean.replace("_", "")
        with_us = canonicalize_symbol(clean)

        candidates = [with_us, no_us, clean]
        for c in candidates:
            p = os.path.join(self.data_dir, c)
            if os.path.isdir(p):
                return p
        return None

    def get_trade_files(self, symbol: str) -> List[str]:
        """Returns sorted list of CSV file paths for the given symbol."""
        sym_dir = self.resolve_symbol_path(symbol)
        if not sym_dir:
            return []
        return sorted(glob.glob(os.path.join(sym_dir, "*.csv")))

    def stream_ticks(
        self,
        symbol: str,
        start_ms: int,
        end_ms: Optional[int] = None
    ) -> Generator[TradeTick, None, None]:
        """
        Yields TradeTick instances chronologically starting from start_ms up to end_ms.
        Uses binary offset seek to start reading exactly around start_ms.
        """
        files = self.get_trade_files(symbol)
        if not files:
            return

        for fpath in files:
            file_size = os.path.getsize(fpath)
            if file_size == 0:
                continue

            # Determine whether this file covers our target time range
            # Check last timestamp of the file
            _, file_last_ts = self._get_file_last_ts(fpath)
            if file_last_ts and file_last_ts < start_ms:
                # File is entirely in the past, skip
                continue

            _, file_first_ts = self._get_file_first_ts(fpath)
            if end_ms and file_first_ts and file_first_ts > end_ms:
                # File is entirely in the future, stop
                break

            # Find fast binary seek offset
            offset = find_byte_offset_for_timestamp(fpath, start_ms, ts_col_idx=4)

            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(offset)
                # Discard partial line if we seeked past 0
                if offset > 0:
                    f.readline()

                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 6:
                        continue
                    try:
                        t = int(float(row[4]))
                        if t < start_ms:
                            continue
                        if end_ms and t > end_ms:
                            return

                        tid = int(float(row[0]))
                        p = float(row[1])
                        q = float(row[2])
                        qq = float(row[3]) if len(row) > 3 else (p * q)
                        ibm = (str(row[5]).strip().lower() == "true")

                        yield TradeTick(
                            trade_id=tid,
                            price=p,
                            qty=q,
                            quote_qty=qq,
                            timestamp_ms=t,
                            is_buyer_maker=ibm
                        )
                    except (ValueError, IndexError):
                        continue

    def _get_file_first_ts(self, csv_path: str) -> Tuple[bool, Optional[int]]:
        try:
            with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
                f.readline()
                line = f.readline()
                if line:
                    parts = line.strip().split(",")
                    if len(parts) > 4:
                        return True, int(float(parts[4]))
        except Exception:
            pass
        return False, None

    def _get_file_last_ts(self, csv_path: str) -> Tuple[bool, Optional[int]]:
        try:
            sz = os.path.getsize(csv_path)
            with open(csv_path, "rb") as f:
                read_sz = min(2048, sz)
                f.seek(sz - read_sz)
                chunk = f.read(read_sz).decode("utf-8", errors="ignore")
                lines = [l.strip() for l in chunk.split("\n") if l.strip()]
                if lines:
                    parts = lines[-1].split(",")
                    if len(parts) > 4:
                        return True, int(float(parts[4]))
        except Exception:
            pass
        return False, None
