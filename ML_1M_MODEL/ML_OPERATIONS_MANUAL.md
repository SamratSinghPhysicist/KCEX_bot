# Machine Learning 1-Minute Alpha Model: Operations & Training Manual

---

## 📌 Executive Summary

This document provides complete quantitative and operational documentation for the **1-Minute Multi-Horizon Machine Learning Trading Model** integrated into the KCEX algorithmic trading ecosystem.

It covers:
1. **The Critical Model Artifact** (which file must never be deleted).
2. **Multi-Task Architecture** (Directional Classifier + Dynamic Volatility Risk Regressor).
3. **Step-by-Step Retraining & Testing Protocols** (Local CLI & Cloud for current or new pairs).
4. **Order Execution Paradigms** (Limit/Maker Post-Only vs Market/Taker).
5. **Quantitative Leverage Analysis** (Why 20x–30x is the sweet spot vs 75x liquidation danger).
6. **Live Analytics & MongoDB Telemetry**.

---

## 1. 🛡️ The Critical Artifact: Where the Model Lives

### 📁 Primary File Location
The single most important file in the machine learning system is the serialized model artifact:

```
d:\My_Bots\Trading\KCEX\ML_1M_MODEL\saved_models\ml_1m_model_{symbol.lower()}.pkl
```

Specifically:
- **`ml_1m_model_trumpusdt.pkl`** (~2.56 MB): Trained model for TRUMPUSDT.
- **`ml_1m_model_dogeusdt.pkl`** (~1.33 MB): Trained model for DOGEUSDT.

### ⚠️ Critical Rules:
> **NEVER DELETE OR RENAME THESE `.pkl` FILES** unless you intend to retrain.
> - The live engine (`run_engine.py`), the semi-autonomous trader (`semi_auto_trader.py`), and the backtester (`BACKTESTER/engine/execution_sim.py`) **load this exact binary artifact into memory at startup**.
> - If this file is deleted or corrupt, the system will raise `FileNotFoundError` or fall back to baseline heuristic strategies.
> - **Always keep a backup** copy of working `.pkl` files in a safe directory (e.g., `ML_1M_MODEL/saved_models/backups/`).

### What is Inside the `.pkl` Artifact?
The file is serialized via standard Python `pickle` and contains an instance of `TradingModel`:
1. **`HistGradientBoostingClassifier`**: 3-class directional predictor (`BUY=1`, `SELL=-1`, `WAIT/HOLD=0`).
2. **`HistGradientBoostingRegressor (TP)`**: Predicts optimal favorable excursion tick distance.
3. **`HistGradientBoostingRegressor (SL)`**: Predicts adverse excursion risk tick distance calibrated to ATR.
4. **`feature_cols`**: Exact ordered list of 40+ microstructural and technical feature names used during training.
5. **`cfg`**: Embedded configuration hyperparameters (learning rate, min samples, max leaf nodes).

---

## 2. 🧠 Model Architecture & Feature Engineering

The model uses pure scikit-learn algorithms (HistGradientBoostingClassifier and HistGradientBoostingRegressor). This ensures **100% environment parity** between local Windows execution and Linux GitHub Actions runners with zero external native build dependencies.

### Feature Pipeline (40+ Alpha Signals):
1. **Momentum & Trend**:
   - Multi-horizon log returns: 1-min, 3-min, 5-min, 15-min, 30-min.
   - Moving average ratios: Price vs EMA8, EMA21, EMA55, EMA200.
   - Exponential Moving Average slopes and ribbon spreads.
2. **Mean-Reversion & Volatility**:
   - RSI(14) and Stochastic RSI (%K, %D).
   - ATR(14) volatility normalized against baseline rolling 100-bar ATR.
   - Bollinger Band %B and bandwidth compression.
3. **Microstructure & Order-Flow Aggression**:
   - Cumulative Volume Delta (CVD) slope over 5-min and 15-min windows.
   - Taker buy volume ratio (aggressive buyer vs seller market order flow).
   - Order-flow volume imbalance ratio.
4. **Dynamic Risk Calibration**:
   - The model dynamically adjusts Take-Profit (TP ticks) and Stop-Loss (SL ticks) based on real-time market volatility (ATR_14), ensuring wider targets during volatile expansions and tighter targets during calm consolidation.

---

## 3. 🔄 How to Retrain, Test & Deploy New Models

### Scenario A: Retraining Existing Pairs (e.g. TRUMP or DOGE) with Newer Data

When you have downloaded new historical 1-minute OHLCV or tick trade data into BACKTESTER/OHLCV_Data_Binance/ and BACKTESTER/Historical_Trades_Data_Binance/:

#### Run Local Training & Evaluation Pipeline:
Open PowerShell / Command Prompt in d:\My_Bots\Trading\KCEX\:

`powershell
python -m ML_1M_MODEL.run_pipeline 
  --symbol TRUMPUSDT 
  --train-start 2026-01-01 
  --train-end 2026-07-31 
  --oos-start 2026-08-01 
  --oos-end 2026-08-31 
  --eval-ticks 
  --min-confidence 0.38
`

#### What Happens Automatically:
1. Loads historical 1m OHLCV and millisecond trades.
2. Generates labels using the **Triple-Barrier Method** (target hit vs stop hit vs horizontal barrier timeout).
3. Trains the classifier and dynamic TP/SL regressors.
4. Saves the updated model to ML_1M_MODEL/saved_models/ml_1m_model_trumpusdt.pkl.
5. Executes an independent Out-Of-Sample (OOS) backtest simulation on August 2026.
6. Writes comprehensive markdown reports and metrics to ML_1M_MODEL/reports/trumpusdt_oos_report.md.

---

### Scenario B: Training a Completely New Pair (e.g. BTCUSDT, ETHUSDT, SOLUSDT, PEPEUSDT)

To train an ML model on a new trading pair, follow these 4 steps:

#### Step 1: Register Tick Specification in ML_1M_MODEL/config.py
Open ML_1M_MODEL/config.py and locate TICK_SPECS. Add the new symbol with its KCEX tick size (price unit):

`python
TICK_SPECS: Dict[str, Dict[str, Any]] = {
    TRUMPUSDT: {tick_size: 0.001, price_precision: 3, min_qty: 1.0},
    DOGEUSDT:  {tick_size: 0.00001, price_precision: 5, min_qty: 1.0},
    BTCUSDT:   {tick_size: 0.1, price_precision: 1, min_qty: 0.001},
    SOLUSDT:   {tick_size: 0.01, price_precision: 2, min_qty: 0.01},
}
`

#### Step 2: Download Historical Data
Use the backtester downloader to pull 1m OHLCV data:
`powershell
python BACKTESTER/engine/downloader.py --symbol SOL_USDT --timeframe 1m --start 2026-01-01 --end 2026-08-31 --ticks
`

#### Step 3: Run the ML Pipeline for the New Symbol
`powershell
python -m ML_1M_MODEL.run_pipeline 
  --symbol SOLUSDT 
  --train-start 2026-01-01 
  --train-end 2026-07-31 
  --oos-start 2026-08-01 
  --oos-end 2026-08-31 
  --eval-ticks
`
This produces ML_1M_MODEL/saved_models/ml_1m_model_solusdt.pkl.

#### Step 4: Add Preset to settings.py
Add the new preset under STRATEGY_PRESETS in settings.py:
`python
SOL_ML_MOMENTUM: {
    name: SOL 1M Machine Learning Alpha Scalper,
    symbol: SOL_USDT,
    strategy_mode: ML_1M_MODEL,
    leverage: 25,
    volume_multiplier: 1.0,
    order_type: LIMIT,
    cancel_if_unfilled: False,
}
`

---

## 4. ⚡ Order Execution: Limit / Maker vs Market / Taker

The system fully supports both execution styles across all entry points:

| Mode | Order Type | Fee Schedule | Slippage | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **LIMIT (Maker)** | Post-Only Limit at id1 (Long) / sk1 (Short) | **0.00%** (Zero maker fee on KCEX) | **0 ticks** (Fills at exact limit price) | Best for maximum profit retention. |
| **MARKET (Taker)** | Immediate Market Order | Taker fee | May experience 1-tick spread friction | Best for urgent signal capture. |

### Resting Limit Order Behavior (cancel_if_unfilled = False)
Per design preference, **unfilled limit orders are NOT cancelled automatically by default**.
- When --order-type LIMIT is selected, the order is placed at top-of-book.
- If not filled immediately, the order rests in the exchange orderbook until matching liquidity crosses it.
- To cancel on timeout, pass --cancel-unfilled explicitly on the CLI.

### Where to Switch Maker vs Taker:
1. **Live Engine CLI**:
   `powershell
   python run_engine.py --strategy ML_1M --order-type LIMIT
   python run_engine.py --strategy ML_1M --order-type MARKET
   `
2. **Semi-Autonomous Trader (semi_auto_trader.py)**:
   - Menu Option [5] Order Execution Style: Select 1 for MARKET or 2 for LIMIT.
3. **GitHub Actions Workflows**:
   - In both live_trading.yml and acktest.yml, choose execution_style: MAKER_HYBRID or PURE_MARKET.

---

## 5. ⚖️ Quantitative Leverage Analysis: 20x–30x Sweet Spot vs 75x Hazard

> **DO NOT RUN THE 1-MINUTE ML MODEL AT 75X LEVERAGE.**  
> Quantitative proof below explains why 20x to 30x is the mathematical optimal range.

### Mathematical Proof:
Let $ be the entry price, $ be leverage, and $\text{MMR} = 1.0\%$ (KCEX Maintenance Margin Ratio).

\text{Liquidation Buffer Pct} = \frac{1}{L} - \text{MMR}

\text{Buffer Ticks} = \frac{P_0 \times \text{Buffer Pct}}{\text{Price Unit (pu)}}

#### Comparison Table on TRUMPUSDT ( = 2.434\text{ USDT}$,  = 0.001\text{ USDT}$):

| Leverage ($) | Liquidation Buffer % | Distance to Liquidation | Model 1.0x ATR Stop Loss | Vulnerability Verdict |
| :---: | :---: | :---: | :---: | :--- |
| **75x** | /75 - 0.01 = \mathbf{0.33\%}$ | **~8.1 ticks** | **~6 to 10 ticks** | 🚨 **EXTREME RISK**: A normal 1-minute random fluctuation or bid-ask bounce triggers exchange liquidation *before* the Stop Loss can execute! |
| **50x** | /50 - 0.01 = \mathbf{1.00\%}$ | **~24.3 ticks** | **~6 to 10 ticks** | ⚠️ **BORDERLINE**: Vulnerable to minor volatility spikes. |
| **30x** | /30 - 0.01 = \mathbf{2.33\%}$ | **~56.8 ticks** | **~6 to 10 ticks** | ✅ **OPTIMAL SWEET SPOT**: Stop Loss has a **6x safety buffer** above liquidation. |
| **20x** | /20 - 0.01 = \mathbf{4.00\%}$ | **~97.4 ticks** | **~6 to 10 ticks** | 🛡️ **MAXIMUM SAFETY**: High margin efficiency with zero liquidation hazard. |

### Conclusion:
- Set leverage to **20x to 30x**.
- This allows the machine learning model's dynamic ATR Stop Loss (3 to 8 ticks) to breathe naturally and cut losses precisely, without risking exchange liquidation collars.

---

## 6. 📊 Real-Time Analytics & MongoDB Telemetry

Every trade executed by the ML strategy logs enriched telemetry directly to MongoDB Atlas:
- ml_confidence: Classifier conviction probability (e.g. .482 = 48.2\%$).
- ml_prob_buy: Softmax probability for BUY action.
- ml_prob_sell: Softmax probability for SELL action.
- ml_prob_wait: Softmax probability for WAIT/HOLD action.
- ml_tp_ticks: Dynamic Take-Profit distance generated by the volatility regressor.
- ml_sl_ticks: Dynamic Stop-Loss distance generated by the volatility regressor.
- ml_atr_14: Real-time ATR(14) volatility at time of order entry.

### Viewing ML Telemetry:
Launch the interactive dashboard:
`powershell
python run_live_analytics.py
`
- Press **[M]** to enter the **Machine Learning Model Telemetry View**:
  - Displays ML Win Rate, Profit Factor, and Net PnL.
  - Compares average conviction on winning trades vs losing trades.
  - Displays average dynamic TP and SL tick distances.
  - Lists the 10 most recent ML predictions with full confidence breakdowns.
- Press **[F]** to filter all analytics views strictly to ML_1M_MODEL.
- Press **[8]** to export all 32 telemetry fields to CSV.
