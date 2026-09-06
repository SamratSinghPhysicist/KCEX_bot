# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 14:14:53 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.9604 USDT` | `₹9,441.26` | `-0.04%` |
| **Net Realized PnL** | **`-0.0396 USDT`** | **`₹-3.74`** | **`-0.04% Net ROI`** |
| **Gross Profit** | `+3.2748 USDT` | `₹309.30` | Total positive trade returns |
| **Gross Loss** | `-3.3144 USDT` | `₹313.05` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.99`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0784 USDT` | `₹7.40` | **`-0.08%` Peak-to-Trough** |
| **Win Rate** | **`49.70%`** | — | `8187 Wins / 8286 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-0.47` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-0.47` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.51` | — | Net ROI divided by Max Drawdown |

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
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
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
| **Winning Trades** | `8187` | `49.70%` of total trades |
| **Losing Trades** | `8286` | `50.30%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0000 USDT` (`₹-0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.2% ROE)` | Trade #23 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-3.2% ROE)` | Trade #5 (SHORT) |
| **Max Consecutive Wins** | `11` trades | Peak winning streak |
| **Max Consecutive Losses** | `15` trades | Peak losing streak |
| **Average Trade Duration** | `29.1s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #230 |
| **Longest Trade In-Position** | `10m 14s` | Trade #1700 |
| **Cumulative Time In Position** | `132h 58m 26s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `8197` (49.8%) | `8276` (50.2%) | `16473` |
| **Wins / Losses** | `4030 W / 4167 L` | `4157 W / 4119 L` | `8187 W / 8286 L` |
| **Win Rate** | **`49.16%`** | **`50.23%`** | **`49.70%`** |
| **Gross Profit** | `+1.6120 USDT` | `+1.6628 USDT` | `+3.2748 USDT` |
| **Gross Loss** | `-1.6668 USDT` | `-1.6476 USDT` | `-3.3144 USDT` |
| **Net Realized PnL** | **`-0.0548 USDT`** | **`+0.0152 USDT`** | **`-0.0396 USDT`** |
| **Net PnL (INR)** | `₹-5.18` | `₹+1.44` | `₹-3.74` |
| **Profit Factor** | `0.97` | `1.01` | `0.99` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `8187` | `49.7%` | `+3.2748 USDT` | `₹+309.30` | `100.0%` | `29.0s` |
| `STOP_LOSS_HIT` | `8286` | `50.3%` | `-3.3144 USDT` | `₹-313.05` | `0.0%` | `29.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:19 UTC | 20.0s | `4.809` | `4.811` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 01:20:59 UTC | 2026-01-01 01:21:15 UTC | 15.6s | `4.811` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `SHORT` | 2026-01-01 01:50:59 UTC | 2026-01-01 01:51:30 UTC | 30.9s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 4 | `SHORT` | 2026-01-01 02:36:59 UTC | 2026-01-01 02:38:34 UTC | 1m 34s | `4.793` | `4.791` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 5 | `SHORT` | 2026-01-01 04:19:59 UTC | 2026-01-01 04:20:00 UTC | 0.5s | `4.712` | `4.714` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 6 | `SHORT` | 2026-01-01 04:22:59 UTC | 2026-01-01 04:23:36 UTC | 36.7s | `4.712` | `4.710` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 7 | `SHORT` | 2026-01-01 04:31:59 UTC | 2026-01-01 04:32:54 UTC | 54.3s | `4.709` | `4.711` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 8 | `SHORT` | 2026-01-01 05:05:59 UTC | 2026-01-01 05:07:17 UTC | 1m 17s | `4.718` | `4.720` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 9 | `LONG` | 2026-01-01 05:45:59 UTC | 2026-01-01 05:48:43 UTC | 2m 43s | `4.715` | `4.713` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $99.9996 |
| 10 | `SHORT` | 2026-01-01 09:47:59 UTC | 2026-01-01 09:48:29 UTC | 29.2s | `4.737` | `4.735` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 11 | `LONG` | 2026-01-01 10:01:59 UTC | 2026-01-01 10:02:00 UTC | 0.6s | `4.738` | `4.740` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 12 | `SHORT` | 2026-01-01 11:12:59 UTC | 2026-01-01 11:15:41 UTC | 2m 41s | `4.713` | `4.715` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 13 | `LONG` | 2026-01-01 11:21:59 UTC | 2026-01-01 11:22:36 UTC | 36.5s | `4.716` | `4.718` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 14 | `SHORT` | 2026-01-01 11:26:59 UTC | 2026-01-01 11:30:05 UTC | 3m 05s | `4.717` | `4.719` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 15 | `LONG` | 2026-01-01 11:41:59 UTC | 2026-01-01 11:45:46 UTC | 3m 46s | `4.722` | `4.724` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 16 | `SHORT` | 2026-01-01 12:34:59 UTC | 2026-01-01 12:35:13 UTC | 13.1s | `4.713` | `4.711` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 17 | `SHORT` | 2026-01-01 12:46:59 UTC | 2026-01-01 12:47:26 UTC | 26.1s | `4.715` | `4.717` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 18 | `SHORT` | 2026-01-01 12:54:59 UTC | 2026-01-01 12:55:51 UTC | 51.6s | `4.713` | `4.711` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 19 | `SHORT` | 2026-01-01 14:22:59 UTC | 2026-01-01 14:23:34 UTC | 34.7s | `4.732` | `4.734` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 20 | `SHORT` | 2026-01-01 14:54:59 UTC | 2026-01-01 14:55:04 UTC | 4.7s | `4.742` | `4.740` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 21 | `LONG` | 2026-01-01 15:14:59 UTC | 2026-01-01 15:15:11 UTC | 11.8s | `4.738` | `4.736` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 22 | `LONG` | 2026-01-01 15:43:59 UTC | 2026-01-01 15:44:21 UTC | 21.9s | `4.740` | `4.738` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0000 |
| 23 | `LONG` | 2026-01-01 16:09:59 UTC | 2026-01-01 16:10:19 UTC | 19.9s | `4.741` | `4.743` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 24 | `LONG` | 2026-01-01 16:15:59 UTC | 2026-01-01 16:16:15 UTC | 15.1s | `4.743` | `4.745` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 25 | `LONG` | 2026-01-01 16:24:59 UTC | 2026-01-01 16:25:05 UTC | 5.0s | `4.737` | `4.739` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| ... | ... | *(16423 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 16449 | `LONG` | 2026-08-30 15:54:59 UTC | 2026-08-30 15:55:04 UTC | 4.8s | `2.518` | `2.520` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $99.9644 |
| 16450 | `SHORT` | 2026-08-30 16:03:59 UTC | 2026-08-30 16:04:06 UTC | 6.2s | `2.533` | `2.531` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $99.9648 |
| 16451 | `SHORT` | 2026-08-30 16:05:59 UTC | 2026-08-30 16:06:13 UTC | 13.1s | `2.533` | `2.535` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9644 |
| 16452 | `LONG` | 2026-08-30 16:12:59 UTC | 2026-08-30 16:13:00 UTC | 0.4s | `2.531` | `2.529` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9640 |
| 16453 | `LONG` | 2026-08-30 16:25:59 UTC | 2026-08-30 16:26:06 UTC | 6.2s | `2.553` | `2.551` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9636 |
| 16454 | `LONG` | 2026-08-30 16:58:59 UTC | 2026-08-30 16:59:01 UTC | 1.9s | `2.583` | `2.581` | $0.52 | $0.01 | $0.000000 | **-0.0004** | `-5.8%` | `STOP_LOSS_HIT` | $99.9632 |
| 16455 | `SHORT` | 2026-08-30 17:01:59 UTC | 2026-08-30 17:02:02 UTC | 3.0s | `2.577` | `2.579` | $0.52 | $0.01 | $0.000000 | **-0.0004** | `-5.8%` | `STOP_LOSS_HIT` | $99.9628 |
| 16456 | `LONG` | 2026-08-30 17:20:59 UTC | 2026-08-30 17:21:07 UTC | 7.9s | `2.561` | `2.559` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9624 |
| 16457 | `SHORT` | 2026-08-30 17:41:59 UTC | 2026-08-30 17:42:16 UTC | 16.4s | `2.550` | `2.548` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $99.9628 |
| 16458 | `LONG` | 2026-08-30 18:09:59 UTC | 2026-08-30 18:10:24 UTC | 24.2s | `2.540` | `2.538` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9624 |
| 16459 | `SHORT` | 2026-08-30 18:30:59 UTC | 2026-08-30 18:31:11 UTC | 11.6s | `2.554` | `2.556` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9620 |
| 16460 | `LONG` | 2026-08-30 18:45:59 UTC | 2026-08-30 18:46:29 UTC | 29.4s | `2.558` | `2.560` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $99.9624 |
| 16461 | `LONG` | 2026-08-30 18:52:59 UTC | 2026-08-30 18:53:23 UTC | 23.5s | `2.554` | `2.556` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $99.9628 |
| 16462 | `LONG` | 2026-08-30 19:05:59 UTC | 2026-08-30 19:06:05 UTC | 5.8s | `2.543` | `2.541` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9624 |
| 16463 | `SHORT` | 2026-08-30 19:15:59 UTC | 2026-08-30 19:16:07 UTC | 7.1s | `2.547` | `2.545` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $99.9628 |
| 16464 | `LONG` | 2026-08-30 19:25:59 UTC | 2026-08-30 19:26:50 UTC | 50.5s | `2.542` | `2.540` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9624 |
| 16465 | `LONG` | 2026-08-30 19:29:59 UTC | 2026-08-30 19:30:04 UTC | 4.3s | `2.540` | `2.538` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9620 |
| 16466 | `SHORT` | 2026-08-30 20:14:59 UTC | 2026-08-30 20:16:20 UTC | 1m 20s | `2.538` | `2.540` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9616 |
| 16467 | `LONG` | 2026-08-30 20:22:59 UTC | 2026-08-30 20:23:08 UTC | 8.3s | `2.538` | `2.536` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $99.9612 |
| 16468 | `LONG` | 2026-08-30 20:33:59 UTC | 2026-08-30 20:34:15 UTC | 15.7s | `2.518` | `2.516` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $99.9608 |
| 16469 | `SHORT` | 2026-08-30 20:59:59 UTC | 2026-08-30 21:00:00 UTC | 0.6s | `2.515` | `2.517` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $99.9604 |
| 16470 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:08 UTC | 8.4s | `2.505` | `2.507` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $99.9608 |
| 16471 | `SHORT` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:02 UTC | 2.5s | `2.506` | `2.508` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $99.9604 |
| 16472 | `LONG` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:03 UTC | 3.7s | `2.516` | `2.518` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $99.9608 |
| 16473 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:18 UTC | 18.2s | `2.501` | `2.499` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $99.9604 |

> 💡 *Full granular dataset with all 16473 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
