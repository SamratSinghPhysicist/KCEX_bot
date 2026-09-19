# 🤖 ML Model Out-of-Sample Performance: ETHUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `ETHUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `3` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-1.25%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`1.25%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-4.11`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-4.05`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-4.6 (p=0.0441)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-41.68`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `2` trades | Win Rate: `0.0%` | PnL: `$-100.98`
- **SHORT Trades**: `1` trades | Win Rate: `0.0%` | PnL: `$-24.07`

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
| **1.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-1.2%`** | `-4.11` | `1.2%` | `-4.59 (p=0.044)` | `1.0000` |
| **2.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-1.2%`** | `-4.11` | `1.2%` | `-4.60 (p=0.044)` | `1.0000` |
| **3.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-1.2%`** | `-4.11` | `1.2%` | `-4.61 (p=0.044)` | `1.0000` |
| **5.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-1.3%`** | `-4.11` | `1.3%` | `-4.64 (p=0.043)` | `1.0000` |
