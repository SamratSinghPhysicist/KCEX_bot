# 🤖 ML Model Out-of-Sample Performance: KOMAUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `KOMAUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `3` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-2.64%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`2.64%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-4.26`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-4.2`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-9.85 (p=0.0101)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-87.85`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `2` trades | Win Rate: `0.0%` | PnL: `$-179.59`
- **SHORT Trades**: `1` trades | Win Rate: `0.0%` | PnL: `$-83.96`

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
| **1.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-2.0%`** | `-4.14` | `2.0%` | `-5.01 (p=0.038)` | `1.0000` |
| **2.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-2.6%`** | `-4.26` | `2.6%` | `-9.85 (p=0.010)` | `1.0000` |
| **3.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-3.3%`** | `-4.30` | `3.3%` | `-21.05 (p=0.002)` | `1.0000` |
| **5.0 ticks** | `3` | `0.0%` | **`0.00`** | **`-4.6%`** | `-4.30` | `4.6%` | `-22.28 (p=0.002)` | `1.0000` |
