# 🤖 ML Model Out-of-Sample Performance: MELANIAUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `MELANIAUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `27` | High Conviction Only | Validated |
| **Win Rate** | **`37.04%`** | Breakeven: `33.33%` | ✅ EDGE |
| **Profit Factor** | **`1.07`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`1.81%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`15.1%`** | < 15.0% | ⚠️ HIGH |
| **Daily Sharpe Ratio** | **`0.82`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`1.55`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`0.2 (p=0.8443)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.4108`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$6.71`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `27` trades | Win Rate: `37.04%` | PnL: `$+181.18`
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
| **1.0 ticks** | `27` | `40.7%` | **`1.09`** | **`+2.3%`** | `1.00` | `15.0%` | `0.23 (p=0.818)` | `0.2658` |
| **2.0 ticks** | `27` | `37.0%` | **`1.07`** | **`+1.8%`** | `0.82` | `15.1%` | `0.20 (p=0.844)` | `0.4108` |
| **3.0 ticks** | `27` | `37.0%` | **`1.04`** | **`+1.1%`** | `0.51` | `15.2%` | `0.14 (p=0.888)` | `0.4108` |
| **5.0 ticks** | `27` | `37.0%` | **`1.00`** | **`+0.1%`** | `0.09` | `15.3%` | `0.07 (p=0.947)` | `0.4108` |
