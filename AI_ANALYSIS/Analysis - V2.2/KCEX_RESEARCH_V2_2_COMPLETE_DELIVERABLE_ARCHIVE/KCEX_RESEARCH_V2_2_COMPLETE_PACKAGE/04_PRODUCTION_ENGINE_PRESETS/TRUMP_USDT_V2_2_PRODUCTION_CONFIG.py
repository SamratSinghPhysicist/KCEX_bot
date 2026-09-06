"""
Production Strategy Configuration: TRUMP_USDT V2.2 Direct 25% ROE Scalper
========================================================================
Empirically validated on 34,250 trades across 8 months of Binance millisecond ticks.
Results: Net Realized PnL: +$1.2896 USDT (75x, $100 capital) | PF: 1.12 | Win Rate: 84.77%
Critical S_max: 0.150 ticks
"""

CONFIG = {
    "symbol": "TRUMP_USDT",
    "leverage": 75,
    "capital": 100.00,
    "strategy_type": "STOCH_RSI",
    "timeframe": "1m",
    "stoch_rsi_preset": "FAST_SCALP",
    "rsi_length": 9,
    "stoch_length": 9,
    "k_period": 3,
    "d_period": 3,
    "overbought_threshold": 80.0,
    "oversold_threshold": 20.0,
    "invert_signal": False,           # Direct momentum entry
    
    # Execution Geometry
    "take_profit_ticks": 2.0,         # Limit maker order (+2 ticks)
    "stop_loss_roe_pct": 25.0,        # Percentage ROE stop loss (25% ROE = -0.333% price move at 75x)
    
    # Dynamic Regime Filter
    "chop_filter_enabled": True,
    "chop_max_threshold": 55.0,       # Avoid dead consolidation chop
    
    # Order Queue Management
    "order_timeout_seconds": 10.0
}
