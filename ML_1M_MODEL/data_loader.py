"""
Data Loader & Downloader for 1-Minute Crypto Futures
===================================================
Handles seamless ingestion from:
1. Local directories on user's machine (D:\\My_Bots\\Trading\\BINANCE_DATA\\...)
2. Local repository cache (data/...)
3. Automated on-demand download from Binance Vision archives (for GitHub Actions)
"""

import os
import io
import re
import glob
import zipfile
import urllib.request
import datetime
from typing import List, Tuple, Optional
import pandas as pd

from .config import (
    LOCAL_OHLCV_DIR,
    LOCAL_TRADES_DIR,
    CLOUD_OHLCV_DIR,
    CLOUD_TRADES_DIR,
)

BINANCE_VISION_BASE = "https://data.binance.vision/data/futures/um/monthly"


def normalize_symbol_name(symbol: str) -> str:
    """Normalizes symbol representations (e.g. 'TRUMP_USDT' -> 'TRUMPUSDT')."""
    return symbol.upper().replace("-", "").replace("_", "")


def generate_month_tuples(start_date: str, end_date: str) -> List[Tuple[int, int]]:
    """Generates a list of (year, month) tuples between start_date and end_date."""
    s_dt = datetime.datetime.strptime(start_date[:10], "%Y-%m-%d")
    e_dt = datetime.datetime.strptime(end_date[:10], "%Y-%m-%d")

    months = []
    curr = datetime.datetime(s_dt.year, s_dt.month, 1)
    end = datetime.datetime(e_dt.year, e_dt.month, 1)

    while curr <= end:
        months.append((curr.year, curr.month))
        next_m = curr.month + 1 if curr.month < 12 else 1
        next_y = curr.year if curr.month < 12 else curr.year + 1
        curr = datetime.datetime(next_y, next_m, 1)

    return months


def download_zip_from_binance(url: str, extract_to: str, expected_csv_name: str) -> bool:
    """Downloads a zip from Binance Vision and extracts the CSV."""
    os.makedirs(extract_to, exist_ok=True)
    target_csv = os.path.join(extract_to, expected_csv_name)
    if os.path.exists(target_csv) and os.path.getsize(target_csv) > 0:
        return True

    print(f"[DataLoader] Downloading archive from {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            if resp.status != 200:
                print(f"[!] HTTP error {resp.status} for {url}")
                return False
            data = resp.read()

        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(extract_to)

        if os.path.exists(target_csv):
            print(f"[+] Downloaded & extracted {expected_csv_name} ({os.path.getsize(target_csv)/(1024*1024):.2f} MB)")
            return True
        return False
    except Exception as e:
        print(f"[!] Warning: Failed to download archive {url}: {e}")
        return False


def get_ohlcv_file_path(symbol: str, year: int, month: int, auto_download: bool = True) -> Optional[str]:
    """
    Finds or downloads the 1m OHLCV CSV file for the given symbol and year-month.
    Checks:
    1. User's D:\\ drive path
    2. Cloud fallback directory (data/binance_futures_ohlcv/...)
    3. Downloads from Binance Vision if requested
    """
    sym = normalize_symbol_name(symbol)
    m_str = f"{month:02d}"
    expected_filename = f"{sym}-1m-{year}-{m_str}.csv"

    # 1. Check local D:\ drive
    local_path = os.path.join(LOCAL_OHLCV_DIR, sym, "1m", expected_filename)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return local_path

    # 2. Check cloud / repo path
    cloud_dir = os.path.join(CLOUD_OHLCV_DIR, sym, "1m")
    cloud_path = os.path.join(cloud_dir, expected_filename)
    if os.path.exists(cloud_path) and os.path.getsize(cloud_path) > 0:
        return cloud_path

    # 3. Download from Binance Vision if permitted
    if auto_download:
        url = f"{BINANCE_VISION_BASE}/klines/{sym}/1m/{sym}-1m-{year}-{m_str}.zip"
        success = download_zip_from_binance(url, cloud_dir, expected_filename)
        if success and os.path.exists(cloud_path):
            return cloud_path

    return None


def get_trades_file_path(symbol: str, year: int, month: int, auto_download: bool = True) -> Optional[str]:
    """
    Finds or downloads the tick trades CSV file for the given symbol and year-month.
    Checks:
    1. User's D:\\ drive path
    2. Cloud fallback directory (data/binance_futures_trades/...)
    3. Downloads from Binance Vision if requested
    """
    sym = normalize_symbol_name(symbol)
    m_str = f"{month:02d}"
    expected_filename = f"{sym}-trades-{year}-{m_str}.csv"

    # 1. Check local D:\ drive
    local_path = os.path.join(LOCAL_TRADES_DIR, sym, expected_filename)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return local_path

    # 2. Check cloud / repo path
    cloud_dir = os.path.join(CLOUD_TRADES_DIR, sym)
    cloud_path = os.path.join(cloud_dir, expected_filename)
    if os.path.exists(cloud_path) and os.path.getsize(cloud_path) > 0:
        return cloud_path

    # 3. Download from Binance Vision if permitted
    if auto_download:
        url = f"{BINANCE_VISION_BASE}/trades/{sym}/{sym}-trades-{year}-{m_str}.zip"
        success = download_zip_from_binance(url, cloud_dir, expected_filename)
        if success and os.path.exists(cloud_path):
            return cloud_path

    return None


def load_ohlcv_range(
    symbol: str,
    start_date: str,
    end_date: str,
    auto_download: bool = True
) -> pd.DataFrame:
    """
    Loads 1-minute OHLCV candles for the requested symbol across the date range.
    Returns a sorted DataFrame with datetime index.
    """
    sym = normalize_symbol_name(symbol)
    months = generate_month_tuples(start_date, end_date)
    dfs = []

    standard_cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "count", "taker_buy_volume",
        "taker_buy_quote_volume", "ignore"
    ]

    for y, m in months:
        path = get_ohlcv_file_path(sym, y, m, auto_download=auto_download)
        if path is None:
            print(f"[DataLoader] Notice: 1m OHLCV file not found for {sym} {y}-{m:02d}")
            continue

        try:
            # Check header
            first_line = pd.read_csv(path, nrows=1)
            has_header = "open_time" in first_line.columns or "open" in first_line.columns
            if has_header:
                df_month = pd.read_csv(path)
            else:
                df_month = pd.read_csv(path, names=standard_cols)

            dfs.append(df_month)
        except Exception as e:
            print(f"[!] Error loading {path}: {e}")

    if not dfs:
        raise FileNotFoundError(
            f"No 1m OHLCV files found for symbol {symbol} between {start_date} and {end_date}."
        )

    df_full = pd.concat(dfs, ignore_index=True)

    # Standardize column naming
    rename_dict = {
        "open_time": "timestamp",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "quote_volume": "quote_volume",
        "count": "trades_count",
        "taker_buy_volume": "taker_buy_volume",
        "taker_buy_quote_volume": "taker_buy_quote_volume"
    }
    df_full = df_full.rename(columns={k: v for k, v in rename_dict.items() if k in df_full.columns})

    # Numeric conversion
    numeric_cols = ["timestamp", "open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        if col in df_full.columns:
            df_full[col] = pd.to_numeric(df_full[col], errors="coerce")

    # Drop invalid rows and duplicate timestamps
    df_full = df_full.dropna(subset=["timestamp", "close"])
    df_full["timestamp"] = df_full["timestamp"].astype("int64")
    df_full = df_full.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    # Date filtering with strict UTC timezone enforcement
    s_ts = int(datetime.datetime.strptime(start_date[:10], "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    e_ts = int(datetime.datetime.strptime(end_date[:10] + " 23:59:59", "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)

    df_filtered = df_full[(df_full["timestamp"] >= s_ts) & (df_full["timestamp"] <= e_ts)].reset_index(drop=True)
    df_filtered["datetime"] = pd.to_datetime(df_filtered["timestamp"], unit="ms", utc=True)

    print(f"[DataLoader] Successfully loaded {len(df_filtered)} 1m candles for {sym} ({start_date} to {end_date} UTC)")
    return df_filtered
