# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 23:59:26 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `95.0814 USDT` | `₹8,980.44` | `-4.92%` |
| **Net Realized PnL** | **`-4.9186 USDT`** | **`₹-464.56`** | **`-4.92% Net ROI`** |
| **Gross Profit** | `+12.8630 USDT` | `₹1,214.91` | Total positive trade returns |
| **Gross Loss** | `-17.7816 USDT` | `₹1,679.47` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`0.72`** | — | Unprofitable / Needs Optimization |
| **Win / Loss Payoff** | `1.99` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-4.9282 USDT` | `₹465.47` | **`-4.93%` Peak-to-Trough** |
| **Win Rate** | **`26.70%`** | — | `12863 Wins / 35315 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `-11.75` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `-15.09` | — | Downside risk-adjusted return ratio |
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
| **Slippage Tolerance** | `1 ticks` (`0.00001 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Average Trade PnL** | `-0.0001 USDT` (`₹-0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0010 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0005 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0010 USDT (+3.0% ROE)` | Trade #175 (SHORT) |
| **Largest Losing Trade** | `-0.0006 USDT (-1.8% ROE)` | Trade #4574 (LONG) |
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
| **Gross Loss** | `-8.8984 USDT` | `-8.8832 USDT` | `-17.7816 USDT` |
| **Net Realized PnL** | **`-2.3404 USDT`** | **`-2.5782 USDT`** | **`-4.9186 USDT`** |
| **Net PnL (INR)** | `₹-221.05` | `₹-243.51` | `₹-464.56` |
| **Profit Factor** | `0.74` | `0.71` | `0.72` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RATCHET_BREAKEVEN_HIT` | `6791` | `14.1%` | `-1.3582 USDT` | `₹-128.28` | `0.0%` | `41.1s` |
| `RATCHET_TIGHTEN_HIT` | `3455` | `7.2%` | `-1.3820 USDT` | `₹-130.53` | `0.0%` | `47.6s` |
| `STOP_LOSS_HIT` | `25069` | `52.0%` | `-15.0414 USDT` | `₹-1,420.66` | `0.0%` | `11.2s` |
| `MIN_PROFIT_TP_HIT` | `12863` | `26.7%` | `+12.8630 USDT` | `₹+1,214.91` | `100.0%` | `31.3s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:34:01 UTC | 1m 01s | `0.11787` | `0.11788` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9998 |
| 2 | `LONG` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:26 UTC | 26.5s | `0.11778` | `0.11776` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `RATCHET_TIGHTEN_HIT` | $99.9994 |
| 3 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:02 UTC | 2.3s | `0.11775` | `0.11772` | $2.35 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:55:38 UTC | 38.1s | `0.11782` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9982 |
| 5 | `SHORT` | 2026-01-01 01:00:59 UTC | 2026-01-01 01:01:18 UTC | 18.7s | `0.11788` | `0.11791` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9976 |
| 6 | `SHORT` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:20 UTC | 20.9s | `0.11797` | `0.11798` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9974 |
| 7 | `SHORT` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:14:05 UTC | 5.2s | `0.11838` | `0.11841` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9968 |
| 8 | `LONG` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:25:22 UTC | 1m 22s | `0.11822` | `0.11819` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9962 |
| 9 | `LONG` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:56 UTC | 56.2s | `0.11814` | `0.11813` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9960 |
| 10 | `SHORT` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:01 UTC | 1.2s | `0.11817` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9954 |
| 11 | `SHORT` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:45:38 UTC | 1m 38s | `0.11831` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9952 |
| 12 | `SHORT` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:40 UTC | 40.8s | `0.11856` | `0.11857` | $2.37 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9950 |
| 13 | `SHORT` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:23 UTC | 23.1s | `0.11849` | `0.11844` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9960 |
| 14 | `LONG` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:34 UTC | 34.4s | `0.11847` | `0.11846` | $2.37 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9958 |
| 15 | `SHORT` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:11:43 UTC | 1m 43s | `0.11845` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 16 | `LONG` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:08 UTC | 8.6s | `0.11830` | `0.11835` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9978 |
| 17 | `LONG` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:11 UTC | 11.6s | `0.11842` | `0.11839` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9972 |
| 18 | `SHORT` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:27 UTC | 28.0s | `0.11839` | `0.11834` | $2.37 | $0.03 | $0.000000 | **+0.0010** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $99.9982 |
| 19 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:18 UTC | 18.2s | `0.11854` | `0.11855` | $2.37 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9980 |
| 20 | `LONG` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:09 UTC | 9.2s | `0.11863` | `0.11860` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9974 |
| 21 | `LONG` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:26 UTC | 1m 26s | `0.11855` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9968 |
| 22 | `LONG` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:04:22 UTC | 22.1s | `0.11850` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9962 |
| 23 | `LONG` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:23 UTC | 23.7s | `0.11826` | `0.11823` | $2.37 | $0.03 | $0.000000 | **-0.0006** | `-1.9%` | `STOP_LOSS_HIT` | $99.9956 |
| 24 | `SHORT` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:14 UTC | 14.2s | `0.11822` | `0.11823` | $2.36 | $0.03 | $0.000000 | **-0.0002** | `-0.6%` | `RATCHET_BREAKEVEN_HIT` | $99.9954 |
| 25 | `SHORT` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:02 UTC | 2m 02s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `RATCHET_TIGHTEN_HIT` | $99.9950 |
| ... | ... | *(48128 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 48154 | `SHORT` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:01 UTC | 1.1s | `0.08459` | `0.08462` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0880 |
| 48155 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:01 UTC | 1.3s | `0.08460` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0874 |
| 48156 | `LONG` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:14 UTC | 14.6s | `0.08446` | `0.08444` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `RATCHET_TIGHTEN_HIT` | $95.0870 |
| 48157 | `SHORT` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:11 UTC | 11.1s | `0.08480` | `0.08475` | $1.70 | $0.02 | $0.000000 | **+0.0010** | `+4.4%` | `MIN_PROFIT_TP_HIT` | $95.0880 |
| 48158 | `LONG` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:09 UTC | 9.4s | `0.08438` | `0.08435` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0874 |
| 48159 | `LONG` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:10 UTC | 10.0s | `0.08435` | `0.08432` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0868 |
| 48160 | `SHORT` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:56:04 UTC | 4.6s | `0.08446` | `0.08449` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0862 |
| 48161 | `SHORT` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:00 UTC | 0.2s | `0.08458` | `0.08461` | $1.69 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0856 |
| 48162 | `SHORT` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:21 UTC | 21.9s | `0.08465` | `0.08466` | $1.69 | $0.02 | $0.000000 | **-0.0002** | `-0.9%` | `RATCHET_BREAKEVEN_HIT` | $95.0854 |
| 48163 | `LONG` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:14 UTC | 14.1s | `0.08423` | `0.08428` | $1.68 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $95.0864 |
| 48164 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:00 UTC | 0.9s | `0.08424` | `0.08421` | $1.68 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0858 |
| 48165 | `SHORT` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:04 UTC | 4.0s | `0.08385` | `0.08388` | $1.68 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0852 |
| 48166 | `LONG` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:00 UTC | 0.5s | `0.08371` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0846 |
| 48167 | `SHORT` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:00 UTC | 0.4s | `0.08358` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0840 |
| 48168 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:15 UTC | 15.2s | `0.08370` | `0.08365` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $95.0850 |
| 48169 | `LONG` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:11 UTC | 11.3s | `0.08359` | `0.08358` | $1.67 | $0.02 | $0.000000 | **-0.0002** | `-0.9%` | `RATCHET_BREAKEVEN_HIT` | $95.0848 |
| 48170 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:08 UTC | 8.9s | `0.08339` | `0.08342` | $1.67 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0842 |
| 48171 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:48 UTC | 48.1s | `0.08333` | `0.08328` | $1.67 | $0.02 | $0.000000 | **+0.0010** | `+4.5%` | `MIN_PROFIT_TP_HIT` | $95.0852 |
| 48172 | `LONG` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:05 UTC | 5.5s | `0.08245` | `0.08244` | $1.65 | $0.02 | $0.000000 | **-0.0002** | `-0.9%` | `RATCHET_BREAKEVEN_HIT` | $95.0850 |
| 48173 | `LONG` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:00 UTC | 0.6s | `0.08215` | `0.08212` | $1.64 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0844 |
| 48174 | `SHORT` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:00 UTC | 0.1s | `0.08197` | `0.08200` | $1.64 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0838 |
| 48175 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.8s | `0.08150` | `0.08147` | $1.63 | $0.02 | $0.000000 | **-0.0006** | `-2.8%` | `STOP_LOSS_HIT` | $95.0832 |
| 48176 | `LONG` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:00 UTC | 0.8s | `0.08156` | `0.08153` | $1.63 | $0.02 | $0.000000 | **-0.0006** | `-2.8%` | `STOP_LOSS_HIT` | $95.0826 |
| 48177 | `SHORT` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:05 UTC | 5.4s | `0.08179` | `0.08182` | $1.64 | $0.02 | $0.000000 | **-0.0006** | `-2.8%` | `STOP_LOSS_HIT` | $95.0820 |
| 48178 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.8s | `0.08182` | `0.08185` | $1.64 | $0.02 | $0.000000 | **-0.0006** | `-2.7%` | `STOP_LOSS_HIT` | $95.0814 |

> 💡 *Full granular dataset with all 48178 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
