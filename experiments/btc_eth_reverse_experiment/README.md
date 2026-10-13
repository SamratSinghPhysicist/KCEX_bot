# Dual-Account Reverse Trading Experiment (BTC vs ETH)

## Overview
This experiment tests a synchronized pairs trading strategy using two segregated accounts:
- **Account A:** Trades exclusively **BTCUSDT** (starts with **$1,000 USDT**).
- **Account B:** Trades exclusively **ETHUSDT** (starts with **$1,000 USDT**).
- **Position Sizing:** 100% current compounding capital per account at **2x leverage**.
- **Reverse Trading Direction:**
  - **Case 1:** Always Buy BTC (Long), Sell ETH (Short)
  - **Case 2:** Always Sell BTC (Short), Buy ETH (Long)
- **Take Profit (TP) & Stop Loss (SL) Configurations:**
  1. `TP = 3.0%`, `SL = 3.0%`
  2. `TP = 1.5%`, `SL = 1.5%`
  3. `TP = 1.5%`, `SL = 3.0%`
  4. `TP = 0.75%`, `SL = 1.5%`
- **Synchronization Rule:** Both accounts enter simultaneously. The next trade is taken only when, and as soon as, **both** accounts become free.
- **Dispute Resolution:** In case both TP and SL are hit in the same candle, 1-minute sub-candles are evaluated chronologically. If both are hit within the same 1-minute candle, **Stop Loss** is declared.
- **Period:** `2025-01-01` to `2026-08-31`
- **Timeframes:** `1m`, `5m`, `15m`, `1h`, `4h`, `1d`

## Running Locally

To run the complete 48-combination backtest locally:

```bash
python experiments/btc_eth_reverse_experiment/run_experiment.py
```

Options:
- `--start-date 2025-01-01`
- `--end-date 2026-08-31`
- `--timeframes 1m,5m,15m,1h,4h,1d`
- `--cases "Case 1,Case 2"`
- `--capital 1000.0`
- `--leverage 2.0`
- `--fee-rate 0.0004` (0.04% roundtrip)

## Running on GitHub Actions

1. Navigate to GitHub Actions tab in the repository:
   `.github/workflows/experiment_btc_eth_reverse.yml`
2. Click **Run workflow** and customize any input parameters.
3. Or dispatch via Python script:
   ```bash
   python experiments/btc_eth_reverse_experiment/dispatch_experiment.py
   ```
4. Artifacts generated:
   - `summary_matrix.csv`: Complete table of all 48 configurations with Account A, Account B, and Combined stats.
   - `all_trades.csv`: Trade-by-trade breakdown including entry/exit timestamps, prices, exit reasons, PnL, and balance.
   - `EXPERIMENT_REPORT.md`: Exhaustive Markdown report published directly to GitHub Step Summary.
