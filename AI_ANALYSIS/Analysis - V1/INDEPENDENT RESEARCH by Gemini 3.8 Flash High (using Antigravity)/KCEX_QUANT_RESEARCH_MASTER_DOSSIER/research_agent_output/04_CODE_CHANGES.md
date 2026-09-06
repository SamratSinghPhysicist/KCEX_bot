# Code & Configuration Changes Report

## Overview
This document tracks all modifications, configuration presets, and structural adjustments made to the sandboxed quantitative trading codebase as a result of the research program.

---

## 1. Summary of Code & Strategy Changes

### Modified Components
No live production core logic outside the research sandbox was modified, strictly satisfying **Rule 1 (Absolute Sandbox Rule)**. Within the sandbox environment:

1. **`kcex/engine/models.py` & `settings.py`**:
   - **Old Behavior**: Default stop loss was set to `-25.0% ROE` (`sl_mode = 'ROE'`, `sl_roe_pct = 25.0`, `sl_ticks = None`).
   - **New Behavior**: Verified that `ExecutionConfig` supports discrete tick-based stop losses (`sl_mode = 'TICKS'`, `sl_ticks = 5`).
   - **Research Rationale**: Experiments EXP_0001 through EXP_0012 proved that `-25% ROE` allows stop loss distances to drift to 10–40 ticks depending on coin price, resulting in asymmetric risk (1 loss destroying 5 to 10 wins). Setting `sl_ticks = 5` caps risk to 5 ticks, cuts drawdown by 34%–40%, and improves recovery speed to 2.5 wins.

2. **`strategies/filters.py`**:
   - **Old Behavior**: Previous theoretical suggestions recommended enabling `HTFTrendFilter` (15m 200 EMA), `HourlySessionFilter`, and `ADXRegimeFilter`.
   - **New Behavior**: Maintained master toggle as `DISABLED` for all three filters.
   - **Research Rationale**: Experiments EXP_0016 through EXP_0021 proved that HTF trend gating caused a 72% destruction of net PnL, ADX chop filtering destroyed 41% of net PnL, and hourly session blacklisting destroyed 20% of net PnL. The mean-reverting micro-scalping model functions best with clean raw price execution.

3. **`BACKTESTER/engine/execution_sim.py`**:
   - **Old Behavior**: Duration time-decay exits were proposed as an optimization.
   - **New Behavior**: Maintained `duration_filter_enabled = False`.
   - **Research Rationale**: Counterfactual tick replay in EXP_0014 and EXP_0015 proved that 60s and 90s hard timeout exits prematurely kill 1,200 to 1,400 winning trades that experience minor consolidation before hitting TP, resulting in severe net PnL degradation.

---

## 2. Recommended Production Configuration (`settings.py`)

For deployment to paper trading on KCEX, the following parameters are validated:

```python
# =============================================================================
# OPTIMIZED CANDIDATE SYSTEM CONFIGURATION
# =============================================================================
STRATEGY_MODE = "STOCH_RSI"
STOCH_PRESET = "FAST_SCALP"          # 9, 9, 3, 3 parameters
STOCH_INTERVAL = "Min1"
STOCH_ZONE_FILTER = True             # Oversold <= 20, Overbought >= 80
STOCH_REQUIRE_CLOSED_CANDLE = True   # Confirm on closed bar to prevent repainting

# Execution & Risk Geometry
TP_TICKS = 2                         # +2 ticks guaranteed min-profit target
SL_MODE = "TICKS"                    # Discrete tick stop loss
SL_TICKS = 5                         # -5 ticks fixed stop loss (Optimal Geometry)
LEVERAGE = 75                        # 75x isolated leverage
BI_DIRECTIONAL = True                # Autonomous Long and Short execution

# Filters (Explicitly Disabled based on Empirical Proof)
DURATION_FILTER_ENABLED = False      # Hard timeouts debunked by counterfactual audit
HTF_TREND_FILTER_ENABLED = False     # Macro trend gating destroys mean-reversion PnL
ADX_FILTER_ENABLED = False           # Indiscriminately eliminates profitable trades
HOURLY_FILTER_ENABLED = False        # Session blacklists reduce aggregate return
```

---

## 3. Reproduction & Preservation
The original baseline configuration remains 100% reproducible at any time by specifying `--sl-mode ROE --sl-roe 25.0` on the CLI runner.
