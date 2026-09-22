# 🤖 ML Model Performance with Fees (0.10% Total): MELANIAUSDT

## 📊 Executive Summary
| Metric | Zero-Fee Baseline (KCEX) | 0.10% Total Fee (0.05%/side) | Impact / Delta | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Symbol** | `MELANIAUSDT` | `MELANIAUSDT` | — | Active |
| **Fee Model** | `0.0% Maker / 0.0% Taker` | `0.05% Taker (0.10% Round-trip)` | `-0.10% / trade` | Simulated |
| **Total Trades** | `27` | `27` | `0` | Validated |
| **Win Rate** | **`37.04%`** | **`33.33%`** | `-3.71%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`1.07`** | **`0.88`** | `-0.19` | ⚠️ COMPRESSED |
| **Total Net PnL** | **`1.81%`** | **`-3.54%`** | `-5.35%` | ❌ NET LOSS |
| **Final Equity** | `$10,181.18` | `$9,645.64` | `$-535.54` | Validated |
| **Max Drawdown** | `< 15.0%` | **`16.15%`** | Slight expansion | ⚠️ HIGH |
| **Daily Sharpe** | `-3.25` | Daily Annualized ($\sqrt{365.25}$) | Institutional Metric |
| **Expectancy** | **`$-13.12`** / trade | Positive EV | Validated |

---

## ⚖️ Directional Trade Breakdown (After Fees)
- **LONG Trades**: `27` trades | Win Rate: `33.33%` | PnL: `$-354.35`
- **SHORT Trades**: `0` trades | Win Rate: `0.0%` | PnL: `$+0.00`

---

## 🧪 Fee Sensitivity Spectrum for MELANIAUSDT

| Total Fee Rate | Win Rate | Profit Factor | Net PnL (%) | Final Equity ($) | Edge Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.00%** | `37.04%` | **`1.07`** | **`+1.81%`** | `$10,181.18` | ✅ Profitable |
| **0.02%** | `37.04%` | **`1.03`** | **`+0.72%`** | `$10,071.83` | ✅ Profitable |
| **0.04%** | `37.04%` | **`0.99`** | **`-0.36%`** | `$9,963.61` | ❌ Sub-Breakeven |
| **0.06%** | `37.04%` | **`0.95`** | **`-1.43%`** | `$9,856.52` | ❌ Sub-Breakeven |
| **0.08%** | `37.04%` | **`0.91`** | **`-2.49%`** | `$9,750.53` | ❌ Sub-Breakeven |
| **0.10%** | `33.33%` | **`0.88`** | **`-3.54%`** | `$9,645.64` | ❌ Sub-Breakeven |
| **0.15%** | `33.33%` | **`0.80`** | **`-6.12%`** | `$9,388.15` | ❌ Sub-Breakeven |
| **0.20%** | `33.33%` | **`0.73`** | **`-8.63%`** | `$9,137.28` | ❌ Sub-Breakeven |

---

## 🛡️ Risk & Execution Parameters
- **Slippage Friction**: 2.0 ticks
- **Leverage**: 20.0x
- **Take-Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop-Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
