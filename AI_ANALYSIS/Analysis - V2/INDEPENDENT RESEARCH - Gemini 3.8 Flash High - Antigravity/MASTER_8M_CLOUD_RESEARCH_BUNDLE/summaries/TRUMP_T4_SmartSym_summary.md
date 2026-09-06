# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 13:10:24 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `101.0900 USDT` | `₹9,547.95` | `+1.09%` |
| **Net Realized PnL** | **`+1.0900 USDT`** | **`₹+102.95`** | **`+1.09% Net ROI`** |
| **Gross Profit** | `+3.8396 USDT` | `₹362.65` | Total positive trade returns |
| **Gross Loss** | `-2.7496 USDT` | `₹259.70` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.40`** | — | Profitable |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0116 USDT` | `₹1.10` | **`-0.01%` Peak-to-Trough** |
| **Win Rate** | **`58.27%`** | — | `9599 Wins / 6874 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `13.04` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `12.86` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `94.62` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `TRUMP_USDT` | Base Asset: `TRUMP` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `SMART_STRATEGY` | SMART_STRATEGY |
| **Strategy Preset** | `DEFAULT` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-01-01` → `2026-08-31` | Historical evaluation window |
| **High-Fidelity Simulation** | `DISABLED (Candle OHLC)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

### Strategy & Indicator Hyperparameters
| Hyperparameter | Value | Technical Context |
| :--- | :--- | :--- |
| **Active Strategy Engine** | `SMART_STRATEGY` | Quantitative model evaluated |
| **Active Strategy Preset** | `DEFAULT` | Selected preset configuration |
| **Directional Flow Mode** | `Autonomous Bi-Directional (LONG & SHORT)` | Order generation policy |
| **Signal Inversion Mode** | `DISABLED (Direct)` | Signal execution orientation |

### Trade Optimization & Regime Filters
| Filter Dimension | Configuration | Operational Action & Trigger |
| :--- | :--- | :--- |
| **Trade Duration Monitoring** | `DISABLED` | Deep in-position monitoring at `60.0s` elapsed |
| **Time-Stop Protective Exit** | `DISABLED` | Action `CLOSE` triggered if open duration > `90.0s` |
| **ADX Trend Regime Filter** | `DISABLED` | Period: `14` / Threshold: `25.0` |
| **HTF Trend Baseline (200 EMA)** | `DISABLED` | Timeframe: `15m` / Period: `200` |
| **Hourly Session Filter** | `DISABLED` | Blacklisted UTC Hours: `None` |
| **Directional Bias Policy** | `BOTH` | Pre-trade signal directional allowance |

### Position Sizing, Leverage & Risk Management
| Risk Parameter | Value | Operational Details |
| :--- | :--- | :--- |
| **Sizing Mode** | `MULTIPLIER` | Mode: `CONTRACTS`, `MULTIPLIER`, or `MIN` |
| **Trade Volume / Quantity** | `2 contract(s) (0.2 TRUMP per trade)` | Quantity committed per trade signal |
| **Leverage Multiplier** | `75x` | Margin required = Position Notional / Leverage |
| **Starting Capital** | `100.00 USDT` | `₹9,445.00 INR` (`1 USDT = ₹94.45`) |
| **Take Profit Target** | `+2 ticks` (`+0.002 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-2 ticks away from entry (0.002 USDT)` | Stop loss evaluation logic |

### Exchange Contract Specifications & Fees
| Specification | Value | Notes |
| :--- | :--- | :--- |
| **Fee Schedule Mode** | `ZERO` | Live KCEX API, 0.0% zero-fee pair, or manual rate |
| **Maker Fee Rate** | `0.0000%` | Rate for passive limit orders |
| **Taker Fee Rate** | `0.0000%` | Rate for aggressive market / stop triggers |
| **Contract Size (cs)** | `0.1 TRUMP` | 1 contract = 0.1 underlying coin |
| **Price Unit (pu / tick)** | `0.001` | Minimum tick increment on order book |
| **Price Precision** | `3 decimal places` | Precision formatting for quotes and orders |
| **Min Volume** | `1.0 contract(s)` | Minimum permissible order size |
| **Max Leverage** | `75x` | Maximum allowed leverage on exchange |

---

## 📈 Trade Execution & Statistical Breakdown

| Metric | Value | Context / Benchmark |
| :--- | :--- | :--- |
| **Total Trades Executed** | `16473` | Total completed trade lifecycle events |
| **Winning Trades** | `9599` | `58.27%` of total trades |
| **Losing Trades** | `6874` | `41.73%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0001 USDT` (`₹+0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.2% ROE)` | Trade #23 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-3.2% ROE)` | Trade #5 (SHORT) |
| **Max Consecutive Wins** | `34` trades | Peak winning streak |
| **Max Consecutive Losses** | `12` trades | Peak losing streak |
| **Average Trade Duration** | `1m 12s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `1m 00s` | Trade #1 |
| **Longest Trade In-Position** | `11m 00s` | Trade #1700 |
| **Cumulative Time In Position** | `333h 01m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `8197` (49.8%) | `8276` (50.2%) | `16473` |
| **Wins / Losses** | `4744 W / 3453 L` | `4855 W / 3421 L` | `9599 W / 6874 L` |
| **Win Rate** | **`57.87%`** | **`58.66%`** | **`58.27%`** |
| **Gross Profit** | `+1.8976 USDT` | `+1.9420 USDT` | `+3.8396 USDT` |
| **Gross Loss** | `-1.3812 USDT` | `-1.3684 USDT` | `-2.7496 USDT` |
| **Net Realized PnL** | **`+0.5164 USDT`** | **`+0.5736 USDT`** | **`+1.0900 USDT`** |
| **Net PnL (INR)** | `₹+48.77` | `₹+54.18` | `₹+102.95` |
| **Profit Factor** | `1.37` | `1.42` | `1.40` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `9599` | `58.3%` | `+3.8396 USDT` | `₹+362.65` | `100.0%` | `1m 11s` |
| `STOP_LOSS_HIT` | `6874` | `41.7%` | `-2.7496 USDT` | `₹-259.70` | `0.0%` | `1m 14s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `4.809` | `4.811` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 01:20:59 UTC | 2026-01-01 01:21:59 UTC | 1m 00s | `4.811` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `SHORT` | 2026-01-01 01:50:59 UTC | 2026-01-01 01:51:59 UTC | 1m 00s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 4 | `SHORT` | 2026-01-01 02:36:59 UTC | 2026-01-01 02:38:59 UTC | 2m 00s | `4.793` | `4.791` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 5 | `SHORT` | 2026-01-01 04:19:59 UTC | 2026-01-01 04:20:59 UTC | 1m 00s | `4.712` | `4.714` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 6 | `SHORT` | 2026-01-01 04:22:59 UTC | 2026-01-01 04:23:59 UTC | 1m 00s | `4.712` | `4.710` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 7 | `SHORT` | 2026-01-01 04:31:59 UTC | 2026-01-01 04:32:59 UTC | 1m 00s | `4.709` | `4.711` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 8 | `SHORT` | 2026-01-01 05:05:59 UTC | 2026-01-01 05:07:59 UTC | 2m 00s | `4.718` | `4.720` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 9 | `LONG` | 2026-01-01 05:45:59 UTC | 2026-01-01 05:48:59 UTC | 3m 00s | `4.715` | `4.713` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $99.9996 |
| 10 | `SHORT` | 2026-01-01 09:47:59 UTC | 2026-01-01 09:48:59 UTC | 1m 00s | `4.737` | `4.735` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 11 | `LONG` | 2026-01-01 10:01:59 UTC | 2026-01-01 10:02:59 UTC | 1m 00s | `4.738` | `4.740` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 12 | `SHORT` | 2026-01-01 11:12:59 UTC | 2026-01-01 11:15:59 UTC | 3m 00s | `4.713` | `4.715` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 13 | `LONG` | 2026-01-01 11:21:59 UTC | 2026-01-01 11:22:59 UTC | 1m 00s | `4.716` | `4.718` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 14 | `SHORT` | 2026-01-01 11:26:59 UTC | 2026-01-01 11:30:59 UTC | 4m 00s | `4.717` | `4.719` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 15 | `LONG` | 2026-01-01 11:41:59 UTC | 2026-01-01 11:45:59 UTC | 4m 00s | `4.722` | `4.724` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 16 | `SHORT` | 2026-01-01 12:34:59 UTC | 2026-01-01 12:35:59 UTC | 1m 00s | `4.713` | `4.711` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 17 | `SHORT` | 2026-01-01 12:46:59 UTC | 2026-01-01 12:47:59 UTC | 1m 00s | `4.715` | `4.717` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 18 | `SHORT` | 2026-01-01 12:54:59 UTC | 2026-01-01 12:55:59 UTC | 1m 00s | `4.713` | `4.711` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 19 | `SHORT` | 2026-01-01 14:22:59 UTC | 2026-01-01 14:23:59 UTC | 1m 00s | `4.732` | `4.734` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 20 | `SHORT` | 2026-01-01 14:54:59 UTC | 2026-01-01 14:55:59 UTC | 1m 00s | `4.742` | `4.740` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 21 | `LONG` | 2026-01-01 15:14:59 UTC | 2026-01-01 15:15:59 UTC | 1m 00s | `4.738` | `4.736` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 22 | `LONG` | 2026-01-01 15:43:59 UTC | 2026-01-01 15:44:59 UTC | 1m 00s | `4.740` | `4.738` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 23 | `LONG` | 2026-01-01 16:09:59 UTC | 2026-01-01 16:10:59 UTC | 1m 00s | `4.741` | `4.743` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 24 | `LONG` | 2026-01-01 16:15:59 UTC | 2026-01-01 16:16:59 UTC | 1m 00s | `4.743` | `4.745` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 25 | `LONG` | 2026-01-01 16:24:59 UTC | 2026-01-01 16:25:59 UTC | 1m 00s | `4.737` | `4.739` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| ... | ... | *(16423 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 16449 | `LONG` | 2026-08-30 15:54:59 UTC | 2026-08-30 15:55:59 UTC | 1m 00s | `2.518` | `2.520` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.0884 |
| 16450 | `SHORT` | 2026-08-30 16:03:59 UTC | 2026-08-30 16:04:59 UTC | 1m 00s | `2.533` | `2.531` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0888 |
| 16451 | `SHORT` | 2026-08-30 16:05:59 UTC | 2026-08-30 16:06:59 UTC | 1m 00s | `2.533` | `2.531` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0892 |
| 16452 | `LONG` | 2026-08-30 16:12:59 UTC | 2026-08-30 16:13:59 UTC | 1m 00s | `2.531` | `2.533` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0896 |
| 16453 | `LONG` | 2026-08-30 16:25:59 UTC | 2026-08-30 16:26:59 UTC | 1m 00s | `2.553` | `2.555` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0900 |
| 16454 | `LONG` | 2026-08-30 16:58:59 UTC | 2026-08-30 16:59:59 UTC | 1m 00s | `2.583` | `2.581` | $0.52 | $0.01 | $0.000000 | **-0.0004** | `-5.8%` | `STOP_LOSS_HIT` | $101.0896 |
| 16455 | `SHORT` | 2026-08-30 17:01:59 UTC | 2026-08-30 17:02:59 UTC | 1m 00s | `2.577` | `2.575` | $0.52 | $0.01 | $0.000000 | **+0.0004** | `+5.8%` | `MIN_PROFIT_TP_HIT` | $101.0900 |
| 16456 | `LONG` | 2026-08-30 17:20:59 UTC | 2026-08-30 17:21:59 UTC | 1m 00s | `2.561` | `2.563` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0904 |
| 16457 | `SHORT` | 2026-08-30 17:41:59 UTC | 2026-08-30 17:42:59 UTC | 1m 00s | `2.550` | `2.548` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0908 |
| 16458 | `LONG` | 2026-08-30 18:09:59 UTC | 2026-08-30 18:10:59 UTC | 1m 00s | `2.540` | `2.538` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0904 |
| 16459 | `SHORT` | 2026-08-30 18:30:59 UTC | 2026-08-30 18:31:59 UTC | 1m 00s | `2.554` | `2.556` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0900 |
| 16460 | `LONG` | 2026-08-30 18:45:59 UTC | 2026-08-30 18:46:59 UTC | 1m 00s | `2.558` | `2.560` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0904 |
| 16461 | `LONG` | 2026-08-30 18:52:59 UTC | 2026-08-30 18:53:59 UTC | 1m 00s | `2.554` | `2.556` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0908 |
| 16462 | `LONG` | 2026-08-30 19:05:59 UTC | 2026-08-30 19:06:59 UTC | 1m 00s | `2.543` | `2.541` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0904 |
| 16463 | `SHORT` | 2026-08-30 19:15:59 UTC | 2026-08-30 19:16:59 UTC | 1m 00s | `2.547` | `2.545` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0908 |
| 16464 | `LONG` | 2026-08-30 19:25:59 UTC | 2026-08-30 19:26:59 UTC | 1m 00s | `2.542` | `2.540` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0904 |
| 16465 | `LONG` | 2026-08-30 19:29:59 UTC | 2026-08-30 19:30:59 UTC | 1m 00s | `2.540` | `2.542` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.0908 |
| 16466 | `SHORT` | 2026-08-30 20:14:59 UTC | 2026-08-30 20:16:59 UTC | 2m 00s | `2.538` | `2.540` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0904 |
| 16467 | `LONG` | 2026-08-30 20:22:59 UTC | 2026-08-30 20:23:59 UTC | 1m 00s | `2.538` | `2.536` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $101.0900 |
| 16468 | `LONG` | 2026-08-30 20:33:59 UTC | 2026-08-30 20:34:59 UTC | 1m 00s | `2.518` | `2.516` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $101.0896 |
| 16469 | `SHORT` | 2026-08-30 20:59:59 UTC | 2026-08-30 21:00:59 UTC | 1m 00s | `2.515` | `2.513` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.0900 |
| 16470 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:59 UTC | 1m 00s | `2.505` | `2.507` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.0904 |
| 16471 | `SHORT` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:59 UTC | 1m 00s | `2.506` | `2.508` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $101.0900 |
| 16472 | `LONG` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:59 UTC | 1m 00s | `2.516` | `2.518` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.0904 |
| 16473 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `2.501` | `2.499` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $101.0900 |

> 💡 *Full granular dataset with all 16473 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
