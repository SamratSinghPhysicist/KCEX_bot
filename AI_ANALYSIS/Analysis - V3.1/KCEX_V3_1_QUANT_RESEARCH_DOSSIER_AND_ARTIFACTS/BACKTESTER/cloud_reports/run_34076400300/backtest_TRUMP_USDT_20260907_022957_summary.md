# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 02:29:57 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.6656 USDT` | `₹9,413.42` | `-0.33%` |
| **Net Realized PnL** | **`-0.3344 USDT`** | **`₹-31.58`** | **`-0.33% Net ROI`** |
| **Gross Profit** | `+0.2736 USDT` | `₹25.84` | Total positive trade returns |
| **Gross Loss** | `-0.6080 USDT` | `₹57.43` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.45`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.60` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.3382 USDT` | `₹31.94` | **`-0.34%` Peak-to-Trough** |
| **Win Rate** | **`21.95%`** | — | `171 Wins / 608 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-31.00` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-33.39` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.99` | — | Net ROI divided by Max Drawdown |

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
| **Slippage Tolerance** | `1 ticks` (`0.001 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Take Profit Target** | `+8 ticks` (`+0.008 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-4 ticks away from entry (0.004 USDT)` | Stop loss evaluation logic |

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
| **Total Trades Executed** | `779` | Total completed trade lifecycle events |
| **Winning Trades** | `171` | `21.95%` of total trades |
| **Losing Trades** | `608` | `78.05%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0016 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0010 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0016 USDT (+35.2% ROE)` | Trade #5 (LONG) |
| **Largest Losing Trade** | `-0.0010 USDT (-22.6% ROE)` | Trade #3 (LONG) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `17` trades | Peak losing streak |
| **Average Trade Duration** | `12m 02s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #64 |
| **Longest Trade In-Position** | `3h 24m 33s` | Trade #755 |
| **Cumulative Time In Position** | `156h 24m 24s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `395` (50.7%) | `384` (49.3%) | `779` |
| **Wins / Losses** | `83 W / 312 L` | `88 W / 296 L` | `171 W / 608 L` |
| **Win Rate** | **`21.01%`** | **`22.92%`** | **`21.95%`** |
| **Gross Profit** | `+0.1328 USDT` | `+0.1408 USDT` | `+0.2736 USDT` |
| **Gross Loss** | `-0.3120 USDT` | `-0.2960 USDT` | `-0.6080 USDT` |
| **Net Realized PnL** | **`-0.1792 USDT`** | **`-0.1552 USDT`** | **`-0.3344 USDT`** |
| **Net PnL (INR)** | `₹-16.93` | `₹-14.66` | `₹-31.58` |
| **Profit Factor** | `0.43` | `0.48` | `0.45` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `608` | `78.0%` | `-0.6080 USDT` | `₹-57.43` | `0.0%` | `9m 44s` |
| `MIN_PROFIT_TP_HIT` | `171` | `22.0%` | `+0.2736 USDT` | `₹+25.84` | `100.0%` | `20m 15s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-07-01 00:24:59 UTC | 2026-07-01 00:29:47 UTC | 4m 47s | `1.659` | `1.664` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9990 |
| 2 | `LONG` | 2026-07-01 00:30:59 UTC | 2026-07-01 01:05:16 UTC | 34m 16s | `1.666` | `1.661` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.5%` | `STOP_LOSS_HIT` | $99.9980 |
| 3 | `LONG` | 2026-07-01 01:23:59 UTC | 2026-07-01 01:24:49 UTC | 49.9s | `1.657` | `1.652` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9970 |
| 4 | `SHORT` | 2026-07-01 02:37:59 UTC | 2026-07-01 02:38:14 UTC | 14.0s | `1.695` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9960 |
| 5 | `LONG` | 2026-07-01 02:58:59 UTC | 2026-07-01 03:01:39 UTC | 2m 39s | `1.703` | `1.711` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.2%` | `MIN_PROFIT_TP_HIT` | $99.9976 |
| 6 | `SHORT` | 2026-07-01 03:16:59 UTC | 2026-07-01 03:37:08 UTC | 20m 08s | `1.703` | `1.708` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9966 |
| 7 | `LONG` | 2026-07-01 03:38:59 UTC | 2026-07-01 03:52:16 UTC | 13m 16s | `1.705` | `1.713` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.2%` | `MIN_PROFIT_TP_HIT` | $99.9982 |
| 8 | `SHORT` | 2026-07-01 04:00:59 UTC | 2026-07-01 04:01:40 UTC | 40.6s | `1.706` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9972 |
| 9 | `LONG` | 2026-07-01 04:20:59 UTC | 2026-07-01 04:35:07 UTC | 14m 07s | `1.705` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9962 |
| 10 | `SHORT` | 2026-07-01 04:36:59 UTC | 2026-07-01 05:12:42 UTC | 35m 42s | `1.703` | `1.708` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9952 |
| 11 | `SHORT` | 2026-07-01 05:22:59 UTC | 2026-07-01 05:27:08 UTC | 4m 08s | `1.700` | `1.705` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9942 |
| 12 | `LONG` | 2026-07-01 05:29:59 UTC | 2026-07-01 05:30:33 UTC | 33.0s | `1.708` | `1.703` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9932 |
| 13 | `SHORT` | 2026-07-01 05:32:59 UTC | 2026-07-01 05:44:37 UTC | 11m 37s | `1.701` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9922 |
| 14 | `LONG` | 2026-07-01 05:45:59 UTC | 2026-07-01 05:46:19 UTC | 19.8s | `1.707` | `1.702` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9912 |
| 15 | `SHORT` | 2026-07-01 06:03:59 UTC | 2026-07-01 06:05:27 UTC | 1m 27s | `1.704` | `1.709` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9902 |
| 16 | `LONG` | 2026-07-01 06:14:59 UTC | 2026-07-01 06:17:04 UTC | 2m 04s | `1.712` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9892 |
| 17 | `SHORT` | 2026-07-01 06:19:59 UTC | 2026-07-01 06:34:32 UTC | 14m 32s | `1.704` | `1.696` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.2%` | `MIN_PROFIT_TP_HIT` | $99.9908 |
| 18 | `LONG` | 2026-07-01 06:54:59 UTC | 2026-07-01 06:56:34 UTC | 1m 34s | `1.693` | `1.688` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.2%` | `STOP_LOSS_HIT` | $99.9898 |
| 19 | `SHORT` | 2026-07-01 06:57:59 UTC | 2026-07-01 07:22:01 UTC | 24m 01s | `1.690` | `1.695` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.2%` | `STOP_LOSS_HIT` | $99.9888 |
| 20 | `SHORT` | 2026-07-01 07:41:59 UTC | 2026-07-01 07:50:06 UTC | 8m 06s | `1.694` | `1.699` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9878 |
| 21 | `SHORT` | 2026-07-01 08:02:59 UTC | 2026-07-01 08:10:05 UTC | 7m 05s | `1.693` | `1.698` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.2%` | `STOP_LOSS_HIT` | $99.9868 |
| 22 | `LONG` | 2026-07-01 08:11:59 UTC | 2026-07-01 08:17:04 UTC | 5m 04s | `1.697` | `1.692` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9858 |
| 23 | `SHORT` | 2026-07-01 08:18:59 UTC | 2026-07-01 08:33:37 UTC | 14m 37s | `1.693` | `1.685` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.4%` | `MIN_PROFIT_TP_HIT` | $99.9874 |
| 24 | `LONG` | 2026-07-01 08:43:59 UTC | 2026-07-01 08:46:34 UTC | 2m 34s | `1.694` | `1.689` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9864 |
| 25 | `SHORT` | 2026-07-01 08:48:59 UTC | 2026-07-01 08:51:47 UTC | 2m 47s | `1.685` | `1.690` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.3%` | `STOP_LOSS_HIT` | $99.9854 |
| ... | ... | *(729 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 755 | `SHORT` | 2026-07-13 09:10:59 UTC | 2026-07-13 12:35:33 UTC | 3h 24m 33s | `1.552` | `1.544` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+38.7%` | `MIN_PROFIT_TP_HIT` | $99.6740 |
| 756 | `LONG` | 2026-07-13 12:49:59 UTC | 2026-07-13 12:53:22 UTC | 3m 22s | `1.550` | `1.545` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.2%` | `STOP_LOSS_HIT` | $99.6730 |
| 757 | `SHORT` | 2026-07-13 12:55:59 UTC | 2026-07-13 13:05:40 UTC | 9m 40s | `1.544` | `1.549` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $99.6720 |
| 758 | `LONG` | 2026-07-13 13:06:59 UTC | 2026-07-13 13:09:35 UTC | 2m 35s | `1.551` | `1.546` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.2%` | `STOP_LOSS_HIT` | $99.6710 |
| 759 | `SHORT` | 2026-07-13 13:12:59 UTC | 2026-07-13 13:34:55 UTC | 21m 55s | `1.545` | `1.550` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $99.6700 |
| 760 | `SHORT` | 2026-07-13 13:41:59 UTC | 2026-07-13 13:46:37 UTC | 4m 37s | `1.537` | `1.542` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.6690 |
| 761 | `LONG` | 2026-07-13 13:59:59 UTC | 2026-07-13 14:10:22 UTC | 10m 22s | `1.543` | `1.551` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+38.9%` | `MIN_PROFIT_TP_HIT` | $99.6706 |
| 762 | `SHORT` | 2026-07-13 14:44:59 UTC | 2026-07-13 14:46:49 UTC | 1m 49s | `1.555` | `1.560` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $99.6696 |
| 763 | `SHORT` | 2026-07-13 15:17:59 UTC | 2026-07-13 15:31:35 UTC | 13m 35s | `1.563` | `1.555` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+38.4%` | `MIN_PROFIT_TP_HIT` | $99.6712 |
| 764 | `LONG` | 2026-07-13 15:48:59 UTC | 2026-07-13 16:19:21 UTC | 30m 21s | `1.556` | `1.551` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $99.6702 |
| 765 | `LONG` | 2026-07-13 17:01:59 UTC | 2026-07-13 17:04:47 UTC | 2m 47s | `1.544` | `1.539` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $99.6692 |
| 766 | `SHORT` | 2026-07-13 17:06:59 UTC | 2026-07-13 17:09:54 UTC | 2m 54s | `1.540` | `1.545` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.6682 |
| 767 | `SHORT` | 2026-07-13 17:16:59 UTC | 2026-07-13 17:36:51 UTC | 19m 51s | `1.538` | `1.530` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.0%` | `MIN_PROFIT_TP_HIT` | $99.6698 |
| 768 | `LONG` | 2026-07-13 18:07:59 UTC | 2026-07-13 18:10:04 UTC | 2m 04s | `1.526` | `1.521` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.6688 |
| 769 | `SHORT` | 2026-07-13 18:11:59 UTC | 2026-07-13 18:13:39 UTC | 1m 39s | `1.517` | `1.522` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.7%` | `STOP_LOSS_HIT` | $99.6678 |
| 770 | `LONG` | 2026-07-13 18:18:59 UTC | 2026-07-13 18:19:14 UTC | 14.8s | `1.524` | `1.519` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.6668 |
| 771 | `SHORT` | 2026-07-13 18:20:59 UTC | 2026-07-13 18:23:42 UTC | 2m 42s | `1.521` | `1.526` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.7%` | `STOP_LOSS_HIT` | $99.6658 |
| 772 | `LONG` | 2026-07-13 18:24:59 UTC | 2026-07-13 18:27:34 UTC | 2m 34s | `1.528` | `1.523` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.6648 |
| 773 | `SHORT` | 2026-07-13 18:31:59 UTC | 2026-07-13 18:43:59 UTC | 11m 59s | `1.521` | `1.526` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.7%` | `STOP_LOSS_HIT` | $99.6638 |
| 774 | `SHORT` | 2026-07-13 18:57:59 UTC | 2026-07-13 19:01:46 UTC | 3m 46s | `1.521` | `1.526` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.7%` | `STOP_LOSS_HIT` | $99.6628 |
| 775 | `LONG` | 2026-07-13 19:05:59 UTC | 2026-07-13 19:18:25 UTC | 12m 25s | `1.528` | `1.523` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.6618 |
| 776 | `LONG` | 2026-07-13 19:28:59 UTC | 2026-07-13 19:35:11 UTC | 6m 11s | `1.526` | `1.534` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.3%` | `MIN_PROFIT_TP_HIT` | $99.6634 |
| 777 | `SHORT` | 2026-07-13 20:10:59 UTC | 2026-07-13 21:38:10 UTC | 1h 27m 10s | `1.534` | `1.526` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.1%` | `MIN_PROFIT_TP_HIT` | $99.6650 |
| 778 | `LONG` | 2026-07-13 21:53:59 UTC | 2026-07-13 22:03:33 UTC | 9m 33s | `1.525` | `1.533` | $0.30 | $0.00 | $0.000000 | **+0.0016** | `+39.3%` | `MIN_PROFIT_TP_HIT` | $99.6666 |
| 779 | `SHORT` | 2026-07-13 22:35:59 UTC | 2026-07-13 23:20:43 UTC | 44m 43s | `1.533` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.6656 |

> 💡 *Full granular dataset with all 779 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
