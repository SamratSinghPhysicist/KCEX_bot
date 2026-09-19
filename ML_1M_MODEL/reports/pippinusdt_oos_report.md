# 🤖 ML Model Out-of-Sample Performance: PIPPINUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `PIPPINUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `13` | High Conviction Only | Validated |
| **Win Rate** | **`7.69%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.08`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-6.77%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`7.35%`** | < 15.0% | ✅ CONTROLLED |
| **Daily Sharpe Ratio** | **`-5.02`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-4.97`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-4.06 (p=0.0016)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`0.9949`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-52.1`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `13` trades | Win Rate: `7.69%` | PnL: `$-677.30`
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
| **1.0 ticks** | `13` | `23.1%` | **`0.28`** | **`-3.8%`** | `-3.20` | `4.9%` | `-1.87 (p=0.086)` | `0.8613` |
| **2.0 ticks** | `13` | `7.7%` | **`0.08`** | **`-6.8%`** | `-5.02` | `7.3%` | `-4.06 (p=0.002)` | `0.9949` |
| **3.0 ticks** | `13` | `0.0%` | **`0.00`** | **`-9.2%`** | `-6.04` | `9.2%` | `-8.36 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `14` | `0.0%` | **`0.00`** | **`-12.8%`** | `-5.77` | `12.8%` | `-12.31 (p=0.000)` | `1.0000` |
