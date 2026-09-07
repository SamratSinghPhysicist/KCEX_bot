# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 02:30:23 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.0432 USDT` | `₹9,354.63` | `-0.96%` |
| **Net Realized PnL** | **`-0.9568 USDT`** | **`₹-90.37`** | **`-0.96% Net ROI`** |
| **Gross Profit** | `+0.4220 USDT` | `₹39.86` | Total positive trade returns |
| **Gross Loss** | `-1.3788 USDT` | `₹130.23` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.31`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `3.33` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.9568 USDT` | `₹90.37` | **`-0.96%` Peak-to-Trough** |
| **Win Rate** | **`8.41%`** | — | `211 Wins / 2298 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-41.10` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-49.43` | — | Downside risk-adjusted return ratio |
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
| **Total Trades Executed** | `2509` | Total completed trade lifecycle events |
| **Winning Trades** | `211` | `8.41%` of total trades |
| **Losing Trades** | `2298` | `91.59%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0020 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0006 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0020 USDT (+10.6% ROE)` | Trade #6 (LONG) |
| **Largest Losing Trade** | `-0.0006 USDT (-3.1% ROE)` | Trade #1 (LONG) |
| **Max Consecutive Wins** | `4` trades | Peak winning streak |
| **Max Consecutive Losses** | `77` trades | Peak losing streak |
| **Average Trade Duration** | `37.0s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #14 |
| **Longest Trade In-Position** | `33m 18s` | Trade #1938 |
| **Cumulative Time In Position** | `25h 47m 39s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1263` (50.3%) | `1246` (49.7%) | `2509` |
| **Wins / Losses** | `104 W / 1159 L` | `107 W / 1139 L` | `211 W / 2298 L` |
| **Win Rate** | **`8.23%`** | **`8.59%`** | **`8.41%`** |
| **Gross Profit** | `+0.2080 USDT` | `+0.2140 USDT` | `+0.4220 USDT` |
| **Gross Loss** | `-0.6954 USDT` | `-0.6834 USDT` | `-1.3788 USDT` |
| **Net Realized PnL** | **`-0.4874 USDT`** | **`-0.4694 USDT`** | **`-0.9568 USDT`** |
| **Net PnL (INR)** | `₹-46.03` | `₹-44.33` | `₹-90.37` |
| **Profit Factor** | `0.30` | `0.31` | `0.31` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `2298` | `91.6%` | `-1.3788 USDT` | `₹-130.23` | `0.0%` | `26.1s` |
| `MIN_PROFIT_TP_HIT` | `211` | `8.4%` | `+0.4220 USDT` | `₹+39.86` | `100.0%` | `2m 35s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:05 UTC | 5.7s | `0.07183` | `0.07180` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:36:01 UTC | 1.2s | `0.07185` | `0.07188` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:45:00 UTC | 0.3s | `0.07170` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9982 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:00 UTC | 0.1s | `0.07174` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9976 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:09:00 UTC | 0.2s | `0.07137` | `0.07134` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9970 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:07 UTC | 7.5s | `0.07103` | `0.07113` | $1.42 | $0.02 | $0.000000 | **+0.0020** | `+10.6%` | `MIN_PROFIT_TP_HIT` | $99.9990 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:00 UTC | 0.3s | `0.07111` | `0.07114` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9984 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:22 UTC | 22.0s | `0.07125` | `0.07128` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9978 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:13 UTC | 13.2s | `0.07137` | `0.07140` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.9972 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:00 UTC | 0.9s | `0.07188` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9966 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:00 UTC | 1.0s | `0.07185` | `0.07182` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9960 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:02 UTC | 2.8s | `0.07183` | `0.07186` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9954 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:09 UTC | 9.2s | `0.07195` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9948 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:10:00 UTC | 0.1s | `0.07177` | `0.07174` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9942 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:00 UTC | 0.7s | `0.07201` | `0.07204` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9936 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:22 UTC | 22.2s | `0.07209` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9930 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:31:07 UTC | 1m 07s | `0.07210` | `0.07220` | $1.44 | $0.02 | $0.000000 | **+0.0020** | `+10.4%` | `MIN_PROFIT_TP_HIT` | $99.9950 |
| 18 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:00 UTC | 0.2s | `0.07215` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9944 |
| 19 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:10 UTC | 10.8s | `0.07190` | `0.07193` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9938 |
| 20 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:00 UTC | 0.3s | `0.07195` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9932 |
| 21 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 02:59:01 UTC | 1.7s | `0.07194` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9926 |
| 22 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:24 UTC | 24.8s | `0.07208` | `0.07211` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9920 |
| 23 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:00 UTC | 0.2s | `0.07187` | `0.07184` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9914 |
| 24 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:24:00 UTC | 1.0s | `0.07193` | `0.07190` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9908 |
| 25 | `SHORT` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:28:12 UTC | 12.6s | `0.07188` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.9902 |
| ... | ... | *(2459 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2485 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:36 UTC | 36.5s | `0.07164` | `0.07161` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0550 |
| 2486 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:17:26 UTC | 3m 26s | `0.07153` | `0.07150` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0544 |
| 2487 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:00 UTC | 0.2s | `0.07163` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0538 |
| 2488 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:03 UTC | 3.1s | `0.07141` | `0.07138` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0532 |
| 2489 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:42:02 UTC | 2.6s | `0.07121` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0526 |
| 2490 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:27 UTC | 27.2s | `0.07128` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0520 |
| 2491 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:51:05 UTC | 5.5s | `0.07125` | `0.07128` | $1.42 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0514 |
| 2492 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:10 UTC | 10.6s | `0.07141` | `0.07144` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0508 |
| 2493 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:01 UTC | 1.5s | `0.07152` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0502 |
| 2494 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:00 UTC | 0.7s | `0.07159` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0496 |
| 2495 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:13:15 UTC | 15.0s | `0.07165` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0490 |
| 2496 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:17:34 UTC | 34.9s | `0.07173` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0484 |
| 2497 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:05 UTC | 5.0s | `0.07173` | `0.07176` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0478 |
| 2498 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:18 UTC | 18.9s | `0.07170` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0472 |
| 2499 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:36:49 UTC | 1m 49s | `0.07157` | `0.07154` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0466 |
| 2500 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:50:38 UTC | 2m 38s | `0.07157` | `0.07147` | $1.43 | $0.02 | $0.000000 | **+0.0020** | `+10.5%` | `MIN_PROFIT_TP_HIT` | $99.0486 |
| 2501 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:01 UTC | 1.5s | `0.07133` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0480 |
| 2502 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:02 UTC | 2.2s | `0.07128` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0474 |
| 2503 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:09:02 UTC | 2.2s | `0.07127` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0468 |
| 2504 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:16:00 UTC | 0.8s | `0.07142` | `0.07145` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.2%` | `STOP_LOSS_HIT` | $99.0462 |
| 2505 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:10 UTC | 10.2s | `0.07154` | `0.07157` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0456 |
| 2506 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:09 UTC | 9.7s | `0.07167` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0450 |
| 2507 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:00 UTC | 0.4s | `0.07162` | `0.07159` | $1.43 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0444 |
| 2508 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:02 UTC | 2.4s | `0.07186` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0438 |
| 2509 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:00 UTC | 0.5s | `0.07201` | `0.07198` | $1.44 | $0.02 | $0.000000 | **-0.0006** | `-3.1%` | `STOP_LOSS_HIT` | $99.0432 |

> 💡 *Full granular dataset with all 2509 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
