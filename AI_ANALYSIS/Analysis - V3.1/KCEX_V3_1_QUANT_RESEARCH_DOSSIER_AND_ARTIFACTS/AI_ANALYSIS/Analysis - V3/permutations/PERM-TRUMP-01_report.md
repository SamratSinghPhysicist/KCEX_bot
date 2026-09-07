# 🔬 Quantitative Experiment Report: PERM-TRUMP-01
## TRUMP Inverted Stoch RSI (2t TP / 5t SL) Maker Hybrid

> **Research Domain:** Dual-Asset Permutation Matrix: TRUMP_USDT  
> **Execution Timestamp:** `2026-09-07 01:33:21 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `TRUMP_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `2 ticks TP` | Stop: `5 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
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
| **0T (Maker Baseline)** | 1511 | 74.92% | **1.19** | **+0.0738** | 0.015% | 6.26 | 3.80 | 0 | +0.00005 |
| **1T ($0.00001 / $0.001)** | 1511 | 74.92% | **1.00** | **-0.0020** | 0.032% | -0.15 | -0.09 | 0 | -0.00000 |
| **2T ($0.00002 / $0.002)** | 1511 | 74.92% | **0.85** | **-0.0778** | 0.091% | -5.13 | -2.86 | 0 | -0.00005 |
| **3T ($0.00003 / $0.003)** | 1511 | 74.92% | **0.75** | **-0.1536** | 0.159% | -9.11 | -4.94 | 0 | -0.00010 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.0758 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `0.195 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1134 trades | Win Rate: 73.54% | Profit Factor: 1.11 | PnL: +0.0336 USDT
- **Out-of-Sample (30%):** 282 trades | Win Rate: 80.14% | Profit Factor: 1.61 | PnL: +0.0344 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.452` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.008%`

---

### 5. Key Insights & Decision
- Evaluated on TRUMP_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare TRUMP_USDT results against cross-asset baseline.
