# Final System Comparison: Baseline vs Candidate

## 1. High-Level Head-to-Head Scorecard

### TRUMP_USDT (Discovery Period: 2026-07-01 to 2026-07-24)
| Performance Metric | BASELINE SYSTEM (EXP_0001) | CANDIDATE SYSTEM (EXP_0007) | Difference / Delta |
| :--- | :--- | :--- | :--- |
| **Strategy Engine** | `STOCH_RSI (FAST_SCALP)` | `STOCH_RSI (FAST_SCALP)` | Identical |
| **Timeframe** | `1m` | `1m` | Identical |
| **Take Profit** | `+2 ticks (+0.002 USDT)` | `+2 ticks (+0.002 USDT)` | Identical |
| **Stop Loss Rule** | `-25.0% ROE (~10 ticks)` | `-5 ticks (Fixed)` | Capped risk |
| **Total Trades** | `3,066` | `3,114` | +48 trades (+1.6%) |
| **Win Rate** | `77.40%` | `76.11%` | -1.29% |
| **Average Win** | `+0.0004 USDT` | `+0.0004 USDT` | Identical |
| **Average Loss** | `-0.0011 USDT` | `-0.0010 USDT` | Capped strictly at 5 ticks |
| **Payoff Ratio (Loss:Win)** | `2.75 : 1` | `2.50 : 1` | Improved risk-reward |
| **Profit Factor** | `1.29` | `1.27` | -0.02 |
| **Net Realized PnL** | **`+0.2120 USDT`** | **`+0.2040 USDT`** | -$0.0080 USDT (96.2% retained) |
| **Net ROI %** | `+302.86%` | `+291.43%` | -11.43% |
| **Max Drawdown (%)** | **`12.69%`** | **`8.40%`** | **-33.8% Drawdown Reduction** |
| **Max Drawdown (USDT)** | `0.0136 USDT` | `0.0092 USDT` | -$0.0044 USDT lower peak drop |
| **PnL per Trade** | `+0.000069 USDT` | `+0.000065 USDT` | Stable expectancy |
| **PnL per Unit Time** | `+0.0088 USDT / day` | `+0.0085 USDT / day` | Highly consistent payload |

---

### TRUMP_USDT (Untouched Final Holdout Period: 2026-08-16 to 2026-08-31)
| Performance Metric | BASELINE SYSTEM (EXP_0045) | CANDIDATE SYSTEM (EXP_0044) | Difference / Delta |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `2,549` | `2,578` | +29 trades |
| **Win Rate** | `80.74%` | `74.20%` | -6.54% |
| **Average Win** | `+0.0004 USDT` | `+0.0004 USDT` | Identical |
| **Average Loss** | `-0.0017 USDT` | `-0.0010 USDT` | -41.2% lower loss magnitude |
| **Profit Factor** | `1.15` | `1.15` | Identical PF |
| **Net Realized PnL** | **`+0.1056 USDT`** | **`+0.1002 USDT`** | -$0.0054 USDT |
| **Max Drawdown (%)** | **`12.32%`** | **`9.23%`** | **-25.1% Drawdown Reduction** |

---

### DOGE_USDT Cross-Pair Generalization (2026-07-01 to 2026-08-31)
| Performance Metric | BASELINE SYSTEM (EXP_0049) | CANDIDATE SYSTEM (EXP_0048) | Difference / Delta |
| :--- | :--- | :--- | :--- |
| **Total Trades** | `8,839` | `11,661` | +2,822 trades |
| **Win Rate** | `92.39%` | `73.05%` | -19.34% |
| **Average Win** | `+0.0002 USDT` | `+0.0002 USDT` | Identical |
| **Average Loss** | `-0.0024 USDT (~35 ticks)` | `-0.0005 USDT (5 ticks)` | -79.2% lower loss magnitude |
| **Profit Factor** | **`0.97 (UNPROFITABLE)`** | **`1.08 (PROFITABLE)`** | **+0.11 (+11.3%)** |
| **Net Realized PnL** | **`-0.0470 USDT (LOSS)`** | **`+0.1326 USDT (PROFIT)`** | **+$0.1796 USDT (TURNED PROFITABLE)** |
| **Max Drawdown (%)** | `0.07%` | `0.02%` | -71.4% lower drawdown |

---

## 2. Counterfactual Analysis Summary of Rejected Filters

The table below illustrates why candidate filters were rejected after counterfactual auditing:

| Candidate Filter / Mechanism | Losses Avoided | Winners Sacrificed | Net Economic Impact | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Breakeven Stop on +1 Tick Excursion** | 188 losses (+0.1986 USDT) | 997 winners (-0.3988 USDT) | **-0.2002 USDT (-95% PnL)** | **REJECTED** |
| **Hard 60s Duration Timeout** | 625 losses (+0.5312 USDT) | 1,469 winners (-0.6832 USDT) | **-0.1520 USDT (-72% PnL)** | **REJECTED** |
| **Hard 90s Duration Timeout** | 586 losses (+0.4768 USDT) | 1,212 winners (-0.5834 USDT) | **-0.1066 USDT (-50% PnL)** | **REJECTED** |
| **HTF 200 EMA Trend Gate** | ~350 losses avoided | ~800 winners discarded | **-0.1520 USDT (-72% PnL)** | **REJECTED** |
| **Hourly Blacklist (2,3,4,5,17 UTC)** | 148 losses avoided | 510 winners discarded | **-0.0418 USDT (-20% PnL)** | **REJECTED** |

---

## 3. Why the Candidate System Dominates
1. **Asymmetric Risk Compression**: By replacing `-25% ROE` with a fixed `5 ticks` stop loss, the maximum adverse loss on any single trade is capped at 5 ticks ($0.0010$ USDT) instead of drifting to 10–40 ticks.
2. **Drawdown Protection**: Drawdown is reduced by 25% to 34% across all TRUMP evaluation periods.
3. **Cross-Asset Survival**: On assets with lower tick values (like DOGE), the baseline system failed because `-25% ROE` was 35 ticks wide. The candidate system remained profitable with a $1.08$ profit factor.
