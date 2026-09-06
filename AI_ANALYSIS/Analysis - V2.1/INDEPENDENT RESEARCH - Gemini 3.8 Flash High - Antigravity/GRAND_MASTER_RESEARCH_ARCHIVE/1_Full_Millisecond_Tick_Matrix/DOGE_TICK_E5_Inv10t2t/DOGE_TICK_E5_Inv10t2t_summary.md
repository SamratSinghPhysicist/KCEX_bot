# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:53:57 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `102.5708 USDT` | `₹9,687.81` | `+2.57%` |
| **Net Realized PnL** | **`+2.5708 USDT`** | **`₹+242.81`** | **`+2.57% Net ROI`** |
| **Gross Profit** | `+17.5340 USDT` | `₹1,656.09` | Total positive trade returns |
| **Gross Loss** | `-14.9632 USDT` | `₹1,413.27` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.17`** | — | Profitable |
| **Win / Loss Payoff** | `5.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0600 USDT` | `₹5.67` | **`-0.06%` Peak-to-Trough** |
| **Win Rate** | **`18.99%`** | — | `8767 Wins / 37408 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `4.61` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `10.86` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `43.96` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `46175` | Total completed trade lifecycle events |
| **Winning Trades** | `8767` | `18.99%` of total trades |
| **Losing Trades** | `37408` | `81.01%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0001 USDT` (`₹+0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0020 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0020 USDT (+6.0% ROE)` | Trade #160 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #138 (LONG) |
| **Max Consecutive Wins** | `6` trades | Peak winning streak |
| **Max Consecutive Losses** | `44` trades | Peak losing streak |
| **Average Trade Duration** | `56.1s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #99 |
| **Longest Trade In-Position** | `1h 10m 45s` | Trade #43789 |
| **Cumulative Time In Position** | `719h 41m 21s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `22890` (49.6%) | `23285` (50.4%) | `46175` |
| **Wins / Losses** | `4408 W / 18482 L` | `4359 W / 18926 L` | `8767 W / 37408 L` |
| **Win Rate** | **`19.26%`** | **`18.72%`** | **`18.99%`** |
| **Gross Profit** | `+8.8160 USDT` | `+8.7180 USDT` | `+17.5340 USDT` |
| **Gross Loss** | `-7.3928 USDT` | `-7.5704 USDT` | `-14.9632 USDT` |
| **Net Realized PnL** | **`+1.4232 USDT`** | **`+1.1476 USDT`** | **`+2.5708 USDT`** |
| **Net PnL (INR)** | `₹+134.42` | `₹+108.39` | `₹+242.81` |
| **Profit Factor** | `1.19` | `1.15` | `1.17` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `37408` | `81.0%` | `-14.9632 USDT` | `₹-1,413.27` | `0.0%` | `42.4s` |
| `MIN_PROFIT_TP_HIT` | `8767` | `19.0%` | `+17.5340 USDT` | `₹+1,656.09` | `100.0%` | `1m 54s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:35 UTC | 35.1s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:00 UTC | 0.7s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:18 UTC | 18.5s | `0.11775` | `0.11777` | $2.35 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 01:01:21 UTC | 6m 21s | `0.11782` | `0.11792` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 5 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:02 UTC | 2.8s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0004 |
| 6 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:16:50 UTC | 2m 50s | `0.11838` | `0.11836` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0000 |
| 7 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:26:17 UTC | 2m 17s | `0.11822` | `0.11812` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 8 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:00 UTC | 0.7s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 9 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:41:52 UTC | 2m 52s | `0.11817` | `0.11827` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 10 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:03 UTC | 3.2s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0032 |
| 11 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:25 UTC | 25.8s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0028 |
| 12 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:16 UTC | 16.7s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 13 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:06 UTC | 6.9s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0020 |
| 14 | `LONG` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:04 UTC | 4.2s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 15 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:04 UTC | 5.0s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0012 |
| 16 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:16 UTC | 16.5s | `0.11842` | `0.11844` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0008 |
| 17 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:01 UTC | 1.3s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0004 |
| 18 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:00 UTC | 0.7s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0000 |
| 19 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:43:22 UTC | 2m 22s | `0.11863` | `0.11853` | $2.37 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 20 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:50:30 UTC | 2m 30s | `0.11855` | `0.11857` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 21 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:05:18 UTC | 1m 18s | `0.11850` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 22 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:00 UTC | 0.9s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0032 |
| 23 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:05 UTC | 5.9s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0028 |
| 24 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:01 UTC | 2m 01s | `0.11817` | `0.11815` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 25 | `LONG` | 2026-01-01 03:30:59 UTC | 2026-01-01 03:31:24 UTC | 24.3s | `0.11843` | `0.11841` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0020 |
| ... | ... | *(46125 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 46151 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:40 UTC | 40.1s | `0.08459` | `0.08469` | $1.69 | $0.02 | $0.000000 | **+0.0020** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $102.5684 |
| 46152 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:10 UTC | 10.2s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5680 |
| 46153 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:00 UTC | 0.8s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5676 |
| 46154 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:09 UTC | 9.5s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5672 |
| 46155 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:16 UTC | 17.0s | `0.08438` | `0.08440` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5668 |
| 46156 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:05 UTC | 5.2s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5664 |
| 46157 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:57:02 UTC | 1m 02s | `0.08446` | `0.08444` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5660 |
| 46158 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:01 UTC | 1.0s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5656 |
| 46159 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:06 UTC | 7.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5652 |
| 46160 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:01 UTC | 1.6s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5648 |
| 46161 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:06 UTC | 6.6s | `0.08424` | `0.08426` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5644 |
| 46162 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:25 UTC | 25.4s | `0.08385` | `0.08395` | $1.68 | $0.02 | $0.000000 | **+0.0020** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $102.5664 |
| 46163 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:08 UTC | 8.9s | `0.08371` | `0.08361` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $102.5684 |
| 46164 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:25 UTC | 25.9s | `0.08358` | `0.08356` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5680 |
| 46165 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:01 UTC | 1.1s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5676 |
| 46166 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:06 UTC | 6.9s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5672 |
| 46167 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:41 UTC | 41.4s | `0.08339` | `0.08349` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $102.5692 |
| 46168 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:02 UTC | 2.7s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5688 |
| 46169 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:00 UTC | 0.4s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5684 |
| 46170 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:01 UTC | 1.1s | `0.08215` | `0.08205` | $1.64 | $0.02 | $0.000000 | **+0.0020** | `+9.1%` | `MIN_PROFIT_TP_HIT` | $102.5704 |
| 46171 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:05 UTC | 6.0s | `0.08197` | `0.08195` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5700 |
| 46172 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:04 UTC | 4.6s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5696 |
| 46173 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:05 UTC | 5.6s | `0.08156` | `0.08146` | $1.63 | $0.02 | $0.000000 | **+0.0020** | `+9.2%` | `MIN_PROFIT_TP_HIT` | $102.5716 |
| 46174 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:00 UTC | 0.9s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5712 |
| 46175 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.9s | `0.08182` | `0.08180` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $102.5708 |

> 💡 *Full granular dataset with all 46175 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
