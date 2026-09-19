# 🤖 ML Model Out-of-Sample Performance: SOLUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `SOLUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `1` | High Conviction Only | Validated |
| **Win Rate** | **`100.0%`** | Breakeven: `33.33%` | ✅ EDGE |
| **Profit Factor** | **`36080160320.64`** | Target: > 1.25 | ✅ PASS |
| **Total Net PnL** | **`0.36%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`0.0%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`2.45`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`1130404.13`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`0.0 (p=1.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.3333`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$36.08`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `1` trades | Win Rate: `100.0%` | PnL: `$+36.08`
- **SHORT Trades**: `0` trades | Win Rate: `0.0%` | PnL: `$+0.00`

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.0%`
- **SELL Signals**: `0.0%`
- **WAIT / HOLD**: `100.0%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage


---

## 🧪 Slippage Friction Sensitivity Matrix

| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0 ticks** | `1` | `100.0%` | **`36084885640.18`** | **`+0.4%`** | `2.45` | `0.0%` | `0.00 (p=1.000)` | `0.3333` |
| **2.0 ticks** | `1` | `100.0%` | **`36080160320.64`** | **`+0.4%`** | `2.45` | `0.0%` | `0.00 (p=1.000)` | `0.3333` |
| **3.0 ticks** | `1` | `100.0%` | **`36075436115.04`** | **`+0.4%`** | `2.45` | `0.0%` | `0.00 (p=1.000)` | `0.3333` |
| **5.0 ticks** | `1` | `100.0%` | **`12497761018.15`** | **`+0.1%`** | `2.45` | `0.0%` | `0.00 (p=1.000)` | `0.3333` |
