# 📊 Institutional Backtest Performance Report: DOGE_USDT

> **Generated:** `2026-09-06 13:09:14 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `103.8132 USDT` | `₹9,805.16` | `+3.81%` |
| **Net Realized PnL** | **`+3.8132 USDT`** | **`₹+360.16`** | **`+3.81% Net ROI`** |
| **Gross Profit** | `+7.0724 USDT` | `₹667.99` | Total positive trade returns |
| **Gross Loss** | `-3.2592 USDT` | `₹307.83` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`2.17`** | — | Exceptional (Institutional Grade) |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0076 USDT` | `₹0.72` | **`-0.01%` Peak-to-Trough** |
| **Win Rate** | **`68.45%`** | — | `17681 Wins / 8148 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `30.95` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `28.79` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `518.81` | — | Net ROI divided by Max Drawdown |

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
| **High-Fidelity Simulation** | `DISABLED (Candle OHLC)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.00000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

### Strategy & Indicator Hyperparameters
| Hyperparameter | Value | Technical Context |
| :--- | :--- | :--- |
| **Active Strategy Engine** | `SMART_STRATEGY` | Quantitative model evaluated |
| **Active Strategy Preset** | `DEFAULT` | Selected preset configuration |
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
| **Winning Trades** | `17681` | `68.45%` of total trades |
| **Losing Trades** | `8148` | `31.55%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0001 USDT` (`₹+0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+1.2% ROE)` | Trade #78 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-1.2% ROE)` | Trade #89 (LONG) |
| **Max Consecutive Wins** | `43` trades | Peak winning streak |
| **Max Consecutive Losses** | `10` trades | Peak losing streak |
| **Average Trade Duration** | `1m 03s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `1m 00s` | Trade #1 |
| **Longest Trade In-Position** | `10m 00s` | Trade #24363 |
| **Cumulative Time In Position** | `453h 52m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `12773` (49.5%) | `13056` (50.5%) | `25829` |
| **Wins / Losses** | `8760 W / 4013 L` | `8921 W / 4135 L` | `17681 W / 8148 L` |
| **Win Rate** | **`68.58%`** | **`68.33%`** | **`68.45%`** |
| **Gross Profit** | `+3.5040 USDT` | `+3.5684 USDT` | `+7.0724 USDT` |
| **Gross Loss** | `-1.6052 USDT` | `-1.6540 USDT` | `-3.2592 USDT` |
| **Net Realized PnL** | **`+1.8988 USDT`** | **`+1.9144 USDT`** | **`+3.8132 USDT`** |
| **Net PnL (INR)** | `₹+179.34` | `₹+180.82` | `₹+360.16` |
| **Profit Factor** | `2.18` | `2.16` | `2.17` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `17681` | `68.5%` | `+7.0724 USDT` | `₹+667.99` | `100.0%` | `1m 02s` |
| `STOP_LOSS_HIT` | `8148` | `31.5%` | `-3.2592 USDT` | `₹-307.83` | `0.0%` | `1m 04s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:39:59 UTC | 2026-01-01 00:40:59 UTC | 1m 00s | `0.11774` | `0.11772` | $2.35 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 00:41:59 UTC | 2026-01-01 00:42:59 UTC | 1m 00s | `0.11776` | `0.11774` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 3 | `LONG` | 2026-01-01 01:38:59 UTC | 2026-01-01 01:39:59 UTC | 1m 00s | `0.11817` | `0.11819` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 4 | `LONG` | 2026-01-01 01:43:59 UTC | 2026-01-01 01:44:59 UTC | 1m 00s | `0.11831` | `0.11829` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0008 |
| 5 | `SHORT` | 2026-01-01 02:05:59 UTC | 2026-01-01 02:06:59 UTC | 1m 00s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 6 | `SHORT` | 2026-01-01 02:15:59 UTC | 2026-01-01 02:16:59 UTC | 1m 00s | `0.11830` | `0.11828` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0016 |
| 7 | `SHORT` | 2026-01-01 02:18:59 UTC | 2026-01-01 02:19:59 UTC | 1m 00s | `0.11842` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 8 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:36:59 UTC | 1m 00s | `0.11854` | `0.11852` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0016 |
| 9 | `SHORT` | 2026-01-01 02:40:59 UTC | 2026-01-01 02:41:59 UTC | 1m 00s | `0.11863` | `0.11861` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0020 |
| 10 | `SHORT` | 2026-01-01 02:47:59 UTC | 2026-01-01 02:49:59 UTC | 2m 00s | `0.11855` | `0.11853` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0024 |
| 11 | `SHORT` | 2026-01-01 03:47:59 UTC | 2026-01-01 03:48:59 UTC | 1m 00s | `0.11848` | `0.11846` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0028 |
| 12 | `SHORT` | 2026-01-01 03:53:59 UTC | 2026-01-01 03:54:59 UTC | 1m 00s | `0.11823` | `0.11821` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0032 |
| 13 | `LONG` | 2026-01-01 04:05:59 UTC | 2026-01-01 04:06:59 UTC | 1m 00s | `0.11830` | `0.11832` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0036 |
| 14 | `LONG` | 2026-01-01 04:08:59 UTC | 2026-01-01 04:09:59 UTC | 1m 00s | `0.11808` | `0.11810` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 15 | `SHORT` | 2026-01-01 04:12:59 UTC | 2026-01-01 04:13:59 UTC | 1m 00s | `0.11820` | `0.11822` | $2.36 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0036 |
| 16 | `LONG` | 2026-01-01 04:17:59 UTC | 2026-01-01 04:18:59 UTC | 1m 00s | `0.11826` | `0.11828` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0040 |
| 17 | `SHORT` | 2026-01-01 04:42:59 UTC | 2026-01-01 04:43:59 UTC | 1m 00s | `0.11806` | `0.11804` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0044 |
| 18 | `LONG` | 2026-01-01 05:05:59 UTC | 2026-01-01 05:06:59 UTC | 1m 00s | `0.11816` | `0.11818` | $2.36 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0048 |
| 19 | `SHORT` | 2026-01-01 05:43:59 UTC | 2026-01-01 05:44:59 UTC | 1m 00s | `0.11850` | `0.11848` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 20 | `SHORT` | 2026-01-01 06:12:59 UTC | 2026-01-01 06:13:59 UTC | 1m 00s | `0.11843` | `0.11845` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0048 |
| 21 | `LONG` | 2026-01-01 06:18:59 UTC | 2026-01-01 06:19:59 UTC | 1m 00s | `0.11849` | `0.11851` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 22 | `SHORT` | 2026-01-01 06:33:59 UTC | 2026-01-01 06:34:59 UTC | 1m 00s | `0.11831` | `0.11833` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0048 |
| 23 | `LONG` | 2026-01-01 06:54:59 UTC | 2026-01-01 06:56:59 UTC | 2m 00s | `0.11838` | `0.11840` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0052 |
| 24 | `LONG` | 2026-01-01 06:58:59 UTC | 2026-01-01 06:59:59 UTC | 1m 00s | `0.11835` | `0.11837` | $2.37 | $0.03 | $0.000000 | **+0.0004** | `+1.3%` | `MIN_PROFIT_TP_HIT` | $100.0056 |
| 25 | `LONG` | 2026-01-01 07:04:59 UTC | 2026-01-01 07:05:59 UTC | 1m 00s | `0.11858` | `0.11856` | $2.37 | $0.03 | $0.000000 | **-0.0004** | `-1.3%` | `STOP_LOSS_HIT` | $100.0052 |
| ... | ... | *(25779 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 25805 | `LONG` | 2026-08-30 15:11:59 UTC | 2026-08-30 15:12:59 UTC | 1m 00s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8084 |
| 25806 | `SHORT` | 2026-08-30 15:17:59 UTC | 2026-08-30 15:18:59 UTC | 1m 00s | `0.08521` | `0.08519` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8088 |
| 25807 | `LONG` | 2026-08-30 15:21:59 UTC | 2026-08-30 15:22:59 UTC | 1m 00s | `0.08524` | `0.08526` | $1.70 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8092 |
| 25808 | `LONG` | 2026-08-30 15:28:59 UTC | 2026-08-30 15:29:59 UTC | 1m 00s | `0.08526` | `0.08524` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8088 |
| 25809 | `LONG` | 2026-08-30 15:35:59 UTC | 2026-08-30 15:36:59 UTC | 1m 00s | `0.08539` | `0.08541` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8092 |
| 25810 | `SHORT` | 2026-08-30 15:54:59 UTC | 2026-08-30 15:55:59 UTC | 1m 00s | `0.08528` | `0.08526` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8096 |
| 25811 | `LONG` | 2026-08-30 16:07:59 UTC | 2026-08-30 16:08:59 UTC | 1m 00s | `0.08545` | `0.08547` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8100 |
| 25812 | `SHORT` | 2026-08-30 16:30:59 UTC | 2026-08-30 16:31:59 UTC | 1m 00s | `0.08569` | `0.08571` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8096 |
| 25813 | `LONG` | 2026-08-30 16:39:59 UTC | 2026-08-30 16:40:59 UTC | 1m 00s | `0.08582` | `0.08584` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8100 |
| 25814 | `SHORT` | 2026-08-30 17:09:59 UTC | 2026-08-30 17:10:59 UTC | 1m 00s | `0.08627` | `0.08625` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8104 |
| 25815 | `LONG` | 2026-08-30 17:16:59 UTC | 2026-08-30 17:17:59 UTC | 1m 00s | `0.08601` | `0.08603` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8108 |
| 25816 | `LONG` | 2026-08-30 18:02:59 UTC | 2026-08-30 18:03:59 UTC | 1m 00s | `0.08584` | `0.08586` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8112 |
| 25817 | `SHORT` | 2026-08-30 18:12:59 UTC | 2026-08-30 18:13:59 UTC | 1m 00s | `0.08559` | `0.08557` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8116 |
| 25818 | `LONG` | 2026-08-30 18:21:59 UTC | 2026-08-30 18:22:59 UTC | 1m 00s | `0.08585` | `0.08587` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8120 |
| 25819 | `LONG` | 2026-08-30 18:54:59 UTC | 2026-08-30 18:55:59 UTC | 1m 00s | `0.08629` | `0.08631` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8124 |
| 25820 | `SHORT` | 2026-08-30 18:59:59 UTC | 2026-08-30 19:00:59 UTC | 1m 00s | `0.08631` | `0.08629` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8128 |
| 25821 | `SHORT` | 2026-08-30 19:14:59 UTC | 2026-08-30 19:15:59 UTC | 1m 00s | `0.08628` | `0.08626` | $1.73 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8132 |
| 25822 | `SHORT` | 2026-08-30 19:30:59 UTC | 2026-08-30 19:31:59 UTC | 1m 00s | `0.08600` | `0.08598` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8136 |
| 25823 | `SHORT` | 2026-08-30 20:10:59 UTC | 2026-08-30 20:11:59 UTC | 1m 00s | `0.08581` | `0.08579` | $1.72 | $0.02 | $0.000000 | **+0.0004** | `+1.7%` | `MIN_PROFIT_TP_HIT` | $103.8140 |
| 25824 | `SHORT` | 2026-08-30 20:21:59 UTC | 2026-08-30 20:22:59 UTC | 1m 00s | `0.08568` | `0.08566` | $1.71 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8144 |
| 25825 | `LONG` | 2026-08-30 20:27:59 UTC | 2026-08-30 20:28:59 UTC | 1m 00s | `0.08571` | `0.08569` | $1.71 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8140 |
| 25826 | `LONG` | 2026-08-30 20:58:59 UTC | 2026-08-30 20:59:59 UTC | 1m 00s | `0.08511` | `0.08509` | $1.70 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8136 |
| 25827 | `LONG` | 2026-08-30 22:05:59 UTC | 2026-08-30 22:06:59 UTC | 1m 00s | `0.08465` | `0.08463` | $1.69 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8132 |
| 25828 | `LONG` | 2026-08-30 22:46:59 UTC | 2026-08-30 22:47:59 UTC | 1m 00s | `0.08361` | `0.08363` | $1.67 | $0.02 | $0.000000 | **+0.0004** | `+1.8%` | `MIN_PROFIT_TP_HIT` | $103.8136 |
| 25829 | `LONG` | 2026-08-30 23:01:59 UTC | 2026-08-30 23:02:59 UTC | 1m 00s | `0.08352` | `0.08350` | $1.67 | $0.02 | $0.000000 | **-0.0004** | `-1.8%` | `STOP_LOSS_HIT` | $103.8132 |

> 💡 *Full granular dataset with all 25829 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
