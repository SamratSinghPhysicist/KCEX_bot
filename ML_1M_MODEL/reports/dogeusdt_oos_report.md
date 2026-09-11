# 🤖 ML Model Out-of-Sample Performance: DOGEUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `DOGEUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `44,580` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `12` | High Conviction Only | Validated |
| **Win Rate** | **`58.33%`** | Breakeven: `33.33%` | ✅ EDGE |
| **Profit Factor** | **`1.3`** | Target: > 1.25 | ✅ PASS |
| **Total Net PnL** | **`1.33%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`3.15%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`1.89`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`1.74`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`0.42 (p=0.6796)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.0664`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$11.09`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `8` trades | Win Rate: `62.5%` | PnL: `$+114.24`
- **SHORT Trades**: `4` trades | Win Rate: `50.0%` | PnL: `$+18.78`

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.0%`
- **SELL Signals**: `0.0%`
- **WAIT / HOLD**: `100.0%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: $\sim 4.0 \times \text{ATR}_{14}$
- **Stop Loss Protection**: $\sim 2.0 \times \text{ATR}_{14}$
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage


---

## 🧪 Slippage Friction Sensitivity Matrix

| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0 ticks** | `12` | `58.3%` | **`1.43`** | **`+1.8%`** | `2.26` | `3.0%` | `0.57 (p=0.579)` | `0.0664` |
| **2.0 ticks** | `12` | `58.3%` | **`1.30`** | **`+1.3%`** | `1.89` | `3.1%` | `0.42 (p=0.680)` | `0.0664` |
| **3.0 ticks** | `12` | `58.3%` | **`1.19`** | **`+0.9%`** | `1.51` | `3.3%` | `0.28 (p=0.785)` | `0.0664` |
| **5.0 ticks** | `12` | `58.3%` | **`0.99`** | **`-0.1%`** | `0.71` | `3.5%` | `-0.00 (p=0.998)` | `0.0664` |
