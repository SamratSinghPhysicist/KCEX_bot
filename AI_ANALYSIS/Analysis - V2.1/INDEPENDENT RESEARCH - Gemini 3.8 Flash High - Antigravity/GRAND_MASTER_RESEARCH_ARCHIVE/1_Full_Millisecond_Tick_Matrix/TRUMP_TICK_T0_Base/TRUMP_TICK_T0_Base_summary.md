# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 14:01:17 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `101.2896 USDT` | `₹9,566.80` | `+1.29%` |
| **Net Realized PnL** | **`+1.2896 USDT`** | **`₹+121.80`** | **`+1.29% Net ROI`** |
| **Gross Profit** | `+11.6140 USDT` | `₹1,096.94` | Total positive trade returns |
| **Gross Loss** | `-10.3244 USDT` | `₹975.14` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.12`** | — | Profitable |
| **Win / Loss Payoff** | `0.20` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.1028 USDT` | `₹9.71` | **`-0.10%` Peak-to-Trough** |
| **Win Rate** | **`84.77%`** | — | `29035 Wins / 5215 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `3.41` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `1.47` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `12.55` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `TRUMP_USDT` | Base Asset: `TRUMP` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-01-01` → `2026-08-31` | Historical evaluation window |
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
| **Stop Loss Rule** | `-25.0% ROE on committed margin` | Stop loss evaluation logic |

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
| **Total Trades Executed** | `34250` | Total completed trade lifecycle events |
| **Winning Trades** | `29035` | `84.77%` of total trades |
| **Losing Trades** | `5215` | `15.23%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0020 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.1% ROE)` | Trade #7 (LONG) |
| **Largest Losing Trade** | `-0.0020 USDT (-15.9% ROE)` | Trade #22 (LONG) |
| **Max Consecutive Wins** | `55` trades | Peak winning streak |
| **Max Consecutive Losses** | `7` trades | Peak losing streak |
| **Average Trade Duration** | `3m 58s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #21 |
| **Longest Trade In-Position** | `3h 55m 27s` | Trade #32063 |
| **Cumulative Time In Position** | `2265h 29m 18s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `17187` (50.2%) | `17063` (49.8%) | `34250` |
| **Wins / Losses** | `14496 W / 2691 L` | `14539 W / 2524 L` | `29035 W / 5215 L` |
| **Win Rate** | **`84.34%`** | **`85.21%`** | **`84.77%`** |
| **Gross Profit** | `+5.7984 USDT` | `+5.8156 USDT` | `+11.6140 USDT` |
| **Gross Loss** | `-5.3264 USDT` | `-4.9980 USDT` | `-10.3244 USDT` |
| **Net Realized PnL** | **`+0.4720 USDT`** | **`+0.8176 USDT`** | **`+1.2896 USDT`** |
| **Net PnL (INR)** | `₹+44.58` | `₹+77.22` | `₹+121.80` |
| **Profit Factor** | `1.09` | `1.16` | `1.12` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `29035` | `84.8%` | `+11.6140 USDT` | `₹+1,096.94` | `100.0%` | `2m 57s` |
| `STOP_LOSS_HIT` | `5215` | `15.2%` | `-10.3244 USDT` | `₹-975.14` | `0.0%` | `9m 38s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:27:59 UTC | 2026-01-01 00:34:00 UTC | 6m 00s | `4.806` | `4.804` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `LONG` | 2026-01-01 00:36:59 UTC | 2026-01-01 00:38:32 UTC | 1m 32s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `LONG` | 2026-01-01 00:43:59 UTC | 2026-01-01 00:49:02 UTC | 5m 02s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 01:04:12 UTC | 9m 12s | `4.808` | `4.818` | $0.96 | $0.01 | $0.000000 | **-0.0020** | `-15.6%` | `STOP_LOSS_HIT` | $99.9992 |
| 5 | `SHORT` | 2026-01-01 01:11:59 UTC | 2026-01-01 01:12:02 UTC | 2.2s | `4.822` | `4.820` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 6 | `LONG` | 2026-01-01 01:17:59 UTC | 2026-01-01 01:26:09 UTC | 8m 09s | `4.816` | `4.806` | $0.96 | $0.01 | $0.000000 | **-0.0020** | `-15.6%` | `STOP_LOSS_HIT` | $99.9976 |
| 7 | `LONG` | 2026-01-01 01:30:59 UTC | 2026-01-01 01:31:06 UTC | 6.2s | `4.805` | `4.807` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| 8 | `SHORT` | 2026-01-01 01:34:59 UTC | 2026-01-01 01:38:04 UTC | 3m 04s | `4.805` | `4.803` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9984 |
| 9 | `SHORT` | 2026-01-01 01:46:59 UTC | 2026-01-01 02:00:20 UTC | 13m 20s | `4.807` | `4.805` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9988 |
| 10 | `LONG` | 2026-01-01 02:01:59 UTC | 2026-01-01 02:02:05 UTC | 5.3s | `4.800` | `4.802` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 11 | `LONG` | 2026-01-01 02:03:59 UTC | 2026-01-01 02:10:46 UTC | 6m 46s | `4.799` | `4.801` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 12 | `SHORT` | 2026-01-01 02:13:59 UTC | 2026-01-01 02:15:39 UTC | 1m 39s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 13 | `SHORT` | 2026-01-01 02:21:59 UTC | 2026-01-01 02:25:43 UTC | 3m 43s | `4.796` | `4.794` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 14 | `LONG` | 2026-01-01 02:31:59 UTC | 2026-01-01 02:32:27 UTC | 27.9s | `4.793` | `4.795` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 15 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:37:19 UTC | 1m 19s | `4.794` | `4.792` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 16 | `LONG` | 2026-01-01 02:44:59 UTC | 2026-01-01 02:45:50 UTC | 51.0s | `4.782` | `4.784` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 17 | `SHORT` | 2026-01-01 02:54:59 UTC | 2026-01-01 02:57:44 UTC | 2m 44s | `4.783` | `4.781` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 18 | `SHORT` | 2026-01-01 02:58:59 UTC | 2026-01-01 03:00:03 UTC | 1m 03s | `4.784` | `4.782` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 19 | `SHORT` | 2026-01-01 03:01:59 UTC | 2026-01-01 03:02:02 UTC | 2.2s | `4.716` | `4.726` | $0.94 | $0.01 | $0.000000 | **-0.0020** | `-15.9%` | `STOP_LOSS_HIT` | $100.0004 |
| 20 | `SHORT` | 2026-01-01 03:13:59 UTC | 2026-01-01 03:43:56 UTC | 29m 56s | `4.733` | `4.731` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 21 | `LONG` | 2026-01-01 03:44:59 UTC | 2026-01-01 03:45:00 UTC | 0.1s | `4.733` | `4.735` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 22 | `LONG` | 2026-01-01 04:00:59 UTC | 2026-01-01 04:05:06 UTC | 4m 06s | `4.722` | `4.712` | $0.94 | $0.01 | $0.000000 | **-0.0020** | `-15.9%` | `STOP_LOSS_HIT` | $99.9992 |
| 23 | `LONG` | 2026-01-01 04:10:59 UTC | 2026-01-01 04:13:54 UTC | 2m 54s | `4.711` | `4.713` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 24 | `SHORT` | 2026-01-01 04:17:59 UTC | 2026-01-01 04:18:46 UTC | 46.1s | `4.715` | `4.713` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 25 | `LONG` | 2026-01-01 04:27:59 UTC | 2026-01-01 04:28:52 UTC | 52.6s | `4.714` | `4.716` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| ... | ... | *(34200 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 34226 | `SHORT` | 2026-08-30 20:40:59 UTC | 2026-08-30 20:42:10 UTC | 1m 10s | `2.514` | `2.512` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2872 |
| 34227 | `LONG` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:47:10 UTC | 10.1s | `2.518` | `2.520` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2876 |
| 34228 | `SHORT` | 2026-08-30 20:50:59 UTC | 2026-08-30 20:52:17 UTC | 1m 17s | `2.525` | `2.523` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.2880 |
| 34229 | `SHORT` | 2026-08-30 20:54:59 UTC | 2026-08-30 20:56:30 UTC | 1m 30s | `2.525` | `2.523` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $101.2884 |
| 34230 | `LONG` | 2026-08-30 21:03:59 UTC | 2026-08-30 21:04:03 UTC | 3.9s | `2.500` | `2.502` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2888 |
| 34231 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:07 UTC | 7.4s | `2.503` | `2.501` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2892 |
| 34232 | `SHORT` | 2026-08-30 21:32:59 UTC | 2026-08-30 21:33:09 UTC | 9.9s | `2.509` | `2.507` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2896 |
| 34233 | `SHORT` | 2026-08-30 21:35:59 UTC | 2026-08-30 21:37:12 UTC | 1m 12s | `2.510` | `2.508` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2900 |
| 34234 | `LONG` | 2026-08-30 21:50:59 UTC | 2026-08-30 21:51:00 UTC | 0.5s | `2.488` | `2.490` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2904 |
| 34235 | `SHORT` | 2026-08-30 21:58:59 UTC | 2026-08-30 22:00:04 UTC | 1m 04s | `2.506` | `2.504` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2908 |
| 34236 | `LONG` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:03 UTC | 3.7s | `2.516` | `2.518` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $101.2912 |
| 34237 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:22:25 UTC | 2m 25s | `2.501` | `2.491` | $0.50 | $0.01 | $0.000000 | **-0.0020** | `-30.0%` | `STOP_LOSS_HIT` | $101.2892 |
| 34238 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:04 UTC | 4.8s | `2.429` | `2.427` | $0.49 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2896 |
| 34239 | `LONG` | 2026-08-30 22:51:59 UTC | 2026-08-30 22:52:04 UTC | 4.7s | `2.416` | `2.418` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2900 |
| 34240 | `SHORT` | 2026-08-30 22:56:59 UTC | 2026-08-30 22:59:02 UTC | 2m 02s | `2.424` | `2.422` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2904 |
| 34241 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:42 UTC | 42.1s | `2.409` | `2.419` | $0.48 | $0.01 | $0.000000 | **-0.0020** | `-31.1%` | `STOP_LOSS_HIT` | $101.2884 |
| 34242 | `SHORT` | 2026-08-30 23:10:59 UTC | 2026-08-30 23:11:42 UTC | 42.8s | `2.405` | `2.415` | $0.48 | $0.01 | $0.000000 | **-0.0020** | `-31.2%` | `STOP_LOSS_HIT` | $101.2864 |
| 34243 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:00 UTC | 0.8s | `2.422` | `2.420` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2868 |
| 34244 | `SHORT` | 2026-08-30 23:18:59 UTC | 2026-08-30 23:19:00 UTC | 0.6s | `2.415` | `2.413` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2872 |
| 34245 | `SHORT` | 2026-08-30 23:24:59 UTC | 2026-08-30 23:25:00 UTC | 0.6s | `2.414` | `2.412` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $101.2876 |
| 34246 | `LONG` | 2026-08-30 23:32:59 UTC | 2026-08-30 23:33:01 UTC | 1.6s | `2.388` | `2.390` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $101.2880 |
| 34247 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:19 UTC | 19.7s | `2.330` | `2.332` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $101.2884 |
| 34248 | `SHORT` | 2026-08-30 23:53:59 UTC | 2026-08-30 23:54:11 UTC | 11.8s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $101.2888 |
| 34249 | `SHORT` | 2026-08-30 23:57:59 UTC | 2026-08-30 23:58:00 UTC | 0.5s | `2.343` | `2.341` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $101.2892 |
| 34250 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:02 UTC | 2.0s | `2.338` | `2.336` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $101.2896 |

> 💡 *Full granular dataset with all 34250 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
