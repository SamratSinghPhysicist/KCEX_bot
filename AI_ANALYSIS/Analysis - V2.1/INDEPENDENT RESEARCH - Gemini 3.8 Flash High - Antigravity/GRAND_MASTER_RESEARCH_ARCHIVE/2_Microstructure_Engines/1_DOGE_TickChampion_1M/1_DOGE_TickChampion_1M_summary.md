# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:47:51 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0930 USDT` | `₹9,453.78` | `+0.09%` |
| **Net Realized PnL** | **`+0.0930 USDT`** | **`₹+8.78`** | **`+0.09% Net ROI`** |
| **Gross Profit** | `+1.6610 USDT` | `₹156.88` | Total positive trade returns |
| **Gross Loss** | `-1.5680 USDT` | `₹148.10` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.06`** | — | Profitable |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0212 USDT` | `₹2.00` | **`-0.02%` Peak-to-Trough** |
| **Win Rate** | **`29.76%`** | — | `1661 Wins / 3920 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `2.02` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `3.24` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `4.39` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `DOGE_USDT` | Base Asset: `DOGE` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-08-01` → `2026-08-31` | Historical evaluation window |
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
| **Total Trades Executed** | `5581` | Total completed trade lifecycle events |
| **Winning Trades** | `1661` | `29.76%` of total trades |
| **Losing Trades** | `3920` | `70.24%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+5.4% ROE)` | Trade #10 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-2.2% ROE)` | Trade #1 (SHORT) |
| **Max Consecutive Wins** | `8` trades | Peak winning streak |
| **Max Consecutive Losses** | `19` trades | Peak losing streak |
| **Average Trade Duration** | `1m 13s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #100 |
| **Longest Trade In-Position** | `30m 12s` | Trade #2782 |
| **Cumulative Time In Position** | `113h 36m 43s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `2759` (49.4%) | `2822` (50.6%) | `5581` |
| **Wins / Losses** | `790 W / 1969 L` | `871 W / 1951 L` | `1661 W / 3920 L` |
| **Win Rate** | **`28.63%`** | **`30.86%`** | **`29.76%`** |
| **Gross Profit** | `+0.7900 USDT` | `+0.8710 USDT` | `+1.6610 USDT` |
| **Gross Loss** | `-0.7876 USDT` | `-0.7804 USDT` | `-1.5680 USDT` |
| **Net Realized PnL** | **`+0.0024 USDT`** | **`+0.0906 USDT`** | **`+0.0930 USDT`** |
| **Net PnL (INR)** | `₹+0.23` | `₹+8.56` | `₹+8.78` |
| **Profit Factor** | `1.00` | `1.12` | `1.06` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `3920` | `70.2%` | `-1.5680 USDT` | `₹-148.10` | `0.0%` | `58.8s` |
| `MIN_PROFIT_TP_HIT` | `1661` | `29.8%` | `+1.6610 USDT` | `₹+156.88` | `100.0%` | `1m 47s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-08-01 00:27:59 UTC | 2026-08-01 00:28:28 UTC | 28.9s | `0.06964` | `0.06966` | $1.39 | $0.02 | $0.000000 | **-0.0004** | `-2.2%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `LONG` | 2026-08-01 00:31:59 UTC | 2026-08-01 00:32:13 UTC | 13.6s | `0.06963` | `0.06961` | $1.39 | $0.02 | $0.000000 | **-0.0004** | `-2.2%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `LONG` | 2026-08-01 00:40:59 UTC | 2026-08-01 00:44:00 UTC | 3m 00s | `0.06983` | `0.06988` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.4%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `SHORT` | 2026-08-01 00:50:59 UTC | 2026-08-01 00:52:43 UTC | 1m 43s | `0.06988` | `0.06990` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 5 | `SHORT` | 2026-08-01 01:00:59 UTC | 2026-08-01 01:01:00 UTC | 0.5s | `0.06999` | `0.07001` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9994 |
| 6 | `LONG` | 2026-08-01 01:06:59 UTC | 2026-08-01 01:07:10 UTC | 10.5s | `0.07000` | `0.07005` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.4%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 7 | `SHORT` | 2026-08-01 01:12:59 UTC | 2026-08-01 01:17:22 UTC | 4m 22s | `0.07009` | `0.07011` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 8 | `SHORT` | 2026-08-01 01:21:59 UTC | 2026-08-01 01:22:34 UTC | 34.6s | `0.07004` | `0.07006` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 9 | `SHORT` | 2026-08-01 01:30:59 UTC | 2026-08-01 01:31:22 UTC | 22.1s | `0.07014` | `0.07016` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 10 | `LONG` | 2026-08-01 01:34:59 UTC | 2026-08-01 01:37:57 UTC | 2m 57s | `0.07007` | `0.07012` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.4%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 11 | `SHORT` | 2026-08-01 01:38:59 UTC | 2026-08-01 01:39:01 UTC | 1.7s | `0.07006` | `0.07008` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9998 |
| 12 | `SHORT` | 2026-08-01 01:49:59 UTC | 2026-08-01 01:50:38 UTC | 38.7s | `0.07007` | `0.07002` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.4%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 13 | `SHORT` | 2026-08-01 01:53:59 UTC | 2026-08-01 01:54:57 UTC | 57.8s | `0.07008` | `0.07010` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 14 | `LONG` | 2026-08-01 02:03:59 UTC | 2026-08-01 02:04:19 UTC | 19.4s | `0.07012` | `0.07010` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 15 | `SHORT` | 2026-08-01 02:11:59 UTC | 2026-08-01 02:12:25 UTC | 25.3s | `0.07008` | `0.07010` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 16 | `LONG` | 2026-08-01 02:17:59 UTC | 2026-08-01 02:18:55 UTC | 55.3s | `0.07015` | `0.07020` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0006 |
| 17 | `LONG` | 2026-08-01 02:23:59 UTC | 2026-08-01 02:24:35 UTC | 35.2s | `0.07021` | `0.07019` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0002 |
| 18 | `SHORT` | 2026-08-01 02:27:59 UTC | 2026-08-01 02:29:25 UTC | 1m 25s | `0.07023` | `0.07018` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 19 | `SHORT` | 2026-08-01 02:33:59 UTC | 2026-08-01 02:35:08 UTC | 1m 08s | `0.07014` | `0.07009` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.3%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 20 | `SHORT` | 2026-08-01 02:40:59 UTC | 2026-08-01 02:46:31 UTC | 5m 31s | `0.07001` | `0.07003` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0018 |
| 21 | `LONG` | 2026-08-01 02:50:59 UTC | 2026-08-01 02:53:11 UTC | 2m 11s | `0.07008` | `0.07006` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0014 |
| 22 | `LONG` | 2026-08-01 03:00:59 UTC | 2026-08-01 03:01:26 UTC | 26.2s | `0.07014` | `0.07012` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0010 |
| 23 | `SHORT` | 2026-08-01 03:08:59 UTC | 2026-08-01 03:09:08 UTC | 8.4s | `0.07012` | `0.07014` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0006 |
| 24 | `SHORT` | 2026-08-01 03:15:59 UTC | 2026-08-01 03:16:33 UTC | 33.1s | `0.07007` | `0.07009` | $1.40 | $0.02 | $0.000000 | **-0.0004** | `-2.1%` | `STOP_LOSS_HIT` | $100.0002 |
| 25 | `LONG` | 2026-08-01 03:21:59 UTC | 2026-08-01 03:22:31 UTC | 31.4s | `0.07006` | `0.07011` | $1.40 | $0.02 | $0.000000 | **+0.0010** | `+5.4%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| ... | ... | *(5531 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 5557 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:30 UTC | 30.7s | `0.08459` | `0.08464` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $100.0914 |
| 5558 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:10 UTC | 10.2s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0910 |
| 5559 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:00 UTC | 0.8s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0906 |
| 5560 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:09 UTC | 9.5s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0902 |
| 5561 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:16 UTC | 17.0s | `0.08438` | `0.08440` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0898 |
| 5562 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:05 UTC | 5.2s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0894 |
| 5563 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:15 UTC | 15.2s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $100.0904 |
| 5564 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:01 UTC | 1.0s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0900 |
| 5565 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:06 UTC | 7.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0896 |
| 5566 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:01 UTC | 1.6s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0892 |
| 5567 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:06 UTC | 6.6s | `0.08424` | `0.08426` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0888 |
| 5568 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:10 UTC | 10.7s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $100.0898 |
| 5569 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:06 UTC | 6.2s | `0.08371` | `0.08366` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $100.0908 |
| 5570 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:07 UTC | 7.1s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $100.0918 |
| 5571 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:01 UTC | 1.1s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0914 |
| 5572 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:06 UTC | 6.9s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0910 |
| 5573 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:15 UTC | 15.7s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 5574 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:02 UTC | 2.7s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0916 |
| 5575 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:00 UTC | 0.4s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0912 |
| 5576 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:01 UTC | 1.1s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $100.0922 |
| 5577 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.4s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $100.0932 |
| 5578 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:04 UTC | 4.6s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0928 |
| 5579 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:03 UTC | 3.3s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $100.0938 |
| 5580 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:00 UTC | 0.9s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0934 |
| 5581 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.9s | `0.08182` | `0.08180` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0930 |

> 💡 *Full granular dataset with all 5581 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
