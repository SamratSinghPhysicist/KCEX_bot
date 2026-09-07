# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 02:29:42 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `98.0496 USDT` | `₹9,260.78` | `-1.95%` |
| **Net Realized PnL** | **`-1.9504 USDT`** | **`₹-184.22`** | **`-1.95% Net ROI`** |
| **Gross Profit** | `+0.0920 USDT` | `₹8.69` | Total positive trade returns |
| **Gross Loss** | `-2.0424 USDT` | `₹192.90` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.05`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-1.9504 USDT` | `₹184.22` | **`-1.95%` Peak-to-Trough** |
| **Win Rate** | **`1.77%`** | — | `46 Wins / 2553 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-158.28` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-72.96` | — | Downside risk-adjusted return ratio |
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
| **Slippage Tolerance** | `2 ticks` (`0.00002 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Total Trades Executed** | `2599` | Total completed trade lifecycle events |
| **Winning Trades** | `46` | `1.77%` of total trades |
| **Losing Trades** | `2553` | `98.23%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0008 USDT` (`₹-0.07`) | Expected return per signal |
| **Average Winning Trade** | `+0.0020 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0008 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0020 USDT (+10.4% ROE)` | Trade #17 (LONG) |
| **Largest Losing Trade** | `-0.0008 USDT (-4.2% ROE)` | Trade #6 (LONG) |
| **Max Consecutive Wins** | `3` trades | Peak winning streak |
| **Max Consecutive Losses** | `242` trades | Peak losing streak |
| **Average Trade Duration** | `5.9s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #1 |
| **Longest Trade In-Position** | `9m 44s` | Trade #2007 |
| **Cumulative Time In Position** | `4h 15m 35s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `1309` (50.4%) | `1290` (49.6%) | `2599` |
| **Wins / Losses** | `26 W / 1283 L` | `20 W / 1270 L` | `46 W / 2553 L` |
| **Win Rate** | **`1.99%`** | **`1.55%`** | **`1.77%`** |
| **Gross Profit** | `+0.0520 USDT` | `+0.0400 USDT` | `+0.0920 USDT` |
| **Gross Loss** | `-1.0264 USDT` | `-1.0160 USDT` | `-2.0424 USDT` |
| **Net Realized PnL** | **`-0.9744 USDT`** | **`-0.9760 USDT`** | **`-1.9504 USDT`** |
| **Net PnL (INR)** | `₹-92.03` | `₹-92.18` | `₹-184.22` |
| **Profit Factor** | `0.05` | `0.04` | `0.05` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `2553` | `98.2%` | `-2.0424 USDT` | `₹-192.90` | `0.0%` | `3.8s` |
| `MIN_PROFIT_TP_HIT` | `46` | `1.8%` | `+0.0920 USDT` | `₹+8.69` | `100.0%` | `2m 00s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-07-01 00:28:59 UTC | 2026-07-01 00:29:00 UTC | 0.1s | `0.07184` | `0.07180` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9992 |
| 2 | `SHORT` | 2026-07-01 00:35:59 UTC | 2026-07-01 00:36:00 UTC | 0.3s | `0.07184` | `0.07188` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9984 |
| 3 | `LONG` | 2026-07-01 00:44:59 UTC | 2026-07-01 00:45:00 UTC | 0.1s | `0.07171` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9976 |
| 4 | `SHORT` | 2026-07-01 00:54:59 UTC | 2026-07-01 00:55:00 UTC | 0.1s | `0.07173` | `0.07177` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9968 |
| 5 | `LONG` | 2026-07-01 01:08:59 UTC | 2026-07-01 01:09:00 UTC | 0.1s | `0.07138` | `0.07134` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9960 |
| 6 | `LONG` | 2026-07-01 01:14:59 UTC | 2026-07-01 01:15:00 UTC | 0.1s | `0.07104` | `0.07100` | $1.42 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9952 |
| 7 | `SHORT` | 2026-07-01 01:18:59 UTC | 2026-07-01 01:19:00 UTC | 0.3s | `0.07110` | `0.07114` | $1.42 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9944 |
| 8 | `SHORT` | 2026-07-01 01:22:59 UTC | 2026-07-01 01:23:05 UTC | 5.5s | `0.07124` | `0.07128` | $1.42 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9936 |
| 9 | `SHORT` | 2026-07-01 01:32:59 UTC | 2026-07-01 01:33:11 UTC | 11.9s | `0.07136` | `0.07140` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9928 |
| 10 | `SHORT` | 2026-07-01 01:43:59 UTC | 2026-07-01 01:44:00 UTC | 0.3s | `0.07187` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9920 |
| 11 | `LONG` | 2026-07-01 01:52:59 UTC | 2026-07-01 01:53:00 UTC | 0.4s | `0.07186` | `0.07182` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9912 |
| 12 | `SHORT` | 2026-07-01 01:58:59 UTC | 2026-07-01 01:59:00 UTC | 0.9s | `0.07182` | `0.07186` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9904 |
| 13 | `LONG` | 2026-07-01 02:03:59 UTC | 2026-07-01 02:04:01 UTC | 1.1s | `0.07196` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9896 |
| 14 | `LONG` | 2026-07-01 02:09:59 UTC | 2026-07-01 02:10:00 UTC | 0.1s | `0.07178` | `0.07174` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9888 |
| 15 | `SHORT` | 2026-07-01 02:18:59 UTC | 2026-07-01 02:19:00 UTC | 0.2s | `0.07200` | `0.07204` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9880 |
| 16 | `SHORT` | 2026-07-01 02:25:59 UTC | 2026-07-01 02:26:00 UTC | 0.6s | `0.07208` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9872 |
| 17 | `LONG` | 2026-07-01 02:29:59 UTC | 2026-07-01 02:31:07 UTC | 1m 07s | `0.07211` | `0.07221` | $1.44 | $0.02 | $0.000000 | **+0.0020** | `+10.4%` | `MIN_PROFIT_TP_HIT` | $99.9892 |
| 18 | `LONG` | 2026-07-01 02:35:59 UTC | 2026-07-01 02:36:00 UTC | 0.2s | `0.07216` | `0.07212` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9884 |
| 19 | `SHORT` | 2026-07-01 02:47:59 UTC | 2026-07-01 02:48:00 UTC | 0.6s | `0.07189` | `0.07193` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9876 |
| 20 | `LONG` | 2026-07-01 02:51:59 UTC | 2026-07-01 02:52:00 UTC | 0.3s | `0.07196` | `0.07192` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9868 |
| 21 | `SHORT` | 2026-07-01 02:58:59 UTC | 2026-07-01 02:59:01 UTC | 1.1s | `0.07193` | `0.07197` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9860 |
| 22 | `SHORT` | 2026-07-01 03:09:59 UTC | 2026-07-01 03:10:00 UTC | 0.4s | `0.07207` | `0.07211` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9852 |
| 23 | `LONG` | 2026-07-01 03:19:59 UTC | 2026-07-01 03:20:00 UTC | 0.2s | `0.07188` | `0.07184` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9844 |
| 24 | `LONG` | 2026-07-01 03:23:59 UTC | 2026-07-01 03:24:00 UTC | 0.8s | `0.07194` | `0.07190` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9836 |
| 25 | `SHORT` | 2026-07-01 03:27:59 UTC | 2026-07-01 03:28:00 UTC | 1.0s | `0.07187` | `0.07191` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $99.9828 |
| ... | ... | *(2549 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2575 | `LONG` | 2026-07-13 21:09:59 UTC | 2026-07-13 21:10:00 UTC | 0.4s | `0.07165` | `0.07161` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0688 |
| 2576 | `LONG` | 2026-07-13 21:13:59 UTC | 2026-07-13 21:14:00 UTC | 0.3s | `0.07154` | `0.07150` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0680 |
| 2577 | `SHORT` | 2026-07-13 21:24:59 UTC | 2026-07-13 21:25:00 UTC | 0.1s | `0.07162` | `0.07166` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0672 |
| 2578 | `LONG` | 2026-07-13 21:31:59 UTC | 2026-07-13 21:32:03 UTC | 3.1s | `0.07142` | `0.07138` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0664 |
| 2579 | `LONG` | 2026-07-13 21:41:59 UTC | 2026-07-13 21:42:00 UTC | 0.4s | `0.07122` | `0.07118` | $1.42 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0656 |
| 2580 | `LONG` | 2026-07-13 21:44:59 UTC | 2026-07-13 21:45:00 UTC | 0.4s | `0.07129` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0648 |
| 2581 | `SHORT` | 2026-07-13 21:50:59 UTC | 2026-07-13 21:51:00 UTC | 0.4s | `0.07124` | `0.07128` | $1.42 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0640 |
| 2582 | `SHORT` | 2026-07-13 21:56:59 UTC | 2026-07-13 21:57:05 UTC | 5.0s | `0.07140` | `0.07144` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0632 |
| 2583 | `SHORT` | 2026-07-13 22:00:59 UTC | 2026-07-13 22:01:01 UTC | 1.4s | `0.07151` | `0.07155` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0624 |
| 2584 | `SHORT` | 2026-07-13 22:04:59 UTC | 2026-07-13 22:05:00 UTC | 0.7s | `0.07158` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0616 |
| 2585 | `LONG` | 2026-07-13 22:12:59 UTC | 2026-07-13 22:13:14 UTC | 15.0s | `0.07166` | `0.07162` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0608 |
| 2586 | `LONG` | 2026-07-13 22:16:59 UTC | 2026-07-13 22:17:00 UTC | 0.4s | `0.07174` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0600 |
| 2587 | `SHORT` | 2026-07-13 22:22:59 UTC | 2026-07-13 22:23:01 UTC | 1.1s | `0.07172` | `0.07176` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0592 |
| 2588 | `LONG` | 2026-07-13 22:27:59 UTC | 2026-07-13 22:28:00 UTC | 0.4s | `0.07171` | `0.07167` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0584 |
| 2589 | `LONG` | 2026-07-13 22:34:59 UTC | 2026-07-13 22:35:00 UTC | 0.4s | `0.07158` | `0.07154` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0576 |
| 2590 | `SHORT` | 2026-07-13 22:47:59 UTC | 2026-07-13 22:48:09 UTC | 9.3s | `0.07156` | `0.07160` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0568 |
| 2591 | `LONG` | 2026-07-13 22:59:59 UTC | 2026-07-13 23:00:00 UTC | 0.1s | `0.07134` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0560 |
| 2592 | `LONG` | 2026-07-13 23:03:59 UTC | 2026-07-13 23:04:02 UTC | 2.2s | `0.07129` | `0.07125` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0552 |
| 2593 | `SHORT` | 2026-07-13 23:08:59 UTC | 2026-07-13 23:09:02 UTC | 2.1s | `0.07126` | `0.07130` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0544 |
| 2594 | `SHORT` | 2026-07-13 23:15:59 UTC | 2026-07-13 23:16:00 UTC | 0.7s | `0.07141` | `0.07145` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0536 |
| 2595 | `SHORT` | 2026-07-13 23:20:59 UTC | 2026-07-13 23:21:00 UTC | 1.0s | `0.07153` | `0.07157` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0528 |
| 2596 | `SHORT` | 2026-07-13 23:25:59 UTC | 2026-07-13 23:26:00 UTC | 0.3s | `0.07166` | `0.07170` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0520 |
| 2597 | `LONG` | 2026-07-13 23:33:59 UTC | 2026-07-13 23:34:00 UTC | 0.3s | `0.07163` | `0.07159` | $1.43 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0512 |
| 2598 | `SHORT` | 2026-07-13 23:50:59 UTC | 2026-07-13 23:51:00 UTC | 0.3s | `0.07185` | `0.07189` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0504 |
| 2599 | `LONG` | 2026-07-14 00:00:59 UTC | 2026-07-14 00:01:00 UTC | 0.5s | `0.07202` | `0.07198` | $1.44 | $0.02 | $0.000000 | **-0.0008** | `-4.2%` | `STOP_LOSS_HIT` | $98.0496 |

> 💡 *Full granular dataset with all 2599 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
