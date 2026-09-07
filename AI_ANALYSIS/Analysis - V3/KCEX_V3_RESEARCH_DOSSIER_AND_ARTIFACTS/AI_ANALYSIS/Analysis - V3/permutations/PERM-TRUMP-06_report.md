# 🔬 Quantitative Experiment Report: PERM-TRUMP-06
## TRUMP Inverted Stoch RSI Pure Market Spread-Crossing Baseline

> **Research Domain:** Dual-Asset Permutation Matrix: TRUMP_USDT  
> **Execution Timestamp:** `2026-09-07 01:37:34 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `TRUMP_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `2 ticks TP` | Stop: `5 ticks SL`
- Execution Style: `PURE_MARKET` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "TRUMP_USDT",
  "timeframe": "1m",
  "strategy_mode": "STOCH_RSI",
  "tp_ticks": 2,
  "sl_ticks": 5,
  "execution_style": "PURE_MARKET",
  "queue_dynamics": false,
  "maker_timeout": 10.0,
  "ratchet_enabled": false,
  "invert_signal": true,
  "leverage": 75,
  "fee_mode": "0.00% Zero Fees"
}
```

---

### 2. Empirical Results Table (4-Tier Slippage Stress Matrix)

| Slippage Tier | Total Trades | Win Rate (%) | Profit Factor | Net PnL (USDT) | Max DD (%) | Sharpe Ratio | Sortino Ratio | Liquidations | Expectancy (USDT) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0T (Maker Baseline)** | 1819 | 77.35% | **1.37** | **+0.1508** | 0.008% | 11.00 | 6.45 | 0 | +0.00008 |
| **1T ($0.00001 / $0.001)** | 1646 | 61.48% | **0.53** | **-0.3560** | 0.356% | -21.59 | -14.02 | 0 | -0.00022 |
| **2T ($0.00002 / $0.002)** | 1634 | 42.96% | **0.22** | **-1.0240** | 1.024% | -54.68 | -34.81 | 0 | -0.00063 |
| **3T ($0.00003 / $0.003)** | 1758 | 27.19% | **0.09** | **-1.8568** | 1.857% | -92.28 | -51.34 | 0 | -0.00106 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.6692 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `0.338 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1373 trades | Win Rate: 76.26% | Profit Factor: 1.28 | PnL: +0.0928 USDT
- **Out-of-Sample (30%):** 325 trades | Win Rate: 81.85% | Profit Factor: 1.80 | PnL: +0.0474 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.404` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.007%`

---

### 5. Key Insights & Decision
- Evaluated on TRUMP_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare TRUMP_USDT results against cross-asset baseline.
