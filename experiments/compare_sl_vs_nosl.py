#!/usr/bin/env python3
"""
Head-to-Head Comparative Engine:
No-Stop-Loss System vs. Intended Strategy with Stop Loss & Take Profit
====================================================================
Compares:
1. NO_STOP_LOSS (Runs to Target or 1x Liquidation)
2. INTENDED_ATR_SL (Intended Stop-Loss = 1.5 * ATR14, Intended TP = 2.0 * ATR14)
3. INTENDED_SIGNAL_SL (Exits on opposing indicator reversal signal)
4. DYNAMIC_MODE_SL (Stop-Loss set to mode of adverse moves, TP set to mode MFE)

Tests both:
- Individual key assets (ETH, NEAR, BTC, NVDA)
- Full 10-Asset Portfolio with 10% cash sizing & 1-trade-per-asset lock
"""

import os
import sys
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.strategies import Candle, StrategySignal, run_strategy, compute_atr
from experiments.no_stop_loss_experiment import load_candles, run_baseline_trades, compute_empirical_modes

TARGET_ASSETS = ["NEAR", "BTC", "ETH", "SOL", "SUI", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN"]

@dataclass
class TradeOutcome:
    trade_id: int
    asset: str
    entry_time_ms: int
    entry_price: float
    exit_time_ms: int
    exit_price: float
    exit_reason: str # "TP", "STOP_LOSS", "SIGNAL_EXIT", "END_OF_DATA", "LIQUIDATION"
    notional: float
    margin: float
    gross_pnl: float
    entry_fee: float
    exit_fee: float
    net_pnl: float
    net_return_pct: float
    is_win: bool
    mfe_pct: float
    mae_pct: float

def simulate_trade_with_rules(
    candles: List[Candle],
    sig: StrategySignal,
    mode: str, # "NO_SL", "INTENDED_ATR", "INTENDED_SIGNAL", "DYNAMIC_MODE"
    asset: str,
    fee_maker_pct: float = 0.015,
    fee_taker_pct: float = 0.045,
    be_buffer_pct: float = 0.06,
    dynamic_mfe_pct: float = 5.0,
    dynamic_mae_pct: float = 2.5,
    notional: float = 1000.0,
    atr_val: float = 0.0
) -> TradeOutcome:
    n = len(candles)
    entry_px = sig.entry_price
    start_idx = sig.candle_idx + 1 if sig.candle_idx + 1 < n else sig.candle_idx
    entry_t = candles[start_idx].open_time_ms if start_idx < n else sig.entry_time_ms
    entry_px = candles[start_idx].open if start_idx < n else entry_px
    entry_fee = notional * (fee_maker_pct / 100.0)

    # Determine TP and SL levels based on mode
    if mode == "NO_SL":
        # Dynamic Mode TP, No explicit SL (liquidation at 0.0)
        tp1_px = entry_px * (1.0 + dynamic_mfe_pct / 100.0)
        tp2_px = entry_px * 1.05
        be_px = entry_px * (1.0 + be_buffer_pct / 100.0)
        sl_px = 0.0
        exit_on_opposing = False
    elif mode == "INTENDED_ATR":
        # Intended strategy SL: 1.5 * ATR, TP: 2.0 * ATR
        eff_atr = atr_val if atr_val > 0 else (entry_px * 0.015)
        tp1_px = entry_px + 2.0 * eff_atr
        tp2_px = tp1_px
        be_px = tp1_px
        sl_px = entry_px - 1.5 * eff_atr
        exit_on_opposing = False
    elif mode == "INTENDED_SIGNAL":
        # Intended signal exit: TP at 2.0 * ATR or exit on opposing signal
        eff_atr = atr_val if atr_val > 0 else (entry_px * 0.015)
        tp1_px = entry_px + 2.0 * eff_atr
        tp2_px = tp1_px
        be_px = tp1_px
        sl_px = 0.0
        exit_on_opposing = True
    elif mode == "DYNAMIC_MODE":
        # Dynamic Mode TP and Dynamic Mode SL
        tp1_px = entry_px * (1.0 + dynamic_mfe_pct / 100.0)
        tp2_px = tp1_px
        be_px = tp1_px
        sl_px = entry_px * (1.0 - dynamic_mae_pct / 100.0)
        exit_on_opposing = False
    else:
        raise ValueError(f"Unknown mode: {mode}")

    mfe = 0.0
    mae = 0.0
    tp1_hit = False

    end_idx = sig.exit_signal_idx if (exit_on_opposing and sig.exit_signal_idx is not None and sig.exit_signal_idx < n) else (n - 1)

    for i in range(start_idx, end_idx + 1):
        c = candles[i]
        c_mfe = (c.high - entry_px) / entry_px * 100.0
        c_mae = (entry_px - c.low) / entry_px * 100.0
        mfe = max(mfe, c_mfe)
        mae = max(mae, c_mae)

        # 1. Check Stop Loss / Liquidation
        if sl_px > 0 and c.low <= sl_px:
            exit_px = sl_px
            gross = notional * ((exit_px - entry_px) / entry_px)
            exit_fee = notional * (fee_taker_pct / 100.0)
            net_pnl = gross - entry_fee - exit_fee
            return TradeOutcome(
                trade_id=0, asset=asset, entry_time_ms=entry_t, entry_price=entry_px,
                exit_time_ms=c.open_time_ms, exit_price=exit_px, exit_reason="STOP_LOSS",
                notional=notional, margin=notional, gross_pnl=gross, entry_fee=entry_fee,
                exit_fee=exit_fee, net_pnl=net_pnl, net_return_pct=(net_pnl / notional * 100.0),
                is_win=False, mfe_pct=mfe, mae_pct=mae
            )

        # 2. Check TP
        if not tp1_hit and c.high >= tp1_px:
            if mode == "NO_SL":
                # 50% closed at TP1, runner to BE or TP2
                tp1_hit = True
                continue
            else:
                # 100% closed at Intended TP
                exit_px = tp1_px
                gross = notional * ((exit_px - entry_px) / entry_px)
                exit_fee = notional * (fee_taker_pct / 100.0)
                net_pnl = gross - entry_fee - exit_fee
                return TradeOutcome(
                    trade_id=0, asset=asset, entry_time_ms=entry_t, entry_price=entry_px,
                    exit_time_ms=c.open_time_ms, exit_price=exit_px, exit_reason="TAKE_PROFIT",
                    notional=notional, margin=notional, gross_pnl=gross, entry_fee=entry_fee,
                    exit_fee=exit_fee, net_pnl=net_pnl, net_return_pct=(net_pnl / notional * 100.0),
                    is_win=True, mfe_pct=mfe, mae_pct=mae
                )

        # In NO_SL mode: if TP1 was hit, check runner BE stop or TP2
        if tp1_hit:
            hit_tp2 = c.high >= tp2_px
            hit_be = c.low <= be_px
            if hit_be or hit_tp2:
                runner_px = be_px if hit_be else tp2_px
                exit_reason = "TP1_BE" if hit_be else "TP1_TP2"
                half = notional / 2.0
                tp1_pnl = half * ((tp1_px - entry_px) / entry_px) - half * (fee_taker_pct / 100.0)
                r_pnl = half * ((runner_px - entry_px) / entry_px) - half * (fee_taker_pct / 100.0)
                net_pnl = tp1_pnl + r_pnl - entry_fee
                return TradeOutcome(
                    trade_id=0, asset=asset, entry_time_ms=entry_t, entry_price=entry_px,
                    exit_time_ms=c.open_time_ms, exit_price=runner_px, exit_reason=exit_reason,
                    notional=notional, margin=notional, gross_pnl=tp1_pnl+r_pnl, entry_fee=entry_fee,
                    exit_fee=notional*(fee_taker_pct/100.0), net_pnl=net_pnl,
                    net_return_pct=(net_pnl / notional * 100.0), is_win=(net_pnl > 0),
                    mfe_pct=mfe, mae_pct=mae
                )

        # 3. End of data or Signal Exit
        if i == end_idx:
            exit_reason = "SIGNAL_EXIT" if (exit_on_opposing and sig.exit_signal_idx == end_idx) else "END_OF_DATA"
            exit_px = c.close
            gross = notional * ((exit_px - entry_px) / entry_px)
            exit_fee = notional * (fee_taker_pct / 100.0)
            net_pnl = gross - entry_fee - exit_fee
            return TradeOutcome(
                trade_id=0, asset=asset, entry_time_ms=entry_t, entry_price=entry_px,
                exit_time_ms=c.close_time_ms, exit_price=exit_px, exit_reason=exit_reason,
                notional=notional, margin=notional, gross_pnl=gross, entry_fee=entry_fee,
                exit_fee=exit_fee, net_pnl=net_pnl, net_return_pct=(net_pnl / notional * 100.0),
                is_win=(net_pnl > 0), mfe_pct=mfe, mae_pct=mae
            )

    # Fallback
    c_last = candles[end_idx]
    exit_px = c_last.close
    gross = notional * ((exit_px - entry_px) / entry_px)
    exit_fee = notional * (fee_taker_pct / 100.0)
    net_pnl = gross - entry_fee - exit_fee
    return TradeOutcome(
        trade_id=0, asset=asset, entry_time_ms=entry_t, entry_price=entry_px,
        exit_time_ms=c_last.close_time_ms, exit_price=exit_px, exit_reason="END_OF_DATA",
        notional=notional, margin=notional, gross_pnl=gross, entry_fee=entry_fee,
        exit_fee=exit_fee, net_pnl=net_pnl, net_return_pct=(net_pnl / notional * 100.0),
        is_win=(net_pnl > 0), mfe_pct=mfe, mae_pct=mae
    )


def run_comparative_backtest():
    print("=" * 95)
    print("🔬 COMPREHENSIVE COMPARISON: NO-STOP-LOSS vs. INTENDED STRATEGY WITH STOP-LOSS")
    print("=" * 95)

    crypto_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")
    stocks_dir = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Stocks")

    # Load candles for all 10 assets
    candles_dict = {}
    for sym in TARGET_ASSETS:
        candles_dict[sym] = load_candles(sym, "1h", crypto_dir, stocks_dir)

    common_start = max(candles_dict[sym][0].open_time_ms for sym in TARGET_ASSETS)
    common_end = min(candles_dict[sym][-1].close_time_ms for sym in TARGET_ASSETS)

    trimmed_candles = {sym: [c for c in clist if c.open_time_ms >= common_start and c.close_time_ms <= common_end] for sym, clist in candles_dict.items()}

    modes_to_test = [
        ("NO_SL", "1. No Stop Loss (Run to TP/Liq)"),
        ("INTENDED_ATR", "2. Intended Strategy SL (1.5x ATR SL, 2x ATR TP)"),
        ("INTENDED_SIGNAL", "3. Intended Signal Reversal SL (Exit on Opposing)"),
        ("DYNAMIC_MODE", "4. Dynamic Mode SL (Stop-Loss = Mode MAE)"),
    ]

    # Precalculate ATR, Signals, Modes per asset
    asset_data = {}
    for sym in TARGET_ASSETS:
        clist = trimmed_candles[sym]
        highs = np.array([c.high for c in clist])
        lows = np.array([c.low for c in clist])
        closes = np.array([c.close for c in clist])
        atr_arr = compute_atr(highs, lows, closes, 14)
        
        sigs = run_strategy("ema_cross", clist, direction="long")
        sigs = [s for s in sigs if s.entry_time_ms >= common_start and s.entry_time_ms <= common_end]
        
        base_tr = run_baseline_trades(clist, sigs, direction_mode="long")
        m_mfe, m_mae = compute_empirical_modes(base_tr)
        
        asset_data[sym] = {
            "candles": clist,
            "atr_arr": atr_arr,
            "sigs": sigs,
            "mode_mfe": m_mfe if m_mfe > 0.05 else 5.0,
            "mode_mae": m_mae if m_mae > 0.10 else 2.5
        }

    # ─────────────────────────────────────────────────────────────
    # PART 1: INDIVIDUAL ASSET COMPARISON (ETH, NEAR, BTC, NVDA)
    # ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 95)
    print("📌 PART 1: KEY INDIVIDUAL ASSETS COMPARISON (Fixed $1,000 Margin Per Trade)")
    print("=" * 95)

    key_assets = ["ETH", "NEAR", "BTC", "NVDA"]
    asset_comp_results = []

    for sym in key_assets:
        ad = asset_data[sym]
        clist = ad["candles"]
        sigs = ad["sigs"]
        atr_arr = ad["atr_arr"]
        
        for m_key, m_label in modes_to_test:
            outcomes = []
            for s in sigs:
                atr_v = atr_arr[s.candle_idx] if s.candle_idx < len(atr_arr) else 0.0
                tr = simulate_trade_with_rules(
                    candles=clist, sig=s, mode=m_key, asset=sym,
                    dynamic_mfe_pct=ad["mode_mfe"], dynamic_mae_pct=ad["mode_mae"],
                    notional=1000.0, atr_val=atr_v
                )
                outcomes.append(tr)
                
            df_out = pd.DataFrame([o.__dict__ for o in outcomes])
            n_tot = len(df_out)
            wins = (df_out["net_pnl"] > 0).sum()
            losses = (df_out["net_pnl"] < 0).sum()
            wr = (wins / n_tot * 100.0) if n_tot > 0 else 0.0
            total_pnl = df_out["net_pnl"].sum()
            gross_prof = df_out[df_out["net_pnl"] > 0]["net_pnl"].sum()
            gross_loss = abs(df_out[df_out["net_pnl"] < 0]["net_pnl"].sum())
            pf = (gross_prof / gross_loss) if gross_loss > 0 else 999.0
            avg_win = df_out[df_out["net_pnl"] > 0]["net_pnl"].mean() if wins > 0 else 0.0
            avg_loss = df_out[df_out["net_pnl"] < 0]["net_pnl"].mean() if losses > 0 else 0.0
            
            # Cumulative drawdown
            df_out["cum"] = df_out["net_pnl"].cumsum()
            df_out["peak"] = df_out["cum"].cummax()
            max_dd = (df_out["peak"] - df_out["cum"]).max()
            
            asset_comp_results.append({
                "Asset": sym,
                "Strategy Mode": m_label,
                "Trades": n_tot,
                "Win Rate (%)": f"{wr:.1f}%",
                "Wins": wins,
                "Losses": losses,
                "Net Profit ($)": f"${total_pnl:+,.2f}",
                "Profit Factor": f"{pf:.2f}",
                "Avg Win ($)": f"+${avg_win:.2f}",
                "Avg Loss ($)": f"${avg_loss:.2f}",
                "Max DD ($)": f"${max_dd:,.2f}"
            })

    df_asset_comp = pd.DataFrame(asset_comp_results)
    print(df_asset_comp.to_string(index=False))

    # ─────────────────────────────────────────────────────────────
    # PART 2: FULL 10-PAIR PORTFOLIO COMPARISON (10% CASH SIZING)
    # ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 95)
    print("📌 PART 2: 10-PAIR PORTFOLIO COMPARISON (10% Cash Sizing, Max 1 Trade Per Asset)")
    print("=" * 95)

    port_comp_results = []
    horizon_results = {}

    for m_key, m_label in modes_to_test:
        # Precalculate all trade outcomes
        trajectories = {sym: [] for sym in TARGET_ASSETS}
        for sym in TARGET_ASSETS:
            ad = asset_data[sym]
            clist = ad["candles"]
            for s in ad["sigs"]:
                atr_v = ad["atr_arr"][s.candle_idx] if s.candle_idx < len(ad["atr_arr"]) else 0.0
                tr = simulate_trade_with_rules(
                    candles=clist, sig=s, mode=m_key, asset=sym,
                    dynamic_mfe_pct=ad["mode_mfe"], dynamic_mae_pct=ad["mode_mae"],
                    notional=1000.0, atr_val=atr_v
                )
                trajectories[sym].append(tr)

        # Build chronological event list
        events = []
        for sym, tr_list in trajectories.items():
            for t_idx, tr in enumerate(tr_list):
                events.append({"time_ms": tr.entry_time_ms, "type": "ENTRY", "asset": sym, "t_idx": t_idx, "tr": tr})
                events.append({"time_ms": tr.exit_time_ms, "type": "EXIT", "asset": sym, "t_idx": t_idx, "tr": tr})

        # Sort: time_ms, t_idx, ENTRY before EXIT for same trade
        events.sort(key=lambda x: (x["time_ms"], x["t_idx"], 0 if x["type"] == "ENTRY" else 1))

        cash = 1000.0
        active = {}
        completed = []
        eq_history = []
        skipped = 0

        for ev in events:
            t_ms = ev["time_ms"]
            sym = ev["asset"]
            tr = ev["tr"]

            if ev["type"] == "EXIT":
                if sym in active and active[sym]["t_idx"] == ev["t_idx"]:
                    pos = active.pop(sym)
                    margin = pos["margin"]
                    ret_pct = tr.net_return_pct
                    pnl = margin * (ret_pct / 100.0)
                    cash += (margin + pnl)
                    completed.append({
                        "asset": sym, "pnl": pnl, "is_win": pnl > 0,
                        "exit_reason": tr.exit_reason, "time_ms": t_ms
                    })
            elif ev["type"] == "ENTRY":
                if sym in active:
                    skipped += 1
                    continue
                if cash >= 1.0:
                    margin = cash * 0.10
                    cash -= margin
                    active[sym] = {"margin": margin, "t_idx": ev["t_idx"]}

            inv = sum(p["margin"] for p in active.values())
            eq_history.append({"time_ms": t_ms, "equity": cash + inv, "cash": cash, "invested": inv})

        df_eq = pd.DataFrame(eq_history)
        df_comp = pd.DataFrame(completed)

        final_eq = df_eq["equity"].iloc[-1]
        gain_usd = final_eq - 1000.0
        gain_pct = (gain_usd / 1000.0) * 100.0
        cagr = ((final_eq / 1000.0) ** (1.0 / 2.90) - 1.0) * 100.0

        df_eq["peak"] = df_eq["equity"].cummax()
        df_eq["dd_pct"] = (df_eq["peak"] - df_eq["equity"]) / df_eq["peak"] * 100.0
        max_dd = df_eq["dd_pct"].max()

        n_trades = len(df_comp)
        wins = (df_comp["pnl"] > 0).sum() if not df_comp.empty else 0
        losses = (df_comp["pnl"] < 0).sum() if not df_comp.empty else 0
        wr = (wins / n_trades * 100.0) if n_trades > 0 else 0.0

        port_comp_results.append({
            "Strategy Configuration": m_label,
            "Trades Executed": n_trades,
            "Win Rate (%)": f"{wr:.1f}%",
            "Wins": wins,
            "Losses": losses,
            "Final Equity ($)": f"${final_eq:,.2f}",
            "Net Profit ($)": f"${gain_usd:+,.2f}",
            "Net Gain (%)": f"{gain_pct:+.1f}%",
            "CAGR (%/yr)": f"{cagr:+.1f}%",
            "Max Portfolio DD (%)": f"-{max_dd:.1f}%",
            "Skipped Overlapping": skipped
        })

        # Calculate rolling horizons
        df_eq["dt"] = pd.to_datetime(df_eq["time_ms"], unit="ms", utc=True)
        df_eq["day"] = df_eq["dt"].dt.floor("D")
        daily_s = df_eq.groupby("day")["equity"].last()
        all_days = pd.date_range(start=pd.to_datetime(common_start, unit="ms", utc=True).floor("D"),
                                 end=pd.to_datetime(common_end, unit="ms", utc=True).floor("D"), freq="D", tz="UTC")
        daily_s = daily_s.reindex(all_days).ffill().bfill()

        h_records = {}
        for w_name, d in [("1 Day", 1), ("1 Week", 7), ("1 Month", 30), ("1 Year", 365)]:
            diff = daily_s.diff(d).dropna()
            start = daily_s.shift(d).dropna()
            pct = (diff / start) * 100.0
            h_records[w_name] = {
                "Expected ($)": f"+${diff.mean():.2f}" if diff.mean() >= 0 else f"-${abs(diff.mean()):.2f}",
                "Expected (%)": f"{pct.mean():+.2f}%",
                "Win Prob (%)": f"{(diff > 0).mean() * 100.0:.1f}%"
            }
        horizon_results[m_label] = h_records

    df_port_comp = pd.DataFrame(port_comp_results)
    print(df_port_comp.to_string(index=False))

    print("\n--- TIME HORIZON EXPECTANCY COMPARISON (10-Asset Portfolio) ---")
    rows_h = []
    for m_label, h_dict in horizon_results.items():
        row = {"Configuration": m_label}
        for w_name in ["1 Day", "1 Week", "1 Month", "1 Year"]:
            row[f"{w_name} Expected"] = f"{h_dict[w_name]['Expected ($)']} ({h_dict[w_name]['Expected (%)']})"
            row[f"{w_name} Win Prob"] = h_dict[w_name]["Win Prob (%)"]
        rows_h.append(row)
    print(pd.DataFrame(rows_h).to_string(index=False))

    return df_asset_comp, df_port_comp, pd.DataFrame(rows_h)

if __name__ == "__main__":
    run_comparative_backtest()
