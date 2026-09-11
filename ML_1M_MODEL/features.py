"""
Deep Feature Engineering Pipeline for 1-Minute Crypto Futures
=============================================================
Calculates multi-horizon technical indicators, candlestick anatomy,
realized micro-volatility, cyclical time features, and merges high-resolution
order-flow microstructure signals.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional


def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    """Calculates Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates Relative Strength Index."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def calculate_stoch_rsi(series: pd.Series, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> Tuple[pd.Series, pd.Series]:
    """Calculates Stochastic RSI %K and %D."""
    rsi = calculate_rsi(series, period)
    rsi_min = rsi.rolling(period).min()
    rsi_max = rsi.rolling(period).max()

    stoch = (rsi - rsi_min) / (rsi_max - rsi_min + 1e-9) * 100.0
    k = stoch.rolling(smooth_k).mean().fillna(50.0)
    d = k.rolling(smooth_d).mean().fillna(50.0)
    return k, d


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculates Average True Range."""
    prev_close = df["close"].shift(1)
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - prev_close).abs()
    tr3 = (df["low"] - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


def extract_features(df_ohlcv: pd.DataFrame, df_orderflow: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Extracts deep technical indicators and merges order-flow microstructure.
    Returns feature matrix with aligned timestamp and targets.
    """
    df = df_ohlcv.copy()
    close = df["close"]
    high = df["high"]
    low = df["low"]
    open_p = df["open"]
    vol = df["volume"]

    # 1. Multi-horizon log returns
    for horizon in [1, 2, 3, 5, 10, 15, 30, 60]:
        df[f"ret_{horizon}m"] = np.log(close / close.shift(horizon).replace(0, np.nan)).fillna(0.0)

    # 2. Moving Average Dynamics
    ema9 = calculate_ema(close, 9)
    ema21 = calculate_ema(close, 21)
    ema50 = calculate_ema(close, 50)
    ema200 = calculate_ema(close, 200)

    df["dist_ema9"] = (close - ema9) / ema9
    df["dist_ema21"] = (close - ema21) / ema21
    df["dist_ema50"] = (close - ema50) / ema50
    df["spread_ema9_21"] = (ema9 - ema21) / ema21
    df["spread_ema50_200"] = (ema50 - ema200) / (ema200 + 1e-9)

    # 3. Volatility Metrics
    atr5 = calculate_atr(df, 5)
    atr14 = calculate_atr(df, 14)
    atr30 = calculate_atr(df, 30)

    df["atr_14"] = atr14
    df["atr_norm_14"] = atr14 / close
    df["atr_norm_5"] = atr5 / close
    df["atr_ratio_5_30"] = atr5 / (atr30 + 1e-9)

    # Parkinson Volatility (High-Low estimator)
    df["parkinson_vol"] = np.sqrt((np.log(high / low.replace(0, np.nan)) ** 2) / (4 * np.log(2))).fillna(0.0)

    # Garman-Klass Volatility
    term1 = 0.5 * (np.log(high / low.replace(0, np.nan)) ** 2)
    term2 = (2 * np.log(2) - 1) * (np.log(close / open_p.replace(0, np.nan)) ** 2)
    df["garman_klass_vol"] = np.sqrt(np.maximum(0, term1 - term2)).fillna(0.0)

    # Bollinger Bands
    roll_mean20 = close.rolling(20).mean()
    roll_std20 = close.rolling(20).std()
    upper_bb = roll_mean20 + 2 * roll_std20
    lower_bb = roll_mean20 - 2 * roll_std20
    df["bb_pct_b"] = ((close - lower_bb) / (upper_bb - lower_bb + 1e-9)).clip(-0.5, 1.5).fillna(0.5)
    df["bb_bandwidth"] = (upper_bb - lower_bb) / roll_mean20

    # Carter Volatility Squeeze (Bollinger Bands vs Keltner Channels)
    ema20 = calculate_ema(close, 20)
    atr20 = calculate_atr(df, 20)
    kc_upper = ema20 + 1.5 * atr20
    kc_lower = ema20 - 1.5 * atr20
    df["squeeze_on"] = ((lower_bb > kc_lower) & (upper_bb < kc_upper)).astype("float32")
    df["squeeze_off"] = ((upper_bb > kc_upper) | (lower_bb < kc_lower)).astype("float32")

    # Trend Regime Alignment
    df["trend_alignment"] = np.where(
        (close > ema9) & (ema9 > ema21) & (ema21 > ema50), 1.0,
        np.where((close < ema9) & (ema9 < ema21) & (ema21 < ema50), -1.0, 0.0)
    ).astype("float32")

    # 4. Candlestick Anatomy
    hl_range = (high - low).replace(0, np.nan)
    df["hl_range_pct"] = (high - low) / close
    df["body_ratio"] = (close - open_p).abs() / hl_range
    df["upper_shadow_ratio"] = (high - np.maximum(open_p, close)) / hl_range
    df["lower_shadow_ratio"] = (np.minimum(open_p, close) - low) / hl_range
    df["candle_polarity"] = np.sign(close - open_p)
    for col in ["body_ratio", "upper_shadow_ratio", "lower_shadow_ratio"]:
        df[col] = df[col].fillna(0.0)

    # 5. Momentum Oscillators
    df["rsi_7"] = calculate_rsi(close, 7)
    df["rsi_14"] = calculate_rsi(close, 14)
    stoch_k, stoch_d = calculate_stoch_rsi(close, 14)
    df["stoch_rsi_k"] = stoch_k
    df["stoch_rsi_d"] = stoch_d

    # MACD
    ema12 = calculate_ema(close, 12)
    ema26 = calculate_ema(close, 26)
    macd_line = ema12 - ema26
    macd_signal = calculate_ema(macd_line, 9)
    df["macd_hist_norm"] = (macd_line - macd_signal) / close

    # 6. Volume Anomalies
    vol_mean20 = vol.rolling(20).mean()
    vol_std20 = vol.rolling(20).std()
    df["volume_zscore"] = ((vol - vol_mean20) / (vol_std20 + 1e-9)).clip(-3.0, 5.0).fillna(0.0)
    df["volume_surge"] = (vol / (vol_mean20 + 1e-9)).clip(0.0, 10.0).fillna(1.0)

    # 7. Merge Order Flow Microstructure (if available)
    if df_orderflow is not None and not df_orderflow.empty:
        df = pd.merge(df, df_orderflow, on="timestamp", how="left")

        # Fill missing order-flow values with neutral baselines
        df["of_taker_buy_ratio"] = df["of_taker_buy_ratio"].fillna(0.5)
        df["of_imbalance_ratio"] = df["of_imbalance_ratio"].fillna(0.0)
        df["of_trade_count_ratio"] = df["of_trade_count_ratio"].fillna(0.5)
        df["of_whale_ratio"] = df["of_whale_ratio"].fillna(0.0)
        df["of_vwap_dev"] = ((close - df["of_vwap"]) / (df["of_vwap"] + 1e-9)).fillna(0.0)
        df["of_cvd_slope"] = df["of_cvd_slope"].fillna(0.0)
    else:
        # Fallback to OHLCV native taker metrics if present
        if "taker_buy_volume" in df.columns:
            df["of_taker_buy_ratio"] = (df["taker_buy_volume"] / (vol + 1e-9)).fillna(0.5)
            df["of_imbalance_ratio"] = ((2 * df["taker_buy_volume"] - vol) / (vol + 1e-9)).fillna(0.0)
        else:
            df["of_taker_buy_ratio"] = 0.5
            df["of_imbalance_ratio"] = 0.0

        df["of_trade_count_ratio"] = 0.5
        df["of_whale_ratio"] = 0.0
        df["of_vwap_dev"] = 0.0
        df["of_cvd_slope"] = 0.0

    # 8. Cyclical Time Features
    if "datetime" in df.columns:
        dt = pd.to_datetime(df["datetime"], utc=True)
    else:
        dt = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    minute = dt.dt.minute
    hour = dt.dt.hour
    dow = dt.dt.dayofweek

    df["sin_minute"] = np.sin(2 * np.pi * minute / 60.0)
    df["cos_minute"] = np.cos(2 * np.pi * minute / 60.0)
    df["sin_hour"] = np.sin(2 * np.pi * hour / 24.0)
    df["cos_hour"] = np.cos(2 * np.pi * hour / 24.0)
    df["sin_dow"] = np.sin(2 * np.pi * dow / 7.0)
    df["cos_dow"] = np.cos(2 * np.pi * dow / 7.0)

    # Feature column names list (excluding targets and raw prices)
    exclude_cols = {
        "timestamp", "datetime", "open", "high", "low", "close", "volume",
        "quote_volume", "close_time", "ignore", "of_vwap", "of_cvd",
        "of_cvd_ma5", "of_cvd_ma15", "trades_count", "taker_buy_volume",
        "taker_buy_quote_volume", "of_buy_volume", "of_sell_volume",
        "of_delta_volume", "of_trades_count", "of_buy_trades_count",
        "of_sell_trades_count", "of_avg_trade_size"
    }

    feature_cols = [c for c in df.columns if c not in exclude_cols and not c.startswith("target_")]

    return df, feature_cols
