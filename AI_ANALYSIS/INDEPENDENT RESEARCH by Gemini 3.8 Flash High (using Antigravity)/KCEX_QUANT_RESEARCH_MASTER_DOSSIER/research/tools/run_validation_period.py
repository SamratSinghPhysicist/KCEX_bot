import os
import sys
import json
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct, log_experiment, EXPERIMENTS_DIR

VAL_START = "2026-07-25"
VAL_END = "2026-08-15"

validation_runs = [
    {
        "id": "EXP_0039",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "ROE",
        "sl_roe": 25.0,
        "sl_ticks": None,
        "name": "VALIDATION: Baseline STOCH_RSI (TP=2, SL=25% ROE)",
        "desc": "Baseline STOCH_RSI tested on untouched validation period."
    },
    {
        "id": "EXP_0040",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 5,
        "name": "VALIDATION: Candidate STOCH_RSI (TP=2, SL=5t)",
        "desc": "Optimal geometry candidate tested on untouched validation period."
    },
    {
        "id": "EXP_0041",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 2,
        "name": "VALIDATION: Symmetric STOCH_RSI (TP=2, SL=2t)",
        "desc": "Symmetric 1:1 test on untouched validation period."
    },
    {
        "id": "EXP_0042",
        "strategy": "EMA_CROSSOVER",
        "tp": 2,
        "sl_mode": "ROE",
        "sl_roe": 25.0,
        "sl_ticks": None,
        "name": "VALIDATION: Baseline EMA (TP=2, SL=25% ROE)",
        "desc": "Baseline EMA tested on untouched validation period."
    },
    {
        "id": "EXP_0043",
        "strategy": "EMA_CROSSOVER",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 5,
        "name": "VALIDATION: Candidate EMA (TP=2, SL=5t)",
        "desc": "Candidate EMA tested on untouched validation period."
    }
]

print(f"================ Starting Validation Period Runs ({VAL_START} to {VAL_END}) ================")
print(f"{'Exp ID':<10} | {'Name':<35} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 96)

for v in validation_runs:
    exp_id = v["id"]
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode=v["strategy"],
        stoch_preset="FAST_SCALP",
        ema_preset="5/13",
        start_time=VAL_START,
        end_time=VAL_END,
        tp_ticks=v["tp"],
        sl_mode=v["sl_mode"],
        sl_roe_pct=v["sl_roe"],
        sl_ticks=v["sl_ticks"],
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"{exp_id:<10} | {v['name']:<35} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "VALIDATED" if pnl > 0.10 and pf > 1.15 else ("REJECTED" if pnl <= 0 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Validation test on untouched period {VAL_START} to {VAL_END} to verify stability.",
        "motivation": v["desc"],
        "baseline": "DISCOVERY_RUNS",
        "code_changes": f"Run on validation period: {v['name']}",
        "parameters": f"strat={v['strategy']},tp={v['tp']},sl_mode={v['sl_mode']},sl_ticks={v['sl_ticks']}",
        "symbol": "TRUMP_USDT",
        "strategy": v["strategy"],
        "training_period": "2026-07-01 to 2026-07-24",
        "validation_period": f"{VAL_START} to {VAL_END}",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy {v['strategy']} --start {VAL_START} --end {VAL_END} --tp-ticks {v['tp']}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Proceed to final holdout test"
    })

print("\nValidation Period Runs completed.")
