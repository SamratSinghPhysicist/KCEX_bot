# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 02:30:01 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.4714 USDT` | `₹9,395.07` | `-0.53%` |
| **Net Realized PnL** | **`-0.5286 USDT`** | **`₹-49.93`** | **`-0.53% Net ROI`** |
| **Gross Profit** | `+0.1908 USDT` | `₹18.02` | Total positive trade returns |
| **Gross Loss** | `-0.7194 USDT` | `₹67.95` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.27`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `2.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.5286 USDT` | `₹49.93` | **`-0.53%` Peak-to-Trough** |
| **Win Rate** | **`11.71%`** | — | `159 Wins / 1199 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-52.29` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-50.45` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-1.00` | — | Net ROI divided by Max Drawdown |

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
| **Slippage Tolerance** | `1 ticks` (`0.00001 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Take Profit Target** | `+6 ticks` (`+0.00006 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
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
| **Total Trades Executed** | `1358` | Total completed trade lifecycle events |
| **Winning Trades** | `159` | `11.71%` of total trades |
| **Losing Trades** | `1199` | `88.29%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0012 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0006 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0012 USDT (+6.3% ROE)` | Trade #29 (SHORT) |
| **Largest Losing Trade** | `-0.0006 USDT (-3.1% ROE)` | Trade #1 (LONG) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `49` trades | Peak losing streak |
| **Average Trade Duration** | `23.7s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #44 |
| **Longest Trade In-Position** | `10m 11s` | Trade #1116 |
| **Cumulative Time In Position** | `8h 55m 56s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `673` (49.6%) | `685` (50.4%) | `1358` |
| **Wins / Losses** | `75 W / 598 L` | `84 W / 601 L` | `159 W / 1199 L` |
| **Win Rate** | **`11.14%`** | **`12.26%`** | **`11.71%`** |
| **Gross Profit** | `+0.0900 USDT` | `+0.1008 USDT` | `+0.1908 USDT` |
| **Gross Loss** | `-0.3588 USDT` | `-0.3606 USDT` | `-0.7194 USDT` |
| **Net Realized PnL** | **`-0.2688 USDT`** | **`-0.2598 USDT`** | **`-0.5286 USDT`** |
| **Net PnL (INR)** | `₹-25.39` | `₹-24.54` | `₹-49.93` |
| **Profit Factor** | `0.25` | `0.28` | `0.27` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `1199` | `88.3%` | `-0.7194 USDT` | `₹-67.95` | `0.0%` | `15.8s` |
| `MIN_PROFIT_TP_HIT` | `159` | `11.7%` | `+0.1908 USDT` | `₹+18.02` | `100.0%` | `1m 23s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:32:59 UTC | 2026-07-01 00:33:00 UTC | 0.3s | `0.07199` | `0.07196` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 2 | `SHORT` | 2026-07-01 00:39:59 UTC | 2026-07-01 00:40:00 UTC | 0.2s | `0.07168` | `0.07171` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 3 | `LONG` | 2026-07-01 00:53:59 UTC | 2026-07-01 00:54:00 UTC | 0.1s | `0.07184` | `0.07181` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9982 |
| 4 | `SHORT` | 2026-07-01 01:03:59 UTC | 2026-07-01 01:04:00 UTC | 0.8s | `0.07169` | `0.07172` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9976 |
| 5 | `LONG` | 2026-07-01 01:23:59 UTC | 2026-07-01 01:24:01 UTC | 1.2s | `0.07122` | `0.07119` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9970 |
| 6 | `SHORT` | 2026-07-01 01:26:59 UTC | 2026-07-01 01:27:48 UTC | 48.4s | `0.07123` | `0.07126` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9964 |
| 7 | `SHORT` | 2026-07-01 02:06:59 UTC | 2026-07-01 02:07:02 UTC | 2.1s | `0.07173` | `0.07176` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9958 |
| 8 | `LONG` | 2026-07-01 02:13:59 UTC | 2026-07-01 02:14:18 UTC | 18.3s | `0.07195` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9952 |
| 9 | `SHORT` | 2026-07-01 02:33:59 UTC | 2026-07-01 02:34:01 UTC | 1.3s | `0.07205` | `0.07208` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9946 |
| 10 | `LONG` | 2026-07-01 02:36:59 UTC | 2026-07-01 02:37:01 UTC | 1.8s | `0.07208` | `0.07205` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9940 |
| 11 | `SHORT` | 2026-07-01 02:38:59 UTC | 2026-07-01 02:39:13 UTC | 13.2s | `0.07212` | `0.07215` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9934 |
| 12 | `SHORT` | 2026-07-01 02:41:59 UTC | 2026-07-01 02:42:10 UTC | 10.8s | `0.07212` | `0.07215` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9928 |
| 13 | `SHORT` | 2026-07-01 02:48:59 UTC | 2026-07-01 02:49:01 UTC | 1.9s | `0.07189` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9922 |
| 14 | `LONG` | 2026-07-01 03:06:59 UTC | 2026-07-01 03:07:16 UTC | 16.2s | `0.07220` | `0.07217` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9916 |
| 15 | `SHORT` | 2026-07-01 03:14:59 UTC | 2026-07-01 03:15:00 UTC | 1.0s | `0.07199` | `0.07202` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9910 |
| 16 | `LONG` | 2026-07-01 03:30:59 UTC | 2026-07-01 03:31:00 UTC | 0.7s | `0.07200` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9904 |
| 17 | `SHORT` | 2026-07-01 03:33:59 UTC | 2026-07-01 03:34:04 UTC | 4.9s | `0.07197` | `0.07200` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9898 |
| 18 | `SHORT` | 2026-07-01 04:02:59 UTC | 2026-07-01 04:03:00 UTC | 0.3s | `0.07227` | `0.07230` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9892 |
| 19 | `LONG` | 2026-07-01 04:05:59 UTC | 2026-07-01 04:06:00 UTC | 0.7s | `0.07237` | `0.07234` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9886 |
| 20 | `SHORT` | 2026-07-01 04:35:59 UTC | 2026-07-01 04:36:02 UTC | 2.7s | `0.07233` | `0.07236` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9880 |
| 21 | `LONG` | 2026-07-01 04:42:59 UTC | 2026-07-01 04:43:03 UTC | 3.8s | `0.07252` | `0.07249` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9874 |
| 22 | `SHORT` | 2026-07-01 04:55:59 UTC | 2026-07-01 04:56:23 UTC | 23.7s | `0.07246` | `0.07249` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9868 |
| 23 | `LONG` | 2026-07-01 05:02:59 UTC | 2026-07-01 05:03:02 UTC | 2.4s | `0.07250` | `0.07247` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9862 |
| 24 | `SHORT` | 2026-07-01 05:04:59 UTC | 2026-07-01 05:05:07 UTC | 7.2s | `0.07248` | `0.07251` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9856 |
| 25 | `LONG` | 2026-07-01 05:06:59 UTC | 2026-07-01 05:07:03 UTC | 3.4s | `0.07249` | `0.07246` | $1.45 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9850 |
| ... | ... | *(1308 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1334 | `LONG` | 2026-07-13 16:43:59 UTC | 2026-07-13 16:44:00 UTC | 0.6s | `0.07180` | `0.07177` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4786 |
| 1335 | `SHORT` | 2026-07-13 16:52:59 UTC | 2026-07-13 16:53:43 UTC | 43.8s | `0.07168` | `0.07171` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4780 |
| 1336 | `LONG` | 2026-07-13 17:08:59 UTC | 2026-07-13 17:09:03 UTC | 3.4s | `0.07170` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4774 |
| 1337 | `SHORT` | 2026-07-13 17:18:59 UTC | 2026-07-13 17:19:32 UTC | 32.2s | `0.07163` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4768 |
| 1338 | `LONG` | 2026-07-13 17:22:59 UTC | 2026-07-13 17:23:00 UTC | 0.7s | `0.07173` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4762 |
| 1339 | `SHORT` | 2026-07-13 17:26:59 UTC | 2026-07-13 17:31:38 UTC | 4m 38s | `0.07168` | `0.07162` | $1.43 | $0.02 | $0.000000 | **+0.0012** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $99.4774 |
| 1340 | `SHORT` | 2026-07-13 17:32:59 UTC | 2026-07-13 17:33:02 UTC | 2.2s | `0.07159` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4768 |
| 1341 | `LONG` | 2026-07-13 18:08:59 UTC | 2026-07-13 18:09:00 UTC | 0.4s | `0.07120` | `0.07117` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4762 |
| 1342 | `SHORT` | 2026-07-13 18:10:59 UTC | 2026-07-13 18:13:26 UTC | 2m 26s | `0.07098` | `0.07101` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4756 |
| 1343 | `LONG` | 2026-07-13 18:25:59 UTC | 2026-07-13 18:26:01 UTC | 1.5s | `0.07121` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4750 |
| 1344 | `SHORT` | 2026-07-13 18:35:59 UTC | 2026-07-13 18:36:00 UTC | 0.4s | `0.07110` | `0.07113` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4744 |
| 1345 | `LONG` | 2026-07-13 18:37:59 UTC | 2026-07-13 18:39:24 UTC | 1m 24s | `0.07116` | `0.07113` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4738 |
| 1346 | `SHORT` | 2026-07-13 19:28:59 UTC | 2026-07-13 19:29:28 UTC | 29.0s | `0.07139` | `0.07133` | $1.43 | $0.02 | $0.000000 | **+0.0012** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $99.4750 |
| 1347 | `LONG` | 2026-07-13 19:33:59 UTC | 2026-07-13 19:36:09 UTC | 2m 09s | `0.07150` | `0.07156` | $1.43 | $0.02 | $0.000000 | **+0.0012** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $99.4762 |
| 1348 | `SHORT` | 2026-07-13 20:11:59 UTC | 2026-07-13 20:12:00 UTC | 0.4s | `0.07176` | `0.07179` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4756 |
| 1349 | `LONG` | 2026-07-13 20:25:59 UTC | 2026-07-13 20:26:00 UTC | 0.3s | `0.07188` | `0.07185` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4750 |
| 1350 | `SHORT` | 2026-07-13 20:37:59 UTC | 2026-07-13 20:44:05 UTC | 6m 05s | `0.07180` | `0.07174` | $1.44 | $0.02 | $0.000000 | **+0.0012** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $99.4762 |
| 1351 | `LONG` | 2026-07-13 20:59:59 UTC | 2026-07-13 21:00:12 UTC | 12.5s | `0.07175` | `0.07172` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4756 |
| 1352 | `SHORT` | 2026-07-13 21:10:59 UTC | 2026-07-13 21:11:00 UTC | 0.6s | `0.07157` | `0.07160` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4750 |
| 1353 | `LONG` | 2026-07-13 21:22:59 UTC | 2026-07-13 21:23:01 UTC | 1.1s | `0.07167` | `0.07164` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4744 |
| 1354 | `SHORT` | 2026-07-13 21:27:59 UTC | 2026-07-13 21:28:00 UTC | 0.5s | `0.07137` | `0.07140` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4738 |
| 1355 | `LONG` | 2026-07-13 21:53:59 UTC | 2026-07-13 21:54:00 UTC | 0.3s | `0.07139` | `0.07136` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4732 |
| 1356 | `SHORT` | 2026-07-13 22:29:59 UTC | 2026-07-13 22:30:22 UTC | 22.6s | `0.07166` | `0.07169` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4726 |
| 1357 | `LONG` | 2026-07-13 22:48:59 UTC | 2026-07-13 22:49:08 UTC | 8.6s | `0.07157` | `0.07154` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.4720 |
| 1358 | `LONG` | 2026-07-13 23:12:59 UTC | 2026-07-13 23:13:08 UTC | 8.3s | `0.07137` | `0.07134` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.4714 |

> 💡 *Full granular dataset with all 1358 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
