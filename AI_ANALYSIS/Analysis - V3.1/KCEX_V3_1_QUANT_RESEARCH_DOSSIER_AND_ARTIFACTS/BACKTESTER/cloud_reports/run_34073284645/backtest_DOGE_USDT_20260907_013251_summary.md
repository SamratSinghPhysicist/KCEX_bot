# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 01:32:51 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.1064 USDT` | `₹9,455.05` | `+0.11%` |
| **Net Realized PnL** | **`+0.1064 USDT`** | **`₹+10.05`** | **`+0.11% Net ROI`** |
| **Gross Profit** | `+0.8960 USDT` | `₹84.63` | Total positive trade returns |
| **Gross Loss** | `-0.7896 USDT` | `₹74.58` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.13`** | — | Profitable |
| **Win / Loss Payoff** | `5.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0400 USDT` | `₹3.78` | **`-0.04%` Peak-to-Trough** |
| **Win Rate** | **`18.50%`** | — | `448 Wins / 1974 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `3.67` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `8.54` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `2.66` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `DOGE_USDT` | Base Asset: `DOGE` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-07-01` → `2026-07-14` | Historical evaluation window |
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.00000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Trade Volume / Quantity** | `2 contract(s) (20 DOGE per trade)` | Quantity committed per trade signal |
| **Leverage Multiplier** | `75x` | Margin required = Position Notional / Leverage |
| **Starting Capital** | `100.00 USDT` | `₹9,445.00 INR` (`1 USDT = ₹94.45`) |
| **Take Profit Target** | `+10 ticks` (`+0.00010 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
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
| **Total Trades Executed** | `2422` | Total completed trade lifecycle events |
| **Winning Trades** | `448` | `18.50%` of total trades |
| **Losing Trades** | `1974` | `81.50%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0020 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0020 USDT (+10.6% ROE)` | Trade #6 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-2.1% ROE)` | Trade #2 (SHORT) |
| **Max Consecutive Wins** | `4` trades | Peak winning streak |
| **Max Consecutive Losses** | `53` trades | Peak losing streak |
| **Average Trade Duration** | `1m 13s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #316 |
| **Longest Trade In-Position** | `28m 16s` | Trade #1954 |
| **Cumulative Time In Position** | `49h 32m 59s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1211` (50.0%) | `1211` (50.0%) | `2422` |
| **Wins / Losses** | `218 W / 993 L` | `230 W / 981 L` | `448 W / 1974 L` |
| **Win Rate** | **`18.00%`** | **`18.99%`** | **`18.50%`** |
| **Gross Profit** | `+0.4360 USDT` | `+0.4600 USDT` | `+0.8960 USDT` |
| **Gross Loss** | `-0.3972 USDT` | `-0.3924 USDT` | `-0.7896 USDT` |
| **Net Realized PnL** | **`+0.0388 USDT`** | **`+0.0676 USDT`** | **`+0.1064 USDT`** |
| **Net PnL (INR)** | `₹+3.66` | `₹+6.38` | `₹+10.05` |
| **Profit Factor** | `1.10` | `1.17` | `1.13` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `1974` | `81.5%` | `-0.7896 USDT` | `₹-74.58` | `0.0%` | `56.2s` |
| `MIN_PROFIT_TP_HIT` | `448` | `18.5%` | `+0.8960 USDT` | `₹+84.63` | `100.0%` | `2m 30s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:06 UTC | 6.3s | `0.07182` | `0.07180` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:36:05 UTC | 5.6s | `0.07186` | `0.07188` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:45:03 UTC | 3.9s | `0.07169` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:04 UTC | 4.1s | `0.07175` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9984 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:10:15 UTC | 1m 15s | `0.07136` | `0.07134` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9980 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:07 UTC | 7.4s | `0.07102` | `0.07112` | $1.42 | $0.02 | $0.000000 | **+0.0020** | `+10.6%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:00 UTC | 0.6s | `0.07112` | `0.07114` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:24 UTC | 24.5s | `0.07126` | `0.07128` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:49 UTC | 49.4s | `0.07138` | `0.07128` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:01 UTC | 1.0s | `0.07189` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:00 UTC | 1.0s | `0.07184` | `0.07182` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:05 UTC | 5.0s | `0.07184` | `0.07186` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:11 UTC | 11.5s | `0.07194` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:12:01 UTC | 2m 01s | `0.07176` | `0.07186` | $1.44 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:02 UTC | 2.9s | `0.07202` | `0.07204` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0012 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:22 UTC | 22.2s | `0.07210` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:31:01 UTC | 1m 01s | `0.07209` | `0.07219` | $1.44 | $0.02 | $0.000000 | **+0.0020** | `+10.4%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 18 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:01 UTC | 1.2s | `0.07214` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0024 |
| 19 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:14 UTC | 14.1s | `0.07191` | `0.07193` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0020 |
| 20 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:05 UTC | 5.9s | `0.07194` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0016 |
| 21 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 02:59:09 UTC | 9.9s | `0.07195` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0012 |
| 22 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:15:04 UTC | 5m 04s | `0.07209` | `0.07199` | $1.44 | $0.02 | $0.000000 | **+0.0020** | `+10.4%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 23 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:09 UTC | 9.5s | `0.07186` | `0.07184` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0028 |
| 24 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:24:24 UTC | 24.8s | `0.07192` | `0.07190` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0024 |
| 25 | `SHORT` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:28:12 UTC | 12.9s | `0.07189` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0020 |
| ... | ... | *(2372 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2398 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:36 UTC | 36.5s | `0.07163` | `0.07161` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1064 |
| 2399 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:10 UTC | 10.3s | `0.07152` | `0.07162` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.1084 |
| 2400 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:02 UTC | 2.2s | `0.07164` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1080 |
| 2401 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:09 UTC | 9.3s | `0.07140` | `0.07138` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1076 |
| 2402 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:43:53 UTC | 1m 53s | `0.07120` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1072 |
| 2403 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:29 UTC | 29.1s | `0.07127` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1068 |
| 2404 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:51:43 UTC | 44.0s | `0.07126` | `0.07128` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1064 |
| 2405 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:20 UTC | 20.8s | `0.07142` | `0.07144` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1060 |
| 2406 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:05 UTC | 5.3s | `0.07153` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1056 |
| 2407 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:00 UTC | 0.8s | `0.07160` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1052 |
| 2408 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:14:47 UTC | 1m 47s | `0.07164` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1048 |
| 2409 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:20:31 UTC | 3m 31s | `0.07172` | `0.07182` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.1068 |
| 2410 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:24:28 UTC | 1m 28s | `0.07174` | `0.07164` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.1088 |
| 2411 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:38 UTC | 38.2s | `0.07169` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1084 |
| 2412 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:38:29 UTC | 3m 29s | `0.07156` | `0.07154` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1080 |
| 2413 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:50:36 UTC | 2m 36s | `0.07158` | `0.07148` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $100.1100 |
| 2414 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:03 UTC | 3.2s | `0.07132` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1096 |
| 2415 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:02 UTC | 2.3s | `0.07127` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1092 |
| 2416 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:09:12 UTC | 12.0s | `0.07128` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1088 |
| 2417 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:16:37 UTC | 37.2s | `0.07143` | `0.07145` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1084 |
| 2418 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:11 UTC | 11.8s | `0.07155` | `0.07157` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1080 |
| 2419 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:18 UTC | 18.2s | `0.07168` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1076 |
| 2420 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:00 UTC | 0.7s | `0.07161` | `0.07159` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1072 |
| 2421 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:03 UTC | 3.1s | `0.07187` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1068 |
| 2422 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:00 UTC | 0.9s | `0.07200` | `0.07198` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.1064 |

> 💡 *Full granular dataset with all 2422 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
