# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-07 00:00:08 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `80.9554 USDT` | `₹7,646.24` | `-19.04%` |
| **Net Realized PnL** | **`-19.0446 USDT`** | **`₹-1,798.76`** | **`-19.04% Net ROI`** |
| **Gross Profit** | `+12.8630 USDT` | `₹1,214.91` | Total positive trade returns |
| **Gross Loss** | `-31.9076 USDT` | `₹3,013.67` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.40`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.11` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-19.0446 USDT` | `₹1,798.76` | **`-19.04%` Peak-to-Trough** |
| **Win Rate** | **`26.70%`** | — | `12863 Wins / 35315 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-36.21` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-33.59` | — | Downside risk-adjusted return ratio |
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
| **Slippage Tolerance** | `3 ticks` (`0.00003 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Total Trades Executed** | `48178` | Total completed trade lifecycle events |
| **Winning Trades** | `12863` | `26.70%` of total trades |
| **Losing Trades** | `35315` | `73.30%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `-0.0004 USDT` (`₹-0.04`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0009 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #175 (SHORT) |
| **Largest Losing Trade** | `-0.0010 USDT (-3.0% ROE)` | Trade #158 (SHORT) |
| **Max Consecutive Wins** | `8` trades | Peak winning streak |
| **Max Consecutive Losses** | `29` trades | Peak losing streak |
| **Average Trade Duration** | `23.4s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #74 |
| **Longest Trade In-Position** | `39m 11s` | Trade #45331 |
| **Cumulative Time In Position** | `313h 11m 34s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `24324` (50.5%) | `23854` (49.5%) | `48178` |
| **Wins / Losses** | `6558 W / 17766 L` | `6305 W / 17549 L` | `12863 W / 35315 L` |
| **Win Rate** | **`26.96%`** | **`26.43%`** | **`26.70%`** |
| **Gross Profit** | `+6.5580 USDT` | `+6.3050 USDT` | `+12.8630 USDT` |
| **Gross Loss** | `-16.0048 USDT` | `-15.9028 USDT` | `-31.9076 USDT` |
| **Net Realized PnL** | **`-9.4468 USDT`** | **`-9.5978 USDT`** | **`-19.0446 USDT`** |
| **Net PnL (INR)** | `₹-892.25` | `₹-906.51` | `₹-1,798.76` |
| **Profit Factor** | `0.41` | `0.40` | `0.40` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RATCHET_BREAKEVEN_HIT` | `6791` | `14.1%` | `-4.0746 USDT` | `₹-384.85` | `0.0%` | `41.1s` |
| `RATCHET_TIGHTEN_HIT` | `3455` | `7.2%` | `-2.7640 USDT` | `₹-261.06` | `0.0%` | `47.6s` |
| `STOP_LOSS_HIT` | `25069` | `52.0%` | `-25.0690 USDT` | `₹-2,367.77` | `0.0%` | `11.2s` |
| `MIN_PROFIT_TP_HIT` | `12863` | `26.7%` | `+12.8630 USDT` | `₹+1,214.91` | `100.0%` | `31.3s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:34:01 UTC | 1m 01s | `0.11787` | `0.11790` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9994 |
| 2 | `LONG` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:26 UTC | 26.5s | `0.11778` | `0.11774` | $2.36 | $0.03 | $0.000000 | **-0.0008** | `-2.5%` | `RATCHET_TIGHTEN_HIT` | $99.9986 |
| 3 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:02 UTC | 2.3s | `0.11775` | `0.11770` | $2.35 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9976 |
| 4 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:38 UTC | 38.1s | `0.11782` | `0.11787` | $2.36 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9966 |
| 5 | `SHORT` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:01:18 UTC | 18.7s | `0.11788` | `0.11793` | $2.36 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9956 |
| 6 | `SHORT` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:20 UTC | 20.9s | `0.11797` | `0.11800` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9950 |
| 7 | `SHORT` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:05 UTC | 5.2s | `0.11838` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9940 |
| 8 | `LONG` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:22 UTC | 1m 22s | `0.11822` | `0.11817` | $2.36 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9930 |
| 9 | `LONG` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:56 UTC | 56.2s | `0.11814` | `0.11811` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9924 |
| 10 | `SHORT` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:01 UTC | 1.2s | `0.11817` | `0.11822` | $2.36 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9914 |
| 11 | `SHORT` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:45:38 UTC | 1m 38s | `0.11831` | `0.11834` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9908 |
| 12 | `SHORT` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:40 UTC | 40.8s | `0.11856` | `0.11859` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9902 |
| 13 | `SHORT` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:23 UTC | 23.1s | `0.11849` | `0.11844` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9912 |
| 14 | `LONG` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:34 UTC | 34.4s | `0.11847` | `0.11844` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9906 |
| 15 | `SHORT` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:11:43 UTC | 1m 43s | `0.11845` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9916 |
| 16 | `LONG` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:08 UTC | 8.6s | `0.11830` | `0.11835` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9926 |
| 17 | `LONG` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:11 UTC | 11.6s | `0.11842` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9916 |
| 18 | `SHORT` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:27 UTC | 28.0s | `0.11839` | `0.11834` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9926 |
| 19 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:18 UTC | 18.2s | `0.11854` | `0.11857` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9920 |
| 20 | `LONG` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:09 UTC | 9.2s | `0.11863` | `0.11858` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9910 |
| 21 | `LONG` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:26 UTC | 1m 26s | `0.11855` | `0.11850` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9900 |
| 22 | `LONG` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:22 UTC | 22.1s | `0.11850` | `0.11845` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9890 |
| 23 | `LONG` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:23 UTC | 23.7s | `0.11826` | `0.11821` | $2.37 | $0.03 | $0.000000 | **-0.0010** | `-3.2%` | `STOP_LOSS_HIT` | $99.9880 |
| 24 | `SHORT` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:14 UTC | 14.2s | `0.11822` | `0.11825` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `RATCHET_BREAKEVEN_HIT` | $99.9874 |
| 25 | `SHORT` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:02 UTC | 2m 02s | `0.11817` | `0.11821` | $2.36 | $0.03 | $0.000000 | **-0.0008** | `-2.5%` | `RATCHET_TIGHTEN_HIT` | $99.9866 |
| ... | ... | *(48128 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 48154 | `SHORT` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:01 UTC | 1.1s | `0.08459` | `0.08464` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9700 |
| 48155 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:01 UTC | 1.3s | `0.08460` | `0.08465` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9690 |
| 48156 | `LONG` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:14 UTC | 14.6s | `0.08446` | `0.08442` | $1.69 | $0.02 | $0.000000 | **-0.0008** | `-3.6%` | `RATCHET_TIGHTEN_HIT` | $80.9682 |
| 48157 | `SHORT` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:11 UTC | 11.1s | `0.08480` | `0.08475` | $1.70 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $80.9692 |
| 48158 | `LONG` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:09 UTC | 9.4s | `0.08438` | `0.08433` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9682 |
| 48159 | `LONG` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:10 UTC | 10.0s | `0.08435` | `0.08430` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9672 |
| 48160 | `SHORT` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:04 UTC | 4.6s | `0.08446` | `0.08451` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9662 |
| 48161 | `SHORT` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:00 UTC | 0.2s | `0.08458` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0010** | `-4.4%` | `STOP_LOSS_HIT` | $80.9652 |
| 48162 | `SHORT` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:21 UTC | 21.9s | `0.08465` | `0.08468` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `RATCHET_BREAKEVEN_HIT` | $80.9646 |
| 48163 | `LONG` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:14 UTC | 14.1s | `0.08423` | `0.08428` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $80.9656 |
| 48164 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:00 UTC | 0.9s | `0.08424` | `0.08419` | $1.68 | $0.02 | $0.000000 | **-0.0010** | `-4.5%` | `STOP_LOSS_HIT` | $80.9646 |
| 48165 | `SHORT` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:04 UTC | 4.0s | `0.08385` | `0.08390` | $1.68 | $0.02 | $0.000000 | **-0.0010** | `-4.5%` | `STOP_LOSS_HIT` | $80.9636 |
| 48166 | `LONG` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:00 UTC | 0.5s | `0.08371` | `0.08366` | $1.67 | $0.02 | $0.000000 | **-0.0010** | `-4.5%` | `STOP_LOSS_HIT` | $80.9626 |
| 48167 | `SHORT` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:00 UTC | 0.4s | `0.08358` | `0.08363` | $1.67 | $0.02 | $0.000000 | **-0.0010** | `-4.5%` | `STOP_LOSS_HIT` | $80.9616 |
| 48168 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:15 UTC | 15.2s | `0.08370` | `0.08365` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $80.9626 |
| 48169 | `LONG` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:11 UTC | 11.3s | `0.08359` | `0.08356` | $1.67 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `RATCHET_BREAKEVEN_HIT` | $80.9620 |
| 48170 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:08 UTC | 8.9s | `0.08339` | `0.08344` | $1.67 | $0.02 | $0.000000 | **-0.0010** | `-4.5%` | `STOP_LOSS_HIT` | $80.9610 |
| 48171 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:48 UTC | 48.1s | `0.08333` | `0.08328` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $80.9620 |
| 48172 | `LONG` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:05 UTC | 5.5s | `0.08245` | `0.08242` | $1.65 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `RATCHET_BREAKEVEN_HIT` | $80.9614 |
| 48173 | `LONG` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:00 UTC | 0.6s | `0.08215` | `0.08210` | $1.64 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9604 |
| 48174 | `SHORT` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.1s | `0.08197` | `0.08202` | $1.64 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9594 |
| 48175 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.8s | `0.08150` | `0.08145` | $1.63 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9584 |
| 48176 | `LONG` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:00 UTC | 0.8s | `0.08156` | `0.08151` | $1.63 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9574 |
| 48177 | `SHORT` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:05 UTC | 5.4s | `0.08179` | `0.08184` | $1.64 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9564 |
| 48178 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.8s | `0.08182` | `0.08187` | $1.64 | $0.02 | $0.000000 | **-0.0010** | `-4.6%` | `STOP_LOSS_HIT` | $80.9554 |

> 💡 *Full granular dataset with all 48178 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
