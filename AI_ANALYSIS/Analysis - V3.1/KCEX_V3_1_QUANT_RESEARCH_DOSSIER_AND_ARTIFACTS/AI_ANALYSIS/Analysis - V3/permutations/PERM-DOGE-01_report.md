# 🔬 Quantitative Experiment Report: PERM-DOGE-01
## DOGE Inverted Stoch RSI (5t TP / 2t SL) Maker Hybrid Ratchet (V2.2 Spec)

> **Research Domain:** Dual-Asset Permutation Matrix: DOGE_USDT  
> **Execution Timestamp:** `2026-09-07 01:38:45 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `DOGE_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `5 ticks TP` | Stop: `2 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `True` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "DOGE_USDT",
  "timeframe": "1m",
  "strategy_mode": "STOCH_RSI",
  "tp_ticks": 5,
  "sl_ticks": 2,
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
| **0T (Maker Baseline)** | 2373 | 21.03% | **0.85** | **-0.0425** | 0.045% | -5.05 | -7.36 | 0 | -0.00002 |
| **1T ($0.00001 / $0.001)** | 2373 | 21.03% | **0.52** | **-0.2299** | 0.230% | -23.89 | -28.25 | 0 | -0.00010 |
| **2T ($0.00002 / $0.002)** | 2373 | 21.03% | **0.37** | **-0.4173** | 0.417% | -38.50 | -37.60 | 0 | -0.00018 |
| **3T ($0.00003 / $0.003)** | 2373 | 21.03% | **0.29** | **-0.6047** | 0.605% | -50.12 | -42.89 | 0 | -0.00025 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.1874 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.295 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1637 trades | Win Rate: 20.53% | Profit Factor: 0.82 | PnL: -0.0364 USDT
- **Out-of-Sample (30%):** 551 trades | Win Rate: 23.05% | Profit Factor: 0.97 | PnL: -0.0019 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.181` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.012%`

---

### 5. Key Insights & Decision
- Evaluated on DOGE_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare DOGE_USDT results against cross-asset baseline.
