# 🔬 Quantitative Experiment Report: PERM-TRUMP-04
## TRUMP EMA Crossover (5/13) (2t TP / 5t SL) Maker Hybrid

> **Research Domain:** Dual-Asset Permutation Matrix: TRUMP_USDT  
> **Execution Timestamp:** `2026-09-07 01:35:45 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `TRUMP_USDT` | Strategy: `EMA_CROSSOVER` | Polarity: `Direct (Momentum)`
- Target: `2 ticks TP` | Stop: `5 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "TRUMP_USDT",
  "timeframe": "1m",
  "strategy_mode": "EMA_CROSSOVER",
  "tp_ticks": 2,
  "sl_ticks": 5,
  "execution_style": "MAKER_HYBRID",
  "queue_dynamics": true,
  "maker_timeout": 10.0,
  "ratchet_enabled": false,
  "invert_signal": false,
  "leverage": 75,
  "fee_mode": "0.00% Zero Fees"
}
```

---

### 2. Empirical Results Table (4-Tier Slippage Stress Matrix)

| Slippage Tier | Total Trades | Win Rate (%) | Profit Factor | Net PnL (USDT) | Max DD (%) | Sharpe Ratio | Sortino Ratio | Liquidations | Expectancy (USDT) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0T (Maker Baseline)** | 876 | 69.06% | **0.89** | **-0.0290** | 0.053% | -3.98 | -2.57 | 0 | -0.00003 |
| **1T ($0.00001 / $0.001)** | 876 | 69.06% | **0.74** | **-0.0832** | 0.087% | -9.98 | -6.15 | 0 | -0.00009 |
| **2T ($0.00002 / $0.002)** | 876 | 69.06% | **0.64** | **-0.1374** | 0.140% | -14.65 | -8.71 | 0 | -0.00016 |
| **3T ($0.00003 / $0.003)** | 876 | 69.06% | **0.56** | **-0.1916** | 0.194% | -18.39 | -10.63 | 0 | -0.00022 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.0542 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.126 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 653 trades | Win Rate: 67.69% | Profit Factor: 0.84 | PnL: -0.0342 USDT
- **Out-of-Sample (30%):** 161 trades | Win Rate: 68.94% | Profit Factor: 0.89 | PnL: -0.0056 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.060` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.016%`

---

### 5. Key Insights & Decision
- Evaluated on TRUMP_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare TRUMP_USDT results against cross-asset baseline.
