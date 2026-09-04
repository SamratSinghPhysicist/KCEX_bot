"""
KCEX Trading Bot - "Masterplan" Strategy Settings
=================================================
Edit this file to customize default parameters for the automated engine.
Any changes saved here will be automatically loaded by run_engine.py.
"""

# =============================================================================
# TRADING PAIR & ASSET
# =============================================================================
# Select a zero-fee trading pair. Currently, TRUMP_USDT has 0% maker and 0% taker fees.
SYMBOL = "TRUMP_USDT"

# Default direction: "LONG" or "SHORT"
DIRECTION = "LONG"

# Default execution mode:
# "live"    -> Real trades using KCEX account balance
# "dry-run" -> Real-time market simulation (zero risk, uses live ticker data)
MODE = "live"

# =============================================================================
# MASTERPLAN TAKE-PROFIT & STOP-LOSS RULES
# =============================================================================
# Minimum Take-Profit rule: Number of pu (Price Unit / Tick Size) away from entry price.
# For TRUMP_USDT, 1 pu = 0.001 USDT.
# TP_TICKS = 1 -> TP = Entry Price + 1 * pu (for Long) or Entry Price - 1 * pu (for Short)
# TP_TICKS = 2 -> TP = Entry Price + 2 * pu (for Long) or Entry Price - 2 * pu (for Short)
TP_TICKS = 2

# Stop-Loss rule: Maximum loss on margin (Return on Equity / ROE %).
# 10.0 means -10% ROE.
# At 75x leverage, a 10% ROE stop is approximately a 0.133% price change,
# keeping the position safely away from liquidation.
SL_ROE_PCT = 10.0

# Position leverage (isolated margin)
LEVERAGE = 75

# Margin mode: True for Isolated (openType=1), False for Cross (openType=2)
IS_ISOLATED = True

# =============================================================================
# CYCLE TIMING & LIMITS
# =============================================================================
# Cooldown period in seconds to wait after a trade closes before opening the next trade.
COOLDOWN_SECONDS = 30.0

# Maximum number of trades to execute in this session (0 = unlimited / run continuously)
MAX_TRADES = 3

# Ticker polling interval in seconds while actively monitoring an open trade
POLL_INTERVAL_SECONDS = 0.3

# =============================================================================
# LOGGING DIRECTORIES & FILES
# =============================================================================
LOGS_DIR = "logs"
REALTIME_LOG_FILE = "engine_realtime.log"
OUTCOMES_LOG_FILE = "trade_outcomes.txt"
OUTCOMES_JSONL_FILE = "trade_outcomes.jsonl"
