import os, sys, time
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

t0 = time.time()
m, outcomes = run_backtest_direct(
    symbol="TRUMP_USDT",
    timeframe="1m",
    strategy_mode="STOCH_RSI",
    stoch_preset="FAST_SCALP",
    start_time="2026-01-01",
    end_time="2026-01-31",
    tp_ticks=2,
    sl_mode="TICKS",
    sl_ticks=5,
    use_tick_data=False
)
t_el = time.time() - t0
print(f"TRUMP Jan 2026: Trades={m['total_trades']}, WR={m['win_rate_pct']:.2f}%, PF={m['profit_factor']:.2f}, PnL={m['net_pnl_usdt']:.4f}, DD={m['max_drawdown_pct']:.2f}%, Time={t_el:.2f}s")
