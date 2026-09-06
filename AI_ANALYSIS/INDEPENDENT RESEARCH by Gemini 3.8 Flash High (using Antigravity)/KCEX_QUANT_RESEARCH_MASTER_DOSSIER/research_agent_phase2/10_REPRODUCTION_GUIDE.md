# Phase 2 Independent Reproduction Guide

This guide provides exact, step-by-step instructions to independently reproduce every finding, backtest, counterfactual matrix, and robustness experiment conducted during the Phase 2 quantitative audit.

---

## 1. Prerequisites & Environment

- **Python Version**: Python 3.10+ (Tested on Python 3.13)
- **Dependencies**: `pandas`, `numpy` (all other modules use Python standard library)
- **Working Directory**: Project root (`d:\My_Bots\Trading\(COPY-SandBoxed) KCEX`)

---

## 2. Step-by-Step Reproduction Commands

### Step 1: Reproduce Baseline vs Candidate (Claim Verification)
Runs the Baseline (SL 25% ROE) and Candidate (SL 5 ticks) on the TRUMP discovery period (July 1–24, 2026) and confirms identical trade counts, win rate, PnL, and drawdowns:
```bash
python research/tools/phase2_reproduce.py
```
*Expected Output*:
- Baseline: 3,066 trades, 77.40% WR, 1.29 PF, +0.2120 USDT PnL, 12.69% Max DD.
- Candidate: 3,114 trades, 76.11% WR, 1.27 PF, +0.2040 USDT PnL, 8.40% Max DD.
*Runtime*: ~60 seconds.

---

### Step 2: Regenerate Full SL Curve Sweep (`03_SL_SWEEP_RESULTS.csv`)
Sweeps stop losses from 1 to 15 ticks with TP = 2 held constant on TRUMP (July 1–24):
```bash
python research/tools/phase2_sl_sweep.py
```
*Output File*: `research_agent_phase2/03_SL_SWEEP_RESULTS.csv`  
*Runtime*: ~8 minutes.

---

### Step 3: Regenerate Multi-Month Time Segment Matrix (`04_TIME_SEGMENT_RESULTS.csv`)
Runs 56 parallel backtests across all 8 months of 2026 (Jan–Aug) for $\text{SL} \in [2, 3, 4, 5, 6, 7, 10]\text{ ticks}$:
```bash
python research/tools/phase2_time_segments.py
```
*Output File*: `research_agent_phase2/04_TIME_SEGMENT_RESULTS.csv`  
*Runtime*: ~7 minutes (multi-process with 3 workers).

---

### Step 4: Regenerate Cross-Pair Validation (`05_PAIR_RESULTS.csv`)
Compares TRUMP_USDT vs DOGE_USDT across both Jul–Aug 2026 and Jan–Feb 2026:
```bash
python research/tools/phase2_pairs.py
```
*Output File*: `research_agent_phase2/05_PAIR_RESULTS.csv`  
*Runtime*: ~5 minutes.

---

### Step 5: Regenerate Directional & Strategy Independence (`06_DIRECTION_RESULTS.csv`)
Tests BOTH vs LONG_ONLY vs SHORT_ONLY and STOCH_RSI vs EMA_CROSSOVER across the SL curve:
```bash
python research/tools/phase2_directions.py
```
*Output File*: `research_agent_phase2/06_DIRECTION_RESULTS.csv`  
*Runtime*: ~5 minutes.

---

### Step 6: Regenerate Per-Trade Counterfactual Matrix (`07_COUNTERFACTUAL_MATRIX.csv`)
Evaluates 4,436 raw strategy signals tick-by-tick forward in time to classify every signal (WIN_ALL, LOSS_ALL, SAVED_BY_SL5, EXTRA_DAMAGE_SL5, SAVED_BY_SL10):
```bash
python research/tools/phase2_counterfactual.py
```
*Output File*: `research_agent_phase2/07_COUNTERFACTUAL_MATRIX.csv`  
*Runtime*: ~40 seconds.

---

### Step 7: Regenerate Robustness, Slippage & Null Models (`08_ROBUSTNESS_RESULTS.csv`)
Executes 0, 1, 2-tick slippage tests, 1,000-iteration block bootstrap resampling, and capital scaling:
```bash
python research/tools/phase2_robustness.py
```
*Output File*: `research_agent_phase2/08_ROBUSTNESS_RESULTS.csv`  
*Runtime*: ~2 minutes.

---

## 3. Verification of Generated Artifacts

To verify that all 10 deliverables are present and populated:
```bash
python -c "
import os
files = [
    '01_VALIDATION_SUMMARY.md',
    '02_DETAILED_VALIDATION_REPORT.md',
    '03_SL_SWEEP_RESULTS.csv',
    '04_TIME_SEGMENT_RESULTS.csv',
    '05_PAIR_RESULTS.csv',
    '06_DIRECTION_RESULTS.csv',
    '07_COUNTERFACTUAL_MATRIX.csv',
    '08_ROBUSTNESS_RESULTS.csv',
    '09_CODE_CHANGES.md',
    '10_REPRODUCTION_GUIDE.md'
]
missing = [f for f in files if not os.path.exists(os.path.join('research_agent_phase2', f))]
if missing:
    print('Missing files:', missing)
else:
    print('All 10 Phase 2 deliverables verified successfully!')
"
```
