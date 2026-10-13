# 🔬 FORENSIC AUDIT REPORT: BTC/ETH Hedged Pairs Strategy

> **Generated:** 2026-10-13 21:19:25 UTC
> **Auditor:** Independent Ground-Truth Backtester (v1.0)
> **Data Range:** 2020-01-01 to 2026-09-30 (59160 aligned 1H candles)

---

## 📋 Strategy Parameters (Locked Production Config)

| Parameter | Value |
|---|---|
| Initial Capital | $1,000.00 USDC |
| Notional Per Leg | $750.00 (BTC Long + ETH Short) |
| Total Exposure | 1.50x ($1,500 total) |
| Margin Required | $750 at 2x leverage |
| TP1 (De-Risk) | +0.20% → close 50% |
| BE Lock | +0.10% (after TP1) |
| TP2 (Runner) | +1.00% → close remaining 50% |
| Early-Cut SL | -0.40% (before TP1) |
| Primary Fee | 0.060% round-trip (Limit+Market) |
| Stress Fee | 0.090% round-trip (Market+Market) |

---

## 🎯 VERDICT SUMMARY

| Audit Check | Primary (0.060%) | Stress (0.090%) | Status |
|---|---|---|---|
| Net Profit | $-29,350.05 (-2935.01%) | $-46,482.45 (-4648.24%) | ❌ |
| Final Equity | $-28,350.05 | $-45,482.45 | — |
| Worst Daily DD | $50.85 (5.09%) | $61.65 (6.17%) | ❌ |
| Max Trailing DD | $29353.05 (2931.35%) | $46483.35 (4644.16%) | ❌ |
| Daily DD Breaches | 174 days | 485 days | ❌ |
| Max DD Breached? | YES ❌ | YES ❌ | ❌ |
| Challenge Pass Rate | 0.0% | 0.0% | ⚠️ |
| Avg Days to Pass | 0.0 | 0.0 | — |

---

## 📊 Trade Statistics

| Metric | Primary (0.060%) | Stress (0.090%) |
|---|---|---|
| Total Cycles | 38072 | 38072 |
| Pair Wins | 18525 | 18525 |
| Pair Losses | 19547 | 19547 |
| **Pair Win Rate** | **48.66%** | **48.66%** |

### BTC Leg Outcomes (Primary)

| Exit Type | Count | % |
|---|---|---|
| TP2 (Full Runner) | 3217 | 8.4% |
| BE Stop (Locked Profit) | 22425 | 58.9% |
| Early Cut (-0.40%) | 12430 | 32.6% |
| TP1 Hit Rate | 25642 | 67.4% |

### ETH Leg Outcomes (Primary)

| Exit Type | Count | % |
|---|---|---|
| TP2 (Full Runner) | 3510 | 9.2% |
| BE Stop (Locked Profit) | 21913 | 57.6% |
| Early Cut (-0.40%) | 12649 | 33.2% |
| TP1 Hit Rate | 25423 | 66.8% |

---

## 🔍 FORENSIC AUDIT CHECKLIST

### 1. Intra-Candle Ambiguity Resolution (1-Minute Resolution)
- **Method:** When TP1 (+0.20%) and Early-Cut SL (-0.40%) are both triggered within the same 1H candle, chronological **1-minute OHLCV candles** from Binance Vision are evaluated minute-by-minute ($m \in [0, 59]$).
- **Adversarial Rule:** If within the **exact same 1-minute candle** both TP and SL are touched, the system strictly declares **Early-Cut SL** (zero optimistic fill bias).
- **Phase 2 Disputes:** If both TP2 (+1.00%) and BE-stop (+0.10%) are touched in the same 1H candle, 1-minute candles are evaluated; if both are hit within the same 1m candle, **BE-stop is declared**.
- **Status:** ✅ 100% physically resolved using 1-minute Binance Vision data.

### 2. Lookahead Bias Verification
- **Entry Price:** Uses the `Open` price of the candle at cycle start. ✅
- **Exit Prices:** Constrained to exact TP/SL/BE price levels within the candle's [Low, High] range. ✅
- **No future data** is used to determine entry or exit timing. ✅

### 3. Daily Drawdown (00:00 UTC Boundary)
- **Measurement:** Start-of-day equity (at 00:00 UTC) minus intraday equity trough.
- **Worst Single Day:** $50.85 (5.09%) on 2021-01-19
- **3% Limit ($30.00):** ❌ BREACHED on 174 day(s)

### 4. Max Overall Trailing Drawdown
- **Measurement:** Peak equity to trough equity (trailing high-water mark).
- **Worst Overall DD:** $29353.05 (2931.35%) on 2026-09-28
- **5% Limit ($50.00):** ❌ BREACHED

### 5. Fee Accounting Integrity
- **Primary Model:** Limit entry (0.015%) + Market exit (0.045%) = **0.060% round-trip** per fill.
- **Stress Model:** Market entry (0.045%) + Market exit (0.045%) = **0.090% round-trip** per fill.
- **Application:**
  - On TP1 (50% partial): Fee = $375 × fee_rate = $0.2250 (primary) / $0.3375 (stress)
  - On TP2/BE/Early-Cut (remaining 50%): Fee = $375 × fee_rate
  - On Early-Cut (100%): Fee = $750 × fee_rate = $0.4500 (primary) / $0.6750 (stress)
- **Status:** ✅ Fees deducted per-fill on actual notional transacted.

### 6. Rolling Challenge Pass Rate
- **Windows Tested:** 348 (starting every 7 days, 2020-2026)
- **Passed (Primary):** 0/348 = **0.0%**
- **Passed (Stress):** 0/348 = **0.0%**
- **Average Days to +10% (Primary):** 0.0 days
- **Failure Breakdown (Primary):** Daily DD fails: 53, Max DD fails: 295, Timeouts: 0

---

## ⚠️ BUGS & FLAWS DETECTED IN PREVIOUS SCRIPTS

### Critical Issues Found in Existing Codebase

1. **`run_full_history_backtest_2020_2026.py` - Phantom Breakeven Ratchet Bug**
   - The inner loop only checks `hit_tp` at +1.50% and `hit_sl` at -1.50%.
   - After partial TP at +0.20%, the stop should move to +0.05% (BE). But the loop **never enforces the BE stop** — if price retraces past BE to -1.50%, the backtest only exits at -1.50%.
   - **Impact:** Overstates win rate on the remaining 50% position. Trades that should have exited at BE (+0.05%) instead survive and either hit full TP or full SL.

2. **`run_full_history_backtest_2020_2026.py` - Intra-Candle Path Assumption**
   - Uses per-candle `b_mfe` (max favorable excursion from High) to determine if partial TP (+0.20%) was reached.
   - But within a single 1H candle, the High could occur AFTER the Low. If the candle has Low = -0.60% (SL hit) and High = +0.25% (partial TP), the code assumes partial TP was reached before SL.
   - **Impact:** On candles where both TP and SL are reachable, the backtest optimistically awards partial profit.

3. **`propfirm_1k_exact_sim.py` - Inconsistent Fee Treatment**
   - Uses `rt_fee = 0.09` as a flat percentage deducted once. But the fee should be applied to each exit portion separately (50% partial + 50% final = two separate fills).
   - When early-cut fires at -0.40%, fee is `rt_fee = 0.09%` on the full position (correct).
   - When TP1 hits + BE/TP2, fee should be `0.09%/2 + 0.09%/2 = 0.09%` (approximately correct by coincidence, but the per-portion breakdown is not explicit).

4. **`engine.py` - Fee on Entry vs Exit Notional**
   - Fees are calculated as `notional_a * fee_rate` using entry-time notional. On TP exits, the actual exit notional is higher (price moved favorably). This slightly underestimates fees on winning trades.

---

## 📈 Artifacts Generated

| File | Description |
|---|---|
| `all_trades.csv` | Cycle-by-cycle trade log with per-leg details |
| `summary_matrix.csv` | Key metrics comparison (primary vs stress fees) |
| `EXPERIMENT_REPORT.md` | This forensic audit report |

---

*Report generated by Independent Forensic Backtester v1.0*
