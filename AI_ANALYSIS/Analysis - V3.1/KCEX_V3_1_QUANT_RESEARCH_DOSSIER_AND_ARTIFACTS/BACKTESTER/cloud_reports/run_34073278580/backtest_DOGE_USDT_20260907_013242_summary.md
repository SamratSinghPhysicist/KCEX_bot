# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 01:32:42 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0596 USDT` | `₹9,450.63` | `+0.06%` |
| **Net Realized PnL** | **`+0.0596 USDT`** | **`₹+5.63`** | **`+0.06% Net ROI`** |
| **Gross Profit** | `+0.6410 USDT` | `₹60.54` | Total positive trade returns |
| **Gross Loss** | `-0.5814 USDT` | `₹54.91` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.10`** | — | Profitable |
| **Win / Loss Payoff** | `2.71` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0186 USDT` | `₹1.76` | **`-0.02%` Peak-to-Trough** |
| **Win Rate** | **`24.69%`** | — | `641 Wins / 1578 Losses / 377 Scratch` |
| **Sharpe Ratio (est)** | `3.10` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `4.75` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `3.20` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `2596` | Total completed trade lifecycle events |
| **Winning Trades** | `641` | `24.69%` of total trades |
| **Losing Trades** | `1578` | `60.79%` of total trades |
| **Scratch / Break-even** | `377` | `14.52%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+5.3% ROE)` | Trade #8 (SHORT) |
| **Largest Losing Trade** | `-0.0004 USDT (-2.1% ROE)` | Trade #2 (SHORT) |
| **Max Consecutive Wins** | `6` trades | Peak winning streak |
| **Max Consecutive Losses** | `14` trades | Peak losing streak |
| **Average Trade Duration** | `29.6s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #120 |
| **Longest Trade In-Position** | `6m 42s` | Trade #2175 |
| **Cumulative Time In Position** | `21h 22m 38s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1305` (50.3%) | `1291` (49.7%) | `2596` |
| **Wins / Losses** | `333 W / 794 L` | `308 W / 784 L` | `641 W / 1578 L` |
| **Win Rate** | **`25.52%`** | **`23.86%`** | **`24.69%`** |
| **Gross Profit** | `+0.3330 USDT` | `+0.3080 USDT` | `+0.6410 USDT` |
| **Gross Loss** | `-0.2910 USDT` | `-0.2904 USDT` | `-0.5814 USDT` |
| **Net Realized PnL** | **`+0.0420 USDT`** | **`+0.0176 USDT`** | **`+0.0596 USDT`** |
| **Net PnL (INR)** | `₹+3.97` | `₹+1.66` | `₹+5.63` |
| **Profit Factor** | `1.14` | `1.06` | `1.10` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `1329` | `51.2%` | `-0.5316 USDT` | `₹-50.21` | `0.0%` | `14.7s` |
| `RATCHET_BREAKEVEN_HIT` | `377` | `14.5%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `52.7s` |
| `MIN_PROFIT_TP_HIT` | `641` | `24.7%` | `+0.6410 USDT` | `₹+60.54` | `100.0%` | `41.9s` |
| `RATCHET_TIGHTEN_HIT` | `249` | `9.6%` | `-0.0498 USDT` | `₹-4.70` | `0.0%` | `43.2s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:06 UTC | 6.3s | `0.07182` | `0.07180` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:36:05 UTC | 5.6s | `0.07186` | `0.07188` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:45:03 UTC | 3.9s | `0.07169` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:04 UTC | 4.1s | `0.07175` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9984 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:10:11 UTC | 1m 11s | `0.07136` | `0.07136` | $1.43 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9984 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:00 UTC | 0.7s | `0.07102` | `0.07107` | $1.42 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $99.9994 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:00 UTC | 0.6s | `0.07112` | `0.07114` | $1.42 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9990 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:01 UTC | 1.8s | `0.07126` | `0.07121` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:02 UTC | 2.7s | `0.07138` | `0.07133` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0010 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:01 UTC | 1.0s | `0.07189` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0006 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:00 UTC | 1.0s | `0.07184` | `0.07182` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0002 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:05 UTC | 5.0s | `0.07184` | `0.07186` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:06 UTC | 6.9s | `0.07194` | `0.07194` | $1.44 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9998 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:10:08 UTC | 8.6s | `0.07176` | `0.07176` | $1.44 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9998 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:02 UTC | 2.9s | `0.07202` | `0.07204` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:21 UTC | 21.9s | `0.07210` | `0.07210` | $1.44 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $99.9994 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:30:13 UTC | 13.2s | `0.07209` | `0.07214` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 18 | `LONG` | 2026-07-01 02:31:59 UTC | 2026-07-01 02:32:09 UTC | 9.5s | `0.07206` | `0.07206` | $1.44 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $100.0004 |
| 19 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:01 UTC | 1.2s | `0.07214` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 20 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:13 UTC | 13.2s | `0.07191` | `0.07186` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0010 |
| 21 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:05 UTC | 5.9s | `0.07194` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0006 |
| 22 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 02:59:09 UTC | 9.9s | `0.07195` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0002 |
| 23 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:05 UTC | 5.0s | `0.07209` | `0.07204` | $1.44 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 24 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:09 UTC | 9.5s | `0.07186` | `0.07184` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 25 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:24:24 UTC | 24.8s | `0.07192` | `0.07190` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0004 |
| ... | ... | *(2546 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2572 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:14 UTC | 14.8s | `0.07163` | `0.07163` | $1.43 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $100.0610 |
| 2573 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:03 UTC | 3.5s | `0.07152` | `0.07157` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0620 |
| 2574 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:02 UTC | 2.2s | `0.07164` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0616 |
| 2575 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:09 UTC | 9.3s | `0.07140` | `0.07138` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0612 |
| 2576 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:43:24 UTC | 1m 24s | `0.07120` | `0.07120` | $1.42 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $100.0612 |
| 2577 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:01 UTC | 1.0s | `0.07127` | `0.07132` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0622 |
| 2578 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:51:43 UTC | 44.0s | `0.07126` | `0.07128` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0618 |
| 2579 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:20 UTC | 20.8s | `0.07142` | `0.07144` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0614 |
| 2580 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:05 UTC | 5.3s | `0.07153` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0610 |
| 2581 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:00 UTC | 0.8s | `0.07160` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0606 |
| 2582 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:13:14 UTC | 15.0s | `0.07164` | `0.07164` | $1.43 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $100.0606 |
| 2583 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:17:10 UTC | 10.1s | `0.07172` | `0.07177` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0616 |
| 2584 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:55 UTC | 55.9s | `0.07174` | `0.07169` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0626 |
| 2585 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:38 UTC | 38.2s | `0.07169` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0622 |
| 2586 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:36:09 UTC | 1m 09s | `0.07156` | `0.07156` | $1.43 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `RATCHET_BREAKEVEN_HIT` | $100.0622 |
| 2587 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:49:21 UTC | 1m 21s | `0.07158` | `0.07153` | $1.43 | $0.02 | $0.000000 | **+0.0010** | `+5.2%` | `MIN_PROFIT_TP_HIT` | $100.0632 |
| 2588 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:03 UTC | 3.2s | `0.07132` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0628 |
| 2589 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:02 UTC | 2.3s | `0.07127` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0624 |
| 2590 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:09:12 UTC | 12.0s | `0.07128` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0620 |
| 2591 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:16:37 UTC | 37.2s | `0.07143` | `0.07145` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0616 |
| 2592 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:11 UTC | 11.8s | `0.07155` | `0.07157` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0612 |
| 2593 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:18 UTC | 18.2s | `0.07168` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0608 |
| 2594 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:00 UTC | 0.7s | `0.07161` | `0.07159` | $1.43 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0604 |
| 2595 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:03 UTC | 3.1s | `0.07187` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0600 |
| 2596 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:00 UTC | 0.9s | `0.07200` | `0.07198` | $1.44 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0596 |

> 💡 *Full granular dataset with all 2596 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
