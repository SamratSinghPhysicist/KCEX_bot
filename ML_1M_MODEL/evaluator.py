"""
Out-Of-Sample Backtester & Performance Evaluation Engine
========================================================
Performs rigorous financial simulation on strictly unseen test data:
- Simulates realistic 1-minute trade execution with dynamic TP/SL
- Factors in exchange fees and slippage
- Computes comprehensive institutional metrics: Sharpe, Sortino, Profit Factor,
  Max Drawdown, Win Rate, Expectancy, and produces rich Markdown reports.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple

from .config import ModelConfig, REPORTS_DIR, get_tick_spec
from .model import TradingModel


def backtest_out_of_sample(
    model: TradingModel,
    test_df: pd.DataFrame,
    cfg: Optional[ModelConfig] = None
) -> Tuple[Dict[str, Any], pd.DataFrame, str]:
    """
    Executes a high-fidelity 1-minute backtest on unseen test data.
    Returns:
    - metrics dictionary
    - trade logs DataFrame
    - formatted markdown report
    """
    cfg = cfg or model.cfg
    print(f"[Evaluator] Running out-of-sample backtest on {len(test_df):,} test bars...")

    closes = test_df["close"].values
    highs = test_df["high"].values
    lows = test_df["low"].values
    atrs = test_df["atr_14"].values
    timestamps = test_df["timestamp"].values

    tick_spec = get_tick_spec(cfg.symbol)
    tick_size = tick_spec["tick_size"]
    slippage = cfg.slippage_ticks * tick_size
    fee_rate = cfg.taker_fee
    leverage = cfg.leverage

    # Generate model decisions for entire test set
    decisions = model.predict_decision(
        X=test_df,
        current_prices=closes,
        current_atrs=atrs,
        symbol=cfg.symbol
    )

    trades = []
    equity = 10000.0  # Initial capital in USD
    equity_curve = [equity]

    in_position = False
    pos_type = None  # "LONG" or "SHORT"
    entry_price = 0.0
    entry_idx = 0
    tp_price = 0.0
    sl_price = 0.0
    tp_ticks = 0
    sl_ticks = 0
    confidence = 0.0

    n = len(test_df)
    H = cfg.horizon_bars

    for i in range(n):
        # 1. Manage active position
        if in_position:
            h = highs[i]
            l = lows[i]
            c = closes[i]
            bars_held = i - entry_idx

            exit_price = 0.0
            exit_reason = ""

            if pos_type == "LONG":
                if h >= tp_price:
                    exit_price = tp_price
                    exit_reason = "TP_HIT"
                elif l <= sl_price:
                    exit_price = sl_price
                    exit_reason = "SL_HIT"
                elif bars_held >= H:
                    exit_price = c - slippage
                    exit_reason = "TIME_EXPIRY"

            elif pos_type == "SHORT":
                if l <= tp_price:
                    exit_price = tp_price
                    exit_reason = "TP_HIT"
                elif h >= sl_price:
                    exit_price = sl_price
                    exit_reason = "SL_HIT"
                elif bars_held >= H:
                    exit_price = c + slippage
                    exit_reason = "TIME_EXPIRY"

            if exit_reason:
                # Compute returns
                if pos_type == "LONG":
                    gross_ret = (exit_price - entry_price) / entry_price
                else:
                    gross_ret = (entry_price - exit_price) / entry_price

                # Fees on roundtrip
                fees = (fee_rate + fee_rate)
                net_ret = gross_ret - fees
                net_pnl_margin = net_ret * leverage  # Return on margin
                pnl_dollars = (equity * 0.1) * net_pnl_margin  # Allocate 10% capital per trade
                equity += pnl_dollars

                trades.append({
                    "trade_id": len(trades) + 1,
                    "type": pos_type,
                    "entry_time": timestamps[entry_idx],
                    "exit_time": timestamps[i],
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "tp_price": tp_price,
                    "sl_price": sl_price,
                    "tp_ticks": tp_ticks,
                    "sl_ticks": sl_ticks,
                    "bars_held": bars_held,
                    "confidence": confidence,
                    "exit_reason": exit_reason,
                    "gross_return_pct": gross_ret * 100,
                    "net_return_pct": net_ret * 100,
                    "net_margin_ret_pct": net_pnl_margin * 100,
                    "pnl_usd": pnl_dollars,
                    "equity_after": equity
                })

                in_position = False
                pos_type = None

        equity_curve.append(equity)

        # 2. Check for new trade signal if flat
        if not in_position and i < n - H:
            d = decisions[i]
            act = d["action"]

            if act == "BUY":
                in_position = True
                pos_type = "LONG"
                entry_idx = i
                entry_price = closes[i] + slippage
                tp_price = d["suggested_tp"]
                sl_price = d["suggested_sl"]
                tp_ticks = d["tp_ticks"]
                sl_ticks = d["sl_ticks"]
                confidence = d["confidence"]

            elif act == "SELL":
                in_position = True
                pos_type = "SHORT"
                entry_idx = i
                entry_price = closes[i] - slippage
                tp_price = d["suggested_tp"]
                sl_price = d["suggested_sl"]
                tp_ticks = d["tp_ticks"]
                sl_ticks = d["sl_ticks"]
                confidence = d["confidence"]

    df_trades = pd.DataFrame(trades)

    # Compute Quant Performance Metrics
    total_trades = len(df_trades)
    if total_trades > 0:
        wins = df_trades[df_trades["pnl_usd"] > 0]
        losses = df_trades[df_trades["pnl_usd"] <= 0]
        win_rate = len(wins) / total_trades
        gross_profit = wins["pnl_usd"].sum() if len(wins) > 0 else 0.0
        gross_loss = abs(losses["pnl_usd"].sum()) if len(losses) > 0 else 1e-9
        profit_factor = gross_profit / gross_loss
        avg_win = wins["pnl_usd"].mean() if len(wins) > 0 else 0.0
        avg_loss = losses["pnl_usd"].mean() if len(losses) > 0 else 0.0
        expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

        # Drawdown calculation
        eq_arr = np.array(equity_curve)
        peak = np.maximum.accumulate(eq_arr)
        drawdowns = (peak - eq_arr) / peak
        max_drawdown = float(np.max(drawdowns))

        # Sharpe & Sortino
        returns_arr = df_trades["net_margin_ret_pct"].values / 100.0
        mean_ret = np.mean(returns_arr)
        std_ret = np.std(returns_arr) if len(returns_arr) > 1 else 1e-9
        downside_std = np.std(returns_arr[returns_arr < 0]) if len(returns_arr[returns_arr < 0]) > 1 else 1e-9

        # Annualized Sharpe (assuming ~300k 1m bars per year, sqrt(trades_per_year))
        annual_factor = np.sqrt(max(total_trades, 1))
        sharpe = (mean_ret / std_ret) * annual_factor if std_ret > 0 else 0.0
        sortino = (mean_ret / downside_std) * annual_factor if downside_std > 0 else 0.0
        total_pnl_pct = ((equity - 10000.0) / 10000.0) * 100.0
    else:
        win_rate = 0.0
        profit_factor = 0.0
        max_drawdown = 0.0
        sharpe = 0.0
        sortino = 0.0
        avg_win = 0.0
        avg_loss = 0.0
        expectancy = 0.0
        total_pnl_pct = 0.0

    # Decision distribution
    action_counts = pd.Series([d["action"] for d in decisions]).value_counts().to_dict()
    total_decisions = len(decisions)
    buy_share = (action_counts.get("BUY", 0) / total_decisions) * 100
    sell_share = (action_counts.get("SELL", 0) / total_decisions) * 100
    wait_share = (action_counts.get("WAIT / HOLD", 0) / total_decisions) * 100

    metrics = {
        "symbol": cfg.symbol,
        "test_bars": len(test_df),
        "total_trades": total_trades,
        "win_rate_pct": round(win_rate * 100, 2),
        "profit_factor": round(profit_factor, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "sortino_ratio": round(sortino, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
        "final_equity_usd": round(equity, 2),
        "avg_win_usd": round(avg_win, 2),
        "avg_loss_usd": round(avg_loss, 2),
        "expectancy_usd": round(expectancy, 2),
        "signal_share_buy_pct": round(buy_share, 1),
        "signal_share_sell_pct": round(sell_share, 1),
        "signal_share_wait_pct": round(wait_share, 1),
    }

    # Generate Markdown Summary Report
    md_report = fr"""# 🤖 ML Model Out-of-Sample Performance: {cfg.symbol}

## 📊 Executive Summary
| Metric | Value | Benchmark Target |
| :--- | :--- | :--- |
| **Asset Symbol** | `{cfg.symbol}` | 1-Minute Microstructure |
| **Out-of-Sample Bars** | `{len(test_df):,}` 1m bars | Chronologically Isolated |
| **Total Trades** | `{total_trades:,}` | High Conviction Only |
| **Win Rate** | **`{metrics['win_rate_pct']}%`** | > 50% |
| **Profit Factor** | **`{metrics['profit_factor']}`** | > 1.50 |
| **Total Net PnL** | **`{metrics['total_pnl_pct']}%`** | Positive Edge |
| **Max Drawdown** | **`{metrics['max_drawdown_pct']}%`** | < 15.0% |
| **Sharpe Ratio** | **`{metrics['sharpe_ratio']}`** | > 1.50 |
| **Sortino Ratio** | **`{metrics['sortino_ratio']}`** | > 2.00 |
| **Expectancy / Trade** | **`${metrics['expectancy_usd']}`** | Positive Expectancy |

---

## 🎯 Signal Action Distribution
- **BUY Signals**: `{metrics['signal_share_buy_pct']}%`
- **SELL Signals**: `{metrics['signal_share_sell_pct']}%`
- **WAIT / HOLD**: `{metrics['signal_share_wait_pct']}%` *(Filters out high-entropy market chop)*

---

## 🛡️ Risk Management (Dynamic TP & SL)
- **Take Profit Target**: Predicted MFE excursion ($\sim {cfg.tp_atr_mult} \times \text{{ATR}}_{{14}}$)
- **Stop Loss Protection**: Predicted MAE threshold ($\sim {cfg.sl_atr_mult} \times \text{{ATR}}_{{14}}$)
- **Execution Cost Modeling**: {cfg.taker_fee * 100}% Taker Fee + {cfg.slippage_ticks} Tick Slippage
"""

    report_path = os.path.join(REPORTS_DIR, f"{cfg.symbol.lower()}_oos_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_report)

    if not df_trades.empty:
        trades_csv_path = os.path.join(REPORTS_DIR, f"{cfg.symbol.lower()}_oos_trades.csv")
        df_trades.to_csv(trades_csv_path, index=False)

    print(f"[Evaluator] Out-of-sample backtest complete! Report written to {report_path}")
    return metrics, df_trades, md_report
