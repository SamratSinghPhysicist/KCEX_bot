# 🔬 Quantitative Experiment Report: PERM-DOGE-05
## DOGE EMA Crossover (5/13) (5t TP / 2t SL) Maker Hybrid

> **Research Domain:** Dual-Asset Permutation Matrix: DOGE_USDT  
> **Execution Timestamp:** `2026-09-07 01:45:23 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `DOGE_USDT` | Strategy: `EMA_CROSSOVER` | Polarity: `Direct (Momentum)`
- Target: `5 ticks TP` | Stop: `2 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "DOGE_USDT",
  "timeframe": "1m",
  "strategy_mode": "EMA_CROSSOVER",
  "tp_ticks": 5,
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
| **0T (Maker Baseline)** | 1241 | 26.91% | **0.92** | **-0.0144** | 0.024% | -2.91 | -4.51 | 0 | -0.00001 |
| **1T ($0.00001 / $0.001)** | 1241 | 26.91% | **0.61** | **-0.1051** | 0.106% | -18.55 | -21.95 | 0 | -0.00008 |
| **2T ($0.00002 / $0.002)** | 1241 | 26.91% | **0.46** | **-0.1958** | 0.196% | -30.72 | -30.67 | 0 | -0.00016 |
| **3T ($0.00003 / $0.003)** | 1241 | 26.91% | **0.37** | **-0.2865** | 0.287% | -40.46 | -35.90 | 0 | -0.00023 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.0907 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.067 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 855 trades | Win Rate: 25.38% | Profit Factor: 0.85 | PnL: -0.0191 USDT
- **Out-of-Sample (30%):** 282 trades | Win Rate: 31.21% | Profit Factor: 1.13 | PnL: +0.0052 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.334` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.007%`

---

### 5. Key Insights & Decision
- Evaluated on DOGE_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare DOGE_USDT results against cross-asset baseline.
