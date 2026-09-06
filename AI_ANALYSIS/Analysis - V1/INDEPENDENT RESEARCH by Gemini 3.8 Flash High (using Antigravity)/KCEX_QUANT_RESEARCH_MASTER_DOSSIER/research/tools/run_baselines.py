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

experiments = [
    {
        "id": "EXP_0001",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "ema_preset": "5/13",
        "tp_ticks": 2,
        "sl_mode": "ROE",
        "sl_roe_pct": 25.0,
        "sl_ticks": None,
        "hypothesis": "Baseline STOCH_RSI at 75x with TP=2t and SL=25% ROE produces ~85% win rate due to absorbing barrier geometry (+2 vs -10 ticks).",
        "motivation": "Reconstruct official STOCH_RSI baseline on 24-day discovery period.",
        "baseline": "CURRENT_PRODUCTION",
        "interpretation_target": "Absorbing barrier baseline."
    },
    {
        "id": "EXP_0002",
        "strategy": "EMA_CROSSOVER",
        "stoch_preset": "FAST_SCALP",
        "ema_preset": "5/13",
        "tp_ticks": 2,
        "sl_mode": "ROE",
        "sl_roe_pct": 25.0,
        "sl_ticks": None,
        "hypothesis": "Baseline EMA_CROSSOVER at 75x with TP=2t and SL=25% ROE produces similar absorbing barrier outcome.",
        "motivation": "Reconstruct official EMA_CROSSOVER baseline on 24-day discovery period.",
        "baseline": "CURRENT_PRODUCTION",
        "interpretation_target": "EMA crossover baseline."
    },
    {
        "id": "EXP_0003",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "ema_preset": "5/13",
        "tp_ticks": 2,
        "sl_mode": "TICKS",
        "sl_roe_pct": 25.0,
        "sl_ticks": 2,
        "hypothesis": "Symmetric TP=2 / SL=2 diagnostic test isolates entry directional skill without absorbing barrier asymmetry.",
        "motivation": "Diagnostic test of raw directional predictability for STOCH_RSI.",
        "baseline": "EXP_0001",
        "interpretation_target": "Raw directional skill."
    },
    {
        "id": "EXP_0004",
        "strategy": "EMA_CROSSOVER",
        "stoch_preset": "FAST_SCALP",
        "ema_preset": "5/13",
        "tp_ticks": 2,
        "sl_mode": "TICKS",
        "sl_roe_pct": 25.0,
        "sl_ticks": 2,
        "hypothesis": "Symmetric TP=2 / SL=2 diagnostic test isolates entry directional skill for EMA_CROSSOVER.",
        "motivation": "Diagnostic test of raw directional predictability for EMA_CROSSOVER.",
        "baseline": "EXP_0002",
        "interpretation_target": "Raw directional skill."
    }
]

for exp in experiments:
    exp_id = exp["id"]
    exp_dir = os.path.join(EXPERIMENTS_DIR, exp_id)
    print(f"\n================ Running {exp_id} ({exp['strategy']} | TP={exp['tp_ticks']} | SL={exp['sl_mode']}:{exp['sl_ticks'] or exp['sl_roe_pct']}) ================")
    t0 = time.time()
    metrics, outcomes = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode=exp["strategy"],
        stoch_preset=exp["stoch_preset"],
        ema_preset=exp["ema_preset"],
        start_time=DISCOVERY_START,
        end_time=DISCOVERY_END,
        tp_ticks=exp["tp_ticks"],
        sl_mode=exp["sl_mode"],
        sl_roe_pct=exp["sl_roe_pct"],
        sl_ticks=exp["sl_ticks"],
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"[{exp_id}] Done in {t_elapsed:.1f}s | Trades: {trades} | Win Rate: {wr:.2f}% | PF: {pf:.2f} | Net PnL: {pnl:+.4f} USDT | Max DD: {dd:.2f}%")
    
    status = "BASELINE"
    interp = f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f} USDT. {exp['interpretation_target']}"
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": exp["hypothesis"],
        "motivation": exp["motivation"],
        "baseline": exp["baseline"],
        "code_changes": "None (Baseline Reconstruction)",
        "parameters": f"strat={exp['strategy']},tp={exp['tp_ticks']},sl={exp['sl_mode']}:{exp['sl_ticks'] or exp['sl_roe_pct']}",
        "symbol": "TRUMP_USDT",
        "strategy": exp["strategy"],
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy {exp['strategy']} --start {DISCOVERY_START} --end {DISCOVERY_END} --tp-ticks {exp['tp_ticks']} --sl-mode {exp['sl_mode']}",
        "result": status,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": interp,
        "decision": "ESTABLISHED_BASELINE",
        "next_action": "Conduct granular loss forensics on baseline outcomes"
    })
print("\nAll baseline experiments executed and logged.")
