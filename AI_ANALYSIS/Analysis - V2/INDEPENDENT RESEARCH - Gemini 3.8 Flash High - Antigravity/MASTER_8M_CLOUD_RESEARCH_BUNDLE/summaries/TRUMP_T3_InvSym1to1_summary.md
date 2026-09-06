# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 13:09:16 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `102.4844 USDT` | `₹9,679.65` | `+2.48%` |
| **Net Realized PnL** | **`+2.4844 USDT`** | **`₹+234.65`** | **`+2.48% Net ROI`** |
| **Gross Profit** | `+10.3716 USDT` | `₹979.60` | Total positive trade returns |
| **Gross Loss** | `-7.8872 USDT` | `₹744.95` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.31`** | — | Profitable |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0208 USDT` | `₹1.96` | **`-0.02%` Peak-to-Trough** |
| **Win Rate** | **`56.80%`** | — | `25929 Wins / 19718 Losses / 1 Scratch` |
| **Sharpe Ratio (est)** | `10.70` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `10.60` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `121.94` | — | Net ROI divided by Max Drawdown |

---

## 🛠️ Complete Configuration & Settings Used

### Strategy & Market Setup
| Configuration Setting | Value | Operational Details |
| :--- | :--- | :--- |
| **Trading Pair Symbol** | `TRUMP_USDT` | Base Asset: `TRUMP` / Quote Asset: `USDT` |
| **Candle Timeframe** | `1m` | Dynamic candle granularity evaluated by strategy indicators |
| **Strategy Evaluated** | `STOCH_RSI` | Stochastic RSI Momentum Scalper (Preset: FAST_SCALP ; Overbought/Oversold Reversal) |
| **Strategy Preset** | `FAST_SCALP` | Configured indicator preset profile |
| **Evaluation Date Range** | `2026-01-01` → `2026-08-31` | Historical evaluation window |
| **High-Fidelity Simulation** | `DISABLED (Candle OHLC)` | Millisecond-level trade order matching & stop triggering |
| **Slippage Tolerance** | `0 ticks` (`0.000 USDT` per fill) | Adverse fill penalty applied to entry and exit orders |

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
| **Trade Volume / Quantity** | `2 contract(s) (0.2 TRUMP per trade)` | Quantity committed per trade signal |
| **Leverage Multiplier** | `75x` | Margin required = Position Notional / Leverage |
| **Starting Capital** | `100.00 USDT` | `₹9,445.00 INR` (`1 USDT = ₹94.45`) |
| **Take Profit Target** | `+2 ticks` (`+0.002 USDT`) | Guaranteed Min-Profit TP (`entry + N*pu`) |
| **Stop Loss Rule** | `-2 ticks away from entry (0.002 USDT)` | Stop loss evaluation logic |

### Exchange Contract Specifications & Fees
| Specification | Value | Notes |
| :--- | :--- | :--- |
| **Fee Schedule Mode** | `ZERO` | Live KCEX API, 0.0% zero-fee pair, or manual rate |
| **Maker Fee Rate** | `0.0000%` | Rate for passive limit orders |
| **Taker Fee Rate** | `0.0000%` | Rate for aggressive market / stop triggers |
| **Contract Size (cs)** | `0.1 TRUMP` | 1 contract = 0.1 underlying coin |
| **Price Unit (pu / tick)** | `0.001` | Minimum tick increment on order book |
| **Price Precision** | `3 decimal places` | Precision formatting for quotes and orders |
| **Min Volume** | `1.0 contract(s)` | Minimum permissible order size |
| **Max Leverage** | `75x` | Maximum allowed leverage on exchange |

---

## 📈 Trade Execution & Statistical Breakdown

| Metric | Value | Context / Benchmark |
| :--- | :--- | :--- |
| **Total Trades Executed** | `45648` | Total completed trade lifecycle events |
| **Winning Trades** | `25929` | `56.80%` of total trades |
| **Losing Trades** | `19718` | `43.20%` of total trades |
| **Scratch / Break-even** | `1` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0001 USDT` (`₹+0.01`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.1% ROE)` | Trade #3 (SHORT) |
| **Largest Losing Trade** | `-0.0004 USDT (-3.1% ROE)` | Trade #10 (SHORT) |
| **Max Consecutive Wins** | `27` trades | Peak winning streak |
| **Max Consecutive Losses** | `13` trades | Peak losing streak |
| **Average Trade Duration** | `1m 37s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #45648 |
| **Longest Trade In-Position** | `49m 00s` | Trade #39643 |
| **Cumulative Time In Position** | `1232h 53m 00s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `22803` (50.0%) | `22845` (50.0%) | `45648` |
| **Wins / Losses** | `12850 W / 9952 L` | `13079 W / 9766 L` | `25929 W / 19718 L` |
| **Win Rate** | **`56.35%`** | **`57.25%`** | **`56.80%`** |
| **Gross Profit** | `+5.1400 USDT` | `+5.2316 USDT` | `+10.3716 USDT` |
| **Gross Loss** | `-3.9808 USDT` | `-3.9064 USDT` | `-7.8872 USDT` |
| **Net Realized PnL** | **`+1.1592 USDT`** | **`+1.3252 USDT`** | **`+2.4844 USDT`** |
| **Net PnL (INR)** | `₹+109.49` | `₹+125.17` | `₹+234.65` |
| **Profit Factor** | `1.29` | `1.34` | `1.31` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MIN_PROFIT_TP_HIT` | `25929` | `56.8%` | `+10.3716 USDT` | `₹+979.60` | `100.0%` | `1m 33s` |
| `STOP_LOSS_HIT` | `19718` | `43.2%` | `-7.8872 USDT` | `₹-744.95` | `0.0%` | `1m 41s` |
| `MANUAL_CLOSE` | `1` | `0.0%` | `+0.0000 USDT` | `₹+0.00` | `0.0%` | `0.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `LONG` | 2026-01-01 00:27:59 UTC | 2026-01-01 00:29:59 UTC | 2m 00s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 2 | `SHORT` | 2026-01-01 00:36:59 UTC | 2026-01-01 00:38:59 UTC | 2m 00s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 3 | `SHORT` | 2026-01-01 00:43:59 UTC | 2026-01-01 00:44:59 UTC | 1m 00s | `4.807` | `4.805` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 4 | `SHORT` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:59 UTC | 1m 00s | `4.809` | `4.811` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 5 | `LONG` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:57:59 UTC | 3m 00s | `4.808` | `4.810` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 6 | `LONG` | 2026-01-01 01:03:59 UTC | 2026-01-01 01:04:59 UTC | 1m 00s | `4.816` | `4.818` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 7 | `LONG` | 2026-01-01 01:11:59 UTC | 2026-01-01 01:12:59 UTC | 1m 00s | `4.822` | `4.820` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 8 | `SHORT` | 2026-01-01 01:17:59 UTC | 2026-01-01 01:18:59 UTC | 1m 00s | `4.816` | `4.814` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 9 | `SHORT` | 2026-01-01 01:25:59 UTC | 2026-01-01 01:26:59 UTC | 1m 00s | `4.809` | `4.807` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 10 | `SHORT` | 2026-01-01 01:30:59 UTC | 2026-01-01 01:31:59 UTC | 1m 00s | `4.805` | `4.807` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 11 | `LONG` | 2026-01-01 01:34:59 UTC | 2026-01-01 01:38:59 UTC | 4m 00s | `4.805` | `4.803` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 12 | `LONG` | 2026-01-01 01:46:59 UTC | 2026-01-01 01:47:59 UTC | 1m 00s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 13 | `LONG` | 2026-01-01 01:50:59 UTC | 2026-01-01 01:51:59 UTC | 1m 00s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 14 | `SHORT` | 2026-01-01 02:01:59 UTC | 2026-01-01 02:02:59 UTC | 1m 00s | `4.800` | `4.802` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 15 | `SHORT` | 2026-01-01 02:03:59 UTC | 2026-01-01 02:04:59 UTC | 1m 00s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 16 | `SHORT` | 2026-01-01 02:08:59 UTC | 2026-01-01 02:09:59 UTC | 1m 00s | `4.797` | `4.799` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 17 | `LONG` | 2026-01-01 02:13:59 UTC | 2026-01-01 02:15:59 UTC | 2m 00s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 18 | `LONG` | 2026-01-01 02:21:59 UTC | 2026-01-01 02:22:59 UTC | 1m 00s | `4.796` | `4.798` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 19 | `SHORT` | 2026-01-01 02:31:59 UTC | 2026-01-01 02:32:59 UTC | 1m 00s | `4.793` | `4.791` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| 20 | `LONG` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:37:59 UTC | 2m 00s | `4.794` | `4.792` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0008 |
| 21 | `SHORT` | 2026-01-01 02:44:59 UTC | 2026-01-01 02:45:59 UTC | 1m 00s | `4.782` | `4.784` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0004 |
| 22 | `LONG` | 2026-01-01 02:54:59 UTC | 2026-01-01 02:57:59 UTC | 3m 00s | `4.783` | `4.781` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $100.0000 |
| 23 | `LONG` | 2026-01-01 02:58:59 UTC | 2026-01-01 02:59:59 UTC | 1m 00s | `4.784` | `4.786` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0004 |
| 24 | `LONG` | 2026-01-01 03:01:59 UTC | 2026-01-01 03:02:59 UTC | 1m 00s | `4.716` | `4.718` | $0.94 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0008 |
| 25 | `LONG` | 2026-01-01 03:13:59 UTC | 2026-01-01 03:14:59 UTC | 1m 00s | `4.733` | `4.735` | $0.95 | $0.01 | $0.000000 | **+0.0004** | `+3.2%` | `MIN_PROFIT_TP_HIT` | $100.0012 |
| ... | ... | *(45598 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 45624 | `LONG` | 2026-08-30 20:40:59 UTC | 2026-08-30 20:41:59 UTC | 1m 00s | `2.514` | `2.516` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4800 |
| 45625 | `SHORT` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:47:59 UTC | 1m 00s | `2.518` | `2.516` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4804 |
| 45626 | `LONG` | 2026-08-30 20:50:59 UTC | 2026-08-30 20:51:59 UTC | 1m 00s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $102.4808 |
| 45627 | `LONG` | 2026-08-30 20:54:59 UTC | 2026-08-30 20:56:59 UTC | 2m 00s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **+0.0004** | `+5.9%` | `MIN_PROFIT_TP_HIT` | $102.4812 |
| 45628 | `SHORT` | 2026-08-30 21:03:59 UTC | 2026-08-30 21:04:59 UTC | 1m 00s | `2.500` | `2.502` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $102.4808 |
| 45629 | `LONG` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:59 UTC | 1m 00s | `2.503` | `2.501` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $102.4804 |
| 45630 | `LONG` | 2026-08-30 21:32:59 UTC | 2026-08-30 21:33:59 UTC | 1m 00s | `2.509` | `2.511` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4808 |
| 45631 | `LONG` | 2026-08-30 21:35:59 UTC | 2026-08-30 21:36:59 UTC | 1m 00s | `2.510` | `2.512` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4812 |
| 45632 | `SHORT` | 2026-08-30 21:50:59 UTC | 2026-08-30 21:51:59 UTC | 1m 00s | `2.488` | `2.490` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $102.4808 |
| 45633 | `LONG` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:59 UTC | 1m 00s | `2.506` | `2.508` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4812 |
| 45634 | `SHORT` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:59 UTC | 1m 00s | `2.516` | `2.514` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4816 |
| 45635 | `SHORT` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:59 UTC | 1m 00s | `2.501` | `2.499` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $102.4820 |
| 45636 | `LONG` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:59 UTC | 1m 00s | `2.429` | `2.427` | $0.49 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $102.4816 |
| 45637 | `SHORT` | 2026-08-30 22:51:59 UTC | 2026-08-30 22:52:59 UTC | 1m 00s | `2.416` | `2.418` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $102.4812 |
| 45638 | `LONG` | 2026-08-30 22:56:59 UTC | 2026-08-30 22:57:59 UTC | 1m 00s | `2.424` | `2.426` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $102.4816 |
| 45639 | `LONG` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:59 UTC | 1m 00s | `2.409` | `2.411` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $102.4820 |
| 45640 | `LONG` | 2026-08-30 23:10:59 UTC | 2026-08-30 23:11:59 UTC | 1m 00s | `2.405` | `2.407` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $102.4824 |
| 45641 | `LONG` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:59 UTC | 1m 00s | `2.422` | `2.420` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $102.4820 |
| 45642 | `LONG` | 2026-08-30 23:18:59 UTC | 2026-08-30 23:19:59 UTC | 1m 00s | `2.415` | `2.417` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $102.4824 |
| 45643 | `LONG` | 2026-08-30 23:24:59 UTC | 2026-08-30 23:25:59 UTC | 1m 00s | `2.414` | `2.416` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $102.4828 |
| 45644 | `SHORT` | 2026-08-30 23:32:59 UTC | 2026-08-30 23:33:59 UTC | 1m 00s | `2.388` | `2.386` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $102.4832 |
| 45645 | `SHORT` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:59 UTC | 1m 00s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $102.4836 |
| 45646 | `LONG` | 2026-08-30 23:53:59 UTC | 2026-08-30 23:54:59 UTC | 1m 00s | `2.330` | `2.332` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $102.4840 |
| 45647 | `LONG` | 2026-08-30 23:57:59 UTC | 2026-08-30 23:58:59 UTC | 1m 00s | `2.343` | `2.345` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $102.4844 |
| 45648 | `LONG` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:00:59 UTC | 0.1s | `2.338` | `2.338` | $0.47 | $0.01 | $0.000000 | **+0.0000** | `+0.0%` | `MANUAL_CLOSE` | $102.4844 |

> 💡 *Full granular dataset with all 45648 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
