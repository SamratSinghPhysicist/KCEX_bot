# 🤖 ML Model Out-of-Sample Performance: DOGEUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `DOGEUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `5` | High Conviction Only | Validated |
| **Win Rate** | **`20.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.47`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-1.16%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`1.73%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-2.68`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-2.74`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-0.67 (p=0.5381)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.8683`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-23.23`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `5` trades | Win Rate: `20.0%` | PnL: `$-116.15`
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
| **1.0 ticks** | `5` | `20.0%` | **`0.50`** | **`-1.0%`** | `-2.42` | `1.6%` | `-0.61 (p=0.576)` | `0.8683` |
| **2.0 ticks** | `5` | `20.0%` | **`0.47`** | **`-1.2%`** | `-2.68` | `1.7%` | `-0.67 (p=0.538)` | `0.8683` |
| **3.0 ticks** | `5` | `20.0%` | **`0.45`** | **`-1.3%`** | `-2.93` | `1.8%` | `-0.74 (p=0.503)` | `0.8683` |
| **5.0 ticks** | `5` | `20.0%` | **`0.41`** | **`-1.5%`** | `-3.35` | `2.0%` | `-0.86 (p=0.440)` | `0.8683` |
