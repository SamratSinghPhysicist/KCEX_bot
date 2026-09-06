# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 14:13:26 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `98.9174 USDT` | `₹9,342.75` | `-1.08%` |
| **Net Realized PnL** | **`-1.0826 USDT`** | **`₹-102.25`** | **`-1.08% Net ROI`** |
| **Gross Profit** | `+10.7490 USDT` | `₹1,015.24` | Total positive trade returns |
| **Gross Loss** | `-11.8316 USDT` | `₹1,117.49` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.91`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-1.1852 USDT` | `₹111.94` | **`-1.18%` Peak-to-Trough** |
| **Win Rate** | **`26.65%`** | — | `10749 Wins / 29579 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-3.38` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-5.23` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.91` | — | Net ROI divided by Max Drawdown |

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
| **Signal Inversion Mode** | `ENABLED (Fading: Long<->Short)` | Signal execution orientation |

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
| **Take Profit Target** | `+5 ticks` (`+0.005 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
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
| **Total Trades Executed** | `40328` | Total completed trade lifecycle events |
| **Winning Trades** | `10749` | `26.65%` of total trades |
| **Losing Trades** | `29579` | `73.35%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0000 USDT` (`₹-0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+7.8% ROE)` | Trade #3 (SHORT) |
| **Largest Losing Trade** | `-0.0004 USDT (-3.1% ROE)` | Trade #9 (SHORT) |
| **Max Consecutive Wins** | `7` trades | Peak winning streak |
| **Max Consecutive Losses** | `34` trades | Peak losing streak |
| **Average Trade Duration** | `2m 18s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #27 |
| **Longest Trade In-Position** | `1h 56m 40s` | Trade #36715 |
| **Cumulative Time In Position** | `1553h 13m 42s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `20136` (49.9%) | `20192` (50.1%) | `40328` |
| **Wins / Losses** | `5288 W / 14848 L` | `5461 W / 14731 L` | `10749 W / 29579 L` |
| **Win Rate** | **`26.26%`** | **`27.05%`** | **`26.65%`** |
| **Gross Profit** | `+5.2880 USDT` | `+5.4610 USDT` | `+10.7490 USDT` |
| **Gross Loss** | `-5.9392 USDT` | `-5.8924 USDT` | `-11.8316 USDT` |
| **Net Realized PnL** | **`-0.6512 USDT`** | **`-0.4314 USDT`** | **`-1.0826 USDT`** |
| **Net PnL (INR)** | `₹-61.51` | `₹-40.75` | `₹-102.25` |
| **Profit Factor** | `0.89` | `0.93` | `0.91` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `29579` | `73.3%` | `-11.8316 USDT` | `₹-1,117.49` | `0.0%` | `1m 51s` |
| `MIN_PROFIT_TP_HIT` | `10749` | `26.7%` | `+10.7490 USDT` | `₹+1,015.24` | `100.0%` | `3m 32s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:27:59 UTC | 2026-01-01 00:34:00 UTC | 6m 00s | `4.806` | `4.804` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:36:59 UTC | 2026-01-01 00:38:32 UTC | 1m 32s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:43:59 UTC | 2026-01-01 00:46:04 UTC | 2m 04s | `4.807` | `4.802` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:19 UTC | 20.0s | `4.809` | `4.811` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 5 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 01:01:07 UTC | 6m 07s | `4.808` | `4.813` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 6 | `LONG` | 2026-01-01 01:03:59 UTC | 2026-01-01 01:11:56 UTC | 7m 56s | `4.816` | `4.821` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 7 | `SHORT` | 2026-01-01 01:17:59 UTC | 2026-01-01 01:18:15 UTC | 15.6s | `4.816` | `4.811` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 8 | `SHORT` | 2026-01-01 01:25:59 UTC | 2026-01-01 01:26:25 UTC | 25.3s | `4.809` | `4.804` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 9 | `SHORT` | 2026-01-01 01:30:59 UTC | 2026-01-01 01:31:06 UTC | 6.2s | `4.805` | `4.807` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0034 |
| 10 | `LONG` | 2026-01-01 01:34:59 UTC | 2026-01-01 01:38:04 UTC | 3m 04s | `4.805` | `4.803` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0030 |
| 11 | `LONG` | 2026-01-01 01:46:59 UTC | 2026-01-01 02:00:20 UTC | 13m 20s | `4.807` | `4.805` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0026 |
| 12 | `SHORT` | 2026-01-01 02:01:59 UTC | 2026-01-01 02:02:05 UTC | 5.3s | `4.800` | `4.802` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0022 |
| 13 | `SHORT` | 2026-01-01 02:03:59 UTC | 2026-01-01 02:10:46 UTC | 6m 46s | `4.799` | `4.801` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0018 |
| 14 | `LONG` | 2026-01-01 02:13:59 UTC | 2026-01-01 02:15:39 UTC | 1m 39s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0014 |
| 15 | `LONG` | 2026-01-01 02:21:59 UTC | 2026-01-01 02:25:43 UTC | 3m 43s | `4.796` | `4.794` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0010 |
| 16 | `SHORT` | 2026-01-01 02:31:59 UTC | 2026-01-01 02:32:27 UTC | 27.9s | `4.793` | `4.795` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0006 |
| 17 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:37:19 UTC | 1m 19s | `4.794` | `4.792` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0002 |
| 18 | `SHORT` | 2026-01-01 02:44:59 UTC | 2026-01-01 02:45:50 UTC | 51.0s | `4.782` | `4.784` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 19 | `LONG` | 2026-01-01 02:54:59 UTC | 2026-01-01 02:57:44 UTC | 2m 44s | `4.783` | `4.781` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 20 | `LONG` | 2026-01-01 02:58:59 UTC | 2026-01-01 02:59:00 UTC | 0.9s | `4.784` | `4.789` | $0.96 | $0.01 | $0.000000 | **+0.0010** | `+7.8%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 21 | `LONG` | 2026-01-01 03:01:59 UTC | 2026-01-01 03:02:00 UTC | 0.5s | `4.716` | `4.721` | $0.94 | $0.01 | $0.000000 | **+0.0010** | `+8.0%` | `MIN_PROFIT_TP_HIT` | $100.0014 |
| 22 | `LONG` | 2026-01-01 03:13:59 UTC | 2026-01-01 03:14:45 UTC | 45.8s | `4.733` | `4.738` | $0.95 | $0.01 | $0.000000 | **+0.0010** | `+7.9%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 23 | `LONG` | 2026-01-01 03:18:59 UTC | 2026-01-01 03:25:15 UTC | 6m 15s | `4.734` | `4.739` | $0.95 | $0.01 | $0.000000 | **+0.0010** | `+7.9%` | `MIN_PROFIT_TP_HIT` | $100.0034 |
| 24 | `LONG` | 2026-01-01 03:29:59 UTC | 2026-01-01 03:31:33 UTC | 1m 33s | `4.738` | `4.736` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0030 |
| 25 | `LONG` | 2026-01-01 03:37:59 UTC | 2026-01-01 03:39:36 UTC | 1m 36s | `4.740` | `4.738` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $100.0026 |
| ... | ... | *(40278 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 40304 | `LONG` | 2026-08-30 20:40:59 UTC | 2026-08-30 20:41:52 UTC | 52.8s | `2.514` | `2.519` | $0.50 | $0.01 | $0.000000 | **+0.0010** | `+14.9%` | `MIN_PROFIT_TP_HIT` | $98.9200 |
| 40305 | `SHORT` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:47:10 UTC | 10.1s | `2.518` | `2.520` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9196 |
| 40306 | `LONG` | 2026-08-30 20:50:59 UTC | 2026-08-30 20:52:17 UTC | 1m 17s | `2.525` | `2.523` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $98.9192 |
| 40307 | `LONG` | 2026-08-30 20:54:59 UTC | 2026-08-30 20:56:30 UTC | 1m 30s | `2.525` | `2.523` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $98.9188 |
| 40308 | `SHORT` | 2026-08-30 21:03:59 UTC | 2026-08-30 21:04:03 UTC | 3.9s | `2.500` | `2.502` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9184 |
| 40309 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:07 UTC | 7.4s | `2.503` | `2.501` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9180 |
| 40310 | `LONG` | 2026-08-30 21:32:59 UTC | 2026-08-30 21:33:09 UTC | 9.9s | `2.509` | `2.507` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9176 |
| 40311 | `LONG` | 2026-08-30 21:35:59 UTC | 2026-08-30 21:37:12 UTC | 1m 12s | `2.510` | `2.508` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9172 |
| 40312 | `SHORT` | 2026-08-30 21:50:59 UTC | 2026-08-30 21:51:00 UTC | 0.5s | `2.488` | `2.490` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9168 |
| 40313 | `LONG` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:58 UTC | 58.1s | `2.506` | `2.511` | $0.50 | $0.01 | $0.000000 | **+0.0010** | `+15.0%` | `MIN_PROFIT_TP_HIT` | $98.9178 |
| 40314 | `SHORT` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:03 UTC | 3.7s | `2.516` | `2.518` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $98.9174 |
| 40315 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:21:17 UTC | 1m 17s | `2.501` | `2.496` | $0.50 | $0.01 | $0.000000 | **+0.0010** | `+15.0%` | `MIN_PROFIT_TP_HIT` | $98.9184 |
| 40316 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:04 UTC | 4.8s | `2.429` | `2.427` | $0.49 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9180 |
| 40317 | `SHORT` | 2026-08-30 22:51:59 UTC | 2026-08-30 22:52:04 UTC | 4.7s | `2.416` | `2.418` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9176 |
| 40318 | `LONG` | 2026-08-30 22:56:59 UTC | 2026-08-30 22:59:02 UTC | 2m 02s | `2.424` | `2.422` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9172 |
| 40319 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:05 UTC | 5.0s | `2.409` | `2.414` | $0.48 | $0.01 | $0.000000 | **+0.0010** | `+15.6%` | `MIN_PROFIT_TP_HIT` | $98.9182 |
| 40320 | `LONG` | 2026-08-30 23:10:59 UTC | 2026-08-30 23:11:14 UTC | 14.9s | `2.405` | `2.410` | $0.48 | $0.01 | $0.000000 | **+0.0010** | `+15.6%` | `MIN_PROFIT_TP_HIT` | $98.9192 |
| 40321 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:00 UTC | 0.8s | `2.422` | `2.420` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9188 |
| 40322 | `LONG` | 2026-08-30 23:18:59 UTC | 2026-08-30 23:19:00 UTC | 0.6s | `2.415` | `2.413` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9184 |
| 40323 | `LONG` | 2026-08-30 23:24:59 UTC | 2026-08-30 23:25:00 UTC | 0.6s | `2.414` | `2.412` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $98.9180 |
| 40324 | `SHORT` | 2026-08-30 23:32:59 UTC | 2026-08-30 23:33:01 UTC | 1.6s | `2.388` | `2.390` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.3%` | `STOP_LOSS_HIT` | $98.9176 |
| 40325 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:06 UTC | 6.5s | `2.330` | `2.325` | $0.47 | $0.01 | $0.000000 | **+0.0010** | `+16.1%` | `MIN_PROFIT_TP_HIT` | $98.9186 |
| 40326 | `LONG` | 2026-08-30 23:53:59 UTC | 2026-08-30 23:54:11 UTC | 11.8s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **-0.0004** | `-6.4%` | `STOP_LOSS_HIT` | $98.9182 |
| 40327 | `LONG` | 2026-08-30 23:57:59 UTC | 2026-08-30 23:58:00 UTC | 0.5s | `2.343` | `2.341` | $0.47 | $0.01 | $0.000000 | **-0.0004** | `-6.4%` | `STOP_LOSS_HIT` | $98.9178 |
| 40328 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:02 UTC | 2.0s | `2.338` | `2.336` | $0.47 | $0.01 | $0.000000 | **-0.0004** | `-6.4%` | `STOP_LOSS_HIT` | $98.9174 |

> 💡 *Full granular dataset with all 40328 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
