# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 01:32:59 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.1508 USDT` | `₹9,459.24` | `+0.15%` |
| **Net Realized PnL** | **`+0.1508 USDT`** | **`₹+14.24`** | **`+0.15% Net ROI`** |
| **Gross Profit** | `+0.5628 USDT` | `₹53.16` | Total positive trade returns |
| **Gross Loss** | `-0.4120 USDT` | `₹38.91` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.37`** | — | Profitable |
| **Win / Loss Payoff** | `0.40` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0084 USDT` | `₹0.79` | **`-0.01%` Peak-to-Trough** |
| **Win Rate** | **`77.35%`** | — | `1407 Wins / 412 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `11.00` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `6.45` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `17.97` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `TRUMP_USDT` | Base Asset: `TRUMP` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-07-01` → `2026-07-14` | Historical evaluation window |
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

### Strategy & Indicator Hyperparameters
| Hyperparameter | Value | Technical Context |
| :--- | :--- | :--- |
| **Active Strategy Engine** | `STOCH_RSI` | Quantitative model evaluated |
| **Active Strategy Preset** | `FAST_SCALP` | Selected preset configuration |
| **RSI Period** | `9` | Relative Strength Index calculation length |
| **Stoch Lookback Period** | `9` | Stochastic window over RSI |
| **%K Smoothing** | `3` | Fast stochastic line smoothing period |
| **%D Smoothing** | `3` | Slow signal line smoothing period |
| **Oversold Threshold (OS)** | `20.0` | Extreme oversold boundary (Bullish entry gate) |
| **Overbought Threshold (OB)** | `80.0` | Extreme overbought boundary (Bearish entry gate) |
| **Extreme Zone Filter** | `ENABLED` | Suppresses non-extreme neutral whipsaws |
| **Candle Close Confirmation** | `ENABLED` | Requires bar to close before emitting cross |
| **Directional Flow Mode** | `Autonomous Bi-Directional (LONG & SHORT)` | Order generation policy |

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
| **Stop Loss Rule** | `-5 ticks away from entry (0.005 USDT)` | Stop loss evaluation logic |

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
| **Total Trades Executed** | `1819` | Total completed trade lifecycle events |
| **Winning Trades** | `1407` | `77.35%` of total trades |
| **Losing Trades** | `412` | `22.65%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0001 USDT` (`₹+0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0010 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+9.0% ROE)` | Trade #1 (LONG) |
| **Largest Losing Trade** | `-0.0010 USDT (-22.5% ROE)` | Trade #2 (SHORT) |
| **Max Consecutive Wins** | `26` trades | Peak winning streak |
| **Max Consecutive Losses** | `4` trades | Peak losing streak |
| **Average Trade Duration** | `4m 06s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #288 |
| **Longest Trade In-Position** | `1h 15m 46s` | Trade #1540 |
| **Cumulative Time In Position** | `124h 45m 43s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `894` (49.1%) | `925` (50.9%) | `1819` |
| **Wins / Losses** | `694 W / 200 L` | `713 W / 212 L` | `1407 W / 412 L` |
| **Win Rate** | **`77.63%`** | **`77.08%`** | **`77.35%`** |
| **Gross Profit** | `+0.2776 USDT` | `+0.2852 USDT` | `+0.5628 USDT` |
| **Gross Loss** | `-0.2000 USDT` | `-0.2120 USDT` | `-0.4120 USDT` |
| **Net Realized PnL** | **`+0.0776 USDT`** | **`+0.0732 USDT`** | **`+0.1508 USDT`** |
| **Net PnL (INR)** | `₹+7.33` | `₹+6.91` | `₹+14.24` |
| **Profit Factor** | `1.39` | `1.35` | `1.37` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `1407` | `77.4%` | `+0.5628 USDT` | `₹+53.16` | `100.0%` | `3m 17s` |
| `STOP_LOSS_HIT` | `412` | `22.6%` | `-0.4120 USDT` | `₹-38.91` | `0.0%` | `6m 54s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:47 UTC | 47.6s | `1.661` | `1.663` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-07-01 00:36:59 UTC | 2026-07-01 00:52:44 UTC | 15m 44s | `1.664` | `1.669` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.5%` | `STOP_LOSS_HIT` | $99.9994 |
| 3 | `SHORT` | 2026-07-01 00:55:59 UTC | 2026-07-01 00:56:42 UTC | 42.7s | `1.669` | `1.667` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $99.9998 |
| 4 | `LONG` | 2026-07-01 01:01:59 UTC | 2026-07-01 01:02:09 UTC | 9.1s | `1.667` | `1.669` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 5 | `LONG` | 2026-07-01 01:09:59 UTC | 2026-07-01 01:11:30 UTC | 1m 30s | `1.661` | `1.656` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9992 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:03 UTC | 3.2s | `1.645` | `1.647` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 7 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:12 UTC | 12.6s | `1.658` | `1.656` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 8 | `SHORT` | 2026-07-01 01:34:59 UTC | 2026-07-01 01:36:14 UTC | 1m 14s | `1.658` | `1.663` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9990 |
| 9 | `SHORT` | 2026-07-01 01:47:59 UTC | 2026-07-01 01:50:09 UTC | 2m 09s | `1.676` | `1.674` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $99.9994 |
| 10 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:10 UTC | 10.2s | `1.676` | `1.678` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $99.9998 |
| 11 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 02:02:36 UTC | 3m 36s | `1.678` | `1.683` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 12 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:05:51 UTC | 1m 51s | `1.685` | `1.680` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.3%` | `STOP_LOSS_HIT` | $99.9978 |
| 13 | `LONG` | 2026-07-01 02:08:59 UTC | 2026-07-01 02:09:39 UTC | 39.7s | `1.684` | `1.686` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $99.9982 |
| 14 | `SHORT` | 2026-07-01 02:17:59 UTC | 2026-07-01 02:22:04 UTC | 4m 04s | `1.702` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9972 |
| 15 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:31:13 UTC | 1m 13s | `1.705` | `1.707` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $99.9976 |
| 16 | `LONG` | 2026-07-01 02:34:59 UTC | 2026-07-01 02:35:05 UTC | 5.7s | `1.704` | `1.706` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| 17 | `LONG` | 2026-07-01 02:40:59 UTC | 2026-07-01 02:44:01 UTC | 3m 01s | `1.697` | `1.699` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $99.9984 |
| 18 | `SHORT` | 2026-07-01 03:00:59 UTC | 2026-07-01 03:01:34 UTC | 34.2s | `1.704` | `1.709` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9974 |
| 19 | `SHORT` | 2026-07-01 03:04:59 UTC | 2026-07-01 03:05:07 UTC | 7.4s | `1.707` | `1.712` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9964 |
| 20 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:04 UTC | 4.8s | `1.729` | `1.727` | $0.35 | $0.00 | $0.000000 | **+0.0004** | `+8.7%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 21 | `LONG` | 2026-07-01 03:15:59 UTC | 2026-07-01 03:16:12 UTC | 12.1s | `1.711` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9958 |
| 22 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:23:46 UTC | 3m 46s | `1.704` | `1.699` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9948 |
| 23 | `LONG` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:29:01 UTC | 1m 01s | `1.699` | `1.701` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $99.9952 |
| 24 | `SHORT` | 2026-07-01 03:32:59 UTC | 2026-07-01 03:34:17 UTC | 1m 17s | `1.699` | `1.697` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $99.9956 |
| 25 | `SHORT` | 2026-07-01 03:41:59 UTC | 2026-07-01 03:47:01 UTC | 5m 01s | `1.706` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9946 |
| ... | ... | *(1769 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1795 | `SHORT` | 2026-07-13 19:36:59 UTC | 2026-07-13 19:50:00 UTC | 13m 00s | `1.532` | `1.537` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $100.1482 |
| 1796 | `LONG` | 2026-07-13 19:51:59 UTC | 2026-07-13 19:56:57 UTC | 4m 57s | `1.536` | `1.538` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1486 |
| 1797 | `LONG` | 2026-07-13 20:02:59 UTC | 2026-07-13 20:05:01 UTC | 2m 01s | `1.536` | `1.538` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1490 |
| 1798 | `LONG` | 2026-07-13 20:10:59 UTC | 2026-07-13 20:18:56 UTC | 7m 56s | `1.535` | `1.530` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $100.1480 |
| 1799 | `LONG` | 2026-07-13 20:22:59 UTC | 2026-07-13 20:23:11 UTC | 11.6s | `1.532` | `1.534` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1484 |
| 1800 | `SHORT` | 2026-07-13 20:27:59 UTC | 2026-07-13 20:44:04 UTC | 16m 04s | `1.535` | `1.533` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1488 |
| 1801 | `LONG` | 2026-07-13 20:47:59 UTC | 2026-07-13 20:55:16 UTC | 7m 16s | `1.532` | `1.534` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1492 |
| 1802 | `SHORT` | 2026-07-13 20:57:59 UTC | 2026-07-13 21:00:15 UTC | 2m 15s | `1.534` | `1.532` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1496 |
| 1803 | `SHORT` | 2026-07-13 21:01:59 UTC | 2026-07-13 21:09:23 UTC | 7m 23s | `1.533` | `1.531` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1500 |
| 1804 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:05 UTC | 6.0s | `1.530` | `1.532` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1504 |
| 1805 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:54 UTC | 54.1s | `1.534` | `1.532` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1508 |
| 1806 | `LONG` | 2026-07-13 21:33:59 UTC | 2026-07-13 21:38:10 UTC | 4m 10s | `1.530` | `1.525` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $100.1498 |
| 1807 | `LONG` | 2026-07-13 21:43:59 UTC | 2026-07-13 21:47:02 UTC | 3m 02s | `1.523` | `1.525` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1502 |
| 1808 | `SHORT` | 2026-07-13 21:51:59 UTC | 2026-07-13 22:01:55 UTC | 9m 55s | `1.524` | `1.529` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $100.1492 |
| 1809 | `SHORT` | 2026-07-13 22:05:59 UTC | 2026-07-13 22:06:56 UTC | 56.8s | `1.532` | `1.530` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1496 |
| 1810 | `LONG` | 2026-07-13 22:13:59 UTC | 2026-07-13 22:16:02 UTC | 2m 02s | `1.532` | `1.534` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1500 |
| 1811 | `SHORT` | 2026-07-13 22:20:59 UTC | 2026-07-13 22:21:03 UTC | 3.3s | `1.536` | `1.534` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1504 |
| 1812 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:04 UTC | 4.8s | `1.534` | `1.532` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1508 |
| 1813 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:04 UTC | 4.0s | `1.534` | `1.536` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1512 |
| 1814 | `LONG` | 2026-07-13 22:36:59 UTC | 2026-07-13 22:43:57 UTC | 6m 57s | `1.533` | `1.535` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1516 |
| 1815 | `SHORT` | 2026-07-13 22:48:59 UTC | 2026-07-13 22:51:25 UTC | 2m 25s | `1.535` | `1.533` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1520 |
| 1816 | `LONG` | 2026-07-13 22:56:59 UTC | 2026-07-13 23:19:32 UTC | 22m 32s | `1.534` | `1.536` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.1524 |
| 1817 | `SHORT` | 2026-07-13 23:23:59 UTC | 2026-07-13 23:35:17 UTC | 11m 17s | `1.534` | `1.539` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $100.1514 |
| 1818 | `SHORT` | 2026-07-13 23:43:59 UTC | 2026-07-13 23:54:10 UTC | 10m 10s | `1.539` | `1.544` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $100.1504 |
| 1819 | `SHORT` | 2026-07-13 23:56:59 UTC | 2026-07-14 00:06:08 UTC | 9m 08s | `1.543` | `1.541` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.7%` | `MIN_PROFIT_TP_HIT` | $100.1508 |

> 💡 *Full granular dataset with all 1819 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
