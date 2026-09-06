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

# Let's test ADX threshold variations on SL=5t
adx_thresholds = [15.0, 20.0, 25.0, 30.0]

print("================ Starting Volatility & ADX Sensitivity on SL=5t ================")
print(f"{'Exp ID':<10} | {'ADX Thresh':<10} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8}")
print("-" * 75)

for th in adx_thresholds:
    exp_num = 34 + adx_thresholds.index(th)
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
        sl_ticks=5,
        adx_filter_enabled=True,
        adx_period=14,
        adx_threshold=th,
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    
    print(f"{exp_id:<10} | {th:<10.1f} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}%")
    
    decision = "PROMISING" if pnl > 0.20 and pf > 1.30 else ("REJECTED" if pnl < 0.15 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": f"Testing ADX threshold >= {th} on optimal SL=5t configuration to verify chop avoidance.",
        "motivation": f"Investigate ADX sensitivity on SL=5t system.",
        "baseline": "EXP_0007",
        "code_changes": f"ADX threshold: {th}",
        "parameters": f"strat=STOCH_RSI,tp=2,sl_mode=TICKS,sl_ticks=5,adx_th={th}",
        "symbol": "TRUMP_USDT",
        "strategy": "STOCH_RSI",
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy STOCH_RSI --start {DISCOVERY_START} --end {DISCOVERY_END} --tp-ticks 2 --sl-ticks 5 --adx-filter --adx-threshold {th}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades}, WR: {wr:.2f}%, PF: {pf:.2f}, PnL: {pnl:+.4f} USDT, DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Assess economic value retention"
    })

print("\nADX Sensitivity Suite completed.")
