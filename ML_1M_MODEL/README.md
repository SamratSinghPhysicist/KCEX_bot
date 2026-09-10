# 🧠 ML_1M_MODEL: Deep 1-Minute Crypto Futures Alpha Engine

A production-grade Machine Learning trading system engineered for **1-minute high-frequency crypto futures trading** (e.g. `TRUMPUSDT`, `DOGEUSDT`, `BTCUSDT`). 

The model synergizes **1-minute OHLCV price action** with **tick-by-tick order-flow microstructure** (aggressor volume delta, CVD, trade count imbalances, whale participation, and VWAP deviation) to generate high-conviction **BUY**, **SELL**, and **WAIT / HOLD** signals with **dynamic Take-Profit (TP)** and **Stop-Loss (SL)** recommendations.

---

## 🏛️ System Architecture

```
ML_1M_MODEL/
├── config.py               # Data paths, symbol tick specs, hyperparams, fees
├── requirements.txt        # LightGBM, Scikit-Learn, Pandas, NumPy, PyArrow
├── data_loader.py          # Unified loader: reads local D:\ drive or downloads from Binance Vision
├── orderflow_aggregator.py # Streaming chunked tick parser (aggregates 2-6GB files into 1m order flow)
├── features.py             # Deep technical, volatility, candle anatomy & order-flow features
├── labeler.py              # Triple Barrier Method & Continuous Excursion Targets (MFE/MAE)
├── model.py                # Multi-task LightGBM Classifier + Dynamic TP/SL Regressors
├── trainer.py              # Purged Walk-Forward cross-validation & training engine
├── evaluator.py            # Out-of-Sample backtester: Sharpe, Profit Factor, Win Rate, Drawdown
├── predict.py              # Real-time CLI & inference engine for live bots
├── run_pipeline.py         # Master CLI runner orchestrating the full end-to-end pipeline
└── test_pipeline.py        # Automated test suite
```

---

## 🔍 Deep 1-Minute Microstructure & Technical Features

### 1. Order-Flow & Microstructure (Tick Trades)
- **Taker Aggression Ratio**: $\frac{V_{\text{buy}}}{V_{\text{total}}}$ (aggressive market buy pressure vs market sell pressure).
- **Cumulative Volume Delta (CVD)** & 1m Delta: Acceleration and absorption detection.
- **Order Flow Imbalance (OFI)**: $\frac{V_{\text{buy}} - V_{\text{sell}}}{V_{\text{buy}} + V_{\text{sell}}}$.
- **Trade Arrival Frequency & Imbalance**: Ratio of buyer-initiated trades vs seller-initiated trades.
- **Whale Trade Dominance**: Volume percentage of institutional trades $\ge \$5,000$.
- **1-Minute VWAP Deviation**: $\frac{\text{Close} - \text{VWAP}}{\text{VWAP}}$.

### 2. Price Action & Volatility (1m OHLCV)
- **Multi-Horizon Log Returns**: 1m, 2m, 3m, 5m, 10m, 15m, 30m, 60m.
- **Candlestick Anatomy**: Upper shadow ratio, lower shadow ratio, body proportion, candle polarity.
- **Volatility Estimators**: Parkinson Volatility (High-Low), Garman-Klass, normalized ATR(5, 14, 30), Bollinger Band %B & Bandwidth.
- **Momentum & Trend**: RSI(7, 14), Stochastic RSI (%K, %D), normalized MACD histogram, EMA(9, 21, 50, 200) spreads.
- **Cyclical Time**: Sine & cosine encodings for minute of hour and hour of day.

---

## 🛡️ Triple Barrier Labeling & Dynamic Risk Management

Trades are labeled using the **Triple Barrier Method**:
- **Upper Barrier (Dynamic TP)**: Entry $+ k_{tp} \times \text{ATR}_{14}$ (forecasted via forward Maximum Favorable Excursion).
- **Lower Barrier (Dynamic SL)**: Entry $- k_{sl} \times \text{ATR}_{14}$ (forecasted via forward Maximum Adverse Excursion).
- **Time Barrier**: $H$ bars forward (e.g. 10 1-minute bars).

### Actions Output
1. **`BUY`**: Model forecasts high probability of hitting the upper TP barrier first with positive expectancy.
2. **`SELL`**: Model forecasts high probability of hitting the lower SL barrier first.
3. **`WAIT / HOLD`**: Market is in low-conviction chop, high entropy, or consolidation. Protects capital by staying flat.

---

## ☁️ Zero-Laptop-Compute: Cloud Execution via GitHub Actions

To protect your laptop's CPU and memory, all heavy data ingestion, order-flow chunk streaming, LightGBM training, and out-of-sample backtesting run automatically in GitHub's cloud runners.

### How to trigger in GitHub Actions:
1. Go to your repository on GitHub: `https://github.com/SamratSinghPhysicist/KCEX_bot`
2. Click on the **Actions** tab.
3. Select **"Train & Test 1M ML Trading Model"** workflow on the left sidebar.
4. Click **"Run workflow"** and choose your parameters:
   - **Symbol**: `TRUMPUSDT`, `DOGEUSDT`, or `BTCUSDT`
   - **Start Date**: `2026-01-01` (or any range)
   - **End Date**: `2026-08-31`
   - **Horizon Bars**: `10` (10 minutes)
   - **TP Multiplier**: `2.0`
   - **SL Multiplier**: `1.2`
   - **Confidence Threshold**: `0.55`
5. Click **"Run workflow"**.
6. When complete, GitHub Actions will:
   - Post an interactive **Step Summary** markdown table with Win Rate, Profit Factor, Sharpe Ratio, Max Drawdown, and Sample Trade Signals.
   - Attach a downloadable **Artifacts Zip** containing the trained model binaries (`.pkl`) and trade logs (`.csv`).

---

## 💻 Local Usage & Inference

### 1. Run Pipeline Locally (Uses D:\ Data Drive)
```bash
python -m ML_1M_MODEL.run_pipeline --symbol TRUMPUSDT --start 2026-06-01 --end 2026-08-31 --horizon 10
```

### 2. Generate Real-Time Inference Signals
```bash
python -m ML_1M_MODEL.predict --symbol TRUMPUSDT
```

**Sample Output**:
```json
{
  "symbol": "TRUMPUSDT",
  "timestamp": 1785542880000,
  "datetime": "2026-08-31 23:59:00",
  "current_price": 9.452,
  "action": "BUY",
  "confidence": 0.684,
  "probabilities": {
    "BUY": 0.684,
    "SELL": 0.125,
    "WAIT_HOLD": 0.191
  },
  "dynamic_risk_management": {
    "suggested_tp_price": 9.538,
    "suggested_sl_price": 9.402,
    "tp_ticks_pu": 86,
    "sl_ticks_pu": 50,
    "tp_distance_pct": 0.91,
    "sl_distance_pct": 0.53,
    "risk_reward_ratio": 1.72,
    "tick_size": 0.001
  },
  "market_microstructure": {
    "taker_buy_ratio": 0.612,
    "order_flow_imbalance": 0.224,
    "cvd_pressure": "STRONG_BUY_AGGRESSION",
    "volatility_regime": "NEUTRAL_TRENDING",
    "atr_14": 0.043
  }
}
```

### 3. Integrating into Bot
```python
from ML_1M_MODEL.predict import Predictor

predictor = Predictor(symbol="TRUMPUSDT")
# Feed recent DataFrame with 1m candles
recommendation = predictor.predict_from_dataframe(recent_1m_df)

if recommendation["action"] == "BUY" and recommendation["confidence"] >= 0.60:
    tp_price = recommendation["dynamic_risk_management"]["suggested_tp_price"]
    sl_price = recommendation["dynamic_risk_management"]["suggested_sl_price"]
    # Execute order with dynamic TP/SL
```
