#!/usr/bin/env python3
"""
High-Speed Binance Downloader for SUI and NEAR
==============================================
Downloads full historical 1h (and 1m/5m sample) OHLCV data directly from Binance public API.
"""

import os
import sys
import time
import requests
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")

def fetch_full_history(symbol: str, interval: str = "1h", max_batches: int = 40):
    binance_sym = f"{symbol.upper()}USDT"
    print(f"[*] Downloading full {interval} history for {binance_sym}...")
    url = "https://api.binance.com/api/v3/klines"
    
    all_rows = []
    end_time = None
    
    for i in range(max_batches):
        params = {
            "symbol": binance_sym,
            "interval": interval,
            "limit": 1000
        }
        if end_time:
            params["endTime"] = end_time
            
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if not data:
                    print(f"    Batch {i+1}: No more data received.")
                    break
                all_rows = data + all_rows
                earliest_open = int(data[0][0])
                end_time = earliest_open - 1
                earliest_dt = pd.to_datetime(earliest_open, unit="ms")
                print(f"    Batch {i+1}: Got {len(data)} bars (earliest: {earliest_dt.strftime('%Y-%m-%d %H:%M')})")
                if len(data) < 1000:
                    print("    Reached beginning of trading history.")
                    break
                time.sleep(0.05) # respect rate limit
            else:
                print(f"[!] HTTP error {r.status_code}: {r.text}")
                break
        except Exception as e:
            print(f"[!] Request error: {e}")
            break
            
    if not all_rows:
        print(f"[ERROR] Failed to fetch data for {binance_sym}")
        return None
        
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
    
    target_dir = os.path.join(OUTPUT_DIR, symbol.upper())
    os.makedirs(target_dir, exist_ok=True)
    csv_path = os.path.join(target_dir, f"{interval}.csv")
    df.to_csv(csv_path, index=False)
    
    t_start = pd.to_datetime(df["open_time"].min(), unit="ms")
    t_end = pd.to_datetime(df["close_time"].max(), unit="ms")
    days = (t_end - t_start).total_seconds() / 86400.0
    print(f"[SUCCESS] Saved {len(df):,} {interval} bars for {symbol} ({t_start.strftime('%Y-%m-%d')} to {t_end.strftime('%Y-%m-%d')}, {days:.1f} days) at:\n   {csv_path}\n")
    return csv_path

if __name__ == "__main__":
    for sym in ["SUI", "NEAR"]:
        fetch_full_history(sym, interval="1h", max_batches=50)
        # Also fetch recent 5m / 1m for dispute resolver
        fetch_full_history(sym, interval="1m", max_batches=10)
