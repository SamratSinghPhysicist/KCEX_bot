import os
import sys
import csv
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

OUT_CSV = os.path.join(ROOT_DIR, "research_agent_phase2", "06_DIRECTION_RESULTS.csv")

DIRECTIONS = ["BOTH", "LONG_ONLY", "SHORT_ONLY"]
STRATEGIES = ["STOCH_RSI", "EMA_CROSSOVER"]
SL_CHOICES = [2, 3, 4, 5, 6, 7, 10]

def run_single(task):
    strat, direction, sl = task
    t0 = time.time()
    try:
        m, _ = run_backtest_direct(
            symbol="TRUMP_USDT",
            timeframe="1m",
            strategy_mode=strat,
            stoch_preset="FAST_SCALP",
            ema_preset="5/13",
            start_time="2026-07-01",
            end_time="2026-07-24",
            tp_ticks=2,
            sl_mode="TICKS",
            sl_ticks=sl,
            direction_bias=direction,
            use_tick_data=True
        )
        sim_t = time.time() - t0
        return {
            "strategy": strat,
            "direction": direction,
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
            "sim_time_sec": f"{sim_t:.2f}"
        }
    except Exception as e:
        print(f"Error on {strat} {direction} SL={sl}: {e}")
        return None

def main():
    print("=== RUNNING DIRECTIONAL & STRATEGY INDEPENDENCE BATTERY ===")
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    
    tasks = []
    for strat in STRATEGIES:
        for d in DIRECTIONS:
            for sl in SL_CHOICES:
                tasks.append((strat, d, sl))
                
    fields = [
        "strategy", "direction", "SL_ticks", "TP_ticks", "trade_count",
        "win_rate_pct", "profit_factor", "net_pnl_usdt", "max_drawdown_pct",
        "avg_win_usdt", "avg_loss_usdt", "avg_duration_seconds", "sim_time_sec"
    ]
    
    results = []
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_single, t): t for t in tasks}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.append(res)
                print(f"[{len(results)}/{len(tasks)}] {res['strategy']} | {res['direction']:<10} | SL={res['SL_ticks']:2d}t | Trades={res['trade_count']:4d} | WR={res['win_rate_pct']:>7}% | PF={res['profit_factor']:>5} | PnL={res['net_pnl_usdt']}")
                
                # Sort before saving
                def sort_key(r):
                    return (r["strategy"], r["direction"], int(r["SL_ticks"]))
                sorted_res = sorted(results, key=sort_key)
                with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(sorted_res)

    print(f"\nSaved {len(results)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()
