# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:50:43 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0016 USDT` | `₹9,445.15` | `+0.00%` |
| **Net Realized PnL** | **`+0.0016 USDT`** | **`₹+0.15`** | **`+0.00% Net ROI`** |
| **Gross Profit** | `+41.9240 USDT` | `₹3,959.72` | Total positive trade returns |
| **Gross Loss** | `-41.9224 USDT` | `₹3,959.57` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.00`** | — | Profitable |
| **Win / Loss Payoff** | `0.79` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.5544 USDT` | `₹52.36` | **`-0.55%` Peak-to-Trough** |
| **Win Rate** | **`55.90%`** | — | `24547 Wins / 19367 Losses / 1 Scratch` |
| **Sharpe Ratio (est)** | `0.00` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `0.00` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `0.00` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `43915` | Total completed trade lifecycle events |
| **Winning Trades** | `24547` | `55.90%` of total trades |
| **Losing Trades** | `19367` | `44.10%` of total trades |
| **Scratch / Break-even** | `1` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0017 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0022 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0302 USDT (+89.1% ROE)` | Trade #3255 (SHORT) |
| **Largest Losing Trade** | `-0.0210 USDT (-62.5% ROE)` | Trade #3258 (SHORT) |
| **Max Consecutive Wins** | `15` trades | Peak winning streak |
| **Max Consecutive Losses** | `12` trades | Peak losing streak |
| **Average Trade Duration** | `2m 29s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #43915 |
| **Longest Trade In-Position** | `47m 00s` | Trade #6789 |
| **Cumulative Time In Position** | `1829h 06m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `21759` (49.5%) | `22156` (50.5%) | `43915` |
| **Wins / Losses** | `12108 W / 9650 L` | `12439 W / 9717 L` | `24547 W / 19367 L` |
| **Win Rate** | **`55.65%`** | **`56.14%`** | **`55.90%`** |
| **Gross Profit** | `+20.6976 USDT` | `+21.2264 USDT` | `+41.9240 USDT` |
| **Gross Loss** | `-20.9342 USDT` | `-20.9882 USDT` | `-41.9224 USDT` |
| **Net Realized PnL** | **`-0.2366 USDT`** | **`+0.2382 USDT`** | **`+0.0016 USDT`** |
| **Net PnL (INR)** | `₹-22.35` | `₹+22.50` | `₹+0.15` |
| **Profit Factor** | `0.99` | `1.01` | `1.00` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `24547` | `55.9%` | `+41.9240 USDT` | `₹+3,959.72` | `100.0%` | `2m 22s` |
| `STOP_LOSS_HIT` | `19367` | `44.1%` | `-41.9224 USDT` | `₹-3,959.57` | `0.0%` | `2m 39s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:35:59 UTC | 3m 00s | `0.11787` | `0.11792` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0010 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:43:59 UTC | 3m 00s | `0.11778` | `0.11772` | $2.36 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:59 UTC | 1m 00s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0042 |
| 5 | `LONG` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:02:59 UTC | 2m 00s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 6 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:59 UTC | 1m 00s | `0.11797` | `0.11802` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0062 |
| 7 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:15:59 UTC | 2m 00s | `0.11838` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0014** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $100.0076 |
| 8 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:26:59 UTC | 3m 00s | `0.11822` | `0.11815` | $2.36 | $0.03 | $0.000000 | **+0.0014** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $100.0090 |
| 9 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:38:59 UTC | 7m 00s | `0.11814` | `0.11808` | $2.36 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0102 |
| 10 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:48:59 UTC | 5m 00s | `0.11831` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0114 |
| 11 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:57:59 UTC | 2m 00s | `0.11856` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0014** | `-4.4%` | `STOP_LOSS_HIT` | $100.0100 |
| 12 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 02:00:59 UTC | 2m 00s | `0.11849` | `0.11842` | $2.37 | $0.03 | $0.000000 | **-0.0014** | `-4.4%` | `STOP_LOSS_HIT` | $100.0086 |
| 13 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:11:59 UTC | 7m 00s | `0.11847` | `0.11841` | $2.37 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0098 |
| 14 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11836` | $2.37 | $0.03 | $0.000000 | **-0.0012** | `-3.8%` | `STOP_LOSS_HIT` | $100.0086 |
| 15 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0096 |
| 16 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:31:59 UTC | 5m 00s | `0.11839` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0108 |
| 17 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:39:59 UTC | 4m 00s | `0.11854` | `0.11861` | $2.37 | $0.03 | $0.000000 | **+0.0014** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $100.0122 |
| 18 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:59 UTC | 1m 00s | `0.11863` | `0.11857` | $2.37 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0134 |
| 19 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:59 UTC | 2m 00s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0144 |
| 20 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:59 UTC | 1m 00s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0154 |
| 21 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:59 UTC | 1m 00s | `0.11826` | `0.11820` | $2.37 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0166 |
| 22 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:20:59 UTC | 3m 00s | `0.11822` | `0.11828` | $2.36 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0178 |
| 23 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:59 UTC | 3m 00s | `0.11817` | `0.11823` | $2.36 | $0.03 | $0.000000 | **+0.0012** | `+3.8%` | `MIN_PROFIT_TP_HIT` | $100.0190 |
| 24 | `LONG` | 2026-01-01 03:30:59 UTC | 2026-01-01 03:31:59 UTC | 1m 00s | `0.11843` | `0.11836` | $2.37 | $0.03 | $0.000000 | **-0.0014** | `-4.4%` | `STOP_LOSS_HIT` | $100.0176 |
| 25 | `LONG` | 2026-01-01 03:40:59 UTC | 2026-01-01 03:43:59 UTC | 3m 00s | `0.11853` | `0.11846` | $2.37 | $0.03 | $0.000000 | **-0.0014** | `-4.4%` | `STOP_LOSS_HIT` | $100.0162 |
| ... | ... | *(43865 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 43891 | `SHORT` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:48:59 UTC | 2m 00s | `0.08503` | `0.08519` | $1.70 | $0.02 | $0.000000 | **-0.0032** | `-14.1%` | `STOP_LOSS_HIT` | $100.0172 |
| 43892 | `LONG` | 2026-08-30 20:53:59 UTC | 2026-08-30 20:58:59 UTC | 5m 00s | `0.08528` | `0.08515` | $1.71 | $0.02 | $0.000000 | **-0.0026** | `-11.4%` | `STOP_LOSS_HIT` | $100.0146 |
| 43893 | `SHORT` | 2026-08-30 21:04:59 UTC | 2026-08-30 21:08:59 UTC | 4m 00s | `0.08449` | `0.08469` | $1.69 | $0.02 | $0.000000 | **-0.0040** | `-17.8%` | `STOP_LOSS_HIT` | $100.0106 |
| 43894 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:23:59 UTC | 12m 00s | `0.08459` | `0.08441` | $1.69 | $0.02 | $0.000000 | **-0.0036** | `-16.0%` | `STOP_LOSS_HIT` | $100.0070 |
| 43895 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:28:59 UTC | 3m 00s | `0.08446` | `0.08459` | $1.69 | $0.02 | $0.000000 | **-0.0026** | `-11.5%` | `STOP_LOSS_HIT` | $100.0044 |
| 43896 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:38:59 UTC | 2m 00s | `0.08480` | `0.08468` | $1.70 | $0.02 | $0.000000 | **-0.0024** | `-10.6%` | `STOP_LOSS_HIT` | $100.0020 |
| 43897 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:47:59 UTC | 2m 00s | `0.08438` | `0.08429` | $1.69 | $0.02 | $0.000000 | **+0.0018** | `+8.0%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 43898 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:55:59 UTC | 6m 00s | `0.08435` | `0.08447` | $1.69 | $0.02 | $0.000000 | **-0.0024** | `-10.7%` | `STOP_LOSS_HIT` | $100.0014 |
| 43899 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:59 UTC | 1m 00s | `0.08458` | `0.08447` | $1.69 | $0.02 | $0.000000 | **-0.0022** | `-9.8%` | `STOP_LOSS_HIT` | $99.9992 |
| 43900 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:09:59 UTC | 4m 00s | `0.08465` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0034** | `-15.1%` | `STOP_LOSS_HIT` | $99.9958 |
| 43901 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:16:59 UTC | 3m 00s | `0.08423` | `0.08412` | $1.68 | $0.02 | $0.000000 | **+0.0022** | `+9.8%` | `MIN_PROFIT_TP_HIT` | $99.9980 |
| 43902 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:21:59 UTC | 2m 00s | `0.08424` | `0.08411` | $1.68 | $0.02 | $0.000000 | **+0.0026** | `+11.6%` | `MIN_PROFIT_TP_HIT` | $100.0006 |
| 43903 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:25:59 UTC | 3m 00s | `0.08385` | `0.08364` | $1.68 | $0.02 | $0.000000 | **-0.0042** | `-18.8%` | `STOP_LOSS_HIT` | $99.9964 |
| 43904 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:59 UTC | 1m 00s | `0.08371` | `0.08356` | $1.67 | $0.02 | $0.000000 | **+0.0030** | `+13.4%` | `MIN_PROFIT_TP_HIT` | $99.9994 |
| 43905 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:39:59 UTC | 4m 00s | `0.08358` | `0.08373` | $1.67 | $0.02 | $0.000000 | **+0.0030** | `+13.5%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 43906 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:47:59 UTC | 4m 00s | `0.08370` | `0.08355` | $1.67 | $0.02 | $0.000000 | **-0.0030** | `-13.4%` | `STOP_LOSS_HIT` | $99.9994 |
| 43907 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:55:59 UTC | 2m 00s | `0.08359` | `0.08349` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0014 |
| 43908 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `0.08339` | `0.08349` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $100.0034 |
| 43909 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:17:59 UTC | 2m 00s | `0.08333` | `0.08320` | $1.67 | $0.02 | $0.000000 | **-0.0026** | `-11.7%` | `STOP_LOSS_HIT` | $100.0008 |
| 43910 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:59 UTC | 1m 00s | `0.08245` | `0.08228` | $1.65 | $0.02 | $0.000000 | **+0.0034** | `+15.5%` | `MIN_PROFIT_TP_HIT` | $100.0042 |
| 43911 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:35:59 UTC | 4m 00s | `0.08215` | `0.08193` | $1.64 | $0.02 | $0.000000 | **+0.0044** | `+20.1%` | `MIN_PROFIT_TP_HIT` | $100.0086 |
| 43912 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:38:59 UTC | 2m 00s | `0.08197` | `0.08171` | $1.64 | $0.02 | $0.000000 | **-0.0052** | `-23.8%` | `STOP_LOSS_HIT` | $100.0034 |
| 43913 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:45:59 UTC | 3m 00s | `0.08150` | `0.08129` | $1.63 | $0.02 | $0.000000 | **+0.0042** | `+19.3%` | `MIN_PROFIT_TP_HIT` | $100.0076 |
| 43914 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:55:59 UTC | 5m 00s | `0.08156` | `0.08186` | $1.63 | $0.02 | $0.000000 | **-0.0060** | `-27.6%` | `STOP_LOSS_HIT` | $100.0016 |
| 43915 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `0.08182` | `0.08182` | $1.64 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $100.0016 |

> 💡 *Full granular dataset with all 43915 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
