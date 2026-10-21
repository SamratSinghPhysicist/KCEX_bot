#!/usr/bin/env python3
"""
Fast downloader for DOGEUSDT and TRUMPUSDT 1h candles from Binance.
"""

import os
import sys
import time
import requests
import pandas as pd
import datetime

# Ensure unbuffered output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
CRYPTO_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")

def download_full_binance_history(symbol: str, interval: str = "1h") -> pd.DataFrame:
    binance_sym = f"{symbol.upper()}USDT"
    url = "https://api.binance.com/api/v3/klines"
    
    print(f"[*] Starting download for {binance_sym} ({interval})...", flush=True)
    all_rows = []
    start_time = 0
    batch_count = 0
    
    session = requests.Session()
    
    while True:
        params = {
            "symbol": binance_sym,
            "interval": interval,
            "startTime": start_time,
            "limit": 1000
        }
        try:
            r = session.get(url, params=params, timeout=10)
            if r.status_code != 200:
                print(f"[!] HTTP Error {r.status_code}: {r.text[:100]}", flush=True)
                time.sleep(1)
                continue
            data = r.json()
            if not data:
                print(f"[+] Reached end of data for {binance_sym}. Total bars: {len(all_rows):,}", flush=True)
                break
                
            all_rows.extend(data)
            batch_count += 1
            last_ts = data[-1][0]
            start_time = last_ts + 1
            
            dt = datetime.datetime.fromtimestamp(last_ts / 1000, datetime.timezone.utc)
            if batch_count % 15 == 0 or len(data) < 1000:
                print(f"    Batch {batch_count}: reached {dt.strftime('%Y-%m-%d %H:%M')} UTC ({len(all_rows):,} bars)", flush=True)
            
            if len(data) < 1000:
                print(f"[+] Completed {binance_sym}! Total bars: {len(all_rows):,}", flush=True)
                break
                
            time.sleep(0.05)
        except Exception as e:
            print(f"[!] Request exception: {e}", flush=True)
            time.sleep(1)
            
    if not all_rows:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_rows, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "count", "tb_base", "tb_quote", "ignore"
    ])
    
    df = df[["open_time", "open", "high", "low", "close", "volume", "close_time"]].copy()
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    df["open_time"] = df["open_time"].astype(int)
    df["close_time"] = df["close_time"].astype(int)
    
    df = df.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    return df

def main():
    symbols = ["TRUMP", "DOGE"]
    for sym in symbols:
        out_dir = os.path.join(CRYPTO_DIR, sym)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "1h.csv")
        
        df = download_full_binance_history(sym, "1h")
        if df.empty:
            print(f"[!] Failed to download data for {sym}", flush=True)
            continue
            
        df.to_csv(out_file, index=False)
        start_dt = datetime.datetime.fromtimestamp(df["open_time"].iloc[0] / 1000, datetime.timezone.utc)
        end_dt = datetime.datetime.fromtimestamp(df["close_time"].iloc[-1] / 1000, datetime.timezone.utc)
        print(f"[✓] Saved {len(df):,} candles to {out_file}", flush=True)
        print(f"    Date Range: {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%Y-%m-%d %H:%M')} UTC\n", flush=True)

if __name__ == "__main__":
    main()
