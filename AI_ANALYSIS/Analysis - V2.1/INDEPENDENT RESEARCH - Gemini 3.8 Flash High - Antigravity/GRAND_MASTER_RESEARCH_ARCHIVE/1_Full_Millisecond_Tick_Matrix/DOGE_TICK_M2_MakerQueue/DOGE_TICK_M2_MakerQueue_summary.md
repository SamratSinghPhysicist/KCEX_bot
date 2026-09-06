# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 14:19:13 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `97.6860 USDT` | `₹9,226.44` | `-2.31%` |
| **Net Realized PnL** | **`-2.3140 USDT`** | **`₹-218.56`** | **`-2.31% Net ROI`** |
| **Gross Profit** | `+9.8380 USDT` | `₹929.20` | Total positive trade returns |
| **Gross Loss** | `-12.1520 USDT` | `₹1,147.76` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.81`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-2.3200 USDT` | `₹219.12` | **`-2.32%` Peak-to-Trough** |
| **Win Rate** | **`24.46%`** | — | `9838 Wins / 30380 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-7.43` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-11.18` | — | Downside risk-adjusted return ratio |
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
| **Total Trades Executed** | `40218` | Total completed trade lifecycle events |
| **Winning Trades** | `9838` | `24.46%` of total trades |
| **Losing Trades** | `30380` | `75.54%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0001 USDT` (`₹-0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #142 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #125 (LONG) |
| **Max Consecutive Wins** | `10` trades | Peak winning streak |
| **Max Consecutive Losses** | `34` trades | Peak losing streak |
| **Average Trade Duration** | `24.2s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #18 |
| **Longest Trade In-Position** | `26m 55s` | Trade #37776 |
| **Cumulative Time In Position** | `269h 48m 49s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `19765` (49.1%) | `20453` (50.9%) | `40218` |
| **Wins / Losses** | `4852 W / 14913 L` | `4986 W / 15467 L` | `9838 W / 30380 L` |
| **Win Rate** | **`24.55%`** | **`24.38%`** | **`24.46%`** |
| **Gross Profit** | `+4.8520 USDT` | `+4.9860 USDT` | `+9.8380 USDT` |
| **Gross Loss** | `-5.9652 USDT` | `-6.1868 USDT` | `-12.1520 USDT` |
| **Net Realized PnL** | **`-1.1132 USDT`** | **`-1.2008 USDT`** | **`-2.3140 USDT`** |
| **Net PnL (INR)** | `₹-105.14` | `₹-113.42` | `₹-218.56` |
| **Profit Factor** | `0.81` | `0.81` | `0.81` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `30380` | `75.5%` | `-12.1520 USDT` | `₹-1,147.76` | `0.0%` | `17.9s` |
| `MIN_PROFIT_TP_HIT` | `9838` | `24.5%` | `+9.8380 USDT` | `₹+929.20` | `100.0%` | `43.4s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:33:02 UTC | 2026-01-01 00:33:35 UTC | 32.8s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:41:00 UTC | 2026-01-01 00:41:00 UTC | 0.4s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:50:00 UTC | 2026-01-01 00:50:08 UTC | 8.6s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `LONG` | 2026-01-01 00:55:00 UTC | 2026-01-01 00:55:38 UTC | 37.9s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 5 | `LONG` | 2026-01-01 01:01:01 UTC | 2026-01-01 01:02:05 UTC | 1m 03s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 6 | `LONG` | 2026-01-01 01:06:02 UTC | 2026-01-01 01:06:02 UTC | 0.5s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0018 |
| 7 | `LONG` | 2026-01-01 01:14:00 UTC | 2026-01-01 01:14:49 UTC | 48.6s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 8 | `SHORT` | 2026-01-01 01:24:00 UTC | 2026-01-01 01:25:49 UTC | 1m 48s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 9 | `SHORT` | 2026-01-01 01:32:00 UTC | 2026-01-01 01:32:00 UTC | 0.7s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0034 |
| 10 | `LONG` | 2026-01-01 01:44:01 UTC | 2026-01-01 01:44:03 UTC | 1.7s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0030 |
| 11 | `LONG` | 2026-01-01 01:56:00 UTC | 2026-01-01 01:56:25 UTC | 25.3s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0026 |
| 12 | `LONG` | 2026-01-01 01:59:01 UTC | 2026-01-01 01:59:16 UTC | 14.8s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0022 |
| 13 | `SHORT` | 2026-01-01 02:05:02 UTC | 2026-01-01 02:05:06 UTC | 4.4s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0018 |
| 14 | `LONG` | 2026-01-01 02:10:02 UTC | 2026-01-01 02:10:04 UTC | 1.2s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0014 |
| 15 | `SHORT` | 2026-01-01 02:16:00 UTC | 2026-01-01 02:16:04 UTC | 4.9s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0010 |
| 16 | `SHORT` | 2026-01-01 02:19:00 UTC | 2026-01-01 02:19:16 UTC | 15.6s | `0.11842` | `0.11844` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0006 |
| 17 | `LONG` | 2026-01-01 02:27:00 UTC | 2026-01-01 02:27:01 UTC | 0.9s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0002 |
| 18 | `LONG` | 2026-01-01 02:36:00 UTC | 2026-01-01 02:36:00 UTC | 0.1s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9998 |
| 19 | `SHORT` | 2026-01-01 02:41:06 UTC | 2026-01-01 02:41:16 UTC | 10.0s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 20 | `SHORT` | 2026-01-01 02:48:07 UTC | 2026-01-01 02:49:28 UTC | 1m 21s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 21 | `SHORT` | 2026-01-01 03:04:01 UTC | 2026-01-01 03:04:40 UTC | 39.0s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 22 | `SHORT` | 2026-01-01 03:11:00 UTC | 2026-01-01 03:11:00 UTC | 0.2s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 23 | `LONG` | 2026-01-01 03:18:01 UTC | 2026-01-01 03:18:05 UTC | 4.8s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0020 |
| 24 | `LONG` | 2026-01-01 03:23:00 UTC | 2026-01-01 03:25:01 UTC | 2m 00s | `0.11817` | `0.11815` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 25 | `LONG` | 2026-01-01 03:31:02 UTC | 2026-01-01 03:31:24 UTC | 22.1s | `0.11843` | `0.11841` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0012 |
| ... | ... | *(40168 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 40194 | `SHORT` | 2026-08-30 20:47:00 UTC | 2026-08-30 20:47:08 UTC | 7.8s | `0.08503` | `0.08505` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6886 |
| 40195 | `LONG` | 2026-08-30 20:54:00 UTC | 2026-08-30 20:54:00 UTC | 0.2s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6882 |
| 40196 | `SHORT` | 2026-08-30 21:05:00 UTC | 2026-08-30 21:05:01 UTC | 1.2s | `0.08449` | `0.08451` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6878 |
| 40197 | `LONG` | 2026-08-30 21:16:07 UTC | 2026-08-30 21:16:10 UTC | 2.8s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6874 |
| 40198 | `SHORT` | 2026-08-30 21:26:00 UTC | 2026-08-30 21:26:00 UTC | 0.2s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6870 |
| 40199 | `LONG` | 2026-08-30 21:37:03 UTC | 2026-08-30 21:37:09 UTC | 6.5s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6866 |
| 40200 | `SHORT` | 2026-08-30 21:46:00 UTC | 2026-08-30 21:46:16 UTC | 16.4s | `0.08438` | `0.08440` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6862 |
| 40201 | `SHORT` | 2026-08-30 21:50:01 UTC | 2026-08-30 21:50:05 UTC | 3.7s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6858 |
| 40202 | `LONG` | 2026-08-30 21:56:00 UTC | 2026-08-30 21:56:15 UTC | 14.9s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $97.6868 |
| 40203 | `LONG` | 2026-08-30 22:00:00 UTC | 2026-08-30 22:00:01 UTC | 0.9s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6864 |
| 40204 | `LONG` | 2026-08-30 22:06:02 UTC | 2026-08-30 22:06:06 UTC | 4.7s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6860 |
| 40205 | `SHORT` | 2026-08-30 22:14:01 UTC | 2026-08-30 22:14:01 UTC | 0.5s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6856 |
| 40206 | `SHORT` | 2026-08-30 22:20:06 UTC | 2026-08-30 22:20:06 UTC | 0.4s | `0.08424` | `0.08426` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6852 |
| 40207 | `LONG` | 2026-08-30 22:23:00 UTC | 2026-08-30 22:23:10 UTC | 10.5s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $97.6862 |
| 40208 | `LONG` | 2026-08-30 22:44:00 UTC | 2026-08-30 22:44:01 UTC | 0.2s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6858 |
| 40209 | `SHORT` | 2026-08-30 22:54:06 UTC | 2026-08-30 22:54:06 UTC | 0.1s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6854 |
| 40210 | `LONG` | 2026-08-30 23:01:00 UTC | 2026-08-30 23:01:15 UTC | 15.1s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $97.6864 |
| 40211 | `LONG` | 2026-08-30 23:16:00 UTC | 2026-08-30 23:16:02 UTC | 2.6s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6860 |
| 40212 | `SHORT` | 2026-08-30 23:28:00 UTC | 2026-08-30 23:28:00 UTC | 0.1s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6856 |
| 40213 | `SHORT` | 2026-08-30 23:32:00 UTC | 2026-08-30 23:32:01 UTC | 1.0s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $97.6866 |
| 40214 | `LONG` | 2026-08-30 23:37:02 UTC | 2026-08-30 23:37:05 UTC | 3.4s | `0.08197` | `0.08195` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6862 |
| 40215 | `SHORT` | 2026-08-30 23:43:00 UTC | 2026-08-30 23:43:04 UTC | 4.6s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6858 |
| 40216 | `SHORT` | 2026-08-30 23:51:00 UTC | 2026-08-30 23:51:03 UTC | 3.2s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $97.6868 |
| 40217 | `LONG` | 2026-08-30 23:55:00 UTC | 2026-08-30 23:55:00 UTC | 0.2s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6864 |
| 40218 | `LONG` | 2026-08-31 00:01:00 UTC | 2026-08-31 00:01:00 UTC | 0.1s | `0.08182` | `0.08180` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $97.6860 |

> 💡 *Full granular dataset with all 40218 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
