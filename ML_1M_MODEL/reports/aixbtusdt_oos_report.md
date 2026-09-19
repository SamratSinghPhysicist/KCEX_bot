# 🤖 ML Model Out-of-Sample Performance: AIXBTUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Symbol** | `AIXBTUSDT` | Microstructure Engine | Active |
| **Out-of-Sample Window** | `89,265` 1m bars | August 1–31, 2026 (Pure OOS) | Zero Leakage |
| **Total Trades** | `240` | High Conviction Only | Validated |
| **Win Rate** | **`2.08%`** | Breakeven: `33.33%` | ⚠️ SUB-PAR |
| **Profit Factor** | **`0.04`** | Target: > 1.25 | ⚠️ MONITOR |
| **Total Net PnL** | **`-63.45%`** | Positive Edge | ❌ LOSS |
| **Max Drawdown** | **`63.45%`** | < 15.0% | ⚠️ HIGH |
| **Daily Sharpe Ratio** | **`-11.08`** | Daily Aggregation ($\sqrt{365.25}$) | Institutional Metric |
| **Daily Sortino Ratio** | **`-9.64`** | Downside Deviation | Institutional Metric |
| **t-statistic (p-value)** | **`-33.91 (p=0.0)`** | $H_0: \mu = 0$ | Two-tailed |
| **Binomial Test p-value** | **`1.0`** | $H_0: p \le p_{be}$ | One-tailed |
| **Expectancy / Trade** | **`$-26.44`** | Positive Expected Value | Validated |

---

## ⚖️ Directional Trade Breakdown
- **LONG Trades**: `236` trades | Win Rate: `2.12%` | PnL: `$-6,211.02`
- **SHORT Trades**: `4` trades | Win Rate: `0.0%` | PnL: `$-134.03`

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.3%`
- **SELL Signals**: `0.0%`
- **WAIT / HOLD**: `99.7%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: $\sim 3.0 \times \text{ATR}_{14}$
- **Stop Loss Protection**: $\sim 1.5 \times \text{ATR}_{14}$
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage


---

## 🧪 Slippage Friction Sensitivity Matrix

| Slippage (Ticks) | Trades | Win Rate | Profit Factor | Net PnL | Daily Sharpe | Max DD | t-stat (p-val) | Binomial p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0 ticks** | `155` | `20.0%` | **`0.35`** | **`-23.9%`** | `-9.84` | `25.3%` | `-6.31 (p=0.000)` | `0.9999` |
| **2.0 ticks** | `240` | `2.1%` | **`0.04`** | **`-63.5%`** | `-11.08` | `63.5%` | `-33.91 (p=0.000)` | `1.0000` |
| **3.0 ticks** | `246` | `0.8%` | **`0.01`** | **`-73.9%`** | `-11.81` | `73.9%` | `-59.28 (p=0.000)` | `1.0000` |
| **5.0 ticks** | `251` | `0.0%` | **`0.00`** | **`-85.9%`** | `-12.05` | `85.9%` | `-203.14 (p=0.000)` | `1.0000` |
