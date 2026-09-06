import os
import sys
import csv
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

OUT_CSV = os.path.join(ROOT_DIR, "research_agent_phase2", "05_PAIR_RESULTS.csv")

PERIODS = [
    ("2026-07-01", "2026-08-31", "Jul-Aug 2026"),
    ("2026-01-01", "2026-02-28", "Jan-Feb 2026")
]

PAIRS = ["TRUMP_USDT", "DOGE_USDT"]
SL_CHOICES = [2, 3, 4, 5, 6, 7, 10]

def run_single(task):
    symbol, start_d, end_d, period_label, sl = task
    t0 = time.time()
    try:
        # Use tick data for TRUMP on Jul-Aug where tick files exist; otherwise candle fallback
        use_ticks = (symbol == "TRUMP_USDT" and "2026-07" in start_d)
        m, _ = run_backtest_direct(
            symbol=symbol,
            timeframe="1m",
            strategy_mode="STOCH_RSI",
            stoch_preset="FAST_SCALP",
            start_time=start_d,
            end_time=end_d,
            tp_ticks=2,
            sl_mode="TICKS",
            sl_ticks=sl,
            use_tick_data=use_ticks
        )
        sim_t = time.time() - t0
        return {
            "symbol": symbol,
            "period_label": period_label,
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
            "sim_time_sec": f"{sim_t:.2f}"
        }
    except Exception as e:
        print(f"Error on {symbol} {period_label} SL={sl}: {e}")
        return None

def main():
    print("=== STARTING CROSS-PAIR VALIDATION BATTERY (TRUMP vs DOGE) ===")
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    
    tasks = []
    for s_d, e_d, p_lbl in PERIODS:
        for sym in PAIRS:
            for sl in SL_CHOICES:
                tasks.append((sym, s_d, e_d, p_lbl, sl))
                
    fields = [
        "symbol", "period_label", "start_date", "end_date", "SL_ticks", "TP_ticks",
        "trade_count", "win_rate_pct", "profit_factor", "net_pnl_usdt",
        "max_drawdown_pct", "avg_win_usdt", "avg_loss_usdt", "avg_duration_seconds", "sim_time_sec"
    ]
    
    results = []
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_single, t): t for t in tasks}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.append(res)
                print(f"[{len(results)}/{len(tasks)}] {res['symbol']:<10} | {res['period_label']:<12} | SL={res['SL_ticks']:2d}t | Trades={res['trade_count']:5d} | WR={res['win_rate_pct']:>7}% | PF={res['profit_factor']:>5} | PnL={res['net_pnl_usdt']}")
                
                def sort_key(r):
                    return (r["symbol"], r["start_date"], int(r["SL_ticks"]))
                sorted_res = sorted(results, key=sort_key)
                with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(sorted_res)

    print(f"\nSaved {len(results)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()
