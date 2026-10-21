#!/usr/bin/env python3
"""
Market Data Downloader & Aggregator for No-Stop-Loss Backtest Suite
==================================================================
Downloads and normalizes OHLCV candlestick data for:
1. Cryptos: BTC, ETH, SOL (via Binance Public API / Binance Vision local archives)
   Stored under: BACKTESTER/OHLCV_Data_Crypto/{symbol}/{tf}.csv
2. Commodity: GOLD (GC=F) (via Yahoo Finance)
   Stored under: BACKTESTER/OHLCV_Data_Stocks/GOLD/{tf}.csv
3. US Equities (10): AAPL, MSFT, AMZN, GOOGL, FB (META), TSLA, JPM, BAC, NFLX, NVDA
   Stored under: BACKTESTER/OHLCV_Data_Stocks/{symbol}/{tf}.csv

Timeframes supported: 1m, 5m, 15m, 1h, 4h, 1d.
"""

from __future__ import annotations
import os
import sys
import glob
import time
import argparse
import datetime
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import requests

# Add repository root to sys.path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "SUI", "NEAR"]
COMMODITY_SYMBOLS = ["GOLD"]
STOCK_SYMBOLS = ["AAPL", "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "JPM", "BAC", "NFLX", "NVDA"]

YAHOO_TICKER_MAP = {
    "GOLD": "GC=F",
    "FB": "META",
    "AAPL": "AAPL",
    "MSFT": "MSFT",
    "AMZN": "AMZN",
    "GOOGL": "GOOGL",
    "TSLA": "TSLA",
    "JPM": "JPM",
    "BAC": "BAC",
    "NFLX": "NFLX",
    "NVDA": "NVDA"
}

ALL_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

DEFAULT_CRYPTO_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
DEFAULT_STOCKS_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Stocks")
BINANCE_ARCHIVE_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Binance")


def resample_ohlcv(df: pd.DataFrame, target_rule: str) -> pd.DataFrame:
    """Resamples an OHLCV dataframe indexed by datetime to target timeframe."""
    if df.empty:
        return df
    resampled = df.resample(target_rule).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()
    resampled["open_time"] = resampled.index.astype("int64") // 10**6
    resampled["close_time"] = resampled["open_time"] + int(pd.Timedelta(target_rule).total_seconds() * 1000)
    return resampled.reset_index(drop=True)


def download_crypto_binance_api(symbol: str, timeframe: str, limit: int = 1000) -> pd.DataFrame:
    """Fetches recent OHLCV candles from Binance public REST API."""
    binance_sym = f"{symbol.upper()}USDT"
    interval_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h", "1d": "1d"}
    api_interval = interval_map.get(timeframe.lower(), "1h")
    
    url = "https://api.binance.com/api/v3/klines"
    all_rows = []
    end_time = None
    
    # Fetch in batches if necessary
    for _ in range(3):
        params = {"symbol": binance_sym, "interval": api_interval, "limit": limit}
        if end_time:
            params["endTime"] = end_time
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if not data:
                    break
                all_rows = data + all_rows
                end_time = int(data[0][0]) - 1
            else:
                break
        except Exception as e:
            print(f"[!] Binance API error for {binance_sym} {timeframe}: {e}")
            break
            
    if not all_rows:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_rows, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "count", "taker_buy_vol", "taker_buy_quote_vol", "ignore"
    ])
    df = df[["open_time", "open", "high", "low", "close", "volume", "close_time"]].copy()
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    df["open_time"] = df["open_time"].astype(int)
    df["close_time"] = df["close_time"].astype(int)
    df = df.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    return df


def load_local_binance_archive(symbol: str, timeframe: str) -> pd.DataFrame:
    """Loads and consolidates local monthly Binance Vision CSVs if present."""
    binance_sym = f"{symbol.upper()}USDT"
    tf_dir = os.path.join(BINANCE_ARCHIVE_DIR, binance_sym, timeframe)
    if not os.path.isdir(tf_dir):
        return pd.DataFrame()
        
    csv_files = sorted(glob.glob(os.path.join(tf_dir, "*.csv")))
    if not csv_files:
        return pd.DataFrame()
        
    dfs = []
    for f in csv_files:
        try:
            # Check if header exists
            first_line = ""
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                first_line = fp.readline()
            has_header = "open" in first_line.lower() or "timestamp" in first_line.lower()
            
            if has_header:
                sub_df = pd.read_csv(f)
                col_map = {c: c.lower().strip() for c in sub_df.columns}
                sub_df.rename(columns=col_map, inplace=True)
            else:
                sub_df = pd.read_csv(f, header=None, names=[
                    "open_time", "open", "high", "low", "close", "volume",
                    "close_time", "quote_volume", "count", "tb_base", "tb_quote", "ignore"
                ])
                
            req_cols = ["open_time", "open", "high", "low", "close", "volume"]
            if all(c in sub_df.columns for c in req_cols):
                if "close_time" not in sub_df.columns:
                    sub_df["close_time"] = sub_df["open_time"]
                sub_df = sub_df[["open_time", "open", "high", "low", "close", "volume", "close_time"]].copy()
                dfs.append(sub_df)
        except Exception:
            continue
            
    if not dfs:
        return pd.DataFrame()
        
    full_df = pd.concat(dfs, ignore_index=True)
    for col in ["open", "high", "low", "close", "volume"]:
        full_df[col] = pd.to_numeric(full_df[col], errors="coerce")
    full_df["open_time"] = pd.to_numeric(full_df["open_time"], errors="coerce").astype(int)
    full_df["close_time"] = pd.to_numeric(full_df["close_time"], errors="coerce").astype(int)
    full_df = full_df.dropna().drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    return full_df


def download_crypto(symbol: str, timeframe: str, output_dir: str) -> Optional[str]:
    """Ensures crypto OHLCV CSV exists under output_dir/{symbol}/{tf}.csv."""
    os.makedirs(os.path.join(output_dir, symbol), exist_ok=True)
    target_csv = os.path.join(output_dir, symbol, f"{timeframe}.csv")
    
    if os.path.isfile(target_csv) and os.path.getsize(target_csv) > 1024:
        print(f"[+] Crypto {symbol} {timeframe} cached at: {target_csv}")
        return target_csv
        
    print(f"[*] Sourcing {symbol} {timeframe} data...")
    df = load_local_binance_archive(symbol, timeframe)
    
    # If local archive empty or insufficient, query Binance API
    if df.empty or len(df) < 50:
        api_df = download_crypto_binance_api(symbol, timeframe)
        if not api_df.empty:
            if not df.empty:
                df = pd.concat([df, api_df], ignore_index=True).drop_duplicates(subset=["open_time"]).sort_values("open_time")
            else:
                df = api_df

    if df.empty and timeframe in ("4h", "1d"):
        # Resample from 1h if available
        h1_csv = download_crypto(symbol, "1h", output_dir)
        if h1_csv and os.path.isfile(h1_csv):
            h1_df = pd.read_csv(h1_csv)
            h1_df["dt"] = pd.to_datetime(h1_df["open_time"], unit="ms", utc=True)
            h1_df.set_index("dt", inplace=True)
            rule = "4h" if timeframe == "4h" else "1D"
            df = resample_ohlcv(h1_df, rule)

    if not df.empty:
        df.to_csv(target_csv, index=False)
        print(f"[OK] Saved {len(df)} bars to {target_csv}")
        return target_csv
    else:
        print(f"[!] Failed to obtain data for crypto {symbol} {timeframe}")
        return None


def download_stock_or_commodity(symbol: str, timeframe: str, output_dir: str) -> Optional[str]:
    """Fetches stock or commodity OHLCV using yfinance and caches to output_dir/{symbol}/{tf}.csv."""
    import yfinance as yf
    
    os.makedirs(os.path.join(output_dir, symbol), exist_ok=True)
    target_csv = os.path.join(output_dir, symbol, f"{timeframe}.csv")
    
    if os.path.isfile(target_csv) and os.path.getsize(target_csv) > 1024:
        print(f"[+] Stock/Commodity {symbol} {timeframe} cached at: {target_csv}")
        return target_csv
        
    ticker = YAHOO_TICKER_MAP.get(symbol.upper(), symbol.upper())
    print(f"[*] Downloading {symbol} ({ticker}) {timeframe} via yfinance...")
    
    yf_interval_map = {
        "1m": ("1m", "7d"),
        "5m": ("5m", "60d"),
        "15m": ("15m", "60d"),
        "1h": ("1h", "730d"),
        "4h": ("1h", "730d"),  # Resample from 1h
        "1d": ("1d", "5y")
    }
    
    interval_info = yf_interval_map.get(timeframe.lower())
    if not interval_info:
        print(f"[!] Unsupported timeframe for yfinance: {timeframe}")
        return None
        
    yf_interval, yf_period = interval_info
    
    try:
        data = yf.download(ticker, period=yf_period, interval=yf_interval, progress=False, auto_adjust=True)
        if data.empty:
            print(f"[!] No data returned from yfinance for {ticker} ({timeframe})")
            return None
            
        # Clean multi-index columns if returned
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0].lower() for col in data.columns]
        else:
            data.columns = [col.lower() for col in data.columns]
            
        data = data.dropna(subset=["close"]).copy()
        
        if timeframe.lower() == "4h":
            # Resample 1h bars into 4h bars
            data = resample_ohlcv(data, "4h")
        else:
            data["open_time"] = data.index.astype("int64") // 10**6
            tf_delta_s = {
                "1m": 60, "5m": 300, "15m": 900, "1h": 3600, "1d": 86400
            }.get(timeframe.lower(), 3600)
            data["close_time"] = data["open_time"] + (tf_delta_s * 1000)
            
        export_df = data[["open_time", "open", "high", "low", "close", "volume", "close_time"]].copy()
        export_df = export_df.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
        export_df.to_csv(target_csv, index=False)
        print(f"[OK] Saved {len(export_df)} bars to {target_csv}")
        return target_csv
    except Exception as e:
        print(f"[!] yfinance exception for {symbol} ({ticker}): {e}")
        return None


def download_market_data(
    assets: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    crypto_dir: str = DEFAULT_CRYPTO_DIR,
    stocks_dir: str = DEFAULT_STOCKS_DIR
) -> Dict[str, Dict[str, str]]:
    """Master routine to download market data for specified assets and timeframes."""
    target_assets = assets or (CRYPTO_SYMBOLS + COMMODITY_SYMBOLS + STOCK_SYMBOLS)
    target_tfs = timeframes or ALL_TIMEFRAMES
    
    results: Dict[str, Dict[str, str]] = {}
    
    for asset in target_assets:
        sym_clean = asset.upper().strip()
        results[sym_clean] = {}
        is_crypto = sym_clean in CRYPTO_SYMBOLS
        
        for tf in target_tfs:
            if is_crypto:
                path = download_crypto(sym_clean, tf, crypto_dir)
            else:
                path = download_stock_or_commodity(sym_clean, tf, stocks_dir)
                
            if path:
                results[sym_clean][tf] = path
                
    return results


def main():
    parser = argparse.ArgumentParser(description="Download & prepare OHLCV market data for no-stop-loss backtesting.")
    parser.add_argument("--assets", nargs="+", default=None, help="Target assets (e.g. BTC ETH GOLD AAPL)")
    parser.add_argument("--timeframes", nargs="+", default=None, help="Target timeframes (e.g. 1m 5m 15m 1h 4h 1d)")
    parser.add_argument("--crypto_dir", type=str, default=DEFAULT_CRYPTO_DIR, help="Output directory for crypto data")
    parser.add_argument("--stocks_dir", type=str, default=DEFAULT_STOCKS_DIR, help="Output directory for stocks/commodities")
    
    args = parser.parse_args()
    download_market_data(
        assets=args.assets,
        timeframes=args.timeframes,
        crypto_dir=args.crypto_dir,
        stocks_dir=args.stocks_dir
    )


if __name__ == "__main__":
    main()
