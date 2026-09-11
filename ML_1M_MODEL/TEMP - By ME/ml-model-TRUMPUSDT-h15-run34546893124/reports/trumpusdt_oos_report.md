# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark Target |
| :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | 1-Minute Microstructure |
| **Out-of-Sample Bars** | `26,493` 1m bars | Chronologically Isolated |
| **Total Trades** | `36` | High Conviction Only |
| **Win Rate** | **`47.22%`** | > 50% |
| **Profit Factor** | **`1.1`** | > 1.50 |
| **Total Net PnL** | **`2.94%`** | Positive Edge |
| **Max Drawdown** | **`8.85%`** | < 15.0% |
| **Sharpe Ratio** | **`0.3`** | > 1.50 |
| **Sortino Ratio** | **`0.56`** | > 2.00 |
| **Expectancy / Trade** | **`$8.16`** | Positive Expectancy |

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.1%`
- **SELL Signals**: `0.2%`
- **WAIT / HOLD**: `99.8%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: Predicted MFE excursion ($\sim 3.0 \times \text{ATR}_{14}$)
- **Stop Loss Protection**: Predicted MAE threshold ($\sim 1.5 \times \text{ATR}_{14}$)
- **Execution Cost Modeling**: 0.0% Taker Fee + 2.0 Tick Slippage
