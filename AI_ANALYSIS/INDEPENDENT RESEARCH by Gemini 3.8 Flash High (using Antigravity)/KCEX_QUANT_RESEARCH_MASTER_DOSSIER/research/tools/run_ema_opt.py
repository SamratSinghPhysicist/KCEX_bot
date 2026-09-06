import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct, log_experiment, EXPERIMENTS_DIR

exp_id = "EXP_0038"
exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)

metrics, outcomes = run_backtest_direct(
    symbol="TRUMP_USDT",
    timeframe="1m",
    strategy_mode="EMA_CROSSOVER",
    ema_preset="5/13",
    start_time="2026-07-01",
    end_time="2026-07-24",
    tp_ticks=2,
    sl_mode="TICKS",
    sl_ticks=5,
    save_reports=True,
    exp_dir=exp_dir
)

trades = metrics["total_trades"]
wr = metrics["win_rate_pct"]
pf = metrics["profit_factor"]
pnl = metrics["net_pnl_usdt"]
dd = metrics["max_drawdown_pct"]

rw_prob = (5.0 / 7.0) * 100.0
delta_p = wr - rw_prob

print(f"EXP_0038 (EMA_CROSSOVER TP=2/SL=5) | Trades: {trades} | WR: {wr:.2f}% (RW: {rw_prob:.1f}%, Delta: {delta_p:+.2f}%) | PF: {pf:.2f} | PnL: {pnl:+.4f} | DD: {dd:.2f}%")

log_experiment({
    "experiment_id": exp_id,
    "date": "2026-09-06",
    "hypothesis": "Test whether optimal geometry (SL=5t) improves EMA_CROSSOVER similarly.",
    "motivation": "Compare STOCH_RSI vs EMA_CROSSOVER under identical optimal TP/SL geometry.",
    "baseline": "EXP_0002",
    "code_changes": "EMA_CROSSOVER with SL=5t",
    "parameters": "strat=EMA_CROSSOVER,tp=2,sl_mode=TICKS,sl_ticks=5",
    "symbol": "TRUMP_USDT",
    "strategy": "EMA_CROSSOVER",
    "training_period": "2026-07-01 to 2026-07-24",
    "validation_period": "2026-07-25 to 2026-08-15",
    "test_period": "2026-08-16 to 2026-08-31",
    "backtest_command": "python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy EMA_CROSSOVER --start 2026-07-01 --end 2026-07-24 --tp-ticks 2 --sl-ticks 5",
    "result": "INCONCLUSIVE",
    "PnL": pnl,
    "trade_count": trades,
    "win_rate": wr,
    "profit_factor": pf,
    "drawdown": dd,
    "interpretation": f"Trades: {trades}, WR: {wr:.2f}% (Delta: {delta_p:+.2f}%), PF: {pf:.2f}, PnL: {pnl:+.4f}, DD: {dd:.2f}%",
    "decision": "INCONCLUSIVE",
    "next_action": "Compare against STOCH_RSI"
})
