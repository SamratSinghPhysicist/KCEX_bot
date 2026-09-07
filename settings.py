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

# Default volume sizing: 2x min for TRUMP_USDT, 1x min for DOGE_USDT
VOLUME_MULTIPLIER = 2.0

# If VOLUME_MODE == "CONTRACTS":
# Exact number of contracts (must be >= contract min_volume, which is 1 for TRUMP)
VOLUME_CONTRACTS = 2


def get_default_quantity_for_symbol(symbol: str) -> tuple[str, float]:
    """
    Returns default (volume_mode, volume_value) tailored per symbol:
    - TRUMP_USDT: 2x minimum volume (2 contracts / 2.0x multiplier)
    - DOGE_USDT : 1x minimum volume (1 contract / 1.0x multiplier)
    - Others    : 1.0x minimum multiplier
    """
    s = str(symbol).upper()
    if "TRUMP" in s:
        return ("MULTIPLIER", 2.0)
    elif "DOGE" in s:
        return ("MULTIPLIER", 1.0)
    return ("MULTIPLIER", 1.0)


# =============================================================================
# 3. TAKE-PROFIT (TP) RULES
# =============================================================================
# Minimum Take-Profit rule: Number of pu (Price Unit / Tick Size) away from entry price.
# For TRUMP_USDT, 1 pu = 0.001 USDT.
# TP_TICKS = 1 -> TP = Entry Price + 1 * pu (for Long) or Entry Price - 1 * pu (for Short)
# TP_TICKS = 2 -> TP = Entry Price + 2 * pu (for Long) or Entry Price - 2 * pu (for Short)
TP_TICKS = 2

# Dynamic TP Scaling:
# False (RECOMMENDED) -> Strictly locks Take Profit to TP_TICKS (e.g. 2 pu scalp is always closed at +2 pu).
# True                -> Allows microstructure signals to scale TP dynamically (1 to 3 pu) on strong confluence.
DYNAMIC_TP = False


# =============================================================================
# 4. STOP-LOSS (SL) RULES & MODES
# =============================================================================
# Choose how the Stop Loss distance is determined:
#   "ROE"       -> Return on Equity / Margin loss percentage (e.g. 25.0% loss on margin) [Default]
#   "TICKS"     -> Fixed number of price units / ticks away from entry
#   "PRICE_PCT" -> Direct asset price movement percentage (e.g. 0.5% price drop)
SL_MODE = "ROE"

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
# Note: At 75x leverage, 25% ROE loss represents a 0.333% price move (approx ~7.8 ticks for TRUMP).
# In case of conflict between liquidation and SL, 75x leverage is strictly prioritized.
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
#   "SMART_STRATEGY" -> Autonomous Regime-Adaptive Strategy (Switches Momentum EMA / Range Stoch RSI)
#   "STOCH_RSI"      -> Stochastic RSI Fast Scalp & Reversal Strategy [Default]
#   "EMA_CROSSOVER"  -> Fast / Slow EMA Crossover Strategy (5/13, 9/21, 3/8)
STRATEGY_MODE = "STOCH_RSI"

# -----------------------------------------------------------------------------
# Order Execution Type & Slippage Protection
# -----------------------------------------------------------------------------
# "MARKET" -> Immediate taker fill (standard execution)
# "LIMIT"  -> Post-only Maker entry at best bid/ask with timeout cancellation (zero taker slippage)
ORDER_TYPE = "MARKET"
LIMIT_ORDER_TIMEOUT_SECONDS = 10.0

# -----------------------------------------------------------------------------
# Smart Strategy Configuration (Regime-Adaptive Scalping Engine)
# -----------------------------------------------------------------------------
# Dynamically classifies 1m market microstructure into 5 regimes:
# - STRONG_BULL_MOMENTUM / STRONG_BEAR_MOMENTUM -> Routes to EMA Crossover
# - BALANCED_RANGE                              -> Routes to Stochastic RSI
# - SUB_ATR_COMPRESSION / VOLATILITY_CLIMAX     -> Pauses execution safely
SMART_ATR_FILTER_ENABLED = True          # True = blocks entries when volatility is too compressed
SMART_MIN_ATR_TICKS = 2.5                # Minimum 1m ATR in ticks required for target traversability
SMART_CHOP_CEILING = 58.0                # Choppiness Index ceiling (above 58.0 = erratic chop)
SMART_ADX_TREND_THRESHOLD = 26.0         # ADX threshold for strong directional momentum
SMART_USE_EMA200_FILTER = False          # 200 EMA direction lock (Default OFF per empirical validation)
SMART_CLIMAX_FILTER_ENABLED = True       # True = suppresses entries during parabolic range surges
SMART_MAX_ATR_EXPANSION = 2.2            # Candle range > 2.2x ATR is considered climax
SMART_EMA_PRESET = "5/13"                # Fast/Slow EMA preset when in momentum regime
SMART_STOCH_PRESET = "FAST_SCALP"        # Stoch RSI preset when in balanced range regime
SMART_INTERVAL = "Min1"
SMART_REQUIRE_CLOSED_CANDLE = True


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
# Stochastic RSI Strategy Configuration (Option 2)
# -----------------------------------------------------------------------------
# Presets:
#   "FAST_SCALP"  -> RSI 9, Stoch 9, %K 3, %D 3, Oversold 20, Overbought 80 [Recommended for HFT]
#   "STANDARD"    -> RSI 14, Stoch 14, %K 3, %D 3, Oversold 20, Overbought 80 [Classic]
#   "MICRO_BURST" -> RSI 7, Stoch 7, %K 3, %D 3, Oversold 15, Overbought 85 [Extreme Reversals]
#   "custom"      -> Uses individual parameters below
STOCH_PRESET = "FAST_SCALP"
STOCH_RSI_PERIOD = 9
STOCH_PERIOD = 9
STOCH_K_PERIOD = 3
STOCH_D_PERIOD = 3
STOCH_OVERSOLD = 20.0
STOCH_OVERBOUGHT = 80.0

# Candle timeframe for StochRSI: "Min1" (1-minute), "Min5", "Min15"
STOCH_INTERVAL = "Min1"

# Zone Gating:
# True (RECOMMENDED) -> Only triggers %K/%D crossover in or exiting from extreme zones (<=20 / >=80).
# False              -> Triggers crossovers anywhere across the 0-100 oscillator spectrum.
STOCH_ZONE_FILTER = True

# Confirmation on completed candle close:
STOCH_REQUIRE_CLOSED_CANDLE = True

# Autonomous trading direction for StochRSI strategy:
# True  -> Scalps BOTH Long (Oversold bounce) and Short (Overbought rejection) dynamically.
# False -> Restricts scalps strictly to the DIRECTION specified in Section 1.
STOCH_BI_DIRECTIONAL = True


# =============================================================================
# 8. TRADE OPTIMIZATION & REGIME FILTERS (OPTIONAL / TOGGLEABLE)
# =============================================================================
# 1. Trade Duration Monitoring & Time-Decay Safeguards
# Solves statistical degradation where trades lasting >60s drift toward the full -25% ROE stop.
DURATION_FILTER_ENABLED = False          # False = Standard unmonitored hold; True = Enables duration safeguards
DURATION_DEEP_MONITOR_SECONDS = 60.0     # Engages high-priority monitoring after 60s
DURATION_MAX_HOLD_SECONDS = 90.0         # Hard time-stop timeout: triggers exit action after 90s
DURATION_ACTION = "CLOSE"                # "CLOSE" (market exit), "SCRATCH_OR_MARKET" (exit if >= -1 tick), or "TIGHTEN_SL"

# 2. ADX / Volatility Chop Filter
# Suppresses entries during non-directional, choppy sideways markets.
ADX_FILTER_ENABLED = False               # False = Disabled; True = Suppresses signals when ADX < ADX_THRESHOLD
ADX_PERIOD = 14
ADX_THRESHOLD = 25.0

# 3. Higher-Timeframe (HTF) 200 EMA Macro Trend Filter
# Restricts micro-scalps to trade strictly in alignment with the dominant trend:
# Longs only when price >= HTF EMA; Shorts only when price <= HTF EMA.
HTF_TREND_FILTER_ENABLED = False
HTF_TIMEFRAME = "15m"
HTF_EMA_PERIOD = 200

# 4. Hourly Session Blacklist (Dead-Zone Filter)
# Blocks trade entry during historically erratic, low-liquidity UTC hours.
HOURLY_FILTER_ENABLED = False
HOURLY_BLACKLIST_UTC = [2, 3, 4, 5, 17]  # UTC hours to block (e.g. 02:00-05:00, 17:00 UTC)

# 5. Directional Bias Policy
# "BOTH"       -> Bi-directional scalping (Longs & Shorts)
# "LONG_ONLY"  -> Restricts all trades strictly to Long positions
# "SHORT_ONLY" -> Restricts all trades strictly to Short positions
DIRECTION_BIAS = "BOTH"


# =============================================================================
# 9. LOGGING DIRECTORIES & AUDIT FILES
# =============================================================================
LOGS_DIR = "logs"
REALTIME_LOG_FILE = "engine_realtime.log"     # Live stream of all engine events & price polls
OUTCOMES_LOG_FILE = "trade_outcomes.txt"      # Human-readable visual trade outcome journal cards
OUTCOMES_JSONL_FILE = "trade_outcomes.jsonl"  # Machine-readable JSONL audit trail of every trade


# =============================================================================
# 10. QUANTITATIVE RESEARCH PRESET REGISTRY & OPTIMIZATION TOGGLES
# =============================================================================
# Select an active strategy preset by its self-documenting name:
#
#   1. "DOGE_V2_2_RATCHET_CHAMPION"
#      • Phase V2.2 Full 8-Month Macro Backtest (48,178 trades):
#      • Net Profit (0T Maker Hybrid): +$2.14 USDT (Profitable with 0 slippage / Maker execution)
#      • Slippage Sensitivity: 1T (-$4.92 USDT Loss), 2T (-$11.98 USDT Loss), 3T (-$19.04 USDT Loss)
#      • Setup: DOGE_USDT, Inverted Stoch RSI, 5t TP / 2t SL, Micro-Excursion Tick Ratchet
#      • Execution: Maker Limit Entry at bid1/ask1 (10s timeout) + Resting Limit TP (0 slippage)
#
#   2. "DOGE_ASYMMETRIC_MOMENTUM_10T2T"
#      • Asymmetric 5:1 Reward-to-Risk Setup: 10t TP / 2t SL, Direct Stoch RSI momentum
#      • Net Profit: +$3.00 USDT, Profit Factor: 1.20, Sortino: 12.69
#
#   3. "TRUMP_LEGACY_BASELINE"
#      • TRUMP_USDT, Direct Stoch RSI, 2t TP / 25% ROE SL (~7.8 ticks), Pure Market execution
#      • Net Profit: +$0.39 USDT, Profit Factor: 1.02, Sortino: 1.15
#
#   4. "CUSTOM"
#      • Ignores preset overrides; uses the individual toggle parameters configured below.
#
ACTIVE_PRESET = "DOGE_V2_2_RATCHET_CHAMPION"

# -----------------------------------------------------------------------------
# Individual Modular Feature Toggles (Used when ACTIVE_PRESET = "CUSTOM")
# -----------------------------------------------------------------------------
# 1. Signal Direction Inversion (Exhaustion Fading)
# When True: Stoch RSI overbought cross triggers LONG; oversold cross triggers SHORT.
# Discovered in Phase V2.1: +61% to +84% PF increase in consolidation/range regimes.
INVERT_SIGNAL = True

# 2. Dynamic Regime Fading
# Automatically inverts signals in consolidation (ADX < cutoff) while preserving direct
# momentum signals in strong breakouts (ADX >= cutoff).
DYNAMIC_REGIME_FADING = False
ADX_FADING_CUTOFF = 25.0

# 3. Order Execution Style & Slippage Elimination
# "MAKER_HYBRID" -> Places post-only Maker limit order at bid1/ask1 with queue timeout
#                   and rests Take-Profit limit orders (0.00 ticks slippage).
# "PURE_MARKET"  -> Legacy market order taker execution.
EXECUTION_STYLE = "MAKER_HYBRID"
MAKER_QUEUE_TIMEOUT_SECONDS = 10.0
RESTING_LIMIT_TP = True

# 4. Phase V2.2 Champion Micro-Excursion Tick Ratchet
# In-position trailing stop protection based on millisecond Maximum Favorable Excursion (MFE):
# • Tier 1: When MFE >= +1.0t and position stalls >= 10.0s -> Tighten SL to -1.0t
# • Tier 2: When MFE >= +2.5t -> Lock SL to Breakeven (0.0t)
RATCHET_ENABLED = True
RATCHET_TRIGGER_TICKS = 1.0
RATCHET_STALL_SECONDS = 10.0
RATCHET_TIGHTEN_TICKS = 1.0
RATCHET_BREAKEVEN_TICKS = 2.5

# 5. Realistic Slippage Engine (Dry-Run and Backtesting)
# Enables adverse execution friction penalties (e.g. 1 tick, 2 ticks, 3 ticks adverse).
SLIPPAGE_ENABLED = False
SLIPPAGE_TICKS = 0


# =============================================================================
# STRATEGY PRESET DEFINITIONS (Complete Configurations & Backtest Records)
# =============================================================================
STRATEGY_PRESETS = {
    "DOGE_V2_2_RATCHET_CHAMPION": {
        "name": "DOGE V2.2 Tick Ratchet Champion (Phase V2.2 Deep Dive Winner)",
        "description": (
            "Multi-stage micro-excursion ratchet trailing stop combined with inverted "
            "Stoch RSI exhaustion fading and maker limit execution on DOGE_USDT."
        ),
        "symbol": "DOGE_USDT",
        "strategy_mode": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "timeframe": "1m",
        "invert_signal": True,
        "dynamic_regime_fading": False,
        "adx_fading_cutoff": 25.0,
        "tp_ticks": 5,
        "sl_mode": "TICKS",
        "sl_ticks": 2,
        "ratchet_enabled": True,
        "ratchet_trigger_ticks": 1.0,
        "ratchet_stall_seconds": 10.0,
        "ratchet_tighten_ticks": 1.0,
        "ratchet_breakeven_ticks": 2.5,
        "execution_style": "MAKER_HYBRID",
        "maker_queue_timeout_seconds": 10.0,
        "resting_limit_tp": True,
        "slippage_enabled": False,
        "slippage_ticks": 0,
        "backtest_config": {
            "initial_capital_usdt": 100.0,
            "leverage": 75,
            "margin_mode": "ISOLATED",
            "fee_schedule": "0.00% Maker / 0.00% Taker (KCEX Zero-Fee Contract)",
            "data_feed": "High-Fidelity Binance Millisecond Tick Trades Data",
            "contract_size": 1.0,
            "tick_size_pu": 0.0001,
            "volume": "1x min volume (1 contract = 1.0 DOGE)",
            "execution": "Maker Limit bid1/ask1 (10s timeout), Resting Limit TP (0 slippage)"
        },
        "backtest_results_by_slippage": {
            "slippage_0t": {
                "net_profit_usdt": 2.14,
                "profit_factor": 1.08,
                "sortino_ratio": 3.82,
                "max_drawdown_pct": -0.014,
                "total_trades": 48178,
                "verdict": "Profitable Under Zero Slippage / Maker Hybrid (+$2.14 USDT)"
            },
            "slippage_1t": {
                "net_profit_usdt": -4.92,
                "profit_factor": 0.86,
                "sortino_ratio": -1.82,
                "max_drawdown_pct": -0.049,
                "verdict": "Unprofitable with 1T Stop Friction (-$4.92 USDT Net Loss) - Demands Maker Execution"
            },
            "slippage_2t": {
                "net_profit_usdt": -11.98,
                "profit_factor": 0.72,
                "sortino_ratio": -3.45,
                "max_drawdown_pct": -0.120,
                "verdict": "Negative Expectancy with 2T Friction (-$11.98 USDT Net Loss)"
            },
            "slippage_3t": {
                "net_profit_usdt": -19.04,
                "profit_factor": 0.61,
                "sortino_ratio": -5.12,
                "max_drawdown_pct": -0.190,
                "verdict": "High Friction Degradation (-$19.04 USDT Net Loss)"
            }
        }
    },
    "DOGE_ASYMMETRIC_MOMENTUM_10T2T": {
        "name": "DOGE Asymmetric Momentum Scalp (10t TP / 2t SL)",
        "description": (
            "High-asymmetry 5:1 reward-to-risk scalp capturing multi-tick volatility bursts "
            "using direct Stoch RSI momentum without signal inversion."
        ),
        "symbol": "DOGE_USDT",
        "strategy_mode": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "timeframe": "1m",
        "invert_signal": False,
        "dynamic_regime_fading": False,
        "adx_fading_cutoff": 25.0,
        "tp_ticks": 10,
        "sl_mode": "TICKS",
        "sl_ticks": 2,
        "ratchet_enabled": False,
        "execution_style": "MAKER_HYBRID",
        "maker_queue_timeout_seconds": 10.0,
        "resting_limit_tp": True,
        "slippage_enabled": False,
        "slippage_ticks": 0,
        "backtest_config": {
            "initial_capital_usdt": 100.0,
            "leverage": 75,
            "margin_mode": "ISOLATED",
            "fee_schedule": "0.00% Maker / 0.00% Taker",
            "data_feed": "High-Fidelity Binance Millisecond Tick Trades Data",
            "contract_size": 1.0,
            "tick_size_pu": 0.0001,
            "volume": "1x min volume (1 DOGE)"
        },
        "backtest_results_by_slippage": {
            "slippage_0t": {
                "net_profit_usdt": 3.00,
                "profit_factor": 1.20,
                "sortino_ratio": 12.69,
                "max_drawdown_pct": -0.046,
                "win_rate_pct": 21.6,
                "verdict": "Strong Asymmetric Expectancy"
            },
            "slippage_1t": {
                "net_profit_usdt": -0.23,
                "profit_factor": 0.98,
                "sortino_ratio": -0.15,
                "max_drawdown_pct": -0.065,
                "verdict": "Marginal Drawdown (Breakeven threshold S_max = 0.834 ticks)"
            }
        }
    },
    "TRUMP_LEGACY_BASELINE": {
        "name": "TRUMP Legacy Baseline (Original 2t TP / 25% ROE SL Setup)",
        "description": "Original baseline configuration on TRUMP_USDT using direct Stoch RSI and market taker orders.",
        "symbol": "TRUMP_USDT",
        "strategy_mode": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "timeframe": "1m",
        "invert_signal": False,
        "dynamic_regime_fading": False,
        "adx_fading_cutoff": 25.0,
        "tp_ticks": 2,
        "sl_mode": "ROE",
        "sl_roe_pct": 25.0,
        "sl_ticks": 10,
        "ratchet_enabled": False,
        "execution_style": "PURE_MARKET",
        "maker_queue_timeout_seconds": 10.0,
        "resting_limit_tp": False,
        "slippage_enabled": False,
        "slippage_ticks": 0,
        "backtest_config": {
            "initial_capital_usdt": 100.0,
            "leverage": 75,
            "margin_mode": "ISOLATED",
            "fee_schedule": "0.00% Maker / 0.00% Taker",
            "data_feed": "High-Fidelity Binance Millisecond Tick Trades Data",
            "contract_size": 0.1,
            "tick_size_pu": 0.001,
            "volume": "2x min volume (2 contracts = 0.2 TRUMP)"
        },
        "backtest_results_by_slippage": {
            "slippage_0t": {
                "net_profit_usdt": 0.39,
                "profit_factor": 1.02,
                "sortino_ratio": 1.15,
                "max_drawdown_pct": -0.089,
                "win_rate_pct": 79.4,
                "verdict": "Marginal Baseline (High WR, fragile risk/reward)"
            },
            "slippage_1t": {
                "net_profit_usdt": -11.45,
                "profit_factor": 0.65,
                "sortino_ratio": -8.50,
                "max_drawdown_pct": -0.210,
                "verdict": "Severely Degraded (2t TP / 8t SL cannot withstand market order slippage)"
            }
        }
    },
    "CUSTOM": {
        "name": "Custom User Configuration",
        "description": "Bypasses presets and uses manual individual toggle variables from settings.py.",
        "symbol": SYMBOL,
        "strategy_mode": STRATEGY_MODE
    }
}


def get_active_preset_config(preset_name: str = None) -> dict:
    """
    Returns the resolved configuration dictionary for the specified or ACTIVE_PRESET.
    Falls back to individual variables if preset is 'CUSTOM' or unrecognized.
    """
    key = (preset_name or ACTIVE_PRESET).upper()
    if key in STRATEGY_PRESETS and key != "CUSTOM":
        return STRATEGY_PRESETS[key]
    return {
        "name": "Custom Manual Configuration",
        "symbol": SYMBOL,
        "strategy_mode": STRATEGY_MODE,
        "invert_signal": INVERT_SIGNAL,
        "dynamic_regime_fading": DYNAMIC_REGIME_FADING,
        "adx_fading_cutoff": ADX_FADING_CUTOFF,
        "execution_style": EXECUTION_STYLE,
        "maker_queue_timeout_seconds": MAKER_QUEUE_TIMEOUT_SECONDS,
        "resting_limit_tp": RESTING_LIMIT_TP,
        "ratchet_enabled": RATCHET_ENABLED,
        "ratchet_trigger_ticks": RATCHET_TRIGGER_TICKS,
        "ratchet_stall_seconds": RATCHET_STALL_SECONDS,
        "ratchet_tighten_ticks": RATCHET_TIGHTEN_TICKS,
        "ratchet_breakeven_ticks": RATCHET_BREAKEVEN_TICKS,
        "slippage_enabled": SLIPPAGE_ENABLED,
        "slippage_ticks": SLIPPAGE_TICKS,
        "tp_ticks": TP_TICKS,
        "sl_mode": SL_MODE,
        "sl_ticks": SL_TICKS,
        "sl_roe_pct": SL_ROE_PCT
    }



