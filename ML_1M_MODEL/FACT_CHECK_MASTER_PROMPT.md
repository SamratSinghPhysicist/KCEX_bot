# Quantitative Audit & Independent Fact-Checking Master Prompt
**Target System:** `ML_1M_MODEL/` Repository & GitHub Actions Cloud Pipeline  
**Asset Scope:** `TRUMPUSDT` (Primary), `DOGEUSDT` (Secondary)  
**Timeframe:** 1-Minute Microstructure (1m OHLCV + Ticker Trades Order Flow)  
**Auditor Target:** Any Senior Quantitative Research & Algorithmic Trading Systems Auditor AI (e.g., Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1)

---

## 📋 Instructions for the Auditor AI
You are acting as an **Independent Senior Quantitative Trading Auditor and Algorithmic Systems Engineer**.
You have been provided with the complete codebase, historical market data paths, configuration files, and empirical backtest results for an automated 1-minute crypto futures machine learning trading engine.

Your task is to conduct an **uncompromising, mathematically rigorous, end-to-end audit** of the system. You must:
1. **Fact-check every line of code** for subtle lookahead bias, execution latency leakage, data snooping, and mathematical errors.
2. **Independently execute the backtesting pipeline** on your own compute environment without trusting any pre-computed numbers or summaries.
3. **Verify exchange cost models**, fee schedules, dynamic slippage multipliers, and margin mechanics.
4. **Evaluate statistical validity**, sample size sufficiency, $p$-values, Monte Carlo robustness, and Sharpe ratio significance.
5. **Issue a formal verdict** (PASS / CONDITIONAL PASS / REJECT) with specific findings and mathematical proofs.

---

## 🏛️ 1. Project Background & System Specifications

### Asset & Exchange Mechanics
- **Primary Instrument:** `TRUMPUSDT` (Binance Futures data / KCEX execution).
- **Secondary Instrument:** `DOGEUSDT`.
- **Timeframe:** 1-Minute (`1m`) OHLCV bars combined with streaming millisecond tick trade logs (`is_buyer_maker` directional aggressor flags).
- **Exchange Fee Structure (KCEX Real-World Specs):**
  - **`TRUMPUSDT` & `DOGEUSDT`:** **0.0% Maker Fee, 0.0% Taker Fee** (Zero exchange fees).
  - **Other pairs (e.g. BTC, ETH):** **0.0% Maker Fee, 0.01% Taker Fee** (No maker fee).
- **Slippage Model:**
  - `TRUMPUSDT` tick size: `$0.001`.
  - Baseline execution slippage: **2 ticks** (`$0.002`).
  - Dynamic volatility slippage: Automatically scales up to **6–8 ticks** (`$0.006–$0.008`) during volatility surges ($\text{ATR} / \overline{\text{ATR}} \ge 1.8\times$).
  - Stress testing range: **1 to 10 ticks**.
- **Leverage & Position Sizing:**
  - Nominal leverage: **20x margin**.
  - Risk allocation: **10% of portfolio equity** per trade.

---

## 📂 2. Codebase Architecture & File Responsibilities

All strategy logic resides in the isolated subfolder `ML_1M_MODEL/`:

```
d:\My_Bots\Trading\KCEX\
├── ML_1M_MODEL/
│   ├── config.py              # Central asset specs, fee schedule, barrier configs, HGB params
│   ├── data_loader.py         # Dual ingestion: D:\ local drive or Binance Vision cloud download
│   ├── orderflow_aggregator.py# Chunked streaming tick parser (CVD, taker ratio, VWAP, whale trades)
│   ├── features.py            # Deep technicals: multi-horizon returns, volatility, Carter Squeeze, OFI
│   ├── labeler.py             # Symmetric triple barrier method (H=15, TP=3.0x ATR, SL=1.5x ATR)
│   ├── model.py               # 100% Scikit-Learn pipeline (HistGradientBoostingClassifier & Regressors)
│   ├── trainer.py             # Purged Walk-Forward train/test split with embargo period
│   ├── evaluator.py           # Out-of-sample backtest engine with latency fill and worst-case tie-breaks
│   ├── predict.py             # Live inference CLI emitting BUY/SELL/WAIT with dynamic TP/SL ticks
│   ├── run_pipeline.py        # Master pipeline orchestrator CLI
│   ├── test_pipeline.py       # Automated unit test suite
│   ├── requirements.txt       # Dependencies: scikit-learn, pandas, numpy, scipy, pyarrow
│   ├── data_cache/            # Parquet and pickle cached 1m order flow bars
│   ├── reports/               # Performance markdown reports, trade logs CSV, and metrics JSON
│   └── saved_models/          # Pickled Scikit-Learn model artifacts
└── .github/
    └── workflows/
        └── ml_model_train_test.yml  # Remote GitHub Actions automated training & testing workflow
```

---

## 🔍 3. Known Discrepancies & Silent Bugs Audit History

In earlier iterations (Runs 1 to 4), an audit revealed several silent bugs and environment divergences that have since been addressed. **Your job as the auditor is to inspect the codebase and confirm whether each fix is mathematically sound and completely eliminates the defect:**

### Bug 1: Host Timezone Timestamp Displacement (`data_loader.py`)
- **Vulnerability:** `datetime.datetime.strptime().timestamp()` on naive datetime objects defaulted to host local timezone. On Indian Standard Time (IST, UTC+05:30), `s_ts` and `e_ts` shifted by 330 minutes (330 candles) compared to GitHub Actions cloud runners running in UTC. This caused local datasets to have 68 trades vs cloud runner's 36 trades.
- **Required Check:** Verify that `data_loader.py` enforces `replace(tzinfo=datetime.timezone.utc).timestamp()` and that `pd.to_datetime(..., utc=True)` is used everywhere. Confirm that loading `TRUMPUSDT` for `2026-06-01` to `2026-08-31` produces **exactly 132,480 1-minute bars** both locally and in cloud runners.

### Bug 2: Intra-Bar Simultaneous TP/SL Tie-Breaking Bias (`evaluator.py`)
- **Vulnerability:** If within a single 1-minute bar $i$, both `high >= tp_price` AND `low <= sl_price` occurred, the previous code evaluated `if h >= tp_price:` first, artificially awarding a win.
- **Required Check:** Verify that `evaluator.py` enforces conservative institutional accounting: if both barriers are breached within the same candle, the stop-loss (`SL_HIT`) is strictly triggered first.

### Bug 3: Execution Latency & Same-Candle Lookahead (`evaluator.py`)
- **Vulnerability:** Decision at bar $i$ was previously filled at bar $i$ close price, ignoring that candle $i$ close is only known after the bar finishes.
- **Required Check:** Verify that decisions computed at bar $i$ close strictly enter on **bar $i+1$ open** (`opens[i+1] + entry_slip` for Long, `opens[i+1] - entry_slip` for Short), with zero lookahead into bar $i+1$'s high/low before entry.

### Bug 4: Dummy Feature Importances (`model.py`)
- **Vulnerability:** `HistGradientBoostingClassifier` does not expose `feature_importances_`. The code previously fell back to `np.ones`.
- **Required Check:** Verify that `get_feature_importances` implements genuine `sklearn.inspection.permutation_importance` on a validation holdout slice.

### Bug 5: Probability Distortion via `class_weight='balanced'` (`model.py`)
- **Vulnerability:** In an unbalanced dataset (WAIT ~85%, BUY ~7.5%, SELL ~7.5%), `class_weight='balanced'` artificially inflated minority class probabilities by ~5.6x, making fixed probability thresholds fragile.
- **Required Check:** Verify how class weights and probability thresholds are handled and whether predicted probabilities reflect genuine empirical likelihoods.

---

## 🧪 4. Step-by-Step Fact-Checking Verification Protocol

Execute the following verification steps in sequence:

### Step 1: Automated Unit Test Suite
Run the unit test suite to verify pipeline integrity:
```bash
python -m unittest ML_1M_MODEL/test_pipeline.py
```
*Verification criteria:* 100% of tests must pass with 0 errors and 0 failures.

### Step 2: Timestamp Alignment & Candle Count Verification
Run the data loader on `TRUMPUSDT` for the evaluation period (`2026-06-01` to `2026-08-31`):
```python
from ML_1M_MODEL.data_loader import load_ohlcv_range
df = load_ohlcv_range("TRUMPUSDT", "2026-06-01", "2026-08-31")
assert len(df) == 132480, f"Expected 132,480 candles, got {len(df)}"
assert str(df['datetime'].iloc[0]) == "2026-06-01 00:00:00+00:00"
assert str(df['datetime'].iloc[-1]) == "2026-08-31 23:59:00+00:00"
```

### Step 3: Lookahead Bias & Leakage Audit
Inspect `features.py` and `labeler.py`:
- In `features.py`: Confirm that every technical indicator (EMA, RSI, ATR, Parkinson, Garman-Klass, Bollinger Bands, Volume Z-score) uses exclusively backward-looking rolling windows (`shift`, `rolling`, `ewm`) with **zero forward shifts**.
- In `labeler.py`: Confirm that target labels (`target_label`, `target_tp_dist`, `target_sl_dist`) look forward into `i+1 : i+1+H`, but are **never included** in `feature_cols` passed to `model.fit()`.
- In `trainer.py`: Confirm that the train/test split has an `embargo_bars` gap ($\ge 30$ bars) strictly preventing boundary leakage between training targets and test features.

### Step 4: Independent Out-of-Sample Backtest Execution
Execute the pipeline on your own compute:
```bash
python -m ML_1M_MODEL.run_pipeline --symbol TRUMPUSDT --start 2026-06-01 --end 2026-08-31 --horizon 15 --tp-mult 3.0 --sl-mult 1.5 --confidence 0.70
```
Extract and verify the out-of-sample metrics:
- Number of test bars (August): **`26,493`**
- Total trades taken ($N$)
- Win rate (%)
- Profit Factor ($PF = \text{Gross Profit} / \text{Gross Loss}$)
- Maximum Drawdown (%)
- Expectancy per trade ($)
- Annualized Sharpe Ratio

### Step 5: Cost & Slippage Stress Test
Modify `slippage_ticks` in `config.py` across `[1.0, 2.0, 3.0, 5.0, 7.0, 10.0]` ticks.
Confirm whether Profit Factor remains $> 1.20$ under realistic slippage regimes.

---

## 📊 5. Deliverables Required in Your Audit Report
Produce a formal Quantitative Audit Report containing:
1. **Executive Verdict:** (APPROVED / CONDITIONAL / REJECTED) with high-level summary.
2. **Verification Table:** Side-by-side comparison of claimed vs independently reproduced metrics.
3. **Lookahead Bias & Leakage Audit Results:** Line-by-line confirmation of data isolation.
4. **Microstructure & Execution Realism Analysis:** Assessment of next-bar open fills, intra-bar tie-breaking, and dynamic slippage scaling.
5. **Statistical Significance Testing:**
   - Binomial test $p$-value for $H_0: \text{Win Rate} \le 33.3\%$ (or break-even win rate given 2:1 RR).
   - Deflated Sharpe Ratio (DSR) or $t$-statistic for sample size $N$.
6. **Actionable Recommendations:** Any further enhancements needed prior to live automated capital deployment.
