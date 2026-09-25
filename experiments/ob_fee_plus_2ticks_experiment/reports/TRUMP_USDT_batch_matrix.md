# Order Block + Demand Strategy Experiment: Fee Coverage + 2 Ticks TP
**Asset:** `TRUMP_USDT`  
**Worker / Tag:** `CONSOLIDATED_MASTER`  
**Execution Mode:** Pure OHLCV (1m Sub-Candle Disambiguation)  
**Date Generated:** 2026-09-25 05:36:27 UTC  

## 1. Experiment Overview & Rationale
- **Base Strategy:** Order Block + Demand Zone (Vivek Yadav Smart Money Concepts).
- **Stop Loss:** Preserved at exact Order Block boundary (+/- buffer ticks).
- **Take Profit:** Dynamic rapid scalp target set at `Fee Coverage Ticks + 2 Ticks`.
- **Partial TP:** Disabled (100% position exits at the fee+2tick target).
- **Disambiguation Rule:** If candle hits both TP and SL, 1m sub-candles verify precedence. If still on same 1m candle, declares Stop Loss Hit.

## 2. Top Performing Configurations (by Net ROI %)

| Rank | Timeframe | Fee Schedule | Slippage | Win Rate | Profit Factor | Net PnL (USDT) | Net ROI % | Max DD % | Trades |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **15m** | Maker 0.00% / Taker 0.01% | 1t | 86.2% | 0.57 | $-3.46 | **-3.46%** | 4.12% | 109 |
| 2 | **1m** | Maker 0.00% / Taker 0.01% | 1t | 63.3% | 0.40 | $-53.46 | **-53.46%** | 53.51% | 1653 |

## 3. Comprehensive Parameter Sweep Matrix

| Timeframe | Fee Schedule | Slip | Trades | Win Rate | PF | Net PnL | Net ROI % | Max DD % | Exp (USDT) | Total Fees | Final Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1m | Maker 0.00% / Taker 0.01% | 1t | 1653 | 63.3% | 0.40 | $-53.46 | -53.46% | 53.51% | $-0.0323 | $22.89 | $46.54 |
| 15m | Maker 0.00% / Taker 0.01% | 1t | 109 | 86.2% | 0.57 | $-3.46 | -3.46% | 4.12% | $-0.0318 | $2.14 | $96.54 |