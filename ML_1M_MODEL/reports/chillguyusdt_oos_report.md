# 🤖 ML Model Out-of-Sample Performance: CHILLGUYUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `CHILLGUYUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `10` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-6.89%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`6.89%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-4.36`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-4.29`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-20.09 (p=0.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-68.91`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `10` trades | Win Rate: `0.0%` | PnL: `$-689.14`
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
| **1.0 ticks** | `6` | `16.7%` | **`0.20`** | **`-2.2%`** | `-3.14` | `2.2%` | `-1.94 (p=0.111)` | `0.9122` |
| **2.0 ticks** | `10` | `0.0%` | **`0.00`** | **`-6.9%`** | `-4.36` | `6.9%` | `-20.09 (p=0.000)` | `1.0000` |
| **3.0 ticks** | `10` | `0.0%` | **`0.00`** | **`-8.5%`** | `-4.35` | `8.5%` | `-20.81 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `10` | `0.0%` | **`0.00`** | **`-11.5%`** | `-4.34` | `11.5%` | `-21.34 (p=0.000)` | `1.0000` |
