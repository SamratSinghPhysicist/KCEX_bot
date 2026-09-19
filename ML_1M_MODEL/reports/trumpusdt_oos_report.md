# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `14` | High Conviction Only | Validated |
| **Win Rate** | **`64.29%`** | Breakeven: `33.33%` | ✅ EDGE |
| **Profit Factor** | **`9.76`** | Target: > 1.25 | ✅ PASS |
| **Total Net PnL** | **`47.3%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`3.41%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`3.24`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`67.19`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`2.43 (p=0.0305)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.0174`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$337.84`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `13` trades | Win Rate: `69.23%` | PnL: `$+4,822.26`
- **SHORT Trades**: `1` trades | Win Rate: `0.0%` | PnL: `$-92.55`

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
| **1.0 ticks** | `14` | `64.3%` | **`11.34`** | **`+48.3%`** | `3.27` | `3.1%` | `2.49 (p=0.027)` | `0.0174` |
| **2.0 ticks** | `14` | `64.3%` | **`9.76`** | **`+47.3%`** | `3.24` | `3.4%` | `2.43 (p=0.030)` | `0.0174` |
| **3.0 ticks** | `14` | `64.3%` | **`7.58`** | **`+45.5%`** | `3.16` | `3.7%` | `2.31 (p=0.038)` | `0.0174` |
| **5.0 ticks** | `13` | `61.5%` | **`6.12`** | **`+41.0%`** | `2.98` | `4.4%` | `2.09 (p=0.059)` | `0.0347` |
