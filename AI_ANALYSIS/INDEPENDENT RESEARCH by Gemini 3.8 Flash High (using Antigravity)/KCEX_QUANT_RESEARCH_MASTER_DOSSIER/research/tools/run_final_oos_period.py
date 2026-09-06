import os
import sys
import json
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct, log_experiment, EXPERIMENTS_DIR

OOS_START = "2026-08-16"
OOS_END = "2026-08-31"

oos_runs = [
    {
        "id": "EXP_0044",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 5,
        "name": "FINAL_OOS: Candidate STOCH_RSI (TP=2, SL=5t)",
        "desc": "Final untouched out-of-sample evaluation of Candidate System."
    },
    {
        "id": "EXP_0045",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "ROE",
        "sl_roe": 25.0,
        "sl_ticks": None,
        "name": "FINAL_OOS: Baseline STOCH_RSI (TP=2, SL=25% ROE)",
        "desc": "Final untouched out-of-sample evaluation of Baseline System."
    },
    {
        "id": "EXP_0046",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 2,
        "name": "FINAL_OOS: Symmetric STOCH_RSI (TP=2, SL=2t)",
        "desc": "Final untouched out-of-sample diagnostic symmetric test."
    },
    {
        "id": "EXP_0047",
        "strategy": "EMA_CROSSOVER",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 5,
        "name": "FINAL_OOS: Candidate EMA (TP=2, SL=5t)",
        "desc": "Final untouched out-of-sample evaluation of EMA_CROSSOVER."
    }
]

print(f"================ Starting Final Untouched OOS Runs ({OOS_START} to {OOS_END}) ================")
print(f"{'Exp ID':<10} | {'Name':<35} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 96)

for o in oos_runs:
    exp_id = o["id"]
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode=o["strategy"],
        stoch_preset="FAST_SCALP",
        ema_preset="5/13",
        start_time=OOS_START,
        end_time=OOS_END,
        tp_ticks=o["tp"],
        sl_mode=o["sl_mode"],
        sl_roe_pct=o["sl_roe"],
        sl_ticks=o["sl_ticks"],
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"{exp_id:<10} | {o['name']:<35} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "VALIDATED" if pnl > 0.08 and pf > 1.15 else ("REJECTED" if pnl <= 0 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Final holdout test on untouched out-of-sample period {OOS_START} to {OOS_END}.",
        "motivation": o["desc"],
        "baseline": "VALIDATION_RUNS",
        "code_changes": f"Run on final OOS period: {o['name']}",
        "parameters": f"strat={o['strategy']},tp={o['tp']},sl_mode={o['sl_mode']},sl_ticks={o['sl_ticks']}",
        "symbol": "TRUMP_USDT",
        "strategy": o["strategy"],
        "training_period": "2026-07-01 to 2026-07-24",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": f"{OOS_START} to {OOS_END}",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy {o['strategy']} --start {OOS_START} --end {OOS_END} --tp-ticks {o['tp']}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Cross-pair validation"
    })

print("\nFinal OOS Runs completed.")
