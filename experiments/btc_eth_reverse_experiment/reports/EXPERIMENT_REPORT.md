# 🧪 Dual-Account Reverse Trading Experiment: Final Backtest Report

**Backtest Date Range:** `2025-01-01` to `2026-08-31`  
**Execution Model:** Pure OHLCV with 1m Dispute Resolution  
**Initial Capital:** $1,000.00 USDT per account ($2,000.00 combined)  
**Leverage:** 2.0x (100% current compounding capital per trade)  
**Synchronization Rule:** Strictly simultaneous entries; next trade is triggered only when and as soon as **both** accounts become free.  

## 1. Executive Summary & Core Findings

- **Top Combined Strategy Overall:** `Case 1` on `1d` with `TP3.0_SL3.0`
  - Combined Net PnL: **$+1,579.97** (+79.00% return)
  - Account A (BTC) Final: **$228.71** | Account B (ETH) Final: **$3,351.26**
  - Total Trade Cycles: `228`

- **Best Case 1 (Long BTC / Short ETH):** `1d` with `TP3.0_SL3.0` -> **$+1,579.97** (+79.00%)
- **Best Case 2 (Short BTC / Long ETH):** `1d` with `TP0.75_SL1.5` -> **$-455.38** (-22.77%)

---

## 2. Complete Performance Matrix (All 48 Configurations)

| Case | TF | TP/SL Config | Cycles | Acc A (BTC) PnL | Acc A Win% | Acc A Max Win/Loss Strk | Acc A To +10%/-3% | Acc B (ETH) PnL | Acc B Win% | Acc B Max Win/Loss Strk | Acc B To +10%/-3% | Combined PnL | Comb ROI% |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Case 1 | 1m | TP3.0_SL3.0 | 352 | $-561.09 | 50.3% | 7W / 7L | #2/#28 | $-827.81 | 48.0% | 6 / 8L | #6/#1 | $-1,388.90 | -69.5% |
| Case 1 | 1m | TP1.5_SL1.5 | 1383 | $-785.85 | 50.2% | 9W / 10L | #4/#11 | $-228.06 | 51.8% | 9 / 8L | #83/#1 | $-1,013.91 | -50.7% |
| Case 1 | 1m | TP1.5_SL3.0 | 674 | $-734.26 | 66.3% | 13W / 5L | #4/#7 | $-922.94 | 64.4% | 11 / 6L | #N/A/#1 | $-1,657.20 | -82.9% |
| Case 1 | 1m | TP0.75_SL1.5 | 2509 | $-971.20 | 65.8% | 14W / 6L | #10/#20 | $-771.21 | 67.6% | 18 / 7L | #236/#1 | $-1,742.41 | -87.1% |
| Case 1 | 5m | TP3.0_SL3.0 | 346 | $-723.06 | 49.1% | 9W / 9L | #2/#9 | $-542.32 | 50.3% | 9 / 6L | #6/#1 | $-1,265.38 | -63.3% |
| Case 1 | 5m | TP1.5_SL1.5 | 1342 | $-741.44 | 50.4% | 8W / 11L | #6/#17 | $-540.76 | 51.1% | 10 / 9L | #137/#1 | $-1,282.20 | -64.1% |
| Case 1 | 5m | TP1.5_SL3.0 | 663 | $-838.76 | 65.5% | 17W / 5L | #4/#7 | $-893.45 | 64.9% | 16 / 7L | #N/A/#1 | $-1,732.21 | -86.6% |
| Case 1 | 5m | TP0.75_SL1.5 | 2407 | $-959.43 | 66.0% | 13W / 6L | #7/#17 | $-845.77 | 67.2% | 20 / 7L | #184/#1 | $-1,805.20 | -90.3% |
| Case 1 | 15m | TP3.0_SL3.0 | 346 | $-499.98 | 50.6% | 10W / 8L | #2/#45 | $-594.18 | 50.0% | 6 / 8L | #31/#1 | $-1,094.16 | -54.7% |
| Case 1 | 15m | TP1.5_SL1.5 | 1277 | $-850.35 | 49.6% | 12W / 10L | #4/#13 | $+190.19 | 52.3% | 12 / 8L | #54/#1 | $-660.16 | -33.0% |
| Case 1 | 15m | TP1.5_SL3.0 | 647 | $-721.62 | 66.3% | 12W / 5L | #4/#8 | $-681.47 | 66.6% | 10 / 6L | #N/A/#1 | $-1,403.09 | -70.2% |
| Case 1 | 15m | TP0.75_SL1.5 | 2222 | $-945.65 | 66.0% | 21W / 6L | #7/#38 | $-804.21 | 67.3% | 16 / 6L | #107/#1 | $-1,749.86 | -87.5% |
| Case 1 | 1h | TP3.0_SL3.0 | 325 | $-523.01 | 50.1% | 11W / 7L | #2/#41 | $-169.54 | 51.7% | 10 / 6L | #6/#1 | $-692.55 | -34.6% |
| Case 1 | 1h | TP1.5_SL1.5 | 1154 | $-529.53 | 51.0% | 9W / 9L | #4/#11 | $-629.09 | 50.7% | 12 / 10L | #41/#1 | $-1,158.62 | -57.9% |
| Case 1 | 1h | TP1.5_SL3.0 | 608 | $-189.95 | 68.1% | 13W / 4L | #4/#11 | $-863.58 | 65.0% | 16 / 5L | #32/#1 | $-1,053.53 | -52.7% |
| Case 1 | 1h | TP0.75_SL1.5 | 1905 | $-908.62 | 66.1% | 16W / 6L | #7/#20 | $-872.03 | 66.6% | 19 / 6L | #N/A/#1 | $-1,780.65 | -89.0% |
| Case 1 | 4h | TP3.0_SL3.0 | 298 | $-361.57 | 51.0% | 10W / 8L | #2/#35 | $+357.22 | 53.0% | 8 / 6L | #6/#1 | $-4.35 | -0.2% |
| Case 1 | 4h | TP1.5_SL1.5 | 895 | $-729.57 | 49.6% | 9W / 9L | #4/#9 | $-397.90 | 51.2% | 8 / 7L | #33/#1 | $-1,127.47 | -56.4% |
| Case 1 | 4h | TP1.5_SL3.0 | 502 | $-734.91 | 65.5% | 13W / 8L | #N/A/#5 | $-698.66 | 65.9% | 14 / 6L | #32/#1 | $-1,433.57 | -71.7% |
| Case 1 | 4h | TP0.75_SL1.5 | 1350 | $-693.93 | 67.0% | 13W / 5L | #342/#12 | $+1,204.79 | 70.2% | 19 / 6L | #17/#1 | $+510.86 | +25.5% |
| Case 1 | 1d | TP3.0_SL3.0 | 228 | $-771.29 | 46.9% | 5W / 10L | #2/#5 | $+2,351.26 | 56.6% | 10 / 5L | #17/#1 | $+1,579.97 | +79.0% |
| Case 1 | 1d | TP1.5_SL1.5 | 448 | $-523.25 | 49.3% | 7W / 10L | #N/A/#17 | $-493.73 | 49.5% | 18 / 8L | #79/#1 | $-1,016.98 | -50.9% |
| Case 1 | 1d | TP1.5_SL3.0 | 331 | $-805.49 | 63.1% | 11W / 6L | #N/A/#5 | $-556.78 | 65.9% | 14 / 5L | #N/A/#1 | $-1,362.27 | -68.1% |
| Case 1 | 1d | TP0.75_SL1.5 | 528 | $-270.85 | 67.6% | 11W / 5L | #126/#6 | $-164.49 | 68.2% | 11 / 5L | #30/#1 | $-435.34 | -21.8% |
| Case 2 | 1m | TP3.0_SL3.0 | 352 | $-635.40 | 49.7% | 7W / 7L | #44/#1 | $-72.99 | 52.0% | 8 / 6L | #2/#5 | $-708.39 | -35.4% |
| Case 2 | 1m | TP1.5_SL1.5 | 1383 | $-869.87 | 49.6% | 10W / 9L | #N/A/#1 | $-968.01 | 47.9% | 8 / 9L | #4/#28 | $-1,837.88 | -91.9% |
| Case 2 | 1m | TP1.5_SL3.0 | 657 | $-664.57 | 66.7% | 14W / 4L | #80/#1 | $-328.79 | 67.9% | 15 / 5L | #N/A/#5 | $-993.36 | -49.7% |
| Case 2 | 1m | TP0.75_SL1.5 | 2570 | $-945.03 | 66.4% | 23W / 7L | #N/A/#3 | $-977.44 | 65.7% | 19 / 7L | #10/#19 | $-1,922.47 | -96.1% |
| Case 2 | 5m | TP3.0_SL3.0 | 346 | $-404.01 | 50.9% | 9W / 9L | #54/#1 | $-640.15 | 49.7% | 6 / 9L | #2/#5 | $-1,044.16 | -52.2% |
| Case 2 | 5m | TP1.5_SL1.5 | 1342 | $-873.17 | 49.5% | 11W / 8L | #150/#1 | $-928.65 | 48.8% | 9 / 10L | #6/#13 | $-1,801.82 | -90.1% |
| Case 2 | 5m | TP1.5_SL3.0 | 661 | $-584.25 | 67.0% | 19W / 8L | #86/#1 | $-790.84 | 66.0% | 11 / 5L | #N/A/#5 | $-1,375.09 | -68.8% |
| Case 2 | 5m | TP0.75_SL1.5 | 2408 | $-871.70 | 67.0% | 21W / 6L | #N/A/#3 | $-982.29 | 65.2% | 17 / 7L | #N/A/#16 | $-1,853.99 | -92.7% |
| Case 2 | 15m | TP3.0_SL3.0 | 346 | $-669.68 | 49.4% | 8W / 10L | #N/A/#1 | $-594.18 | 50.0% | 8 / 6L | #2/#5 | $-1,263.86 | -63.2% |
| Case 2 | 15m | TP1.5_SL1.5 | 1277 | $-726.20 | 50.4% | 10W / 12L | #94/#1 | $-965.60 | 47.7% | 8 / 12L | #4/#13 | $-1,691.80 | -84.6% |
| Case 2 | 15m | TP1.5_SL3.0 | 634 | $-670.33 | 66.6% | 13W / 8L | #77/#1 | $-861.34 | 65.1% | 11 / 5L | #N/A/#5 | $-1,531.67 | -76.6% |
| Case 2 | 15m | TP0.75_SL1.5 | 2285 | $-808.26 | 67.3% | 16W / 6L | #162/#3 | $-962.06 | 65.8% | 17 / 6L | #10/#23 | $-1,770.32 | -88.5% |
| Case 2 | 1h | TP3.0_SL3.0 | 325 | $-613.47 | 49.9% | 7W / 11L | #69/#1 | $-778.74 | 48.3% | 6 / 10L | #2/#5 | $-1,392.21 | -69.6% |
| Case 2 | 1h | TP1.5_SL1.5 | 1154 | $-881.51 | 49.0% | 9W / 9L | #133/#1 | $-849.71 | 49.3% | 10 / 12L | #4/#19 | $-1,731.22 | -86.6% |
| Case 2 | 1h | TP1.5_SL3.0 | 596 | $-427.33 | 67.5% | 17W / 6L | #45/#1 | $-799.17 | 65.6% | 10 / 8L | #N/A/#5 | $-1,226.50 | -61.3% |
| Case 2 | 1h | TP0.75_SL1.5 | 1942 | $-857.65 | 66.7% | 16W / 8L | #N/A/#3 | $-855.70 | 66.7% | 17 / 6L | #10/#75 | $-1,713.35 | -85.7% |
| Case 2 | 4h | TP3.0_SL3.0 | 298 | $-667.71 | 49.0% | 8W / 10L | #42/#1 | $-844.15 | 47.0% | 6 / 8L | #2/#5 | $-1,511.86 | -75.6% |
| Case 2 | 4h | TP1.5_SL1.5 | 895 | $-605.89 | 50.4% | 9W / 9L | #12/#1 | $-833.32 | 48.7% | 7 / 8L | #4/#9 | $-1,439.21 | -72.0% |
| Case 2 | 4h | TP1.5_SL3.0 | 516 | $-703.60 | 65.9% | 15W / 6L | #64/#1 | $-802.13 | 65.1% | 13 / 6L | #N/A/#5 | $-1,505.73 | -75.3% |
| Case 2 | 4h | TP0.75_SL1.5 | 1371 | $-475.18 | 67.9% | 17W / 5L | #175/#3 | $-879.56 | 65.5% | 17 / 6L | #7/#30 | $-1,354.74 | -67.7% |
| Case 2 | 1d | TP3.0_SL3.0 | 228 | $+336.46 | 53.1% | 10W / 5L | #23/#1 | $-909.09 | 43.4% | 5 / 10L | #2/#5 | $-572.63 | -28.6% |
| Case 2 | 1d | TP1.5_SL1.5 | 448 | $-316.38 | 50.7% | 10W / 7L | #29/#1 | $-356.24 | 50.5% | 8 / 18L | #10/#19 | $-672.62 | -33.6% |
| Case 2 | 1d | TP1.5_SL3.0 | 334 | $-447.46 | 66.5% | 13W / 5L | #32/#1 | $-787.95 | 63.5% | 9 / 4L | #N/A/#4 | $-1,235.41 | -61.8% |
| Case 2 | 1d | TP0.75_SL1.5 | 520 | $-480.87 | 66.2% | 13W / 6L | #52/#13 | $+25.49 | 69.0% | 13 / 4L | #10/#23 | $-455.38 | -22.8% |

---

## 3. Deep Dive: Case 1 (Always Buy BTC, Sell ETH)

In Case 1, **Account A is permanently LONG BTC** and **Account B is permanently SHORT ETH**.

### 📍 Timeframe: `1m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `352`
- **Combined Portfolio Balance:** `$611.10` (Net PnL: `$-1,388.90`, ROI: `-69.45%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $438.91 | $-561.09 | -56.11% | 50.3% | 177 / 175 | 0.93 | 82.1% | 7 | 7 | 2 | 28 |
| **Account B** | ETHUSDT | SHORT | $172.19 | $-827.81 | -82.78% | 48.0% | 169 / 183 | 0.89 | 86.1% | 6 | 8 | 6 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 37x, len 2: 20x, len 3: 19x, len 4: 5x, len 5: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 41x, len 2: 18x, len 3: 15x, len 4: 4x, len 5: 1x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 40x, len 2: 26x, len 3: 14x, len 4: 6x, len 5: 1x (+1 more)
- **Account B (ETH) Loss Streaks:** len 1: 45x, len 2: 18x, len 3: 12x, len 4: 8x, len 5: 4x (+2 more)

### 📍 Timeframe: `1m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1383`
- **Combined Portfolio Balance:** `$986.09` (Net PnL: `$-1,013.91`, ROI: `-50.70%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $214.15 | $-785.85 | -78.58% | 50.2% | 695 / 688 | 0.94 | 90.1% | 9 | 10 | 4 | 11 |
| **Account B** | ETHUSDT | SHORT | $771.94 | $-228.06 | -22.81% | 51.8% | 716 / 667 | 0.99 | 80.1% | 9 | 8 | 83 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 175x, len 2: 83x, len 3: 43x, len 4: 16x, len 5: 11x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 159x, len 2: 98x, len 3: 45x, len 4: 21x, len 5: 8x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 157x, len 2: 82x, len 3: 37x, len 4: 21x, len 5: 14x (+4 more)
- **Account B (ETH) Loss Streaks:** len 1: 166x, len 2: 83x, len 3: 36x, len 4: 22x, len 5: 10x (+3 more)

### 📍 Timeframe: `1m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `674`
- **Combined Portfolio Balance:** `$342.80` (Net PnL: `$-1,657.20`, ROI: `-82.86%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $265.74 | $-734.26 | -73.43% | 66.3% | 447 / 227 | 0.92 | 86.4% | 13 | 5 | 4 | 7 |
| **Account B** | ETHUSDT | SHORT | $77.06 | $-922.94 | -92.29% | 64.4% | 434 / 240 | 0.84 | 93.3% | 11 | 6 | Never | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 51x, len 2: 41x, len 3: 16x, len 4: 20x, len 5: 14x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 110x, len 2: 29x, len 3: 14x, len 4: 3x, len 5: 1x
- **Account B (ETH) Win Streaks:** len 1: 49x, len 2: 31x, len 3: 25x, len 4: 16x, len 5: 8x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 95x, len 2: 33x, len 3: 12x, len 4: 4x, len 5: 3x (+1 more)

### 📍 Timeframe: `1m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2509`
- **Combined Portfolio Balance:** `$257.59` (Net PnL: `$-1,742.41`, ROI: `-87.12%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $28.80 | $-971.20 | -97.12% | 65.8% | 1651 / 858 | 0.90 | 97.8% | 14 | 6 | 10 | 20 |
| **Account B** | ETHUSDT | SHORT | $228.79 | $-771.21 | -77.12% | 67.6% | 1697 / 812 | 0.96 | 90.8% | 18 | 7 | 236 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 188x, len 2: 135x, len 3: 90x, len 4: 48x, len 5: 40x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 372x, len 2: 132x, len 3: 38x, len 4: 19x, len 5: 4x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 171x, len 2: 113x, len 3: 67x, len 4: 58x, len 5: 41x (+10 more)
- **Account B (ETH) Loss Streaks:** len 1: 355x, len 2: 119x, len 3: 32x, len 4: 22x, len 5: 2x (+2 more)

### 📍 Timeframe: `5m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `346`
- **Combined Portfolio Balance:** `$734.62` (Net PnL: `$-1,265.38`, ROI: `-63.27%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $276.94 | $-723.06 | -72.31% | 49.1% | 170 / 176 | 0.90 | 86.9% | 9 | 9 | 2 | 9 |
| **Account B** | ETHUSDT | SHORT | $457.68 | $-542.32 | -54.23% | 50.3% | 174 / 172 | 0.95 | 76.5% | 9 | 6 | 6 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 34x, len 2: 21x, len 3: 19x, len 5: 3x, len 6: 1x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 36x, len 2: 18x, len 3: 12x, len 4: 7x, len 5: 2x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 47x, len 2: 17x, len 3: 12x, len 4: 5x, len 5: 3x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 46x, len 2: 18x, len 3: 14x, len 4: 4x, len 5: 4x (+1 more)

### 📍 Timeframe: `5m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1342`
- **Combined Portfolio Balance:** `$717.80` (Net PnL: `$-1,282.20`, ROI: `-64.11%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $258.56 | $-741.44 | -74.14% | 50.4% | 676 / 666 | 0.93 | 87.9% | 8 | 11 | 6 | 17 |
| **Account B** | ETHUSDT | SHORT | $459.24 | $-540.76 | -54.08% | 51.1% | 686 / 656 | 0.98 | 79.4% | 10 | 9 | 137 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 163x, len 2: 85x, len 3: 40x, len 4: 23x, len 5: 6x (+3 more)
- **Account A (BTC) Loss Streaks:** len 1: 162x, len 2: 94x, len 3: 39x, len 4: 13x, len 5: 10x (+5 more)
- **Account B (ETH) Win Streaks:** len 1: 180x, len 2: 81x, len 3: 45x, len 4: 18x, len 5: 14x (+4 more)
- **Account B (ETH) Loss Streaks:** len 1: 189x, len 2: 83x, len 3: 40x, len 4: 20x, len 5: 11x (+3 more)

### 📍 Timeframe: `5m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `663`
- **Combined Portfolio Balance:** `$267.79` (Net PnL: `$-1,732.21`, ROI: `-86.61%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $161.24 | $-838.76 | -83.88% | 65.5% | 434 / 229 | 0.87 | 91.9% | 17 | 5 | 4 | 7 |
| **Account B** | ETHUSDT | SHORT | $106.55 | $-893.45 | -89.35% | 64.9% | 430 / 233 | 0.86 | 89.8% | 16 | 7 | Never | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 50x, len 2: 37x, len 3: 18x, len 4: 15x, len 5: 13x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 99x, len 2: 27x, len 3: 18x, len 4: 3x, len 5: 2x
- **Account B (ETH) Win Streaks:** len 1: 47x, len 2: 26x, len 3: 31x, len 4: 13x, len 5: 13x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 96x, len 2: 24x, len 3: 15x, len 4: 8x, len 5: 1x (+1 more)

### 📍 Timeframe: `5m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2407`
- **Combined Portfolio Balance:** `$194.80` (Net PnL: `$-1,805.20`, ROI: `-90.26%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $40.57 | $-959.43 | -95.94% | 66.0% | 1588 / 819 | 0.89 | 97.1% | 13 | 6 | 7 | 17 |
| **Account B** | ETHUSDT | SHORT | $154.23 | $-845.77 | -84.58% | 67.2% | 1618 / 789 | 0.95 | 92.8% | 20 | 7 | 184 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 185x, len 2: 124x, len 3: 73x, len 4: 53x, len 5: 24x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 340x, len 2: 137x, len 3: 36x, len 4: 15x, len 5: 5x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 183x, len 2: 123x, len 3: 68x, len 4: 57x, len 5: 41x (+10 more)
- **Account B (ETH) Loss Streaks:** len 1: 371x, len 2: 108x, len 3: 38x, len 4: 14x, len 5: 5x (+1 more)

### 📍 Timeframe: `15m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `346`
- **Combined Portfolio Balance:** `$905.84` (Net PnL: `$-1,094.16`, ROI: `-54.71%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $500.02 | $-499.98 | -50.00% | 50.6% | 175 / 171 | 0.95 | 83.6% | 10 | 8 | 2 | 45 |
| **Account B** | ETHUSDT | SHORT | $405.82 | $-594.18 | -59.42% | 50.0% | 173 / 173 | 0.93 | 73.9% | 6 | 8 | 31 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 29x, len 2: 25x, len 3: 13x, len 4: 5x, len 5: 3x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 31x, len 2: 23x, len 3: 13x, len 4: 5x, len 5: 1x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 48x, len 2: 16x, len 3: 8x, len 4: 8x, len 5: 5x (+1 more)
- **Account B (ETH) Loss Streaks:** len 1: 45x, len 2: 21x, len 3: 12x, len 4: 6x, len 5: 1x (+3 more)

### 📍 Timeframe: `15m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1277`
- **Combined Portfolio Balance:** `$1,339.84` (Net PnL: `$-660.16`, ROI: `-33.01%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $149.65 | $-850.35 | -85.03% | 49.6% | 633 / 644 | 0.90 | 92.1% | 12 | 10 | 4 | 13 |
| **Account B** | ETHUSDT | SHORT | $1,190.19 | $+190.19 | +19.02% | 52.3% | 668 / 609 | 1.01 | 62.3% | 12 | 8 | 54 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 147x, len 2: 83x, len 3: 34x, len 4: 20x, len 5: 11x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 141x, len 2: 82x, len 3: 39x, len 4: 17x, len 5: 18x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 140x, len 2: 78x, len 3: 45x, len 4: 21x, len 5: 18x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 161x, len 2: 78x, len 3: 31x, len 4: 26x, len 5: 6x (+3 more)

### 📍 Timeframe: `15m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `647`
- **Combined Portfolio Balance:** `$596.91` (Net PnL: `$-1,403.09`, ROI: `-70.15%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $278.38 | $-721.62 | -72.16% | 66.3% | 429 / 218 | 0.90 | 84.7% | 12 | 5 | 4 | 8 |
| **Account B** | ETHUSDT | SHORT | $318.53 | $-681.47 | -68.15% | 66.6% | 431 / 216 | 0.91 | 74.7% | 10 | 6 | Never | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 58x, len 2: 30x, len 3: 15x, len 4: 14x, len 5: 11x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 102x, len 2: 32x, len 3: 10x, len 4: 3x, len 5: 2x
- **Account B (ETH) Win Streaks:** len 1: 48x, len 2: 24x, len 3: 25x, len 4: 14x, len 5: 14x (+5 more)
- **Account B (ETH) Loss Streaks:** len 1: 102x, len 2: 20x, len 3: 12x, len 4: 3x, len 5: 4x (+1 more)

### 📍 Timeframe: `15m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2222`
- **Combined Portfolio Balance:** `$250.14` (Net PnL: `$-1,749.86`, ROI: `-87.49%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $54.35 | $-945.65 | -94.57% | 66.0% | 1467 / 755 | 0.89 | 96.2% | 21 | 6 | 7 | 38 |
| **Account B** | ETHUSDT | SHORT | $195.79 | $-804.21 | -80.42% | 67.3% | 1496 / 726 | 0.95 | 90.7% | 16 | 6 | 107 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 167x, len 2: 120x, len 3: 62x, len 4: 53x, len 5: 24x (+9 more)
- **Account A (BTC) Loss Streaks:** len 1: 324x, len 2: 112x, len 3: 38x, len 4: 10x, len 5: 7x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 147x, len 2: 110x, len 3: 63x, len 4: 48x, len 5: 33x (+9 more)
- **Account B (ETH) Loss Streaks:** len 1: 320x, len 2: 97x, len 3: 31x, len 4: 17x, len 5: 9x (+1 more)

### 📍 Timeframe: `1h` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `325`
- **Combined Portfolio Balance:** `$1,307.45` (Net PnL: `$-692.55`, ROI: `-34.63%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $476.99 | $-523.01 | -52.30% | 50.1% | 163 / 162 | 0.94 | 81.1% | 11 | 7 | 2 | 41 |
| **Account B** | ETHUSDT | SHORT | $830.46 | $-169.54 | -16.95% | 51.7% | 168 / 157 | 0.98 | 72.2% | 10 | 6 | 6 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 29x, len 2: 23x, len 3: 13x, len 4: 4x, len 5: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 32x, len 2: 20x, len 3: 14x, len 4: 1x, len 5: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 45x, len 2: 13x, len 3: 13x, len 4: 5x, len 5: 4x (+2 more)
- **Account B (ETH) Loss Streaks:** len 1: 39x, len 2: 23x, len 3: 12x, len 4: 5x, len 5: 2x (+1 more)

### 📍 Timeframe: `1h` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1154`
- **Combined Portfolio Balance:** `$841.38` (Net PnL: `$-1,158.62`, ROI: `-57.93%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $470.47 | $-529.53 | -52.95% | 51.0% | 588 / 566 | 0.96 | 80.5% | 9 | 9 | 4 | 11 |
| **Account B** | ETHUSDT | SHORT | $370.91 | $-629.09 | -62.91% | 50.7% | 585 / 569 | 0.95 | 75.1% | 12 | 10 | 41 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 130x, len 2: 71x, len 3: 27x, len 4: 21x, len 5: 13x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 126x, len 2: 79x, len 3: 31x, len 4: 19x, len 5: 8x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 129x, len 2: 67x, len 3: 32x, len 4: 21x, len 5: 6x (+5 more)
- **Account B (ETH) Loss Streaks:** len 1: 115x, len 2: 77x, len 3: 39x, len 4: 26x, len 5: 8x (+4 more)

### 📍 Timeframe: `1h` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `608`
- **Combined Portfolio Balance:** `$946.47` (Net PnL: `$-1,053.53`, ROI: `-52.68%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $810.05 | $-189.95 | -19.00% | 68.1% | 414 / 194 | 0.99 | 73.7% | 13 | 4 | 4 | 11 |
| **Account B** | ETHUSDT | SHORT | $136.42 | $-863.58 | -86.36% | 65.0% | 395 / 213 | 0.87 | 91.6% | 16 | 5 | 32 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 45x, len 2: 21x, len 3: 17x, len 4: 15x, len 5: 9x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 85x, len 2: 28x, len 3: 15x, len 4: 2x
- **Account B (ETH) Win Streaks:** len 1: 50x, len 2: 24x, len 3: 20x, len 4: 11x, len 5: 11x (+5 more)
- **Account B (ETH) Loss Streaks:** len 1: 82x, len 2: 31x, len 3: 15x, len 4: 1x, len 5: 4x

### 📍 Timeframe: `1h` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `1905`
- **Combined Portfolio Balance:** `$219.35` (Net PnL: `$-1,780.65`, ROI: `-89.03%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $91.38 | $-908.62 | -90.86% | 66.1% | 1260 / 645 | 0.90 | 94.0% | 16 | 6 | 7 | 20 |
| **Account B** | ETHUSDT | SHORT | $127.97 | $-872.03 | -87.20% | 66.6% | 1268 / 637 | 0.89 | 89.5% | 19 | 6 | Never | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 164x, len 2: 94x, len 3: 50x, len 4: 33x, len 5: 22x (+10 more)
- **Account A (BTC) Loss Streaks:** len 1: 281x, len 2: 98x, len 3: 34x, len 4: 11x, len 5: 2x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 139x, len 2: 108x, len 3: 58x, len 4: 31x, len 5: 22x (+9 more)
- **Account B (ETH) Loss Streaks:** len 1: 273x, len 2: 95x, len 3: 32x, len 4: 14x, len 5: 2x (+1 more)

### 📍 Timeframe: `4h` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `298`
- **Combined Portfolio Balance:** `$1,995.65` (Net PnL: `$-4.35`, ROI: `-0.22%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $638.43 | $-361.57 | -36.16% | 51.0% | 152 / 146 | 0.96 | 72.0% | 10 | 8 | 2 | 35 |
| **Account B** | ETHUSDT | SHORT | $1,357.22 | $+357.22 | +35.72% | 53.0% | 158 / 140 | 1.03 | 56.9% | 8 | 6 | 6 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 37x, len 2: 19x, len 3: 7x, len 4: 6x, len 5: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 38x, len 2: 15x, len 3: 11x, len 4: 4x, len 5: 3x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 33x, len 2: 18x, len 3: 11x, len 4: 6x, len 5: 2x (+2 more)
- **Account B (ETH) Loss Streaks:** len 1: 38x, len 2: 19x, len 3: 10x, len 4: 3x, len 5: 2x (+1 more)

### 📍 Timeframe: `4h` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `895`
- **Combined Portfolio Balance:** `$872.53` (Net PnL: `$-1,127.47`, ROI: `-56.37%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $270.43 | $-729.57 | -72.96% | 49.6% | 444 / 451 | 0.91 | 82.1% | 9 | 9 | 4 | 9 |
| **Account B** | ETHUSDT | SHORT | $602.10 | $-397.90 | -39.79% | 51.2% | 458 / 437 | 0.97 | 71.8% | 8 | 7 | 33 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 113x, len 2: 48x, len 3: 30x, len 4: 14x, len 5: 9x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 109x, len 2: 54x, len 3: 23x, len 4: 18x, len 5: 9x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 102x, len 2: 47x, len 3: 29x, len 4: 17x, len 5: 13x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 106x, len 2: 55x, len 3: 18x, len 4: 15x, len 5: 14x (+2 more)

### 📍 Timeframe: `4h` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `502`
- **Combined Portfolio Balance:** `$566.43` (Net PnL: `$-1,433.57`, ROI: `-71.68%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $265.09 | $-734.91 | -73.49% | 65.5% | 329 / 173 | 0.86 | 82.5% | 13 | 8 | Never | 5 |
| **Account B** | ETHUSDT | SHORT | $301.34 | $-698.66 | -69.87% | 65.9% | 331 / 171 | 0.91 | 77.2% | 14 | 6 | 32 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 40x, len 2: 25x, len 3: 12x, len 4: 17x, len 5: 6x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 73x, len 2: 28x, len 3: 8x, len 4: 3x, len 8: 1x
- **Account B (ETH) Win Streaks:** len 1: 32x, len 2: 22x, len 3: 18x, len 4: 11x, len 5: 4x (+8 more)
- **Account B (ETH) Loss Streaks:** len 1: 62x, len 2: 23x, len 3: 16x, len 4: 1x, len 5: 1x (+1 more)

### 📍 Timeframe: `4h` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `1350`
- **Combined Portfolio Balance:** `$2,510.86` (Net PnL: `$+510.86`, ROI: `+25.54%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $306.07 | $-693.93 | -69.39% | 67.0% | 904 / 446 | 0.92 | 79.6% | 13 | 5 | 342 | 12 |
| **Account B** | ETHUSDT | SHORT | $2,204.79 | $+1,204.79 | +120.48% | 70.2% | 948 / 402 | 1.05 | 57.0% | 19 | 6 | 17 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 96x, len 2: 64x, len 3: 43x, len 4: 27x, len 5: 12x (+7 more)
- **Account A (BTC) Loss Streaks:** len 1: 183x, len 2: 70x, len 3: 25x, len 4: 7x, len 5: 4x
- **Account B (ETH) Win Streaks:** len 1: 71x, len 2: 58x, len 3: 45x, len 4: 24x, len 5: 26x (+11 more)
- **Account B (ETH) Loss Streaks:** len 1: 176x, len 2: 74x, len 3: 12x, len 4: 5x, len 5: 2x (+1 more)

### 📍 Timeframe: `1d` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `228`
- **Combined Portfolio Balance:** `$3,579.97` (Net PnL: `$+1,579.97`, ROI: `+79.00%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $228.71 | $-771.29 | -77.13% | 46.9% | 107 / 121 | 0.79 | 84.2% | 5 | 10 | 2 | 5 |
| **Account B** | ETHUSDT | SHORT | $3,351.26 | $+2,351.26 | +235.13% | 56.6% | 129 / 99 | 1.21 | 41.9% | 10 | 5 | 17 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 33x, len 2: 13x, len 3: 7x, len 4: 3x, len 5: 3x
- **Account A (BTC) Loss Streaks:** len 1: 31x, len 2: 12x, len 3: 8x, len 4: 3x, len 6: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 21x, len 2: 16x, len 3: 7x, len 4: 6x, len 6: 1x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 28x, len 2: 18x, len 3: 3x, len 4: 4x, len 5: 2x

### 📍 Timeframe: `1d` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `448`
- **Combined Portfolio Balance:** `$983.02` (Net PnL: `$-1,016.98`, ROI: `-50.85%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $476.75 | $-523.25 | -52.32% | 49.3% | 221 / 227 | 0.89 | 65.1% | 7 | 10 | Never | 17 |
| **Account B** | ETHUSDT | SHORT | $506.27 | $-493.73 | -49.37% | 49.5% | 222 / 226 | 0.90 | 64.1% | 18 | 8 | 79 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 55x, len 2: 24x, len 3: 13x, len 4: 5x, len 5: 4x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 46x, len 2: 28x, len 3: 15x, len 4: 12x, len 5: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 55x, len 2: 19x, len 3: 18x, len 4: 9x, len 5: 3x (+2 more)
- **Account B (ETH) Loss Streaks:** len 1: 44x, len 2: 35x, len 3: 14x, len 4: 8x, len 5: 2x (+3 more)

### 📍 Timeframe: `1d` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `331`
- **Combined Portfolio Balance:** `$637.73` (Net PnL: `$-1,362.27`, ROI: `-68.11%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $194.51 | $-805.49 | -80.55% | 63.1% | 209 / 122 | 0.78 | 85.3% | 11 | 6 | Never | 5 |
| **Account B** | ETHUSDT | SHORT | $443.22 | $-556.78 | -55.68% | 65.9% | 218 / 113 | 0.88 | 58.3% | 14 | 5 | Never | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 27x, len 2: 20x, len 3: 12x, len 4: 7x, len 5: 3x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 46x, len 2: 20x, len 3: 6x, len 4: 3x, len 6: 1x
- **Account B (ETH) Win Streaks:** len 1: 18x, len 2: 12x, len 3: 16x, len 4: 4x, len 5: 4x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 36x, len 2: 17x, len 3: 11x, len 5: 2x

### 📍 Timeframe: `1d` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `528`
- **Combined Portfolio Balance:** `$1,564.66` (Net PnL: `$-435.34`, ROI: `-21.77%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | LONG | $729.15 | $-270.85 | -27.08% | 67.6% | 357 / 171 | 0.94 | 45.8% | 11 | 5 | 126 | 6 |
| **Account B** | ETHUSDT | SHORT | $835.51 | $-164.49 | -16.45% | 68.2% | 360 / 168 | 0.96 | 46.7% | 11 | 5 | 30 | 1 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 27x, len 2: 22x, len 3: 20x, len 4: 11x, len 5: 8x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 63x, len 2: 30x, len 3: 6x, len 4: 5x, len 5: 2x
- **Account B (ETH) Win Streaks:** len 1: 35x, len 2: 26x, len 3: 13x, len 4: 12x, len 5: 6x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 80x, len 2: 22x, len 3: 5x, len 4: 1x, len 5: 5x

---

## 4. Deep Dive: Case 2 (Always Sell BTC, Buy ETH)

In Case 2, **Account A is permanently SHORT BTC** and **Account B is permanently LONG ETH**.

### 📍 Timeframe: `1m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `352`
- **Combined Portfolio Balance:** `$1,291.61` (Net PnL: `$-708.39`, ROI: `-35.42%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $364.60 | $-635.40 | -63.54% | 49.7% | 175 / 177 | 0.91 | 74.0% | 7 | 7 | 44 | 1 |
| **Account B** | ETHUSDT | LONG | $927.01 | $-72.99 | -7.30% | 52.0% | 183 / 169 | 0.99 | 70.5% | 8 | 6 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 41x, len 2: 18x, len 3: 15x, len 4: 4x, len 5: 1x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 37x, len 2: 20x, len 3: 19x, len 4: 5x, len 5: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 45x, len 2: 18x, len 3: 12x, len 4: 8x, len 5: 4x (+2 more)
- **Account B (ETH) Loss Streaks:** len 1: 40x, len 2: 26x, len 3: 14x, len 4: 6x, len 5: 1x (+1 more)

### 📍 Timeframe: `1m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1383`
- **Combined Portfolio Balance:** `$162.12` (Net PnL: `$-1,837.88`, ROI: `-91.89%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $130.13 | $-869.87 | -86.99% | 49.6% | 686 / 697 | 0.89 | 88.0% | 10 | 9 | Never | 1 |
| **Account B** | ETHUSDT | LONG | $31.99 | $-968.01 | -96.80% | 47.9% | 663 / 720 | 0.77 | 98.5% | 8 | 9 | 4 | 28 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 160x, len 2: 97x, len 3: 45x, len 4: 21x, len 5: 8x (+3 more)
- **Account A (BTC) Loss Streaks:** len 1: 174x, len 2: 84x, len 3: 43x, len 4: 15x, len 5: 12x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 167x, len 2: 85x, len 3: 33x, len 4: 22x, len 5: 10x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 155x, len 2: 83x, len 3: 37x, len 4: 22x, len 5: 14x (+4 more)

### 📍 Timeframe: `1m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `657`
- **Combined Portfolio Balance:** `$1,006.64` (Net PnL: `$-993.36`, ROI: `-49.67%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $335.43 | $-664.57 | -66.46% | 66.7% | 438 / 219 | 0.92 | 75.9% | 14 | 4 | 80 | 1 |
| **Account B** | ETHUSDT | LONG | $671.21 | $-328.79 | -32.88% | 67.9% | 446 / 211 | 0.95 | 77.0% | 15 | 5 | Never | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 51x, len 2: 37x, len 3: 15x, len 4: 14x, len 5: 12x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 102x, len 2: 27x, len 3: 17x, len 4: 3x
- **Account B (ETH) Win Streaks:** len 1: 41x, len 2: 21x, len 3: 22x, len 4: 16x, len 5: 11x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 80x, len 2: 36x, len 3: 11x, len 4: 4x, len 5: 2x

### 📍 Timeframe: `1m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2570`
- **Combined Portfolio Balance:** `$77.53` (Net PnL: `$-1,922.47`, ROI: `-96.12%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $54.97 | $-945.03 | -94.50% | 66.4% | 1707 / 863 | 0.89 | 95.1% | 23 | 7 | Never | 3 |
| **Account B** | ETHUSDT | LONG | $22.56 | $-977.44 | -97.74% | 65.7% | 1688 / 882 | 0.85 | 98.7% | 19 | 7 | 10 | 19 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 211x, len 2: 117x, len 3: 98x, len 4: 54x, len 5: 43x (+10 more)
- **Account A (BTC) Loss Streaks:** len 1: 401x, len 2: 133x, len 3: 30x, len 4: 18x, len 5: 3x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 227x, len 2: 131x, len 3: 69x, len 4: 52x, len 5: 36x (+11 more)
- **Account B (ETH) Loss Streaks:** len 1: 391x, len 2: 132x, len 3: 43x, len 4: 16x, len 5: 3x (+2 more)

### 📍 Timeframe: `5m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `346`
- **Combined Portfolio Balance:** `$955.84` (Net PnL: `$-1,044.16`, ROI: `-52.21%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $595.99 | $-404.01 | -40.40% | 50.9% | 176 / 170 | 0.95 | 70.9% | 9 | 9 | 54 | 1 |
| **Account B** | ETHUSDT | LONG | $359.85 | $-640.15 | -64.02% | 49.7% | 172 / 174 | 0.87 | 86.8% | 6 | 9 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 36x, len 2: 18x, len 3: 12x, len 4: 7x, len 5: 2x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 34x, len 2: 21x, len 3: 19x, len 5: 3x, len 6: 1x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 46x, len 2: 18x, len 3: 14x, len 4: 4x, len 5: 4x (+1 more)
- **Account B (ETH) Loss Streaks:** len 1: 47x, len 2: 17x, len 3: 12x, len 4: 5x, len 5: 3x (+3 more)

### 📍 Timeframe: `5m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1342`
- **Combined Portfolio Balance:** `$198.18` (Net PnL: `$-1,801.82`, ROI: `-90.09%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $126.83 | $-873.17 | -87.32% | 49.5% | 665 / 677 | 0.92 | 90.3% | 11 | 8 | 150 | 1 |
| **Account B** | ETHUSDT | LONG | $71.35 | $-928.65 | -92.87% | 48.8% | 655 / 687 | 0.84 | 97.0% | 9 | 10 | 6 | 13 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 163x, len 2: 94x, len 3: 39x, len 4: 13x, len 5: 10x (+5 more)
- **Account A (BTC) Loss Streaks:** len 1: 164x, len 2: 85x, len 3: 40x, len 4: 23x, len 5: 6x (+3 more)
- **Account B (ETH) Win Streaks:** len 1: 190x, len 2: 82x, len 3: 40x, len 4: 20x, len 5: 11x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 179x, len 2: 82x, len 3: 45x, len 4: 18x, len 5: 14x (+4 more)

### 📍 Timeframe: `5m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `661`
- **Combined Portfolio Balance:** `$624.91` (Net PnL: `$-1,375.09`, ROI: `-68.75%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $415.75 | $-584.25 | -58.43% | 67.0% | 443 / 218 | 0.94 | 76.4% | 19 | 8 | 86 | 1 |
| **Account B** | ETHUSDT | LONG | $209.16 | $-790.84 | -79.08% | 66.0% | 436 / 225 | 0.85 | 87.8% | 11 | 5 | Never | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 50x, len 2: 24x, len 3: 18x, len 4: 19x, len 5: 12x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 94x, len 2: 25x, len 3: 18x, len 4: 3x, len 8: 1x
- **Account B (ETH) Win Streaks:** len 1: 54x, len 2: 28x, len 3: 23x, len 4: 17x, len 5: 7x (+5 more)
- **Account B (ETH) Loss Streaks:** len 1: 103x, len 2: 28x, len 3: 10x, len 4: 4x, len 5: 4x

### 📍 Timeframe: `5m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2408`
- **Combined Portfolio Balance:** `$146.01` (Net PnL: `$-1,853.99`, ROI: `-92.70%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $128.30 | $-871.70 | -87.17% | 67.0% | 1614 / 794 | 0.92 | 88.5% | 21 | 6 | Never | 3 |
| **Account B** | ETHUSDT | LONG | $17.71 | $-982.29 | -98.23% | 65.2% | 1571 / 837 | 0.78 | 98.8% | 17 | 7 | Never | 16 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 170x, len 2: 102x, len 3: 91x, len 4: 48x, len 5: 38x (+10 more)
- **Account A (BTC) Loss Streaks:** len 1: 340x, len 2: 113x, len 3: 47x, len 4: 19x, len 5: 1x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 188x, len 2: 127x, len 3: 89x, len 4: 50x, len 5: 42x (+10 more)
- **Account B (ETH) Loss Streaks:** len 1: 361x, len 2: 121x, len 3: 54x, len 4: 6x, len 5: 7x (+2 more)

### 📍 Timeframe: `15m` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `346`
- **Combined Portfolio Balance:** `$736.14` (Net PnL: `$-1,263.86`, ROI: `-63.19%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $330.32 | $-669.68 | -66.97% | 49.4% | 171 / 175 | 0.89 | 76.0% | 8 | 10 | Never | 1 |
| **Account B** | ETHUSDT | LONG | $405.82 | $-594.18 | -59.42% | 50.0% | 173 / 173 | 0.91 | 82.5% | 8 | 6 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 31x, len 2: 23x, len 3: 13x, len 4: 5x, len 5: 1x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 29x, len 2: 25x, len 3: 13x, len 4: 5x, len 5: 3x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 45x, len 2: 21x, len 3: 12x, len 4: 6x, len 5: 1x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 48x, len 2: 16x, len 3: 8x, len 4: 8x, len 5: 5x (+1 more)

### 📍 Timeframe: `15m` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1277`
- **Combined Portfolio Balance:** `$308.20` (Net PnL: `$-1,691.80`, ROI: `-84.59%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $273.80 | $-726.20 | -72.62% | 50.4% | 644 / 633 | 0.95 | 82.1% | 10 | 12 | 94 | 1 |
| **Account B** | ETHUSDT | LONG | $34.40 | $-965.60 | -96.56% | 47.7% | 609 / 668 | 0.77 | 98.3% | 8 | 12 | 4 | 13 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 141x, len 2: 82x, len 3: 39x, len 4: 17x, len 5: 18x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 147x, len 2: 83x, len 3: 34x, len 4: 20x, len 5: 11x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 161x, len 2: 78x, len 3: 31x, len 4: 26x, len 5: 6x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 140x, len 2: 78x, len 3: 45x, len 4: 21x, len 5: 18x (+3 more)

### 📍 Timeframe: `15m` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `634`
- **Combined Portfolio Balance:** `$468.33` (Net PnL: `$-1,531.67`, ROI: `-76.58%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $329.67 | $-670.33 | -67.03% | 66.6% | 422 / 212 | 0.93 | 77.6% | 13 | 8 | 77 | 1 |
| **Account B** | ETHUSDT | LONG | $138.66 | $-861.34 | -86.13% | 65.1% | 413 / 221 | 0.84 | 92.6% | 11 | 5 | Never | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 48x, len 2: 32x, len 3: 15x, len 4: 16x, len 5: 10x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 102x, len 2: 20x, len 3: 13x, len 4: 3x, len 5: 1x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 57x, len 2: 29x, len 3: 21x, len 4: 14x, len 5: 6x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 92x, len 2: 38x, len 3: 12x, len 4: 3x, len 5: 1x

### 📍 Timeframe: `15m` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `2285`
- **Combined Portfolio Balance:** `$229.68` (Net PnL: `$-1,770.32`, ROI: `-88.52%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $191.74 | $-808.26 | -80.83% | 67.3% | 1539 / 746 | 0.94 | 88.8% | 16 | 6 | 162 | 3 |
| **Account B** | ETHUSDT | LONG | $37.94 | $-962.06 | -96.21% | 65.8% | 1503 / 782 | 0.84 | 97.7% | 17 | 6 | 10 | 23 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 151x, len 2: 113x, len 3: 69x, len 4: 46x, len 5: 35x (+11 more)
- **Account A (BTC) Loss Streaks:** len 1: 318x, len 2: 109x, len 3: 37x, len 4: 14x, len 5: 5x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 155x, len 2: 133x, len 3: 83x, len 4: 57x, len 5: 22x (+9 more)
- **Account B (ETH) Loss Streaks:** len 1: 337x, len 2: 108x, len 3: 45x, len 4: 12x, len 5: 8x (+1 more)

### 📍 Timeframe: `1h` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `325`
- **Combined Portfolio Balance:** `$607.79` (Net PnL: `$-1,392.21`, ROI: `-69.61%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $386.53 | $-613.47 | -61.35% | 49.9% | 162 / 163 | 0.91 | 75.7% | 7 | 11 | 69 | 1 |
| **Account B** | ETHUSDT | LONG | $221.26 | $-778.74 | -77.87% | 48.3% | 157 / 168 | 0.86 | 86.9% | 6 | 10 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 32x, len 2: 20x, len 3: 14x, len 4: 1x, len 5: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 29x, len 2: 23x, len 3: 13x, len 4: 4x, len 5: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 39x, len 2: 23x, len 3: 12x, len 4: 5x, len 5: 2x (+1 more)
- **Account B (ETH) Loss Streaks:** len 1: 45x, len 2: 13x, len 3: 13x, len 4: 5x, len 5: 4x (+2 more)

### 📍 Timeframe: `1h` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `1154`
- **Combined Portfolio Balance:** `$268.78` (Net PnL: `$-1,731.22`, ROI: `-86.56%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $118.49 | $-881.51 | -88.15% | 49.0% | 566 / 588 | 0.89 | 90.6% | 9 | 9 | 133 | 1 |
| **Account B** | ETHUSDT | LONG | $150.29 | $-849.71 | -84.97% | 49.3% | 569 / 585 | 0.88 | 92.1% | 10 | 12 | 4 | 19 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 126x, len 2: 79x, len 3: 31x, len 4: 19x, len 5: 8x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 130x, len 2: 71x, len 3: 27x, len 4: 21x, len 5: 13x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 115x, len 2: 77x, len 3: 39x, len 4: 26x, len 5: 8x (+4 more)
- **Account B (ETH) Loss Streaks:** len 1: 129x, len 2: 67x, len 3: 32x, len 4: 21x, len 5: 6x (+5 more)

### 📍 Timeframe: `1h` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `596`
- **Combined Portfolio Balance:** `$773.50` (Net PnL: `$-1,226.50`, ROI: `-61.32%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $572.67 | $-427.33 | -42.73% | 67.5% | 402 / 194 | 0.95 | 81.1% | 17 | 6 | 45 | 1 |
| **Account B** | ETHUSDT | LONG | $200.83 | $-799.17 | -79.92% | 65.6% | 391 / 205 | 0.86 | 88.7% | 10 | 8 | Never | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 38x, len 2: 25x, len 3: 19x, len 4: 12x, len 5: 6x (+8 more)
- **Account A (BTC) Loss Streaks:** len 1: 79x, len 2: 27x, len 3: 11x, len 4: 3x, len 5: 2x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 44x, len 2: 39x, len 3: 19x, len 4: 9x, len 5: 11x (+5 more)
- **Account B (ETH) Loss Streaks:** len 1: 94x, len 2: 27x, len 3: 13x, len 4: 1x, len 6: 1x (+1 more)

### 📍 Timeframe: `1h` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `1942`
- **Combined Portfolio Balance:** `$286.65` (Net PnL: `$-1,713.35`, ROI: `-85.67%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $142.35 | $-857.65 | -85.77% | 66.7% | 1296 / 646 | 0.91 | 87.1% | 16 | 8 | Never | 3 |
| **Account B** | ETHUSDT | LONG | $144.30 | $-855.70 | -85.57% | 66.7% | 1296 / 646 | 0.90 | 91.5% | 17 | 6 | 10 | 75 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 146x, len 2: 94x, len 3: 53x, len 4: 51x, len 5: 28x (+10 more)
- **Account A (BTC) Loss Streaks:** len 1: 283x, len 2: 96x, len 3: 29x, len 4: 14x, len 5: 4x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 130x, len 2: 93x, len 3: 66x, len 4: 40x, len 5: 30x (+11 more)
- **Account B (ETH) Loss Streaks:** len 1: 256x, len 2: 116x, len 3: 31x, len 4: 12x, len 5: 1x (+1 more)

### 📍 Timeframe: `4h` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `298`
- **Combined Portfolio Balance:** `$488.14` (Net PnL: `$-1,511.86`, ROI: `-75.59%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $332.29 | $-667.71 | -66.77% | 49.0% | 146 / 152 | 0.88 | 73.8% | 8 | 10 | 42 | 1 |
| **Account B** | ETHUSDT | LONG | $155.85 | $-844.15 | -84.42% | 47.0% | 140 / 158 | 0.79 | 92.1% | 6 | 8 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 38x, len 2: 15x, len 3: 11x, len 4: 4x, len 5: 3x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 37x, len 2: 19x, len 3: 7x, len 4: 6x, len 5: 2x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 38x, len 2: 19x, len 3: 10x, len 4: 3x, len 5: 2x (+1 more)
- **Account B (ETH) Loss Streaks:** len 1: 33x, len 2: 18x, len 3: 11x, len 4: 6x, len 5: 2x (+2 more)

### 📍 Timeframe: `4h` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `895`
- **Combined Portfolio Balance:** `$560.79` (Net PnL: `$-1,439.21`, ROI: `-71.96%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $394.11 | $-605.89 | -60.59% | 50.4% | 451 / 444 | 0.93 | 67.7% | 9 | 9 | 12 | 1 |
| **Account B** | ETHUSDT | LONG | $166.68 | $-833.32 | -83.33% | 48.7% | 436 / 459 | 0.87 | 89.8% | 7 | 8 | 4 | 9 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 109x, len 2: 54x, len 3: 23x, len 4: 18x, len 5: 9x (+4 more)
- **Account A (BTC) Loss Streaks:** len 1: 113x, len 2: 48x, len 3: 30x, len 4: 14x, len 5: 9x (+4 more)
- **Account B (ETH) Win Streaks:** len 1: 107x, len 2: 54x, len 3: 18x, len 4: 15x, len 5: 14x (+2 more)
- **Account B (ETH) Loss Streaks:** len 1: 102x, len 2: 47x, len 3: 28x, len 4: 18x, len 5: 13x (+3 more)

### 📍 Timeframe: `4h` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `516`
- **Combined Portfolio Balance:** `$494.27` (Net PnL: `$-1,505.73`, ROI: `-75.29%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $296.40 | $-703.60 | -70.36% | 65.9% | 340 / 176 | 0.88 | 80.0% | 15 | 6 | 64 | 1 |
| **Account B** | ETHUSDT | LONG | $197.87 | $-802.13 | -80.21% | 65.1% | 336 / 180 | 0.85 | 89.8% | 13 | 6 | Never | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 40x, len 2: 23x, len 3: 15x, len 4: 14x, len 5: 9x (+7 more)
- **Account A (BTC) Loss Streaks:** len 1: 77x, len 2: 19x, len 3: 13x, len 4: 4x, len 6: 1x
- **Account B (ETH) Win Streaks:** len 1: 38x, len 2: 21x, len 3: 17x, len 4: 16x, len 5: 10x (+6 more)
- **Account B (ETH) Loss Streaks:** len 1: 70x, len 2: 28x, len 3: 10x, len 4: 2x, len 5: 2x (+1 more)

### 📍 Timeframe: `4h` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `1371`
- **Combined Portfolio Balance:** `$645.26` (Net PnL: `$-1,354.74`, ROI: `-67.74%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $524.82 | $-475.18 | -47.52% | 67.9% | 931 / 440 | 0.96 | 54.8% | 17 | 5 | 175 | 3 |
| **Account B** | ETHUSDT | LONG | $120.44 | $-879.56 | -87.96% | 65.5% | 898 / 473 | 0.86 | 91.2% | 17 | 6 | 7 | 30 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 92x, len 2: 60x, len 3: 42x, len 4: 21x, len 5: 20x (+12 more)
- **Account A (BTC) Loss Streaks:** len 1: 183x, len 2: 60x, len 3: 29x, len 4: 10x, len 5: 2x
- **Account B (ETH) Win Streaks:** len 1: 94x, len 2: 77x, len 3: 41x, len 4: 31x, len 5: 18x (+10 more)
- **Account B (ETH) Loss Streaks:** len 1: 187x, len 2: 71x, len 3: 23x, len 4: 8x, len 5: 5x (+1 more)

### 📍 Timeframe: `1d` | Configuration: `TP3.0_SL3.0`

- **Completed Trade Cycles:** `228`
- **Combined Portfolio Balance:** `$1,427.37` (Net PnL: `$-572.63`, ROI: `-28.63%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $1,336.46 | $+336.46 | +33.65% | 53.1% | 121 / 107 | 1.04 | 49.8% | 10 | 5 | 23 | 1 |
| **Account B** | ETHUSDT | LONG | $90.91 | $-909.09 | -90.91% | 43.4% | 99 / 129 | 0.72 | 93.1% | 5 | 10 | 2 | 5 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 31x, len 2: 12x, len 3: 8x, len 4: 3x, len 6: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 33x, len 2: 13x, len 3: 7x, len 4: 3x, len 5: 3x
- **Account B (ETH) Win Streaks:** len 1: 28x, len 2: 18x, len 3: 3x, len 4: 4x, len 5: 2x
- **Account B (ETH) Loss Streaks:** len 1: 21x, len 2: 16x, len 3: 7x, len 4: 6x, len 6: 1x (+3 more)

### 📍 Timeframe: `1d` | Configuration: `TP1.5_SL1.5`

- **Completed Trade Cycles:** `448`
- **Combined Portfolio Balance:** `$1,327.38` (Net PnL: `$-672.62`, ROI: `-33.63%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $683.62 | $-316.38 | -31.64% | 50.7% | 227 / 221 | 0.95 | 62.1% | 10 | 7 | 29 | 1 |
| **Account B** | ETHUSDT | LONG | $643.76 | $-356.24 | -35.62% | 50.5% | 226 / 222 | 0.94 | 57.7% | 8 | 18 | 10 | 19 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 46x, len 2: 28x, len 3: 15x, len 4: 12x, len 5: 2x (+2 more)
- **Account A (BTC) Loss Streaks:** len 1: 55x, len 2: 24x, len 3: 13x, len 4: 5x, len 5: 4x (+2 more)
- **Account B (ETH) Win Streaks:** len 1: 44x, len 2: 35x, len 3: 14x, len 4: 8x, len 5: 2x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 55x, len 2: 19x, len 3: 18x, len 4: 9x, len 5: 3x (+2 more)

### 📍 Timeframe: `1d` | Configuration: `TP1.5_SL3.0`

- **Completed Trade Cycles:** `334`
- **Combined Portfolio Balance:** `$764.59` (Net PnL: `$-1,235.41`, ROI: `-61.77%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $552.54 | $-447.46 | -44.75% | 66.5% | 222 / 112 | 0.93 | 61.5% | 13 | 5 | 32 | 1 |
| **Account B** | ETHUSDT | LONG | $212.05 | $-787.95 | -78.79% | 63.5% | 212 / 122 | 0.75 | 86.8% | 9 | 4 | Never | 4 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 20x, len 2: 14x, len 3: 13x, len 4: 11x, len 5: 3x (+7 more)
- **Account A (BTC) Loss Streaks:** len 1: 46x, len 2: 14x, len 3: 7x, len 4: 3x, len 5: 1x
- **Account B (ETH) Win Streaks:** len 1: 23x, len 2: 20x, len 3: 8x, len 4: 13x, len 5: 4x (+3 more)
- **Account B (ETH) Loss Streaks:** len 1: 44x, len 2: 18x, len 3: 10x, len 4: 3x

### 📍 Timeframe: `1d` | Configuration: `TP0.75_SL1.5`

- **Completed Trade Cycles:** `520`
- **Combined Portfolio Balance:** `$1,544.62` (Net PnL: `$-455.38`, ROI: `-22.77%`)

| Account | Symbol | Side | Final Balance | Net PnL | ROI% | Win Rate | Wins / Losses | Profit Factor | Max DD | Max Win Streak | Max Loss Streak | Trades to +10% Profit | Trades to -3% Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Account A** | BTCUSDT | SHORT | $519.13 | $-480.87 | -48.09% | 66.2% | 344 / 176 | 0.89 | 59.9% | 13 | 6 | 52 | 13 |
| **Account B** | ETHUSDT | LONG | $1,025.49 | $+25.49 | +2.55% | 69.0% | 359 / 161 | 1.01 | 36.8% | 13 | 4 | 10 | 23 |

**Streak Frequency Distribution:**
- **Account A (BTC) Win Streaks:** len 1: 38x, len 2: 18x, len 3: 22x, len 4: 10x, len 5: 10x (+6 more)
- **Account A (BTC) Loss Streaks:** len 1: 73x, len 2: 26x, len 3: 9x, len 4: 2x, len 5: 2x (+1 more)
- **Account B (ETH) Win Streaks:** len 1: 31x, len 2: 23x, len 3: 21x, len 4: 12x, len 5: 7x (+7 more)
- **Account B (ETH) Loss Streaks:** len 1: 71x, len 2: 30x, len 3: 6x, len 4: 3x

---

## 5. Milestone Forensics: Trades to +10% Net Profit vs -3% Net Loss

Analysis of how rapidly each account crossed either the +10% target ($1,100 balance) or the -3% risk threshold ($970 balance):

| Case | Timeframe | Config | Account A Reached +10% | Account A Reached -3% | Account B Reached +10% | Account B Reached -3% |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| Case 1 | 1m | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #28 (2025-02-03) | Trade #6 (2025-01-09) | Trade #1 (2025-01-02) |
| Case 1 | 1m | TP1.5_SL1.5 | Trade #4 (2025-01-06) | Trade #11 (2025-01-08) | Trade #83 (2025-01-27) | Trade #1 (2025-01-02) |
| Case 1 | 1m | TP1.5_SL3.0 | Trade #4 (2025-01-06) | Trade #7 (2025-01-09) | ❌ Never | Trade #1 (2025-01-02) |
| Case 1 | 1m | TP0.75_SL1.5 | Trade #10 (2025-01-06) | Trade #20 (2025-01-08) | Trade #236 (2025-02-07) | Trade #1 (2025-01-02) |
| Case 1 | 5m | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #9 (2025-01-13) | Trade #6 (2025-01-09) | Trade #1 (2025-01-02) |
| Case 1 | 5m | TP1.5_SL1.5 | Trade #6 (2025-01-06) | Trade #17 (2025-01-09) | Trade #137 (2025-02-14) | Trade #1 (2025-01-02) |
| Case 1 | 5m | TP1.5_SL3.0 | Trade #4 (2025-01-06) | Trade #7 (2025-01-09) | ❌ Never | Trade #1 (2025-01-02) |
| Case 1 | 5m | TP0.75_SL1.5 | Trade #7 (2025-01-03) | Trade #17 (2025-01-08) | Trade #184 (2025-02-02) | Trade #1 (2025-01-02) |
| Case 1 | 15m | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #45 (2025-02-25) | Trade #31 (2025-02-02) | Trade #1 (2025-01-02) |
| Case 1 | 15m | TP1.5_SL1.5 | Trade #4 (2025-01-06) | Trade #13 (2025-01-09) | Trade #54 (2025-01-20) | Trade #1 (2025-01-02) |
| Case 1 | 15m | TP1.5_SL3.0 | Trade #4 (2025-01-06) | Trade #8 (2025-01-09) | ❌ Never | Trade #1 (2025-01-02) |
| Case 1 | 15m | TP0.75_SL1.5 | Trade #7 (2025-01-04) | Trade #38 (2025-01-13) | Trade #107 (2025-01-23) | Trade #1 (2025-01-02) |
| Case 1 | 1h | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #41 (2025-02-25) | Trade #6 (2025-01-09) | Trade #1 (2025-01-02) |
| Case 1 | 1h | TP1.5_SL1.5 | Trade #4 (2025-01-06) | Trade #11 (2025-01-09) | Trade #41 (2025-01-20) | Trade #1 (2025-01-02) |
| Case 1 | 1h | TP1.5_SL3.0 | Trade #4 (2025-01-06) | Trade #11 (2025-01-09) | Trade #32 (2025-01-23) | Trade #1 (2025-01-02) |
| Case 1 | 1h | TP0.75_SL1.5 | Trade #7 (2025-01-06) | Trade #20 (2025-01-09) | ❌ Never | Trade #1 (2025-01-02) |
| Case 1 | 4h | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #35 (2025-02-24) | Trade #6 (2025-01-09) | Trade #1 (2025-01-02) |
| Case 1 | 4h | TP1.5_SL1.5 | Trade #4 (2025-01-06) | Trade #9 (2025-01-08) | Trade #33 (2025-01-20) | Trade #1 (2025-01-02) |
| Case 1 | 4h | TP1.5_SL3.0 | ❌ Never | Trade #5 (2025-01-08) | Trade #32 (2025-01-27) | Trade #1 (2025-01-02) |
| Case 1 | 4h | TP0.75_SL1.5 | Trade #342 (2025-05-08) | Trade #12 (2025-01-08) | Trade #17 (2025-01-09) | Trade #1 (2025-01-02) |
| Case 1 | 1d | TP3.0_SL3.0 | Trade #2 (2025-01-06) | Trade #5 (2025-01-09) | Trade #17 (2025-01-28) | Trade #1 (2025-01-02) |
| Case 1 | 1d | TP1.5_SL1.5 | ❌ Never | Trade #17 (2025-01-22) | Trade #79 (2025-04-07) | Trade #1 (2025-01-02) |
| Case 1 | 1d | TP1.5_SL3.0 | ❌ Never | Trade #5 (2025-01-08) | ❌ Never | Trade #1 (2025-01-02) |
| Case 1 | 1d | TP0.75_SL1.5 | Trade #126 (2025-05-26) | Trade #6 (2025-01-09) | Trade #30 (2025-02-04) | Trade #1 (2025-01-02) |
| Case 2 | 1m | TP3.0_SL3.0 | Trade #44 (2025-02-28) | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-08) |
| Case 2 | 1m | TP1.5_SL1.5 | ❌ Never | Trade #1 (2025-01-01) | Trade #4 (2025-01-04) | Trade #28 (2025-01-13) |
| Case 2 | 1m | TP1.5_SL3.0 | Trade #80 (2025-02-25) | Trade #1 (2025-01-02) | ❌ Never | Trade #5 (2025-01-07) |
| Case 2 | 1m | TP0.75_SL1.5 | ❌ Never | Trade #3 (2025-01-02) | Trade #10 (2025-01-06) | Trade #19 (2025-01-08) |
| Case 2 | 5m | TP3.0_SL3.0 | Trade #54 (2025-02-28) | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-07) |
| Case 2 | 5m | TP1.5_SL1.5 | Trade #150 (2025-02-25) | Trade #1 (2025-01-01) | Trade #6 (2025-01-04) | Trade #13 (2025-01-08) |
| Case 2 | 5m | TP1.5_SL3.0 | Trade #86 (2025-02-25) | Trade #1 (2025-01-02) | ❌ Never | Trade #5 (2025-01-07) |
| Case 2 | 5m | TP0.75_SL1.5 | ❌ Never | Trade #3 (2025-01-02) | ❌ Never | Trade #16 (2025-01-07) |
| Case 2 | 15m | TP3.0_SL3.0 | ❌ Never | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-08) |
| Case 2 | 15m | TP1.5_SL1.5 | Trade #94 (2025-02-03) | Trade #1 (2025-01-01) | Trade #4 (2025-01-04) | Trade #13 (2025-01-09) |
| Case 2 | 15m | TP1.5_SL3.0 | Trade #77 (2025-02-25) | Trade #1 (2025-01-02) | ❌ Never | Trade #5 (2025-01-07) |
| Case 2 | 15m | TP0.75_SL1.5 | Trade #162 (2025-02-02) | Trade #3 (2025-01-02) | Trade #10 (2025-01-06) | Trade #23 (2025-01-08) |
| Case 2 | 1h | TP3.0_SL3.0 | Trade #69 (2025-03-11) | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-08) |
| Case 2 | 1h | TP1.5_SL1.5 | Trade #133 (2025-02-26) | Trade #1 (2025-01-01) | Trade #4 (2025-01-04) | Trade #19 (2025-01-10) |
| Case 2 | 1h | TP1.5_SL3.0 | Trade #45 (2025-02-03) | Trade #1 (2025-01-02) | ❌ Never | Trade #5 (2025-01-07) |
| Case 2 | 1h | TP0.75_SL1.5 | ❌ Never | Trade #3 (2025-01-02) | Trade #10 (2025-01-06) | Trade #75 (2025-01-20) |
| Case 2 | 4h | TP3.0_SL3.0 | Trade #42 (2025-02-28) | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-08) |
| Case 2 | 4h | TP1.5_SL1.5 | Trade #12 (2025-01-09) | Trade #1 (2025-01-01) | Trade #4 (2025-01-06) | Trade #9 (2025-01-08) |
| Case 2 | 4h | TP1.5_SL3.0 | Trade #64 (2025-02-26) | Trade #1 (2025-01-02) | ❌ Never | Trade #5 (2025-01-07) |
| Case 2 | 4h | TP0.75_SL1.5 | Trade #175 (2025-03-05) | Trade #3 (2025-01-02) | Trade #7 (2025-01-04) | Trade #30 (2025-01-13) |
| Case 2 | 1d | TP3.0_SL3.0 | Trade #23 (2025-02-18) | Trade #1 (2025-01-02) | Trade #2 (2025-01-03) | Trade #5 (2025-01-09) |
| Case 2 | 1d | TP1.5_SL1.5 | Trade #29 (2025-02-04) | Trade #1 (2025-01-01) | Trade #10 (2025-01-15) | Trade #19 (2025-01-24) |
| Case 2 | 1d | TP1.5_SL3.0 | Trade #32 (2025-02-12) | Trade #1 (2025-01-02) | ❌ Never | Trade #4 (2025-01-08) |
| Case 2 | 1d | TP0.75_SL1.5 | Trade #52 (2025-02-26) | Trade #13 (2025-01-14) | Trade #10 (2025-01-11) | Trade #23 (2025-01-24) |

---

## 6. Mathematical & Strategic Conclusions

1. **Asset Drift & Trend Dominance:** During 2025 to 2026, Bitcoin outperformed Ethereum significantly in relative strength (BTC dominance rose). Consequently, Case 1 (Long BTC / Short ETH) captures the structural trend of the pair, whereas Case 2 (Short BTC / Long ETH) suffers from negative asset drift.
2. **Synchronization Lag Effect:** Because the faster exit must wait for the slower exit before re-entering, the strategy avoids over-trading during single-leg consolidations, but holds dead capital while waiting for the lagging asset.
3. **Asymmetric Risk/Reward Impact:** Configurations with 1:2 adverse risk/reward (e.g. TP 0.75% / SL 1.5% or TP 1.5% / SL 3.0%) require high win rates (>67%) to remain profitable. Friction from trading fees on ultra-short scalps makes 1m high-frequency scalping fragile unless exchange fees are zero.
