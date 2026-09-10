"""
Order Flow & Tick Microstructure Aggregator
============================================
Processes high-frequency millisecond tick trade logs (2-6 GB CSVs) in streaming
chunks to extract rich 1-minute institutional microstructure features:
- Aggressor Buy/Sell volume & Delta
- Cumulative Volume Delta (CVD)
- Order Flow Imbalance (OFI)
- 1-minute VWAP
- Trade arrival frequency & Retail vs Whale participation
- Graceful caching to compact Parquet files for near-instant reload.
"""

import os
import glob
import numpy as np
import pandas as pd
from typing import Optional, List, Dict

from .config import (
    PROCESSED_DATA_DIR,
    get_tick_spec,
    normalize_symbol_name,
)
from .data_loader import get_trades_file_path, generate_month_tuples


def get_cache_path(symbol: str, year: int, month: int) -> str:
    """Returns local parquet cache path for 1m aggregated orderflow."""
    sym = normalize_symbol_name(symbol)
    return os.path.join(PROCESSED_DATA_DIR, f"{sym}_orderflow_1m_{year}_{month:02d}.parquet")


def aggregate_trades_file_to_1m(
    trades_csv_path: str,
    chunksize: int = 500_000,
    whale_threshold_quote: float = 5000.0
) -> pd.DataFrame:
    """
    Reads a multi-gigabyte tick trades CSV file in streaming chunks
    and collapses it into precise 1-minute order-flow summary bars.
    """
    print(f"[OrderFlow] Processing trades file in streaming chunks: {os.path.basename(trades_csv_path)}")

    minute_accumulators: Dict[int, Dict[str, float]] = {}

    # Read column header or deduce names
    header_check = pd.read_csv(trades_csv_path, nrows=1)
    has_header = "id" in header_check.columns or "price" in header_check.columns
    names = ["id", "price", "qty", "quote_qty", "time", "is_buyer_maker"] if not has_header else None

    chunk_idx = 0
    total_trades = 0

    for chunk in pd.read_csv(
        trades_csv_path,
        chunksize=chunksize,
        names=names,
        header=0 if has_header else None,
        usecols=["price", "qty", "quote_qty", "time", "is_buyer_maker"],
        dtype={
            "price": "float32",
            "qty": "float32",
            "quote_qty": "float32",
            "time": "int64",
            "is_buyer_maker": "bool"
        }
    ):
        chunk_idx += 1
        total_trades += len(chunk)

        # Vectorized calculations for chunk
        # In Binance: is_buyer_maker = True means buyer was passive maker -> seller was taker (market sell)
        # is_buyer_maker = False means buyer was active taker (market buy)
        is_buy = (~chunk["is_buyer_maker"]).values
        is_sell = chunk["is_buyer_maker"].values

        qty = chunk["qty"].values
        price = chunk["price"].values
        quote_qty = chunk["quote_qty"].values
        time_ms = chunk["time"].values
        minute_ts = (time_ms // 60000) * 60000

        buy_qty = np.where(is_buy, qty, 0.0)
        sell_qty = np.where(is_sell, qty, 0.0)
        pv = price * qty
        is_whale = quote_qty >= whale_threshold_quote
        whale_qty = np.where(is_whale, qty, 0.0)

        # Chunk dataframe for fast group aggregation
        temp_df = pd.DataFrame({
            "minute_ts": minute_ts,
            "buy_vol": buy_qty,
            "sell_vol": sell_qty,
            "tot_vol": qty,
            "pv": pv,
            "whale_vol": whale_qty,
            "buy_cnt": is_buy.astype("int32"),
            "sell_cnt": is_sell.astype("int32"),
            "tot_cnt": 1
        })

        chunk_grp = temp_df.groupby("minute_ts").sum()

        for ts, row in chunk_grp.iterrows():
            if ts not in minute_accumulators:
                minute_accumulators[ts] = {
                    "buy_vol": row["buy_vol"],
                    "sell_vol": row["sell_vol"],
                    "tot_vol": row["tot_vol"],
                    "pv": row["pv"],
                    "whale_vol": row["whale_vol"],
                    "buy_cnt": row["buy_cnt"],
                    "sell_cnt": row["sell_cnt"],
                    "tot_cnt": row["tot_cnt"]
                }
            else:
                acc = minute_accumulators[ts]
                acc["buy_vol"] += row["buy_vol"]
                acc["sell_vol"] += row["sell_vol"]
                acc["tot_vol"] += row["tot_vol"]
                acc["pv"] += row["pv"]
                acc["whale_vol"] += row["whale_vol"]
                acc["buy_cnt"] += row["buy_cnt"]
                acc["sell_cnt"] += row["sell_cnt"]
                acc["tot_cnt"] += row["tot_cnt"]

        if chunk_idx % 10 == 0:
            print(f"[OrderFlow] Streamed {total_trades:,} ticks across {len(minute_accumulators):,} 1m bars...")

    if not minute_accumulators:
        return pd.DataFrame()

    # Build final DataFrame
    records = []
    for ts in sorted(minute_accumulators.keys()):
        acc = minute_accumulators[ts]
        tot_vol = max(acc["tot_vol"], 1e-9)
        tot_cnt = max(acc["tot_cnt"], 1)

        buy_vol = acc["buy_vol"]
        sell_vol = acc["sell_vol"]
        delta_vol = buy_vol - sell_vol
        vwap = acc["pv"] / tot_vol if tot_vol > 0 else 0.0

        records.append({
            "timestamp": ts,
            "of_buy_volume": buy_vol,
            "of_sell_volume": sell_vol,
            "of_delta_volume": delta_vol,
            "of_taker_buy_ratio": buy_vol / tot_vol,
            "of_imbalance_ratio": delta_vol / tot_vol,
            "of_trades_count": tot_cnt,
            "of_buy_trades_count": acc["buy_cnt"],
            "of_sell_trades_count": acc["sell_cnt"],
            "of_trade_count_ratio": acc["buy_cnt"] / tot_cnt,
            "of_vwap": vwap,
            "of_avg_trade_size": tot_vol / tot_cnt,
            "of_whale_ratio": acc["whale_vol"] / tot_vol
        })

    df_out = pd.DataFrame(records)
    print(f"[OrderFlow] Finished aggregating {total_trades:,} trades into {len(df_out):,} 1m order-flow bars.")
    return df_out


def get_or_create_orderflow_1m(
    symbol: str,
    year: int,
    month: int,
    auto_download: bool = True
) -> Optional[pd.DataFrame]:
    """
    Returns 1m order-flow metrics DataFrame for the given month.
    Uses cached Parquet if present; otherwise processes the raw trades CSV.
    """
    cache_file = get_cache_path(symbol, year, month)
    cache_pkl = cache_file.replace(".parquet", ".pkl")

    if os.path.exists(cache_file):
        try:
            return pd.read_parquet(cache_file)
        except Exception:
            pass

    if os.path.exists(cache_pkl):
        try:
            return pd.read_pickle(cache_pkl)
        except Exception:
            pass

    # Look for raw trades CSV
    trades_path = get_trades_file_path(symbol, year, month, auto_download=auto_download)
    if trades_path is None or not os.path.exists(trades_path):
        return None

    df_1m = aggregate_trades_file_to_1m(trades_path)
    if not df_1m.empty:
        saved = False
        try:
            df_1m.to_parquet(cache_file, index=False)
            print(f"[+] Saved order-flow cache to {cache_file}")
            saved = True
        except Exception:
            pass

        if not saved:
            try:
                df_1m.to_pickle(cache_pkl)
                print(f"[+] Saved order-flow cache to {cache_pkl}")
            except Exception as e:
                print(f"[!] Could not write cache {cache_pkl}: {e}")

    return df_1m


def build_orderflow_features_range(
    symbol: str,
    start_date: str,
    end_date: str,
    auto_download: bool = True
) -> pd.DataFrame:
    """
    Builds or loads aggregated 1m order-flow metrics for all months in the date range.
    """
    months = generate_month_tuples(start_date, end_date)
    dfs = []
    for y, m in months:
        df_month = get_or_create_orderflow_1m(symbol, y, m, auto_download=auto_download)
        if df_month is not None and not df_month.empty:
            dfs.append(df_month)

    if not dfs:
        return pd.DataFrame()

    df_combined = pd.concat(dfs, ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    # Compute Cumulative Volume Delta (CVD)
    df_combined["of_cvd"] = df_combined["of_delta_volume"].cumsum()
    df_combined["of_cvd_ma5"] = df_combined["of_cvd"].rolling(5, min_periods=1).mean()
    df_combined["of_cvd_ma15"] = df_combined["of_cvd"].rolling(15, min_periods=1).mean()
    df_combined["of_cvd_slope"] = (df_combined["of_cvd"] - df_combined["of_cvd_ma5"]) / (df_combined["of_cvd_ma5"].abs() + 1e-6)

    return df_combined
