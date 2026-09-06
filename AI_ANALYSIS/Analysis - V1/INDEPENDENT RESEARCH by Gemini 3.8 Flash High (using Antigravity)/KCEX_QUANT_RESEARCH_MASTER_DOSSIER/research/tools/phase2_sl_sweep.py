import os
import sys
import csv
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

OUT_CSV = os.path.join(ROOT_DIR, "research_agent_phase2", "03_SL_SWEEP_RESULTS.csv")

def run_sl_sweep():
    print("=== RUNNING FULL SL SWEEP: SL in [1..15] ticks, TP = 2 ticks ===")
    
    sl_values = list(range(1, 16))
    results = []
    
    fields = [
        "SL_ticks",
        "TP_ticks",
        "trade_count",
        "win_count",
        "loss_count",
        "win_rate_pct",
        "theoretical_rw_wr_pct",
        "delta_wr_pct",
        "avg_win_usdt",
        "avg_loss_usdt",
        "profit_factor",
        "net_pnl_usdt",
        "pnl_per_trade_usdt",
        "max_drawdown_pct",
        "avg_duration_seconds",
        "sim_time_sec"
    ]
    
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    
    for sl in sl_values:
        t0 = time.time()
        m, outcomes = run_backtest_direct(
            symbol="TRUMP_USDT",
            timeframe="1m",
            strategy_mode="STOCH_RSI",
            stoch_preset="FAST_SCALP",
            start_time="2026-07-01",
            end_time="2026-07-24",
            tp_ticks=2,
            sl_mode="TICKS",
            sl_ticks=sl,
            use_tick_data=True
        )
        sim_t = time.time() - t0
        
        tc = m["total_trades"]
        wc = m["winning_trades"]
        lc = m["losing_trades"]
        wr = m["win_rate_pct"]
        rw_wr = (sl / (2.0 + sl)) * 100.0
        delta_wr = wr - rw_wr
        pf = m["profit_factor"]
        pnl = m["net_pnl_usdt"]
        pnl_per_trade = pnl / tc if tc > 0 else 0.0
        dd = m["max_drawdown_pct"]
        avg_win = m["avg_win_pnl_usdt"]
        avg_loss = m["avg_loss_pnl_usdt"]
        dur = m["avg_duration_seconds"]
        
        row = {
            "SL_ticks": sl,
            "TP_ticks": 2,
            "trade_count": tc,
            "win_count": wc,
            "loss_count": lc,
            "win_rate_pct": f"{wr:.4f}",
            "theoretical_rw_wr_pct": f"{rw_wr:.4f}",
            "delta_wr_pct": f"{delta_wr:.4f}",
            "avg_win_usdt": f"{avg_win:.6f}",
            "avg_loss_usdt": f"{avg_loss:.6f}",
            "profit_factor": f"{pf:.4f}",
            "net_pnl_usdt": f"{pnl:.6f}",
            "pnl_per_trade_usdt": f"{pnl_per_trade:.6f}",
            "max_drawdown_pct": f"{dd:.4f}",
            "avg_duration_seconds": f"{dur:.2f}",
            "sim_time_sec": f"{sim_t:.2f}"
        }
        results.append(row)
        print(f"SL={sl:2d}t | Trades={tc:4d} | WR={wr:6.2f}% (RW: {rw_wr:5.2f}%, dWR: {delta_wr:+5.2f}%) | PF={pf:5.2f} | PnL={pnl:+8.4f} | DD={dd:5.2f}% | Time={sim_t:4.1f}s")
        
        # Write incrementally so progress is preserved
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(results)

    print(f"\nSaved {len(results)} rows to {OUT_CSV}")

if __name__ == "__main__":
    run_sl_sweep()
