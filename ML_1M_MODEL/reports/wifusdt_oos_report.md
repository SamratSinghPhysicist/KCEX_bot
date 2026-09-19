# 🤖 ML Model Out-of-Sample Performance: WIFUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `WIFUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `16` | High Conviction Only | Validated |
| **Win Rate** | **`6.25%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.13`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-9.05%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`9.05%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-3.65`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-3.62`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-3.18 (p=0.0062)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.9985`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-56.56`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `16` trades | Win Rate: `6.25%` | PnL: `$-904.97`
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
| **1.0 ticks** | `9` | `44.4%` | **`0.62`** | **`-2.0%`** | `-1.27` | `3.4%` | `-0.58 (p=0.581)` | `0.3497` |
| **2.0 ticks** | `16` | `6.2%` | **`0.13`** | **`-9.1%`** | `-3.65` | `9.1%` | `-3.18 (p=0.006)` | `0.9985` |
| **3.0 ticks** | `19` | `5.3%` | **`0.09`** | **`-14.2%`** | `-3.39` | `14.2%` | `-5.20 (p=0.000)` | `0.9995` |
| **5.0 ticks** | `20` | `5.0%` | **`0.06`** | **`-19.0%`** | `-3.33` | `19.0%` | `-6.80 (p=0.000)` | `0.9997` |
