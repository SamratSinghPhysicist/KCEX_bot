# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 02:30:32 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.0258 USDT` | `₹9,352.99` | `-0.97%` |
| **Net Realized PnL** | **`-0.9742 USDT`** | **`₹-92.01`** | **`-0.97% Net ROI`** |
| **Gross Profit** | `+0.3070 USDT` | `₹29.00` | Total positive trade returns |
| **Gross Loss** | `-1.2812 USDT` | `₹121.01` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.24`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.79` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.9742 USDT` | `₹92.01` | **`-0.97%` Peak-to-Trough** |
| **Win Rate** | **`11.81%`** | — | `307 Wins / 2292 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-56.71` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-51.14` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-1.00` | — | Net ROI divided by Max Drawdown |

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
| **Slippage Tolerance** | `1 ticks` (`0.00001 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Total Trades Executed** | `2599` | Total completed trade lifecycle events |
| **Winning Trades** | `307` | `11.81%` of total trades |
| **Losing Trades** | `2292` | `88.19%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0006 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+5.3% ROE)` | Trade #6 (LONG) |
| **Largest Losing Trade** | `-0.0006 USDT (-3.1% ROE)` | Trade #1 (LONG) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `51` trades | Peak losing streak |
| **Average Trade Duration** | `16.0s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #14 |
| **Longest Trade In-Position** | `6m 24s` | Trade #2178 |
| **Cumulative Time In Position** | `11h 33m 26s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1305` (50.2%) | `1294` (49.8%) | `2599` |
| **Wins / Losses** | `153 W / 1152 L` | `154 W / 1140 L` | `307 W / 2292 L` |
| **Win Rate** | **`11.72%`** | **`11.90%`** | **`11.81%`** |
| **Gross Profit** | `+0.1530 USDT` | `+0.1540 USDT` | `+0.3070 USDT` |
| **Gross Loss** | `-0.6394 USDT` | `-0.6418 USDT` | `-1.2812 USDT` |
| **Net Realized PnL** | **`-0.4864 USDT`** | **`-0.4878 USDT`** | **`-0.9742 USDT`** |
| **Net PnL (INR)** | `₹-45.94` | `₹-46.07` | `₹-92.01` |
| **Profit Factor** | `0.24` | `0.24` | `0.24` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `1994` | `76.7%` | `-1.1964 USDT` | `₹-113.00` | `0.0%` | `6.5s` |
| `MIN_PROFIT_TP_HIT` | `307` | `11.8%` | `+0.3070 USDT` | `₹+29.00` | `100.0%` | `43.1s` |
| `RATCHET_BREAKEVEN_HIT` | `172` | `6.6%` | `-0.0344 USDT` | `₹-3.25` | `0.0%` | `54.1s` |
| `RATCHET_TIGHTEN_HIT` | `126` | `4.8%` | `-0.0504 USDT` | `₹-4.76` | `0.0%` | `49.0s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:05 UTC | 5.7s | `0.07183` | `0.07180` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:36:01 UTC | 1.2s | `0.07185` | `0.07188` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:45:00 UTC | 0.3s | `0.07170` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9982 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:00 UTC | 0.1s | `0.07174` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9976 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:09:00 UTC | 0.2s | `0.07137` | `0.07134` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9970 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:00 UTC | 0.8s | `0.07103` | `0.07108` | $1.42 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:00 UTC | 0.3s | `0.07111` | `0.07114` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9974 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:03 UTC | 3.1s | `0.07125` | `0.07126` | $1.42 | $0.02 | $0.000000 | **-0.0002** | `-1.1%` | `RATCHET_BREAKEVEN_HIT` | $99.9972 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:06 UTC | 6.2s | `0.07137` | `0.07132` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $99.9982 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:00 UTC | 0.9s | `0.07188` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9976 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:00 UTC | 1.0s | `0.07185` | `0.07182` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9970 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:02 UTC | 2.8s | `0.07183` | `0.07186` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9964 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:09 UTC | 9.2s | `0.07195` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9958 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:10:00 UTC | 0.1s | `0.07177` | `0.07174` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9952 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:00 UTC | 0.7s | `0.07201` | `0.07204` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9946 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:21 UTC | 21.9s | `0.07209` | `0.07211` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `RATCHET_TIGHTEN_HIT` | $99.9942 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:30:24 UTC | 24.3s | `0.07210` | `0.07209` | $1.44 | $0.02 | $0.000000 | **-0.0002** | `-1.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9940 |
| 18 | `LONG` | 2026-07-01 02:31:59 UTC | 2026-07-01 02:32:08 UTC | 8.9s | `0.07207` | `0.07206` | $1.44 | $0.02 | $0.000000 | **-0.0002** | `-1.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9938 |
| 19 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:00 UTC | 0.2s | `0.07215` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9932 |
| 20 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:10 UTC | 10.8s | `0.07190` | `0.07193` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9926 |
| 21 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:00 UTC | 0.3s | `0.07195` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9920 |
| 22 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 02:59:01 UTC | 1.7s | `0.07194` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9914 |
| 23 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:16 UTC | 16.7s | `0.07208` | `0.07209` | $1.44 | $0.02 | $0.000000 | **-0.0002** | `-1.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9912 |
| 24 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:00 UTC | 0.2s | `0.07187` | `0.07184` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9906 |
| 25 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:24:00 UTC | 1.0s | `0.07193` | `0.07190` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9900 |
| ... | ... | *(2549 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2575 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:14 UTC | 14.8s | `0.07164` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `RATCHET_TIGHTEN_HIT` | $99.0360 |
| 2576 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:03 UTC | 3.7s | `0.07153` | `0.07158` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $99.0370 |
| 2577 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:00 UTC | 0.2s | `0.07163` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0364 |
| 2578 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:03 UTC | 3.1s | `0.07141` | `0.07138` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0358 |
| 2579 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:42:02 UTC | 2.6s | `0.07121` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0352 |
| 2580 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:15 UTC | 15.4s | `0.07128` | `0.07127` | $1.43 | $0.02 | $0.000000 | **-0.0002** | `-1.1%` | `RATCHET_BREAKEVEN_HIT` | $99.0350 |
| 2581 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:51:05 UTC | 5.5s | `0.07125` | `0.07128` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0344 |
| 2582 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:10 UTC | 10.6s | `0.07141` | `0.07144` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0338 |
| 2583 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:01 UTC | 1.5s | `0.07152` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0332 |
| 2584 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:00 UTC | 0.7s | `0.07159` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0326 |
| 2585 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:13:15 UTC | 15.0s | `0.07165` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0320 |
| 2586 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:17:30 UTC | 30.6s | `0.07173` | `0.07172` | $1.43 | $0.02 | $0.000000 | **-0.0002** | `-1.0%` | `RATCHET_BREAKEVEN_HIT` | $99.0318 |
| 2587 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:05 UTC | 5.0s | `0.07173` | `0.07176` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0312 |
| 2588 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:18 UTC | 18.9s | `0.07170` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0306 |
| 2589 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:36:09 UTC | 1m 09s | `0.07157` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `RATCHET_TIGHTEN_HIT` | $99.0302 |
| 2590 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:49:23 UTC | 1m 23s | `0.07157` | `0.07152` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $99.0312 |
| 2591 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:01 UTC | 1.5s | `0.07133` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0306 |
| 2592 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:02 UTC | 2.2s | `0.07128` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0300 |
| 2593 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:09:02 UTC | 2.2s | `0.07127` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0294 |
| 2594 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:16:00 UTC | 0.8s | `0.07142` | `0.07145` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0288 |
| 2595 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:10 UTC | 10.2s | `0.07154` | `0.07157` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0282 |
| 2596 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:09 UTC | 9.7s | `0.07167` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0276 |
| 2597 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:00 UTC | 0.4s | `0.07162` | `0.07159` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0270 |
| 2598 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:02 UTC | 2.4s | `0.07186` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0264 |
| 2599 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:00 UTC | 0.5s | `0.07201` | `0.07198` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0258 |

> 💡 *Full granular dataset with all 2599 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
