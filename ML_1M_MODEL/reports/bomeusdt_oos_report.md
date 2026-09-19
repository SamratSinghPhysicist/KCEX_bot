# 🤖 ML Model Out-of-Sample Performance: BOMEUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `BOMEUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `152` | High Conviction Only | Validated |
| **Win Rate** | **`0.66%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.01`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-80.88%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`81.69%`** | < 15.0% | ⚠️ HIGH |
| **Daily Sharpe Ratio** | **`-7.55`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-7.1`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-26.69 (p=0.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-53.21`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `147` trades | Win Rate: `0.68%` | PnL: `$-7,925.86`
- **SHORT Trades**: `5` trades | Win Rate: `0.0%` | PnL: `$-162.45`

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.2%`
- **SELL Signals**: `0.0%`
- **WAIT / HOLD**: `99.8%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage


---

## 🧪 Slippage Friction Sensitivity Matrix

| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0 ticks** | `152` | `0.7%` | **`0.03`** | **`-61.4%`** | `-7.37` | `63.0%` | `-16.39 (p=0.000)` | `1.0000` |
| **2.0 ticks** | `152` | `0.7%` | **`0.01`** | **`-80.9%`** | `-7.55` | `81.7%` | `-26.69 (p=0.000)` | `1.0000` |
| **3.0 ticks** | `152` | `0.7%` | **`0.00`** | **`-90.5%`** | `-7.68` | `90.9%` | `-35.52 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `152` | `0.7%` | **`0.00`** | **`-97.7%`** | `-7.90` | `97.8%` | `-49.45 (p=0.000)` | `1.0000` |
