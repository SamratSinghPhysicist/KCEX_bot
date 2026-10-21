#!/usr/bin/env python3
"""
TRUMP/USDT and DOGE/USDT Zero-Fee Quantitative Experiment
=========================================================
Evaluates the Long-Only, No-Stop-Loss (1x Leverage) strategy with ZERO exchange fees:
1. DOGE/USDT Single-Asset (100% Capital Compounding)
   - Full History (2019-2026)
   - 2020-2021 Dogecoin Mania Bull Market
   - 2023-2024 Bull Rally
2. TRUMP/USDT Single-Asset (100% Capital Compounding)
   - Full Available History (Jan 2025 - Oct 2026)
   - Initial Expansion / Rally Phase
3. Dual-Asset Portfolio (DOGE + TRUMP)
   - Synchronized timeline (Jan 2025 - Oct 2026)
   - 50% Position Sizing (Max 1 active per coin, total 100% capital utilization)
4. Fee Comparison:
   - Zero-Fee (0.0% Maker, 0.0% Taker, 0.0% BE buffer) vs
   - Standard Fee (0.015% Maker, 0.045% Taker, 0.06% BE buffer)
5. Time Horizons:
   - 1 Day, 1 Week, 1 Month, 3 Months, 6 Months, 1 Year
"""

import os
import sys
import pandas as pd
import numpy as np
import datetime
from dataclasses import asdict

# Ensure unbuffered utf-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.strategies import Candle, StrategySignal, run_strategy
from experiments.no_stop_loss_experiment import simulate_single_leg

CRYPTO_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "OHLCV_Data_Crypto")

def load_local_candles(symbol: str, timeframe: str = "1h") -> list:
    csv_path = os.path.join(CRYPTO_DIR, symbol, f"{timeframe}.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing {csv_path}")
        
    df = pd.read_csv(csv_path)
    col_map = {c: c.lower().strip() for c in df.columns}
    df.rename(columns=col_map, inplace=True)
    df = df.dropna(subset=["open_time", "open", "high", "low", "close"]).sort_values("open_time").reset_index(drop=True)
    
    candles = []
    for row in df.itertuples(index=False):
        ot = int(getattr(row, "open_time"))
        o = float(getattr(row, "open"))
        h = float(getattr(row, "high"))
        l = float(getattr(row, "low"))
        c = float(getattr(row, "close"))
        v = float(getattr(row, "volume")) if hasattr(row, "volume") else 0.0
        ct = int(getattr(row, "close_time")) if hasattr(row, "close_time") else ot + 3600000 - 1
        candles.append(Candle(open_time_ms=ot, open=o, high=h, low=l, close=c, volume=v, close_time_ms=ct))
    return candles

def run_single_asset(
    symbol: str,
    candles: list,
    initial_capital: float = 1000.0,
    zero_fee: bool = True,
    tp_pct: float = 5.0,
    regime_label: str = ""
):
    if len(candles) < 50:
        return None
        
    fee_maker = 0.0 if zero_fee else 0.015
    fee_taker = 0.0 if zero_fee else 0.045
    be_buf = 0.0 if zero_fee else 0.06
    
    signals = run_strategy("ema_cross", candles, direction="long")
    
    capital = initial_capital
    active_until_ms = 0
    executed_trades = []
    skipped = 0
    
    for s in signals:
        s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
        c_entry = candles[s_idx] if s_idx < len(candles) else candles[s.candle_idx]
        
        if c_entry.open_time_ms < active_until_ms:
            skipped += 1
            continue
            
        entry_px = c_entry.open
        current_margin = capital
        
        tr = simulate_single_leg(
            direction="LONG",
            candles=candles,
            start_idx=s_idx,
            entry_px=entry_px,
            entry_time_ms=c_entry.open_time_ms,
            notional=current_margin,
            margin_used=current_margin,
            tp1_pct=tp_pct,
            be_buffer_pct=be_buf,
            tp2_pct=tp_pct,
            exit_signal_idx=s.exit_signal_idx,
            resolver=None,
            symbol=symbol,
            timeframe="1h",
            tp_rule="mode_dynamic",
            fee_maker_pct=fee_maker,
            fee_taker_pct=fee_taker,
            exit_on_signal=False
        )
        
        capital += tr.net_pnl
        active_until_ms = tr.exit_time_ms
        
        d = asdict(tr)
        d["capital_after"] = capital
        d["duration_hours"] = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0
        d["entry_dt"] = pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True)
        d["exit_dt"] = pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True)
        executed_trades.append(d)
        
    df_trades = pd.DataFrame(executed_trades)
    span_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)
    
    return {
        "symbol": symbol,
        "regime": regime_label,
        "zero_fee": zero_fee,
        "span_days": span_days,
        "initial_capital": initial_capital,
        "final_capital": capital,
        "net_gain_pct": ((capital - initial_capital) / initial_capital) * 100.0,
        "trades_count": len(executed_trades),
        "skipped_count": skipped,
        "df_trades": df_trades,
        "candles": candles
    }

def run_dual_asset(
    candles_doge: list,
    candles_trump: list,
    initial_capital: float = 1000.0,
    zero_fee: bool = True,
    tp_pct: float = 5.0,
    max_pos_fraction: float = 0.50
):
    t0_ms = max(candles_doge[0].open_time_ms, candles_trump[0].open_time_ms)
    t1_ms = min(candles_doge[-1].close_time_ms, candles_trump[-1].close_time_ms)
    
    c_doge = [c for c in candles_doge if c.open_time_ms >= t0_ms and c.close_time_ms <= t1_ms]
    c_trump = [c for c in candles_trump if c.open_time_ms >= t0_ms and c.close_time_ms <= t1_ms]
    
    fee_maker = 0.0 if zero_fee else 0.015
    fee_taker = 0.0 if zero_fee else 0.045
    be_buf = 0.0 if zero_fee else 0.06
    
    sig_doge = run_strategy("ema_cross", c_doge, direction="long")
    sig_trump = run_strategy("ema_cross", c_trump, direction="long")
    
    events = []
    for s in sig_doge:
        idx = s.candle_idx + 1 if s.candle_idx + 1 < len(c_doge) else s.candle_idx
        events.append(("DOGE", c_doge[idx].open_time_ms, idx, s))
    for s in sig_trump:
        idx = s.candle_idx + 1 if s.candle_idx + 1 < len(c_trump) else s.candle_idx
        events.append(("TRUMP", c_trump[idx].open_time_ms, idx, s))
    events.sort(key=lambda x: x[1])
    
    signal_map = {}
    for sym, ts, idx, s in events:
        signal_map.setdefault(ts, []).append((sym, idx, s))
        
    all_timestamps = sorted(list(set([c.open_time_ms for c in c_doge] + [c.open_time_ms for c in c_trump])))
    
    cash = initial_capital
    active_positions = {}
    completed_trades = []
    
    for ts in all_timestamps:
        # Check closed trades
        for sym in list(active_positions.keys()):
            pos = active_positions[sym]
            if ts >= pos["exit_time_ms"]:
                cash += pos["returned_cash"]
                pos["capital_after"] = cash
                completed_trades.append(pos)
                del active_positions[sym]
                
        # Check new signals
        if ts in signal_map:
            for sym, idx, sig in signal_map[ts]:
                if sym in active_positions:
                    continue
                    
                total_equity = cash + sum(p["notional"] for p in active_positions.values())
                target_pos = total_equity * max_pos_fraction
                pos_size = min(cash, target_pos)
                
                if pos_size < 10.0:
                    continue
                    
                candles_ref = c_doge if sym == "DOGE" else c_trump
                c_entry = candles_ref[idx]
                
                cash -= pos_size
                
                tr = simulate_single_leg(
                    direction="LONG",
                    candles=candles_ref,
                    start_idx=idx,
                    entry_px=c_entry.open,
                    entry_time_ms=c_entry.open_time_ms,
                    notional=pos_size,
                    margin_used=pos_size,
                    tp1_pct=tp_pct,
                    be_buffer_pct=be_buf,
                    tp2_pct=tp_pct,
                    exit_signal_idx=sig.exit_signal_idx,
                    resolver=None,
                    symbol=sym,
                    timeframe="1h",
                    tp_rule="mode_dynamic",
                    fee_maker_pct=fee_maker,
                    fee_taker_pct=fee_taker,
                    exit_on_signal=False
                )
                
                d = asdict(tr)
                d["notional"] = pos_size
                d["returned_cash"] = pos_size + tr.net_pnl
                d["duration_hours"] = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0
                d["entry_dt"] = pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True)
                d["exit_dt"] = pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True)
                active_positions[sym] = d
                
    for sym, pos in list(active_positions.items()):
        cash += pos["returned_cash"]
        pos["capital_after"] = cash
        completed_trades.append(pos)
        
    df_trades = pd.DataFrame(completed_trades)
    span_days = (t1_ms - t0_ms) / (1000.0 * 86400.0)
    
    return {
        "symbol": "DOGE + TRUMP Dual",
        "regime": "Synchronized (Jan 2025 - Oct 2026)",
        "zero_fee": zero_fee,
        "span_days": span_days,
        "initial_capital": initial_capital,
        "final_capital": cash,
        "net_gain_pct": ((cash - initial_capital) / initial_capital) * 100.0,
        "trades_count": len(completed_trades),
        "df_trades": df_trades,
        "candles": c_doge
    }

def compute_rolling_horizons(df_trades, candles, initial_capital=1000.0):
    if df_trades.empty:
        return pd.DataFrame()
        
    start_dt = pd.to_datetime(candles[0].open_time_ms, unit="ms", utc=True).floor("D")
    end_dt = pd.to_datetime(candles[-1].close_time_ms, unit="ms", utc=True).floor("D")
    all_days = pd.date_range(start=start_dt, end=end_dt, freq="D")
    
    df_copy = df_trades.copy()
    df_copy["exit_day"] = df_copy["exit_dt"].dt.floor("D")
    last_cap = df_copy.groupby("exit_day")["capital_after"].last()
    daily_s = last_cap.reindex(all_days).ffill().fillna(initial_capital)
    
    windows = [
        ("1 Day", 1),
        ("1 Week (7d)", 7),
        ("1 Month (30d)", 30),
        ("3 Months (90d)", 90),
        ("6 Months (180d)", 180),
        ("1 Year (365d)", 365)
    ]
    res = []
    for w_name, d in windows:
        if len(daily_s) < d:
            continue
        diff = daily_s.diff(d).dropna()
        start = daily_s.shift(d).dropna()
        pct = (diff / start) * 100.0
        res.append({
            "Time Horizon": w_name,
            "Expected Profit ($)": f"+${diff.mean():,.2f}",
            "Expected Gain (%)": f"+{pct.mean():.2f}%",
            "Median Profit ($)": f"+${diff.median():,.2f}",
            "Median Gain (%)": f"+{pct.median():.2f}%",
            "Typical Range (10th-90th Pct)": f"+{pct.quantile(0.10):.1f}% to +{pct.quantile(0.90):.1f}%",
            "Win Prob (%)": f"{(diff > 0).mean()*100:.1f}%"
        })
    return pd.DataFrame(res)

def print_report(res, title):
    if not res:
        return
    df = res["df_trades"]
    c_init = res["initial_capital"]
    c_final = res["final_capital"]
    gain_pct = res["net_gain_pct"]
    n_exec = res["trades_count"]
    wins = (df["net_pnl"] > 0).sum() if not df.empty else 0
    span_days = res["span_days"]
    cagr = ((c_final / c_init) ** (1.0 / max(0.1, span_days / 365.25)) - 1.0) * 100.0
    fee_type = "ZERO FEES (0.0% Maker / 0.0% Taker)" if res["zero_fee"] else "STANDARD FEES (0.015% Maker / 0.045% Taker)"
    
    print("\n" + "=" * 90)
    print(f"🚀 {title}")
    print(f"Fee Structure: {fee_type}")
    print(f"Duration:      {span_days:.1f} days ({span_days/30.417:.1f} months) | {pd.to_datetime(res['candles'][0].open_time_ms, unit='ms').strftime('%Y-%m-%d')} to {pd.to_datetime(res['candles'][-1].close_time_ms, unit='ms').strftime('%Y-%m-%d')}")
    print(f"Capital:       ${c_init:,.2f}  -->  ${c_final:,.2f}  (Net Gain: +{gain_pct:,.1f}%)")
    print(f"Performance:   CAGR: +{cagr:.1f}%/yr | Trades: {n_exec} | Wins: {wins} ({wins/max(1, n_exec)*100:.1f}%)")
    if not df.empty and "duration_hours" in df.columns:
        print(f"Trade Duration:Avg {df['duration_hours'].mean():.1f}h ({df['duration_hours'].mean()/24.0:.1f}d) | Median {df['duration_hours'].median():.1f}h ({df['duration_hours'].median()/24.0:.1f}d) | Max {df['duration_hours'].max():.1f}h ({df['duration_hours'].max()/24.0:.1f}d)")
        # Calculate max trade drawdown if available
        if "mae_pct" in df.columns:
            print(f"Intra-trade Drawdown: Median MAE: -{df['mae_pct'].median():.2f}% | Max MAE: -{df['mae_pct'].max():.2f}%")
    print("=" * 90)
    
    rolling = compute_rolling_horizons(df, res["candles"], c_init)
    if not rolling.empty:
        print("\n--- EXPECTED EARNINGS BREAKDOWN (Rolling Horizons) ---")
        print(rolling.to_string(index=False))

def main():
    doge_candles = load_local_candles("DOGE", "1h")
    trump_candles = load_local_candles("TRUMP", "1h")
    
    print(f"Loaded DOGE candles: {len(doge_candles):,}")
    print(f"Loaded TRUMP candles: {len(trump_candles):,}")
    
    # ─────────────────────────────────────────────────────────────
    # 1. DOGE 100% Capital (Zero-Fee vs Standard-Fee)
    # ─────────────────────────────────────────────────────────────
    # Full History
    res_doge_full_0fee = run_single_asset("DOGE", doge_candles, 1000.0, zero_fee=True, regime_label="Full History (2019-2026)")
    res_doge_full_std = run_single_asset("DOGE", doge_candles, 1000.0, zero_fee=False, regime_label="Full History (2019-2026)")
    print_report(res_doge_full_0fee, "DOGE 100% CAPITAL - FULL HISTORY (2019-2026)")
    diff_doge_full = res_doge_full_0fee['final_capital'] - res_doge_full_std['final_capital']
    print(f"\n💰 ZERO-FEE BONUS (DOGE Full History):")
    print(f"   Zero Fees Final:     ${res_doge_full_0fee['final_capital']:,.2f} (+{res_doge_full_0fee['net_gain_pct']:,.1f}%)")
    print(f"   Standard Fees Final: ${res_doge_full_std['final_capital']:,.2f} (+{res_doge_full_std['net_gain_pct']:,.1f}%)")
    print(f"   Extra Profit Kept:   +${diff_doge_full:,.2f} (+{diff_doge_full/res_doge_full_std['final_capital']*100:.1f}% fee compounding advantage)")

    # DOGE 2020-2021 Bull Run
    t0_bull1 = int(pd.Timestamp("2020-10-01", tz="UTC").timestamp() * 1000)
    t1_bull1 = int(pd.Timestamp("2021-06-01", tz="UTC").timestamp() * 1000)
    c_doge_bull1 = [c for c in doge_candles if c.open_time_ms >= t0_bull1 and c.close_time_ms <= t1_bull1]
    res_doge_bull1 = run_single_asset("DOGE", c_doge_bull1, 1000.0, zero_fee=True, regime_label="2020-2021 Doge Mania")
    print_report(res_doge_bull1, "DOGE 100% CAPITAL - 2020-2021 DOGECOIN MANIA BULL MARKET")

    # DOGE 2023-2024 Bull Rally
    t0_bull2 = int(pd.Timestamp("2023-10-01", tz="UTC").timestamp() * 1000)
    t1_bull2 = int(pd.Timestamp("2024-10-01", tz="UTC").timestamp() * 1000)
    c_doge_bull2 = [c for c in doge_candles if c.open_time_ms >= t0_bull2 and c.close_time_ms <= t1_bull2]
    res_doge_bull2 = run_single_asset("DOGE", c_doge_bull2, 1000.0, zero_fee=True, regime_label="2023-2024 Bull Rally")
    print_report(res_doge_bull2, "DOGE 100% CAPITAL - 2023-2024 BULL RALLY")

    # ─────────────────────────────────────────────────────────────
    # 2. TRUMP 100% Capital (Zero-Fee vs Standard-Fee)
    # ─────────────────────────────────────────────────────────────
    res_trump_full_0fee = run_single_asset("TRUMP", trump_candles, 1000.0, zero_fee=True, regime_label="Full Available History (2025-2026)")
    res_trump_full_std = run_single_asset("TRUMP", trump_candles, 1000.0, zero_fee=False, regime_label="Full Available History (2025-2026)")
    print_report(res_trump_full_0fee, "TRUMP 100% CAPITAL - FULL AVAILABLE HISTORY (Jan 2025 - Oct 2026)")
    diff_trump_full = res_trump_full_0fee['final_capital'] - res_trump_full_std['final_capital']
    print(f"\n💰 ZERO-FEE BONUS (TRUMP Full History):")
    print(f"   Zero Fees Final:     ${res_trump_full_0fee['final_capital']:,.2f} (+{res_trump_full_0fee['net_gain_pct']:,.1f}%)")
    print(f"   Standard Fees Final: ${res_trump_full_std['final_capital']:,.2f} (+{res_trump_full_std['net_gain_pct']:,.1f}%)")
    print(f"   Extra Profit Kept:   +${diff_trump_full:,.2f} (+{diff_trump_full/res_trump_full_std['final_capital']*100:.1f}% fee compounding advantage)")

    # TRUMP 90-day post-launch rally
    t0_trump_rally = trump_candles[0].open_time_ms
    t1_trump_rally = t0_trump_rally + int(90 * 86400 * 1000)
    c_trump_rally = [c for c in trump_candles if c.open_time_ms >= t0_trump_rally and c.close_time_ms <= t1_trump_rally]
    res_trump_rally = run_single_asset("TRUMP", c_trump_rally, 1000.0, zero_fee=True, regime_label="TRUMP Initial 90-Day Expansion")
    print_report(res_trump_rally, "TRUMP 100% CAPITAL - INITIAL 90-DAY EXPANSION")

    # ─────────────────────────────────────────────────────────────
    # 3. DUAL PORTFOLIO (DOGE + TRUMP) Synchronized Timeline
    # ─────────────────────────────────────────────────────────────
    res_dual_0fee = run_dual_asset(doge_candles, trump_candles, 1000.0, zero_fee=True, max_pos_fraction=0.50)
    res_dual_std = run_dual_asset(doge_candles, trump_candles, 1000.0, zero_fee=False, max_pos_fraction=0.50)
    print_report(res_dual_0fee, "DUAL PORTFOLIO: DOGE + TRUMP (50% MAX SIZING PER COIN, ZERO FEES)")
    diff_dual = res_dual_0fee['final_capital'] - res_dual_std['final_capital']
    print(f"\n💰 ZERO-FEE BONUS (Dual Portfolio):")
    print(f"   Zero Fees Final:     ${res_dual_0fee['final_capital']:,.2f} (+{res_dual_0fee['net_gain_pct']:,.1f}%)")
    print(f"   Standard Fees Final: ${res_dual_std['final_capital']:,.2f} (+{res_dual_std['net_gain_pct']:,.1f}%)")
    print(f"   Extra Profit Kept:   +${diff_dual:,.2f} (+{diff_dual/res_dual_std['final_capital']*100:.1f}% fee compounding advantage)")

if __name__ == "__main__":
    main()
