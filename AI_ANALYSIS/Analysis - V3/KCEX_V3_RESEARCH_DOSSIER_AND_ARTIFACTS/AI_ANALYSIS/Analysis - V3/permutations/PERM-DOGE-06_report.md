# 🔬 Quantitative Experiment Report: PERM-DOGE-06
## DOGE Inverted Stoch RSI (5t TP / 2t SL) Pure Market Taker Baseline

> **Research Domain:** Dual-Asset Permutation Matrix: DOGE_USDT  
> **Execution Timestamp:** `2026-09-07 01:46:26 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `DOGE_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `5 ticks TP` | Stop: `2 ticks SL`
- Execution Style: `PURE_MARKET` | Ratchet: `False` | Duration Safeguard: `False`
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
| **0T (Maker Baseline)** | 2577 | 30.19% | **1.08** | **+0.0292** | 0.013% | 2.74 | 4.41 | 0 | +0.00001 |
| **1T ($0.00001 / $0.001)** | 2588 | 14.10% | **0.27** | **-0.4844** | 0.484% | -52.27 | -48.52 | 0 | -0.00019 |
| **2T ($0.00002 / $0.002)** | 2609 | 2.53% | **0.03** | **-0.9842** | 0.984% | -207.65 | -73.34 | 0 | -0.00038 |
| **3T ($0.00003 / $0.003)** | 2614 | 0.00% | **0.00** | **-1.3070** | 1.307% | -20473.12 | -77.77 | 0 | -0.00050 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.4454 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `0.067 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1792 trades | Win Rate: 30.19% | Profit Factor: 1.08 | PnL: +0.0203 USDT
- **Out-of-Sample (30%):** 584 trades | Win Rate: 30.65% | Profit Factor: 1.10 | PnL: +0.0085 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.022` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.009%`

---

### 5. Key Insights & Decision
- Evaluated on DOGE_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare DOGE_USDT results against cross-asset baseline.
