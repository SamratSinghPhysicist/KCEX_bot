# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 14:10:08 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0812 USDT` | `₹9,452.67` | `+0.08%` |
| **Net Realized PnL** | **`+0.0812 USDT`** | **`₹+7.67`** | **`+0.08% Net ROI`** |
| **Gross Profit** | `+5.2064 USDT` | `₹491.74` | Total positive trade returns |
| **Gross Loss** | `-5.1252 USDT` | `₹484.08` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.02`** | — | Profitable |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.1048 USDT` | `₹9.90` | **`-0.10%` Peak-to-Trough** |
| **Win Rate** | **`50.39%`** | — | `13016 Wins / 12813 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `0.61` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `0.61` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `0.78` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `DOGE_USDT` | Base Asset: `DOGE` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `SMART_STRATEGY` | SMART_STRATEGY |
| **Strategy Preset** | `DEFAULT` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-01-01` → `2026-08-31` | Historical evaluation window |
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.00000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

### Strategy & Indicator Hyperparameters
| Hyperparameter | Value | Technical Context |
| :--- | :--- | :--- |
| **Active Strategy Engine** | `SMART_STRATEGY` | Quantitative model evaluated |
| **Active Strategy Preset** | `DEFAULT` | Selected preset configuration |
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
| **Total Trades Executed** | `25829` | Total completed trade lifecycle events |
| **Winning Trades** | `13016` | `50.39%` of total trades |
| **Losing Trades** | `12813` | `49.61%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+1.2% ROE)` | Trade #85 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #78 (SHORT) |
| **Max Consecutive Wins** | `15` trades | Peak winning streak |
| **Max Consecutive Losses** | `19` trades | Peak losing streak |
| **Average Trade Duration** | `12.4s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #49 |
| **Longest Trade In-Position** | `9m 47s` | Trade #24541 |
| **Cumulative Time In Position** | `89h 19m 01s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `13056` (50.5%) | `12773` (49.5%) | `25829` |
| **Wins / Losses** | `6695 W / 6361 L` | `6321 W / 6452 L` | `13016 W / 12813 L` |
| **Win Rate** | **`51.28%`** | **`49.49%`** | **`50.39%`** |
| **Gross Profit** | `+2.6780 USDT` | `+2.5284 USDT` | `+5.2064 USDT` |
| **Gross Loss** | `-2.5444 USDT` | `-2.5808 USDT` | `-5.1252 USDT` |
| **Net Realized PnL** | **`+0.1336 USDT`** | **`-0.0524 USDT`** | **`+0.0812 USDT`** |
| **Net PnL (INR)** | `₹+12.62` | `₹-4.95` | `₹+7.67` |
| **Profit Factor** | `1.05` | `0.98` | `1.02` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `12813` | `49.6%` | `-5.1252 USDT` | `₹-484.08` | `0.0%` | `12.4s` |
| `MIN_PROFIT_TP_HIT` | `13016` | `50.4%` | `+5.2064 USDT` | `₹+491.74` | `100.0%` | `12.5s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:39:59 UTC | 2026-01-01 00:40:00 UTC | 0.5s | `0.11774` | `0.11772` | $2.35 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `LONG` | 2026-01-01 00:41:59 UTC | 2026-01-01 00:42:20 UTC | 20.3s | `0.11776` | `0.11774` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9992 |
| 3 | `SHORT` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:01 UTC | 1.2s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 4 | `SHORT` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:03 UTC | 3.2s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 5 | `LONG` | 2026-01-01 02:05:59 UTC | 2026-01-01 02:06:03 UTC | 3.1s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 6 | `LONG` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:04 UTC | 5.0s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 7 | `LONG` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:11 UTC | 11.6s | `0.11842` | `0.11840` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 8 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:00 UTC | 0.7s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 9 | `LONG` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:09 UTC | 9.2s | `0.11863` | `0.11861` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9988 |
| 10 | `LONG` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:26 UTC | 1m 26s | `0.11855` | `0.11853` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9984 |
| 11 | `LONG` | 2026-01-01 03:47:59 UTC | 2026-01-01 03:48:08 UTC | 8.9s | `0.11848` | `0.11846` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9980 |
| 12 | `LONG` | 2026-01-01 03:53:59 UTC | 2026-01-01 03:54:48 UTC | 48.9s | `0.11823` | `0.11821` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9976 |
| 13 | `SHORT` | 2026-01-01 04:05:59 UTC | 2026-01-01 04:06:10 UTC | 10.6s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9972 |
| 14 | `SHORT` | 2026-01-01 04:08:59 UTC | 2026-01-01 04:09:08 UTC | 8.1s | `0.11808` | `0.11810` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9968 |
| 15 | `LONG` | 2026-01-01 04:12:59 UTC | 2026-01-01 04:13:00 UTC | 0.3s | `0.11820` | `0.11822` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9972 |
| 16 | `SHORT` | 2026-01-01 04:17:59 UTC | 2026-01-01 04:18:12 UTC | 12.8s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9968 |
| 17 | `LONG` | 2026-01-01 04:42:59 UTC | 2026-01-01 04:43:05 UTC | 5.2s | `0.11806` | `0.11808` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9972 |
| 18 | `SHORT` | 2026-01-01 05:05:59 UTC | 2026-01-01 05:06:04 UTC | 4.1s | `0.11816` | `0.11818` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9968 |
| 19 | `LONG` | 2026-01-01 05:43:59 UTC | 2026-01-01 05:44:18 UTC | 18.1s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9964 |
| 20 | `LONG` | 2026-01-01 06:12:59 UTC | 2026-01-01 06:13:20 UTC | 20.1s | `0.11843` | `0.11845` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 21 | `SHORT` | 2026-01-01 06:18:59 UTC | 2026-01-01 06:19:00 UTC | 0.2s | `0.11849` | `0.11851` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9964 |
| 22 | `LONG` | 2026-01-01 06:33:59 UTC | 2026-01-01 06:34:17 UTC | 17.8s | `0.11831` | `0.11833` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9968 |
| 23 | `SHORT` | 2026-01-01 06:54:59 UTC | 2026-01-01 06:56:02 UTC | 1m 02s | `0.11838` | `0.11840` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9964 |
| 24 | `SHORT` | 2026-01-01 06:58:59 UTC | 2026-01-01 06:59:15 UTC | 15.0s | `0.11835` | `0.11837` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $99.9960 |
| 25 | `SHORT` | 2026-01-01 07:04:59 UTC | 2026-01-01 07:05:31 UTC | 31.3s | `0.11858` | `0.11856` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $99.9964 |
| ... | ... | *(25779 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 25805 | `SHORT` | 2026-08-30 15:11:59 UTC | 2026-08-30 15:12:06 UTC | 6.1s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0780 |
| 25806 | `LONG` | 2026-08-30 15:17:59 UTC | 2026-08-30 15:18:20 UTC | 20.9s | `0.08521` | `0.08523` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0784 |
| 25807 | `SHORT` | 2026-08-30 15:21:59 UTC | 2026-08-30 15:22:07 UTC | 7.2s | `0.08524` | `0.08526` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0780 |
| 25808 | `SHORT` | 2026-08-30 15:28:59 UTC | 2026-08-30 15:29:06 UTC | 6.2s | `0.08526` | `0.08524` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0784 |
| 25809 | `SHORT` | 2026-08-30 15:35:59 UTC | 2026-08-30 15:36:01 UTC | 1.5s | `0.08539` | `0.08541` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0780 |
| 25810 | `LONG` | 2026-08-30 15:54:59 UTC | 2026-08-30 15:55:11 UTC | 11.7s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0776 |
| 25811 | `SHORT` | 2026-08-30 16:07:59 UTC | 2026-08-30 16:08:02 UTC | 2.0s | `0.08545` | `0.08547` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0772 |
| 25812 | `LONG` | 2026-08-30 16:30:59 UTC | 2026-08-30 16:31:15 UTC | 15.6s | `0.08569` | `0.08571` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0776 |
| 25813 | `SHORT` | 2026-08-30 16:39:59 UTC | 2026-08-30 16:40:01 UTC | 1.9s | `0.08582` | `0.08580` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0780 |
| 25814 | `LONG` | 2026-08-30 17:09:59 UTC | 2026-08-30 17:10:04 UTC | 4.5s | `0.08627` | `0.08629` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0784 |
| 25815 | `SHORT` | 2026-08-30 17:16:59 UTC | 2026-08-30 17:17:00 UTC | 0.1s | `0.08601` | `0.08599` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0788 |
| 25816 | `SHORT` | 2026-08-30 18:02:59 UTC | 2026-08-30 18:03:00 UTC | 0.6s | `0.08584` | `0.08586` | $1.72 | $0.02 | $0.000000 | **-0.0004** | `-1.7%` | `STOP_LOSS_HIT` | $100.0784 |
| 25817 | `LONG` | 2026-08-30 18:12:59 UTC | 2026-08-30 18:13:11 UTC | 11.5s | `0.08559` | `0.08557` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $100.0780 |
| 25818 | `SHORT` | 2026-08-30 18:21:59 UTC | 2026-08-30 18:22:01 UTC | 1.8s | `0.08585` | `0.08587` | $1.72 | $0.02 | $0.000000 | **-0.0004** | `-1.7%` | `STOP_LOSS_HIT` | $100.0776 |
| 25819 | `SHORT` | 2026-08-30 18:54:59 UTC | 2026-08-30 18:55:21 UTC | 21.8s | `0.08629` | `0.08627` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0780 |
| 25820 | `LONG` | 2026-08-30 18:59:59 UTC | 2026-08-30 19:00:09 UTC | 9.7s | `0.08631` | `0.08629` | $1.73 | $0.02 | $0.000000 | **-0.0004** | `-1.7%` | `STOP_LOSS_HIT` | $100.0776 |
| 25821 | `LONG` | 2026-08-30 19:14:59 UTC | 2026-08-30 19:15:10 UTC | 10.6s | `0.08628` | `0.08630` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0780 |
| 25822 | `LONG` | 2026-08-30 19:30:59 UTC | 2026-08-30 19:31:10 UTC | 10.6s | `0.08600` | `0.08602` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0784 |
| 25823 | `LONG` | 2026-08-30 20:10:59 UTC | 2026-08-30 20:11:31 UTC | 31.2s | `0.08581` | `0.08583` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $100.0788 |
| 25824 | `LONG` | 2026-08-30 20:21:59 UTC | 2026-08-30 20:22:12 UTC | 12.5s | `0.08568` | `0.08570` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0792 |
| 25825 | `SHORT` | 2026-08-30 20:27:59 UTC | 2026-08-30 20:28:13 UTC | 13.3s | `0.08571` | `0.08569` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0796 |
| 25826 | `SHORT` | 2026-08-30 20:58:59 UTC | 2026-08-30 20:59:03 UTC | 3.1s | `0.08511` | `0.08509` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0800 |
| 25827 | `SHORT` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:06 UTC | 7.0s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0804 |
| 25828 | `SHORT` | 2026-08-30 22:46:59 UTC | 2026-08-30 22:47:01 UTC | 2.0s | `0.08361` | `0.08359` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0808 |
| 25829 | `SHORT` | 2026-08-30 23:01:59 UTC | 2026-08-30 23:02:00 UTC | 0.9s | `0.08352` | `0.08350` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $100.0812 |

> 💡 *Full granular dataset with all 25829 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
