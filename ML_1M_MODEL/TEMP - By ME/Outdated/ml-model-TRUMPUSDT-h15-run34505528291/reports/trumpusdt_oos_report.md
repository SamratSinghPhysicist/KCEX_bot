# 🤖 ML Model Out-of-Sample Performance: TRUMPUSDT

## 📊 Executive Summary
| Metric | Value | Benchmark Target |
| :--- | :--- | :--- |
| **Asset Symbol** | `TRUMPUSDT` | 1-Minute Microstructure |
| **Out-of-Sample Bars** | `26,493` 1m bars | Chronologically Isolated |
| **Total Trades** | `71` | High Conviction Only |
| **Win Rate** | **`42.25%`** | > 50% |
| **Profit Factor** | **`0.91`** | > 1.50 |
| **Total Net PnL** | **`-5.54%`** | Positive Edge |
| **Max Drawdown** | **`16.65%`** | < 15.0% |
| **Sharpe Ratio** | **`-0.21`** | > 1.50 |
| **Sortino Ratio** | **`-0.72`** | > 2.00 |
| **Expectancy / Trade** | **`$-7.81`** | Positive Expectancy |

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `0.1%`
- **SELL Signals**: `0.3%`
- **WAIT / HOLD**: `99.5%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: Predicted MFE excursion ($\sim 3.0 \times \text{ATR}_{14}$)
- **Stop Loss Protection**: Predicted MAE threshold ($\sim 1.5 \times \text{ATR}_{14}$)
- **Execution Cost Modeling**: 0.02% Taker Fee + 1.0 Tick Slippage
