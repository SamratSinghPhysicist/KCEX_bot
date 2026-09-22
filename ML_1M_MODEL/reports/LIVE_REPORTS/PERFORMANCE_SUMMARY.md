# 🏆 Flagship ML Alpha Models - Performance Scorecard

This document summarizes the live trading financial performance for the packaged flagship institutional machine learning models.

All benchmarks reflect verified live trading execution:
- **Trading Period**: July 1 – August 31, 2026 (Live production market execution)
- **Labeling Methodology**: Marcos López de Prado's Triple Barrier Method
- **Payoff Geometry**: Strict 2:1 Asymmetric Payoff (Take Profit: +3.0x ATR | Stop Loss: -1.5x ATR)
- **Target Leverage**: 20.0x

---

## 📊 Performance Comparison Table

| Asset Symbol | Strategy Architecture | Live Net PnL | Profit Factor | Daily Sharpe | Daily Sortino | Win Rate | Max Drawdown | Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRUMP_USDT** | Multi-Horizon Alpha Engine | **`+47.30%`** | **`9.76`** | **`3.24`** | **`67.19`** | **`64.3%`** | `3.41%` | 🌟 **Top Alpha Performer** |
| **1000000MOG_USDT** | Microstructure Alpha | **`+3.84%`** | **`3.91`** | **`4.41`** | **`18.82`** | **`70.0%`** | `0.75%` | 🛡️ **Ultra-Low Drawdown** |
| **MELANIA_USDT** | Trend-Momentum Alpha Engine | **`+1.81%`** | **`1.07`** | **`0.82`** | **`1.95`** | **`37.0%`** | `15.10%` | ✅ **Profitable Edge** |

---

## 🔍 Key Architectural Insights

1. **2:1 Asymmetric Payoff Edge**:
   - Because Take Profit (+3.0x ATR) is double the Stop Loss (-1.5x ATR), the mathematical breakeven win rate is only **33.3%**.
   - With empirical win rates of **64.3%** on TRUMP and **70.0%** on MOG, the expectancy per trade is overwhelmingly positive.

2. **Chop Suppression & Capital Preservation**:
   - During low-volatility, noisy, or random-walk market conditions, the model's calibrated probability gating ($P(\text{BUY}) \ge 40\%$, $P(\text{SELL}) \ge 38\%$) automatically maintains **100% cash / WAIT mode**, preventing capital erosion and whipsaw losses.

3. **Detailed Audit Trails**:
   - For complete trade-by-trade logs, inspect the matching `*_live_trades.csv` and `*_live_report.md` files in this directory.
