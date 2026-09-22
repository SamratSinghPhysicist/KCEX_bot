# 🤖 ML Model Performance with Fees (0.10% Total): TRUMPUSDT

## 📊 Executive Summary
| Metric | Zero-Fee Baseline (KCEX) | 0.10% Total Fee (0.05%/side) | Impact / Delta | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | `TRUMPUSDT` | — | Active |
| **Fee Model** | `0.0% Maker / 0.0% Taker` | `0.05% Taker (0.10% Round-trip)` | `-0.10% / trade` | Simulated |
| **Total Trades** | `14` | `14` | `0` | Validated |
| **Win Rate** | **`64.29%`** | **`64.29%`** | `+0.00%` | ✅ EDGE |
| **Profit Factor** | **`9.76`** | **`7.74`** | `-2.02` | ✅ PASS |
| **Total Net PnL** | **`47.30%`** | **`43.33%`** | `-3.97%` | ✅ PROFITABLE |
| **Final Equity** | `$14,729.71` | `$14,333.25` | `$-396.46` | Validated |
| **Max Drawdown** | `< 15.0%` | **`3.99%`** | Slight expansion | ✅ CONTROLLED |
| **Daily Sharpe** | `8.3` | Daily Annualized ($\sqrt{365.25}$) | Institutional Metric |
| **Expectancy** | **`$309.52`** / trade | Positive EV | Validated |

---

## ⚖️ Directional Trade Breakdown (After Fees)
- **LONG Trades**: `13` trades | Win Rate: `69.23%` | PnL: `$+4,451.60`
- **SHORT Trades**: `1` trades | Win Rate: `0.0%` | PnL: `$-118.36`

---

## 🧪 Fee Sensitivity Spectrum for TRUMPUSDT

| Total Fee Rate | Win Rate | Profit Factor | Net PnL (%) | Final Equity ($) | Edge Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.00%** | `64.29%` | **`9.76`** | **`+47.30%`** | `$14,729.71` | ✅ Highly Robust |
| **0.02%** | `64.29%` | **`9.29`** | **`+46.50%`** | `$14,649.61` | ✅ Highly Robust |
| **0.04%** | `64.29%` | **`8.86`** | **`+45.70%`** | `$14,569.92` | ✅ Highly Robust |
| **0.06%** | `64.29%` | **`8.46`** | **`+44.91%`** | `$14,490.63` | ✅ Highly Robust |
| **0.08%** | `64.29%` | **`8.09`** | **`+44.12%`** | `$14,411.74` | ✅ Highly Robust |
| **0.10%** | `64.29%` | **`7.74`** | **`+43.33%`** | `$14,333.25` | ✅ Highly Robust |
| **0.15%** | `64.29%` | **`6.97`** | **`+41.39%`** | `$14,138.75` | ✅ Highly Robust |
| **0.20%** | `64.29%` | **`6.30`** | **`+39.47%`** | `$13,946.70` | ✅ Highly Robust |

---

## 🛡️ Risk & Execution Parameters
- **Slippage Friction**: 2.0 ticks
- **Leverage**: 20.0x
- **Take-Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop-Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
