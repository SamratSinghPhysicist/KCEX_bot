import os
import sys
import json
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct, log_experiment, EXPERIMENTS_DIR

cross_pair_runs = [
    {
        "id": "EXP_0048",
        "symbol": "DOGE_USDT",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 5,
        "start": "2026-07-01",
        "end": "2026-08-31",
        "name": "CROSS_PAIR: DOGE_USDT Candidate (TP=2, SL=5t)",
        "desc": "Cross-pair evaluation of Candidate System on DOGE_USDT."
    },
    {
        "id": "EXP_0049",
        "symbol": "DOGE_USDT",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "ROE",
        "sl_roe": 25.0,
        "sl_ticks": None,
        "start": "2026-07-01",
        "end": "2026-08-31",
        "name": "CROSS_PAIR: DOGE_USDT Baseline (TP=2, SL=25% ROE)",
        "desc": "Cross-pair evaluation of Baseline System on DOGE_USDT."
    },
    {
        "id": "EXP_0050",
        "symbol": "DOGE_USDT",
        "strategy": "STOCH_RSI",
        "tp": 2,
        "sl_mode": "TICKS",
        "sl_roe": 25.0,
        "sl_ticks": 2,
        "start": "2026-07-01",
        "end": "2026-08-31",
        "name": "CROSS_PAIR: DOGE_USDT Symmetric (TP=2, SL=2t)",
        "desc": "Cross-pair diagnostic symmetric test on DOGE_USDT."
    }
]

print("================ Starting Cross-Pair Generalization on DOGE_USDT ================")
print(f"{'Exp ID':<10} | {'Name':<40} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 100)

for cp in cross_pair_runs:
    exp_id = cp["id"]
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol=cp["symbol"],
        timeframe="1m",
        strategy_mode=cp["strategy"],
        stoch_preset="FAST_SCALP",
        ema_preset="5/13",
        start_time=cp["start"],
        end_time=cp["end"],
        tp_ticks=cp["tp"],
        sl_mode=cp["sl_mode"],
        sl_roe_pct=cp["sl_roe"],
        sl_ticks=cp["sl_ticks"],
        volume_mode="CONTRACTS",
        volume_contracts=1,
        capital=100.0,
        use_tick_data=False, # Use 1m candle High/Low for DOGE
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"{exp_id:<10} | {cp['name']:<40} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "VALIDATED" if pnl > 0 and pf > 1.05 else ("REJECTED" if pnl <= 0 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Cross-pair generalization test on {cp['symbol']}.",
        "motivation": cp["desc"],
        "baseline": "TRUMP_RUNS",
        "code_changes": f"Run on DOGE_USDT: {cp['name']}",
        "parameters": f"symbol=DOGE_USDT,strat={cp['strategy']},tp={cp['tp']},sl_mode={cp['sl_mode']},sl_ticks={cp['sl_ticks']}",
        "symbol": "DOGE_USDT",
        "strategy": cp["strategy"],
        "training_period": "TRUMP July 2026",
        "validation_period": "TRUMP August 2026",
        "test_period": "DOGE July-August 2026",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol DOGE_USDT --strategy {cp['strategy']} --start {cp['start']} --end {cp['end']} --tp-ticks {cp['tp']}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Complete research ledger and finalize reports"
    })

print("\nCross-Pair Generalization completed.")
