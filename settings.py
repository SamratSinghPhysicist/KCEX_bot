"""
KCEX Trading Bot - "Masterplan" Strategy Settings & Configuration Guide
=============================================================================
This file defines all default parameters for the Automated Trade Execution Engine.
Any changes saved here are automatically loaded whenever `run_engine.py` is started.

=============================================================================
📖 QUICK REFERENCE & STRATEGY GUIDE
=============================================================================
The "Masterplan" strategy is designed for automated high-frequency cycle trading
on KCEX zero-fee contracts (such as TRUMP_USDT).

Key Concepts:
1. ZERO-FEE PAIR:
   - Ensures maker and taker fees are 0.00% so that even micro-tick scalps are pure profit.
2. MIN-PROFIT TAKE PROFIT (pu ticks):
   - Places the profit target at a fixed distance in price units (pu).
   - For TRUMP_USDT, 1 pu = 0.001 USDT.
   - Example: Entry 2.3500 + 2 pu = 2.3520 USDT (+0.085% price move).
3. STOP LOSS & HIGH-LEVERAGE MATHEMATICS:
   - In futures trading, ROE (Return on Equity) is calculated on MARGIN:
       Price Move % = ROE % / Leverage
   - At 75x leverage:
       * 10% ROE loss = 0.133% price move (~3 ticks / 0.003 USDT).
       * Total Liquidation buffer = 0.333% (~7.8 ticks / 0.0078 USDT)!
       * Any stop loss > 7 ticks is impossible at 75x because KCEX liquidates at 8 ticks!
   - At 30x leverage (RECOMMENDED):
       * Liquidation buffer = ~55 ticks (safe breathing room).
       * 10 ticks stop loss (0.010 USDT) = ~12.7% ROE loss.
       * Margin required for 1 contract (0.1 TRUMP) = ~0.0079 USDT (INR ~0.75).
=============================================================================
"""

# =============================================================================
# 1. TRADING PAIR & ASSET CONFIGURATION
# =============================================================================
# Select a zero-fee trading pair. Currently, TRUMP_USDT has 0% maker and 0% taker fees.
# Other pairs can be specified here if KCEX enables zero-fee promotions on them.
SYMBOL = "TRUMP_USDT"

# Default order direction: "LONG" or "SHORT"
# The engine's directional cycle sub-strategy will execute trades in this direction.
DIRECTION = "LONG"

# Default execution mode:
# "live"    -> Real trades using KCEX futures wallet balance (requires API token in .env)
# "dry-run" -> Real-time market simulation (zero risk, uses live orderbook prices)
MODE = "live"


# =============================================================================
# 2. TAKE-PROFIT (TP) RULES
# =============================================================================
# Minimum Take-Profit rule: Number of pu (Price Unit / Tick Size) away from entry price.
# For TRUMP_USDT, 1 pu = 0.001 USDT.
# TP_TICKS = 1 -> TP = Entry Price + 1 * pu (for Long) or Entry Price - 1 * pu (for Short)
# TP_TICKS = 2 -> TP = Entry Price + 2 * pu (for Long) or Entry Price - 2 * pu (for Short)
TP_TICKS = 2


# =============================================================================
# 3. STOP-LOSS (SL) RULES & MODES
# =============================================================================
# Choose how the Stop Loss distance is determined:
#   "TICKS"     -> Fixed number of price units / ticks away from entry (RECOMMENDED)
#   "ROE"       -> Return on Equity / Margin loss percentage (e.g. 25.0% loss on margin)
#   "PRICE_PCT" -> Direct asset price movement percentage (e.g. 0.5% price drop)
SL_MODE = "TICKS"

# Setting for SL_MODE = "TICKS":
# Number of pu (tick size) away from entry price.
#   10 ticks = 0.0100 USDT offset (~0.42% price move) -> safe at <= 40x leverage
#   15 ticks = 0.0150 USDT offset (~0.64% price move) -> safe at <= 30x leverage
#   20 ticks = 0.0200 USDT offset (~0.85% price move) -> safe at <= 25x leverage
SL_TICKS = 10

# Setting for SL_MODE = "ROE":
# Percentage of margin committed to risk (e.g. 25.0 means max 25% loss of margin).
SL_ROE_PCT = 25.0

# Setting for SL_MODE = "PRICE_PCT":
# Direct percentage move in the underlying token price (e.g. 0.5 means 0.5% price move).
SL_PRICE_PCT = 0.5


# =============================================================================
# 4. LEVERAGE & MARGIN SETTINGS
# =============================================================================
# Position leverage multiplier.
#
# ⚠️ CRITICAL LEVERAGE & LIQUIDATION BUFFER CHEAT SHEET (TRUMP_USDT at 2.35 USDT):
#   Leverage | Liq Distance | Safe SL Max | 10% ROE Move | Margin (1 contract)
#   ---------+--------------+-------------+--------------+--------------------
#     75x    |  7.8 ticks   |   5 ticks   |  3.1 ticks   | 0.0031 USDT (INR 0.30)
#     50x    | 23.5 ticks   |  15 ticks   |  4.7 ticks   | 0.0047 USDT (INR 0.44)
#     30x    | 54.8 ticks   |  35 ticks   |  7.8 ticks   | 0.0079 USDT (INR 0.75) [Recommended]
#     20x    | 94.0 ticks   |  60 ticks   | 11.8 ticks   | 0.0118 USDT (INR 1.11)
#     10x    | 211.5 ticks  | 150 ticks   | 23.5 ticks   | 0.0235 USDT (INR 2.22)
LEVERAGE = 75

# Margin mode: True for Isolated (openType=1), False for Cross (openType=2).
# Isolated margin is strongly recommended to restrict risk strictly to position margin.
IS_ISOLATED = True


# =============================================================================
# 5. CYCLE TIMING & SESSION LIMITS
# =============================================================================
# Cooldown period in seconds to wait after a trade closes before opening the next trade.
# Allows the orderbook and ticker to stabilize after order closure.
COOLDOWN_SECONDS = 30.0

# Maximum number of trades to execute in this session.
# Set to 0 for UNLIMITED / continuous 24/7 automated operation until stopped.
MAX_TRADES = 3

# Ticker polling interval in seconds while actively monitoring an open trade.
# Faster polling (0.2s - 0.3s) ensures rapid detection of TP hits for immediate market close.
POLL_INTERVAL_SECONDS = 0.2


# =============================================================================
# 6. LOGGING DIRECTORIES & AUDIT FILES
# =============================================================================
LOGS_DIR = "logs"
REALTIME_LOG_FILE = "engine_realtime.log"     # Live stream of all engine events & price polls
OUTCOMES_LOG_FILE = "trade_outcomes.txt"      # Human-readable visual trade outcome journal cards
OUTCOMES_JSONL_FILE = "trade_outcomes.jsonl"  # Machine-readable JSONL audit trail of every trade

