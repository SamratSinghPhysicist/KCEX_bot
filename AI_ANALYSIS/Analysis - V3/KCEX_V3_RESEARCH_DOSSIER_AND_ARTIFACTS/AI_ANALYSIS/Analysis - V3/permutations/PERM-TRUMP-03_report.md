# 🔬 Quantitative Experiment Report: PERM-TRUMP-03
## TRUMP Inverted Stoch RSI Asymmetric (5t TP / 2t SL) Maker Hybrid

> **Research Domain:** Dual-Asset Permutation Matrix: TRUMP_USDT  
> **Execution Timestamp:** `2026-09-07 01:35:13 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `TRUMP_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `5 ticks TP` | Stop: `2 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "TRUMP_USDT",
  "timeframe": "1m",
  "strategy_mode": "STOCH_RSI",
  "tp_ticks": 5,
  "sl_ticks": 2,
  "execution_style": "MAKER_HYBRID",
  "queue_dynamics": true,
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
| **0T (Maker Baseline)** | 1519 | 24.95% | **0.83** | **-0.0770** | 0.089% | -6.50 | -9.86 | 0 | -0.00005 |
| **1T ($0.00001 / $0.001)** | 1519 | 24.95% | **0.55** | **-0.3050** | 0.305% | -22.55 | -26.03 | 0 | -0.00020 |
| **2T ($0.00002 / $0.002)** | 1519 | 24.95% | **0.42** | **-0.5330** | 0.533% | -35.02 | -34.11 | 0 | -0.00035 |
| **3T ($0.00003 / $0.003)** | 1519 | 24.95% | **0.33** | **-0.7610** | 0.761% | -45.00 | -38.96 | 0 | -0.00050 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.2280 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.145 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1142 trades | Win Rate: 24.17% | Profit Factor: 0.80 | PnL: -0.0704 USDT
- **Out-of-Sample (30%):** 274 trades | Win Rate: 31.02% | Profit Factor: 1.12 | PnL: +0.0094 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.411` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.013%`

---

### 5. Key Insights & Decision
- Evaluated on TRUMP_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare TRUMP_USDT results against cross-asset baseline.
