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

import os

# =============================================================================
# 1. TRADING PAIR & ASSET CONFIGURATION
# =============================================================================
# Select any KCEX futures pair (e.g. TRUMP_USDT, DOGE_USDT, BTC_USDT, ETH_USDT, SOL_USDT, PEPE_USDT).
# Pairs like TRUMP_USDT and DOGE_USDT enjoy 0% maker and 0% taker fees.
# Other pairs operate under standard exchange fee tiers (e.g. 0.01% taker).
# Can also be overridden via the KCEX_SYMBOL environment variable.
SYMBOL = os.getenv("KCEX_SYMBOL", "TRUMP_USDT")

# Default order direction: "LONG" or "SHORT"
# The engine's directional cycle sub-strategy will execute trades in this direction.
DIRECTION = "LONG"

# Default execution mode:
# "live"    -> Real trades using KCEX futures wallet balance (requires API token in .env)
# "dry-run" -> Real-time market simulation (zero risk, uses live orderbook prices)
MODE = "live"


# =============================================================================
# 2. TRADE QUANTITY / VOLUME CONFIGURATION (POSITION SIZING)
# =============================================================================
# ⚠️ CRITICAL DISTINCTION: TRADE QUANTITY (VOLUME) IS NOT THE SAME AS MARGIN!
#
# • Trade Quantity (Notional Value):
#     The total market value/exposure of your position in USDT.
#     Formula: Trade Quantity = Volume (contracts) * Contract Size * Entry Price
#     Example (TRUMP_USDT at 2.35 USDT, Contract Size = 0.1 TRUMP coins):
#       - 1 contract  = 0.1 coins = ~0.235 USDT Trade Quantity
#       - 2 contracts = 0.2 coins = ~0.470 USDT Trade Quantity
#       - 5 contracts = 0.5 coins = ~1.175 USDT Trade Quantity
#
# • Committed Margin (Cash from Wallet):
#     The actual collateral deducted from your KCEX wallet balance to hold the trade.
#     Formula: Margin Required = Trade Quantity / Leverage
#     Example (at 75x leverage):
#       - 1 contract  margin = 0.235 USDT / 75 = ~0.0031 USDT (INR ~0.30)
#       - 2 contracts margin = 0.470 USDT / 75 = ~0.0063 USDT (INR ~0.60)
#       - 5 contracts margin = 1.175 USDT / 75 = ~0.0157 USDT (INR ~1.48)
#
# Configuration Modes:
#   "MIN"        -> Always execute exactly minimum possible quantity (1x min_volume).
#   "MULTIPLIER" -> Execute x times the contract's minimum volume (e.g. 1.0, 2.0, 5.0).
#   "CONTRACTS"  -> Execute an exact integer number of contracts (e.g. 1, 2, 5).
VOLUME_MODE = "MULTIPLIER"  # "MIN", "MULTIPLIER", or "CONTRACTS"

# If VOLUME_MODE == "MULTIPLIER":
# Multiplier of min_volume (e.g. 1.0 = 1x min, 2.0 = 2x min, 5.0 = 5x min quantity)
VOLUME_MULTIPLIER = 1.0

# If VOLUME_MODE == "CONTRACTS":
# Exact number of contracts (must be >= contract min_volume, which is 1 for TRUMP)
VOLUME_CONTRACTS = 1


# =============================================================================
# 3. TAKE-PROFIT (TP) RULES
# =============================================================================
# Minimum Take-Profit rule: Number of pu (Price Unit / Tick Size) away from entry price.
# For TRUMP_USDT, 1 pu = 0.001 USDT.
# TP_TICKS = 1 -> TP = Entry Price + 1 * pu (for Long) or Entry Price - 1 * pu (for Short)
# TP_TICKS = 2 -> TP = Entry Price + 2 * pu (for Long) or Entry Price - 2 * pu (for Short)
TP_TICKS = 1

# Dynamic TP Scaling:
# False (RECOMMENDED) -> Strictly locks Take Profit to TP_TICKS (e.g. 1 pu scalp is always closed at +1 pu).
# True                -> Allows microstructure signals to scale TP dynamically (1 to 3 pu) on strong confluence.
DYNAMIC_TP = False


# =============================================================================
# 4. STOP-LOSS (SL) RULES & MODES
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
# 5. LEVERAGE & MARGIN SETTINGS
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
# 6. CYCLE TIMING & SESSION LIMITS
# =============================================================================
# Cooldown period in seconds to wait after a trade closes before opening the next trade.
COOLDOWN_SECONDS = 10.0

# Maximum number of trades to execute in this session.
# Set to 0 for UNLIMITED / continuous 24/7 automated operation until stopped.
MAX_TRADES = 3

# Ticker polling interval in seconds while actively monitoring an open trade.
# Faster polling (0.2s - 0.3s) ensures rapid detection of TP hits for immediate market close.
POLL_INTERVAL_SECONDS = 0.2


# =============================================================================
# 7. STRATEGY SELECTION & INDICATOR SETTINGS
# =============================================================================
# Strategy mode selection:
#   "EMA_CROSSOVER"  -> Fast / Slow EMA Crossover Strategy (5/13, 9/21, 3/8) [Default / Recommended]
#   "MICROSTRUCTURE" -> High-Frequency Market Microstructure (Autonomous Order Book & Tape Imbalance)
#   "CYCLE"          -> Directional Cycle (Classic fixed-direction Long/Short cycle)
STRATEGY_MODE = "EMA_CROSSOVER"

# -----------------------------------------------------------------------------
# EMA Crossover Configuration
# -----------------------------------------------------------------------------
# EMA Presets:
#   "5/13" -> Fast 5, Slow 13 (Fibonacci Scalp, highly responsive) [Default]
#   "9/21" -> Fast 9, Slow 21 (Momentum / Intraday Trend Scalp)
#   "3/8"  -> Fast 3, Slow 8  (Ultra-Fast Micro-Scalp)
#   "custom" -> Uses EMA_FAST and EMA_SLOW below
EMA_PRESET = "5/13"
EMA_FAST = 5
EMA_SLOW = 13

# Candle timeframe for EMA calculation: "Min1" (1-minute), "Min5" (5-minute), "Min15", etc.
EMA_INTERVAL = "Min1"

# Confirmation on completed candle close:
# True (RECOMMENDED) -> Only triggers on closed candle cross to prevent repainting/whipsaws.
# False              -> Triggers in real-time mid-bar on latest tick.
EMA_REQUIRE_CLOSED_CANDLE = True

# Autonomous trading direction for EMA Crossover strategy:
# True  -> Scalps BOTH Long (Golden Cross) and Short (Death Cross) dynamically.
# False -> Restricts scalps strictly to the DIRECTION specified in Section 1.
EMA_BI_DIRECTIONAL = True

# -----------------------------------------------------------------------------
# Microstructure Strategy Configuration
# -----------------------------------------------------------------------------
# Autonomous trading direction for Microstructure strategy:
# True  -> Scalps BOTH Long and Short dynamically as market order flow tilts.
# False -> Restricts scalps strictly to the DIRECTION specified in Section 1.
MICRO_BI_DIRECTIONAL = True

# Microstructure signal calibration (standard deviations in z-space):
MICRO_OBI_Z = 1.6           # Order Book Imbalance z-score threshold
MICRO_DELTA_Z = 1.8         # Trade Delta burst z-score threshold
MICRO_VAMP_Z = 1.5          # Volume-Adjusted Midpoint (micro-price) z-score threshold
MICRO_MIN_CONFLUENCE = 2    # Number of signals that must agree (>= 2 of 3)
MICRO_BURST_RECENCY = 0.35  # Fraction of 2s volume concentrated in last 0.5s burst
MICRO_MAX_SPREAD_TICKS = 1.5 # Max allowed spread in pu ticks before suppressing signals


# =============================================================================
# 8. LOGGING DIRECTORIES & AUDIT FILES
# =============================================================================
LOGS_DIR = "logs"
REALTIME_LOG_FILE = "engine_realtime.log"     # Live stream of all engine events & price polls
OUTCOMES_LOG_FILE = "trade_outcomes.txt"      # Human-readable visual trade outcome journal cards
OUTCOMES_JSONL_FILE = "trade_outcomes.jsonl"  # Machine-readable JSONL audit trail of every trade


