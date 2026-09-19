# 🤖 ML Model Out-of-Sample Performance: DOGSUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `DOGSUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `39` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-98.63%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`98.63%`** | < 15.0% | ⚠️ HIGH |
| **Daily Sharpe Ratio** | **`-8.95`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-8.16`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-132.06 (p=0.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-252.9`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `38` trades | Win Rate: `0.0%` | PnL: `$-8,914.78`
- **SHORT Trades**: `1` trades | Win Rate: `0.0%` | PnL: `$-948.51`

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
| **1.0 ticks** | `39` | `0.0%` | **`0.00`** | **`-88.2%`** | `-8.68` | `88.2%` | `-137.37 (p=0.000)` | `1.0000` |
| **2.0 ticks** | `39` | `0.0%` | **`0.00`** | **`-98.6%`** | `-8.95` | `98.6%` | `-132.06 (p=0.000)` | `1.0000` |
| **3.0 ticks** | `39` | `0.0%` | **`0.00`** | **`-99.8%`** | `-9.21` | `99.8%` | `-121.85 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `39` | `0.0%` | **`0.00`** | **`-100.0%`** | `-9.65` | `100.0%` | `-96.14 (p=0.000)` | `1.0000` |
