import os
import sys
import csv
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

OUT_CSV = os.path.join(ROOT_DIR, "research_agent_phase2", "04_TIME_SEGMENT_RESULTS.csv")

MONTHS = [
    ("2026_01_Jan", "2026-01-01", "2026-01-31"),
    ("2026_02_Feb", "2026-02-01", "2026-02-28"),
    ("2026_03_Mar", "2026-03-01", "2026-03-31"),
    ("2026_04_Apr", "2026-04-01", "2026-04-30"),
    ("2026_05_May", "2026-05-01", "2026-05-31"),
    ("2026_06_Jun", "2026-06-01", "2026-06-30"),
    ("2026_07_Jul", "2026-07-01", "2026-07-31"),
    ("2026_08_Aug", "2026-08-01", "2026-08-31"),
]

SL_CHOICES = [2, 3, 4, 5, 6, 7, 10]

def run_single_task(task):
    seg_name, start_d, end_d, sl = task
    t0 = time.time()
    try:
        m, _ = run_backtest_direct(
            symbol="TRUMP_USDT",
            timeframe="1m",
            strategy_mode="STOCH_RSI",
            stoch_preset="FAST_SCALP",
            start_time=start_d,
            end_time=end_d,
            tp_ticks=2,
            sl_mode="TICKS",
            sl_ticks=sl,
            use_tick_data=True
        )
        sim_t = time.time() - t0
        return {
            "segment_name": seg_name,
            "start_date": start_d,
            "end_date": end_d,
            "SL_ticks": sl,
            "TP_ticks": 2,
            "trade_count": m["total_trades"],
            "win_rate_pct": f"{m['win_rate_pct']:.4f}",
            "profit_factor": f"{m['profit_factor']:.4f}",
            "net_pnl_usdt": f"{m['net_pnl_usdt']:.6f}",
            "max_drawdown_pct": f"{m['max_drawdown_pct']:.4f}",
            "avg_win_usdt": f"{m['avg_win_pnl_usdt']:.6f}",
            "avg_loss_usdt": f"{m['avg_loss_pnl_usdt']:.6f}",
            "avg_duration_seconds": f"{m['avg_duration_seconds']:.2f}",
            "long_win_rate_pct": f"{m['long_win_rate_pct']:.2f}",
            "short_win_rate_pct": f"{m['short_win_rate_pct']:.2f}",
            "sim_time_sec": f"{sim_t:.2f}"
        }
    except Exception as e:
        print(f"Error on {seg_name} SL={sl}: {e}")
        return None

def main():
    print("=== STARTING TIME-SEGMENT GENERALIZATION (8 Months x 7 SLs = 56 runs) ===")
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    
    tasks = []
    for seg_name, s_d, e_d in MONTHS:
        for sl in SL_CHOICES:
            tasks.append((seg_name, s_d, e_d, sl))
            
    fields = [
        "segment_name", "start_date", "end_date", "SL_ticks", "TP_ticks",
        "trade_count", "win_rate_pct", "profit_factor", "net_pnl_usdt",
        "max_drawdown_pct", "avg_win_usdt", "avg_loss_usdt",
        "avg_duration_seconds", "long_win_rate_pct", "short_win_rate_pct", "sim_time_sec"
    ]
    
    results = []
    # Use 3 workers to prevent CPU exhaustion while maximizing throughput
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_single_task, t): t for t in tasks}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.append(res)
                print(f"[{len(results)}/56] {res['segment_name']} | SL={res['SL_ticks']}t | Trades={res['trade_count']} | WR={res['win_rate_pct']}% | PF={res['profit_factor']} | PnL={res['net_pnl_usdt']}")
                # Sort by month and SL before saving
                def sort_key(r):
                    return (r["start_date"], int(r["SL_ticks"]))
                sorted_res = sorted(results, key=sort_key)
                with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(sorted_res)
                    
    print(f"\nCompleted all {len(results)} runs. Saved to {OUT_CSV}")

if __name__ == "__main__":
    main()
