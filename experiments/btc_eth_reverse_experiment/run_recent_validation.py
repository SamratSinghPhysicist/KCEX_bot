"""
Recent Out-of-Sample Backtest Validation (Sep 2026 & Oct 1-12, 2026)
===================================================================
Tests Case 1: Long BTC / Short ETH
Configuration: TP = 1.50%, SL = 3.00%, Leverage: 2x
Timeframes: 1h, 4h (also 15m, 1d)
Periods:
- Period 1: 2026-09-01 to 2026-09-30 (September 2026)
- Period 2: 2026-10-01 to 2026-10-12 (October 1 to October 12, 2026)
- Combined: 2026-09-01 to 2026-10-12
"""

from __future__ import annotations
import os
import sys
import io
import csv
import zipfile
import urllib.request
import datetime
from typing import List, Dict, Any, Optional

# Ensure utf-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    CandleData,
    TP_SL_Config,
    load_candles_from_dir,
    build_sub_1m_map,
    run_dual_account_simulation,
    parse_date_to_ms,
    format_ms
)

BINANCE_MONTHLY_URL = "https://data.binance.vision/data/futures/um/monthly/klines"
BINANCE_DAILY_URL = "https://data.binance.vision/data/futures/um/daily/klines"


def download_recent_data(
    symbols: List[str] = ["BTCUSDT", "ETHUSDT"],
    timeframes: List[str] = ["1m", "15m", "1h", "4h", "1d"],
    base_dir: str = "BACKTESTER/OHLCV_Data_Binance"
):
    """Downloads September 2026 monthly archive and October 1-12 daily archives."""
    if not os.path.isabs(base_dir):
        base_dir = os.path.join(ROOT_DIR, base_dir)

    for sym in symbols:
        for tf in timeframes:
            dest_dir = os.path.join(base_dir, sym, tf)
            os.makedirs(dest_dir, exist_ok=True)

            # 1. Download September 2026 monthly
            sep_csv = f"{sym}-{tf}-2026-09.csv"
            sep_path = os.path.join(dest_dir, sep_csv)
            if not os.path.exists(sep_path) or os.path.getsize(sep_path) < 100:
                sep_url = f"{BINANCE_MONTHLY_URL}/{sym}/{tf}/{sym}-{tf}-2026-09.zip"
                try:
                    req = urllib.request.Request(sep_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        z_data = resp.read()
                    with zipfile.ZipFile(io.BytesIO(z_data)) as zf:
                        zf.extractall(dest_dir)
                    print(f"[+] Downloaded {sep_csv}")
                except Exception as e:
                    print(f"[!] Error downloading {sep_url}: {e}")

            # 2. Download October 1-12 daily files
            for d in range(1, 13):
                d_str = f"2026-10-{d:02d}"
                oct_csv = f"{sym}-{tf}-{d_str}.csv"
                oct_path = os.path.join(dest_dir, oct_csv)
                if not os.path.exists(oct_path) or os.path.getsize(oct_path) < 100:
                    oct_url = f"{BINANCE_DAILY_URL}/{sym}/{tf}/{sym}-{tf}-{d_str}.zip"
                    try:
                        req = urllib.request.Request(oct_url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=15) as resp:
                            z_data = resp.read()
                        with zipfile.ZipFile(io.BytesIO(z_data)) as zf:
                            zf.extractall(dest_dir)
                        print(f"[+] Downloaded {oct_csv}")
                    except Exception as e:
                        print(f"[!] Error downloading {oct_url}: {e}")


def run_period_backtest(
    period_name: str,
    start_date: str,
    end_date: str,
    timeframes: List[str] = ["1h", "4h"],
    tp_pct: float = 1.5,
    sl_pct: float = 3.0,
    capital: float = 1000.0,
    leverage: float = 2.0,
    fee_rate: float = 0.0004,
    base_dir: str = "BACKTESTER/OHLCV_Data_Binance"
) -> Dict[str, Any]:
    """Runs backtest for a specific period on requested timeframes."""
    if not os.path.isabs(base_dir):
        base_dir = os.path.join(ROOT_DIR, base_dir)

    start_ms = parse_date_to_ms(start_date)
    end_ms = parse_date_to_ms(end_date) + (24 * 3600 * 1000 - 1)

    print(f"\n{'='*75}")
    print(f"📊 BACKTEST PERIOD: {period_name} ({start_date} to {end_date})")
    print(f"   Strategy: Long BTC / Short ETH (Case 1)")
    print(f"   Config:   TP {tp_pct}% / SL {sl_pct}% | Leverage: {leverage}x | Sizing: 100% Capital")
    print(f"{'='*75}")

    # Load 1m candles for dispute resolution
    btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
    eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)

    cfg = TP_SL_Config(name=f"TP{tp_pct}_SL{sl_pct}", tp_pct=tp_pct, sl_pct=sl_pct, description="")

    results = {}

    for tf in timeframes:
        btc_c = load_candles_from_dir("BTCUSDT", tf, base_dir, start_ms, end_ms)
        eth_c = load_candles_from_dir("ETHUSDT", tf, base_dir, start_ms, end_ms)

        btc_sub_map = build_sub_1m_map(btc_c, btc_1m)
        eth_sub_map = build_sub_1m_map(eth_c, eth_1m)

        cycles, perf_a, perf_b = run_dual_account_simulation(
            btc_candles=btc_c,
            eth_candles=eth_c,
            btc_sub_1m=btc_sub_map,
            eth_sub_1m=eth_sub_map,
            case_name="Case 1",
            timeframe=tf,
            config=cfg,
            initial_balance_each=capital,
            leverage=leverage,
            fee_rate=fee_rate
        )

        # Calculate exact co-occurrences
        both_win = 0
        only_btc = 0
        only_eth = 0
        both_lose = 0

        for cy in cycles:
            b_win = cy.btc_trade.is_win
            e_win = cy.eth_trade.is_win
            if b_win and e_win:
                both_win += 1
            elif b_win and not e_win:
                only_btc += 1
            elif not b_win and e_win:
                only_eth += 1
            else:
                both_lose += 1

        tot_cycles = len(cycles)
        p_at_least = ((tot_cycles - both_lose) / tot_cycles * 100.0) if tot_cycles > 0 else 0.0

        comb_init = capital * 2
        comb_final = perf_a.final_balance + perf_b.final_balance
        comb_pnl = comb_final - comb_init
        comb_roi = (comb_pnl / comb_init * 100.0)

        results[tf] = {
            "total_cycles": tot_cycles,
            "p_at_least_one_wins": p_at_least,
            "both_win": both_win,
            "only_btc_win": only_btc,
            "only_eth_win": only_eth,
            "both_lose": both_lose,
            "perf_a": perf_a,
            "perf_b": perf_b,
            "comb_final": comb_final,
            "comb_pnl": comb_pnl,
            "comb_roi": comb_roi,
            "cycles": cycles
        }

        print(f"\n--- TIMEFRAME: {tf.upper()} ---")
        print(f"Total Completed Cycles: {tot_cycles}")
        print(f"P(At least 1 wins):     {p_at_least:.2f}% ({tot_cycles - both_lose}/{tot_cycles})")
        print(f"  ├─ BOTH Win:          {both_win} ({(both_win/tot_cycles*100) if tot_cycles else 0:.1f}%)")
        print(f"  ├─ Only BTC Wins:     {only_btc} ({(only_btc/tot_cycles*100) if tot_cycles else 0:.1f}%)")
        print(f"  └─ Only ETH Wins:     {only_eth} ({(only_eth/tot_cycles*100) if tot_cycles else 0:.1f}%)")
        print(f"  ❌ BOTH Lose:         {both_lose} ({(both_lose/tot_cycles*100) if tot_cycles else 0:.1f}%)")
        print(f"Account A (BTC Long):   Final: ${perf_a.final_balance:.2f} | Net: ${perf_a.net_pnl:+,.2f} ({perf_a.net_roi_pct:+.1f}%) | WinRate: {perf_a.win_rate_pct:.1f}% ({perf_a.winning_trades}W/{perf_a.losing_trades}L)")
        print(f"Account B (ETH Short):  Final: ${perf_b.final_balance:.2f} | Net: ${perf_b.net_pnl:+,.2f} ({perf_b.net_roi_pct:+.1f}%) | WinRate: {perf_b.win_rate_pct:.1f}% ({perf_b.winning_trades}W/{perf_b.losing_trades}L)")
        print(f"Combined Portfolio:     Final: ${comb_final:.2f} | Net: ${comb_pnl:+,.2f} ({comb_roi:+.1f}%)")

        # Print trade-by-trade breakdown
        print("\n  Trade Log Breakdown:")
        for cy in cycles:
            b_r = cy.btc_trade.exit_reason
            e_r = cy.eth_trade.exit_reason
            b_pnl = cy.btc_trade.net_pnl
            e_pnl = cy.eth_trade.net_pnl
            print(f"    Cycle #{cy.cycle_id:02d} [{cy.entry_time_iso[5:16]}]: BTC {b_r} (${b_pnl:+.1f}) | ETH {e_r} (${e_pnl:+.1f}) | Free: {cy.cycle_exit_time_iso[5:16]} ({cy.holding_candles} candles)")

    return results


if __name__ == "__main__":
    print("[*] Downloading recent September & October 2026 market data...")
    download_recent_data()

    # Period 1: September 2026
    res_sep = run_period_backtest(
        period_name="September 2026",
        start_date="2026-09-01",
        end_date="2026-09-30",
        timeframes=["1h", "4h"]
    )

    # Period 2: October 1 to 12, 2026
    res_oct = run_period_backtest(
        period_name="October 1-12, 2026",
        start_date="2026-10-01",
        end_date="2026-10-12",
        timeframes=["1h", "4h"]
    )

    # Combined Period: Sep 1 to Oct 12, 2026
    res_comb = run_period_backtest(
        period_name="September 1 - October 12, 2026",
        start_date="2026-09-01",
        end_date="2026-10-12",
        timeframes=["1h", "4h"]
    )
