# MASTER QUANTITATIVE RESEARCH DOSSIER
## VOLUME II: THE ABSORBING BARRIER PARADOX & MICROSTRUCTURE FORENSICS
**Mathematical Foundations of Micro-Scalping in Zero-Fee Derivatives Markets**  
**Author**: Autonomous Quantitative Research Agent  
**Date**: September 2026  

---

## 1. Mathematical Formulation: Absorbing Barriers in Random Walks

In high-frequency quantitative trading, understanding the baseline behavior of price paths under discrete boundaries is the first requirement before any directional edge can be claimed.

### 1.1 The Gambler's Ruin / Absorbing Barrier Theorem
Let a price process $S_t$ follow a discrete, unbiased random walk on a lattice with step size equal to the instrument's price unit (tick size $\delta$):
$$S_{t+1} = S_t + \delta \cdot X_{t+1}, \quad P(X = +1) = P(X = -1) = 0.5$$

Consider two absorbing boundaries placed relative to entry price $S_0$:
- Upper boundary (Take Profit): $+A \cdot \delta$ (where $A > 0$)
- Lower boundary (Stop Loss): $-B \cdot \delta$ (where $B > 0$)

The probability $P(+A \text{ before } -B)$ that the price hits the upper absorbing barrier before hitting the lower absorbing barrier is given analytically by:
$$P(+A \text{ before } -B) = \frac{B}{A + B}$$

### 1.2 The High Win Rate Illusion
When trading with a $+2\text{ tick}$ profit target ($A = 2$) and asymmetric stop losses ($B \in [2, 10]$), the theoretical random walk absorption probabilities are:

| Barrier Configuration | Stop Loss ($B$) | Take Profit ($A$) | Payoff Ratio ($B : A$) | Theoretical Random Walk Win Rate ($P$) | Required Break-Even Win Rate |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Symmetric (1:1)** | 2 ticks | 2 ticks | 1 : 1 | **50.00%** | 50.00% |
| **Mild Asymmetry** | 3 ticks | 2 ticks | 1.5 : 1 | **60.00%** | 60.00% |
| **Moderate Asymmetry**| 4 ticks | 2 ticks | 2 : 1 | **66.67%** | 66.67% |
| **Candidate Geometry** | **5 ticks** | **2 ticks** | **2.5 : 1** | **71.43%** | **71.43%** |
| **Wide Stop** | 6 ticks | 2 ticks | 3 : 1 | **75.00%** | 75.00% |
| **Wide Stop** | 7 ticks | 2 ticks | 3.5 : 1 | **77.78%** | 77.78% |
| **Baseline Stop** | **10 ticks** | **2 ticks** | **5 : 1** | **83.33%** | **83.33%** |

### Mathematical Consequence:
A trading strategy boasting an **85% win rate** is not necessarily a high-alpha system. In an unbiased random walk with $A = 2$ and $B = 10$, a pure coin-toss system hits the target **83.33% of the time**. 
An empirical win rate of 85.0% contains only **+1.67% of true directional drift ($\Delta P$)**. 

Furthermore, under an asymmetric barrier where $B = 10$ and $A = 2$:
$$\text{Expected Value} = P \cdot (+2) - (1 - P) \cdot (-10)$$
**A single losing trade destroys 5 consecutive winning trades.** If the empirical win rate drops from 85% to 82% (a mere 3% drop), the entire system switches from profitable to heavily loss-making!

---

## 2. The 25% ROE Liquidation Proof

In KCEX futures trading at 75x leverage, the original system default was configured as `sl_roe_pct = 25.0`. Here we mathematically prove why 25% ROE is the exact exchange liquidation barrier, and how it evaluates directly to 5 ticks.

### Theorem 1: The 25% ROE Liquidation Barrier
Given:
- Leverage $L = 75$
- Initial Margin Fraction $IM = \frac{1}{L} = \frac{1}{75} \approx 1.3333\%$
- Exchange Maintenance Margin Ratio $MMR = 1.0\%$

Liquidation is triggered when position equity falls to the Maintenance Margin requirement:
$$\text{Position Equity} = IM - \text{Adverse Price Fraction} = MMR$$
$$\text{Adverse Price Fraction to Liquidation} = IM - MMR = \frac{1}{75} - 0.010 = 0.013333 - 0.010 = \mathbf{0.003333} = \frac{1}{300}$$

Now, compute the Return on Equity (ROE) loss at this liquidation point:
$$\text{ROE Loss} = \text{Adverse Price Fraction} \times \text{Leverage} = 0.003333 \times 75 = \mathbf{25.0\%}$$

$$\mathbf{\text{Q.E.D.}: \text{ At } 75\times \text{ leverage with } 1\% \text{ MMR, a } 25\% \text{ ROE loss IS the exact exchange liquidation event.}}$$

### Theorem 2: The TRUMP 5-Tick Equivalence
The stop loss price offset $\Delta P$ for a 25% ROE stop on contract price $P$ is:
$$\Delta P = P \times \frac{\text{ROE}}{100 \times L} = P \times \frac{0.25}{75} = \frac{P}{300}$$

For TRUMP_USDT, the minimum price unit is $\delta = 0.001\text{ USDT}$. Converting $\Delta P$ to ticks:
$$\text{Stop Distance (ticks)} = \frac{\Delta P}{\delta} = \frac{P / 300}{0.001} = \frac{P}{0.300} = \frac{10}{3} \cdot P \approx 3.333 \cdot P$$

Evaluating for TRUMP across different historical price regimes:
- At $P = \$1.50\text{ USDT}$ (TRUMP in July 2026): $\text{Stop Distance} = 3.333 \times 1.50 = \mathbf{5.0\text{ ticks}}$!
- At $P = \$1.60\text{ USDT}$ (TRUMP mean July 2026): $\text{Stop Distance} = 3.333 \times 1.60 = \mathbf{5.33\text{ ticks}}$!
- At $P = \$3.00\text{ USDT}$ (TRUMP in March 2026): $\text{Stop Distance} = 3.333 \times 3.00 = \mathbf{10.0\text{ ticks}}$!
- At $P = \$5.11\text{ USDT}$ (TRUMP in January 2026): $\text{Stop Distance} = 3.333 \times 5.11 = \mathbf{17.0\text{ ticks}}$!

### Implication:
When Phase 1 tested the "Candidate SL = 5 ticks" against the "Baseline SL = 25% ROE" on July 1–24 (mean price $1.628), the Baseline was **already executing an average stop of 5.4 ticks**. 
The entire Phase 1 investigation was unwittingly comparing a fixed 5.0-tick stop to a dynamic 5.4-tick stop, and any stop beyond 5.4 ticks was physically impossible without triggering exchange liquidation!

---

## 3. The Volatility Regime Theorem

Why did `SL = 5 ticks` appear to peak in July 2026, but fail across all other months?

We computed the 1-minute Average True Range (Bar High minus Low) in ticks ($\delta = 0.001$) across all 8 months of 2026 for TRUMP_USDT:

| Month | Mean Price | Median 1m Range | Mean 1m Range | 90th Percentile 1m Range | Preferred Stop |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2026-01 (Jan)** | $5.11 | 4.0 ticks | **4.93 ticks** | 9.0 ticks | **SL = 2 ticks** |
| **2026-02 (Feb)** | $3.53 | 4.0 ticks | **5.11 ticks** | 9.0 ticks | **SL = 2 ticks** |
| **2026-03 (Mar)** | $3.29 | 4.0 ticks | **5.68 ticks** | 11.0 ticks | **SL = 2 ticks** |
| **2026-04 (Apr)** | $2.81 | 3.0 ticks | **3.60 ticks** | 6.0 ticks | **SL = 2 ticks** |
| **2026-05 (May)** | $2.21 | 2.0 ticks | **2.85 ticks** | 5.0 ticks | **SL = 7 ticks** |
| **2026-06 (Jun)** | $1.81 | 3.0 ticks | **3.78 ticks** | 7.0 ticks | **SL = 2 ticks** |
| **2026-07 (Jul)** | $1.60 | **2.0 ticks** | **2.16 ticks** | **4.0 ticks** | **SL = 5 ticks** |
| **2026-08 (Aug)** | $1.80 | 2.0 ticks | **5.08 ticks** | 12.0 ticks | **SL = 10 ticks** |

### The Regime Mechanics Explained:
1. **The July Noise Shelter**:
   In July 2026, TRUMP was in an exceptionally quiet consolidation regime. 90% of all 1-minute candles had a range of $\le 4.0\text{ ticks}$. A 5-tick stop sat **outside** the 1-minute random noise boundary. Mean-reverting oscillator entries had the temporal leeway to endure small 2–3 tick adverse excursions and subsequently push $+2\text{ ticks}$ to hit TP.
2. **The Normal-Volatility Trap**:
   In January–March and August, the average 1-minute candle had a range of **5.0 to 5.7 ticks**. In this normal environment, normal random noise routinely spans 5 ticks within a single bar. 
   Under an asymmetric payoff ratio ($1:2.5$), every noise stop-out costs $-0.0010\text{ USDT}$, requiring 2.5 winning trades (+0.0004 USDT each) just to break even. As a result, SL = 5 was repeatedly stopped out by random noise, causing PnL to collapse from $+0.2682$ in July down to $+0.0456$ in January.
3. **Why Symmetric SL = 2 Dominates Under Normal Volatility**:
   Under SL = 2, the payoff ratio is $1:1$ (+2 ticks win, -2 ticks loss). One loss only costs one win. When market volatility is high and Stochastic RSI provides directional accuracy between 55% and 60%, a $1:1$ system extracts steady, high-frequency alpha (+0.3492 in Jan, +0.4520 in Feb, +0.4504 in Mar) without suffering from the devastating tail-risk of asymmetric barriers.

---

## 4. Millisecond Order Flow Microstructure Forensics

Using our tick analysis pipeline on the 265 MB millisecond trade data of July 2026, we extracted microstructure features across winning vs losing trades.

### 4.1 Maximum Adverse Excursion (MAE) Distribution
For winning trades in July 2026:
- **MAE = 0 ticks**: 24.8% of winning trades moved directly to $+2\text{ ticks}$ without a single adverse tick.
- **MAE = 1 tick**: 38.6% of winning trades experienced a 1-tick pullback before hitting TP.
- **MAE = 2 ticks**: 19.1% of winning trades experienced a 2-tick pullback before hitting TP.
- **MAE = 3–4 ticks**: 17.5% of winning trades dipped 3 to 4 ticks adverse before recovering to TP.
- **MAE $\ge 5$ ticks**: 0.0% (by definition, stopped out under SL = 5).

### 4.2 Time to Resolution
- **Median Time to Take Profit**: 58.2 seconds.
- **Median Time to Stop Loss**: 114.6 seconds.
- Winning trades resolve almost **twice as fast** as losing trades. When a signal is correct, the mean-reversion impulse pushes price into TP within the first 60 seconds. When a signal fails, price enters an adverse drift that slowly grinds into the stop loss.
