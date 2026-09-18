#!/usr/bin/env python3
"""
Binance Vision to Google Drive Archiver
=======================================
High-speed, resilient archiver for streaming/uploading official Binance Vision
historical USD-M futures market data directly to Google Drive.

Key Features:
- Zero Persistent Local Disk Usage: Downloads each file to a temporary location,
  immediately uploads it to Google Drive, and deletes the local copy.
- Idempotent & Resumable: Scans Google Drive directory to skip already-uploaded archives.
- Complete Data Type & Subtype Support:
  - Kline Types (all timeframes): klines, markPriceKlines, indexPriceKlines, premiumIndexKlines
  - Direct Types: trades, aggTrades, bookTicker, fundingRate
- Shortlisted Pairs + Majors by default, with arbitrary custom symbol support.
"""

import os
import sys
import time
import shutil
import argparse
import tempfile
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import requests

# Default list of major symbols to include alongside the shortlisted pairs
DEFAULT_MAJOR_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "TRUMPUSDT"]

# Supported Data Types
ALL_KLINE_TYPES = ["klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
ALL_DIRECT_TYPES = ["trades", "aggTrades", "bookTicker", "fundingRate"]
ALL_DATA_TYPES = ALL_KLINE_TYPES + ALL_DIRECT_TYPES

# Standard Kline Timeframes on Binance Vision
ALL_TIMEFRAMES = [
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "6h", "8h", "12h",
    "1d", "3d", "1w", "1mo"
]

# S3 Bucket URL for Binance Vision
BINANCE_S3_BUCKET = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
BINANCE_DATA_BASE_URL = "https://data.binance.vision"


def get_shortlisted_symbols(csv_path: Optional[str] = None) -> List[str]:
    """Reads shortlisted binance symbols from the generated CSV file."""
    if not csv_path:
        default_csv = Path(__file__).resolve().parent.parent / "Network_logs_by_codex" / "ALL_PAIRS_DETAILS_18Sep2026" / "SHORTLISTED_kcex_shortlisted_pairs.csv"
        csv_path = str(default_csv)

    symbols = []
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        if "binance_symbol" in df.columns:
            symbols = [str(s).strip() for s in df["binance_symbol"].dropna().tolist()]
        elif "symbol" in df.columns:
            symbols = [str(s).replace("_", "").strip() for s in df["symbol"].dropna().tolist()]
    return list(dict.fromkeys(symbols))


def list_s3_keys_with_prefix(prefix: str, max_retries: int = 4) -> List[str]:
    """Lists all S3 keys matching a prefix using AWS S3 XML ListObjects API."""
    keys = []
    marker = ""
    session = requests.Session()
    session.headers.update({"User-Agent": "BinanceVisionArchiver/1.0"})

    while True:
        url = f"{BINANCE_S3_BUCKET}?prefix={prefix}"
        if marker:
            url += f"&marker={marker}"

        for attempt in range(1, max_retries + 1):
            try:
                r = session.get(url, timeout=12)
                if r.status_code == 200:
                    root = ET.fromstring(r.text)
                    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
                    page_keys = [
                        elem.text for elem in root.findall(".//s3:Contents/s3:Key", ns)
                        if elem.text and elem.text.endswith(".zip")
                    ]
                    keys.extend(page_keys)

                    is_truncated_elem = root.find(".//s3:IsTruncated", ns)
                    is_truncated = is_truncated_elem is not None and is_truncated_elem.text.lower() == "true"
                    if is_truncated and page_keys:
                        marker = page_keys[-1]
                        break
                    else:
                        return keys
                elif r.status_code == 404:
                    return keys
                else:
                    time.sleep(1.5 * attempt)
            except Exception as e:
                if attempt == max_retries:
                    print(f"  [Warning] S3 request failed after {max_retries} attempts: {url} ({e})")
                    return keys
                time.sleep(1.5 * attempt)
        else:
            break

    return keys


def extract_month_from_key(key: str) -> Optional[str]:
    """Extracts YYYY-MM from a Binance archive S3 key."""
    fn = key.split("/")[-1]
    if not fn.endswith(".zip"):
        return None
    stem = fn[:-4]
    parts = stem.split("-")
    if len(parts) >= 2:
        y, m = parts[-2], parts[-1]
        if len(y) == 4 and y.isdigit() and len(m) == 2 and m.isdigit():
            return f"{y}-{m}"
    return None


class BinanceDriveArchiver:
    def __init__(
        self,
        rclone_remote: str = "gdrive",
        gdrive_folder: str = "Online/BINANCE_HISTORICAL_DATA (till August 2026)",
        market: str = "futures/um",
        temp_dir: Optional[str] = None,
        dry_run: bool = False
    ):
        self.rclone_remote = rclone_remote
        self.gdrive_folder = gdrive_folder.strip("/\\").replace("\\", "/")
        self.market = market
        self.temp_dir = temp_dir or tempfile.mkdtemp(prefix="binance_archive_")
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "BinanceVisionArchiver/1.0"})

        os.makedirs(self.temp_dir, exist_ok=True)
        self.existing_remote_files: Dict[str, Set[str]] = {}
        self._rclone_checked = False

    def check_rclone_available(self) -> bool:
        possible_bins = [
            "rclone",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.75.1-windows-amd64\rclone.exe")
        ]
        for cmd in possible_bins:
            try:
                res = subprocess.run([cmd, "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if res.returncode == 0:
                    self._rclone_checked = True
                    self.rclone_bin = cmd
                    return True
            except (FileNotFoundError, OSError):
                pass
        return False

    def get_existing_remote_filenames(self, remote_subfolder: str) -> Set[str]:
        if self.dry_run or not self._rclone_checked:
            return set()

        if remote_subfolder in self.existing_remote_files:
            return self.existing_remote_files[remote_subfolder]

        full_remote_path = f"{self.rclone_remote}:{self.gdrive_folder}/{remote_subfolder}".strip("/")
        bin_cmd = getattr(self, "rclone_bin", "rclone")
        try:
            res = subprocess.run(
                [bin_cmd, "lsf", full_remote_path, "--files-only"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            if res.returncode == 0:
                files = set(line.strip() for line in res.stdout.splitlines() if line.strip())
                self.existing_remote_files[remote_subfolder] = files
                return files
        except Exception:
            pass
        self.existing_remote_files[remote_subfolder] = set()
        return set()

    def discover_keys_for_symbol_and_type(
        self,
        symbol: str,
        data_type: str,
        timeframe: Optional[str] = None,
        start_month: Optional[str] = None,
        end_month: Optional[str] = None
    ) -> List[str]:
        if data_type in ALL_KLINE_TYPES:
            tf = timeframe or "1m"
            prefix = f"data/{self.market}/monthly/{data_type}/{symbol}/{tf}/"
        else:
            prefix = f"data/{self.market}/monthly/{data_type}/{symbol}/"

        keys = list_s3_keys_with_prefix(prefix)

        filtered_keys = []
        for k in keys:
            m = extract_month_from_key(k)
            if m:
                if start_month and m < start_month:
                    continue
                if end_month and m > end_month:
                    continue
            filtered_keys.append(k)

        return sorted(filtered_keys)

    def download_file_to_temp(self, s3_key: str, dest_path: str, max_retries: int = 4) -> bool:
        url = f"{BINANCE_DATA_BASE_URL}/{s3_key}"
        for attempt in range(1, max_retries + 1):
            try:
                with self.session.get(url, stream=True, timeout=30) as r:
                    if r.status_code == 200:
                        with open(dest_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=1024 * 512):
                                if chunk:
                                    f.write(chunk)
                        return True
                    elif r.status_code == 404:
                        return False
            except Exception as e:
                if attempt == max_retries:
                    print(f"  [Error] Failed to download {url}: {e}")
                    return False
                time.sleep(2 * attempt)
        return False

    def upload_temp_file_to_drive(self, local_path: str, remote_subfolder: str) -> bool:
        if self.dry_run:
            return True

        filename = os.path.basename(local_path)
        full_remote_path = f"{self.rclone_remote}:{self.gdrive_folder}/{remote_subfolder}/{filename}".replace("\\", "/")
        bin_cmd = getattr(self, "rclone_bin", "rclone")
        try:
            res = subprocess.run(
                [bin_cmd, "copyto", local_path, full_remote_path, "--retries", "3", "--low-level-retries", "10"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300
            )
            return res.returncode == 0
        except Exception as e:
            print(f"  [Error] rclone upload exception for {filename}: {e}")
            return False

    def sync_key_to_drive(self, s3_key: str) -> str:
        parts = s3_key.split("/")
        filename = parts[-1]

        if len(parts) >= 6 and parts[3] in ALL_KLINE_TYPES:
            remote_subfolder = f"{parts[4]}/{parts[5]}/{parts[6]}"
        elif len(parts) >= 5:
            remote_subfolder = f"{parts[4]}/{parts[5]}"
        else:
            remote_subfolder = "misc"

        existing_files = self.get_existing_remote_filenames(remote_subfolder)
        if filename in existing_files:
            return "skipped"

        if self.dry_run:
            return "uploaded"

        local_temp_file = os.path.join(self.temp_dir, filename)
        try:
            success = self.download_file_to_temp(s3_key, local_temp_file)
            if not success:
                return "error"

            upload_success = self.upload_temp_file_to_drive(local_temp_file, remote_subfolder)
            if upload_success:
                if remote_subfolder in self.existing_remote_files:
                    self.existing_remote_files[remote_subfolder].add(filename)
                return "uploaded"
            else:
                return "error"
        finally:
            if os.path.exists(local_temp_file):
                try:
                    os.remove(local_temp_file)
                except Exception:
                    pass

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception:
                pass


def run_archival_pipeline(
    symbols: List[str],
    data_types: List[str],
    timeframes: List[str],
    start_month: Optional[str] = None,
    end_month: Optional[str] = "2026-08",
    rclone_remote: str = "gdrive",
    gdrive_folder: str = "Online/BINANCE_HISTORICAL_DATA (till August 2026)",
    dry_run: bool = False
):
    archiver = BinanceDriveArchiver(
        rclone_remote=rclone_remote,
        gdrive_folder=gdrive_folder,
        dry_run=dry_run
    )

    if not dry_run:
        has_rclone = archiver.check_rclone_available()
        if not has_rclone:
            print("[Error] 'rclone' executable was not found on PATH. Please install and configure rclone.")
            sys.exit(1)

    print("=" * 80)
    print("BINANCE PUBLIC DATA VISION -> GOOGLE DRIVE ARCHIVER")
    print("=" * 80)
    print(f"Target Google Drive Folder : {gdrive_folder}")
    print(f"Remote Name                : {rclone_remote}")
    print(f"Dry Run Mode               : {dry_run}")
    print(f"Date Cutoff                : {start_month or 'Earliest'} -> {end_month or 'Latest'}")
    print(f"Total Symbols              : {len(symbols)} ({', '.join(symbols[:8])}{'...' if len(symbols)>8 else ''})")
    print(f"Data Types                 : {', '.join(data_types)}")
    print(f"Kline Timeframes           : {', '.join(timeframes)}")
    print("=" * 80)

    total_discovered = 0
    total_uploaded = 0
    total_skipped = 0
    total_errors = 0

    start_time = time.time()

    for s_idx, symbol in enumerate(symbols, 1):
        print(f"\n[{s_idx}/{len(symbols)}] Processing Symbol: {symbol}")
        sym_discovered = 0
        sym_uploaded = 0
        sym_skipped = 0

        for dt in data_types:
            if dt in ALL_KLINE_TYPES:
                for tf in timeframes:
                    keys = archiver.discover_keys_for_symbol_and_type(
                        symbol, dt, timeframe=tf, start_month=start_month, end_month=end_month
                    )
                    if not keys:
                        continue
                    sym_discovered += len(keys)
                    total_discovered += len(keys)
                    print(f"  -> {dt:<18} [{tf:<4}]: {len(keys)} files found", end="", flush=True)

                    up_count = 0
                    skip_count = 0
                    err_count = 0

                    for k in keys:
                        res = archiver.sync_key_to_drive(k)
                        if res == "uploaded":
                            up_count += 1
                        elif res == "skipped":
                            skip_count += 1
                        else:
                            err_count += 1

                    sym_uploaded += up_count
                    sym_skipped += skip_count
                    total_uploaded += up_count
                    total_skipped += skip_count
                    total_errors += err_count

                    status_str = f" | +{up_count} uploaded, {skip_count} existing"
                    if err_count:
                        status_str += f", {err_count} failed"
                    print(status_str)
            else:
                keys = archiver.discover_keys_for_symbol_and_type(
                    symbol, dt, start_month=start_month, end_month=end_month
                )
                if not keys:
                    continue
                sym_discovered += len(keys)
                total_discovered += len(keys)
                print(f"  -> {dt:<18}       : {len(keys)} files found", end="", flush=True)

                up_count = 0
                skip_count = 0
                err_count = 0

                for k in keys:
                    res = archiver.sync_key_to_drive(k)
                    if res == "uploaded":
                        up_count += 1
                    elif res == "skipped":
                        skip_count += 1
                    else:
                        err_count += 1

                sym_uploaded += up_count
                sym_skipped += skip_count
                total_uploaded += up_count
                total_skipped += skip_count
                total_errors += err_count

                status_str = f" | +{up_count} uploaded, {skip_count} existing"
                if err_count:
                    status_str += f", {err_count} failed"
                print(status_str)

    archiver.cleanup()

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("ARCHIVAL RUN SUMMARY")
    print("=" * 80)
    print(f"Total Archives Discovered : {total_discovered}")
    print(f"Successfully Uploaded     : {total_uploaded}")
    print(f"Skipped (Already in Drive): {total_skipped}")
    print(f"Errors                    : {total_errors}")
    print(f"Elapsed Time              : {elapsed/60:.2f} minutes")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Binance Vision Historical Data to Google Drive Archiver")
    parser.add_argument(
        "--symbols",
        type=str,
        default="ALL_TARGETED",
        help="Symbols mode: 'ALL_TARGETED' (shortlisted + majors), 'SHORTLISTED_ONLY', 'MAJORS_ONLY', or comma-separated list"
    )
    parser.add_argument(
        "--shortlisted-csv",
        type=str,
        default="",
        help="Path to SHORTLISTED_kcex_shortlisted_pairs.csv (defaults to auto-detect)"
    )
    parser.add_argument(
        "--data-types",
        type=str,
        default="ALL",
        help="Comma-separated data types (e.g. klines,trades,aggTrades,fundingRate) or 'ALL'"
    )
    parser.add_argument(
        "--timeframes",
        type=str,
        default="ALL",
        help="Comma-separated timeframes (e.g. 1m,5m,1h,1d) or 'ALL'"
    )
    parser.add_argument(
        "--start-month",
        type=str,
        default=None,
        help="Earliest month to fetch (format YYYY-MM, e.g. 2024-01)"
    )
    parser.add_argument(
        "--end-month",
        type=str,
        default="2026-08",
        help="Latest month to fetch (format YYYY-MM, default: 2026-08)"
    )
    parser.add_argument(
        "--rclone-remote",
        type=str,
        default="gdrive",
        help="Rclone remote name (default: gdrive)"
    )
    parser.add_argument(
        "--gdrive-folder",
        type=str,
        default="Online/BINANCE_HISTORICAL_DATA (till August 2026)",
        help="Target folder in Google Drive"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report available files without downloading or uploading"
    )

    args = parser.parse_args()

    shortlisted = get_shortlisted_symbols(args.shortlisted_csv or None)
    if args.symbols == "ALL_TARGETED":
        symbols = list(dict.fromkeys(DEFAULT_MAJOR_SYMBOLS + shortlisted))
    elif args.symbols == "SHORTLISTED_ONLY":
        symbols = shortlisted
    elif args.symbols == "MAJORS_ONLY":
        symbols = DEFAULT_MAJOR_SYMBOLS
    else:
        symbols = [s.strip().upper().replace("_", "") for s in args.symbols.split(",") if s.strip()]

    if args.data_types.upper() == "ALL":
        data_types = ALL_DATA_TYPES
    else:
        data_types = [dt.strip() for dt in args.data_types.split(",") if dt.strip() in ALL_DATA_TYPES]

    if args.timeframes.upper() == "ALL":
        timeframes = ALL_TIMEFRAMES
    else:
        timeframes = [tf.strip() for tf in args.timeframes.split(",") if tf.strip() in ALL_TIMEFRAMES]

    run_archival_pipeline(
        symbols=symbols,
        data_types=data_types,
        timeframes=timeframes,
        start_month=args.start_month,
        end_month=args.end_month,
        rclone_remote=args.rclone_remote,
        gdrive_folder=args.gdrive_folder,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
