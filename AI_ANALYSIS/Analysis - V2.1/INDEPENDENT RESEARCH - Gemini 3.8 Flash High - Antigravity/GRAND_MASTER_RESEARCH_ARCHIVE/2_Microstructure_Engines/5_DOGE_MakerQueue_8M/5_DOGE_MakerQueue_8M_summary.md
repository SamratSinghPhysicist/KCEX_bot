# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:50:51 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `110.4110 USDT` | `₹10,428.32` | `+10.41%` |
| **Net Realized PnL** | **`+10.4110 USDT`** | **`₹+983.32`** | **`+10.41% Net ROI`** |
| **Gross Profit** | `+20.7610 USDT` | `₹1,960.88` | Total positive trade returns |
| **Gross Loss** | `-10.3500 USDT` | `₹977.56` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`2.01`** | — | Exceptional (Institutional Grade) |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0184 USDT` | `₹1.74` | **`-0.02%` Peak-to-Trough** |
| **Win Rate** | **`44.52%`** | — | `20761 Wins / 25875 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `25.14` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `43.93` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `619.06` | — | Net ROI divided by Max Drawdown |

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
| **High-Fidelity Simulation** | `DISABLED (Candle OHLC)` | Millisecond-level trade order matching & stop triggering |
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
| **Total Trades Executed** | `46636` | Total completed trade lifecycle events |
| **Winning Trades** | `20761` | `44.52%` of total trades |
| **Losing Trades** | `25875` | `55.48%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0002 USDT` (`₹+0.02`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #155 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #152 (LONG) |
| **Max Consecutive Wins** | `17` trades | Peak winning streak |
| **Max Consecutive Losses** | `25` trades | Peak losing streak |
| **Average Trade Duration** | `1m 16s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `60.0s` | Trade #1 |
| **Longest Trade In-Position** | `30m 59s` | Trade #43891 |
| **Cumulative Time In Position** | `988h 17m 13s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `23082` (49.5%) | `23554` (50.5%) | `46636` |
| **Wins / Losses** | `10202 W / 12880 L` | `10559 W / 12995 L` | `20761 W / 25875 L` |
| **Win Rate** | **`44.20%`** | **`44.83%`** | **`44.52%`** |
| **Gross Profit** | `+10.2020 USDT` | `+10.5590 USDT` | `+20.7610 USDT` |
| **Gross Loss** | `-5.1520 USDT` | `-5.1980 USDT` | `-10.3500 USDT` |
| **Net Realized PnL** | **`+5.0500 USDT`** | **`+5.3610 USDT`** | **`+10.4110 USDT`** |
| **Net PnL (INR)** | `₹+476.97` | `₹+506.35` | `₹+983.32` |
| **Profit Factor** | `1.98` | `2.03` | `2.01` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `25875` | `55.5%` | `-10.3500 USDT` | `₹-977.56` | `0.0%` | `1m 15s` |
| `MIN_PROFIT_TP_HIT` | `20761` | `44.5%` | `+20.7610 USDT` | `₹+1,960.88` | `100.0%` | `1m 17s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:33:00 UTC | 2026-01-01 00:33:59 UTC | 60.0s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:41:00 UTC | 2026-01-01 00:41:59 UTC | 60.0s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:50:00 UTC | 2026-01-01 00:50:59 UTC | 60.0s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `LONG` | 2026-01-01 00:55:00 UTC | 2026-01-01 00:55:59 UTC | 60.0s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 5 | `LONG` | 2026-01-01 01:01:00 UTC | 2026-01-01 01:02:59 UTC | 1m 59s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 6 | `LONG` | 2026-01-01 01:06:00 UTC | 2026-01-01 01:06:59 UTC | 60.0s | `0.11797` | `0.11802` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 7 | `LONG` | 2026-01-01 01:14:00 UTC | 2026-01-01 01:14:59 UTC | 60.0s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0042 |
| 8 | `SHORT` | 2026-01-01 01:24:00 UTC | 2026-01-01 01:25:59 UTC | 1m 59s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 9 | `SHORT` | 2026-01-01 01:32:00 UTC | 2026-01-01 01:32:59 UTC | 60.0s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0048 |
| 10 | `LONG` | 2026-01-01 01:39:00 UTC | 2026-01-01 01:41:59 UTC | 2m 59s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0058 |
| 11 | `LONG` | 2026-01-01 01:44:00 UTC | 2026-01-01 01:44:59 UTC | 60.0s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0054 |
| 12 | `LONG` | 2026-01-01 01:56:00 UTC | 2026-01-01 01:56:59 UTC | 60.0s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0050 |
| 13 | `LONG` | 2026-01-01 01:59:00 UTC | 2026-01-01 01:59:59 UTC | 60.0s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0046 |
| 14 | `SHORT` | 2026-01-01 02:05:00 UTC | 2026-01-01 02:05:59 UTC | 60.0s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0042 |
| 15 | `LONG` | 2026-01-01 02:10:00 UTC | 2026-01-01 02:10:59 UTC | 60.0s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0038 |
| 16 | `SHORT` | 2026-01-01 02:16:00 UTC | 2026-01-01 02:16:59 UTC | 60.0s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0034 |
| 17 | `SHORT` | 2026-01-01 02:19:00 UTC | 2026-01-01 02:19:59 UTC | 60.0s | `0.11842` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 18 | `LONG` | 2026-01-01 02:27:00 UTC | 2026-01-01 02:27:59 UTC | 60.0s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0040 |
| 19 | `LONG` | 2026-01-01 02:36:00 UTC | 2026-01-01 02:36:59 UTC | 60.0s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0036 |
| 20 | `SHORT` | 2026-01-01 02:41:00 UTC | 2026-01-01 02:41:59 UTC | 60.0s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0046 |
| 21 | `SHORT` | 2026-01-01 02:48:00 UTC | 2026-01-01 02:49:59 UTC | 1m 59s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 22 | `SHORT` | 2026-01-01 03:04:00 UTC | 2026-01-01 03:04:59 UTC | 60.0s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0066 |
| 23 | `SHORT` | 2026-01-01 03:11:00 UTC | 2026-01-01 03:11:59 UTC | 60.0s | `0.11826` | `0.11821` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0076 |
| 24 | `LONG` | 2026-01-01 03:18:00 UTC | 2026-01-01 03:18:59 UTC | 60.0s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0072 |
| 25 | `LONG` | 2026-01-01 03:23:00 UTC | 2026-01-01 03:25:59 UTC | 2m 59s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0082 |
| ... | ... | *(46586 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 46612 | `SHORT` | 2026-08-30 20:47:00 UTC | 2026-08-30 20:47:59 UTC | 60.0s | `0.08503` | `0.08505` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4010 |
| 46613 | `LONG` | 2026-08-30 20:54:00 UTC | 2026-08-30 20:54:59 UTC | 60.0s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4006 |
| 46614 | `SHORT` | 2026-08-30 21:05:00 UTC | 2026-08-30 21:05:59 UTC | 60.0s | `0.08449` | `0.08444` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $110.4016 |
| 46615 | `LONG` | 2026-08-30 21:16:00 UTC | 2026-08-30 21:16:59 UTC | 60.0s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4012 |
| 46616 | `SHORT` | 2026-08-30 21:26:00 UTC | 2026-08-30 21:26:59 UTC | 60.0s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4008 |
| 46617 | `LONG` | 2026-08-30 21:37:00 UTC | 2026-08-30 21:37:59 UTC | 60.0s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4004 |
| 46618 | `SHORT` | 2026-08-30 21:46:00 UTC | 2026-08-30 21:46:59 UTC | 60.0s | `0.08438` | `0.08433` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $110.4014 |
| 46619 | `SHORT` | 2026-08-30 21:50:00 UTC | 2026-08-30 21:50:59 UTC | 60.0s | `0.08435` | `0.08430` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $110.4024 |
| 46620 | `LONG` | 2026-08-30 21:56:00 UTC | 2026-08-30 21:56:59 UTC | 60.0s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $110.4034 |
| 46621 | `LONG` | 2026-08-30 22:00:00 UTC | 2026-08-30 22:00:59 UTC | 60.0s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4030 |
| 46622 | `LONG` | 2026-08-30 22:06:00 UTC | 2026-08-30 22:06:59 UTC | 60.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4026 |
| 46623 | `SHORT` | 2026-08-30 22:14:00 UTC | 2026-08-30 22:14:59 UTC | 60.0s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4022 |
| 46624 | `SHORT` | 2026-08-30 22:20:00 UTC | 2026-08-30 22:20:59 UTC | 60.0s | `0.08424` | `0.08419` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4032 |
| 46625 | `LONG` | 2026-08-30 22:23:00 UTC | 2026-08-30 22:23:59 UTC | 60.0s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4042 |
| 46626 | `LONG` | 2026-08-30 22:36:00 UTC | 2026-08-30 22:36:59 UTC | 60.0s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4052 |
| 46627 | `LONG` | 2026-08-30 22:44:00 UTC | 2026-08-30 22:44:59 UTC | 60.0s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4048 |
| 46628 | `SHORT` | 2026-08-30 22:54:00 UTC | 2026-08-30 22:54:59 UTC | 60.0s | `0.08359` | `0.08354` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4058 |
| 46629 | `LONG` | 2026-08-30 23:01:00 UTC | 2026-08-30 23:01:59 UTC | 60.0s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4068 |
| 46630 | `LONG` | 2026-08-30 23:16:00 UTC | 2026-08-30 23:16:59 UTC | 60.0s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4064 |
| 46631 | `SHORT` | 2026-08-30 23:28:00 UTC | 2026-08-30 23:28:59 UTC | 60.0s | `0.08245` | `0.08240` | $1.65 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $110.4074 |
| 46632 | `SHORT` | 2026-08-30 23:32:00 UTC | 2026-08-30 23:32:59 UTC | 60.0s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $110.4084 |
| 46633 | `LONG` | 2026-08-30 23:37:00 UTC | 2026-08-30 23:37:59 UTC | 60.0s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $110.4094 |
| 46634 | `SHORT` | 2026-08-30 23:43:00 UTC | 2026-08-30 23:43:59 UTC | 60.0s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.4090 |
| 46635 | `SHORT` | 2026-08-30 23:51:00 UTC | 2026-08-30 23:51:59 UTC | 60.0s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $110.4100 |
| 46636 | `LONG` | 2026-08-30 23:55:00 UTC | 2026-08-30 23:55:59 UTC | 60.0s | `0.08179` | `0.08184` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $110.4110 |

> 💡 *Full granular dataset with all 46636 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
