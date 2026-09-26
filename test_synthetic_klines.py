import pytest
from unittest.mock import MagicMock
from kcex.market import KCEXMarket, normalize_kcex_interval

def test_normalize_kcex_interval():
    assert normalize_kcex_interval("3m") == "Min3"
    assert normalize_kcex_interval("3min") == "Min3"
    assert normalize_kcex_interval("Min3") == "Min3"
    assert normalize_kcex_interval("1m") == "Min1"
    assert normalize_kcex_interval("5m") == "Min5"

def test_synthetic_min3_resampling():
    mock_client = MagicMock()
    market = KCEXMarket(client=mock_client)
    
    # 6 consecutive 1-minute candles spanning two 3-minute buckets:
    # Bucket 1: ts 0, 60, 120 -> b_ts = 0
    # Bucket 2: ts 180, 240, 300 -> b_ts = 180
    sample_min1_candles = [
        {"timestamp": 0,   "open": 100.0, "high": 105.0, "low": 99.0,  "close": 102.0, "volume": 10.0, "amount": 1000.0},
        {"timestamp": 60,  "open": 102.0, "high": 108.0, "low": 101.0, "close": 107.0, "volume": 15.0, "amount": 1500.0},
        {"timestamp": 120, "open": 107.0, "high": 107.5, "low": 103.0, "close": 104.0, "volume": 20.0, "amount": 2000.0},
        {"timestamp": 180, "open": 104.0, "high": 110.0, "low": 103.5, "close": 109.0, "volume": 12.0, "amount": 1200.0},
        {"timestamp": 240, "open": 109.0, "high": 112.0, "low": 108.0, "close": 111.0, "volume": 18.0, "amount": 1800.0},
        {"timestamp": 300, "open": 111.0, "high": 115.0, "low": 110.0, "close": 114.0, "volume": 25.0, "amount": 2500.0},
    ]
    
    # Mock recursive get_klines call when interval="Min1"
    original_get_klines = market.get_klines
    def mock_get_klines(symbol, interval="Min1", start_time=None, end_time=None, limit=100):
        if interval == "Min1":
            return sample_min1_candles
        return original_get_klines(symbol, interval, start_time, end_time, limit)
        
    market.get_klines = mock_get_klines
    
    min3_candles = market.get_klines("SPCX_USDT", interval="Min3", limit=2)
    assert len(min3_candles) == 2
    
    # Bucket 1 checks
    b1 = min3_candles[0]
    assert b1["timestamp"] == 0
    assert b1["open"] == 100.0
    assert b1["high"] == 108.0
    assert b1["low"] == 99.0
    assert b1["close"] == 104.0
    assert b1["volume"] == 45.0
    assert b1["amount"] == 4500.0
    
    # Bucket 2 checks
    b2 = min3_candles[1]
    assert b2["timestamp"] == 180
    assert b2["open"] == 104.0
    assert b2["high"] == 115.0
    assert b2["low"] == 103.5
    assert b2["close"] == 114.0
    assert b2["volume"] == 55.0
    assert b2["amount"] == 5500.0
