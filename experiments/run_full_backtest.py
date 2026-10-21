#!/usr/bin/env python3
"""
Full Back-Test Automation Suite
==============================
Executes comprehensive quantitative trading evaluations across 5 distinct scenarios:
  - Scenario A: Long-only, 10% position sizing, 10 assets with intended Stop-Loss & Take-Profit.
  - Scenario B: No-Stop-Loss baseline on the same 10 assets & comparative analysis vs Scenario A.
  - Scenario C: Single-asset extreme sizing (NEAR only, 100% capital, no stop-loss) + bull projection.
  - Scenario D: Zero-fee pairs (TRUMP/USDT & DOGE/USDT) under 100% and 10% sizing (2025-08-01 to 2026-09-30).
  - Scenario E: 1-tick move chasing on zero-fee pairs across 0 to 7 ticks slippage with drawdown recovery.

All outputs are printed to stdout, logged to backtest_output.txt, and written as CSVs under results/.
"""

from __future__ import annotations
import os
import sys
import math
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

# Set up unbuffered UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

# Ensure repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

RESULTS_DIR = os.path.join(ROOT_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(ROOT_DIR, "backtest_output.txt")


class TeeLogger:
    """Duplicates all stdout writes to both console and a log file."""
    def __init__(self, filename: str):
        self.terminal = sys.stdout
        self.logfile = open(filename, "w", encoding="utf-8", errors="replace")

    def write(self, message: str) -> None:
        self.terminal.write(message)
        self.terminal.flush()
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self) -> None:
        self.terminal.flush()
        self.logfile.flush()


# Activate TeeLogger so all terminal output is also captured to backtest_output.txt
sys.stdout = TeeLogger(LOG_FILE_PATH)

from experiments.strategies import Candle, StrategySignal, run_strategy, compute_atr
from experiments.no_stop_loss_experiment import simulate_single_leg
from scripts.download_market_data import (
    download_crypto,
    download_stock_or_commodity,
    DEFAULT_CRYPTO_DIR,
    DEFAULT_STOCKS_DIR
)


def ensure_asset_data(symbol: str, timeframe: str = "1h") -> None:
    """Verifies data file exists for symbol, and downloads if missing."""
    sym = symbol.upper().strip()
    is_crypto = sym in ["BTC", "ETH", "SOL", "SUI", "NEAR", "DOGE", "TRUMP"]
    target_dir = DEFAULT_CRYPTO_DIR if is_crypto else DEFAULT_STOCKS_DIR
    target_csv = os.path.join(target_dir, sym, f"{timeframe}.csv")

    if os.path.isfile(target_csv) and os.path.getsize(target_csv) > 100:
        return

    print(f"[*] OHLCV data missing for {sym} ({timeframe}). Downloading...", flush=True)
    if sym in ["DOGE", "TRUMP"]:
        from scripts.download_doge_trump import download_full_binance_history
        df = download_full_binance_history(sym, timeframe)
        if not df.empty:
            os.makedirs(os.path.dirname(target_csv), exist_ok=True)
            df.to_csv(target_csv, index=False)
            print(f"[✓] Saved {len(df):,} bars to {target_csv}", flush=True)
    elif sym in ["BTC", "ETH", "SOL", "SUI", "NEAR"]:
        download_crypto(sym, timeframe, DEFAULT_CRYPTO_DIR)
    else:
        download_stock_or_commodity(sym, timeframe, DEFAULT_STOCKS_DIR)


def load_asset_candles(symbol: str, timeframe: str = "1h") -> List[Candle]:
    """Loads OHLCV candlestick data into a list of Candle objects."""
    sym = symbol.upper().strip()
    crypto_csv = os.path.join(DEFAULT_CRYPTO_DIR, sym, f"{timeframe}.csv")
    stocks_csv = os.path.join(DEFAULT_STOCKS_DIR, sym, f"{timeframe}.csv")

    if os.path.isfile(crypto_csv) and os.path.getsize(crypto_csv) > 100:
        csv_path = crypto_csv
    elif os.path.isfile(stocks_csv) and os.path.getsize(stocks_csv) > 100:
        csv_path = stocks_csv
    else:
        ensure_asset_data(sym, timeframe)
        if os.path.isfile(crypto_csv) and os.path.getsize(crypto_csv) > 100:
            csv_path = crypto_csv
        elif os.path.isfile(stocks_csv) and os.path.getsize(stocks_csv) > 100:
            csv_path = stocks_csv
        else:
            raise FileNotFoundError(f"Failed to find or download OHLCV data for {sym} ({timeframe})")

    df = pd.read_csv(csv_path)
    col_map = {c: c.lower().strip() for c in df.columns}
    df.rename(columns=col_map, inplace=True)
    df = df.dropna(subset=["open_time", "open", "high", "low", "close"]).sort_values("open_time").reset_index(drop=True)

    candles = []
    has_vol = "volume" in df.columns
    has_close_time = "close_time" in df.columns
    for row in df.itertuples(index=False):
        ot = int(getattr(row, "open_time"))
        o = float(getattr(row, "open"))
        h = float(getattr(row, "high"))
        l = float(getattr(row, "low"))
        c = float(getattr(row, "close"))
        v = float(getattr(row, "volume")) if has_vol else 0.0
        ct = int(getattr(row, "close_time")) if has_close_time else ot + 3600000 - 1
        candles.append(Candle(open_time_ms=ot, open=o, high=h, low=l, close=c, volume=v, close_time_ms=ct))
    return candles


@dataclass
class TradeOutcome:
    trade_id: int
    asset: str
    entry_time_ms: int
    entry_price: float
    exit_time_ms: int
    exit_price: float
    exit_reason: str
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


def simulate_trade_with_sl_tp(
    candles: List[Candle],
    sig: StrategySignal,
    asset: str,
    enable_stop_loss: bool = True,
    atr_val: float = 0.0,
    sl_multiplier: float = 1.5,
    tp_multiplier: float = 2.0,
    fee_maker_pct: float = 0.015,
    fee_taker_pct: float = 0.045,
    notional: float = 1000.0,
) -> TradeOutcome:
    """Simulates an individual trade with customizable SL/TP and transaction fees."""
    n = len(candles)
    start_idx = sig.candle_idx + 1 if sig.candle_idx + 1 < n else sig.candle_idx
    entry_px = candles[start_idx].open if start_idx < n else sig.entry_price
    entry_t = candles[start_idx].open_time_ms if start_idx < n else sig.entry_time_ms
    entry_fee = notional * (fee_maker_pct / 100.0)

    eff_atr = atr_val if atr_val > 0 else (entry_px * 0.015)
    tp_px = entry_px + tp_multiplier * eff_atr
    sl_px = (entry_px - sl_multiplier * eff_atr) if enable_stop_loss else 0.0

    mfe = 0.0
    mae = 0.0

    for i in range(start_idx, n):
        c = candles[i]
        c_mfe = (c.high - entry_px) / entry_px * 100.0
        c_mae = (entry_px - c.low) / entry_px * 100.0
        mfe = max(mfe, c_mfe)
        mae = max(mae, c_mae)

        # 1. Check Stop-Loss
        if sl_px > 0.0 and c.low <= sl_px:
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

        # 2. Check Take-Profit
        if c.high >= tp_px:
            exit_px = tp_px
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

    # 3. End of Data
    c_last = candles[-1]
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


def run_portfolio_simulation(
    target_assets: List[str],
    enable_stop_loss: bool = True,
    initial_capital: float = 1000.0,
    sizing_pct: float = 0.10,
    scenario_name: str = "Scenario"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Runs a synchronized 10-asset chronological portfolio backtest."""
    # Load candles for all assets
    candles_dict: Dict[str, List[Candle]] = {}
    for sym in target_assets:
        candles_dict[sym] = load_asset_candles(sym, "1h")

    # Find common overlapping period across all 10 assets
    common_start = max(candles_dict[s][0].open_time_ms for s in target_assets)
    common_end = min(candles_dict[s][-1].close_time_ms for s in target_assets)

    t_start_dt = pd.to_datetime(common_start, unit="ms", utc=True)
    t_end_dt = pd.to_datetime(common_end, unit="ms", utc=True)
    span_days = (common_end - common_start) / (1000.0 * 86400.0)

    # Trim candles to common period
    trimmed_candles = {
        s: [c for c in clist if c.open_time_ms >= common_start and c.close_time_ms <= common_end]
        for s, clist in candles_dict.items()
    }

    # Precalculate signals & trajectories
    trajectories: Dict[str, List[TradeOutcome]] = {s: [] for s in target_assets}
    for s in target_assets:
        clist = trimmed_candles[s]
        highs = np.array([c.high for c in clist], dtype=float)
        lows = np.array([c.low for c in clist], dtype=float)
        closes = np.array([c.close for c in clist], dtype=float)
        atr_arr = compute_atr(highs, lows, closes, 14)

        sigs = run_strategy("ema_cross", clist, direction="long")
        sigs = [sig for sig in sigs if sig.entry_time_ms >= common_start and sig.entry_time_ms <= common_end]

        for sig in sigs:
            atr_v = atr_arr[sig.candle_idx] if sig.candle_idx < len(atr_arr) else 0.0
            tr = simulate_trade_with_sl_tp(
                candles=clist, sig=sig, asset=s,
                enable_stop_loss=enable_stop_loss, atr_val=atr_v
            )
            trajectories[s].append(tr)

    # Build chronological event list
    events = []
    for s, tr_list in trajectories.items():
        for t_idx, tr in enumerate(tr_list):
            events.append({"time_ms": tr.entry_time_ms, "type": "ENTRY", "asset": s, "t_idx": t_idx, "tr": tr})
            events.append({"time_ms": tr.exit_time_ms, "type": "EXIT", "asset": s, "t_idx": t_idx, "tr": tr})

    events.sort(key=lambda x: (x["time_ms"], x["t_idx"], 0 if x["type"] == "ENTRY" else 1))

    cash = initial_capital
    active_positions: Dict[str, Dict[str, Any]] = {}
    completed_trades: List[Dict[str, Any]] = []
    eq_history: List[Dict[str, Any]] = []
    skipped_count = 0

    asset_stats = {s: {"executed": 0, "wins": 0, "losses": 0, "net_pnl": 0.0} for s in target_assets}

    for ev in events:
        t_ms = ev["time_ms"]
        sym = ev["asset"]
        tr = ev["tr"]

        if ev["type"] == "EXIT":
            if sym in active_positions and active_positions[sym]["t_idx"] == ev["t_idx"]:
                pos = active_positions.pop(sym)
                margin = pos["margin"]
                ret_pct = tr.net_return_pct
                pnl = margin * (ret_pct / 100.0)
                cash += (margin + pnl)

                is_win = pnl > 0
                completed_trades.append({
                    "asset": sym,
                    "entry_time_ms": tr.entry_time_ms,
                    "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
                    "entry_price": tr.entry_price,
                    "exit_time_ms": tr.exit_time_ms,
                    "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
                    "exit_price": tr.exit_price,
                    "exit_reason": tr.exit_reason,
                    "margin": margin,
                    "net_pnl": pnl,
                    "net_return_pct": ret_pct,
                    "is_win": is_win,
                    "cash_after": cash
                })

                asset_stats[sym]["executed"] += 1
                if is_win:
                    asset_stats[sym]["wins"] += 1
                else:
                    asset_stats[sym]["losses"] += 1
                asset_stats[sym]["net_pnl"] += pnl

        elif ev["type"] == "ENTRY":
            if sym in active_positions:
                skipped_count += 1
                continue
            if cash >= 1.0:
                margin = cash * sizing_pct
                cash -= margin
                active_positions[sym] = {"margin": margin, "t_idx": ev["t_idx"]}

        invested = sum(p["margin"] for p in active_positions.values())
        eq_history.append({"time_ms": t_ms, "equity": cash + invested, "cash": cash, "invested": invested})

    df_trades = pd.DataFrame(completed_trades)
    df_eq = pd.DataFrame(eq_history)

    final_equity = cash + sum(p["margin"] for p in active_positions.values())
    total_gain_usd = final_equity - initial_capital
    total_gain_pct = (total_gain_usd / initial_capital) * 100.0
    cagr = ((final_equity / initial_capital) ** (1.0 / max(0.1, span_days / 365.25)) - 1.0) * 100.0

    df_eq["peak"] = df_eq["equity"].cummax()
    df_eq["dd_pct"] = (df_eq["peak"] - df_eq["equity"]) / df_eq["peak"] * 100.0
    max_dd_pct = df_eq["dd_pct"].max() if not df_eq.empty else 0.0

    total_executed = len(df_trades)
    total_wins = (df_trades["net_pnl"] > 0).sum() if not df_trades.empty else 0
    total_losses = (df_trades["net_pnl"] < 0).sum() if not df_trades.empty else 0
    win_rate = (total_wins / total_executed * 100.0) if total_executed > 0 else 0.0

    # Per-Asset contribution table
    asset_rows = []
    for s in target_assets:
        st = asset_stats[s]
        wr = (st["wins"] / st["executed"] * 100.0) if st["executed"] > 0 else 0.0
        share = (st["net_pnl"] / total_gain_usd * 100.0) if total_gain_usd != 0 else 0.0
        asset_rows.append({
            "Asset": s,
            "Trades Executed": st["executed"],
            "Wins": st["wins"],
            "Losses": st["losses"],
            "Win Rate (%)": round(wr, 2),
            "Total PnL Generated ($)": round(st["net_pnl"], 2),
            "Share of Total Profit (%)": round(share, 2)
        })
    df_assets = pd.DataFrame(asset_rows)

    # Rolling Time Horizon Returns (daily resample)
    df_eq["dt"] = pd.to_datetime(df_eq["time_ms"], unit="ms", utc=True)
    df_eq["day"] = df_eq["dt"].dt.floor("D")
    daily_s = df_eq.groupby("day")["equity"].last()
    all_days = pd.date_range(start=t_start_dt.floor("D"), end=t_end_dt.floor("D"), freq="D", tz="UTC")
    daily_s = daily_s.reindex(all_days).ffill().bfill()

    windows = [
        ("Daily (1d)", 1),
        ("Weekly (7d)", 7),
        ("Monthly (30d)", 30),
        ("Yearly (365d)", 365)
    ]
    horizon_rows = []
    for w_name, d in windows:
        if len(daily_s) <= d:
            continue
        diff = daily_s.diff(d).dropna()
        start = daily_s.shift(d).dropna()
        pct = (diff / start) * 100.0
        horizon_rows.append({
            "Time Horizon": w_name,
            "Expected Profit ($)": round(diff.mean(), 2),
            "Expected Return (%)": round(pct.mean(), 2),
            "Median Return (%)": round(pct.median(), 2),
            "10th Pct (%)": round(pct.quantile(0.10), 2),
            "90th Pct (%)": round(pct.quantile(0.90), 2),
            "Win Probability (%)": round((diff > 0).mean() * 100.0, 2)
        })
    df_horizons = pd.DataFrame(horizon_rows)

    summary = {
        "scenario": scenario_name,
        "assets": target_assets,
        "span_days": span_days,
        "start_date": t_start_dt.strftime("%Y-%m-%d"),
        "end_date": t_end_dt.strftime("%Y-%m-%d"),
        "initial_capital": initial_capital,
        "final_equity": final_equity,
        "net_gain_usd": total_gain_usd,
        "net_gain_pct": total_gain_pct,
        "cagr": cagr,
        "max_drawdown_pct": max_dd_pct,
        "trades_executed": total_executed,
        "wins": total_wins,
        "losses": total_losses,
        "win_rate": win_rate,
        "skipped_signals": skipped_count
    }

    return df_trades, df_assets, df_horizons, summary


# =====================================================================
# SCENARIO A: Long-only, 10% Position Sizing, 10 Assets (Intended SL/TP)
# =====================================================================
def execute_scenario_a(target_assets: List[str]) -> Tuple[Dict[str, Any], pd.DataFrame]:
    print("\n" + "=" * 90)
    print("📈 SCENARIO A: LONG-ONLY 10-ASSET PORTFOLIO (10% SIZING, INTENDED SL & TP)")
    print("=" * 90)

    df_trades, df_assets, df_horizons, summary = run_portfolio_simulation(
        target_assets=target_assets,
        enable_stop_loss=True,
        initial_capital=1000.0,
        sizing_pct=0.10,
        scenario_name="Scenario_A"
    )

    print(f"Data Overlapping Span: {summary['start_date']} to {summary['end_date']} ({summary['span_days']:.1f} days / {summary['span_days']/365.25:.2f} yrs)")
    print(f"Initial Capital:       ${summary['initial_capital']:,.2f}")
    print(f"Final Equity:          ${summary['final_equity']:,.2f} ({summary['net_gain_pct']:+.2f}%)")
    print(f"Net Profit:            ${summary['net_gain_usd']:+,.2f}")
    print(f"CAGR:                  {summary['cagr']:+.2f}% / year")
    print(f"Max Portfolio DD:      -{summary['max_drawdown_pct']:.2f}%")
    print(f"Trades Executed:       {summary['trades_executed']} (Wins: {summary['wins']}, Losses: {summary['losses']}, Win Rate: {summary['win_rate']:.1f}%)")

    print("\n--- PER-ASSET PROFITABILITY TABLE ---")
    print(df_assets.to_string(index=False))

    print("\n--- ROLLING CUMULATIVE RETURNS (HORIZONS) ---")
    print(df_horizons.to_string(index=False))

    # Save CSVs
    csv_a = os.path.join(RESULTS_DIR, "scenario_A.csv")
    df_trades.to_csv(csv_a, index=False)
    df_assets.to_csv(os.path.join(RESULTS_DIR, "scenario_A_per_asset.csv"), index=False)
    df_horizons.to_csv(os.path.join(RESULTS_DIR, "scenario_A_horizons.csv"), index=False)
    print(f"[✓] Saved Scenario A results to {csv_a}")

    return summary, df_trades


# =====================================================================
# SCENARIO B: No-Stop-Loss Baseline & Comparison vs Scenario A
# =====================================================================
def execute_scenario_b(target_assets: List[str], summary_a: Dict[str, Any]) -> Tuple[Dict[str, Any], pd.DataFrame]:
    print("\n" + "=" * 90)
    print("📉 SCENARIO B: NO-STOP-LOSS BASELINE (SAME 10 ASSETS, SL DISABLED, TP ACTIVE)")
    print("=" * 90)

    df_trades_b, df_assets_b, df_horizons_b, summary_b = run_portfolio_simulation(
        target_assets=target_assets,
        enable_stop_loss=False,
        initial_capital=1000.0,
        sizing_pct=0.10,
        scenario_name="Scenario_B"
    )

    print(f"Initial Capital:       ${summary_b['initial_capital']:,.2f}")
    print(f"Final Equity:          ${summary_b['final_equity']:,.2f} ({summary_b['net_gain_pct']:+.2f}%)")
    print(f"Net Profit:            ${summary_b['net_gain_usd']:+,.2f}")
    print(f"CAGR:                  {summary_b['cagr']:+.2f}% / year")
    print(f"Max Portfolio DD:      -{summary_b['max_drawdown_pct']:.2f}%")
    print(f"Trades Executed:       {summary_b['trades_executed']} (Wins: {summary_b['wins']}, Losses: {summary_b['losses']}, Win Rate: {summary_b['win_rate']:.1f}%)")

    # Comparative analysis against Scenario A
    diff_pnl = summary_b["net_gain_usd"] - summary_a["net_gain_usd"]
    diff_pnl_pct = ((summary_b["net_gain_usd"] - summary_a["net_gain_usd"]) / abs(summary_a["net_gain_usd"]) * 100.0) if summary_a["net_gain_usd"] != 0 else 0.0
    diff_equity_pct = ((summary_b["final_equity"] - summary_a["final_equity"]) / summary_a["final_equity"]) * 100.0
    diff_wr = summary_b["win_rate"] - summary_a["win_rate"]
    diff_dd = summary_b["max_drawdown_pct"] - summary_a["max_drawdown_pct"]

    print("\n" + "-" * 90)
    print("⚖️ HEAD-TO-HEAD COMPARISON: SCENARIO A (INTENDED SL) vs. SCENARIO B (NO SL)")
    print("-" * 90)
    comp_data = [
        {"Metric": "Final Equity ($)", "Scenario A (SL+TP)": f"${summary_a['final_equity']:,.2f}", "Scenario B (No SL)": f"${summary_b['final_equity']:,.2f}", "Absolute Difference": f"${summary_b['final_equity'] - summary_a['final_equity']:+,.2f}", "Percentage Difference": f"{diff_equity_pct:+.2f}%"},
        {"Metric": "Net Profit ($)", "Scenario A (SL+TP)": f"${summary_a['net_gain_usd']:+,.2f}", "Scenario B (No SL)": f"${summary_b['net_gain_usd']:+,.2f}", "Absolute Difference": f"${diff_pnl:+,.2f}", "Percentage Difference": f"{diff_pnl_pct:+.2f}%"},
        {"Metric": "Net Return (%)", "Scenario A (SL+TP)": f"{summary_a['net_gain_pct']:+.2f}%", "Scenario B (No SL)": f"{summary_b['net_gain_pct']:+.2f}%", "Absolute Difference": f"{summary_b['net_gain_pct'] - summary_a['net_gain_pct']:+.2f}%", "Percentage Difference": f"{diff_pnl_pct:+.2f}%"},
        {"Metric": "Win Rate (%)", "Scenario A (SL+TP)": f"{summary_a['win_rate']:.2f}%", "Scenario B (No SL)": f"{summary_b['win_rate']:.2f}%", "Absolute Difference": f"{diff_wr:+.2f}%", "Percentage Difference": f"{((summary_b['win_rate']-summary_a['win_rate'])/summary_a['win_rate']*100):+.2f}%"},
        {"Metric": "Max Drawdown (%)", "Scenario A (SL+TP)": f"-{summary_a['max_drawdown_pct']:.2f}%", "Scenario B (No SL)": f"-{summary_b['max_drawdown_pct']:.2f}%", "Absolute Difference": f"{diff_dd:+.2f}%", "Percentage Difference": f"{((diff_dd)/summary_a['max_drawdown_pct']*100):+.2f}%"},
        {"Metric": "Trades Executed", "Scenario A (SL+TP)": str(summary_a["trades_executed"]), "Scenario B (No SL)": str(summary_b["trades_executed"]), "Absolute Difference": f"{summary_b['trades_executed'] - summary_a['trades_executed']:+d}", "Percentage Difference": f"{((summary_b['trades_executed']-summary_a['trades_executed'])/summary_a['trades_executed']*100):+.2f}%"}
    ]
    df_comp = pd.DataFrame(comp_data)
    print(df_comp.to_string(index=False))

    # Save CSVs
    csv_b = os.path.join(RESULTS_DIR, "scenario_B.csv")
    csv_comp = os.path.join(RESULTS_DIR, "scenario_B_comparison.csv")
    df_trades_b.to_csv(csv_b, index=False)
    df_comp.to_csv(csv_comp, index=False)
    print(f"[✓] Saved Scenario B results to {csv_b} and comparison to {csv_comp}")

    return summary_b, df_trades_b


# =====================================================================
# SCENARIO C: Single-Asset Extreme Sizing (NEAR 100% Capital, No SL)
# =====================================================================
def execute_scenario_c() -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 90)
    print("🌐 SCENARIO C: SINGLE-ASSET EXTREME SIZING (NEAR 100% CAPITAL, NO STOP-LOSS)")
    print("=" * 90)

    candles = load_asset_candles("NEAR", "1h")
    span_days = (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000.0 * 86400.0)

    # 1. Full Historical Horizon
    sigs = run_strategy("ema_cross", candles, direction="long")
    capital = 1000.0
    active_until_ms = 0
    executed_trades = []

    for s in sigs:
        s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
        c_entry = candles[s_idx]
        if c_entry.open_time_ms < active_until_ms:
            continue

        margin = capital
        tr = simulate_single_leg(
            direction="LONG", candles=candles, start_idx=s_idx, entry_px=c_entry.open,
            entry_time_ms=c_entry.open_time_ms, notional=margin, margin_used=margin,
            tp1_pct=5.0, be_buffer_pct=0.06, tp2_pct=5.0, exit_signal_idx=s.exit_signal_idx,
            resolver=None, symbol="NEAR", timeframe="1h", tp_rule="mode_dynamic",
            fee_maker_pct=0.015, fee_taker_pct=0.045, exit_on_signal=False
        )
        capital += tr.net_pnl
        active_until_ms = tr.exit_time_ms
        dur_h = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0

        executed_trades.append({
            "asset": "NEAR",
            "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
            "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
            "entry_price": tr.entry_price,
            "exit_price": tr.exit_price,
            "margin": margin,
            "net_pnl": tr.net_pnl,
            "net_return_pct": tr.net_return_pct,
            "duration_hours": dur_h,
            "capital_after": capital,
            "is_win": tr.is_win,
            "exit_reason": tr.exit_reason
        })

    df_full = pd.DataFrame(executed_trades)
    gain_pct = ((capital - 1000.0) / 1000.0) * 100.0
    cagr = ((capital / 1000.0) ** (1.0 / max(0.1, span_days / 365.25)) - 1.0) * 100.0
    wins = (df_full["is_win"]).sum() if not df_full.empty else 0
    total_tr = len(df_full)
    wr = (wins / total_tr * 100.0) if total_tr > 0 else 0.0

    print(f"Full History Span:     {pd.to_datetime(candles[0].open_time_ms, unit='ms', utc=True).strftime('%Y-%m-%d')} to {pd.to_datetime(candles[-1].close_time_ms, unit='ms', utc=True).strftime('%Y-%m-%d')} ({span_days:.1f} days / {span_days/365.25:.2f} yrs)")
    print(f"Final Capital (Full):  ${capital:,.2f} ({gain_pct:+.2f}%)")
    print(f"CAGR (Full History):   {cagr:.2f}% / year")
    print(f"Trades Executed:       {total_tr} | Wins: {wins} | Losses: {total_tr - wins} | Win Rate: {wr:.2f}%")
    print(f"Average Duration:      {df_full['duration_hours'].mean():.1f} hours ({df_full['duration_hours'].mean()/24.0:.1f} days)")

    # 2. Bull Market / Non-Bear Projection
    bull_start_ms = int(pd.Timestamp("2023-10-01", tz="UTC").timestamp() * 1000)
    bull_end_ms = int(pd.Timestamp("2024-10-01", tz="UTC").timestamp() * 1000)
    bull_candles = [c for c in candles if c.open_time_ms >= bull_start_ms and c.close_time_ms <= bull_end_ms]

    bull_capital = 1000.0
    bull_active_until = 0
    bull_trades = []
    bull_sigs = run_strategy("ema_cross", bull_candles, direction="long")

    for s in bull_sigs:
        s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(bull_candles) else s.candle_idx
        c_entry = bull_candles[s_idx]
        if c_entry.open_time_ms < bull_active_until:
            continue
        margin = bull_capital
        tr = simulate_single_leg(
            direction="LONG", candles=bull_candles, start_idx=s_idx, entry_px=c_entry.open,
            entry_time_ms=c_entry.open_time_ms, notional=margin, margin_used=margin,
            tp1_pct=5.0, be_buffer_pct=0.06, tp2_pct=5.0, exit_signal_idx=s.exit_signal_idx,
            resolver=None, symbol="NEAR", timeframe="1h", tp_rule="mode_dynamic",
            fee_maker_pct=0.015, fee_taker_pct=0.045, exit_on_signal=False
        )
        bull_capital += tr.net_pnl
        bull_active_until = tr.exit_time_ms
        bull_trades.append({
            "asset": "NEAR",
            "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
            "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
            "entry_price": tr.entry_price,
            "exit_price": tr.exit_price,
            "margin": margin,
            "net_pnl": tr.net_pnl,
            "net_return_pct": tr.net_return_pct,
            "duration_hours": (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0,
            "capital_after": bull_capital,
            "is_win": tr.is_win
        })

    df_bull = pd.DataFrame(bull_trades)
    bull_span = 366.0
    bull_cagr = ((bull_capital / 1000.0) ** (1.0 / (bull_span / 365.25)) - 1.0) * 100.0

    print("\n--- PROJECTED EARNINGS ASSUMING NON-BEAR / BULL CONDITIONS (2023-2024 Bull Rally) ---")
    print(f"Projected 1-Year Bull Capital:  ${bull_capital:,.2f} on $1,000 initial ({((bull_capital-1000)/1000)*100:+.1f}%)")
    print(f"Projected Annual Growth Rate:   {bull_cagr:.2f}% / year")
    print(f"Bull Trades Completed:          {len(df_bull)} (Win Rate: {((df_bull['is_win'].sum()/len(df_bull))*100):.1f}%)")
    print(f"Median Bull Trade Duration:     {df_bull['duration_hours'].median():.1f} hours ({df_bull['duration_hours'].median()/24:.1f} days)")

    # Time Horizon projections based on non-bear daily returns
    daily_idx = pd.date_range(start="2023-10-01", end="2024-10-01", freq="D", tz="UTC")
    df_bull["exit_day"] = df_bull["exit_dt"].dt.floor("D")
    daily_cap = df_bull.groupby("exit_day")["capital_after"].last().reindex(daily_idx).ffill().fillna(1000.0)

    proj_horizons = []
    for h_name, d in [("1 Day", 1), ("1 Week", 7), ("1 Month", 30), ("3 Months", 90), ("6 Months", 180), ("1 Year", 365)]:
        if len(daily_cap) > d:
            diff = daily_cap.diff(d).dropna()
            start = daily_cap.shift(d).dropna()
            pct = (diff / start) * 100.0
            proj_horizons.append({
                "Time Horizon": h_name,
                "Expected Profit ($)": round(diff.mean(), 2),
                "Expected Gain (%)": round(pct.mean(), 2),
                "Median Gain (%)": round(pct.median(), 2),
                "Win Probability (%)": round((diff > 0).mean() * 100.0, 2)
            })
    df_proj = pd.DataFrame(proj_horizons)
    print(df_proj.to_string(index=False))

    # Save CSVs
    csv_c = os.path.join(RESULTS_DIR, "scenario_C.csv")
    csv_proj = os.path.join(RESULTS_DIR, "scenario_C_bull_projection.csv")
    df_full.to_csv(csv_c, index=False)
    df_proj.to_csv(csv_proj, index=False)
    print(f"[✓] Saved Scenario C results to {csv_c} and bull projection to {csv_proj}")

    return df_full, df_proj


# =====================================================================
# SCENARIO D: Zero-Fee Pairs (TRUMP/USDT & DOGE/USDT)
# =====================================================================
def execute_scenario_d() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 90)
    print("💹 SCENARIO D: ZERO-FEE PAIRS (TRUMP/USDT & DOGE/USDT, 2025-08-01 to 2026-09-30)")
    print("=" * 90)

    t0_ms = int(pd.Timestamp("2025-08-01 00:00:00", tz="UTC").timestamp() * 1000)
    t1_ms = int(pd.Timestamp("2026-09-30 23:59:59", tz="UTC").timestamp() * 1000)

    all_trump = load_asset_candles("TRUMP", "1h")
    all_doge = load_asset_candles("DOGE", "1h")

    trump_candles = [c for c in all_trump if c.open_time_ms >= t0_ms and c.close_time_ms <= t1_ms]
    doge_candles = [c for c in all_doge if c.open_time_ms >= t0_ms and c.close_time_ms <= t1_ms]

    def run_zero_fee_sim(candles: List[Candle], sym: str, sizing_fraction: float) -> Tuple[float, List[Dict[str, Any]]]:
        sigs = run_strategy("ema_cross", candles, direction="long")
        cash = 1000.0
        active_until_ms = 0
        trades = []

        for s in sigs:
            s_idx = s.candle_idx + 1 if s.candle_idx + 1 < len(candles) else s.candle_idx
            c = candles[s_idx]
            if c.open_time_ms < active_until_ms:
                continue

            pos_size = cash * sizing_fraction
            if pos_size < 1.0:
                continue

            tr = simulate_single_leg(
                direction="LONG", candles=candles, start_idx=s_idx, entry_px=c.open,
                entry_time_ms=c.open_time_ms, notional=pos_size, margin_used=pos_size,
                tp1_pct=5.0, be_buffer_pct=0.0, tp2_pct=5.0, exit_signal_idx=s.exit_signal_idx,
                resolver=None, symbol=sym, timeframe="1h", tp_rule="mode_dynamic",
                fee_maker_pct=0.0, fee_taker_pct=0.0, exit_on_signal=False
            )
            cash += tr.net_pnl
            active_until_ms = tr.exit_time_ms
            dur_h = (tr.exit_time_ms - tr.entry_time_ms) / 3600000.0

            trades.append({
                "pair": sym,
                "sizing": f"{int(sizing_fraction*100)}%",
                "entry_dt": pd.to_datetime(tr.entry_time_ms, unit="ms", utc=True),
                "exit_dt": pd.to_datetime(tr.exit_time_ms, unit="ms", utc=True),
                "entry_price": tr.entry_price,
                "exit_price": tr.exit_price,
                "margin": pos_size,
                "net_pnl": tr.net_pnl,
                "net_return_pct": tr.net_return_pct,
                "duration_hours": dur_h,
                "capital_after": cash,
                "is_win": tr.is_win,
                "exit_reason": tr.exit_reason
            })
        return cash, trades

    # Sub-scenario 1: 100% Capital
    final_cap_trump_100, trades_trump_100 = run_zero_fee_sim(trump_candles, "TRUMP/USDT", 1.00)
    final_cap_doge_100, trades_doge_100 = run_zero_fee_sim(doge_candles, "DOGE/USDT", 1.00)

    # Sub-scenario 2: 10% Capital
    final_cap_trump_10, trades_trump_10 = run_zero_fee_sim(trump_candles, "TRUMP/USDT", 0.10)
    final_cap_doge_10, trades_doge_10 = run_zero_fee_sim(doge_candles, "DOGE/USDT", 0.10)

    df_d_100 = pd.DataFrame(trades_trump_100 + trades_doge_100)
    df_d_10 = pd.DataFrame(trades_trump_10 + trades_doge_10)

    # Summary table
    d_summary = [
        {
            "Pair": "TRUMP/USDT", "Sizing Mode": "100% Capital", "Period": "2025-08-01 to 2026-09-30",
            "Initial Capital ($)": 1000.0, "Final Capital ($)": round(final_cap_trump_100, 2),
            "Net Profit ($)": round(final_cap_trump_100 - 1000.0, 2), "Net Return (%)": round(((final_cap_trump_100 - 1000)/1000)*100, 2),
            "Trades": len(trades_trump_100), "Win Rate (%)": round((sum(t['is_win'] for t in trades_trump_100)/len(trades_trump_100)*100) if trades_trump_100 else 0, 1),
            "Fees": "0.0% Maker / 0.0% Taker"
        },
        {
            "Pair": "TRUMP/USDT", "Sizing Mode": "10% Capital", "Period": "2025-08-01 to 2026-09-30",
            "Initial Capital ($)": 1000.0, "Final Capital ($)": round(final_cap_trump_10, 2),
            "Net Profit ($)": round(final_cap_trump_10 - 1000.0, 2), "Net Return (%)": round(((final_cap_trump_10 - 1000)/1000)*100, 2),
            "Trades": len(trades_trump_10), "Win Rate (%)": round((sum(t['is_win'] for t in trades_trump_10)/len(trades_trump_10)*100) if trades_trump_10 else 0, 1),
            "Fees": "0.0% Maker / 0.0% Taker"
        },
        {
            "Pair": "DOGE/USDT", "Sizing Mode": "100% Capital", "Period": "2025-08-01 to 2026-09-30",
            "Initial Capital ($)": 1000.0, "Final Capital ($)": round(final_cap_doge_100, 2),
            "Net Profit ($)": round(final_cap_doge_100 - 1000.0, 2), "Net Return (%)": round(((final_cap_doge_100 - 1000)/1000)*100, 2),
            "Trades": len(trades_doge_100), "Win Rate (%)": round((sum(t['is_win'] for t in trades_doge_100)/len(trades_doge_100)*100) if trades_doge_100 else 0, 1),
            "Fees": "0.0% Maker / 0.0% Taker"
        },
        {
            "Pair": "DOGE/USDT", "Sizing Mode": "10% Capital", "Period": "2025-08-01 to 2026-09-30",
            "Initial Capital ($)": 1000.0, "Final Capital ($)": round(final_cap_doge_10, 2),
            "Net Profit ($)": round(final_cap_doge_10 - 1000.0, 2), "Net Return (%)": round(((final_cap_doge_10 - 1000)/1000)*100, 2),
            "Trades": len(trades_doge_10), "Win Rate (%)": round((sum(t['is_win'] for t in trades_doge_10)/len(trades_doge_10)*100) if trades_doge_10 else 0, 1),
            "Fees": "0.0% Maker / 0.0% Taker"
        }
    ]
    df_d_summary = pd.DataFrame(d_summary)
    print(df_d_summary.to_string(index=False))

    # Save CSVs
    csv_d = os.path.join(RESULTS_DIR, "scenario_D.csv")
    csv_d_100 = os.path.join(RESULTS_DIR, "scenario_D_100pct.csv")
    csv_d_10 = os.path.join(RESULTS_DIR, "scenario_D_10pct.csv")
    df_d_summary.to_csv(csv_d, index=False)
    df_d_100.to_csv(csv_d_100, index=False)
    df_d_10.to_csv(csv_d_10, index=False)
    print(f"[✓] Saved Scenario D results to {csv_d}, {csv_d_100}, and {csv_d_10}")

    return df_d_summary, df_d_100, df_d_10


# =====================================================================
# SCENARIO E: 1-Tick Chase on Zero-Fee Pairs (Slippage Sweep 0-7 Ticks)
# =====================================================================
def execute_scenario_e() -> pd.DataFrame:
    print("\n" + "=" * 90)
    print("🎯 SCENARIO E: 1-TICK MOVE CHASING & SLIPPAGE SENSITIVITY (DOGE & TRUMP)")
    print("=" * 90)

    asset_configs = [
        {"name": "TRUMP/USDT", "typical_price": 2.50, "tick_size": 0.0010, "capital": 1000.0},
        {"name": "DOGE/USDT", "typical_price": 0.12, "tick_size": 0.00001, "capital": 1000.0}
    ]

    slippage_levels = [0, 1, 2, 3, 4, 5, 6, 7]
    all_rows = []

    for a in asset_configs:
        sym = a["name"]
        px = a["typical_price"]
        ts = a["tick_size"]
        cap = a["capital"]

        tick_bps = (ts / px) * 10000.0
        tick_pct = (ts / px) * 100.0
        drop_ticks = int((px * 0.05) / ts)

        print(f"\nAsset: {sym} (Reference Price: ${px:.4f} | Tick Size: {ts} | 1 Tick = {tick_bps:.2f} bps / {tick_pct:.4f}%)")
        print(f"5% Drawdown = {drop_ticks:,} ticks adverse drop")
        print("-" * 90)

        pair_rows = []
        for slip in slippage_levels:
            net_ticks = 1 - slip
            net_pct = (net_ticks * ts / px) * 100.0
            net_dollar = cap * (net_pct / 100.0)

            # 3-tick stop loss rule
            tp_ticks_realized = 1 - slip
            sl_ticks_realized = 3 + slip

            if tp_ticks_realized > 0:
                req_win_rate = (sl_ticks_realized / (sl_ticks_realized + tp_ticks_realized)) * 100.0
                winrate_str = f"{req_win_rate:.1f}%"
                req_wr_val = round(req_win_rate, 2)
            elif tp_ticks_realized == 0:
                winrate_str = "100.0% (Zero Edge)"
                req_wr_val = 100.0
            else:
                winrate_str = "Impossible (Negative Edge)"
                req_wr_val = None

            # Consecutive wins required to recover 5% drawdown
            if net_ticks > 0:
                consecutive_wins = int(math.ceil(drop_ticks / net_ticks))
                recovery_str = f"{consecutive_wins:,} wins"
            else:
                consecutive_wins = None
                recovery_str = "Never (Negative Expectancy)"

            row_data = {
                "Asset": sym,
                "Slippage Ticks": slip,
                "Gross Target": "+1 tick",
                "Net Ticks": net_ticks,
                "Net Return (%)": round(net_pct, 4),
                "PnL per $1,000 ($)": round(net_dollar, 4),
                "Breakeven Win Rate (3-Tick SL)": winrate_str,
                "Breakeven Win Rate (%)": req_wr_val,
                "Consecutive Wins to Recover 5% DD": consecutive_wins,
                "Drawdown Recovery": recovery_str
            }
            pair_rows.append(row_data)
            all_rows.append(row_data)

        df_pair = pd.DataFrame(pair_rows)
        print(df_pair[["Slippage Ticks", "Net Ticks", "Net Return (%)", "PnL per $1,000 ($)", "Breakeven Win Rate (3-Tick SL)", "Drawdown Recovery"]].to_string(index=False))

    df_scenario_e = pd.DataFrame(all_rows)

    # Save consolidated CSV
    csv_e = os.path.join(RESULTS_DIR, "scenario_E.csv")
    df_scenario_e.to_csv(csv_e, index=False)
    print(f"\n[✓] Saved consolidated Scenario E results to {csv_e}")

    # Save individual slippage CSVs (e.g. results/scenario_E_slippage_0.csv)
    for slip in slippage_levels:
        df_slip = df_scenario_e[df_scenario_e["Slippage Ticks"] == slip]
        slip_csv = os.path.join(RESULTS_DIR, f"scenario_E_slippage_{slip}.csv")
        df_slip.to_csv(slip_csv, index=False)
        print(f"    - Saved {slip_csv}")

    return df_scenario_e


# =====================================================================
# MASTER WORKFLOW RUNNER
# =====================================================================
def main() -> int:
    t_start = datetime.datetime.now(datetime.timezone.utc)
    print("=" * 90)
    print("🚀 QUANTITATIVE AUTOMATED BACKTEST SUITE STARTING")
    print(f"Timestamp: {t_start.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Workspace Root: {ROOT_DIR}")
    print(f"Results Directory: {RESULTS_DIR}")
    print(f"Log File: {LOG_FILE_PATH}")
    print("=" * 90)

    # 10 Assets for Scenarios A & B
    target_10_assets = ["NEAR", "BTC", "ETH", "SOL", "SUI", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN"]

    try:
        # Run Scenario A
        summary_a, _ = execute_scenario_a(target_10_assets)

        # Run Scenario B
        summary_b, _ = execute_scenario_b(target_10_assets, summary_a)

        # Run Scenario C
        execute_scenario_c()

        # Run Scenario D
        execute_scenario_d()

        # Run Scenario E
        execute_scenario_e()

        t_end = datetime.datetime.now(datetime.timezone.utc)
        elapsed = (t_end - t_start).total_seconds()

        print("\n" + "=" * 90)
        print("✅ ALL 5 BACKTEST SCENARIOS COMPLETED SUCCESSFULLY")
        print(f"Total Execution Time: {elapsed:.2f} seconds")
        print(f"Artifact Output Log:  {LOG_FILE_PATH}")
        print(f"Artifact CSV Folder:  {RESULTS_DIR}/")
        print("=" * 90)
        return 0

    except Exception as e:
        print(f"\n[!] ERROR in backtest execution: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
