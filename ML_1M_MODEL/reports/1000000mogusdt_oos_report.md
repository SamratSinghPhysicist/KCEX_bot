# 🤖 ML Model Out-of-Sample Performance: 1000000MOGUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `1000000MOGUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `10` | High Conviction Only | Validated |
| **Win Rate** | **`70.0%`** | Breakeven: `33.33%` | ✅ EDGE |
| **Profit Factor** | **`3.91`** | Target: > 1.25 | ✅ PASS |
| **Total Net PnL** | **`3.84%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`0.75%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`4.41`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`25.32`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`1.72 (p=0.1189)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.0197`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$38.43`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `10` trades | Win Rate: `70.0%` | PnL: `$+384.29`
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
| **1.0 ticks** | `10` | `70.0%` | **`3.91`** | **`+3.8%`** | `4.41` | `0.8%` | `1.72 (p=0.119)` | `0.0197` |
| **2.0 ticks** | `10` | `70.0%` | **`3.91`** | **`+3.8%`** | `4.41` | `0.8%` | `1.72 (p=0.119)` | `0.0197` |
| **3.0 ticks** | `10` | `70.0%` | **`3.91`** | **`+3.8%`** | `4.41` | `0.8%` | `1.72 (p=0.119)` | `0.0197` |
| **5.0 ticks** | `10` | `70.0%` | **`3.91`** | **`+3.8%`** | `4.41` | `0.8%` | `1.72 (p=0.119)` | `0.0197` |
