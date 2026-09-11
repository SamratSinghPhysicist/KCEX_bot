# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark Target |
| :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | 1-Minute Microstructure |
| **Out-of-Sample Bars** | `26,494` 1m bars | Chronologically Isolated |
| **Total Trades** | `2,730` | High Conviction Only |
| **Win Rate** | **`37.33%`** | > 50% |
| **Profit Factor** | **`0.32`** | > 1.50 |
| **Total Net PnL** | **`-99.78%`** | Positive Edge |
| **Max Drawdown** | **`99.78%`** | < 15.0% |
| **Sharpe Ratio** | **`-9.46`** | > 1.50 |
| **Sortino Ratio** | **`-16.1`** | > 2.00 |
| **Expectancy / Trade** | **`$-3.65`** | Positive Expectancy |

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.0%`
- **SELL Signals**: `33.2%`
- **WAIT / HOLD**: `66.8%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: Predicted MFE excursion ($\sim 2.0 \times \text{ATR}_{14}$)
- **Stop Loss Protection**: Predicted MAE threshold ($\sim 1.2 \times \text{ATR}_{14}$)
- **Execution Cost Modeling**: 0.02% Taker Fee + 1.0 Tick Slippage
