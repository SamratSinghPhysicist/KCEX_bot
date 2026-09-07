# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 01:32:36 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0368 USDT` | `₹9,448.48` | `+0.04%` |
| **Net Realized PnL** | **`+0.0368 USDT`** | **`₹+3.48`** | **`+0.04% Net ROI`** |
| **Gross Profit** | `+0.4120 USDT` | `₹38.91` | Total positive trade returns |
| **Gross Loss** | `-0.3752 USDT` | `₹35.44` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.10`** | — | Profitable |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0148 USDT` | `₹1.40` | **`-0.01%` Peak-to-Trough** |
| **Win Rate** | **`30.52%`** | — | `412 Wins / 938 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `3.29` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `5.30` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `2.49` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `DOGE_USDT` | Base Asset: `DOGE` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `EMA_CROSSOVER` | EMA Crossover Trend Follower (Preset: 5/13 ; Closed Candle Confirmation: True) |
| **Strategy Preset** | `5/13` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-07-01` → `2026-07-14` | Historical evaluation window |
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.00000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Trade Volume / Quantity** | `2 contract(s) (20 DOGE per trade)` | Quantity committed per trade signal |
| **Leverage Multiplier** | `75x` | Margin required = Position Notional / Leverage |
| **Starting Capital** | `100.00 USDT` | `₹9,445.00 INR` (`1 USDT = ₹94.45`) |
| **Take Profit Target** | `+5 ticks` (`+0.00005 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-2 ticks away from entry (0.00002 USDT)` | Stop loss evaluation logic |

### Exchange Contract Specifications & Fees
| Specification | Value | Notes |
| :--- | :--- | :--- |
| **Fee Schedule Mode** | `ZERO` | Live KCEX API, 0.0% zero-fee pair, or manual rate |
| **Maker Fee Rate** | `0.0000%` | Rate for passive limit orders |
| **Taker Fee Rate** | `0.0000%` | Rate for aggressive market / stop triggers |
| **Contract Size (cs)** | `10.0 DOGE` | 1 contract = 10.0 underlying coin |
| **Price Unit (pu / tick)** | `1e-05` | Minimum tick increment on order book |
| **Price Precision** | `5 decimal places` | Precision formatting for quotes and orders |
| **Min Volume** | `1.0 contract(s)` | Minimum permissible order size |
| **Max Leverage** | `100x` | Maximum allowed leverage on exchange |

---

## 📈 Trade Execution & Statistical Breakdown

| Metric | Value | Context / Benchmark |
| :--- | :--- | :--- |
| **Total Trades Executed** | `1350` | Total completed trade lifecycle events |
| **Winning Trades** | `412` | `30.52%` of total trades |
| **Losing Trades** | `938` | `69.48%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+5.2% ROE)` | Trade #17 (SHORT) |
| **Largest Losing Trade** | `-0.0004 USDT (-2.1% ROE)` | Trade #1 (LONG) |
| **Max Consecutive Wins** | `6` trades | Peak winning streak |
| **Max Consecutive Losses** | `15` trades | Peak losing streak |
| **Average Trade Duration** | `39.7s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #224 |
| **Longest Trade In-Position** | `11m 16s` | Trade #1293 |
| **Cumulative Time In Position** | `14h 54m 13s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `670` (49.6%) | `680` (50.4%) | `1350` |
| **Wins / Losses** | `196 W / 474 L` | `216 W / 464 L` | `412 W / 938 L` |
| **Win Rate** | **`29.25%`** | **`31.76%`** | **`30.52%`** |
| **Gross Profit** | `+0.1960 USDT` | `+0.2160 USDT` | `+0.4120 USDT` |
| **Gross Loss** | `-0.1896 USDT` | `-0.1856 USDT` | `-0.3752 USDT` |
| **Net Realized PnL** | **`+0.0064 USDT`** | **`+0.0304 USDT`** | **`+0.0368 USDT`** |
| **Net PnL (INR)** | `₹+0.60` | `₹+2.87` | `₹+3.48` |
| **Profit Factor** | `1.03` | `1.16` | `1.10` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `938` | `69.5%` | `-0.3752 USDT` | `₹-35.44` | `0.0%` | `28.6s` |
| `MIN_PROFIT_TP_HIT` | `412` | `30.5%` | `+0.4120 USDT` | `₹+38.91` | `100.0%` | `1m 05s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:32:59 UTC | 2026-07-01 00:33:11 UTC | 11.9s | `0.07198` | `0.07196` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-07-01 00:39:59 UTC | 2026-07-01 00:40:11 UTC | 11.0s | `0.07169` | `0.07171` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `LONG` | 2026-07-01 00:53:59 UTC | 2026-07-01 00:54:07 UTC | 7.8s | `0.07183` | `0.07181` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `SHORT` | 2026-07-01 01:03:59 UTC | 2026-07-01 01:04:15 UTC | 15.7s | `0.07170` | `0.07165` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $99.9998 |
| 5 | `LONG` | 2026-07-01 01:23:59 UTC | 2026-07-01 01:24:01 UTC | 1.7s | `0.07121` | `0.07119` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 6 | `SHORT` | 2026-07-01 01:26:59 UTC | 2026-07-01 01:27:19 UTC | 20.0s | `0.07124` | `0.07119` | $1.42 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 7 | `SHORT` | 2026-07-01 02:06:59 UTC | 2026-07-01 02:07:55 UTC | 55.4s | `0.07174` | `0.07176` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 8 | `LONG` | 2026-07-01 02:13:59 UTC | 2026-07-01 02:14:18 UTC | 18.3s | `0.07194` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 9 | `SHORT` | 2026-07-01 02:33:59 UTC | 2026-07-01 02:34:02 UTC | 2.5s | `0.07206` | `0.07208` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 10 | `LONG` | 2026-07-01 02:36:59 UTC | 2026-07-01 02:37:01 UTC | 1.9s | `0.07207` | `0.07205` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 11 | `SHORT` | 2026-07-01 02:38:59 UTC | 2026-07-01 02:39:13 UTC | 13.2s | `0.07213` | `0.07215` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9984 |
| 12 | `SHORT` | 2026-07-01 02:41:59 UTC | 2026-07-01 02:42:10 UTC | 10.8s | `0.07213` | `0.07215` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9980 |
| 13 | `SHORT` | 2026-07-01 02:48:59 UTC | 2026-07-01 02:49:11 UTC | 11.2s | `0.07190` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9976 |
| 14 | `LONG` | 2026-07-01 03:06:59 UTC | 2026-07-01 03:07:13 UTC | 13.9s | `0.07219` | `0.07224` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $99.9986 |
| 15 | `SHORT` | 2026-07-01 03:14:59 UTC | 2026-07-01 03:16:37 UTC | 1m 37s | `0.07200` | `0.07195` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 16 | `LONG` | 2026-07-01 03:30:59 UTC | 2026-07-01 03:31:01 UTC | 1.1s | `0.07199` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 17 | `SHORT` | 2026-07-01 03:33:59 UTC | 2026-07-01 03:34:12 UTC | 12.6s | `0.07198` | `0.07193` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 18 | `SHORT` | 2026-07-01 04:02:59 UTC | 2026-07-01 04:03:03 UTC | 3.1s | `0.07228` | `0.07230` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 19 | `LONG` | 2026-07-01 04:05:59 UTC | 2026-07-01 04:06:00 UTC | 0.7s | `0.07236` | `0.07234` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 20 | `SHORT` | 2026-07-01 04:35:59 UTC | 2026-07-01 04:36:55 UTC | 55.0s | `0.07234` | `0.07236` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9990 |
| 21 | `LONG` | 2026-07-01 04:42:59 UTC | 2026-07-01 04:43:08 UTC | 8.1s | `0.07251` | `0.07249` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9986 |
| 22 | `SHORT` | 2026-07-01 04:55:59 UTC | 2026-07-01 04:56:34 UTC | 34.8s | `0.07247` | `0.07249` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9982 |
| 23 | `LONG` | 2026-07-01 05:02:59 UTC | 2026-07-01 05:04:46 UTC | 1m 46s | `0.07249` | `0.07247` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9978 |
| 24 | `LONG` | 2026-07-01 05:06:59 UTC | 2026-07-01 05:09:21 UTC | 2m 21s | `0.07248` | `0.07246` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9974 |
| 25 | `LONG` | 2026-07-01 05:41:59 UTC | 2026-07-01 05:42:29 UTC | 29.7s | `0.07236` | `0.07234` | $1.45 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9970 |
| ... | ... | *(1300 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1326 | `SHORT` | 2026-07-13 16:52:59 UTC | 2026-07-13 16:54:11 UTC | 1m 11s | `0.07169` | `0.07164` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0352 |
| 1327 | `LONG` | 2026-07-13 17:08:59 UTC | 2026-07-13 17:09:03 UTC | 3.5s | `0.07169` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0348 |
| 1328 | `SHORT` | 2026-07-13 17:18:59 UTC | 2026-07-13 17:20:49 UTC | 1m 49s | `0.07164` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0344 |
| 1329 | `LONG` | 2026-07-13 17:22:59 UTC | 2026-07-13 17:23:12 UTC | 12.6s | `0.07172` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0340 |
| 1330 | `SHORT` | 2026-07-13 17:26:59 UTC | 2026-07-13 17:30:16 UTC | 3m 16s | `0.07169` | `0.07164` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0350 |
| 1331 | `SHORT` | 2026-07-13 17:32:59 UTC | 2026-07-13 17:33:02 UTC | 2.4s | `0.07160` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0346 |
| 1332 | `LONG` | 2026-07-13 18:08:59 UTC | 2026-07-13 18:09:00 UTC | 0.5s | `0.07119` | `0.07117` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0342 |
| 1333 | `SHORT` | 2026-07-13 18:10:59 UTC | 2026-07-13 18:12:34 UTC | 1m 34s | `0.07099` | `0.07094` | $1.42 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0352 |
| 1334 | `LONG` | 2026-07-13 18:25:59 UTC | 2026-07-13 18:26:06 UTC | 6.7s | `0.07120` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0348 |
| 1335 | `SHORT` | 2026-07-13 18:35:59 UTC | 2026-07-13 18:36:07 UTC | 7.8s | `0.07111` | `0.07113` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0344 |
| 1336 | `LONG` | 2026-07-13 18:37:59 UTC | 2026-07-13 18:38:11 UTC | 11.5s | `0.07115` | `0.07120` | $1.42 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0354 |
| 1337 | `SHORT` | 2026-07-13 19:28:59 UTC | 2026-07-13 19:29:04 UTC | 4.9s | `0.07140` | `0.07135` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0364 |
| 1338 | `LONG` | 2026-07-13 19:33:59 UTC | 2026-07-13 19:34:29 UTC | 29.1s | `0.07149` | `0.07154` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0374 |
| 1339 | `SHORT` | 2026-07-13 20:11:59 UTC | 2026-07-13 20:12:19 UTC | 19.5s | `0.07177` | `0.07179` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0370 |
| 1340 | `LONG` | 2026-07-13 20:25:59 UTC | 2026-07-13 20:26:00 UTC | 0.3s | `0.07187` | `0.07185` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0366 |
| 1341 | `SHORT` | 2026-07-13 20:37:59 UTC | 2026-07-13 20:40:33 UTC | 2m 33s | `0.07181` | `0.07176` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0376 |
| 1342 | `SHORT` | 2026-07-13 20:41:59 UTC | 2026-07-13 20:42:26 UTC | 27.0s | `0.07175` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0372 |
| 1343 | `LONG` | 2026-07-13 20:59:59 UTC | 2026-07-13 21:00:12 UTC | 12.6s | `0.07174` | `0.07172` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0368 |
| 1344 | `SHORT` | 2026-07-13 21:10:59 UTC | 2026-07-13 21:11:00 UTC | 0.6s | `0.07158` | `0.07160` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0364 |
| 1345 | `LONG` | 2026-07-13 21:22:59 UTC | 2026-07-13 21:24:18 UTC | 1m 18s | `0.07166` | `0.07164` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0360 |
| 1346 | `SHORT` | 2026-07-13 21:27:59 UTC | 2026-07-13 21:28:00 UTC | 0.6s | `0.07138` | `0.07140` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0356 |
| 1347 | `LONG` | 2026-07-13 21:53:59 UTC | 2026-07-13 21:56:09 UTC | 2m 09s | `0.07138` | `0.07143` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0366 |
| 1348 | `SHORT` | 2026-07-13 22:29:59 UTC | 2026-07-13 22:30:22 UTC | 22.9s | `0.07167` | `0.07169` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0362 |
| 1349 | `LONG` | 2026-07-13 22:48:59 UTC | 2026-07-13 22:49:20 UTC | 20.9s | `0.07156` | `0.07154` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0358 |
| 1350 | `LONG` | 2026-07-13 23:12:59 UTC | 2026-07-13 23:13:39 UTC | 39.7s | `0.07136` | `0.07141` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0368 |

> 💡 *Full granular dataset with all 1350 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
