# 🤖 ML Model Out-of-Sample Performance: MEMEUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `MEMEUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `25` | High Conviction Only | Validated |
| **Win Rate** | **`0.0%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.0`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-24.59%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`24.59%`** | < 15.0% | ⚠️ HIGH |
| **Daily Sharpe Ratio** | **`-7.35`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-6.91`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-19.88 (p=0.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-98.34`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `11` trades | Win Rate: `0.0%` | PnL: `$-1,187.85`
- **SHORT Trades**: `14` trades | Win Rate: `0.0%` | PnL: `$-1,270.74`

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
| **1.0 ticks** | `25` | `0.0%` | **`0.00`** | **`-17.0%`** | `-7.08` | `17.0%` | `-12.22 (p=0.000)` | `1.0000` |
| **2.0 ticks** | `25` | `0.0%` | **`0.00`** | **`-24.6%`** | `-7.35` | `24.6%` | `-19.88 (p=0.000)` | `1.0000` |
| **3.0 ticks** | `25` | `0.0%` | **`0.00`** | **`-31.5%`** | `-7.46` | `31.5%` | `-28.72 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `26` | `0.0%` | **`0.00`** | **`-45.2%`** | `-7.54` | `45.2%` | `-46.83 (p=0.000)` | `1.0000` |
