# 🤖 ML Model Out-of-Sample Performance: BTCUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `BTCUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `0` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `50.0%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`0.0%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`0.0%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`0.0`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`0.0`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`0.0 (p=1.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$0.0`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `0` trades | Win Rate: `0.0%` | PnL: `$+0.00`
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
| **1.0 ticks** | `0` | `0.0%` | **`0.00`** | **`+0.0%`** | `0.00` | `0.0%` | `0.00 (p=1.000)` | `1.0000` |
| **2.0 ticks** | `0` | `0.0%` | **`0.00`** | **`+0.0%`** | `0.00` | `0.0%` | `0.00 (p=1.000)` | `1.0000` |
| **3.0 ticks** | `0` | `0.0%` | **`0.00`** | **`+0.0%`** | `0.00` | `0.0%` | `0.00 (p=1.000)` | `1.0000` |
| **5.0 ticks** | `0` | `0.0%` | **`0.00`** | **`+0.0%`** | `0.00` | `0.0%` | `0.00 (p=1.000)` | `1.0000` |
