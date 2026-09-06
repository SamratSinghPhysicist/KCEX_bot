# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 14:18:44 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `101.9020 USDT` | `₹9,624.64` | `+1.90%` |
| **Net Realized PnL** | **`+1.9020 USDT`** | **`₹+179.64`** | **`+1.90% Net ROI`** |
| **Gross Profit** | `+12.9720 USDT` | `₹1,225.21` | Total positive trade returns |
| **Gross Loss** | `-11.0700 USDT` | `₹1,045.56` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.17`** | — | Profitable |
| **Win / Loss Payoff** | `2.62` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0312 USDT` | `₹2.95` | **`-0.03%` Peak-to-Trough** |
| **Win Rate** | **`26.94%`** | — | `12972 Wins / 29054 Losses / 6124 Scratch` |
| **Sharpe Ratio (est)** | `5.15` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `7.98` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `62.04` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `48150` | Total completed trade lifecycle events |
| **Winning Trades** | `12972` | `26.94%` of total trades |
| **Losing Trades** | `29054` | `60.34%` of total trades |
| **Scratch / Break-even** | `6124` | `12.72%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #158 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #141 (LONG) |
| **Max Consecutive Wins** | `10` trades | Peak winning streak |
| **Max Consecutive Losses** | `25` trades | Peak losing streak |
| **Average Trade Duration** | `24.3s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #102 |
| **Longest Trade In-Position** | `24m 21s` | Trade #45334 |
| **Cumulative Time In Position** | `324h 49m 26s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `23834` (49.5%) | `24316` (50.5%) | `48150` |
| **Wins / Losses** | `6447 W / 14255 L` | `6525 W / 14799 L` | `12972 W / 29054 L` |
| **Win Rate** | **`27.05%`** | **`26.83%`** | **`26.94%`** |
| **Gross Profit** | `+6.4470 USDT` | `+6.5250 USDT` | `+12.9720 USDT` |
| **Gross Loss** | `-5.4244 USDT` | `-5.6456 USDT` | `-11.0700 USDT` |
| **Net Realized PnL** | **`+1.0226 USDT`** | **`+0.8794 USDT`** | **`+1.9020 USDT`** |
| **Net PnL (INR)** | `₹+96.58` | `₹+83.06` | `₹+179.64` |
| **Profit Factor** | `1.19` | `1.16` | `1.17` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `29180` | `60.6%` | `-10.5184 USDT` | `₹-993.46` | `0.0%` | `11.8s` |
| `MIN_PROFIT_TP_HIT` | `12972` | `26.9%` | `+12.9720 USDT` | `₹+1,225.21` | `100.0%` | `32.5s` |
| `TICK_RATCHET_SL` | `5998` | `12.5%` | `-0.5516 USDT` | `₹-52.10` | `0.0%` | `1m 07s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:35 UTC | 35.1s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:00 UTC | 0.7s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:08 UTC | 9.0s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:38 UTC | 38.1s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 5 | `LONG` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:02:05 UTC | 1m 05s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 6 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:02 UTC | 2.8s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0018 |
| 7 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:49 UTC | 49.5s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 8 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:49 UTC | 1m 49s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0038 |
| 9 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:00 UTC | 0.7s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0034 |
| 10 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:36 UTC | 36.9s | `0.11817` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $100.0034 |
| 11 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:03 UTC | 3.2s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0030 |
| 12 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:25 UTC | 25.8s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0026 |
| 13 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:16 UTC | 16.7s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0022 |
| 14 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:06 UTC | 6.9s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0018 |
| 15 | `LONG` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:04 UTC | 4.2s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0014 |
| 16 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:04 UTC | 5.0s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0010 |
| 17 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:16 UTC | 16.5s | `0.11842` | `0.11844` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0006 |
| 18 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:01 UTC | 1.3s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0002 |
| 19 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:00 UTC | 0.7s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9998 |
| 20 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:16 UTC | 16.3s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 21 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:28 UTC | 1m 28s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0018 |
| 22 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:40 UTC | 41.0s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 23 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:00 UTC | 0.9s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 24 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:05 UTC | 5.9s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0020 |
| 25 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:01 UTC | 2m 01s | `0.11817` | `0.11815` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| ... | ... | *(48100 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 48126 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:30 UTC | 30.7s | `0.08459` | `0.08464` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $101.8984 |
| 48127 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:06 UTC | 6.8s | `0.08460` | `0.08460` | $1.69 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `STOP_LOSS_HIT` | $101.8984 |
| 48128 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:00 UTC | 0.8s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8980 |
| 48129 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:09 UTC | 9.5s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8976 |
| 48130 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:10 UTC | 10.9s | `0.08438` | `0.08438` | $1.69 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `STOP_LOSS_HIT` | $101.8976 |
| 48131 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:05 UTC | 5.2s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8972 |
| 48132 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:15 UTC | 15.2s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $101.8982 |
| 48133 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:00 UTC | 0.4s | `0.08458` | `0.08458` | $1.69 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `STOP_LOSS_HIT` | $101.8982 |
| 48134 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:06 UTC | 7.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8978 |
| 48135 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:01 UTC | 1.6s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8974 |
| 48136 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:06 UTC | 6.1s | `0.08424` | `0.08424` | $1.68 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `STOP_LOSS_HIT` | $101.8974 |
| 48137 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:10 UTC | 10.7s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $101.8984 |
| 48138 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:06 UTC | 6.2s | `0.08371` | `0.08366` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $101.8994 |
| 48139 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:07 UTC | 7.1s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $101.9004 |
| 48140 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:01 UTC | 1.1s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.9000 |
| 48141 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:06 UTC | 6.9s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8996 |
| 48142 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:15 UTC | 15.7s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $101.9006 |
| 48143 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:02 UTC | 2.7s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.9002 |
| 48144 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:00 UTC | 0.4s | `0.08245` | `0.08247` | $1.65 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.8998 |
| 48145 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:01 UTC | 1.1s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $101.9008 |
| 48146 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.4s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $101.9018 |
| 48147 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:04 UTC | 4.5s | `0.08150` | `0.08150` | $1.63 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `STOP_LOSS_HIT` | $101.9018 |
| 48148 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:03 UTC | 3.3s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $101.9028 |
| 48149 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:00 UTC | 0.9s | `0.08179` | `0.08177` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.9024 |
| 48150 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.9s | `0.08182` | `0.08180` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $101.9020 |

> 💡 *Full granular dataset with all 48150 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
