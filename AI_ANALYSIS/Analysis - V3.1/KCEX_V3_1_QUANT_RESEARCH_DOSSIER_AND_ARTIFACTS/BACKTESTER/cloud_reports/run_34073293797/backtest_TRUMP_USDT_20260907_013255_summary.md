# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 01:32:55 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0212 USDT` | `₹9,447.00` | `+0.02%` |
| **Net Realized PnL** | **`+0.0212 USDT`** | **`₹+2.00`** | **`+0.02% Net ROI`** |
| **Gross Profit** | `+0.2992 USDT` | `₹28.26` | Total positive trade returns |
| **Gross Loss** | `-0.2780 USDT` | `₹26.26` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.08`** | — | Profitable |
| **Win / Loss Payoff** | `0.40` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0292 USDT` | `₹2.76` | **`-0.03%` Peak-to-Trough** |
| **Win Rate** | **`72.90%`** | — | `748 Wins / 278 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `2.58` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `1.61` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `0.73` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `TRUMP_USDT` | Base Asset: `TRUMP` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `EMA_CROSSOVER` | EMA Crossover Trend Follower (Preset: 5/13 ; Closed Candle Confirmation: True) |
| **Strategy Preset** | `5/13` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-07-01` → `2026-07-14` | Historical evaluation window |
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

### Strategy & Indicator Hyperparameters
| Hyperparameter | Value | Technical Context |
| :--- | :--- | :--- |
| **Active Strategy Engine** | `EMA_CROSSOVER` | Quantitative model evaluated |
| **Active Strategy Preset** | `5/13` | Selected preset configuration |
| **Fast EMA Period** | `5` | Short-term fast moving average |
| **Slow EMA Period** | `13` | Baseline slow moving average |
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
| **Total Trades Executed** | `1026` | Total completed trade lifecycle events |
| **Winning Trades** | `748` | `72.90%` of total trades |
| **Losing Trades** | `278` | `27.10%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0010 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+9.0% ROE)` | Trade #1 (SHORT) |
| **Largest Losing Trade** | `-0.0010 USDT (-22.1% ROE)` | Trade #6 (SHORT) |
| **Max Consecutive Wins** | `19` trades | Peak winning streak |
| **Max Consecutive Losses** | `4` trades | Peak losing streak |
| **Average Trade Duration** | `4m 36s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #615 |
| **Longest Trade In-Position** | `1h 27m 51s` | Trade #854 |
| **Cumulative Time In Position** | `78h 53m 19s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `519` (50.6%) | `507` (49.4%) | `1026` |
| **Wins / Losses** | `373 W / 146 L` | `375 W / 132 L` | `748 W / 278 L` |
| **Win Rate** | **`71.87%`** | **`73.96%`** | **`72.90%`** |
| **Gross Profit** | `+0.1492 USDT` | `+0.1500 USDT` | `+0.2992 USDT` |
| **Gross Loss** | `-0.1460 USDT` | `-0.1320 USDT` | `-0.2780 USDT` |
| **Net Realized PnL** | **`+0.0032 USDT`** | **`+0.0180 USDT`** | **`+0.0212 USDT`** |
| **Net PnL (INR)** | `₹+0.30` | `₹+1.70` | `₹+2.00` |
| **Profit Factor** | `1.02` | `1.14` | `1.08` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `748` | `72.9%` | `+0.2992 USDT` | `₹+28.26` | `100.0%` | `3m 44s` |
| `STOP_LOSS_HIT` | `278` | `27.1%` | `-0.2780 USDT` | `₹-26.26` | `0.0%` | `6m 57s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-07-01 00:24:59 UTC | 2026-07-01 00:25:39 UTC | 39.9s | `1.660` | `1.658` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `LONG` | 2026-07-01 00:30:59 UTC | 2026-07-01 00:31:11 UTC | 11.9s | `1.665` | `1.667` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `SHORT` | 2026-07-01 00:49:59 UTC | 2026-07-01 00:51:03 UTC | 1m 03s | `1.667` | `1.665` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `SHORT` | 2026-07-01 01:05:59 UTC | 2026-07-01 01:07:03 UTC | 1m 03s | `1.663` | `1.661` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 5 | `LONG` | 2026-07-01 01:23:59 UTC | 2026-07-01 01:29:22 UTC | 5m 22s | `1.656` | `1.658` | $0.33 | $0.00 | $0.000000 | **+0.0004** | `+9.1%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 6 | `SHORT` | 2026-07-01 02:37:59 UTC | 2026-07-01 02:38:35 UTC | 35.3s | `1.696` | `1.701` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $100.0010 |
| 7 | `LONG` | 2026-07-01 02:58:59 UTC | 2026-07-01 03:00:56 UTC | 1m 56s | `1.702` | `1.704` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0014 |
| 8 | `SHORT` | 2026-07-01 03:16:59 UTC | 2026-07-01 03:17:03 UTC | 3.8s | `1.704` | `1.702` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 9 | `LONG` | 2026-07-01 03:38:59 UTC | 2026-07-01 03:39:14 UTC | 14.8s | `1.704` | `1.706` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 10 | `SHORT` | 2026-07-01 04:00:59 UTC | 2026-07-01 04:02:45 UTC | 1m 45s | `1.707` | `1.705` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0026 |
| 11 | `LONG` | 2026-07-01 04:20:59 UTC | 2026-07-01 04:22:31 UTC | 1m 31s | `1.704` | `1.706` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0030 |
| 12 | `SHORT` | 2026-07-01 04:36:59 UTC | 2026-07-01 04:37:14 UTC | 14.7s | `1.704` | `1.702` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0034 |
| 13 | `LONG` | 2026-07-01 04:57:59 UTC | 2026-07-01 05:06:16 UTC | 8m 16s | `1.703` | `1.705` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 14 | `SHORT` | 2026-07-01 05:22:59 UTC | 2026-07-01 05:26:59 UTC | 3m 59s | `1.701` | `1.699` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0042 |
| 15 | `LONG` | 2026-07-01 05:29:59 UTC | 2026-07-01 05:30:34 UTC | 34.1s | `1.707` | `1.702` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $100.0032 |
| 16 | `SHORT` | 2026-07-01 05:32:59 UTC | 2026-07-01 05:37:20 UTC | 4m 20s | `1.702` | `1.700` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 17 | `LONG` | 2026-07-01 05:45:59 UTC | 2026-07-01 05:48:36 UTC | 2m 36s | `1.706` | `1.708` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 18 | `SHORT` | 2026-07-01 06:03:59 UTC | 2026-07-01 06:05:28 UTC | 1m 28s | `1.705` | `1.710` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $100.0030 |
| 19 | `LONG` | 2026-07-01 06:14:59 UTC | 2026-07-01 06:18:13 UTC | 3m 13s | `1.711` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $100.0020 |
| 20 | `SHORT` | 2026-07-01 06:19:59 UTC | 2026-07-01 06:21:46 UTC | 1m 46s | `1.705` | `1.703` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 21 | `LONG` | 2026-07-01 06:54:59 UTC | 2026-07-01 07:03:03 UTC | 8m 03s | `1.692` | `1.687` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.2%` | `STOP_LOSS_HIT` | $100.0014 |
| 22 | `SHORT` | 2026-07-01 07:04:59 UTC | 2026-07-01 07:05:24 UTC | 24.2s | `1.688` | `1.686` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 23 | `LONG` | 2026-07-01 07:13:59 UTC | 2026-07-01 07:14:30 UTC | 30.2s | `1.687` | `1.689` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 24 | `LONG` | 2026-07-01 07:17:59 UTC | 2026-07-01 07:21:39 UTC | 3m 39s | `1.690` | `1.692` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $100.0026 |
| 25 | `SHORT` | 2026-07-01 07:41:59 UTC | 2026-07-01 07:44:13 UTC | 2m 13s | `1.695` | `1.693` | $0.34 | $0.00 | $0.000000 | **+0.0004** | `+8.8%` | `MIN_PROFIT_TP_HIT` | $100.0030 |
| ... | ... | *(976 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1002 | `SHORT` | 2026-07-13 14:44:59 UTC | 2026-07-13 14:56:40 UTC | 11m 40s | `1.556` | `1.561` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $100.0228 |
| 1003 | `SHORT` | 2026-07-13 15:17:59 UTC | 2026-07-13 15:21:49 UTC | 3m 49s | `1.564` | `1.562` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.6%` | `MIN_PROFIT_TP_HIT` | $100.0232 |
| 1004 | `SHORT` | 2026-07-13 15:26:59 UTC | 2026-07-13 15:28:50 UTC | 1m 50s | `1.560` | `1.558` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.6%` | `MIN_PROFIT_TP_HIT` | $100.0236 |
| 1005 | `LONG` | 2026-07-13 15:48:59 UTC | 2026-07-13 15:49:37 UTC | 37.1s | `1.555` | `1.557` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.6%` | `MIN_PROFIT_TP_HIT` | $100.0240 |
| 1006 | `SHORT` | 2026-07-13 15:59:59 UTC | 2026-07-13 16:19:09 UTC | 19m 09s | `1.555` | `1.553` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.6%` | `MIN_PROFIT_TP_HIT` | $100.0244 |
| 1007 | `LONG` | 2026-07-13 17:01:59 UTC | 2026-07-13 17:17:20 UTC | 15m 20s | `1.543` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $100.0234 |
| 1008 | `LONG` | 2026-07-13 18:07:59 UTC | 2026-07-13 18:10:08 UTC | 2m 08s | `1.525` | `1.520` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $100.0224 |
| 1009 | `SHORT` | 2026-07-13 18:11:59 UTC | 2026-07-13 18:13:44 UTC | 1m 44s | `1.518` | `1.523` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.7%` | `STOP_LOSS_HIT` | $100.0214 |
| 1010 | `LONG` | 2026-07-13 18:18:59 UTC | 2026-07-13 18:23:42 UTC | 4m 42s | `1.523` | `1.525` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0218 |
| 1011 | `LONG` | 2026-07-13 18:24:59 UTC | 2026-07-13 18:30:12 UTC | 5m 12s | `1.527` | `1.522` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $100.0208 |
| 1012 | `SHORT` | 2026-07-13 18:31:59 UTC | 2026-07-13 18:33:19 UTC | 1m 19s | `1.522` | `1.520` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.9%` | `MIN_PROFIT_TP_HIT` | $100.0212 |
| 1013 | `LONG` | 2026-07-13 18:42:59 UTC | 2026-07-13 18:43:59 UTC | 59.3s | `1.523` | `1.525` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0216 |
| 1014 | `SHORT` | 2026-07-13 18:57:59 UTC | 2026-07-13 19:04:56 UTC | 6m 56s | `1.522` | `1.527` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $100.0206 |
| 1015 | `LONG` | 2026-07-13 19:05:59 UTC | 2026-07-13 19:31:45 UTC | 25m 45s | `1.527` | `1.529` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0210 |
| 1016 | `SHORT` | 2026-07-13 20:10:59 UTC | 2026-07-13 20:15:09 UTC | 4m 09s | `1.535` | `1.533` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0214 |
| 1017 | `LONG` | 2026-07-13 20:26:59 UTC | 2026-07-13 20:27:28 UTC | 29.0s | `1.534` | `1.536` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0218 |
| 1018 | `SHORT` | 2026-07-13 20:44:59 UTC | 2026-07-13 20:59:02 UTC | 14m 02s | `1.531` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $100.0208 |
| 1019 | `SHORT` | 2026-07-13 21:06:59 UTC | 2026-07-13 21:09:23 UTC | 2m 23s | `1.533` | `1.531` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0212 |
| 1020 | `SHORT` | 2026-07-13 21:10:59 UTC | 2026-07-13 21:31:18 UTC | 20m 18s | `1.531` | `1.529` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0216 |
| 1021 | `LONG` | 2026-07-13 21:53:59 UTC | 2026-07-13 21:54:12 UTC | 12.4s | `1.524` | `1.526` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0220 |
| 1022 | `LONG` | 2026-07-13 21:58:59 UTC | 2026-07-13 21:59:04 UTC | 4.0s | `1.525` | `1.527` | $0.30 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0224 |
| 1023 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:03:16 UTC | 2m 16s | `1.527` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $100.0214 |
| 1024 | `SHORT` | 2026-07-13 22:35:59 UTC | 2026-07-13 22:39:19 UTC | 3m 19s | `1.534` | `1.532` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0218 |
| 1025 | `LONG` | 2026-07-13 22:43:59 UTC | 2026-07-13 23:04:45 UTC | 20m 45s | `1.535` | `1.530` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $100.0208 |
| 1026 | `LONG` | 2026-07-13 23:18:59 UTC | 2026-07-13 23:20:43 UTC | 1m 43s | `1.535` | `1.537` | $0.31 | $0.00 | $0.000000 | **+0.0004** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $100.0212 |

> 💡 *Full granular dataset with all 1026 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
