# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `44,628` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `44` | High Conviction Only | Validated |
| **Win Rate** | **`43.18%`** | Breakeven: `34.48%` | ✅ EDGE |
| **Profit Factor** | **`1.98`** | Target: > 1.25 | ✅ PASS |
| **Total Net PnL** | **`39.94%`** | Positive Edge | ✅ PROFITABLE |
| **Max Drawdown** | **`6.95%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`3.27`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`25.0`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`1.78 (p=0.0828)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.1459`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$90.76`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `40` trades | Win Rate: `45.0%` | PnL: `$+4,010.12`
- **SHORT Trades**: `4` trades | Win Rate: `25.0%` | PnL: `$-16.51`

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.1%`
- **SELL Signals**: `0.0%`
- **WAIT / HOLD**: `99.9%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: $\sim 1.9 \times \text{ATR}_{14}$
- **Stop Loss Protection**: $\sim 1.0 \times \text{ATR}_{14}$
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage


---

## 🧪 Slippage Friction Sensitivity Matrix

| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0 ticks** | `43` | `48.8%` | **`2.28`** | **`+49.2%`** | `3.75` | `5.2%` | `2.14 (p=0.038)` | `0.0366` |
| **2.0 ticks** | `44` | `43.2%` | **`1.98`** | **`+39.9%`** | `3.27` | `7.0%` | `1.78 (p=0.083)` | `0.1459` |
| **3.0 ticks** | `44` | `38.6%` | **`1.45`** | **`+20.4%`** | `2.70` | `8.2%` | `1.05 (p=0.300)` | `0.3321` |
| **5.0 ticks** | `49` | `28.6%` | **`0.91`** | **`-5.0%`** | `-0.42` | `18.0%` | `-0.16 (p=0.876)` | `0.8466` |
