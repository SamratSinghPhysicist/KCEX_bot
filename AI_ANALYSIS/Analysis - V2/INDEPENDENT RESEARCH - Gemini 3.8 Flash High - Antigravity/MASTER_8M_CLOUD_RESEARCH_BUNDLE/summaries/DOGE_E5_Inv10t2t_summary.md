# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:08:06 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `110.6016 USDT` | `₹10,446.32` | `+10.60%` |
| **Net Realized PnL** | **`+10.6016 USDT`** | **`₹+1,001.32`** | **`+10.60% Net ROI`** |
| **Gross Profit** | `+24.2260 USDT` | `₹2,288.15` | Total positive trade returns |
| **Gross Loss** | `-13.6244 USDT` | `₹1,286.82` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.78`** | — | Profitable |
| **Win / Loss Payoff** | `5.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0600 USDT` | `₹5.67` | **`-0.05%` Peak-to-Trough** |
| **Win Rate** | **`26.23%`** | — | `12113 Wins / 34061 Losses / 1 Scratch` |
| **Sharpe Ratio (est)** | `17.06` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `45.27` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `194.25` | — | Net ROI divided by Max Drawdown |

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
| **Winning Trades** | `12113` | `26.23%` of total trades |
| **Losing Trades** | `34061` | `73.77%` of total trades |
| **Scratch / Break-even** | `1` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0002 USDT` (`₹+0.02`) | Expected return per signal |
| **Average Winning Trade** | `+0.0020 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0020 USDT (+6.0% ROE)` | Trade #160 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #152 (LONG) |
| **Max Consecutive Wins** | `16` trades | Peak winning streak |
| **Max Consecutive Losses** | `44` trades | Peak losing streak |
| **Average Trade Duration** | `1m 40s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #46175 |
| **Longest Trade In-Position** | `1h 11m 00s` | Trade #43789 |
| **Cumulative Time In Position** | `1289h 00m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `22890` (49.6%) | `23285` (50.4%) | `46175` |
| **Wins / Losses** | `6024 W / 16865 L` | `6089 W / 17196 L` | `12113 W / 34061 L` |
| **Win Rate** | **`26.32%`** | **`26.15%`** | **`26.23%`** |
| **Gross Profit** | `+12.0480 USDT` | `+12.1780 USDT` | `+24.2260 USDT` |
| **Gross Loss** | `-6.7460 USDT` | `-6.8784 USDT` | `-13.6244 USDT` |
| **Net Realized PnL** | **`+5.3020 USDT`** | **`+5.2996 USDT`** | **`+10.6016 USDT`** |
| **Net PnL (INR)** | `₹+500.77` | `₹+500.55` | `₹+1,001.32` |
| **Profit Factor** | `1.79` | `1.77` | `1.78` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `34061` | `73.8%` | `-13.6244 USDT` | `₹-1,286.82` | `0.0%` | `1m 31s` |
| `MIN_PROFIT_TP_HIT` | `12113` | `26.2%` | `+24.2260 USDT` | `₹+2,288.15` | `100.0%` | `2m 06s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:32:59 UTC | 2026-01-01 00:33:59 UTC | 1m 00s | `0.11787` | `0.11785` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `SHORT` | 2026-01-01 00:40:59 UTC | 2026-01-01 00:41:59 UTC | 1m 00s | `0.11778` | `0.11780` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `0.11775` | `0.11777` | $2.35 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 01:01:59 UTC | 7m 00s | `0.11782` | `0.11792` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 5 | `LONG` | 2026-01-01 01:05:59 UTC | 2026-01-01 01:06:59 UTC | 1m 00s | `0.11797` | `0.11795` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0004 |
| 6 | `LONG` | 2026-01-01 01:13:59 UTC | 2026-01-01 01:16:59 UTC | 3m 00s | `0.11838` | `0.11836` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0000 |
| 7 | `SHORT` | 2026-01-01 01:23:59 UTC | 2026-01-01 01:26:59 UTC | 3m 00s | `0.11822` | `0.11812` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 8 | `SHORT` | 2026-01-01 01:31:59 UTC | 2026-01-01 01:32:59 UTC | 1m 00s | `0.11814` | `0.11816` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 9 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:41:59 UTC | 3m 00s | `0.11817` | `0.11827` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 10 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:59 UTC | 1m 00s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0032 |
| 11 | `LONG` | 2026-01-01 01:55:59 UTC | 2026-01-01 01:56:59 UTC | 1m 00s | `0.11856` | `0.11854` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0028 |
| 12 | `LONG` | 2026-01-01 01:58:59 UTC | 2026-01-01 01:59:59 UTC | 1m 00s | `0.11849` | `0.11847` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0024 |
| 13 | `SHORT` | 2026-01-01 02:04:59 UTC | 2026-01-01 02:05:59 UTC | 1m 00s | `0.11847` | `0.11849` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0020 |
| 14 | `LONG` | 2026-01-01 02:09:59 UTC | 2026-01-01 02:10:59 UTC | 1m 00s | `0.11845` | `0.11843` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 15 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0012 |
| 16 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11844` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0008 |
| 17 | `LONG` | 2026-01-01 02:26:59 UTC | 2026-01-01 02:27:59 UTC | 1m 00s | `0.11839` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0004 |
| 18 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:59 UTC | 1m 00s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0000 |
| 19 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:43:59 UTC | 3m 00s | `0.11863` | `0.11853` | $2.37 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 20 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:50:59 UTC | 3m 00s | `0.11855` | `0.11857` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 21 | `SHORT` | 2026-01-01 03:03:59 UTC | 2026-01-01 03:05:59 UTC | 2m 00s | `0.11850` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 22 | `SHORT` | 2026-01-01 03:10:59 UTC | 2026-01-01 03:11:59 UTC | 1m 00s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0032 |
| 23 | `LONG` | 2026-01-01 03:17:59 UTC | 2026-01-01 03:18:59 UTC | 1m 00s | `0.11822` | `0.11820` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0028 |
| 24 | `LONG` | 2026-01-01 03:22:59 UTC | 2026-01-01 03:25:59 UTC | 3m 00s | `0.11817` | `0.11827` | $2.36 | $0.03 | $0.000000 | **+0.0020** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 25 | `LONG` | 2026-01-01 03:30:59 UTC | 2026-01-01 03:31:59 UTC | 1m 00s | `0.11843` | `0.11841` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0044 |
| ... | ... | *(46125 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 46151 | `LONG` | 2026-08-30 21:11:59 UTC | 2026-08-30 21:12:59 UTC | 1m 00s | `0.08459` | `0.08469` | $1.69 | $0.02 | $0.000000 | **+0.0020** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $110.5916 |
| 46152 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:59 UTC | 1m 00s | `0.08460` | `0.08458` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5912 |
| 46153 | `SHORT` | 2026-08-30 21:25:59 UTC | 2026-08-30 21:26:59 UTC | 1m 00s | `0.08446` | `0.08448` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5908 |
| 46154 | `LONG` | 2026-08-30 21:36:59 UTC | 2026-08-30 21:37:59 UTC | 1m 00s | `0.08480` | `0.08478` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5904 |
| 46155 | `SHORT` | 2026-08-30 21:45:59 UTC | 2026-08-30 21:46:59 UTC | 1m 00s | `0.08438` | `0.08440` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5900 |
| 46156 | `SHORT` | 2026-08-30 21:49:59 UTC | 2026-08-30 21:50:59 UTC | 1m 00s | `0.08435` | `0.08437` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5896 |
| 46157 | `LONG` | 2026-08-30 21:55:59 UTC | 2026-08-30 21:57:59 UTC | 2m 00s | `0.08446` | `0.08444` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5892 |
| 46158 | `LONG` | 2026-08-30 21:59:59 UTC | 2026-08-30 22:00:59 UTC | 1m 00s | `0.08458` | `0.08456` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5888 |
| 46159 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:59 UTC | 1m 00s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5884 |
| 46160 | `SHORT` | 2026-08-30 22:13:59 UTC | 2026-08-30 22:14:59 UTC | 1m 00s | `0.08423` | `0.08425` | $1.68 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5880 |
| 46161 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `0.08424` | `0.08414` | $1.68 | $0.02 | $0.000000 | **+0.0020** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $110.5900 |
| 46162 | `LONG` | 2026-08-30 22:22:59 UTC | 2026-08-30 22:23:59 UTC | 1m 00s | `0.08385` | `0.08395` | $1.68 | $0.02 | $0.000000 | **+0.0020** | `+8.9%` | `MIN_PROFIT_TP_HIT` | $110.5920 |
| 46163 | `SHORT` | 2026-08-30 22:29:59 UTC | 2026-08-30 22:30:59 UTC | 1m 00s | `0.08371` | `0.08361` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $110.5940 |
| 46164 | `LONG` | 2026-08-30 22:35:59 UTC | 2026-08-30 22:36:59 UTC | 1m 00s | `0.08358` | `0.08356` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5936 |
| 46165 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:59 UTC | 1m 00s | `0.08370` | `0.08368` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5932 |
| 46166 | `SHORT` | 2026-08-30 22:53:59 UTC | 2026-08-30 22:54:59 UTC | 1m 00s | `0.08359` | `0.08361` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5928 |
| 46167 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `0.08339` | `0.08349` | $1.67 | $0.02 | $0.000000 | **+0.0020** | `+9.0%` | `MIN_PROFIT_TP_HIT` | $110.5948 |
| 46168 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:59 UTC | 1m 00s | `0.08333` | `0.08331` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5944 |
| 46169 | `SHORT` | 2026-08-30 23:27:59 UTC | 2026-08-30 23:28:59 UTC | 1m 00s | `0.08245` | `0.08235` | $1.65 | $0.02 | $0.000000 | **+0.0020** | `+9.1%` | `MIN_PROFIT_TP_HIT` | $110.5964 |
| 46170 | `SHORT` | 2026-08-30 23:31:59 UTC | 2026-08-30 23:32:59 UTC | 1m 00s | `0.08215` | `0.08205` | $1.64 | $0.02 | $0.000000 | **+0.0020** | `+9.1%` | `MIN_PROFIT_TP_HIT` | $110.5984 |
| 46171 | `LONG` | 2026-08-30 23:36:59 UTC | 2026-08-30 23:37:59 UTC | 1m 00s | `0.08197` | `0.08195` | $1.64 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5980 |
| 46172 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:59 UTC | 1m 00s | `0.08150` | `0.08152` | $1.63 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $110.5976 |
| 46173 | `SHORT` | 2026-08-30 23:50:59 UTC | 2026-08-30 23:51:59 UTC | 1m 00s | `0.08156` | `0.08146` | $1.63 | $0.02 | $0.000000 | **+0.0020** | `+9.2%` | `MIN_PROFIT_TP_HIT` | $110.5996 |
| 46174 | `LONG` | 2026-08-30 23:54:59 UTC | 2026-08-30 23:55:59 UTC | 1m 00s | `0.08179` | `0.08189` | $1.64 | $0.02 | $0.000000 | **+0.0020** | `+9.2%` | `MIN_PROFIT_TP_HIT` | $110.6016 |
| 46175 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `0.08182` | `0.08182` | $1.64 | $0.02 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $110.6016 |

> 💡 *Full granular dataset with all 46175 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
