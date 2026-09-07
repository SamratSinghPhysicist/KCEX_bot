# 🔬 Quantitative Experiment Report: PERM-DOGE-03
## DOGE Direct Stoch RSI Momentum Asymmetric (10t TP / 2t SL) Maker Hybrid

> **Research Domain:** Dual-Asset Permutation Matrix: DOGE_USDT  
> **Execution Timestamp:** `2026-09-07 01:43:35 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `DOGE_USDT` | Strategy: `STOCH_RSI` | Polarity: `Direct (Momentum)`
- Target: `10 ticks TP` | Stop: `2 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "DOGE_USDT",
  "timeframe": "1m",
  "strategy_mode": "STOCH_RSI",
  "tp_ticks": 10,
  "sl_ticks": 2,
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
| **0T (Maker Baseline)** | 2236 | 16.06% | **0.96** | **-0.0164** | 0.034% | -1.29 | -2.85 | 0 | -0.00001 |
| **1T ($0.00001 / $0.001)** | 2236 | 16.06% | **0.64** | **-0.2041** | 0.204% | -14.87 | -23.66 | 0 | -0.00009 |
| **2T ($0.00002 / $0.002)** | 2236 | 16.06% | **0.48** | **-0.3918** | 0.392% | -26.51 | -34.07 | 0 | -0.00018 |
| **3T ($0.00003 / $0.003)** | 2236 | 16.06% | **0.38** | **-0.5795** | 0.580% | -36.60 | -40.31 | 0 | -0.00026 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.1877 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.040 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1571 trades | Win Rate: 16.23% | Profit Factor: 0.97 | PnL: -0.0082 USDT
- **Out-of-Sample (30%):** 491 trades | Win Rate: 15.89% | Profit Factor: 0.94 | PnL: -0.0046 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `0.975` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.018%`

---

### 5. Key Insights & Decision
- Evaluated on DOGE_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare DOGE_USDT results against cross-asset baseline.
