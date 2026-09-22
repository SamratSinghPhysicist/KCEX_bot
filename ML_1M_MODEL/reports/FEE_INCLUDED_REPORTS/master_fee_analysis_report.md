# 📊 Master Comparative Performance Report: 0.10% Fee Experiment
**Evaluation Universe:** `TRUMPUSDT`, `1000000MOGUSDT`, `MELANIAUSDT`  
**Test Protocol:** 2-Month Out-of-Sample Historical Simulation (July 1 – August 31, 2026)  
**Execution Modeling:** 0.10% Total Round-trip Fee (0.05% entry + 0.05% exit) + 2.0 Ticks Slippage + 20x Leverage  

---

## 🚀 Executive Comparison Matrix

| Symbol | Baseline PnL (0.0% Fee) | Fee-Adjusted PnL (0.1% Fee) | Baseline PF | Fee-Adjusted PF | Win Rate (0.1% Fee) | Max Drawdown | Expectancy / Trade | Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TRUMP** | `+47.30%` | **`+43.33%`** | `9.76` | **`7.74`** | `64.29%` | `3.99%` | `$+309.52` | ✅ Super Robust |
| **MOG** | `+3.84%` | **`+1.79%`** | `3.91` | **`1.94`** | `70.0%` | `0.95%` | `$+17.92` | ✅ Profitable |
| **MELANIA** | `+1.81%` | **`-3.54%`** | `1.07` | **`0.88`** | `33.33%` | `16.15%` | `$-13.12` | ❌ Negative Edge |

---

## 🔬 Cross-Asset Quantitative Insights

### 1. TRUMPUSDT — High Volatility Alpha Beast
- **Why it thrives:** TRUMP's average winning trade is **+2.54% gross**. Deducting **0.10%** fees takes away only a tiny 3.9% slice of its winning margin.
- **Result:** Profit factor stays extraordinarily high at **7.74** with **+43.33% net return**. It can easily be traded on any high-fee platform.

### 2. 1000000MOGUSDT — High Win-Rate Scalper
- **Why it holds up:** MOG achieves a **70.0% win rate** with tight stops. While its average winning trade is **+0.36% gross**, a 0.10% fee cuts the profit factor from 3.91 down to **1.94**.
- **Result:** It remains solid and profitable (**+1.79% net return**), but turns breakeven if fees exceed **0.18%**.

### 3. MELANIAUSDT — Low Margin Sensitivity
- **Why it suffers:** Under zero-fee conditions, MELANIA generated an average gross gain of only **+0.049% per trade** across 27 trades.
- **Result:** A 0.10% fee exceeds the entire per-trade edge, inflicting 2.70% cumulative fee friction (54% on 20x margin) and turning the performance from **+1.81%** into **-3.54%**. MELANIA requires either KCEX's zero-fee environment or tighter minimum profit filters.

---

## 📂 Artifacts Generated in this Directory
- 📄 `master_fee_analysis_report.md` (This master document)
- 📄 `trumpusdt_fee_0.1pct_report.md` & `trumpusdt_fee_0.1pct_trades.csv`
- 📄 `1000000mogusdt_fee_0.1pct_report.md` & `1000000mogusdt_fee_0.1pct_trades.csv`
- 📄 `melaniausdt_fee_0.1pct_report.md` & `melaniausdt_fee_0.1pct_trades.csv`
- 📊 `combined_fee_metrics.json`
