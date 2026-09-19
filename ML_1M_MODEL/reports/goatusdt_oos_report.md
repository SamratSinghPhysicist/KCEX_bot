# 🤖 ML Model Out-of-Sample Performance: GOATUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `GOATUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `9` | High Conviction Only | Validated |
| **Win Rate** | **`33.33%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.52`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-2.27%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`3.38%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-2.7`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-2.77`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-0.86 (p=0.4158)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.6228`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-25.17`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `9` trades | Win Rate: `33.33%` | PnL: `$-226.55`
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
| **1.0 ticks** | `8` | `37.5%` | **`0.84`** | **`-0.5%`** | `-0.67` | `1.9%` | `-0.20 (p=0.848)` | `0.5318` |
| **2.0 ticks** | `9` | `33.3%` | **`0.52`** | **`-2.3%`** | `-2.70` | `3.4%` | `-0.86 (p=0.416)` | `0.6228` |
| **3.0 ticks** | `10` | `30.0%` | **`0.34`** | **`-4.3%`** | `-3.66` | `5.4%` | `-1.54 (p=0.158)` | `0.7009` |
| **5.0 ticks** | `12` | `0.0%` | **`0.00`** | **`-13.6%`** | `-4.29` | `13.6%` | `-30.60 (p=0.000)` | `1.0000` |
