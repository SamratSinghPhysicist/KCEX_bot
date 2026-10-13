"""
Binance Vision Downloader for BTC and ETH Reverse Trading Experiment
===================================================================
Downloads monthly OHLCV klines (1m, 5m, 15m, 1h, 4h, 1d) for BTCUSDT and ETHUSDT
from Binance Vision (https://data.binance.vision/data/futures/um/monthly/klines/).
"""

from __future__ import annotations
import os
import io
import zipfile
import urllib.request
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

BINANCE_VISION_BASE = "https://data.binance.vision/data/futures/um/monthly/klines"


def generate_month_list(start_date_str: str, end_date_str: str) -> List[Tuple[int, int]]:
    """Generates a list of (year, month) tuples between start and end date strings (YYYY-MM-DD)."""
    s_dt = datetime.datetime.strptime(start_date_str[:10], "%Y-%m-%d")
    e_dt = datetime.datetime.strptime(end_date_str[:10], "%Y-%m-%d")

    months = []
    curr = datetime.datetime(s_dt.year, s_dt.month, 1)
    end = datetime.datetime(e_dt.year, e_dt.month, 1)

    while curr <= end:
        months.append((curr.year, curr.month))
        next_m = curr.month + 1 if curr.month < 12 else 1
        next_y = curr.year if curr.month < 12 else curr.year + 1
        curr = datetime.datetime(next_y, next_m, 1)

    return months


def download_single_month(
    symbol: str,
    timeframe: str,
    year: int,
    month: int,
    dest_dir: str
) -> Tuple[str, bool, str]:
    """Downloads and extracts a single monthly zip archive from Binance Vision."""
    ym_str = f"{year:04d}-{month:02d}"
    expected_csv = f"{symbol}-{timeframe}-{ym_str}.csv"
    csv_path = os.path.join(dest_dir, expected_csv)

    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 100:
        return (expected_csv, True, "Already exists")

    os.makedirs(dest_dir, exist_ok=True)
    zip_filename = f"{symbol}-{timeframe}-{ym_str}.zip"
    url = f"{BINANCE_VISION_BASE}/{symbol}/{timeframe}/{zip_filename}"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return (expected_csv, False, f"HTTP {resp.status}")
            zip_bytes = resp.read()

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.extractall(dest_dir)

        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 100:
            return (expected_csv, True, f"Downloaded ({os.path.getsize(csv_path)/1024:.1f} KB)")
        else:
            return (expected_csv, True, "Extracted archive contents")
    except urllib.error.HTTPError as e:
        return (expected_csv, False, f"HTTP {e.code}")
    except Exception as e:
        return (expected_csv, False, str(e))


def download_experiment_data(
    symbols: List[str] = ["BTCUSDT", "ETHUSDT"],
    timeframes: List[str] = ["1m", "5m", "15m", "1h", "4h", "1d"],
    start_date: str = "2025-01-01",
    end_date: str = "2026-08-31",
    base_data_dir: str = "BACKTESTER/OHLCV_Data_Binance",
    max_workers: int = 8,
    verbose: bool = True
) -> bool:
    """Downloads all requested monthly OHLCV archives concurrently."""
    months = generate_month_list(start_date, end_date)
    tasks = []

    for sym in symbols:
        sym_clean = sym.replace("_", "").upper()
        for tf in timeframes:
            dest = os.path.join(base_data_dir, sym_clean, tf)
            for y, m in months:
                tasks.append((sym_clean, tf, y, m, dest))

    if verbose:
        print(f"[*] Starting download check for {len(tasks)} dataset slices ({len(symbols)} symbols, {len(timeframes)} TFs, {len(months)} months)...")

    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(download_single_month, sym, tf, y, m, dest): (sym, tf, y, m)
            for sym, tf, y, m, dest in tasks
        }
        for future in as_completed(future_map):
            sym, tf, y, m = future_map[future]
            try:
                name, ok, msg = future.result()
                if ok:
                    success_count += 1
                else:
                    fail_count += 1
                    if verbose:
                        print(f"  [!] Failed {sym} {tf} {y:04d}-{m:02d}: {msg}")
            except Exception as e:
                fail_count += 1
                if verbose:
                    print(f"  [!] Exception on {sym} {tf} {y:04d}-{m:02d}: {e}")

    if verbose:
        print(f"[*] Data download check complete: {success_count} OK, {fail_count} Failed.")
    return fail_count == 0


if __name__ == "__main__":
    download_experiment_data()
