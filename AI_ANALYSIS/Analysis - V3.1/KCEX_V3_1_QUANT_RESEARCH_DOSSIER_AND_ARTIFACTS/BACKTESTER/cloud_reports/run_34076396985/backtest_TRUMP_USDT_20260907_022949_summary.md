# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-07 02:29:49 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.3644 USDT` | `₹9,384.97` | `-0.64%` |
| **Net Realized PnL** | **`-0.6356 USDT`** | **`₹-60.03`** | **`-0.64% Net ROI`** |
| **Gross Profit** | `+0.2560 USDT` | `₹24.18` | Total positive trade returns |
| **Gross Loss** | `-0.8916 USDT` | `₹84.21` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.29`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `2.38` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.6388 USDT` | `₹60.33` | **`-0.64%` Peak-to-Trough** |
| **Win Rate** | **`10.75%`** | — | `160 Wins / 1328 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-42.59` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-43.71` | — | Downside risk-adjusted return ratio |
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
| **Total Trades Executed** | `1488` | Total completed trade lifecycle events |
| **Winning Trades** | `160` | `10.75%` of total trades |
| **Losing Trades** | `1328` | `89.25%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0016 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0007 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0016 USDT (+36.1% ROE)` | Trade #1 (LONG) |
| **Largest Losing Trade** | `-0.0010 USDT (-22.0% ROE)` | Trade #17 (SHORT) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `50` trades | Peak losing streak |
| **Average Trade Duration** | `6m 33s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #1002 |
| **Longest Trade In-Position** | `2h 30m 09s` | Trade #1433 |
| **Cumulative Time In Position** | `162h 36m 27s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `716` (48.1%) | `772` (51.9%) | `1488` |
| **Wins / Losses** | `77 W / 639 L` | `83 W / 689 L` | `160 W / 1328 L` |
| **Win Rate** | **`10.75%`** | **`10.75%`** | **`10.75%`** |
| **Gross Profit** | `+0.1232 USDT` | `+0.1328 USDT` | `+0.2560 USDT` |
| **Gross Loss** | `-0.4242 USDT` | `-0.4674 USDT` | `-0.8916 USDT` |
| **Net Realized PnL** | **`-0.3010 USDT`** | **`-0.3346 USDT`** | **`-0.6356 USDT`** |
| **Net PnL (INR)** | `₹-28.43` | `₹-31.60` | `₹-60.03` |
| **Profit Factor** | `0.29` | `0.28` | `0.29` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `160` | `10.8%` | `+0.2560 USDT` | `₹+24.18` | `100.0%` | `12m 06s` |
| `STOP_LOSS_HIT` | `705` | `47.4%` | `-0.7050 USDT` | `₹-66.59` | `0.0%` | `3m 39s` |
| `RATCHET_TIGHTEN_HIT` | `310` | `20.8%` | `-0.1240 USDT` | `₹-11.71` | `0.0%` | `6m 07s` |
| `RATCHET_BREAKEVEN_HIT` | `313` | `21.0%` | `-0.0626 USDT` | `₹-5.91` | `0.0%` | `10m 40s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:34:39 UTC | 5m 39s | `1.662` | `1.670` | $0.33 | $0.00 | $0.000000 | **+0.0016** | `+36.1%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 2 | `SHORT` | 2026-07-01 00:36:59 UTC | 2026-07-01 00:46:07 UTC | 9m 07s | `1.663` | `1.668` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.5%` | `STOP_LOSS_HIT` | $100.0006 |
| 3 | `SHORT` | 2026-07-01 00:55:59 UTC | 2026-07-01 01:02:09 UTC | 6m 09s | `1.668` | `1.670` | $0.33 | $0.00 | $0.000000 | **-0.0004** | `-9.0%` | `RATCHET_TIGHTEN_HIT` | $100.0002 |
| 4 | `LONG` | 2026-07-01 01:09:59 UTC | 2026-07-01 01:10:40 UTC | 40.7s | `1.662` | `1.657` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9992 |
| 5 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:16:20 UTC | 1m 20s | `1.646` | `1.645` | $0.33 | $0.00 | $0.000000 | **-0.0002** | `-4.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9990 |
| 6 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:26:58 UTC | 3m 58s | `1.657` | `1.658` | $0.33 | $0.00 | $0.000000 | **-0.0002** | `-4.5%` | `RATCHET_BREAKEVEN_HIT` | $99.9988 |
| 7 | `SHORT` | 2026-07-01 01:34:59 UTC | 2026-07-01 01:35:33 UTC | 33.8s | `1.657` | `1.662` | $0.33 | $0.00 | $0.000000 | **-0.0010** | `-22.6%` | `STOP_LOSS_HIT` | $99.9978 |
| 8 | `SHORT` | 2026-07-01 01:47:59 UTC | 2026-07-01 01:51:51 UTC | 3m 51s | `1.675` | `1.677` | $0.34 | $0.00 | $0.000000 | **-0.0004** | `-9.0%` | `RATCHET_TIGHTEN_HIT` | $99.9974 |
| 9 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 02:03:45 UTC | 10m 45s | `1.677` | `1.685` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.8%` | `MIN_PROFIT_TP_HIT` | $99.9990 |
| 10 | `LONG` | 2026-07-01 02:08:59 UTC | 2026-07-01 02:11:33 UTC | 2m 33s | `1.685` | `1.693` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.6%` | `MIN_PROFIT_TP_HIT` | $100.0006 |
| 11 | `SHORT` | 2026-07-01 02:17:59 UTC | 2026-07-01 02:18:17 UTC | 17.5s | `1.701` | `1.706` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9996 |
| 12 | `LONG` | 2026-07-01 02:22:59 UTC | 2026-07-01 02:23:00 UTC | 0.9s | `1.710` | `1.705` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9986 |
| 13 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:31:28 UTC | 1m 28s | `1.706` | `1.705` | $0.34 | $0.00 | $0.000000 | **-0.0002** | `-4.4%` | `RATCHET_BREAKEVEN_HIT` | $99.9984 |
| 14 | `LONG` | 2026-07-01 02:34:59 UTC | 2026-07-01 02:36:09 UTC | 1m 09s | `1.705` | `1.703` | $0.34 | $0.00 | $0.000000 | **-0.0004** | `-8.8%` | `RATCHET_TIGHTEN_HIT` | $99.9980 |
| 15 | `LONG` | 2026-07-01 02:40:59 UTC | 2026-07-01 02:45:29 UTC | 4m 29s | `1.698` | `1.697` | $0.34 | $0.00 | $0.000000 | **-0.0002** | `-4.4%` | `RATCHET_BREAKEVEN_HIT` | $99.9978 |
| 16 | `SHORT` | 2026-07-01 03:00:59 UTC | 2026-07-01 03:01:33 UTC | 33.3s | `1.703` | `1.708` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9968 |
| 17 | `SHORT` | 2026-07-01 03:04:59 UTC | 2026-07-01 03:05:07 UTC | 7.4s | `1.706` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9958 |
| 18 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:11:13 UTC | 1m 13s | `1.728` | `1.720` | $0.35 | $0.00 | $0.000000 | **+0.0016** | `+34.7%` | `MIN_PROFIT_TP_HIT` | $99.9974 |
| 19 | `LONG` | 2026-07-01 03:15:59 UTC | 2026-07-01 03:16:00 UTC | 0.7s | `1.712` | `1.707` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-21.9%` | `STOP_LOSS_HIT` | $99.9964 |
| 20 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:11 UTC | 11.2s | `1.705` | `1.700` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9954 |
| 21 | `LONG` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:30:30 UTC | 2m 30s | `1.700` | `1.698` | $0.34 | $0.00 | $0.000000 | **-0.0004** | `-8.8%` | `RATCHET_TIGHTEN_HIT` | $99.9950 |
| 22 | `SHORT` | 2026-07-01 03:32:59 UTC | 2026-07-01 03:36:33 UTC | 3m 33s | `1.698` | `1.703` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.1%` | `STOP_LOSS_HIT` | $99.9940 |
| 23 | `SHORT` | 2026-07-01 03:41:59 UTC | 2026-07-01 03:46:24 UTC | 4m 24s | `1.705` | `1.710` | $0.34 | $0.00 | $0.000000 | **-0.0010** | `-22.0%` | `STOP_LOSS_HIT` | $99.9930 |
| 24 | `LONG` | 2026-07-01 03:51:59 UTC | 2026-07-01 03:52:33 UTC | 33.1s | `1.712` | `1.711` | $0.34 | $0.00 | $0.000000 | **-0.0002** | `-4.4%` | `RATCHET_BREAKEVEN_HIT` | $99.9928 |
| 25 | `SHORT` | 2026-07-01 03:56:59 UTC | 2026-07-01 04:03:10 UTC | 6m 10s | `1.711` | `1.703` | $0.34 | $0.00 | $0.000000 | **+0.0016** | `+35.1%` | `MIN_PROFIT_TP_HIT` | $99.9944 |
| ... | ... | *(1438 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1464 | `LONG` | 2026-07-13 17:57:59 UTC | 2026-07-13 17:58:59 UTC | 59.1s | `1.524` | `1.522` | $0.30 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3744 |
| 1465 | `LONG` | 2026-07-13 18:01:59 UTC | 2026-07-13 18:10:04 UTC | 8m 04s | `1.522` | `1.521` | $0.30 | $0.00 | $0.000000 | **-0.0002** | `-4.9%` | `RATCHET_BREAKEVEN_HIT` | $99.3742 |
| 1466 | `LONG` | 2026-07-13 18:14:59 UTC | 2026-07-13 18:19:02 UTC | 4m 02s | `1.523` | `1.521` | $0.30 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3738 |
| 1467 | `SHORT` | 2026-07-13 18:27:59 UTC | 2026-07-13 18:32:06 UTC | 4m 06s | `1.523` | `1.525` | $0.30 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3734 |
| 1468 | `LONG` | 2026-07-13 18:36:59 UTC | 2026-07-13 18:37:27 UTC | 27.2s | `1.524` | `1.519` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.3724 |
| 1469 | `SHORT` | 2026-07-13 18:46:59 UTC | 2026-07-13 18:49:38 UTC | 2m 38s | `1.525` | `1.530` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.3714 |
| 1470 | `SHORT` | 2026-07-13 18:53:59 UTC | 2026-07-13 19:04:56 UTC | 10m 56s | `1.527` | `1.528` | $0.31 | $0.00 | $0.000000 | **-0.0002** | `-4.9%` | `RATCHET_BREAKEVEN_HIT` | $99.3712 |
| 1471 | `SHORT` | 2026-07-13 19:07:59 UTC | 2026-07-13 19:24:34 UTC | 16m 34s | `1.525` | `1.527` | $0.30 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3708 |
| 1472 | `SHORT` | 2026-07-13 19:29:59 UTC | 2026-07-13 19:31:45 UTC | 1m 45s | `1.525` | `1.530` | $0.30 | $0.00 | $0.000000 | **-0.0010** | `-24.6%` | `STOP_LOSS_HIT` | $99.3698 |
| 1473 | `SHORT` | 2026-07-13 19:36:59 UTC | 2026-07-13 19:44:10 UTC | 7m 10s | `1.531` | `1.536` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.3688 |
| 1474 | `SHORT` | 2026-07-13 19:47:59 UTC | 2026-07-13 19:50:00 UTC | 2m 00s | `1.533` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.3678 |
| 1475 | `LONG` | 2026-07-13 19:51:59 UTC | 2026-07-13 20:15:09 UTC | 23m 09s | `1.537` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.3668 |
| 1476 | `LONG` | 2026-07-13 20:22:59 UTC | 2026-07-13 20:44:04 UTC | 21m 04s | `1.533` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0002** | `-4.9%` | `RATCHET_BREAKEVEN_HIT` | $99.3666 |
| 1477 | `LONG` | 2026-07-13 20:47:59 UTC | 2026-07-13 21:00:13 UTC | 12m 13s | `1.533` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0002** | `-4.9%` | `RATCHET_BREAKEVEN_HIT` | $99.3664 |
| 1478 | `SHORT` | 2026-07-13 21:01:59 UTC | 2026-07-13 21:14:09 UTC | 12m 09s | `1.532` | `1.534` | $0.31 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3660 |
| 1479 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:38:10 UTC | 13m 10s | `1.533` | `1.525` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.1%` | `MIN_PROFIT_TP_HIT` | $99.3676 |
| 1480 | `LONG` | 2026-07-13 21:43:59 UTC | 2026-07-13 21:59:46 UTC | 15m 46s | `1.524` | `1.522` | $0.30 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3672 |
| 1481 | `SHORT` | 2026-07-13 22:05:59 UTC | 2026-07-13 22:07:30 UTC | 1m 30s | `1.531` | `1.533` | $0.31 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3668 |
| 1482 | `LONG` | 2026-07-13 22:13:59 UTC | 2026-07-13 22:17:31 UTC | 3m 31s | `1.533` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0002** | `-4.9%` | `RATCHET_BREAKEVEN_HIT` | $99.3666 |
| 1483 | `SHORT` | 2026-07-13 22:20:59 UTC | 2026-07-13 22:28:04 UTC | 7m 04s | `1.535` | `1.537` | $0.31 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3662 |
| 1484 | `LONG` | 2026-07-13 22:36:59 UTC | 2026-07-13 22:51:25 UTC | 14m 25s | `1.534` | `1.532` | $0.31 | $0.00 | $0.000000 | **-0.0004** | `-9.8%` | `RATCHET_TIGHTEN_HIT` | $99.3658 |
| 1485 | `LONG` | 2026-07-13 22:56:59 UTC | 2026-07-13 23:00:49 UTC | 3m 49s | `1.535` | `1.530` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.4%` | `STOP_LOSS_HIT` | $99.3648 |
| 1486 | `SHORT` | 2026-07-13 23:13:59 UTC | 2026-07-13 23:18:28 UTC | 4m 28s | `1.530` | `1.535` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.3638 |
| 1487 | `SHORT` | 2026-07-13 23:23:59 UTC | 2026-07-13 23:24:15 UTC | 15.1s | `1.533` | `1.538` | $0.31 | $0.00 | $0.000000 | **-0.0010** | `-24.5%` | `STOP_LOSS_HIT` | $99.3628 |
| 1488 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-14 00:01:08 UTC | 27m 08s | `1.538` | `1.546` | $0.31 | $0.00 | $0.000000 | **+0.0016** | `+39.0%` | `MIN_PROFIT_TP_HIT` | $99.3644 |

> 💡 *Full granular dataset with all 1488 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
