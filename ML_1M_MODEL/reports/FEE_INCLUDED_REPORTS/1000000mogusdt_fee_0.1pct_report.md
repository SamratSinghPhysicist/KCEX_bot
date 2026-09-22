# 🤖 ML Model Performance with Fees (0.10% Total): 1000000MOGUSDT

## 📊 Executive Summary
| Metric | Zero-Fee Baseline (KCEX) | 0.10% Total Fee (0.05%/side) | Impact / Delta | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Symbol** | `1000000MOGUSDT` | `1000000MOGUSDT` | — | Active |
| **Fee Model** | `0.0% Maker / 0.0% Taker` | `0.05% Taker (0.10% Round-trip)` | `-0.10% / trade` | Simulated |
| **Total Trades** | `10` | `10` | `0` | Validated |
| **Win Rate** | **`70.00%`** | **`70.0%`** | `+0.00%` | ✅ EDGE |
| **Profit Factor** | **`3.91`** | **`1.94`** | `-1.97` | ✅ PASS |
| **Total Net PnL** | **`3.84%`** | **`1.79%`** | `-2.05%` | ✅ PROFITABLE |
| **Final Equity** | `$10,384.29` | `$10,179.23` | `$-205.06` | Validated |
| **Max Drawdown** | `< 15.0%` | **`0.95%`** | Slight expansion | ✅ CONTROLLED |
| **Daily Sharpe** | `7.89` | Daily Annualized ($\sqrt{365.25}$) | Institutional Metric |
| **Expectancy** | **`$17.92`** / trade | Positive EV | Validated |

---

## ⚖️ Directional Trade Breakdown (After Fees)
- **LONG Trades**: `10` trades | Win Rate: `70.0%` | PnL: `$+179.23`
- **SHORT Trades**: `0` trades | Win Rate: `0.0%` | PnL: `$+0.00`

---

## 🧪 Fee Sensitivity Spectrum for 1000000MOGUSDT

| Total Fee Rate | Win Rate | Profit Factor | Net PnL (%) | Final Equity ($) | Edge Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.00%** | `70.0%` | **`3.91`** | **`+3.84%`** | `$10,384.29` | ✅ Highly Robust |
| **0.02%** | `70.0%` | **`3.38`** | **`+3.43%`** | `$10,342.98` | ✅ Highly Robust |
| **0.04%** | `70.0%` | **`2.94`** | **`+3.02%`** | `$10,301.82` | ✅ Highly Robust |
| **0.06%** | `70.0%` | **`2.55`** | **`+2.61%`** | `$10,260.81` | ✅ Highly Robust |
| **0.08%** | `70.0%` | **`2.22`** | **`+2.20%`** | `$10,219.95` | ✅ Highly Robust |
| **0.10%** | `70.0%` | **`1.94`** | **`+1.79%`** | `$10,179.23` | ✅ Profitable |
| **0.15%** | `70.0%` | **`1.35`** | **`+0.78%`** | `$10,078.07` | ✅ Profitable |
| **0.20%** | `60.0%` | **`0.91`** | **`-0.22%`** | `$9,977.82` | ❌ Sub-Breakeven |

---

## 🛡️ Risk & Execution Parameters
- **Slippage Friction**: 2.0 ticks
- **Leverage**: 20.0x
- **Take-Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop-Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
