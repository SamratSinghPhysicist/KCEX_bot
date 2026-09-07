# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 02:30:25 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.0176 USDT` | `₹9,352.21` | `-0.98%` |
| **Net Realized PnL** | **`-0.9824 USDT`** | **`₹-92.79`** | **`-0.98% Net ROI`** |
| **Gross Profit** | `+0.2992 USDT` | `₹28.26` | Total positive trade returns |
| **Gross Loss** | `-1.2816 USDT` | `₹121.05` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.23`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.33` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.9848 USDT` | `₹93.01` | **`-0.98%` Peak-to-Trough** |
| **Win Rate** | **`14.90%`** | — | `187 Wins / 1068 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-61.05` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-50.74` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-1.00` | — | Net ROI divided by Max Drawdown |

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
| **Slippage Tolerance** | `2 ticks` (`0.002 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Total Trades Executed** | `1255` | Total completed trade lifecycle events |
| **Winning Trades** | `187` | `14.90%` of total trades |
| **Losing Trades** | `1068` | `85.10%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0008 USDT` (`₹-0.07`) | Expected return per signal |
| **Average Winning Trade** | `+0.0016 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0012 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0016 USDT (+35.8% ROE)` | Trade #6 (LONG) |
| **Largest Losing Trade** | `-0.0012 USDT (-27.1% ROE)` | Trade #1 (LONG) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `27` trades | Peak losing streak |
| **Average Trade Duration** | `8m 39s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #830 |
| **Longest Trade In-Position** | `3h 23m 07s` | Trade #1075 |
| **Cumulative Time In Position** | `181h 02m 22s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `632` (50.4%) | `623` (49.6%) | `1255` |
| **Wins / Losses** | `86 W / 546 L` | `101 W / 522 L` | `187 W / 1068 L` |
| **Win Rate** | **`13.61%`** | **`16.21%`** | **`14.90%`** |
| **Gross Profit** | `+0.1376 USDT` | `+0.1616 USDT` | `+0.2992 USDT` |
| **Gross Loss** | `-0.6552 USDT` | `-0.6264 USDT` | `-1.2816 USDT` |
| **Net Realized PnL** | **`-0.5176 USDT`** | **`-0.4648 USDT`** | **`-0.9824 USDT`** |
| **Net PnL (INR)** | `₹-48.89` | `₹-43.90` | `₹-92.79` |
| **Profit Factor** | `0.21` | `0.26` | `0.23` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `1068` | `85.1%` | `-1.2816 USDT` | `₹-121.05` | `0.0%` | `6m 22s` |
| `MIN_PROFIT_TP_HIT` | `187` | `14.9%` | `+0.2992 USDT` | `₹+28.26` | `100.0%` | `21m 38s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 01:10:35 UTC | 41m 35s | `1.663` | `1.657` | $0.33 | $0.00 | $0.000000 | **-0.0012** | `-27.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 2 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:16:49 UTC | 1m 49s | `1.647` | `1.641` | $0.33 | $0.00 | $0.000000 | **-0.0012** | `-27.3%` | `STOP_LOSS_HIT` | $99.9976 |
| 3 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:30:33 UTC | 7m 33s | `1.656` | `1.662` | $0.33 | $0.00 | $0.000000 | **-0.0012** | `-27.2%` | `STOP_LOSS_HIT` | $99.9964 |
| 4 | `SHORT` | 2026-07-01 01:34:59 UTC | 2026-07-01 01:35:12 UTC | 12.7s | `1.656` | `1.662` | $0.33 | $0.00 | $0.000000 | **-0.0012** | `-27.2%` | `STOP_LOSS_HIT` | $99.9952 |
| 5 | `SHORT` | 2026-07-01 01:47:59 UTC | 2026-07-01 01:48:18 UTC | 18.9s | `1.674` | `1.680` | $0.33 | $0.00 | $0.000000 | **-0.0012** | `-26.9%` | `STOP_LOSS_HIT` | $99.9940 |
| 6 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 02:03:45 UTC | 10m 45s | `1.678` | `1.686` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.8%` | `MIN_PROFIT_TP_HIT` | $99.9956 |
| 7 | `LONG` | 2026-07-01 02:08:59 UTC | 2026-07-01 02:11:41 UTC | 2m 41s | `1.686` | `1.694` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.6%` | `MIN_PROFIT_TP_HIT` | $99.9972 |
| 8 | `SHORT` | 2026-07-01 02:17:59 UTC | 2026-07-01 02:18:16 UTC | 17.0s | `1.700` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.5%` | `STOP_LOSS_HIT` | $99.9960 |
| 9 | `LONG` | 2026-07-01 02:22:59 UTC | 2026-07-01 02:23:00 UTC | 0.9s | `1.711` | `1.705` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.3%` | `STOP_LOSS_HIT` | $99.9948 |
| 10 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:33:01 UTC | 3m 01s | `1.707` | `1.701` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9936 |
| 11 | `LONG` | 2026-07-01 02:34:59 UTC | 2026-07-01 02:36:13 UTC | 1m 13s | `1.706` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9924 |
| 12 | `LONG` | 2026-07-01 02:40:59 UTC | 2026-07-01 02:42:33 UTC | 1m 33s | `1.699` | `1.693` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.5%` | `STOP_LOSS_HIT` | $99.9912 |
| 13 | `LONG` | 2026-07-01 02:44:59 UTC | 2026-07-01 02:45:29 UTC | 29.3s | `1.702` | `1.696` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9900 |
| 14 | `SHORT` | 2026-07-01 03:00:59 UTC | 2026-07-01 03:01:24 UTC | 24.7s | `1.702` | `1.708` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9888 |
| 15 | `SHORT` | 2026-07-01 03:04:59 UTC | 2026-07-01 03:05:05 UTC | 5.9s | `1.705` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9876 |
| 16 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:11:13 UTC | 1m 13s | `1.727` | `1.719` | $0.35 | $0.00 | $0.000000 | **+0.0016** | `+34.7%` | `MIN_PROFIT_TP_HIT` | $99.9892 |
| 17 | `LONG` | 2026-07-01 03:15:59 UTC | 2026-07-01 03:16:00 UTC | 0.7s | `1.713` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.3%` | `STOP_LOSS_HIT` | $99.9880 |
| 18 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:09 UTC | 9.5s | `1.706` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9868 |
| 19 | `LONG` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:32:00 UTC | 4m 00s | `1.701` | `1.695` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.5%` | `STOP_LOSS_HIT` | $99.9856 |
| 20 | `SHORT` | 2026-07-01 03:41:59 UTC | 2026-07-01 03:43:50 UTC | 1m 50s | `1.704` | `1.710` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9844 |
| 21 | `SHORT` | 2026-07-01 03:46:59 UTC | 2026-07-01 03:47:31 UTC | 31.0s | `1.708` | `1.714` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.3%` | `STOP_LOSS_HIT` | $99.9832 |
| 22 | `LONG` | 2026-07-01 03:51:59 UTC | 2026-07-01 03:57:03 UTC | 5m 03s | `1.713` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.3%` | `STOP_LOSS_HIT` | $99.9820 |
| 23 | `LONG` | 2026-07-01 04:02:59 UTC | 2026-07-01 04:03:10 UTC | 10.3s | `1.707` | `1.701` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9808 |
| 24 | `LONG` | 2026-07-01 04:11:59 UTC | 2026-07-01 04:12:10 UTC | 10.2s | `1.702` | `1.696` | $0.34 | $0.00 | $0.000000 | **-0.0012** | `-26.4%` | `STOP_LOSS_HIT` | $99.9796 |
| 25 | `LONG` | 2026-07-01 04:14:59 UTC | 2026-07-01 04:31:23 UTC | 16m 23s | `1.700` | `1.708` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.3%` | `MIN_PROFIT_TP_HIT` | $99.9812 |
| ... | ... | *(1205 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1231 | `LONG` | 2026-07-13 16:40:59 UTC | 2026-07-13 16:50:43 UTC | 9m 43s | `1.543` | `1.537` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.2%` | `STOP_LOSS_HIT` | $99.0296 |
| 1232 | `LONG` | 2026-07-13 16:54:59 UTC | 2026-07-13 16:55:14 UTC | 14.9s | `1.540` | `1.534` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.2%` | `STOP_LOSS_HIT` | $99.0284 |
| 1233 | `SHORT` | 2026-07-13 17:03:59 UTC | 2026-07-13 17:09:54 UTC | 5m 54s | `1.540` | `1.546` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.2%` | `STOP_LOSS_HIT` | $99.0272 |
| 1234 | `SHORT` | 2026-07-13 17:12:59 UTC | 2026-07-13 17:25:09 UTC | 12m 09s | `1.541` | `1.533` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+38.9%` | `MIN_PROFIT_TP_HIT` | $99.0288 |
| 1235 | `LONG` | 2026-07-13 17:27:59 UTC | 2026-07-13 17:28:43 UTC | 43.6s | `1.538` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0276 |
| 1236 | `SHORT` | 2026-07-13 17:31:59 UTC | 2026-07-13 17:36:53 UTC | 4m 53s | `1.532` | `1.524` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.2%` | `MIN_PROFIT_TP_HIT` | $99.0292 |
| 1237 | `SHORT` | 2026-07-13 17:45:59 UTC | 2026-07-13 17:57:54 UTC | 11m 54s | `1.531` | `1.523` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.2%` | `MIN_PROFIT_TP_HIT` | $99.0308 |
| 1238 | `LONG` | 2026-07-13 18:01:59 UTC | 2026-07-13 18:11:07 UTC | 9m 07s | `1.523` | `1.517` | $0.30 | $0.00 | $0.000000 | **-0.0012** | `-29.5%` | `STOP_LOSS_HIT` | $99.0296 |
| 1239 | `LONG` | 2026-07-13 18:14:59 UTC | 2026-07-13 18:19:14 UTC | 4m 14s | `1.524` | `1.518` | $0.30 | $0.00 | $0.000000 | **-0.0012** | `-29.5%` | `STOP_LOSS_HIT` | $99.0284 |
| 1240 | `SHORT` | 2026-07-13 18:27:59 UTC | 2026-07-13 18:28:19 UTC | 19.7s | `1.522` | `1.528` | $0.30 | $0.00 | $0.000000 | **-0.0012** | `-29.6%` | `STOP_LOSS_HIT` | $99.0272 |
| 1241 | `LONG` | 2026-07-13 18:36:59 UTC | 2026-07-13 18:37:08 UTC | 8.5s | `1.525` | `1.519` | $0.30 | $0.00 | $0.000000 | **-0.0012** | `-29.5%` | `STOP_LOSS_HIT` | $99.0260 |
| 1242 | `SHORT` | 2026-07-13 18:46:59 UTC | 2026-07-13 18:48:15 UTC | 1m 15s | `1.524` | `1.530` | $0.30 | $0.00 | $0.000000 | **-0.0012** | `-29.5%` | `STOP_LOSS_HIT` | $99.0248 |
| 1243 | `SHORT` | 2026-07-13 18:53:59 UTC | 2026-07-13 19:32:21 UTC | 38m 21s | `1.526` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.5%` | `STOP_LOSS_HIT` | $99.0236 |
| 1244 | `SHORT` | 2026-07-13 19:36:59 UTC | 2026-07-13 19:43:00 UTC | 6m 00s | `1.530` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.4%` | `STOP_LOSS_HIT` | $99.0224 |
| 1245 | `SHORT` | 2026-07-13 19:47:59 UTC | 2026-07-13 19:50:00 UTC | 2m 00s | `1.532` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.4%` | `STOP_LOSS_HIT` | $99.0212 |
| 1246 | `LONG` | 2026-07-13 19:51:59 UTC | 2026-07-13 20:10:09 UTC | 18m 09s | `1.538` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0200 |
| 1247 | `LONG` | 2026-07-13 20:14:59 UTC | 2026-07-13 20:15:09 UTC | 9.1s | `1.537` | `1.531` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0188 |
| 1248 | `LONG` | 2026-07-13 20:22:59 UTC | 2026-07-13 20:45:12 UTC | 22m 12s | `1.534` | `1.528` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0176 |
| 1249 | `LONG` | 2026-07-13 20:47:59 UTC | 2026-07-13 20:50:15 UTC | 2m 15s | `1.534` | `1.528` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0164 |
| 1250 | `SHORT` | 2026-07-13 20:57:59 UTC | 2026-07-13 20:59:02 UTC | 1m 02s | `1.532` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.4%` | `STOP_LOSS_HIT` | $99.0152 |
| 1251 | `SHORT` | 2026-07-13 21:01:59 UTC | 2026-07-13 21:38:10 UTC | 36m 10s | `1.531` | `1.523` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.2%` | `MIN_PROFIT_TP_HIT` | $99.0168 |
| 1252 | `LONG` | 2026-07-13 21:43:59 UTC | 2026-07-13 22:03:33 UTC | 19m 33s | `1.525` | `1.533` | $0.30 | $0.00 | $0.000000 | **+0.0016** | `+39.3%` | `MIN_PROFIT_TP_HIT` | $99.0184 |
| 1253 | `SHORT` | 2026-07-13 22:05:59 UTC | 2026-07-13 22:16:02 UTC | 10m 02s | `1.530` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.4%` | `STOP_LOSS_HIT` | $99.0172 |
| 1254 | `SHORT` | 2026-07-13 22:20:59 UTC | 2026-07-13 23:27:21 UTC | 1h 06m 21s | `1.534` | `1.540` | $0.31 | $0.00 | $0.000000 | **-0.0012** | `-29.3%` | `STOP_LOSS_HIT` | $99.0160 |
| 1255 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-14 00:10:36 UTC | 36m 36s | `1.539` | `1.547` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.0%` | `MIN_PROFIT_TP_HIT` | $99.0176 |

> 💡 *Full granular dataset with all 1255 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
