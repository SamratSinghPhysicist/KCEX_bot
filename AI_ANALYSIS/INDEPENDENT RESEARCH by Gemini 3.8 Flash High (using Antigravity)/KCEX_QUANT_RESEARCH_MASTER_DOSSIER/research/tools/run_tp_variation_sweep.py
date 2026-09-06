import os
import sys
import json
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct, log_experiment, EXPERIMENTS_DIR

DISCOVERY_START = "2026-07-01"
DISCOVERY_END = "2026-07-24"

tp_sl_pairs = [
    (3, 3), # 1:1 risk-reward at 3 ticks
    (3, 5), # 1:1.67
    (3, 6), # 1:2
    (3, 8), # 1:2.67
    (4, 4), # 1:1 risk-reward at 4 ticks
    (4, 6), # 1:1.5
    (4, 8), # 1:2
]

print("================ Starting TP Distance & Payoff Structure Suite ================")
print(f"{'Exp ID':<10} | {'TP/SL':<8} | {'Trades':<6} | {'Win Rate':<9} | {'RW Prob':<8} | {'Delta P':<8} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 90)

for tp, sl in tp_sl_pairs:
    exp_num = 27 + tp_sl_pairs.index((tp, sl))
    exp_id = f"EXP_{exp_num:04d}"
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        stoch_preset="FAST_SCALP",
        start_time=DISCOVERY_START,
        end_time=DISCOVERY_END,
        tp_ticks=tp,
        sl_mode="TICKS",
        sl_ticks=sl,
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    rw_prob = (sl / (tp + sl)) * 100.0
    delta_p = wr - rw_prob
    
    print(f"{exp_id:<10} | {tp}/{sl:<5} | {trades:<6} | {wr:>7.2f}% | {rw_prob:>6.2f}% | {delta_p:>+6.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "PROMISING" if pnl > 0.22 and pf > 1.25 else ("REJECTED" if pnl <= 0.05 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Evaluating TP={tp} / SL={sl} ticks to test whether larger profit targets yield higher economic payoff.",
        "motivation": f"Explore alternative TP distances ({tp} ticks) and risk-reward geometry.",
        "baseline": "EXP_0001",
        "code_changes": f"TP={tp}, SL={sl} ticks",
        "parameters": f"strat=STOCH_RSI,tp={tp},sl_mode=TICKS,sl_ticks={sl}",
        "symbol": "TRUMP_USDT",
        "strategy": "STOCH_RSI",
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy STOCH_RSI --start {DISCOVERY_START} --end {DISCOVERY_END} --tp-ticks {tp} --sl-mode TICKS --sl-ticks {sl}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}% (RW: {rw_prob:.1f}%, Delta: {delta_p:+.2f}%), PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Compare against TP=2 tick baseline"
    })

print("\nTP Distance Suite completed.")
