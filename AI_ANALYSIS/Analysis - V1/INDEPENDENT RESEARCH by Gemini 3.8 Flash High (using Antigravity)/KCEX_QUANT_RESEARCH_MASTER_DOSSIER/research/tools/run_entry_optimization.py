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

entry_experiments = [
    {
        "id": "EXP_0022",
        "preset": "MICRO_BURST",
        "sl_ticks": 5,
        "desc": "MICRO_BURST (7, 7, 3, 3) with extreme zones 15/85 and SL=5t",
        "hypothesis": "MICRO_BURST preset requires more extreme oscillator divergence (15/85), filtering out marginal chop entries."
    },
    {
        "id": "EXP_0023",
        "preset": "STANDARD",
        "sl_ticks": 5,
        "desc": "STANDARD (14, 14, 3, 3) with zones 20/80 and SL=5t",
        "hypothesis": "STANDARD preset smooths out 1m noise over longer 14-period window, improving signal quality."
    },
    {
        "id": "EXP_0024",
        "preset": "FAST_SCALP",
        "sl_ticks": 5,
        "desc": "FAST_SCALP (9, 9, 3, 3) with SL=5t (EXP_0007 reference)",
        "hypothesis": "FAST_SCALP with SL=5t captures peak Delta P (+4.68%) and lowest drawdown."
    },
    {
        "id": "EXP_0025",
        "preset": "MICRO_BURST",
        "sl_ticks": 4,
        "desc": "MICRO_BURST with tighter SL=4t",
        "hypothesis": "MICRO_BURST with tight SL=4t maximizes risk-reward payoff."
    },
    {
        "id": "EXP_0026",
        "preset": "FAST_SCALP",
        "sl_ticks": 4,
        "desc": "FAST_SCALP with tight SL=4t",
        "hypothesis": "FAST_SCALP with SL=4t tests payoff ratio vs win rate."
    }
]

print("================ Starting Strategy Preset & Zone Sensitivity Suite ================")
print(f"{'Exp ID':<10} | {'Preset':<12} | {'SL Ticks':<8} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 88)

for e in entry_experiments:
    exp_id = e["id"]
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        stoch_preset=e["preset"],
        start_time=DISCOVERY_START,
        end_time=DISCOVERY_END,
        tp_ticks=2,
        sl_mode="TICKS",
        sl_ticks=e["sl_ticks"],
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"{exp_id:<10} | {e['preset']:<12} | {e['sl_ticks']:<8} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "PROMISING" if pnl > 0.18 and pf > 1.25 and dd < 10.0 else ("REJECTED" if pnl < 0.10 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": e["hypothesis"],
        "motivation": f"Test {e['desc']}",
        "baseline": "EXP_0001",
        "code_changes": f"Preset: {e['preset']}, SL: {e['sl_ticks']}t",
        "parameters": f"strat=STOCH_RSI,preset={e['preset']},tp=2,sl_mode=TICKS,sl_ticks={e['sl_ticks']}",
        "symbol": "TRUMP_USDT",
        "strategy": "STOCH_RSI",
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy STOCH_RSI --stoch-preset {e['preset']} --start {DISCOVERY_START} --end {DISCOVERY_END} --tp-ticks 2 --sl-mode TICKS --sl-ticks {e['sl_ticks']}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f}, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Compare preset performance and consistency"
    })

print("\nStrategy Preset & Zone Sensitivity Suite completed.")
