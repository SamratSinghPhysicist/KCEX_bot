# 🤖 ML Model Out-of-Sample Performance: ACTUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `ACTUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `11` | High Conviction Only | Validated |
| **Win Rate** | **`9.09%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.12`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-7.27%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`7.27%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-6.11`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-5.87`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-3.59 (p=0.0049)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.9884`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-66.06`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `11` trades | Win Rate: `9.09%` | PnL: `$-726.63`
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
| **1.0 ticks** | `10` | `10.0%` | **`0.19`** | **`-4.5%`** | `-4.96` | `4.5%` | `-2.42 (p=0.039)` | `0.9827` |
| **2.0 ticks** | `11` | `9.1%` | **`0.12`** | **`-7.3%`** | `-6.11` | `7.3%` | `-3.59 (p=0.005)` | `0.9884` |
| **3.0 ticks** | `12` | `0.0%` | **`0.00`** | **`-12.5%`** | `-5.30` | `12.5%` | `-16.99 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `12` | `0.0%` | **`0.00`** | **`-16.8%`** | `-5.45` | `16.8%` | `-25.20 (p=0.000)` | `1.0000` |
