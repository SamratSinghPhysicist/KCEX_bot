# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:05:31 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `99.0392 USDT` | `₹9,354.25` | `-0.96%` |
| **Net Realized PnL** | **`-0.9608 USDT`** | **`₹-90.75`** | **`-0.96% Net ROI`** |
| **Gross Profit** | `+15.2312 USDT` | `₹1,438.59` | Total positive trade returns |
| **Gross Loss** | `-16.1920 USDT` | `₹1,529.33` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.94`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `0.20` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-1.0988 USDT` | `₹103.78` | **`-1.10%` Peak-to-Trough** |
| **Win Rate** | **`82.46%`** | — | `38078 Wins / 8096 Losses / 1 Scratch` |
| **Sharpe Ratio (est)** | `-1.77` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-0.81` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `-0.87` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `46175` | Total completed trade lifecycle events |
| **Winning Trades** | `38078` | `82.46%` of total trades |
| **Losing Trades** | `8096` | `17.53%` of total trades |
| **Scratch / Break-even** | `1` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0000 USDT` (`₹-0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0020 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+1.2% ROE)` | Trade #138 (SHORT) |
| **Largest Losing Trade** | `-0.0020 USDT (-6.0% ROE)` | Trade #160 (SHORT) |
| **Max Consecutive Wins** | `44` trades | Peak winning streak |
| **Max Consecutive Losses** | `5` trades | Peak losing streak |
| **Average Trade Duration** | `1m 40s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #46175 |
| **Longest Trade In-Position** | `1h 11m 00s` | Trade #43789 |
| **Cumulative Time In Position** | `1289h 00m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `23285` (50.4%) | `22890` (49.6%) | `46175` |
| **Wins / Losses** | `19273 W / 4012 L` | `18805 W / 4084 L` | `38078 W / 8096 L` |
| **Win Rate** | **`82.77%`** | **`82.15%`** | **`82.46%`** |
| **Gross Profit** | `+7.7092 USDT` | `+7.5220 USDT` | `+15.2312 USDT` |
| **Gross Loss** | `-8.0240 USDT` | `-8.1680 USDT` | `-16.1920 USDT` |
| **Net Realized PnL** | **`-0.3148 USDT`** | **`-0.6460 USDT`** | **`-0.9608 USDT`** |
| **Net PnL (INR)** | `₹-29.73` | `₹-61.01` | `₹-90.75` |
| **Profit Factor** | `0.96` | `0.92` | `0.94` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `38078` | `82.5%` | `+15.2312 USDT` | `₹+1,438.59` | `100.0%` | `1m 28s` |
| `STOP_LOSS_HIT` | `8096` | `17.5%` | `-16.1920 USDT` | `₹-1,529.33` | `0.0%` | `2m 37s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:59 UTC | 1m 00s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `LONG` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:59 UTC | 1m 00s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `0.11775` | `0.11777` | $2.35 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 01:01:59 UTC | 7m 00s | `0.11782` | `0.11792` | $2.36 | $0.03 | $0.000000 | **-0.0020** | `-6.4%` | `STOP_LOSS_HIT` | $99.9992 |
| 5 | `SHORT` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:59 UTC | 1m 00s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 6 | `SHORT` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:16:59 UTC | 3m 00s | `0.11838` | `0.11836` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 7 | `LONG` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:26:59 UTC | 3m 00s | `0.11822` | `0.11812` | $2.36 | $0.03 | $0.000000 | **-0.0020** | `-6.3%` | `STOP_LOSS_HIT` | $99.9980 |
| 8 | `LONG` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:59 UTC | 1m 00s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9984 |
| 9 | `SHORT` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:41:59 UTC | 3m 00s | `0.11817` | `0.11827` | $2.36 | $0.03 | $0.000000 | **-0.0020** | `-6.3%` | `STOP_LOSS_HIT` | $99.9964 |
| 10 | `SHORT` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:59 UTC | 1m 00s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 11 | `SHORT` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:59 UTC | 1m 00s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9972 |
| 12 | `SHORT` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:59 UTC | 1m 00s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9976 |
| 13 | `LONG` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:59 UTC | 1m 00s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| 14 | `SHORT` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:59 UTC | 1m 00s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9984 |
| 15 | `LONG` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9988 |
| 16 | `LONG` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11844` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 17 | `SHORT` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:59 UTC | 1m 00s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 18 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:59 UTC | 1m 00s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 19 | `LONG` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:43:59 UTC | 3m 00s | `0.11863` | `0.11853` | $2.37 | $0.03 | $0.000000 | **-0.0020** | `-6.3%` | `STOP_LOSS_HIT` | $99.9980 |
| 20 | `LONG` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:50:59 UTC | 3m 00s | `0.11855` | `0.11857` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9984 |
| 21 | `LONG` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:05:59 UTC | 2m 00s | `0.11850` | `0.11840` | $2.37 | $0.03 | $0.000000 | **-0.0020** | `-6.3%` | `STOP_LOSS_HIT` | $99.9964 |
| 22 | `LONG` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:59 UTC | 1m 00s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 23 | `SHORT` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:59 UTC | 1m 00s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9972 |
| 24 | `SHORT` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:59 UTC | 3m 00s | `0.11817` | `0.11815` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9976 |
| 25 | `SHORT` | 2026-01-01 03:30:59 UTC | 2026-01-01 03:31:59 UTC | 1m 00s | `0.11843` | `0.11841` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| ... | ... | *(46125 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 46151 | `SHORT` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:59 UTC | 1m 00s | `0.08459` | `0.08469` | $1.69 | $0.02 | $0.000000 | **-0.0020** | `-8.9%` | `STOP_LOSS_HIT` | $99.0396 |
| 46152 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:59 UTC | 1m 00s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0400 |
| 46153 | `LONG` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:59 UTC | 1m 00s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0404 |
| 46154 | `SHORT` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:59 UTC | 1m 00s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0408 |
| 46155 | `LONG` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:59 UTC | 1m 00s | `0.08438` | `0.08440` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0412 |
| 46156 | `LONG` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:59 UTC | 1m 00s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0416 |
| 46157 | `SHORT` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:57:59 UTC | 2m 00s | `0.08446` | `0.08444` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0420 |
| 46158 | `SHORT` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:59 UTC | 1m 00s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0424 |
| 46159 | `SHORT` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:59 UTC | 1m 00s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0428 |
| 46160 | `LONG` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:59 UTC | 1m 00s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0432 |
| 46161 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `0.08424` | `0.08426` | $1.68 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0436 |
| 46162 | `SHORT` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:59 UTC | 1m 00s | `0.08385` | `0.08395` | $1.68 | $0.02 | $0.000000 | **-0.0020** | `-8.9%` | `STOP_LOSS_HIT` | $99.0416 |
| 46163 | `LONG` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:59 UTC | 1m 00s | `0.08371` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0020** | `-9.0%` | `STOP_LOSS_HIT` | $99.0396 |
| 46164 | `SHORT` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:59 UTC | 1m 00s | `0.08358` | `0.08356` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0400 |
| 46165 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:59 UTC | 1m 00s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0404 |
| 46166 | `LONG` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:59 UTC | 1m 00s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0408 |
| 46167 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `0.08339` | `0.08349` | $1.67 | $0.02 | $0.000000 | **-0.0020** | `-9.0%` | `STOP_LOSS_HIT` | $99.0388 |
| 46168 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:59 UTC | 1m 00s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0392 |
| 46169 | `LONG` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:59 UTC | 1m 00s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0396 |
| 46170 | `LONG` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:59 UTC | 1m 00s | `0.08215` | `0.08205` | $1.64 | $0.02 | $0.000000 | **-0.0020** | `-9.1%` | `STOP_LOSS_HIT` | $99.0376 |
| 46171 | `SHORT` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:59 UTC | 1m 00s | `0.08197` | `0.08195` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0380 |
| 46172 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:59 UTC | 1m 00s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0384 |
| 46173 | `LONG` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:59 UTC | 1m 00s | `0.08156` | `0.08158` | $1.63 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0388 |
| 46174 | `SHORT` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:59 UTC | 1m 00s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $99.0392 |
| 46175 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `0.08182` | `0.08182` | $1.64 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $99.0392 |

> 💡 *Full granular dataset with all 46175 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
