# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 14:02:36 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `97.0008 USDT` | `₹9,161.73` | `-3.00%` |
| **Net Realized PnL** | **`-2.9992 USDT`** | **`₹-283.27`** | **`-3.00% Net ROI`** |
| **Gross Profit** | `+14.8788 USDT` | `₹1,405.30` | Total positive trade returns |
| **Gross Loss** | `-17.8780 USDT` | `₹1,688.58` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.83`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `0.20` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-3.0268 USDT` | `₹285.88` | **`-3.03%` Peak-to-Trough** |
| **Win Rate** | **`80.62%`** | — | `37197 Wins / 8939 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-5.31` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-2.52` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.99` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `DOGE_USDT` | Base Asset: `DOGE` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-01-01` → `2026-08-31` | Historical evaluation window |
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
| **Take Profit Target** | `+2 ticks` (`+0.00002 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-25.0% ROE on committed margin` | Stop loss evaluation logic |

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
| **Total Trades Executed** | `46136` | Total completed trade lifecycle events |
| **Winning Trades** | `37197` | `80.62%` of total trades |
| **Losing Trades** | `8939` | `19.38%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0001 USDT` (`₹-0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0020 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+1.2% ROE)` | Trade #152 (LONG) |
| **Largest Losing Trade** | `-0.0020 USDT (-6.0% ROE)` | Trade #159 (LONG) |
| **Max Consecutive Wins** | `53` trades | Peak winning streak |
| **Max Consecutive Losses** | `8` trades | Peak losing streak |
| **Average Trade Duration** | `55.1s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #72 |
| **Longest Trade In-Position** | `1h 24m 48s` | Trade #43742 |
| **Cumulative Time In Position** | `706h 27m 56s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `22858` (49.5%) | `23278` (50.5%) | `46136` |
| **Wins / Losses** | `18393 W / 4465 L` | `18804 W / 4474 L` | `37197 W / 8939 L` |
| **Win Rate** | **`80.47%`** | **`80.78%`** | **`80.62%`** |
| **Gross Profit** | `+7.3572 USDT` | `+7.5216 USDT` | `+14.8788 USDT` |
| **Gross Loss** | `-8.9300 USDT` | `-8.9480 USDT` | `-17.8780 USDT` |
| **Net Realized PnL** | **`-1.5728 USDT`** | **`-1.4264 USDT`** | **`-2.9992 USDT`** |
| **Net PnL (INR)** | `₹-148.55` | `₹-134.72` | `₹-283.27` |
| **Profit Factor** | `0.82` | `0.84` | `0.83` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `37197` | `80.6%` | `+14.8788 USDT` | `₹+1,405.30` | `100.0%` | `41.2s` |
| `STOP_LOSS_HIT` | `8939` | `19.4%` | `-17.8780 USDT` | `₹-1,688.58` | `0.0%` | `1m 53s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:35:10 UTC | 2m 10s | `0.11787` | `0.11789` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:55 UTC | 55.4s | `0.11778` | `0.11776` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:02 UTC | 2.3s | `0.11775` | `0.11773` | $2.35 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:38 UTC | 38.1s | `0.11782` | `0.11784` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 5 | `LONG` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:01:18 UTC | 18.7s | `0.11788` | `0.11790` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 6 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:20 UTC | 20.9s | `0.11797` | `0.11799` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 7 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:05 UTC | 5.2s | `0.11838` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 8 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:22 UTC | 1m 22s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 9 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:33:47 UTC | 1m 47s | `0.11814` | `0.11812` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 10 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:01 UTC | 1.2s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 11 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:47:33 UTC | 3m 33s | `0.11831` | `0.11833` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 12 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:45 UTC | 45.2s | `0.11856` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 13 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 02:00:01 UTC | 1m 01s | `0.11849` | `0.11851` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 14 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:09:14 UTC | 4m 14s | `0.11847` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 15 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:40 UTC | 40.5s | `0.11830` | `0.11828` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0060 |
| 16 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:11 UTC | 11.6s | `0.11842` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0064 |
| 17 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:30:06 UTC | 3m 06s | `0.11839` | `0.11841` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0068 |
| 18 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:37:55 UTC | 1m 55s | `0.11854` | `0.11856` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0072 |
| 19 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:09 UTC | 9.2s | `0.11863` | `0.11861` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0076 |
| 20 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:26 UTC | 1m 26s | `0.11855` | `0.11853` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0080 |
| 21 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:22 UTC | 22.1s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0084 |
| 22 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:23 UTC | 23.7s | `0.11826` | `0.11824` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0088 |
| 23 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:14 UTC | 14.3s | `0.11822` | `0.11824` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0092 |
| 24 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:02 UTC | 2m 02s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0096 |
| 25 | `LONG` | 2026-01-01 03:30:59 UTC | 2026-01-01 03:31:30 UTC | 30.1s | `0.11843` | `0.11833` | $2.37 | $0.03 | $0.000000 | **-0.0020** | `-6.3%` | `STOP_LOSS_HIT` | $100.0076 |
| ... | ... | *(46086 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 46112 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:01 UTC | 1.1s | `0.08459` | `0.08461` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9984 |
| 46113 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:01 UTC | 1.3s | `0.08460` | `0.08462` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9988 |
| 46114 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:23 UTC | 23.5s | `0.08446` | `0.08444` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9992 |
| 46115 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:38:39 UTC | 1m 39s | `0.08480` | `0.08470` | $1.70 | $0.02 | $0.000000 | **-0.0020** | `-8.8%` | `STOP_LOSS_HIT` | $96.9972 |
| 46116 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:09 UTC | 9.4s | `0.08438` | `0.08436` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9976 |
| 46117 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:10 UTC | 10.0s | `0.08435` | `0.08433` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9980 |
| 46118 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:04 UTC | 4.6s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9984 |
| 46119 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:00 UTC | 0.2s | `0.08458` | `0.08460` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9988 |
| 46120 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:08:10 UTC | 2m 10s | `0.08465` | `0.08455` | $1.69 | $0.02 | $0.000000 | **-0.0020** | `-8.9%` | `STOP_LOSS_HIT` | $96.9968 |
| 46121 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:15:09 UTC | 1m 09s | `0.08423` | `0.08421` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9972 |
| 46122 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:00 UTC | 0.9s | `0.08424` | `0.08422` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9976 |
| 46123 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:04 UTC | 4.0s | `0.08385` | `0.08387` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9980 |
| 46124 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:00 UTC | 0.5s | `0.08371` | `0.08369` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9984 |
| 46125 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:00 UTC | 0.4s | `0.08358` | `0.08360` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9988 |
| 46126 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:45:15 UTC | 1m 15s | `0.08370` | `0.08372` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9992 |
| 46127 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:18 UTC | 18.8s | `0.08359` | `0.08357` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9996 |
| 46128 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:08 UTC | 8.9s | `0.08339` | `0.08341` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $97.0000 |
| 46129 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:17:05 UTC | 1m 05s | `0.08333` | `0.08323` | $1.67 | $0.02 | $0.000000 | **-0.0020** | `-9.0%` | `STOP_LOSS_HIT` | $96.9980 |
| 46130 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:05 UTC | 5.6s | `0.08245` | `0.08243` | $1.65 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9984 |
| 46131 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:00 UTC | 0.6s | `0.08215` | `0.08213` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9988 |
| 46132 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.1s | `0.08197` | `0.08199` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9992 |
| 46133 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.8s | `0.08150` | `0.08148` | $1.63 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $96.9996 |
| 46134 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:00 UTC | 0.8s | `0.08156` | `0.08154` | $1.63 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $97.0000 |
| 46135 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:05 UTC | 5.4s | `0.08179` | `0.08181` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $97.0004 |
| 46136 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.8s | `0.08182` | `0.08184` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $97.0008 |

> 💡 *Full granular dataset with all 46136 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
