# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:08:23 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `111.5426 USDT` | `₹10,535.20` | `+11.54%` |
| **Net Realized PnL** | **`+11.5426 USDT`** | **`₹+1,090.20`** | **`+11.54% Net ROI`** |
| **Gross Profit** | `+21.9050 USDT` | `₹2,068.93` | Total positive trade returns |
| **Gross Loss** | `-10.3624 USDT` | `₹978.73` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`2.11`** | — | Exceptional (Institutional Grade) |
| **Win / Loss Payoff** | `2.50` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0162 USDT` | `₹1.53` | **`-0.01%` Peak-to-Trough** |
| **Win Rate** | **`45.81%`** | — | `21905 Wins / 25906 Losses / 1 Scratch` |
| **Sharpe Ratio (est)** | `27.12` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `47.53` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `786.49` | — | Net ROI divided by Max Drawdown |

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
| **Total Trades Executed** | `47812` | Total completed trade lifecycle events |
| **Winning Trades** | `21905` | `45.81%` of total trades |
| **Losing Trades** | `25906` | `54.18%` of total trades |
| **Scratch / Break-even** | `1` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0002 USDT` (`₹+0.02`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #157 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #154 (LONG) |
| **Max Consecutive Wins** | `18` trades | Peak winning streak |
| **Max Consecutive Losses** | `18` trades | Peak losing streak |
| **Average Trade Duration** | `1m 16s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #47812 |
| **Longest Trade In-Position** | `31m 00s` | Trade #45013 |
| **Cumulative Time In Position** | `1011h 11m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `23683` (49.5%) | `24129` (50.5%) | `47812` |
| **Wins / Losses** | `10778 W / 12904 L` | `11127 W / 13002 L` | `21905 W / 25906 L` |
| **Win Rate** | **`45.51%`** | **`46.11%`** | **`45.81%`** |
| **Gross Profit** | `+10.7780 USDT` | `+11.1270 USDT` | `+21.9050 USDT` |
| **Gross Loss** | `-5.1616 USDT` | `-5.2008 USDT` | `-10.3624 USDT` |
| **Net Realized PnL** | **`+5.6164 USDT`** | **`+5.9262 USDT`** | **`+11.5426 USDT`** |
| **Net PnL (INR)** | `₹+530.47` | `₹+559.73` | `₹+1,090.20` |
| **Profit Factor** | `2.09` | `2.14` | `2.11` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `25906` | `54.2%` | `-10.3624 USDT` | `₹-978.73` | `0.0%` | `1m 15s` |
| `MIN_PROFIT_TP_HIT` | `21905` | `45.8%` | `+21.9050 USDT` | `₹+2,068.93` | `100.0%` | `1m 17s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:59 UTC | 1m 00s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:59 UTC | 1m 00s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0002 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:59 UTC | 1m 00s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 5 | `LONG` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:02:59 UTC | 2m 00s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0022 |
| 6 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:59 UTC | 1m 00s | `0.11797` | `0.11802` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 7 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:59 UTC | 1m 00s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0042 |
| 8 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:59 UTC | 2m 00s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 9 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:59 UTC | 1m 00s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0048 |
| 10 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:41:59 UTC | 3m 00s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0058 |
| 11 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:59 UTC | 1m 00s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0054 |
| 12 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:59 UTC | 1m 00s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0050 |
| 13 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:59 UTC | 1m 00s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0046 |
| 14 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:59 UTC | 1m 00s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0042 |
| 15 | `LONG` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:59 UTC | 1m 00s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0038 |
| 16 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0034 |
| 17 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 18 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:59 UTC | 1m 00s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0040 |
| 19 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:59 UTC | 1m 00s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0036 |
| 20 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:59 UTC | 1m 00s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0046 |
| 21 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:59 UTC | 2m 00s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 22 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:59 UTC | 1m 00s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0066 |
| 23 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:59 UTC | 1m 00s | `0.11826` | `0.11821` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0076 |
| 24 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:59 UTC | 1m 00s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0072 |
| 25 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:59 UTC | 3m 00s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0082 |
| ... | ... | *(47762 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 47788 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:59 UTC | 1m 00s | `0.08459` | `0.08464` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $111.5322 |
| 47789 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:59 UTC | 1m 00s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5318 |
| 47790 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:59 UTC | 1m 00s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5314 |
| 47791 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:59 UTC | 1m 00s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5310 |
| 47792 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:59 UTC | 1m 00s | `0.08438` | `0.08433` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $111.5320 |
| 47793 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:59 UTC | 1m 00s | `0.08435` | `0.08430` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $111.5330 |
| 47794 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:59 UTC | 1m 00s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $111.5340 |
| 47795 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:59 UTC | 1m 00s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5336 |
| 47796 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:59 UTC | 1m 00s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5332 |
| 47797 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:59 UTC | 1m 00s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5328 |
| 47798 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `0.08424` | `0.08419` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5338 |
| 47799 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:59 UTC | 1m 00s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5348 |
| 47800 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:59 UTC | 1m 00s | `0.08371` | `0.08366` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5358 |
| 47801 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:59 UTC | 1m 00s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5368 |
| 47802 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:59 UTC | 1m 00s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5364 |
| 47803 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:59 UTC | 1m 00s | `0.08359` | `0.08354` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5374 |
| 47804 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5384 |
| 47805 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:59 UTC | 1m 00s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5380 |
| 47806 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:59 UTC | 1m 00s | `0.08245` | `0.08240` | $1.65 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $111.5390 |
| 47807 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:59 UTC | 1m 00s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $111.5400 |
| 47808 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:59 UTC | 1m 00s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $111.5410 |
| 47809 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:59 UTC | 1m 00s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $111.5406 |
| 47810 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:59 UTC | 1m 00s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $111.5416 |
| 47811 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:59 UTC | 1m 00s | `0.08179` | `0.08184` | $1.64 | $0.02 | $0.000000 | **+0.0010** | `+4.6%` | `MIN_PROFIT_TP_HIT` | $111.5426 |
| 47812 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `0.08182` | `0.08182` | $1.64 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $111.5426 |

> 💡 *Full granular dataset with all 47812 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
