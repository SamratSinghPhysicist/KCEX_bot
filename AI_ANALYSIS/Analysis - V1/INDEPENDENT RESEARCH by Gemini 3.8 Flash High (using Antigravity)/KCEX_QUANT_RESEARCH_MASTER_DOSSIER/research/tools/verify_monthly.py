import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from research.tools.experiment_suite import run_backtest_direct

months = [
    ("Jan", "2026-01-01", "2026-01-31"),
    ("Feb", "2026-02-01", "2026-02-28"),
    ("Mar", "2026-03-01", "2026-03-31")
]

for m_name, s_d, e_d in months:
    m, _ = run_backtest_direct(
        symbol="TRUMP_USDT",
        start_time=s_d,
        end_time=e_d,
        tp_ticks=2,
        sl_mode="TICKS",
        sl_ticks=5,
        use_tick_data=False
    )
    print(f"{m_name}: Trades={m['total_trades']}, WR={m['win_rate_pct']:.2f}%, PF={m['profit_factor']:.2f}, PnL={m['net_pnl_usdt']:.4f}, DD={m['max_drawdown_pct']:.2f}%")
