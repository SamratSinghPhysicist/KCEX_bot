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

sl_tick_values = [3, 4, 5, 6, 8, 10, 12, 15]

print("================ Starting TP/SL Geometry Sweep (TP=2 ticks) ================")
print(f"{'Exp ID':<10} | {'SL Ticks':<8} | {'Trades':<6} | {'Win Rate':<9} | {'RW Prob':<8} | {'Delta P':<8} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 90)

for sl in sl_tick_values:
    exp_num = 5 + sl_tick_values.index(sl)
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
        tp_ticks=2,
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
    
    rw_prob = (sl / (2.0 + sl)) * 100.0
    delta_p = wr - rw_prob
    
    print(f"{exp_id:<10} | {sl:<8} | {trades:<6} | {wr:>7.2f}% | {rw_prob:>6.2f}% | {delta_p:>+6.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "PROMISING" if pnl > 0.15 and pf > 1.20 else ("REJECTED" if pnl <= 0 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Evaluating TP=2/SL={sl} ticks to measure empirical absorption probability vs random walk boundary ({rw_prob:.1f}%).",
        "motivation": f"Investigate TP/SL geometry and optimal stop distance for STOCH_RSI.",
        "baseline": "EXP_0001",
        "code_changes": "None (TP/SL parameter variation)",
        "parameters": f"strat=STOCH_RSI,tp=2,sl_mode=TICKS,sl_ticks={sl}",
        "symbol": "TRUMP_USDT",
        "strategy": "STOCH_RSI",
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy STOCH_RSI --start {DISCOVERY_START} --end {DISCOVERY_END} --tp-ticks 2 --sl-mode TICKS --sl-ticks {sl}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}% (RW: {rw_prob:.1f}%, Delta: {delta_p:+.2f}%), PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Analyze delta_p peak and expected payoff curve"
    })

print("\nTP/SL Geometry Sweep completed successfully.")
