# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 01:33:17 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.9328 USDT` | `₹9,438.65` | `-0.07%` |
| **Net Realized PnL** | **`-0.0672 USDT`** | **`₹-6.35`** | **`-0.07% Net ROI`** |
| **Gross Profit** | `+0.7148 USDT` | `₹67.51` | Total positive trade returns |
| **Gross Loss** | `-0.7820 USDT` | `₹73.86` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.91`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `0.40` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0702 USDT` | `₹6.63` | **`-0.07%` Peak-to-Trough** |
| **Win Rate** | **`69.56%`** | — | `1787 Wins / 782 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-3.16` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-2.03` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.96` | — | Net ROI divided by Max Drawdown |

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
| **Take Profit Target** | `+2 ticks` (`+0.00002 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-5 ticks away from entry (0.00005 USDT)` | Stop loss evaluation logic |

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
| **Total Trades Executed** | `2569` | Total completed trade lifecycle events |
| **Winning Trades** | `1787` | `69.56%` of total trades |
| **Losing Trades** | `782` | `30.44%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0000 USDT` (`₹-0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0010 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+2.1% ROE)` | Trade #1 (LONG) |
| **Largest Losing Trade** | `-0.0010 USDT (-5.2% ROE)` | Trade #2 (SHORT) |
| **Max Consecutive Wins** | `18` trades | Peak winning streak |
| **Max Consecutive Losses** | `7` trades | Peak losing streak |
| **Average Trade Duration** | `41.4s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #8 |
| **Longest Trade In-Position** | `12m 22s` | Trade #2052 |
| **Cumulative Time In Position** | `29h 31m 35s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1288` (50.1%) | `1281` (49.9%) | `2569` |
| **Wins / Losses** | `886 W / 402 L` | `901 W / 380 L` | `1787 W / 782 L` |
| **Win Rate** | **`68.79%`** | **`70.34%`** | **`69.56%`** |
| **Gross Profit** | `+0.3544 USDT` | `+0.3604 USDT` | `+0.7148 USDT` |
| **Gross Loss** | `-0.4020 USDT` | `-0.3800 USDT` | `-0.7820 USDT` |
| **Net Realized PnL** | **`-0.0476 USDT`** | **`-0.0196 USDT`** | **`-0.0672 USDT`** |
| **Net PnL (INR)** | `₹-4.50` | `₹-1.85` | `₹-6.35` |
| **Profit Factor** | `0.88` | `0.95` | `0.91` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `1787` | `69.6%` | `+0.7148 USDT` | `₹+67.51` | `100.0%` | `33.5s` |
| `STOP_LOSS_HIT` | `782` | `30.4%` | `-0.7820 USDT` | `₹-73.86` | `0.0%` | `59.3s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:30:05 UTC | 1m 05s | `0.07182` | `0.07184` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:37:17 UTC | 1m 17s | `0.07186` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9994 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:48:14 UTC | 3m 14s | `0.07169` | `0.07164` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9984 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:28 UTC | 28.5s | `0.07175` | `0.07180` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9974 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:09:03 UTC | 3.8s | `0.07136` | `0.07138` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9978 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:00 UTC | 0.1s | `0.07102` | `0.07104` | $1.42 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9982 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:03 UTC | 3.7s | `0.07112` | `0.07110` | $1.42 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9986 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:00 UTC | 0.1s | `0.07126` | `0.07124` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9990 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:00 UTC | 0.6s | `0.07138` | `0.07136` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9994 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:06 UTC | 6.6s | `0.07189` | `0.07187` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9998 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:49 UTC | 49.3s | `0.07184` | `0.07186` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:43 UTC | 43.8s | `0.07184` | `0.07182` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0006 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:02 UTC | 2.5s | `0.07194` | `0.07196` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0010 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:10:03 UTC | 3.9s | `0.07176` | `0.07178` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0014 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:25 UTC | 25.8s | `0.07202` | `0.07200` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:11 UTC | 11.1s | `0.07210` | `0.07208` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:30:00 UTC | 0.1s | `0.07209` | `0.07211` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0026 |
| 18 | `LONG` | 2026-07-01 02:31:59 UTC | 2026-07-01 02:32:02 UTC | 2.5s | `0.07206` | `0.07208` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0030 |
| 19 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:33 UTC | 33.6s | `0.07214` | `0.07209` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $100.0020 |
| 20 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:11 UTC | 11.8s | `0.07191` | `0.07189` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 21 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:32 UTC | 32.3s | `0.07194` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $100.0014 |
| 22 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 03:00:05 UTC | 1m 05s | `0.07195` | `0.07200` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $100.0004 |
| 23 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:04 UTC | 4.7s | `0.07209` | `0.07207` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 24 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:21:01 UTC | 1m 01s | `0.07186` | `0.07188` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 25 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:25:38 UTC | 1m 38s | `0.07192` | `0.07194` | $1.44 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| ... | ... | *(2519 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2545 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:05 UTC | 5.5s | `0.07163` | `0.07165` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9400 |
| 2546 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:01 UTC | 1.3s | `0.07152` | `0.07154` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9404 |
| 2547 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:26:16 UTC | 1m 16s | `0.07164` | `0.07169` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9394 |
| 2548 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:22 UTC | 23.0s | `0.07140` | `0.07142` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9398 |
| 2549 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:43:03 UTC | 1m 03s | `0.07120` | `0.07122` | $1.42 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9402 |
| 2550 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:00 UTC | 0.9s | `0.07127` | `0.07129` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9406 |
| 2551 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:52:03 UTC | 1m 03s | `0.07126` | `0.07131` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.3%` | `STOP_LOSS_HIT` | $99.9396 |
| 2552 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:30 UTC | 30.2s | `0.07142` | `0.07147` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.3%` | `STOP_LOSS_HIT` | $99.9386 |
| 2553 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:11 UTC | 11.5s | `0.07153` | `0.07151` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9390 |
| 2554 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:03 UTC | 4.0s | `0.07160` | `0.07165` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9380 |
| 2555 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:13:01 UTC | 1.9s | `0.07164` | `0.07166` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9384 |
| 2556 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:17:05 UTC | 5.4s | `0.07172` | `0.07174` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9388 |
| 2557 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:11 UTC | 11.1s | `0.07174` | `0.07172` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9392 |
| 2558 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:30:43 UTC | 2m 43s | `0.07169` | `0.07164` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9382 |
| 2559 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:35:00 UTC | 0.8s | `0.07156` | `0.07158` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9386 |
| 2560 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:48:29 UTC | 29.4s | `0.07158` | `0.07156` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9390 |
| 2561 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:14 UTC | 14.7s | `0.07132` | `0.07127` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.3%` | `STOP_LOSS_HIT` | $99.9380 |
| 2562 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:25 UTC | 25.4s | `0.07127` | `0.07129` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9384 |
| 2563 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:11:04 UTC | 2m 04s | `0.07128` | `0.07133` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.3%` | `STOP_LOSS_HIT` | $99.9374 |
| 2564 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:18:14 UTC | 2m 14s | `0.07143` | `0.07148` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9364 |
| 2565 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:51 UTC | 51.7s | `0.07155` | `0.07160` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9354 |
| 2566 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:54 UTC | 54.4s | `0.07168` | `0.07173` | $1.43 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9344 |
| 2567 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:55 UTC | 55.1s | `0.07161` | `0.07163` | $1.43 | $0.02 | $0.000000 | **+0.0004** | `+2.1%` | `MIN_PROFIT_TP_HIT` | $99.9348 |
| 2568 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:18 UTC | 18.4s | `0.07187` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9338 |
| 2569 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:46 UTC | 46.5s | `0.07200` | `0.07195` | $1.44 | $0.02 | $0.000000 | **-0.0010** | `-5.2%` | `STOP_LOSS_HIT` | $99.9328 |

> 💡 *Full granular dataset with all 2569 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
