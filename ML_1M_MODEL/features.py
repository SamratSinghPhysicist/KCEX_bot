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


def extract_features(
    df_ohlcv: pd.DataFrame,
    df_orderflow: Optional[pd.DataFrame] = None
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Extracts high-conviction scale-invariant alpha features and merges order-flow microstructure.
    Returns:
    - enriched DataFrame with context columns and indicators
    - list of predictive feature column names for model training
    """
    df = df_ohlcv.copy().reset_index(drop=True)
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    open_p = df["open"].values
    vol = df["volume"].values
    n = len(df)

    # 1. Multi-horizon Volatility Metrics
    prev_c = np.roll(close, 1)
    prev_c[0] = close[0]
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_c), np.abs(low - prev_c)))
    atr14 = pd.Series(tr).ewm(span=14, adjust=False).mean().values
    atr5 = pd.Series(tr).ewm(span=5, adjust=False).mean().values
    atr30 = pd.Series(tr).ewm(span=30, adjust=False).mean().values

    # Store for risk calculation and labeling
    df["atr_14"] = atr14

    # 2. Moving Average Trend Dynamics (ATR-Normalized for Stationarity)
    ema9 = pd.Series(close).ewm(span=9, adjust=False).mean().values
    ema21 = pd.Series(close).ewm(span=21, adjust=False).mean().values
    ema50 = pd.Series(close).ewm(span=50, adjust=False).mean().values
    ema200 = pd.Series(close).ewm(span=200, adjust=False).mean().values

    # Higher Timeframe MAs (15m and 1h equivalents on 1m candles)
    ema15m_21 = pd.Series(close).ewm(span=21 * 15, adjust=False).mean().values
    ema15m_50 = pd.Series(close).ewm(span=50 * 15, adjust=False).mean().values
    ema1h_50 = pd.Series(close).ewm(span=50 * 60, adjust=False).mean().values
    ema1h_200 = pd.Series(close).ewm(span=200 * 60, adjust=False).mean().values

    df["dist_ema9"] = (close - ema9) / (atr14 + 1e-9)
    df["dist_ema21"] = (close - ema21) / (atr14 + 1e-9)
    df["dist_ema50"] = (close - ema50) / (atr14 + 1e-9)
    df["dist_ema200"] = (close - ema200) / (atr14 + 1e-9)
    df["dist_ema15m_21"] = (close - ema15m_21) / (atr14 + 1e-9)
    df["dist_ema1h_50"] = (close - ema1h_50) / (atr14 + 1e-9)
    df["spread_9_21"] = (ema9 - ema21) / (atr14 + 1e-9)
    df["spread_21_50"] = (ema21 - ema50) / (atr14 + 1e-9)
    df["spread_50_200"] = (ema50 - ema200) / (atr14 + 1e-9)

    # 3. Macro & HTF Trend Alignment Scores
    df["trend_score"] = (
        np.sign(close - ema9) +
        np.sign(ema9 - ema21) +
        np.sign(ema21 - ema50) +
        np.sign(ema50 - ema200)
    ).astype("float32") / 4.0

    df["trend_htf"] = (
        np.sign(close - ema15m_21) +
        np.sign(ema15m_21 - ema15m_50) +
        np.sign(ema15m_50 - ema1h_50) +
        np.sign(ema1h_50 - ema1h_200)
    ).astype("float32") / 4.0

    # Macro Regimes for directional gating
    df["macro_bull"] = (ema1h_50 > ema1h_200) & (ema15m_21 > ema15m_50) & (close > ema1h_50)
    df["macro_bear"] = (ema1h_50 < ema1h_200) & (ema15m_21 < ema15m_50) & (close < ema1h_50)

    # 4. Volatility Bands & Squeeze Dynamics
    roll_m20 = pd.Series(close).rolling(20).mean().values
    roll_s20 = pd.Series(close).rolling(20).std().values
    upper_bb = roll_m20 + 2 * roll_s20
    lower_bb = roll_m20 - 2 * roll_s20
    bb_width = (upper_bb - lower_bb) / (roll_m20 + 1e-9)
    bb_width_ma20 = pd.Series(bb_width).rolling(20).mean().values

    df["bb_width"] = bb_width
    df["bb_expansion"] = bb_width / (bb_width_ma20 + 1e-9)
    df["bb_pct_b"] = ((close - lower_bb) / (upper_bb - lower_bb + 1e-9)).clip(-0.5, 1.5)
    df["atr_norm"] = atr14 / close
    df["vol_ratio_5_30"] = atr5 / (atr30 + 1e-9)

    # 5. Microstructure & Order Flow
    if df_orderflow is not None and not df_orderflow.empty:
        if "of_taker_buy_ratio" not in df.columns:
            df = pd.merge(df, df_orderflow, on="timestamp", how="left")
        vwap = df["of_vwap"].values if "of_vwap" in df.columns else roll_m20
        taker_ratio = df["of_taker_buy_ratio"].fillna(0.5).values
        imbalance = df["of_imbalance_ratio"].fillna(0.0).values
        cvd_slope = df["of_cvd_slope"].fillna(0.0).values
        whale_ratio = df["of_whale_ratio"].fillna(0.0).values
    else:
        vwap = roll_m20
        if "taker_buy_volume" in df.columns:
            taker_ratio = (df["taker_buy_volume"] / (vol + 1e-9)).fillna(0.5).values
            imbalance = ((2 * df["taker_buy_volume"] - vol) / (vol + 1e-9)).fillna(0.0).values
        else:
            taker_ratio = np.full(n, 0.5)
            imbalance = np.zeros(n)
        cvd_slope = np.zeros(n)
        whale_ratio = np.zeros(n)

    df["dist_vwap"] = (close - vwap) / (atr14 + 1e-9)
    df["taker_ratio"] = taker_ratio
    df["imbalance"] = imbalance
    df["cvd_slope"] = cvd_slope
    df["whale_ratio"] = whale_ratio
    df["of_taker_buy_ratio"] = taker_ratio  # Kept in df for schema compatibility

    # 6. Volume Intensity
    vol_ma20 = pd.Series(vol).rolling(20).mean().values
    df["vol_surge"] = vol / (vol_ma20 + 1e-9)

    # 7. Multi-Horizon Returns
    df["ret_1m"] = pd.Series(close).pct_change(1).fillna(0.0).values
    df["ret_3m"] = pd.Series(close).pct_change(3).fillna(0.0).values
    df["ret_5m"] = pd.Series(close).pct_change(5).fillna(0.0).values
    df["ret_15m"] = pd.Series(close).pct_change(15).fillna(0.0).values
    df["ret_60m"] = pd.Series(close).pct_change(60).fillna(0.0).values

    # 8. Rejection Wicks & Flow Absorption
    hl_r = np.maximum(high - low, 1e-9)
    lower_wick = (np.minimum(open_p, close) - low) / hl_r
    upper_wick = (high - np.maximum(open_p, close)) / hl_r
    df["lower_wick"] = lower_wick
    df["upper_wick"] = upper_wick
    df["wick_diff"] = lower_wick - upper_wick

    # 9. Additional standard indicators to maintain compatibility with test_pipeline
    df["parkinson_vol"] = np.sqrt((np.log(high / np.maximum(low, 1e-9)) ** 2) / (4 * np.log(2)))
    df["rsi_14"] = calculate_rsi(pd.Series(close), 14).values

    # Verified, deduplicated stationary alpha features
    feature_cols = [
        "dist_ema9", "dist_ema21", "dist_ema50", "dist_ema200",
        "dist_ema15m_21", "dist_ema1h_50",
        "spread_9_21", "spread_21_50", "spread_50_200",
        "trend_score", "trend_htf", "dist_vwap",
        "bb_width", "bb_expansion", "bb_pct_b",
        "taker_ratio", "imbalance", "cvd_slope", "whale_ratio",
        "vol_surge", "atr_norm", "vol_ratio_5_30",
        "ret_1m", "ret_3m", "ret_5m", "ret_15m", "ret_60m",
        "lower_wick", "upper_wick", "wick_diff"
    ]

    return df, feature_cols
