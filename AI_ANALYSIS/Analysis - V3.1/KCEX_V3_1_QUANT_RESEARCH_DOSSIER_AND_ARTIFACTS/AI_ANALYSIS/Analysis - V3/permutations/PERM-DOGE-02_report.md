# 🔬 Quantitative Experiment Report: PERM-DOGE-02
## DOGE Inverted Stoch RSI (2t TP / 5t SL) Maker Hybrid (V3 Geometry)

> **Research Domain:** Dual-Asset Permutation Matrix: DOGE_USDT  
> **Execution Timestamp:** `2026-09-07 01:40:50 UTC`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
**Permutation Configuration:**
- Asset: `DOGE_USDT` | Strategy: `STOCH_RSI` | Polarity: `Inverted (Fade)`
- Target: `2 ticks TP` | Stop: `5 ticks SL`
- Execution Style: `MAKER_HYBRID` | Ratchet: `False` | Duration Safeguard: `False`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`


**Configuration Parameters:**
```json
{
  "symbol": "DOGE_USDT",
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
| **0T (Maker Baseline)** | 2347 | 66.00% | **0.78** | **-0.0892** | 0.090% | -8.91 | -5.91 | 0 | -0.00004 |
| **1T ($0.00001 / $0.001)** | 2347 | 66.00% | **0.65** | **-0.1690** | 0.170% | -14.77 | -9.33 | 0 | -0.00007 |
| **2T ($0.00002 / $0.002)** | 2347 | 66.00% | **0.55** | **-0.2488** | 0.249% | -19.33 | -11.78 | 0 | -0.00011 |
| **3T ($0.00003 / $0.003)** | 2347 | 66.00% | **0.49** | **-0.3286** | 0.329% | -22.98 | -13.61 | 0 | -0.00014 |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\Delta \text{PnL} / \Delta \text{Tick}$):** `-0.0798 USDT/tick`
- **Critical Slippage Threshold ($S_{max}$):** `-0.284 ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{max}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** 1630 trades | Win Rate: 65.21% | Profit Factor: 0.75 | PnL: -0.0709 USDT
- **Out-of-Sample (30%):** 532 trades | Win Rate: 68.61% | Profit Factor: 0.87 | PnL: -0.0105 USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `1.166` (High Stability, Zero Overfitting)
- **Monte Carlo Ruin Probability ($P(\text{DD} \ge 50\%)$):** `0.0000%`
- **Monte Carlo 95% Confidence Interval Max DD:** `0.018%`

---

### 5. Key Insights & Decision
- Evaluated on DOGE_USDT across 14 days of real millisecond tick trades.
- Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.
- Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample.

**Next Logical Mutation / Hypothesis:**
> Compare DOGE_USDT results against cross-asset baseline.
