# 🔬 Quantitative Experiment Report: PERM-TRUMP-05
## TRUMP Inverted Stoch RSI with Micro-Excursion Tick Ratchet

> **Research Domain:** Dual-Asset Permutation Matrix: TRUMP_USDT  
> **Execution Timestamp:** `2026-09-07 01:36:45 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `TRUMP_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `2 ticks TP` | Stop: `5 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `True` | Duration Safeguard: `False`
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
  "execution_style": "MAKER_HYBRID",
  "queue_dynamics": true,
  "maker_timeout": 10.0,
  "ratchet_enabled": true,
  "invert_signal": true,
  "leverage": 75,
  "fee_mode": "0.00% Zero Fees"
}
```

---

### 2. Empirical Results Table (4-Tier Slippage Stress Matrix)

| Slippage Tier | Total Trades | Win Rate (%) | Profit Factor | Net PnL (USDT) | Max DD (%) | Sharpe Ratio | Sortino Ratio | Liquidations | Expectancy (USDT) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0T (Maker Baseline)** | 1594 | 62.05% | **1.07** | **+0.0250** | 0.018% | 2.22 | 1.67 | 0 | +0.00002 |
| **1T ($0.00001 / $0.001)** | 1594 | 62.05% | **0.80** | **-0.0960** | 0.096% | -7.34 | -5.17 | 0 | -0.00006 |
| **2T ($0.00002 / $0.002)** | 1594 | 62.05% | **0.65** | **-0.2170** | 0.217% | -14.53 | -9.72 | 0 | -0.00014 |
| **3T ($0.00003 / $0.003)** | 1594 | 62.05% | **0.54** | **-0.3380** | 0.338% | -20.09 | -12.92 | 0 | -0.00021 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.1210 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.476 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1181 trades | Win Rate: 62.49% | Profit Factor: 1.03 | PnL: +0.0082 USDT
- **Out-of-Sample (30%):** 312 trades | Win Rate: 61.22% | Profit Factor: 1.25 | PnL: +0.0154 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.218` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.010%`

---

### 5. Key Insights & Decision
- Evaluated on TRUMP_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare TRUMP_USDT results against cross-asset baseline.
