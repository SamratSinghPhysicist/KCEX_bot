# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 14:02:21 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0652 USDT` | `₹9,451.16` | `+0.07%` |
| **Net Realized PnL** | **`+0.0652 USDT`** | **`₹+6.16`** | **`+0.07% Net ROI`** |
| **Gross Profit** | `+9.7188 USDT` | `₹917.94` | Total positive trade returns |
| **Gross Loss** | `-9.6536 USDT` | `₹911.78` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.01`** | — | Profitable |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.2132 USDT` | `₹20.14` | **`-0.21%` Peak-to-Trough** |
| **Win Rate** | **`50.17%`** | — | `24297 Wins / 24134 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `0.26` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `0.26` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `0.31` | — | Net ROI divided by Max Drawdown |

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
| **Signal Inversion Mode** | `DISABLED (Direct)` | Signal execution orientation |

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
| **Total Trades Executed** | `48431` | Total completed trade lifecycle events |
| **Winning Trades** | `24297` | `50.17%` of total trades |
| **Losing Trades** | `24134` | `49.83%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+1.2% ROE)` | Trade #155 (SHORT) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #158 (SHORT) |
| **Max Consecutive Wins** | `16` trades | Peak winning streak |
| **Max Consecutive Losses** | `14` trades | Peak losing streak |
| **Average Trade Duration** | `12.8s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #74 |
| **Longest Trade In-Position** | `15m 17s` | Trade #45535 |
| **Cumulative Time In Position** | `172h 29m 08s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `24464` (50.5%) | `23967` (49.5%) | `48431` |
| **Wins / Losses** | `12455 W / 12009 L` | `11842 W / 12125 L` | `24297 W / 24134 L` |
| **Win Rate** | **`50.91%`** | **`49.41%`** | **`50.17%`** |
| **Gross Profit** | `+4.9820 USDT` | `+4.7368 USDT` | `+9.7188 USDT` |
| **Gross Loss** | `-4.8036 USDT` | `-4.8500 USDT` | `-9.6536 USDT` |
| **Net Realized PnL** | **`+0.1784 USDT`** | **`-0.1132 USDT`** | **`+0.0652 USDT`** |
| **Net PnL (INR)** | `₹+16.85` | `₹-10.69` | `₹+6.16` |
| **Profit Factor** | `1.04` | `0.98` | `1.01` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `24297` | `50.2%` | `+9.7188 USDT` | `₹+917.94` | `100.0%` | `12.8s` |
| `STOP_LOSS_HIT` | `24134` | `49.8%` | `-9.6536 USDT` | `₹-911.78` | `0.0%` | `12.8s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:35 UTC | 35.1s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `LONG` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:00 UTC | 0.7s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:02 UTC | 2.3s | `0.11775` | `0.11773` | $2.35 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0004 |
| 4 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:38 UTC | 38.1s | `0.11782` | `0.11784` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0000 |
| 5 | `SHORT` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:01:18 UTC | 18.7s | `0.11788` | `0.11790` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 6 | `SHORT` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:02 UTC | 2.8s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 7 | `SHORT` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:05 UTC | 5.2s | `0.11838` | `0.11840` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 8 | `LONG` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:22 UTC | 1m 22s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 9 | `LONG` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:00 UTC | 0.7s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 10 | `SHORT` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:01 UTC | 1.2s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 11 | `SHORT` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:03 UTC | 3.2s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 12 | `SHORT` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:25 UTC | 25.8s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 13 | `SHORT` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:16 UTC | 16.7s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 14 | `LONG` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:06 UTC | 6.9s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 15 | `SHORT` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:04 UTC | 4.2s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 16 | `LONG` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:04 UTC | 5.0s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 17 | `LONG` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:11 UTC | 11.6s | `0.11842` | `0.11840` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0012 |
| 18 | `SHORT` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:01 UTC | 1.3s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 19 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:00 UTC | 0.7s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 20 | `LONG` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:09 UTC | 9.2s | `0.11863` | `0.11861` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 21 | `LONG` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:26 UTC | 1m 26s | `0.11855` | `0.11853` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0012 |
| 22 | `LONG` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:22 UTC | 22.1s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0008 |
| 23 | `LONG` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:00 UTC | 0.9s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 24 | `SHORT` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:05 UTC | 5.9s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 25 | `SHORT` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:01 UTC | 2m 01s | `0.11817` | `0.11815` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| ... | ... | *(48381 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 48407 | `SHORT` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:01 UTC | 1.1s | `0.08459` | `0.08461` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0668 |
| 48408 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:01 UTC | 1.3s | `0.08460` | `0.08462` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0664 |
| 48409 | `LONG` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:00 UTC | 0.8s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0668 |
| 48410 | `SHORT` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:09 UTC | 9.5s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0672 |
| 48411 | `LONG` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:09 UTC | 9.4s | `0.08438` | `0.08436` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0668 |
| 48412 | `LONG` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:05 UTC | 5.2s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0672 |
| 48413 | `SHORT` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:04 UTC | 4.6s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0668 |
| 48414 | `SHORT` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:00 UTC | 0.2s | `0.08458` | `0.08460` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0664 |
| 48415 | `SHORT` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:06 UTC | 7.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0668 |
| 48416 | `LONG` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:01 UTC | 1.6s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0672 |
| 48417 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:00 UTC | 0.9s | `0.08424` | `0.08422` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0668 |
| 48418 | `SHORT` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:04 UTC | 4.0s | `0.08385` | `0.08387` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0664 |
| 48419 | `LONG` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:00 UTC | 0.5s | `0.08371` | `0.08369` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0660 |
| 48420 | `SHORT` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:00 UTC | 0.4s | `0.08358` | `0.08360` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0656 |
| 48421 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:01 UTC | 1.1s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0660 |
| 48422 | `LONG` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:06 UTC | 6.9s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0664 |
| 48423 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:08 UTC | 8.9s | `0.08339` | `0.08341` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0660 |
| 48424 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:02 UTC | 2.7s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0664 |
| 48425 | `LONG` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:00 UTC | 0.4s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0668 |
| 48426 | `LONG` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:00 UTC | 0.6s | `0.08215` | `0.08213` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0664 |
| 48427 | `SHORT` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.1s | `0.08197` | `0.08199` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0660 |
| 48428 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.8s | `0.08150` | `0.08148` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0656 |
| 48429 | `LONG` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:00 UTC | 0.8s | `0.08156` | `0.08154` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0652 |
| 48430 | `SHORT` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:00 UTC | 0.9s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0656 |
| 48431 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.8s | `0.08182` | `0.08184` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0652 |

> 💡 *Full granular dataset with all 48431 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
