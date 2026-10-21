#!/usr/bin/env python3
import os, sys, time, requests, pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")

def fetch(symbol, interval="1h", max_batches=50):
    binance_sym = f"{symbol.upper()}USDT"
    print(f"[*] Fetching {binance_sym} {interval}...", flush=True)
    url = "https://api.binance.com/api/v3/klines"
    all_rows = []
    end_time = None
    for i in range(max_batches):
        params = {"symbol": binance_sym, "interval": interval, "limit": 1000}
        if end_time:
            params["endTime"] = end_time
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if not data:
                    break
                all_rows = data + all_rows
                earliest_open = int(data[0][0])
                end_time = earliest_open - 1
                if len(data) < 1000:
                    break
                time.sleep(0.04)
            else:
                print(f"[!] Error {r.status_code}", flush=True)
                break
        except Exception as e:
            print(f"[!] Error: {e}", flush=True)
            break
            
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
    
    tdir = os.path.join(OUTPUT_DIR, symbol.upper())
    os.makedirs(tdir, exist_ok=True)
    tcsv = os.path.join(tdir, f"{interval}.csv")
    df.to_csv(tcsv, index=False)
    print(f"[OK] Saved {len(df):,} {interval} bars for {symbol} to {tcsv}", flush=True)

if __name__ == "__main__":
    fetch("NEAR", "1h", max_batches=60)
    fetch("NEAR", "1m", max_batches=10)
    fetch("SUI", "1m", max_batches=10)
