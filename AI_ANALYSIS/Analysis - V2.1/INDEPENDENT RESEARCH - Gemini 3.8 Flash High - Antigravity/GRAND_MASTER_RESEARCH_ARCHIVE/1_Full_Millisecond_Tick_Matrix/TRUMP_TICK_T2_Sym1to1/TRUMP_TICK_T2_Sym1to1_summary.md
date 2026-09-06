# 📊 Institutional Backtest Performance Report: TRUMP_USDT

> **Generated:** `2026-09-06 14:08:29 UTC` | **Engine:** `KCEX High-Fidelity Dual-Feed Simulator v1.3`

---

## ⚡ Executive Scorecard

| Performance Metric | USDT Value | INR Value (₹94.45) | % Return / Ratio |
| :--- | :--- | :--- | :--- |
| **Initial Capital** | `100.0000 USDT` | `₹9,445.00` | Baseline (100.0%) |
| **Final Balance** | `100.0920 USDT` | `₹9,453.69` | `+0.09%` |
| **Net Realized PnL** | **`+0.0920 USDT`** | **`₹+8.69`** | **`+0.09% Net ROI`** |
| **Gross Profit** | `+9.1756 USDT` | `₹866.64` | Total positive trade returns |
| **Gross Loss** | `-9.0836 USDT` | `₹857.95` | Total negative trade drawdowns |
| **Total Taker Fees Paid** | `0.000000 USDT` | `₹0.00` | `0.0000% of capital` |
| **Profit Factor** | **`1.01`** | — | Profitable |
| **Win / Loss Payoff** | `1.00` | — | Average Win vs Average Loss ratio |
| **Max Drawdown** | `-0.0764 USDT` | `₹7.22` | **`-0.08%` Peak-to-Trough** |
| **Win Rate** | **`50.25%`** | — | `22939 Wins / 22709 Losses / 0 Scratch` |
| **Sharpe Ratio (est)** | `0.39` | — | Annualized risk-adjusted excess return |
| **Sortino Ratio** | `0.39` | — | Downside risk-adjusted return ratio |
| **Calmar Ratio** | `1.21` | — | Net ROI divided by Max Drawdown |

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
| **High-Fidelity Simulation** | `ENABLED (Tick Trades)` | Millisecond-level trade order matching & stop triggering |
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
| **Winning Trades** | `22939` | `50.25%` of total trades |
| **Losing Trades** | `22709` | `49.75%` of total trades |
| **Scratch / Break-even** | `0` | `0.00%` of total trades |
| **Average Trade PnL** | `+0.0000 USDT` (`₹+0.00`) | Expected return per signal |
| **Average Winning Trade** | `+0.0004 USDT` | Average gain when trade hits TP |
| **Average Losing Trade** | `-0.0004 USDT` | Average loss when trade hits SL |
| **Largest Winning Trade** | `+0.0004 USDT (+3.1% ROE)` | Trade #10 (LONG) |
| **Largest Losing Trade** | `-0.0004 USDT (-3.1% ROE)` | Trade #3 (LONG) |
| **Max Consecutive Wins** | `15` trades | Peak winning streak |
| **Max Consecutive Losses** | `15` trades | Peak losing streak |
| **Average Trade Duration** | `55.5s` | Mean time from entry to exit fill |
| **Fastest Trade Fill** | `0.1s` | Trade #31 |
| **Longest Trade In-Position** | `48m 43s` | Trade #39643 |
| **Cumulative Time In Position** | `704h 14m 06s` | Total market exposure duration |

---

## 🧭 Directional Performance Analysis (LONG vs SHORT)

| Metric | LONG Trades | SHORT Trades | Combined Total |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `22845` (50.0%) | `22803` (50.0%) | `45648` |
| **Wins / Losses** | `11395 W / 11450 L` | `11544 W / 11259 L` | `22939 W / 22709 L` |
| **Win Rate** | **`49.88%`** | **`50.62%`** | **`50.25%`** |
| **Gross Profit** | `+4.5580 USDT` | `+4.6176 USDT` | `+9.1756 USDT` |
| **Gross Loss** | `-4.5800 USDT` | `-4.5036 USDT` | `-9.0836 USDT` |
| **Net Realized PnL** | **`-0.0220 USDT`** | **`+0.1140 USDT`** | **`+0.0920 USDT`** |
| **Net PnL (INR)** | `₹-2.08` | `₹+10.77` | `₹+8.69` |
| **Profit Factor** | `1.00` | `1.03` | `1.01` |

---

## 🎯 Exit Reason & Outcome Attribution

| Exit Reason Trigger | Count | % of Trades | Total PnL (USDT) | Total PnL (INR) | Win Rate | Avg Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STOP_LOSS_HIT` | `22709` | `49.7%` | `-9.0836 USDT` | `₹-857.95` | `0.0%` | `55.9s` |
| `MIN_PROFIT_TP_HIT` | `22939` | `50.3%` | `+9.1756 USDT` | `₹+866.64` | `100.0%` | `55.1s` |

---

## 📜 Detailed Trade Journal

| # | Dir | Entry Time (UTC) | Exit Time (UTC) | Duration | Entry Price | Exit Price | Notional | Margin | Fee (USDT) | Net PnL (USDT) | ROE % | Exit Reason | Ending Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SHORT` | 2026-01-01 00:27:59 UTC | 2026-01-01 00:29:45 UTC | 1m 45s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 2 | `LONG` | 2026-01-01 00:36:59 UTC | 2026-01-01 00:38:32 UTC | 1m 32s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 3 | `LONG` | 2026-01-01 00:43:59 UTC | 2026-01-01 00:44:04 UTC | 4.6s | `4.807` | `4.805` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 4 | `LONG` | 2026-01-01 00:49:59 UTC | 2026-01-01 00:50:19 UTC | 20.0s | `4.809` | `4.811` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 5 | `SHORT` | 2026-01-01 00:54:59 UTC | 2026-01-01 00:57:12 UTC | 2m 12s | `4.808` | `4.810` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 6 | `SHORT` | 2026-01-01 01:03:59 UTC | 2026-01-01 01:04:12 UTC | 12.7s | `4.816` | `4.818` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 7 | `SHORT` | 2026-01-01 01:11:59 UTC | 2026-01-01 01:12:02 UTC | 2.2s | `4.822` | `4.820` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 8 | `LONG` | 2026-01-01 01:17:59 UTC | 2026-01-01 01:18:14 UTC | 14.0s | `4.816` | `4.814` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 9 | `LONG` | 2026-01-01 01:25:59 UTC | 2026-01-01 01:26:07 UTC | 7.9s | `4.809` | `4.807` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 10 | `LONG` | 2026-01-01 01:30:59 UTC | 2026-01-01 01:31:06 UTC | 6.2s | `4.805` | `4.807` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 11 | `SHORT` | 2026-01-01 01:34:59 UTC | 2026-01-01 01:38:04 UTC | 3m 04s | `4.805` | `4.803` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 12 | `SHORT` | 2026-01-01 01:46:59 UTC | 2026-01-01 01:47:37 UTC | 37.3s | `4.807` | `4.809` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 13 | `SHORT` | 2026-01-01 01:50:59 UTC | 2026-01-01 01:51:30 UTC | 30.9s | `4.806` | `4.808` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 14 | `LONG` | 2026-01-01 02:01:59 UTC | 2026-01-01 02:02:05 UTC | 5.3s | `4.800` | `4.802` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 15 | `LONG` | 2026-01-01 02:03:59 UTC | 2026-01-01 02:04:31 UTC | 31.6s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 16 | `LONG` | 2026-01-01 02:08:59 UTC | 2026-01-01 02:09:05 UTC | 5.1s | `4.797` | `4.799` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 17 | `SHORT` | 2026-01-01 02:13:59 UTC | 2026-01-01 02:15:39 UTC | 1m 39s | `4.799` | `4.797` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 18 | `SHORT` | 2026-01-01 02:21:59 UTC | 2026-01-01 02:22:08 UTC | 8.0s | `4.796` | `4.798` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9992 |
| 19 | `LONG` | 2026-01-01 02:31:59 UTC | 2026-01-01 02:32:05 UTC | 5.6s | `4.793` | `4.791` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9988 |
| 20 | `SHORT` | 2026-01-01 02:35:59 UTC | 2026-01-01 02:37:19 UTC | 1m 19s | `4.794` | `4.792` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9992 |
| 21 | `LONG` | 2026-01-01 02:44:59 UTC | 2026-01-01 02:45:50 UTC | 51.0s | `4.782` | `4.784` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $99.9996 |
| 22 | `SHORT` | 2026-01-01 02:54:59 UTC | 2026-01-01 02:57:44 UTC | 2m 44s | `4.783` | `4.781` | $0.96 | $0.01 | $0.000000 | **+0.0004** | `+3.1%` | `MIN_PROFIT_TP_HIT` | $100.0000 |
| 23 | `SHORT` | 2026-01-01 02:58:59 UTC | 2026-01-01 02:59:00 UTC | 0.7s | `4.784` | `4.786` | $0.96 | $0.01 | $0.000000 | **-0.0004** | `-3.1%` | `STOP_LOSS_HIT` | $99.9996 |
| 24 | `SHORT` | 2026-01-01 03:01:59 UTC | 2026-01-01 03:02:00 UTC | 0.1s | `4.716` | `4.718` | $0.94 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $99.9992 |
| 25 | `SHORT` | 2026-01-01 03:13:59 UTC | 2026-01-01 03:14:14 UTC | 14.1s | `4.733` | `4.735` | $0.95 | $0.01 | $0.000000 | **-0.0004** | `-3.2%` | `STOP_LOSS_HIT` | $99.9988 |
| ... | ... | *(45598 intermediate trades logged in full .csv report)* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 45624 | `SHORT` | 2026-08-30 20:40:59 UTC | 2026-08-30 20:41:14 UTC | 14.5s | `2.514` | `2.516` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $100.0920 |
| 45625 | `LONG` | 2026-08-30 20:46:59 UTC | 2026-08-30 20:47:01 UTC | 1.6s | `2.518` | `2.516` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $100.0916 |
| 45626 | `SHORT` | 2026-08-30 20:50:59 UTC | 2026-08-30 20:51:06 UTC | 6.9s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $100.0912 |
| 45627 | `SHORT` | 2026-08-30 20:54:59 UTC | 2026-08-30 20:56:09 UTC | 1m 09s | `2.525` | `2.527` | $0.51 | $0.01 | $0.000000 | **-0.0004** | `-5.9%` | `STOP_LOSS_HIT` | $100.0908 |
| 45628 | `LONG` | 2026-08-30 21:03:59 UTC | 2026-08-30 21:04:03 UTC | 3.9s | `2.500` | `2.502` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.0912 |
| 45629 | `SHORT` | 2026-08-30 21:15:59 UTC | 2026-08-30 21:16:07 UTC | 7.4s | `2.503` | `2.501` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.0916 |
| 45630 | `SHORT` | 2026-08-30 21:32:59 UTC | 2026-08-30 21:33:09 UTC | 9.9s | `2.509` | `2.507` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45631 | `SHORT` | 2026-08-30 21:35:59 UTC | 2026-08-30 21:36:51 UTC | 51.1s | `2.510` | `2.512` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $100.0916 |
| 45632 | `LONG` | 2026-08-30 21:50:59 UTC | 2026-08-30 21:51:00 UTC | 0.5s | `2.488` | `2.490` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45633 | `SHORT` | 2026-08-30 21:58:59 UTC | 2026-08-30 21:59:02 UTC | 2.5s | `2.506` | `2.508` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $100.0916 |
| 45634 | `LONG` | 2026-08-30 22:09:59 UTC | 2026-08-30 22:10:03 UTC | 3.7s | `2.516` | `2.518` | $0.50 | $0.01 | $0.000000 | **+0.0004** | `+6.0%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45635 | `LONG` | 2026-08-30 22:19:59 UTC | 2026-08-30 22:20:18 UTC | 18.2s | `2.501` | `2.499` | $0.50 | $0.01 | $0.000000 | **-0.0004** | `-6.0%` | `STOP_LOSS_HIT` | $100.0916 |
| 45636 | `SHORT` | 2026-08-30 22:43:59 UTC | 2026-08-30 22:44:04 UTC | 4.8s | `2.429` | `2.427` | $0.49 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45637 | `LONG` | 2026-08-30 22:51:59 UTC | 2026-08-30 22:52:04 UTC | 4.7s | `2.416` | `2.418` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.0924 |
| 45638 | `SHORT` | 2026-08-30 22:56:59 UTC | 2026-08-30 22:57:22 UTC | 22.4s | `2.424` | `2.426` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $100.0920 |
| 45639 | `SHORT` | 2026-08-30 23:00:59 UTC | 2026-08-30 23:01:00 UTC | 0.4s | `2.409` | `2.411` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $100.0916 |
| 45640 | `SHORT` | 2026-08-30 23:10:59 UTC | 2026-08-30 23:11:01 UTC | 1.1s | `2.405` | `2.407` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $100.0912 |
| 45641 | `SHORT` | 2026-08-30 23:15:59 UTC | 2026-08-30 23:16:00 UTC | 0.8s | `2.422` | `2.420` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.0916 |
| 45642 | `SHORT` | 2026-08-30 23:18:59 UTC | 2026-08-30 23:19:00 UTC | 0.6s | `2.415` | `2.413` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.2%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45643 | `SHORT` | 2026-08-30 23:24:59 UTC | 2026-08-30 23:25:00 UTC | 0.4s | `2.414` | `2.416` | $0.48 | $0.01 | $0.000000 | **-0.0004** | `-6.2%` | `STOP_LOSS_HIT` | $100.0916 |
| 45644 | `LONG` | 2026-08-30 23:32:59 UTC | 2026-08-30 23:33:01 UTC | 1.6s | `2.388` | `2.390` | $0.48 | $0.01 | $0.000000 | **+0.0004** | `+6.3%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45645 | `LONG` | 2026-08-30 23:42:59 UTC | 2026-08-30 23:43:00 UTC | 0.7s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **-0.0004** | `-6.4%` | `STOP_LOSS_HIT` | $100.0916 |
| 45646 | `SHORT` | 2026-08-30 23:53:59 UTC | 2026-08-30 23:54:11 UTC | 11.8s | `2.330` | `2.328` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.0920 |
| 45647 | `SHORT` | 2026-08-30 23:57:59 UTC | 2026-08-30 23:58:00 UTC | 0.5s | `2.343` | `2.341` | $0.47 | $0.01 | $0.000000 | **+0.0004** | `+6.4%` | `MIN_PROFIT_TP_HIT` | $100.0924 |
| 45648 | `SHORT` | 2026-08-31 00:00:59 UTC | 2026-08-31 00:01:00 UTC | 0.9s | `2.338` | `2.340` | $0.47 | $0.01 | $0.000000 | **-0.0004** | `-6.4%` | `STOP_LOSS_HIT` | $100.0920 |

> 💡 *Full granular dataset with all 45648 trades is stored in the accompanying `trades.csv` and `trades.jsonl` artifacts.*
