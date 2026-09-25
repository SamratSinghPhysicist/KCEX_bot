"""
Local High-Throughput Matrix Backtest Orchestrator
==================================================
Parallelizes the execution of the 100 (pair x timeframe) matrix runs across
multiple concurrent local worker processes. Gathers all JSON and CSV artifacts,
then triggers the aggregator script to produce consolidated rankings and reports.
"""

from __future__ import annotations
import os
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any

# Ensure utf-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

ALL_TARGET_PAIRS = [
    # 14 Shortlisted KCEX Pairs
    "MELANIA_USDT",
    "DOGS_USDT",
    "MEME_USDT",
    "BOME_USDT",
    "ACT_USDT",
    "AVAAI_USDT",
    "MOG_USDT",
    "CHILLGUY_USDT",
    "GOAT_USDT",
    "PIPPIN_USDT",
    "WIF_USDT",
    "KOMA_USDT",
    "TRUMP_USDT",
    "AIXBT_USDT",
    # 6 High-Cap & Layer-1 / DeFi Pairs
    "XRP_USDT",
    "XMR_USDT",
    "AVAX_USDT",
    "TRX_USDT",
    "HYPE_USDT",
    "LTC_USDT"
]

ALL_TIMEFRAMES = ["5m", "15m", "1h", "4h", "1d"]


def execute_worker(task: Tuple[str, str, int, str]) -> Dict[str, Any]:
    """Spawns an isolated Python worker process for one (pair, timeframe) run."""
    pair, tf, months, artifacts_dir = task
    cmd = [
        sys.executable,
        os.path.join(SCRIPT_DIR, "run_single_backtest.py"),
        "--pair", pair,
        "--timeframe", tf,
        "--months", str(months),
        "--leverage", "15",
        "--margin-pct", "10.0",
        "--capital", "100.0",
        "--strategy", "ORDER_BLOCK_DEMAND",
        "--output-dir", artifacts_dir
    ]

    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=ROOT_DIR
        )
        elapsed = time.time() - t0
        success = (proc.returncode == 0)
        
        # Check if json was generated
        json_file = os.path.join(artifacts_dir, f"results_{pair}_{tf}.json")
        roi = None
        wr = None
        pf = None
        trades = None
        if os.path.exists(json_file):
            import json
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    m = data.get("metrics", {})
                    roi = m.get("total_roi_pct")
                    wr = m.get("win_rate_pct")
                    pf = m.get("profit_factor")
                    trades = m.get("total_trades")
            except Exception:
                pass

        return {
            "pair": pair,
            "timeframe": tf,
            "success": success,
            "elapsed": elapsed,
            "roi": roi,
            "wr": wr,
            "pf": pf,
            "trades": trades,
            "output": proc.stdout
        }
    except Exception as e:
        return {
            "pair": pair,
            "timeframe": tf,
            "success": False,
            "elapsed": time.time() - t0,
            "error": str(e)
        }


def run_matrix_pool(
    pairs: List[str] = ALL_TARGET_PAIRS,
    timeframes: List[str] = ALL_TIMEFRAMES,
    months: int = 6,
    max_workers: int = 4,
    artifacts_dir: str = "local_matrix_artifacts",
    reports_dir: str = "final_matrix_reports"
):
    os.makedirs(artifacts_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    tasks: List[Tuple[str, str, int, str]] = []
    for p in pairs:
        for tf in timeframes:
            tasks.append((p, tf, months, artifacts_dir))

    total_tasks = len(tasks)
    print("\n" + "=" * 80)
    print("🚀 HIGH-THROUGHPUT DISTRIBUTED MATRIX BACKTEST RUNNER (LOCAL)")
    print("=" * 80)
    print(f"Total Configurations:  {total_tasks} ({len(pairs)} pairs x {len(timeframes)} timeframes)")
    print(f"Concurrent Workers:    {max_workers} processes")
    print(f"Historical Lookback:   {months} months")
    print(f"Strategy:              Order Book + Demand Block (SMC 1:2 RR @ 15x)")
    print(f"Compounding Sizing:    10.0% Available Equity")
    print(f"Artifacts Directory:   {artifacts_dir}")
    print(f"Reports Directory:     {reports_dir}")
    print("=" * 80 + "\n")

    start_all = time.time()
    completed_count = 0
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(execute_worker, t): t for t in tasks}

        for future in as_completed(futures):
            res = future.result()
            completed_count += 1
            p = res["pair"]
            tf = res["timeframe"]
            el = res["elapsed"]

            if res.get("success"):
                success_count += 1
                roi_str = f"{res['roi']:+.2f}%" if res.get("roi") is not None else "N/A"
                wr_str = f"{res['wr']:.1f}%" if res.get("wr") is not None else "N/A"
                pf_str = f"{res['pf']:.2f}" if res.get("pf") is not None else "N/A"
                tr_str = f"{res['trades']}" if res.get("trades") is not None else "N/A"
                print(f"[{completed_count:03d}/{total_tasks:03d}] ✅ {p:16s} [{tf:3s}] in {el:5.1f}s | Trades: {tr_str:>3s} | WR: {wr_str:>6s} | PF: {pf_str:>5s} | ROI: {roi_str:>8s}")
            else:
                print(f"[{completed_count:03d}/{total_tasks:03d}] ❌ {p:16s} [{tf:3s}] in {el:5.1f}s | FAILED")
                if "output" in res and res["output"]:
                    last_lines = "\n".join(res["output"].strip().splitlines()[-4:])
                    print(f"      Tail error: {last_lines}")

    total_time = time.time() - start_all
    print("\n" + "=" * 80)
    print(f"🏁 ALL WORKERS COMPLETED: {success_count}/{total_tasks} successful in {total_time/60:.2f} minutes")
    print("=" * 80 + "\n")

    # Run Aggregator
    print("[*] Running Consolidated Analytics & Report Generator...")
    aggregator_script = os.path.join(SCRIPT_DIR, "aggregate_backtest_results.py")
    cmd = [
        sys.executable,
        aggregator_script,
        "--results-dir", artifacts_dir,
        "--output-dir", reports_dir
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Full Backtest Matrix Locally")
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker processes (default: 4)")
    parser.add_argument("--months", type=int, default=6, help="Lookback months (default: 6)")
    parser.add_argument("--pairs", type=str, default="ALL", help="Comma-separated pairs or ALL")
    parser.add_argument("--timeframes", type=str, default="ALL", help="Comma-separated timeframes or ALL")
    parser.add_argument("--artifacts-dir", type=str, default="local_matrix_artifacts", help="Artifacts directory")
    parser.add_argument("--reports-dir", type=str, default="final_matrix_reports", help="Reports directory")

    args = parser.parse_args()

    target_pairs = ALL_TARGET_PAIRS
    if args.pairs != "ALL" and args.pairs != "all":
        req = [x.strip() for x in args.pairs.split(",") if x.strip()]
        target_pairs = [p for p in ALL_TARGET_PAIRS if any(r in p for r in req)]

    target_tfs = ALL_TIMEFRAMES
    if args.timeframes != "ALL" and args.timeframes != "all":
        req_tf = [x.strip() for x in args.timeframes.split(",") if x.strip()]
        target_tfs = [t for t in ALL_TIMEFRAMES if t in req_tf]

    run_matrix_pool(
        pairs=target_pairs,
        timeframes=target_tfs,
        months=args.months,
        max_workers=args.workers,
        artifacts_dir=args.artifacts_dir,
        reports_dir=args.reports_dir
    )
