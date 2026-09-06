# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 14:08:12 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.9856 USDT` | `₹9,538.09` | `+0.99%` |
| **Net Realized PnL** | **`+0.9856 USDT`** | **`₹+93.09`** | **`+0.99% Net ROI`** |
| **Gross Profit** | `+11.4468 USDT` | `₹1,081.15` | Total positive trade returns |
| **Gross Loss** | `-10.4612 USDT` | `₹988.06` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.09`** | — | Profitable |
| **Win / Loss Payoff** | `0.20` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.1916 USDT` | `₹18.10` | **`-0.19%` Peak-to-Trough** |
| **Win Rate** | **`84.41%`** | — | `28617 Wins / 5285 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `2.61` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `1.14` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `5.15` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `33902` | Total completed trade lifecycle events |
| **Winning Trades** | `28617` | `84.41%` of total trades |
| **Losing Trades** | `5285` | `15.59%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0020 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.1% ROE)` | Trade #2 (SHORT) |
| **Largest Losing Trade** | `-0.0020 USDT (-15.9% ROE)` | Trade #66 (LONG) |
| **Max Consecutive Wins** | `49` trades | Peak winning streak |
| **Max Consecutive Losses** | `5` trades | Peak losing streak |
| **Average Trade Duration** | `3m 59s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #493 |
| **Longest Trade In-Position** | `4h 01m 27s` | Trade #31730 |
| **Cumulative Time In Position** | `2254h 18m 40s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `16915` (49.9%) | `16987` (50.1%) | `33902` |
| **Wins / Losses** | `14209 W / 2706 L` | `14408 W / 2579 L` | `28617 W / 5285 L` |
| **Win Rate** | **`84.00%`** | **`84.82%`** | **`84.41%`** |
| **Gross Profit** | `+5.6836 USDT` | `+5.7632 USDT` | `+11.4468 USDT` |
| **Gross Loss** | `-5.3560 USDT` | `-5.1052 USDT` | `-10.4612 USDT` |
| **Net Realized PnL** | **`+0.3276 USDT`** | **`+0.6580 USDT`** | **`+0.9856 USDT`** |
| **Net PnL (INR)** | `₹+30.94` | `₹+62.15` | `₹+93.09` |
| **Profit Factor** | `1.06` | `1.13` | `1.09` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `28617` | `84.4%` | `+11.4468 USDT` | `₹+1,081.15` | `100.0%` | `2m 59s` |
| `STOP_LOSS_HIT` | `5285` | `15.6%` | `-10.4612 USDT` | `₹-988.06` | `0.0%` | `9m 25s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:27:59 UTC | 2026-01-01 00:29:45 UTC | 1m 45s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 00:36:59 UTC | 2026-01-01 00:43:19 UTC | 6m 19s | `4.807` | `4.805` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:53:31 UTC | 3m 31s | `4.809` | `4.807` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:57:12 UTC | 2m 12s | `4.808` | `4.810` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 5 | `LONG` | 2026-01-01 01:03:59 UTC | 2026-01-01 01:04:12 UTC | 12.7s | `4.816` | `4.818` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 6 | `LONG` | 2026-01-01 01:11:59 UTC | 2026-01-01 01:16:06 UTC | 4m 06s | `4.822` | `4.824` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 7 | `SHORT` | 2026-01-01 01:17:59 UTC | 2026-01-01 01:18:14 UTC | 14.0s | `4.816` | `4.814` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 8 | `SHORT` | 2026-01-01 01:25:59 UTC | 2026-01-01 01:26:07 UTC | 7.9s | `4.809` | `4.807` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 9 | `SHORT` | 2026-01-01 01:30:59 UTC | 2026-01-01 01:38:04 UTC | 7m 04s | `4.805` | `4.803` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 10 | `LONG` | 2026-01-01 01:46:59 UTC | 2026-01-01 01:47:37 UTC | 37.3s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 11 | `LONG` | 2026-01-01 01:50:59 UTC | 2026-01-01 01:51:30 UTC | 30.9s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 12 | `SHORT` | 2026-01-01 02:01:59 UTC | 2026-01-01 02:04:23 UTC | 2m 23s | `4.800` | `4.798` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 13 | `SHORT` | 2026-01-01 02:08:59 UTC | 2026-01-01 02:25:43 UTC | 16m 43s | `4.797` | `4.795` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 14 | `SHORT` | 2026-01-01 02:31:59 UTC | 2026-01-01 02:32:05 UTC | 5.6s | `4.793` | `4.791` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 15 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:40:01 UTC | 4m 01s | `4.794` | `4.784` | $0.96 | $0.01 | $0.000000 | **-0.0020** | `-15.6%` | `STOP_LOSS_HIT` | $100.0036 |
| 16 | `SHORT` | 2026-01-01 02:44:59 UTC | 2026-01-01 03:01:00 UTC | 16m 00s | `4.782` | `4.780` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 17 | `LONG` | 2026-01-01 03:13:59 UTC | 2026-01-01 03:14:14 UTC | 14.1s | `4.733` | `4.735` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 18 | `LONG` | 2026-01-01 03:18:59 UTC | 2026-01-01 03:20:02 UTC | 1m 02s | `4.734` | `4.736` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 19 | `LONG` | 2026-01-01 03:24:59 UTC | 2026-01-01 03:25:15 UTC | 15.7s | `4.737` | `4.739` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 20 | `LONG` | 2026-01-01 03:29:59 UTC | 2026-01-01 03:30:09 UTC | 9.9s | `4.738` | `4.740` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 21 | `LONG` | 2026-01-01 03:37:59 UTC | 2026-01-01 03:38:15 UTC | 15.4s | `4.740` | `4.742` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0060 |
| 22 | `LONG` | 2026-01-01 03:40:59 UTC | 2026-01-01 03:54:07 UTC | 13m 07s | `4.737` | `4.727` | $0.95 | $0.01 | $0.000000 | **-0.0020** | `-15.8%` | `STOP_LOSS_HIT` | $100.0040 |
| 23 | `SHORT` | 2026-01-01 04:00:59 UTC | 2026-01-01 04:01:01 UTC | 1.1s | `4.722` | `4.720` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 24 | `SHORT` | 2026-01-01 04:10:59 UTC | 2026-01-01 04:13:33 UTC | 2m 33s | `4.711` | `4.709` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 25 | `LONG` | 2026-01-01 04:17:59 UTC | 2026-01-01 04:18:29 UTC | 29.3s | `4.715` | `4.717` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| ... | ... | *(33852 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 33878 | `LONG` | 2026-08-30 20:40:59 UTC | 2026-08-30 20:41:14 UTC | 14.5s | `2.514` | `2.516` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9832 |
| 33879 | `SHORT` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:47:01 UTC | 1.6s | `2.518` | `2.516` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9836 |
| 33880 | `LONG` | 2026-08-30 20:50:59 UTC | 2026-08-30 20:51:06 UTC | 6.9s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $100.9840 |
| 33881 | `LONG` | 2026-08-30 20:54:59 UTC | 2026-08-30 20:56:09 UTC | 1m 09s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $100.9844 |
| 33882 | `SHORT` | 2026-08-30 21:03:59 UTC | 2026-08-30 21:05:15 UTC | 1m 15s | `2.500` | `2.498` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9848 |
| 33883 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:19:17 UTC | 3m 17s | `2.503` | `2.493` | $0.50 | $0.01 | $0.000000 | **-0.0020** | `-30.0%` | `STOP_LOSS_HIT` | $100.9828 |
| 33884 | `LONG` | 2026-08-30 21:32:59 UTC | 2026-08-30 21:33:24 UTC | 24.1s | `2.509` | `2.511` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9832 |
| 33885 | `LONG` | 2026-08-30 21:35:59 UTC | 2026-08-30 21:36:51 UTC | 51.1s | `2.510` | `2.512` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9836 |
| 33886 | `SHORT` | 2026-08-30 21:50:59 UTC | 2026-08-30 21:53:15 UTC | 2m 15s | `2.488` | `2.498` | $0.50 | $0.01 | $0.000000 | **-0.0020** | `-30.1%` | `STOP_LOSS_HIT` | $100.9816 |
| 33887 | `LONG` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:02 UTC | 2.5s | `2.506` | `2.508` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9820 |
| 33888 | `SHORT` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:12 UTC | 12.5s | `2.516` | `2.514` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9824 |
| 33889 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:18 UTC | 18.2s | `2.501` | `2.499` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.9828 |
| 33890 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:45:08 UTC | 1m 08s | `2.429` | `2.431` | $0.49 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9832 |
| 33891 | `SHORT` | 2026-08-30 22:51:59 UTC | 2026-08-30 22:54:08 UTC | 2m 08s | `2.416` | `2.414` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9836 |
| 33892 | `LONG` | 2026-08-30 22:56:59 UTC | 2026-08-30 22:57:22 UTC | 22.4s | `2.424` | `2.426` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9840 |
| 33893 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:00 UTC | 0.4s | `2.409` | `2.411` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9844 |
| 33894 | `LONG` | 2026-08-30 23:10:59 UTC | 2026-08-30 23:11:01 UTC | 1.1s | `2.405` | `2.407` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9848 |
| 33895 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:17:06 UTC | 1m 06s | `2.422` | `2.412` | $0.48 | $0.01 | $0.000000 | **-0.0020** | `-31.0%` | `STOP_LOSS_HIT` | $100.9828 |
| 33896 | `LONG` | 2026-08-30 23:18:59 UTC | 2026-08-30 23:19:07 UTC | 7.4s | `2.415` | `2.417` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9832 |
| 33897 | `LONG` | 2026-08-30 23:24:59 UTC | 2026-08-30 23:25:00 UTC | 0.4s | `2.414` | `2.416` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.9836 |
| 33898 | `SHORT` | 2026-08-30 23:32:59 UTC | 2026-08-30 23:33:29 UTC | 29.1s | `2.388` | `2.386` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.9840 |
| 33899 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.7s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.9844 |
| 33900 | `LONG` | 2026-08-30 23:53:59 UTC | 2026-08-30 23:54:46 UTC | 46.7s | `2.330` | `2.332` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.9848 |
| 33901 | `LONG` | 2026-08-30 23:57:59 UTC | 2026-08-30 23:58:03 UTC | 3.2s | `2.343` | `2.345` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.9852 |
| 33902 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.9s | `2.338` | `2.340` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.9856 |

> 💡 *Full granular dataset with all 33902 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
