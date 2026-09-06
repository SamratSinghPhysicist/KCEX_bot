# Reproduction Guide: Step-by-Step Execution Manual

This guide enables anyone to reproduce every key baseline, diagnostic test, candidate configuration, and forensic analysis directly from the command line.

---

## 1. Prerequisites & Environment Setup

All commands are executed from the project root directory:
```powershell
cd "d:\My_Bots\Trading\(COPY-SandBoxed) KCEX"
```

Verify Python environment and unit tests:
```powershell
python -m unittest BACKTESTER/test_backtester.py
python -m unittest test_filters.py
```

---

## 2. Reproduce the Baseline System

### 2.1 Baseline STOCH_RSI (EXP_0001)
Run `STOCH_RSI` with $+2\text{ ticks}$ Take Profit and $-25.0\%\text{ ROE}$ Stop Loss on the Discovery Period (`2026-07-01` to `2026-07-24`):
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-mode ROE --sl-roe 25.0 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 3,066\text{ trades}$, Win Rate $\approx 77.4\%$, Net PnL $\approx +0.2120\text{ USDT}$, Max Drawdown $\approx 12.7\%$.

### 2.2 Baseline EMA_CROSSOVER (EXP_0002)
Run `EMA_CROSSOVER` ($5/13$) with $+2\text{ ticks}$ Take Profit and $-25.0\%\text{ ROE}$ Stop Loss:
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy EMA_CROSSOVER --ema-preset 5/13 --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-mode ROE --sl-roe 25.0 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 1,765\text{ trades}$, Win Rate $\approx 74.9\%$, Net PnL $\approx +0.0540\text{ USDT}$, Max Drawdown $\approx 45.3\%$.

---

## 3. Reproduce the Diagnostic Symmetrical Tests (+2 / -2 ticks)

### 3.1 Symmetrical STOCH_RSI (EXP_0003)
Isolate raw directional skill without asymmetric barrier distortion:
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-mode TICKS --sl-ticks 2 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 4,014\text{ trades}$, Win Rate $\approx 50.82\%$, Net PnL $\approx +0.0264\text{ USDT}$.

### 3.2 Symmetrical EMA_CROSSOVER (EXP_0004)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy EMA_CROSSOVER --ema-preset 5/13 --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-mode TICKS --sl-ticks 2 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 2,415\text{ trades}$, Win Rate $\approx 49.86\%$, Net PnL $\approx -0.0028\text{ USDT}$.

---

## 4. Reproduce the Best Candidate System (EXP_0007 / EXP_0040 / EXP_0044)

The Candidate System sets `SL = 5 ticks` (`sl_mode = 'TICKS'`, `sl_ticks = 5`):

### 4.1 Candidate on Discovery Period (`2026-07-01` to `2026-07-24`)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-mode TICKS --sl-ticks 5 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 3,114\text{ trades}$, Win Rate $\approx 76.11\%$, Net PnL $\approx +0.2040\text{ USDT}$, Max Drawdown $\approx 8.40\%$.

### 4.2 Candidate on Validation Period (`2026-07-25` to `2026-08-15`)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-25 --end 2026-08-15 --tp-ticks 2 --sl-mode TICKS --sl-ticks 5 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 2,150\text{ trades}$, Win Rate $\approx 76.47\%$, Net PnL $\approx +0.1516\text{ USDT}$, Max Drawdown $\approx 8.29\%$.

### 4.3 Candidate on Final Out-of-Sample Period (`2026-08-16` to `2026-08-31`)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol TRUMP_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-08-16 --end 2026-08-31 --tp-ticks 2 --sl-mode TICKS --sl-ticks 5 --fee-mode ZERO --capital 0.07 --contracts 2
```
*Expected Result*: $\approx 2,578\text{ trades}$, Win Rate $\approx 74.20\%$, Net PnL $\approx +0.1002\text{ USDT}$, Max Drawdown $\approx 9.23\%$.

---

## 5. Reproduce Cross-Pair Generalization on DOGE_USDT

### 5.1 Candidate System on DOGE_USDT (EXP_0048)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol DOGE_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-01 --end 2026-08-31 --tp-ticks 2 --sl-mode TICKS --sl-ticks 5 --fee-mode ZERO --capital 100.0 --volume-mode CONTRACTS --contracts 1 --no-ticks
```
*Expected Result*: $\approx 11,661\text{ trades}$, Win Rate $\approx 73.05\%$, Net PnL $\approx +0.1326\text{ USDT}$, Profit Factor $\approx 1.08$.

### 5.2 Baseline System on DOGE_USDT (EXP_0049)
```powershell
python BACKTESTER/run_backtest.py --target local --symbol DOGE_USDT --timeframe 1m --strategy STOCH_RSI --stoch-preset FAST_SCALP --start 2026-07-01 --end 2026-08-31 --tp-ticks 2 --sl-mode ROE --sl-roe 25.0 --fee-mode ZERO --capital 100.0 --volume-mode CONTRACTS --contracts 1 --no-ticks
```
*Expected Result*: $\approx 8,839\text{ trades}$, Win Rate $\approx 92.39\%$, Net PnL $\approx -0.0470\text{ USDT}$ (LOSS), Profit Factor $\approx 0.97$.

---

## 6. Reproduce Analytical & Forensic Tools

### 6.1 Granular Loss Forensics
Re-run tick path and excursion classification on baseline trade logs:
```powershell
python research/tools/forensics_analyzer.py
```

### 6.2 Counterfactual Audit (Debunking Breakeven and Duration Timeouts)
Re-run the exact tick-by-tick counterfactual replay:
```powershell
python research/tools/counterfactual_analysis.py
```

### 6.3 Feature Threshold Scanner
Re-scan pre-entry momentum and volatility thresholds across all trades:
```powershell
python research/tools/feature_threshold_scanner.py
```
