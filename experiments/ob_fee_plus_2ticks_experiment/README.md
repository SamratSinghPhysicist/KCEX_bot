# Experiment: Order Block + Demand Zone Strategy with Fee Coverage + 2 Ticks Take Profit

## 1. Executive Summary & Objective

In the baseline Vivek Yadav Order Block + Demand Zone strategy, trades are targeted with a **1:2 Risk-to-Reward ratio** and an optional **50% partial exit at 1:1** with breakeven ratchet.

This experiment tests an alternative, high-win-rate rapid-scalping thesis:
- **Stop Loss:** Retains the exact same placement anchored strictly to the Order Block structural boundary ($ob.low - \text{buffer\_ticks} \times pu$ for Longs, $ob.high + \text{buffer\_ticks} \times pu$ for Shorts).
- **Take Profit:** Instead of aiming for 1:2 R:R, the TP is reduced to **just enough price movement to cover 100% round-trip taker trading fees + 2 extra ticks of guaranteed net profit**.
- **Partial TP:** Completely disabled (100% position exits at the fee+2tick target).
- **Disambiguation Rule:** Pure OHLCV execution. When both TP and SL are breached in the same multi-minute candle, 1m sub-candles are evaluated chronologically. If the discrepancy persists within the same 1m candle, the engine conservatively declares **Stop Loss Hit**.

---

## 2. Mathematical Formulation of Fee Coverage + 2 Ticks TP

When entering and exiting via market orders, both legs incur taker fees.
Let:
- $P_{\text{entry}}$ = Entry fill price (including adverse entry slippage)
- $Q$ = Underlying trade quantity
- $f_{\text{taker}}$ = Taker fee rate (e.g. $0.0001$ for $0.01\%$, $0.0005$ for $0.05\%$, $0.0010$ for $0.10\%$)
- $pu$ = Minimum price unit (tick size)
- $ps$ = Price decimal precision

### Total Round-Trip Fee Calculation:
$$\text{Fee}_{\text{open}} = Q \times P_{\text{entry}} \times f_{\text{taker}}$$
$$\text{Fee}_{\text{close}} = Q \times P_{\text{exit}} \times f_{\text{taker}}$$
$$\text{Fee}_{\text{total}} = Q \times (P_{\text{entry}} + P_{\text{exit}}) \times f_{\text{taker}}$$

### Gross and Net Gain:
For a Long trade:
$$\text{Gross PnL} = Q \times (P_{\text{exit}} - P_{\text{entry}})$$
$$\text{Net PnL} = \text{Gross PnL} - \text{Fee}_{\text{total}} = Q \left[ P_{\text{exit}} (1 - f_{\text{taker}}) - P_{\text{entry}} (1 + f_{\text{taker}}) \right]$$

To cover 100% of fees ($\text{Net PnL} = 0$):
$$P_{\text{exit}} = P_{\text{entry}} \times \frac{1 + f_{\text{taker}}}{1 - f_{\text{taker}}}$$
$$\Delta P_{\text{fees}} = P_{\text{exit}} - P_{\text{entry}} = P_{\text{entry}} \times \frac{2 f_{\text{taker}}}{1 - f_{\text{taker}}}$$

### Discrete Tick Target Calculation:
$$\text{fee\_ticks} = \max\left(1, \left\lceil \frac{\Delta P_{\text{fees}}}{pu} \right\rceil \right)$$
$$\text{target\_ticks} = \text{fee\_ticks} + 2$$

For Long:
$$P_{\text{TP}} = \text{round}\left(P_{\text{entry}} + \text{target\_ticks} \times pu, ps\right)$$

For Short:
$$P_{\text{TP}} = \text{round}\left(P_{\text{entry}} - \text{target\_ticks} \times pu, ps\right)$$

### Net Profit Guarantee:
Because $\text{fee\_ticks}$ rounds *up* ($\lceil \cdot \rceil$), closing at $P_{\text{TP}}$ is guaranteed to leave **at least 2 full ticks of net profit** after all exchange fees are deducted.

---

## 3. Experimental Parameter Variations

| Dimension | Variations Tested |
| :--- | :--- |
| **Trading Assets** | `BTC_USDT`, `TRUMP_USDT`, `1000000MOG_USDT`, `DOGE_USDT`, `ETH_USDT`, `SOL_USDT`, `XAU_USDT`, `XAG_USDT`, `CL_USDT`, `XRP_USDT` |
| **Fee Tiers** | 1. 0% Maker / 0.01% Taker (Round-trip taker = 0.02%)<br>2. 0% Maker / 0.05% Taker (Round-trip taker = 0.10%)<br>3. 0.10% Maker / 0.10% Taker (Round-trip taker = 0.20%) |
| **Slippage** | `1`, `2`, `3`, `4`, `5`, `6`, `7` ticks (applied adversely to entry and stop-loss fills) |
| **Timeframes** | `1m`, `5m`, `15m`, `1h`, `4h`, `1d` |
| **Backtest Period**| `2026-01-01` to `2026-08-31` (8 months historical data) |
| **Capital & Sizing**| $100.00 initial USDT, 10x leverage, 10% margin sizing per trade |
| **Combinations** | $3 \text{ fees} \times 7 \text{ slippages} \times 6 \text{ timeframes} = 126 \text{ runs per coin}$ |

---

## 4. Candle Disambiguation Protocol

To eliminate lookahead bias and ticker inaccuracies:
1. **Ticker Data Disabled:** `use_tick_data = False`. Only verified OHLCV candles are consumed.
2. **Candle Open Breach Check:** If candle open already gaps beyond TP or SL, that price level triggers immediately.
3. **1m Sub-Candle Resolution:** For timeframes $> 1\text{m}$, when both TP and SL fall within the high/low range of the candle, 1m sub-candles spanning $[t_{\text{open}}, t_{\text{close}}]$ are evaluated sequentially in chronological order.
4. **Conservative Tie-Breaking:** If both TP and SL are breached within the same 1m candle, the engine declares **Stop Loss Hit**.

---

## 5. Directory Structure & Files

```
experiments/
└── ob_fee_plus_2ticks_experiment/
    ├── __init__.py                     # Package export
    ├── strategy.py                     # FeePlus2TicksOBStrategy
    ├── run_experiment.py               # Batch sweep runner & reporting
    ├── test_experiment.py              # Unit & integration test suite
    ├── dispatch_experiment.py          # GitHub Actions CLI dispatcher
    ├── README.md                       # Documentation & mathematical proof
    └── reports/                        # Output reports directory
        ├── {symbol}_{tag}_batch_matrix.csv
        ├── {symbol}_{tag}_batch_matrix.md
        ├── {symbol}_{tag}_trades.csv
        ├── master_batch_matrix.csv
        ├── master_batch_matrix.md
        └── master_all_trades.csv
```

---

## 6. How to Run Locally

### Run Unit Tests:
```powershell
python experiments/ob_fee_plus_2ticks_experiment/test_experiment.py
```

### Run Single Coin Sweep:
```powershell
python experiments/ob_fee_plus_2ticks_experiment/run_experiment.py \
  --symbol TRUMP_USDT \
  --timeframes 15m,1h \
  --fee-indices 0,1,2 \
  --slippage-ticks 1,2,3 \
  --start 2026-01-01 \
  --end 2026-08-31 \
  --tag my_local_run
```

### Run All Coins:
```powershell
python experiments/ob_fee_plus_2ticks_experiment/run_experiment.py \
  --symbol ALL \
  --timeframes 15m,1h,4h,1d \
  --fee-indices 0,1,2 \
  --slippage-ticks 1,2,3,4,5,6,7
```

---

## 7. How to Run on GitHub Actions (Free Cloud Parallel Workers)

### Method A: Single-Coin Deep Split (7 Parallel Workers per Coin)
Dispatches `.github/workflows/experiment_fee_plus_2ticks.yml`:
- Worker `w01` (1m, Fee 0, Slip 1-7)
- Worker `w02` (1m, Fee 1, Slip 1-7)
- Worker `w03` (1m, Fee 2, Slip 1-7)
- Worker `w04` (5m, Fee 0, Slip 1-7)
- Worker `w05` (5m, Fee 1, Slip 1-7)
- Worker `w06` (5m, Fee 2, Slip 1-7)
- Worker `w07` (15m, 1h, 4h, 1d, all fees & slips)
- Consolidator: Merges chunk artifacts and produces `{symbol}_batch_matrix.csv` and `{symbol}_all_trades.csv`.

Trigger via CLI:
```powershell
python experiments/ob_fee_plus_2ticks_experiment/dispatch_experiment.py --symbol BTC_USDT --monitor
```

### Method B: All 10 Coins in Parallel Workers
Dispatches `.github/workflows/experiment_fee_plus_2ticks_all_coins.yml`:
- Spawns 10 independent runner containers in parallel:
  - Worker BTC_USDT
  - Worker TRUMP_USDT
  - Worker 1000000MOG_USDT
  - Worker DOGE_USDT
  - Worker ETH_USDT
  - Worker SOL_USDT
  - Worker XAU_USDT
  - Worker XAG_USDT
  - Worker CL_USDT
  - Worker XRP_USDT
- Master Consolidator merges all 10 worker packages into unified cross-coin comparisons (`master_batch_matrix.csv`, `master_batch_matrix.md`, and `master_all_trades.csv`).

Trigger via CLI:
```powershell
python experiments/ob_fee_plus_2ticks_experiment/dispatch_experiment.py --symbol ALL --monitor
```
