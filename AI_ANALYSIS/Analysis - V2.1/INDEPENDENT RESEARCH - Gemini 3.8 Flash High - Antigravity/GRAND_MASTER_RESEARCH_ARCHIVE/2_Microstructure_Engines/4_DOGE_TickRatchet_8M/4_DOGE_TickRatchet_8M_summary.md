# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:50:32 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `112.4408 USDT` | `₹10,620.03` | `+12.44%` |
| **Net Realized PnL** | **`+12.4408 USDT`** | **`₹+1,175.03`** | **`+12.44% Net ROI`** |
| **Gross Profit** | `+19.4970 USDT` | `₹1,841.49` | Total positive trade returns |
| **Gross Loss** | `-7.0562 USDT` | `₹666.46` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`2.76`** | — | Exceptional (Institutional Grade) |
| **Win / Loss Payoff** | `2.92` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.1616 USDT` | `₹15.26` | **`-0.14%` Peak-to-Trough** |
| **Win Rate** | **`40.35%`** | — | `19497 Wins / 20603 Losses / 8219 Scratch` |
| **Sharpe Ratio (est)** | `32.29` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `57.45` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `86.03` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `48319` | Total completed trade lifecycle events |
| **Winning Trades** | `19497` | `40.35%` of total trades |
| **Losing Trades** | `20603` | `42.64%` of total trades |
| **Scratch / Break-even** | `8219` | `17.01%` of total trades |
| **Average Trade PnL** | `+0.0003 USDT` (`₹+0.02`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0003 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #158 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #155 (LONG) |
| **Max Consecutive Wins** | `18` trades | Peak winning streak |
| **Max Consecutive Losses** | `19` trades | Peak losing streak |
| **Average Trade Duration** | `1m 06s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #48319 |
| **Longest Trade In-Position** | `25m 00s` | Trade #45481 |
| **Cumulative Time In Position** | `890h 30m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `23915` (49.5%) | `24404` (50.5%) | `48319` |
| **Wins / Losses** | `9553 W / 10201 L` | `9944 W / 10402 L` | `19497 W / 20603 L` |
| **Win Rate** | **`39.95%`** | **`40.75%`** | **`40.35%`** |
| **Gross Profit** | `+9.5530 USDT` | `+9.9440 USDT` | `+19.4970 USDT` |
| **Gross Loss** | `-3.4872 USDT` | `-3.5690 USDT` | `-7.0562 USDT` |
| **Net Realized PnL** | **`+6.0658 USDT`** | **`+6.3750 USDT`** | **`+12.4408 USDT`** |
| **Net PnL (INR)** | `₹+572.91` | `₹+602.12` | `₹+1,175.03` |
| **Profit Factor** | `2.74` | `2.79` | `2.76` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `14678` | `30.4%` | `-5.8712 USDT` | `₹-554.53` | `0.0%` | `1m 06s` |
| `TICK_RATCHET_SL` | `14143` | `29.3%` | `-1.1850 USDT` | `₹-111.92` | `0.0%` | `1m 09s` |
| `MIN_PROFIT_TP_HIT` | `19497` | `40.4%` | `+19.4970 USDT` | `₹+1,841.49` | `100.0%` | `1m 04s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:59 UTC | 1m 00s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:59 UTC | 1m 00s | `0.11778` | `0.11779` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `TICK_RATCHET_SL` | $99.9994 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:59 UTC | 1m 00s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0014 |
| 5 | `LONG` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:01:59 UTC | 1m 00s | `0.11788` | `0.11788` | $2.36 | $0.03 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $100.0014 |
| 6 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:59 UTC | 1m 00s | `0.11797` | `0.11802` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 7 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:59 UTC | 1m 00s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0034 |
| 8 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:59 UTC | 2m 00s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 9 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:59 UTC | 1m 00s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0040 |
| 10 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:59 UTC | 1m 00s | `0.11817` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $100.0040 |
| 11 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:59 UTC | 1m 00s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0036 |
| 12 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:59 UTC | 1m 00s | `0.11856` | `0.11856` | $2.37 | $0.03 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $100.0036 |
| 13 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:59 UTC | 1m 00s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0032 |
| 14 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:59 UTC | 1m 00s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0028 |
| 15 | `LONG` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:59 UTC | 1m 00s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 16 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11830` | $2.37 | $0.03 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $100.0024 |
| 17 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0034 |
| 18 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:59 UTC | 1m 00s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0030 |
| 19 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:59 UTC | 1m 00s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0026 |
| 20 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:59 UTC | 1m 00s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 21 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:59 UTC | 2m 00s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0046 |
| 22 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:59 UTC | 1m 00s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 23 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:59 UTC | 1m 00s | `0.11826` | `0.11821` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0066 |
| 24 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:59 UTC | 1m 00s | `0.11822` | `0.11821` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `TICK_RATCHET_SL` | $100.0064 |
| 25 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:59 UTC | 3m 00s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0074 |
| ... | ... | *(48269 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 48295 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:59 UTC | 1m 00s | `0.08459` | `0.08464` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $112.4290 |
| 48296 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:59 UTC | 1m 00s | `0.08460` | `0.08460` | $1.69 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $112.4290 |
| 48297 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:59 UTC | 1m 00s | `0.08446` | `0.08447` | $1.69 | $0.02 | $0.000000 | **-0.0002** | `-0.9%` | `TICK_RATCHET_SL` | $112.4288 |
| 48298 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:59 UTC | 1m 00s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $112.4284 |
| 48299 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:59 UTC | 1m 00s | `0.08438` | `0.08433` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $112.4294 |
| 48300 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:59 UTC | 1m 00s | `0.08435` | `0.08430` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $112.4304 |
| 48301 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:59 UTC | 1m 00s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $112.4314 |
| 48302 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:59 UTC | 1m 00s | `0.08458` | `0.08458` | $1.69 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $112.4314 |
| 48303 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:59 UTC | 1m 00s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $112.4310 |
| 48304 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:59 UTC | 1m 00s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $112.4306 |
| 48305 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `0.08424` | `0.08419` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4316 |
| 48306 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:59 UTC | 1m 00s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4326 |
| 48307 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:59 UTC | 1m 00s | `0.08371` | `0.08366` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4336 |
| 48308 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:59 UTC | 1m 00s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4346 |
| 48309 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:59 UTC | 1m 00s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $112.4342 |
| 48310 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:59 UTC | 1m 00s | `0.08359` | `0.08354` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4352 |
| 48311 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4362 |
| 48312 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:59 UTC | 1m 00s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $112.4358 |
| 48313 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:59 UTC | 1m 00s | `0.08245` | `0.08240` | $1.65 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $112.4368 |
| 48314 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:59 UTC | 1m 00s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $112.4378 |
| 48315 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:59 UTC | 1m 00s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $112.4388 |
| 48316 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:59 UTC | 1m 00s | `0.08150` | `0.08150` | $1.63 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `TICK_RATCHET_SL` | $112.4388 |
| 48317 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:59 UTC | 1m 00s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $112.4398 |
| 48318 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:59 UTC | 1m 00s | `0.08179` | `0.08184` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $112.4408 |
| 48319 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `0.08182` | `0.08182` | $1.64 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $112.4408 |

> 💡 *Full granular dataset with all 48319 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
