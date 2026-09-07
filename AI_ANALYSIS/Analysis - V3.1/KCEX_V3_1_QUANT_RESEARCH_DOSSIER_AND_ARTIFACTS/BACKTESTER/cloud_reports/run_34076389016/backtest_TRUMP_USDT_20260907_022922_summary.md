# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 02:29:22 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.5854 USDT` | `₹9,405.84` | `-0.41%` |
| **Net Realized PnL** | **`-0.4146 USDT`** | **`₹-39.16`** | **`-0.41% Net ROI`** |
| **Gross Profit** | `+0.3824 USDT` | `₹36.12` | Total positive trade returns |
| **Gross Loss** | `-0.7970 USDT` | `₹75.28` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.48`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.60` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.4184 USDT` | `₹39.52` | **`-0.42%` Peak-to-Trough** |
| **Win Rate** | **`23.07%`** | — | `239 Wins / 797 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-28.41` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-31.13` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.99` | — | Net ROI divided by Max Drawdown |

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
| **Slippage Tolerance** | `1 ticks` (`0.001 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Total Trades Executed** | `1036` | Total completed trade lifecycle events |
| **Winning Trades** | `239` | `23.07%` of total trades |
| **Losing Trades** | `797` | `76.93%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0016 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0010 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0016 USDT (+36.1% ROE)` | Trade #1 (LONG) |
| **Largest Losing Trade** | `-0.0010 USDT (-22.0% ROE)` | Trade #14 (LONG) |
| **Max Consecutive Wins** | `4` trades | Peak winning streak |
| **Max Consecutive Losses** | `20` trades | Peak losing streak |
| **Average Trade Duration** | `11m 55s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #709 |
| **Longest Trade In-Position** | `2h 37m 33s` | Trade #1005 |
| **Cumulative Time In Position** | `205h 57m 29s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `521` (50.3%) | `515` (49.7%) | `1036` |
| **Wins / Losses** | `115 W / 406 L` | `124 W / 391 L` | `239 W / 797 L` |
| **Win Rate** | **`22.07%`** | **`24.08%`** | **`23.07%`** |
| **Gross Profit** | `+0.1840 USDT` | `+0.1984 USDT` | `+0.3824 USDT` |
| **Gross Loss** | `-0.4060 USDT` | `-0.3910 USDT` | `-0.7970 USDT` |
| **Net Realized PnL** | **`-0.2220 USDT`** | **`-0.1926 USDT`** | **`-0.4146 USDT`** |
| **Net PnL (INR)** | `₹-20.97` | `₹-18.19` | `₹-39.16` |
| **Profit Factor** | `0.45` | `0.51` | `0.48` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `239` | `23.1%` | `+0.3824 USDT` | `₹+36.12` | `100.0%` | `18m 59s` |
| `STOP_LOSS_HIT` | `797` | `76.9%` | `-0.7970 USDT` | `₹-75.28` | `0.0%` | `9m 48s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:34:39 UTC | 5m 39s | `1.662` | `1.670` | $0.33 | $0.00 | $0.000000 | **+0.0016** | `+36.1%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 2 | `SHORT` | 2026-07-01 00:36:59 UTC | 2026-07-01 00:46:07 UTC | 9m 07s | `1.663` | `1.668` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.5%` | `STOP_LOSS_HIT` | $100.0006 |
| 3 | `SHORT` | 2026-07-01 00:55:59 UTC | 2026-07-01 01:09:27 UTC | 13m 27s | `1.668` | `1.660` | $0.33 | $0.00 | $0.000000 | **+0.0016** | `+36.0%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 4 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:21:18 UTC | 6m 18s | `1.646` | `1.654` | $0.33 | $0.00 | $0.000000 | **+0.0016** | `+36.5%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 5 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:30:33 UTC | 7m 33s | `1.657` | `1.662` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $100.0028 |
| 6 | `SHORT` | 2026-07-01 01:34:59 UTC | 2026-07-01 01:35:33 UTC | 33.8s | `1.657` | `1.662` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $100.0018 |
| 7 | `SHORT` | 2026-07-01 01:47:59 UTC | 2026-07-01 01:53:55 UTC | 5m 55s | `1.675` | `1.680` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.4%` | `STOP_LOSS_HIT` | $100.0008 |
| 8 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 02:01:16 UTC | 2m 16s | `1.677` | `1.682` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.4%` | `STOP_LOSS_HIT` | $99.9998 |
| 9 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:36 UTC | 36.0s | `1.686` | `1.681` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.2%` | `STOP_LOSS_HIT` | $99.9988 |
| 10 | `LONG` | 2026-07-01 02:08:59 UTC | 2026-07-01 02:11:33 UTC | 2m 33s | `1.685` | `1.693` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.6%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 11 | `SHORT` | 2026-07-01 02:17:59 UTC | 2026-07-01 02:18:17 UTC | 17.5s | `1.701` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9994 |
| 12 | `LONG` | 2026-07-01 02:22:59 UTC | 2026-07-01 02:23:00 UTC | 0.9s | `1.710` | `1.705` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9984 |
| 13 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:33:05 UTC | 3m 05s | `1.706` | `1.701` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9974 |
| 14 | `LONG` | 2026-07-01 02:34:59 UTC | 2026-07-01 02:36:55 UTC | 1m 55s | `1.705` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9964 |
| 15 | `LONG` | 2026-07-01 02:40:59 UTC | 2026-07-01 02:52:26 UTC | 11m 26s | `1.698` | `1.693` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9954 |
| 16 | `SHORT` | 2026-07-01 03:00:59 UTC | 2026-07-01 03:01:33 UTC | 33.3s | `1.703` | `1.708` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9944 |
| 17 | `SHORT` | 2026-07-01 03:04:59 UTC | 2026-07-01 03:05:07 UTC | 7.4s | `1.706` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9934 |
| 18 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:11:13 UTC | 1m 13s | `1.728` | `1.720` | $0.35 | $0.00 | $0.000000 | **+0.0016** | `+34.7%` | `MIN_PROFIT_TP_HIT` | $99.9950 |
| 19 | `LONG` | 2026-07-01 03:15:59 UTC | 2026-07-01 03:16:00 UTC | 0.7s | `1.712` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9940 |
| 20 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:11 UTC | 11.2s | `1.705` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9930 |
| 21 | `LONG` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:32:27 UTC | 4m 27s | `1.700` | `1.695` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9920 |
| 22 | `SHORT` | 2026-07-01 03:41:59 UTC | 2026-07-01 03:46:24 UTC | 4m 24s | `1.705` | `1.710` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9910 |
| 23 | `LONG` | 2026-07-01 03:51:59 UTC | 2026-07-01 03:57:15 UTC | 5m 15s | `1.712` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9900 |
| 24 | `LONG` | 2026-07-01 04:02:59 UTC | 2026-07-01 04:08:03 UTC | 5m 03s | `1.706` | `1.701` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9890 |
| 25 | `LONG` | 2026-07-01 04:11:59 UTC | 2026-07-01 04:12:49 UTC | 49.3s | `1.701` | `1.696` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9880 |
| ... | ... | *(986 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1012 | `SHORT` | 2026-07-13 14:29:59 UTC | 2026-07-13 14:38:48 UTC | 8m 48s | `1.555` | `1.560` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $99.5990 |
| 1013 | `LONG` | 2026-07-13 14:39:59 UTC | 2026-07-13 14:41:40 UTC | 1m 40s | `1.560` | `1.555` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.0%` | `STOP_LOSS_HIT` | $99.5980 |
| 1014 | `LONG` | 2026-07-13 14:46:59 UTC | 2026-07-13 15:31:35 UTC | 44m 35s | `1.559` | `1.554` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $99.5970 |
| 1015 | `LONG` | 2026-07-13 15:37:59 UTC | 2026-07-13 16:26:15 UTC | 48m 15s | `1.553` | `1.548` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.1%` | `STOP_LOSS_HIT` | $99.5960 |
| 1016 | `SHORT` | 2026-07-13 16:32:59 UTC | 2026-07-13 16:35:31 UTC | 2m 31s | `1.549` | `1.541` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+38.7%` | `MIN_PROFIT_TP_HIT` | $99.5976 |
| 1017 | `LONG` | 2026-07-13 16:40:59 UTC | 2026-07-13 16:52:01 UTC | 11m 01s | `1.542` | `1.537` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $99.5966 |
| 1018 | `LONG` | 2026-07-13 16:54:59 UTC | 2026-07-13 17:21:33 UTC | 26m 33s | `1.539` | `1.534` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5956 |
| 1019 | `LONG` | 2026-07-13 17:22:59 UTC | 2026-07-13 17:25:09 UTC | 2m 09s | `1.537` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5946 |
| 1020 | `LONG` | 2026-07-13 17:27:59 UTC | 2026-07-13 17:30:13 UTC | 2m 13s | `1.537` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5936 |
| 1021 | `SHORT` | 2026-07-13 17:31:59 UTC | 2026-07-13 17:36:53 UTC | 4m 53s | `1.533` | `1.525` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.1%` | `MIN_PROFIT_TP_HIT` | $99.5952 |
| 1022 | `SHORT` | 2026-07-13 17:45:59 UTC | 2026-07-13 17:57:54 UTC | 11m 54s | `1.532` | `1.524` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.2%` | `MIN_PROFIT_TP_HIT` | $99.5968 |
| 1023 | `LONG` | 2026-07-13 18:01:59 UTC | 2026-07-13 18:11:08 UTC | 9m 08s | `1.522` | `1.517` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.5958 |
| 1024 | `LONG` | 2026-07-13 18:14:59 UTC | 2026-07-13 18:19:44 UTC | 4m 44s | `1.523` | `1.518` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.5948 |
| 1025 | `SHORT` | 2026-07-13 18:27:59 UTC | 2026-07-13 18:48:02 UTC | 20m 02s | `1.523` | `1.528` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.5938 |
| 1026 | `SHORT` | 2026-07-13 18:53:59 UTC | 2026-07-13 19:33:16 UTC | 39m 16s | `1.527` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.5928 |
| 1027 | `SHORT` | 2026-07-13 19:36:59 UTC | 2026-07-13 19:44:10 UTC | 7m 10s | `1.531` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.5918 |
| 1028 | `SHORT` | 2026-07-13 19:47:59 UTC | 2026-07-13 19:50:00 UTC | 2m 00s | `1.533` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.5908 |
| 1029 | `LONG` | 2026-07-13 19:51:59 UTC | 2026-07-13 20:15:09 UTC | 23m 09s | `1.537` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5898 |
| 1030 | `LONG` | 2026-07-13 20:22:59 UTC | 2026-07-13 21:31:18 UTC | 1h 08m 18s | `1.533` | `1.528` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.5888 |
| 1031 | `LONG` | 2026-07-13 21:33:59 UTC | 2026-07-13 21:38:06 UTC | 4m 06s | `1.531` | `1.526` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.5878 |
| 1032 | `LONG` | 2026-07-13 21:43:59 UTC | 2026-07-13 22:03:16 UTC | 19m 16s | `1.524` | `1.532` | $0.30 | $0.00 | $0.000000 | **+0.0016** | `+39.4%` | `MIN_PROFIT_TP_HIT` | $99.5894 |
| 1033 | `SHORT` | 2026-07-13 22:05:59 UTC | 2026-07-13 22:16:27 UTC | 10m 27s | `1.531` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.5884 |
| 1034 | `SHORT` | 2026-07-13 22:20:59 UTC | 2026-07-13 23:35:17 UTC | 1h 14m 17s | `1.535` | `1.540` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5874 |
| 1035 | `SHORT` | 2026-07-13 23:43:59 UTC | 2026-07-13 23:47:28 UTC | 3m 28s | `1.538` | `1.543` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.5864 |
| 1036 | `SHORT` | 2026-07-13 23:56:59 UTC | 2026-07-14 00:01:08 UTC | 4m 08s | `1.542` | `1.547` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.3%` | `STOP_LOSS_HIT` | $99.5854 |

> 💡 *Full granular dataset with all 1036 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
