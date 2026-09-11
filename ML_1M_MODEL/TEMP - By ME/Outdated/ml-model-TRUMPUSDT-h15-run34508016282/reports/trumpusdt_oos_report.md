# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark Target |
| :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | 1-Minute Microstructure |
| **Out-of-Sample Bars** | `26,493` 1m bars | Chronologically Isolated |
| **Total Trades** | `21` | High Conviction Only |
| **Win Rate** | **`52.38%`** | > 50% |
| **Profit Factor** | **`1.43`** | > 1.50 |
| **Total Net PnL** | **`7.17%`** | Positive Edge |
| **Max Drawdown** | **`9.15%`** | < 15.0% |
| **Sharpe Ratio** | **`0.75`** | > 1.50 |
| **Sortino Ratio** | **`3.82`** | > 2.00 |
| **Expectancy / Trade** | **`$34.14`** | Positive Expectancy |

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.0%`
- **SELL Signals**: `0.1%`
- **WAIT / HOLD**: `99.9%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: Predicted MFE excursion ($\sim 3.0 \times \text{ATR}_{14}$)
- **Stop Loss Protection**: Predicted MAE threshold ($\sim 1.5 \times \text{ATR}_{14}$)
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage
