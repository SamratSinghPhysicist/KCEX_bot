# Phase 2 Independent Validation Summary: Stress-Testing the SL = 5 Ticks Hypothesis

## Executive Decision & Verdict

```text
FINAL VERDICT: FRAGILE
```

### Did SL = 5 Survive?
**NO.** The claim that `SL = 5 ticks` represents a universally optimal, robust micro-scalping edge that is deployable for live/paper trading does **not** survive independent rigorous stress-testing.

While `SL = 5 ticks` is mathematically reproducible on the specific July 2026 TRUMP_USDT sample, it is **not** a generalizable market property. Across broader multi-month time segments and cross-pair validation, **`SL = 2 ticks` (symmetric 1:1 risk-reward) systematically outperforms `SL = 5 ticks` by +31.0% on TRUMP and by +189% on DOGE**.

---

## Key Question Scorecard

| Question | Verdict | Key Empirical Evidence |
| :--- | :---: | :--- |
| **Reproducibility of Phase 1 Claim?** | **CONFIRMED** | Re-run on July 1–24 reproduced exact metrics: 3,114 trades, 76.11% WR, 1.27 PF, +0.2040 USDT PnL, 8.40% Max DD. |
| **Does it generalize across time?** | **NO** | In 6 out of 8 months of 2026 (Jan, Feb, Mar, Apr, May, Jun), **SL = 2 ticks** outperformed SL = 5. Total 8-month PnL: **SL=2 (+2.0288 USDT) vs SL=5 (+1.5482 USDT)**. |
| **Does it generalize across pairs?** | **NO** | On DOGE_USDT, **SL = 2 ticks** outperformed SL = 5 in every period tested (+1.7592 USDT vs +0.6087 USDT). At SL=10, DOGE became net unprofitable (-0.1046 USDT). |
| **Does it generalize across direction?** | **PARTIAL** | STOCH_RSI edge was heavily short-biased in July (+0.1290 USDT Short vs +0.0798 USDT Long) due to monthly downward drift ($1.87 to $1.50). |
| **Is it robust to execution friction?** | **CATASTROPHIC FAILURE** | **1 tick** of adverse entry slippage completely annihilates the edge: PnL collapses from **+0.2040 USDT to -0.4564 USDT** (PF drops to 0.60). |
| **Is 5 ticks an isolated optimum?** | **REGIME-BOUND** | 5 ticks was an artifact of July 2026's compressed volatility (mean 1m candle range was 2.16 ticks). When volatility expanded to 5.0+ ticks (Jan–Mar), SL=5 degraded sharply. |

---

## Where Did It Work?
1. **Compressed Low-Volatility Regimes (July 2026 on TRUMP)**:
   In July 2026, TRUMP price was consolidating between $1.50 and $1.87. The median 1m candle range was **2.0 ticks**, and the 90th percentile range was **4.0 ticks**. Under this regime, a 5-tick stop sat safely outside the 1-minute random noise boundary, allowing 1,155 signals to retrace between -2 and -5 ticks and recover to hit TP (+2 ticks).
2. **Zero-Slippage Idealized Simulation**:
   When fills occur at exact quoted close prices with zero transaction fees, the mathematical random-walk absorption probability $P = \frac{5}{2 + 5} = 71.43\%$ combines with Stochastic RSI's $+4.68\%$ directional drift to produce positive expectancy ($+0.2040\text{ USDT}$).

---

## Where Did It Fail?
1. **Normal & High Volatility Regimes (Jan, Feb, Mar, Aug 2026)**:
   In January through March 2026, TRUMP traded between $3.00 and $5.50 with a mean 1m bar range of **4.9 to 5.7 ticks**. In this normal environment, normal 1-minute candle noise routinely exceeded 5 ticks. Because each loss under SL=5 costs -5 ticks (destroying 2.5 wins), trades were constantly knocked out at the maximum stop.
   - In Jan 2026: **SL=2 made +0.3492 USDT (PF 1.35)** vs **SL=5 making only +0.0456 USDT (PF 1.03)**.
   - In Feb 2026: **SL=2 made +0.4520 USDT (PF 1.54)** vs **SL=5 making +0.2662 USDT (PF 1.21)**.
   - In Mar 2026: **SL=2 made +0.4504 USDT (PF 1.46)** vs **SL=5 making +0.1714 USDT (PF 1.11)**.
2. **Alternative Crypto Assets (DOGE_USDT)**:
   On DOGE_USDT across both Jan–Feb and Jul–Aug 2026, SL=2 was overwhelmingly superior:
   - DOGE Jul–Aug: **SL=2 (+0.5846 USDT, PF 1.64)** vs **SL=5 (+0.1326 USDT, PF 1.08)**.
   - DOGE Jan–Feb: **SL=2 (+1.1746 USDT, PF 3.04)** vs **SL=5 (+0.4761 USDT, PF 1.36)**.
3. **Execution Slippage**:
   With only +2 ticks (+0.002 USDT) profit target, entry slippage of a single price unit turns the required excursion from +2 to +3 ticks while shrinking stop buffer from 5 to 4 ticks. A 1-tick slippage penalty turns the strategy into an account-draining system (-0.4564 USDT).

---

## Structural Revelation: The Baseline Was Already 5 Ticks

A critical forensic discovery explains why Phase 1 observed identical performance between Baseline and Candidate on the Validation period (July 25 to August 15):
- The original system configured `sl_roe_pct = 25.0` at 75x leverage.
- Stop offset in price: $\Delta P = P \times \frac{ROE\%}{100 \times Leverage} = P \times \frac{0.25}{75} = \frac{P}{300}$.
- For TRUMP trading at **$1.50 USDT**, $\Delta P = \frac{1.50}{300} = 0.0050\text{ USDT} = \mathbf{5.0\text{ ticks}}$!
- Therefore, on TRUMP during July–August 2026, **the 25% ROE Baseline was ALREADY a 5-tick stop!**
- Phase 1 was unwittingly comparing a fixed 5-tick stop against a variable 4.6–5.4 tick stop, creating the illusion of a newly discovered breakthrough when it was actually the baseline's inherent geometry.
- Furthermore, at 75x leverage with a 1.0% Maintenance Margin Ratio (MMR), liquidation occurs at $\frac{1 - MMR}{Leverage} = \frac{1.33\% - 1.0\%}{75} = 0.333\% = \mathbf{25.0\%\text{ ROE}}$. Thus, **5 ticks is the exchange liquidation barrier for a $1.50 coin at 75x leverage**.

---

## Final Performance Comparison Table

### Discovery Period (TRUMP_USDT: 2026-07-01 to 2026-07-24)
| Configuration | Trade Count | Win Rate | Profit Factor | Net PnL (USDT) | Max Drawdown |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline (25% ROE ~5.3t)** | 3,066 | 77.40% | 1.29 | +0.2120 | 12.69% |
| **SL = 2 ticks** | 4,014 | 50.82% | 1.03 | +0.0264 | 18.18% |
| **SL = 3 ticks** | 3,669 | 63.26% | 1.15 | +0.1196 | 15.30% |
| **SL = 4 ticks** | 3,352 | 70.58% | 1.20 | +0.1576 | 8.08% |
| **SL = 5 ticks (Candidate)** | **3,114** | **76.11%** | **1.27** | **+0.2040** | **8.40%** |
| **SL = 6 ticks** | 2,931 | 78.98% | 1.25 | +0.1868 | 12.69% |
| **SL = 7 ticks** | 2,741 | 81.65% | 1.27 | +0.1910 | 12.38% |
| **SL = 10 ticks** | 2,288 | 86.45% | 1.28 | +0.1712 | 15.89% |

### Full 8-Month Period (TRUMP_USDT: 2026-01-01 to 2026-08-31)
| Configuration | Total Trades | Aggregate Win Rate | Net PnL (USDT) | Best Month | Worst Month | Total Return Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SL = 2 ticks** | **44,318** | **55.70%** | **+2.0288** | Feb (+0.4520) | Jul (+0.0248) | **1 (BEST)** |
| **SL = 3 ticks** | 41,507 | 63.85% | +1.7028 | Feb (+0.3468) | Jul (+0.1350) | 2 |
| **SL = 4 ticks** | 39,260 | 69.96% | +1.6002 | Feb (+0.3012) | Jan (+0.0828) | 3 |
| **SL = 5 ticks** | **37,322** | **74.52%** | **+1.5482** | Jul (+0.2682) | Jan (+0.0456) | **4** |
| **SL = 6 ticks** | 35,671 | 77.72% | +1.4868 | Jun (+0.2722) | Jan (+0.0412) | 6 |
| **SL = 7 ticks** | 34,064 | 80.40% | +1.4902 | May (+0.2624) | Jan (+0.0090) | 5 |
| **SL = 10 ticks** | 30,958 | 84.82% | +1.3398 | May (+0.2420) | Jan (-0.0076) | 7 (WORST) |

---

## Final Research Question Answered

> **Is SL = 5 genuinely exposing a robust property of the strategy/market, or did the first autonomous research program merely discover the most attractive historical parameter?**

**Answer**: The first research program discovered an attractive historical parameter that was uniquely tailored to the micro-volatility regime of July 2026. 

The underlying mechanism is:
1. When 1-minute market volatility is compressed (mean candle range $\le 2.5\text{ ticks}$), an entry noise barrier exists around 4 ticks. Placing SL at 5 ticks prevents stop-outs from random noise, giving mean-reverting signals time to reach TP.
2. When market volatility is normal (mean candle range $\ge 4.5\text{ ticks}$), 1-minute noise easily reaches 5 ticks. Under asymmetric payoff ($1:2.5$), the stop-loss destroys capital faster than the oscillator can generate wins. In this normal environment, **symmetric 1:1 risk-reward (SL=2) is vastly superior because 1 loss only costs 1 win**.

## Final Recommendation
**DO NOT deploy a fixed `SL = 5 ticks` stop loss to live trading.**
If a micro-scalping strategy is deployed:
1. Use **`SL = 2 ticks` (symmetric 1:1 risk-reward)** as the default robust stop, which demonstrated superior multi-month profitability across both TRUMP and DOGE without asymmetric barrier trap risk.
2. If wider stops are considered, they must be dynamically scaled to the prevailing 1m True Range (e.g. $\text{SL} = \max(2, \text{round}(1.8 \times \text{ATR}_{1\text{m}}))$) rather than hardcoded to 5 ticks.
3. Require exchange maker/limit execution orders; never execute market orders where 1 tick of taker slippage turns positive expectancy into a severe loss.
