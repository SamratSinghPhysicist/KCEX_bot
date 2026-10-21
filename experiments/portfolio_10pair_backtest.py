#!/usr/bin/env python3
"""
10-Asset Portfolio Backtester (No-Stop-Loss, 1x Leverage, 10% Capital Sizing)
=============================================================================
Rules Enforced:
1. Long-only strategy on 10 assets: BTC, ETH, NEAR, SOL, SUI, NVDA, TSLA, AAPL, MSFT, AMZN.
2. Max 1 active trade per asset (if trade is open in NEAR, cannot open another in NEAR,
   but free to open a trade in BTC, ETH, NVDA, etc.).
3. 10% of Available Cash Capital deployed as margin per trade (compounded).
4. Synchronized across the EXACT common historical period for all 10 assets.
5. Fees applied: Maker 0.015%, Taker 0.045%, BE buffer +0.06%.
6. No stop loss: runs to target (TP1/TP2) or 1x liquidation ($0.00).
"""

import os
import sys
import glob
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.strategies import Candle, StrategySignal, run_strategy
from experiments.no_stop_loss_experiment import load_candles, simulate_single_leg

TARGET_ASSETS = ["NEAR", "BTC", "ETH", "SOL", "SUI", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN"]

@dataclass
class ActivePortfolioTrade:
    trade_id: int
    asset: str
    entry_time_ms: int
    entry_price: float
    margin: float
    tp1_price: float
    tp2_price: float
    be_price: float
    tp1_hit: bool = False
    exit_time_ms: int = 0
    exit_price: float = 0.0
    exit_reason: str = ""
    net_pnl: float = 0.0
    net_return_pct: float = 0.0
    is_win: bool = False
    mae_pct: float = 0.0
    mfe_pct: float = 0.0

def run_portfolio_backtest(
    assets: List[str] = TARGET_ASSETS,
    timeframe: str = "1h",
    strategy_name: str = "ema_cross",
    tp_rule: str = "mode_dynamic",
    initial_capital: float = 1000.0,
    sizing_pct: float = 0.10,
    fee_maker_pct: float = 0.015,
    fee_taker_pct: float = 0.045,
    be_buffer_pct: float = 0.06
):
    print("=" * 85)
    print(f"🚀 RUNNING 10-PAIR PORTFOLIO BACKTEST: {strategy_name.upper()} | {tp_rule.upper()}")
    print("=" * 85)
    
    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    stocks_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Stocks")
    
    # 1. Load candles and find EXACT common time period across all 10 assets
    candles_by_asset: Dict[str, List[Candle]] = {}
    start_times = []
    end_times = []
    
    for sym in assets:
        try:
            c = load_candles(sym, timeframe, crypto_dir, stocks_dir)
            candles_by_asset[sym] = c
            start_times.append(c[0].open_time_ms)
            end_times.append(c[-1].close_time_ms)
        except Exception as e:
            print(f"[!] Error loading {sym}: {e}")
            return
            
    common_start_ms = max(start_times)
    common_end_ms = min(end_times)
    
    t_start_dt = pd.to_datetime(common_start_ms, unit="ms", utc=True)
    t_end_dt = pd.to_datetime(common_end_ms, unit="ms", utc=True)
    span_days = (common_end_ms - common_start_ms) / (1000.0 * 86400.0)
    
    print(f"Selected Assets (10): {', '.join(assets)}")
    print(f"Common Data Period:  {t_start_dt.strftime('%Y-%m-%d %H:%M')} to {t_end_dt.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"Total Common Span:   {span_days:.1f} days ({span_days/365.25:.2f} years / {span_days/30.417:.1f} months)")
    print(f"Initial Portfolio:   ${initial_capital:,.2f} Cash | Sizing: {sizing_pct*100:.0f}% of available cash")
    print(f"Asset Constraint:    Max 1 concurrent position per asset (independent cross-asset signals)")
    
    # Trim candles to common period
    trimmed_candles: Dict[str, List[Candle]] = {}
    for sym, clist in candles_by_asset.items():
        trimmed = [c for c in clist if c.open_time_ms >= common_start_ms and c.close_time_ms <= common_end_ms]
        trimmed_candles[sym] = trimmed
        
    # 2. Run strategy and extract Long-only signals per asset
    signals_by_asset: Dict[str, List[StrategySignal]] = {}
    for sym, clist in trimmed_candles.items():
        sigs = run_strategy(strategy_name, clist, direction="long")
        # Filter signals within common window
        filtered_sigs = [s for s in sigs if s.entry_time_ms >= common_start_ms and s.entry_time_ms <= common_end_ms]
        signals_by_asset[sym] = filtered_sigs
        print(f"  - {sym:<5}: {len(clist):>6,} bars | {len(filtered_sigs):>4} Long signals")
        
    # 3. Precalculate individual trade trajectories using simulate_single_leg
    from experiments.no_stop_loss_experiment import run_baseline_trades, compute_empirical_modes
    trajectories_by_asset: Dict[str, List[Dict[str, Any]]] = {}
    
    for sym, sigs in signals_by_asset.items():
        clist = trimmed_candles[sym]
        asset_trades = []
        
        # Determine TP1 target for this asset
        if tp_rule == "fixed_0.1":
            tp1_target = 0.10
        elif tp_rule == "mode_dynamic":
            base_tr = run_baseline_trades(clist, sigs, direction_mode="long", fee_maker_pct=fee_maker_pct, fee_taker_pct=fee_taker_pct)
            m_mfe, m_mae = compute_empirical_modes(base_tr)
            tp1_target = m_mfe if m_mfe > 0.05 else 0.50
        else:
            tp1_target = 1.00
            
        print(f"  [+] {sym} TP1 Target: +{tp1_target:.2f}% | BE Buffer: +{be_buffer_pct:.2f}% | TP2: +5.00%")
        
        for s in sigs:
            s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(clist) else s.candle_idx
            entry_px = clist[s_idx].open if s_idx < len(clist) else s.entry_price
            entry_t = clist[s_idx].open_time_ms if s_idx < len(clist) else s.entry_time_ms
            
            tr = simulate_single_leg(
                direction="LONG",
                candles=clist,
                start_idx=s_idx,
                entry_px=entry_px,
                entry_time_ms=entry_t,
                notional=1000.0,
                margin_used=1000.0,
                tp1_pct=tp1_target,
                be_buffer_pct=be_buffer_pct,
                tp2_pct=5.0,
                exit_signal_idx=s.exit_signal_idx,
                resolver=None,
                symbol=sym,
                timeframe=timeframe,
                tp_rule=tp_rule,
                fee_maker_pct=fee_maker_pct,
                fee_taker_pct=fee_taker_pct,
                exit_on_signal=False
            )
            asset_trades.append({
                "signal_time_ms": s.entry_time_ms,
                "entry_time_ms": tr.entry_time_ms,
                "entry_price": tr.entry_price,
                "exit_time_ms": tr.exit_time_ms,
                "exit_price": tr.exit_price,
                "exit_reason": tr.exit_reason,
                "net_return_pct": tr.net_return_pct,
                "is_win": tr.is_win,
                "mfe_pct": tr.mfe_pct,
                "mae_pct": tr.mae_pct,
                "asset": sym
            })
        trajectories_by_asset[sym] = asset_trades

    # 4. Master Chronological Event-Driven Portfolio Simulation
    # Flatten all trade events into a chronological timeline
    all_events = []
    for sym, trades in trajectories_by_asset.items():
        for t_idx, tr in enumerate(trades):
            all_events.append({
                "time_ms": tr["entry_time_ms"],
                "type": "ENTRY",
                "asset": sym,
                "trade_idx": t_idx,
                "trade": tr
            })
            all_events.append({
                "time_ms": tr["exit_time_ms"],
                "type": "EXIT",
                "asset": sym,
                "trade_idx": t_idx,
                "trade": tr
            })
            
    # Sort events by timestamp:
    # 1. Primary: time_ms
    # 2. Secondary: trade_idx (so earlier trades finish before later ones)
    # 3. Tertiary: for the same trade_idx, ENTRY must precede EXIT
    all_events.sort(key=lambda x: (x["time_ms"], x["trade_idx"], 0 if x["type"] == "ENTRY" else 1))
    
    available_cash = initial_capital
    active_positions: Dict[str, Dict[str, Any]] = {} # asset -> dict(margin, trade)
    completed_portfolio_trades: List[Dict[str, Any]] = []
    
    equity_history = []
    asset_trade_counts = {sym: {"executed": 0, "wins": 0, "losses": 0, "net_pnl": 0.0} for sym in assets}
    skipped_same_asset_signals = 0
    
    for ev in all_events:
        t_ms = ev["time_ms"]
        sym = ev["asset"]
        tr = ev["trade"]
        
        if ev["type"] == "EXIT":
            # If this trade is currently active for this asset
            if sym in active_positions and active_positions[sym]["trade_idx"] == ev["trade_idx"]:
                pos = active_positions.pop(sym)
                margin = pos["margin"]
                ret_pct = tr["net_return_pct"]
                pnl = margin * (ret_pct / 100.0)
                available_cash += (margin + pnl)
                
                is_win = pnl > 0
                completed_portfolio_trades.append({
                    "asset": sym,
                    "entry_time_ms": tr["entry_time_ms"],
                    "exit_time_ms": t_ms,
                    "margin": margin,
                    "net_pnl": pnl,
                    "net_return_pct": ret_pct,
                    "exit_reason": tr["exit_reason"],
                    "is_win": is_win,
                    "mfe_pct": tr["mfe_pct"],
                    "mae_pct": tr["mae_pct"],
                    "cash_after": available_cash
                })
                
                asset_trade_counts[sym]["executed"] += 1
                if is_win:
                    asset_trade_counts[sym]["wins"] += 1
                else:
                    asset_trade_counts[sym]["losses"] += 1
                asset_trade_counts[sym]["net_pnl"] += pnl
                
        elif ev["type"] == "ENTRY":
            # RULE: Cannot open a new trade in that same coin/asset if already active!
            if sym in active_positions:
                skipped_same_asset_signals += 1
                continue
                
            # If available cash is sufficient, enter with 10% of available cash
            if available_cash >= 1.0:
                margin = available_cash * sizing_pct
                available_cash -= margin
                active_positions[sym] = {
                    "margin": margin,
                    "trade_idx": ev["trade_idx"],
                    "trade": tr,
                    "entry_time_ms": t_ms
                }
                
        # Record equity snapshot
        invested = sum(p["margin"] for p in active_positions.values())
        equity = available_cash + invested
        equity_history.append({
            "time_ms": t_ms,
            "dt": pd.to_datetime(t_ms, unit="ms", utc=True),
            "cash": available_cash,
            "invested": invested,
            "equity": equity,
            "active_assets": len(active_positions)
        })
        
    df_hist = pd.DataFrame(equity_history)
    df_trades = pd.DataFrame(completed_portfolio_trades)
    
    final_equity = available_cash + sum(p["margin"] for p in active_positions.values())
    total_gain_usd = final_equity - initial_capital
    total_gain_pct = (total_gain_usd / initial_capital) * 100.0
    cagr = ((final_equity / initial_capital) ** (1.0 / max(0.1, span_days / 365.25)) - 1.0) * 100.0
    
    # Portfolio Peak-to-Trough Drawdown
    df_hist["peak"] = df_hist["equity"].cummax()
    df_hist["dd_usd"] = df_hist["peak"] - df_hist["equity"]
    df_hist["dd_pct"] = (df_hist["dd_usd"] / df_hist["peak"]) * 100.0
    max_dd_pct = df_hist["dd_pct"].max()
    max_dd_usd = df_hist["dd_usd"].max()
    
    total_executed = len(df_trades)
    total_wins = (df_trades["net_pnl"] > 0).sum() if not df_trades.empty else 0
    total_losses = (df_trades["net_pnl"] < 0).sum() if not df_trades.empty else 0
    overall_win_rate = (total_wins / total_executed * 100.0) if total_executed > 0 else 0.0
    
    print("\n" + "=" * 85)
    print("🏆 10-PAIR PORTFOLIO PERFORMANCE SUMMARY (10% SIZING, LONG ONLY)")
    print("=" * 85)
    print(f"Initial Capital:         ${initial_capital:,.2f}")
    print(f"Final Portfolio Equity:  ${final_equity:,.2f} (Net PnL: +${total_gain_usd:,.2f} / +{total_gain_pct:,.2f}%)")
    print(f"Annualized Return (CAGR):{cagr:.2f}% per year")
    print(f"Max Portfolio Drawdown:  -{max_dd_pct:.2f}% (-${max_dd_usd:,.2f})")
    print(f"Total Completed Trades:  {total_executed:,} | Wins: {total_wins:,} | Losses: {total_losses} | Win Rate: {overall_win_rate:.2f}%")
    print(f"Skipped Overlapping Sigs:{skipped_same_asset_signals:,} (Same-asset lock active)")
    print(f"Avg Active Positions:    {df_hist['active_assets'].mean():.1f} of 10 max (Peak: {df_hist['active_assets'].max()} assets)")
    print(f"Avg Cash Reserve:        ${df_hist['cash'].mean():,.2f} ({(df_hist['cash'].mean()/df_hist['equity'].mean())*100:.1f}% of equity)")
    print(f"Avg Deployed Margin:     ${df_hist['invested'].mean():,.2f} ({(df_hist['invested'].mean()/df_hist['equity'].mean())*100:.1f}% of equity)")
    
    # 5. Asset-by-Asset Contribution Table
    print("\n--- ASSET-BY-ASSET CONTRIBUTION TABLE ---")
    asset_rows = []
    for sym in assets:
        st = asset_trade_counts[sym]
        wr = (st["wins"] / st["executed"] * 100.0) if st["executed"] > 0 else 0.0
        asset_rows.append({
            "Asset": sym,
            "Trades Executed": st["executed"],
            "Wins": st["wins"],
            "Losses": st["losses"],
            "Win Rate (%)": f"{wr:.1f}%",
            "Total PnL Generated": f"+${st['net_pnl']:,.2f}" if st["net_pnl"] >= 0 else f"-${abs(st['net_pnl']):,.2f}",
            "Share of Total Profit": f"{(st['net_pnl']/total_gain_usd*100):.1f}%" if total_gain_usd > 0 else "0.0%"
        })
    print(pd.DataFrame(asset_rows).to_string(index=False))

    # 6. Time Horizon Expectancies (1d, 1w, 1m, 3m, 6m, 1y)
    df_hist["day"] = df_hist["dt"].dt.floor("D")
    daily_eq = df_hist.groupby("day")["equity"].last()
    all_calendar_days = pd.date_range(start=t_start_dt.floor("D"), end=t_end_dt.floor("D"), freq="D", tz="UTC")
    daily_s = daily_eq.reindex(all_calendar_days).ffill().bfill()
    
    windows = [
        ("1 Day", 1),
        ("1 Week (7d)", 7),
        ("1 Month (30d)", 30),
        ("3 Months (90d)", 90),
        ("6 Months (180d)", 180),
        ("1 Year (365d)", 365),
    ]
    
    rolling_records = []
    for w_name, d in windows:
        diff = daily_s.diff(d).dropna()
        start = daily_s.shift(d).dropna()
        pct = (diff / start) * 100.0
        
        avg_usd = diff.mean()
        med_usd = diff.median()
        avg_pct = pct.mean()
        med_pct = pct.median()
        p10 = pct.quantile(0.10)
        p90 = pct.quantile(0.90)
        p_profit = (diff > 0).mean() * 100.0
        
        rolling_records.append({
            "Time Horizon": w_name,
            "Expected ($)": f"+${avg_usd:,.2f}",
            "Expected (%)": f"+{avg_pct:.2f}%",
            "Median ($)": f"+${med_usd:,.2f}",
            "Median (%)": f"+{med_pct:.2f}%",
            "Typical Range (10th-90th Pct)": f"+{p10:.2f}% to +{p90:.2f}%",
            "Win Prob (%)": f"{p_profit:.1f}%"
        })
        
    print("\n--- EXPECTED GAINS BY TIME HORIZON (10-Asset Portfolio, 10% Sizing) ---")
    df_roll = pd.DataFrame(rolling_records)
    print(df_roll.to_string(index=False))
    
    # Save CSV
    out_csv = os.path.join(ROOT_DIR, f"portfolio_10pair_{tp_rule}_{strategy_name}_results.csv")
    df_trades.to_csv(out_csv, index=False)
    print(f"\n[OK] Portfolio trade log saved to: {out_csv}")
    
    return final_equity, df_roll, asset_rows

if __name__ == "__main__":
    # Test Dynamic Swing (Mode Dynamic)
    run_portfolio_backtest(tp_rule="mode_dynamic", strategy_name="ema_cross")
    
    # Test Micro-Scalp (Fixed 0.1%)
    run_portfolio_backtest(tp_rule="fixed_0.1", strategy_name="ema_cross")
