# MASTER QUANTITATIVE RESEARCH DOSSIER
## VOLUME VI: CODEBASE ARCHITECTURE, ALGORITHMS & REPRODUCTION MANUAL
**Complete Source Code Reference, Engineering Architecture & Exact Reproduction Guide**  
**Author**: Autonomous Quantitative Research Agent  
**Date**: September 2026  

---

## 1. Codebase Architecture & Key Components

The research repository contains a complete quantitative backtesting and live execution stack:

```text
(COPY-SandBoxed) KCEX/
├── BACKTESTER/
│   ├── engine/
│   │   ├── config.py             # BacktestConfig dataclass
│   │   ├── data_loader.py        # Dual-feed OHLCVLoader & TickTradeStreamer
│   │   ├── execution_sim.py      # BacktestExecutionEngine & VirtualClock
│   │   ├── market_sim.py         # BacktestMarket contract specs & fee models
│   │   ├── metrics.py            # PerformanceCalculator & PerformanceSummary
│   │   ├── reporting.py          # BacktestReporter (CSV, HTML, JSON export)
│   │   └── scanner.py            # Data directory scanners & timestamp parsers
│   ├── Historical_Trades_Data_Binance/  # Millisecond trade CSV files
│   └── OHLCV_Data_Binance/              # 1m candlestick CSV files (20 months)
├── kcex/
│   ├── engine/
│   │   ├── models.py             # Core models: TradeOutcome, TradeSignal, OrderDirection
│   │   └── strategy.py           # StochasticRSIStrategy, EMACrossoverStrategy, MasterplanStrategy
│   └── market.py                 # ContractInfo definitions
├── strategies/
│   └── filters.py                # FilterPipeline (ADX, HTF EMA, Hourly, Duration)
├── research/
│   ├── EXPERIMENT_LEDGER.csv     # Master ledger of all Phase 1 experiments
│   └── tools/                    # Autonomous analysis & backtest runner suite
├── research_agent_output/        # Phase 1 official deliverables (01 to 06)
├── research_agent_phase2/        # Phase 2 official deliverables (01 to 10)
└── RESEARCH_DOSSIER/             # Master 6-Volume Comprehensive Research Dossier
```

---

## 2. The Critical Tick Streamer Bug Fix

### Location: `BACKTESTER/engine/data_loader.py` (lines 320–330)

### Defect Analysis:
In the original implementation of `TickTradeStreamer.stream_ticks()`:
```python
# ORIGINAL DEFECTIVE CODE:
_, file_first_ts = self._get_file_first_ts(fpath)
if end_ms and file_first_ts and file_first_ts > end_ms:
    break
```
When `end_ms` was None (as in `stream_ticks(self.symbol, start_ms=entry_ms)`), the engine did not check whether `file_first_ts` was months into the future relative to `start_ms`. For trades occurring between January and June 2026 (where no tick files existed locally), the streamer opened `TRUMPUSDT-trades-2026-07.csv` (July 2026) at offset 0, reading July tick prices (~$1.60) for a January trade (price ~$5.11). This instantly closed the trade with an exit timestamp in July, causing the simulation loop to jump directly to the end of July after only 1 trade.

### The Corrected Implementation:
```python
# CORRECTED IMPLEMENTATION:
_, file_first_ts = self._get_file_first_ts(fpath)
if file_first_ts and file_first_ts > start_ms + 86400000:
    # File starts more than 1 day in the future relative to trade entry; stop/skip
    break
if end_ms and file_first_ts and file_first_ts > end_ms:
    break
```
This fix ensures that when no local tick files cover the target date, `stream_ticks()` yields nothing, allowing the execution engine to cleanly execute high-fidelity OHLCV candle fallback.

---

## 3. Core Algorithms of the Validation Tools

### 3.1 `phase2_reproduce.py`
Executes Baseline vs Candidate on July 1–24, 2026 with millisecond tick replay and verifies exact metrics:
```python
from research.tools.experiment_suite import run_backtest_direct

# Baseline (SL = 25% ROE)
m_base, _ = run_backtest_direct(
    symbol="TRUMP_USDT", strategy_mode="STOCH_RSI", stoch_preset="FAST_SCALP",
    start_time="2026-07-01", end_time="2026-07-24", tp_ticks=2,
    sl_mode="ROE", sl_roe_pct=25.0, use_tick_data=True
)

# Candidate (SL = 5 ticks)
m_cand, _ = run_backtest_direct(
    symbol="TRUMP_USDT", strategy_mode="STOCH_RSI", stoch_preset="FAST_SCALP",
    start_time="2026-07-01", end_time="2026-07-24", tp_ticks=2,
    sl_mode="TICKS", sl_ticks=5, use_tick_data=True
)
```

### 3.2 `phase2_time_segments.py`
Runs 56 parallel backtests across 8 months using Python's `ProcessPoolExecutor`:
```python
from concurrent.futures import ProcessPoolExecutor, as_completed

MONTHS = [
    ("2026_01_Jan", "2026-01-01", "2026-01-31"),
    ("2026_02_Feb", "2026-02-01", "2026-02-28"),
    ("2026_03_Mar", "2026-03-01", "2026-03-31"),
    ("2026_04_Apr", "2026-04-01", "2026-04-30"),
    ("2026_05_May", "2026-05-01", "2026-05-31"),
    ("2026_06_Jun", "2026-06-01", "2026-06-30"),
    ("2026_07_Jul", "2026-07-01", "2026-07-31"),
    ("2026_08_Aug", "2026-08-01", "2026-08-31"),
]
SL_CHOICES = [2, 3, 4, 5, 6, 7, 10]
# Dispatches tasks across 3 worker processes and records to 04_TIME_SEGMENT_RESULTS.csv
```

### 3.3 `phase2_counterfactual.py`
Forward-replays 4,436 raw strategy signals against seven simultaneous barrier targets:
```python
# Evaluates MFE, MAE, and outcome under each stop loss
for tick in tick_gen:
    # Track max favorable excursion and adverse excursion
    fav = (tick.price - entry_price) / pu if direction == OrderDirection.LONG else (entry_price - tick.price) / pu
    adv = (entry_price - tick.price) / pu if direction == OrderDirection.LONG else (tick.price - entry_price) / pu
    for sl in [2, 3, 4, 5, 6, 7, 10]:
        if sl not in stop_outcomes:
            if fav >= 2.0:
                stop_outcomes[sl] = "WIN"
            elif adv >= float(sl):
                stop_outcomes[sl] = "LOSS"
```

---

## 4. Complete Reproduction CLI Manual

To independently execute the entire quantitative research suite from terminal:

```bash
# 1. Verify Claim Reproduction
python research/tools/phase2_reproduce.py

# 2. Re-run Full Stop Loss Sweep (1-15 ticks)
python research/tools/phase2_sl_sweep.py

# 3. Re-run 8-Month Temporal Generalization (56 parallel runs)
python research/tools/phase2_time_segments.py

# 4. Re-run Cross-Pair Generalization (TRUMP vs DOGE)
python research/tools/phase2_pairs.py

# 5. Re-run Directional and Multi-Strategy Suite
python research/tools/phase2_directions.py

# 6. Re-run Per-Trade Counterfactual Matrix Replay
python research/tools/phase2_counterfactual.py

# 7. Re-run Slippage, Bootstrap, and Null Robustness Battery
python research/tools/phase2_robustness.py
```
All outputs will be deterministically re-generated in `research_agent_phase2/` matching the reported tables to 4 decimal places.
