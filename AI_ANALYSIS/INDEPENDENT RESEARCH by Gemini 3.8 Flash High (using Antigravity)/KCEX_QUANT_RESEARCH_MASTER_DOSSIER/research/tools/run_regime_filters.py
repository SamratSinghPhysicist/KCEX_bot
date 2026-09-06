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

filter_experiments = [
    {
        "id": "EXP_0016",
        "name": "HTF_200_EMA",
        "htf_enabled": True,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": False,
        "hourly_enabled": False,
        "dir_bias": "BOTH",
        "hypothesis": "Restricting micro-scalps to align with the 15m 200-EMA macro trend will eliminate counter-trend knife-catching losses.",
        "motivation": "Test the Higher Timeframe (HTF) trend filter hypothesis."
    },
    {
        "id": "EXP_0017",
        "name": "ADX_CHOP_FILTER",
        "htf_enabled": False,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": True,
        "adx_period": 14,
        "adx_threshold": 25.0,
        "hourly_enabled": False,
        "dir_bias": "BOTH",
        "hypothesis": "Filtering out low-ADX market conditions (ADX < 25) will suppress choppy sideways whipsaws.",
        "motivation": "Test ADX trend strength chop filter hypothesis."
    },
    {
        "id": "EXP_0018",
        "name": "HOURLY_DEAD_ZONE",
        "htf_enabled": False,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": False,
        "hourly_enabled": True,
        "hourly_bl": [2, 3, 4, 5, 17],
        "dir_bias": "BOTH",
        "hypothesis": "Blacklisting low-liquidity UTC hours (02:00, 03:00, 04:00, 05:00, 17:00) avoids choppy sessions.",
        "motivation": "Test hourly session blacklist hypothesis."
    },
    {
        "id": "EXP_0019",
        "name": "DIRECTION_LONG_ONLY",
        "htf_enabled": False,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": False,
        "hourly_enabled": False,
        "dir_bias": "LONG_ONLY",
        "hypothesis": "Evaluating LONG_ONLY trade signals to isolate direction-specific edge.",
        "motivation": "Test directional bias hypothesis (LONG_ONLY)."
    },
    {
        "id": "EXP_0020",
        "name": "DIRECTION_SHORT_ONLY",
        "htf_enabled": False,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": False,
        "hourly_enabled": False,
        "dir_bias": "SHORT_ONLY",
        "hypothesis": "Evaluating SHORT_ONLY trade signals to test whether shorts outperform longs.",
        "motivation": "Test directional bias hypothesis (SHORT_ONLY)."
    },
    {
        "id": "EXP_0021",
        "name": "ALL_FILTERS_COMBINED",
        "htf_enabled": True,
        "htf_tf": "15m",
        "htf_period": 200,
        "adx_enabled": True,
        "adx_period": 14,
        "adx_threshold": 25.0,
        "hourly_enabled": True,
        "hourly_bl": [2, 3, 4, 5, 17],
        "dir_bias": "BOTH",
        "hypothesis": "Combining HTF 200 EMA + ADX chop filter + Hourly blacklist eliminates the majority of losses.",
        "motivation": "Test composite multi-filter pipeline hypothesis."
    }
]

print("================ Starting Regime & Filter Pipeline Suite ================")
print(f"{'Exp ID':<10} | {'Filter Name':<20} | {'Trades':<6} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Max DD':<8} | {'PnL/Trade':<10}")
print("-" * 96)

for fexp in filter_experiments:
    exp_id = fexp["id"]
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
        sl_mode="ROE",
        sl_roe_pct=25.0,
        htf_trend_filter_enabled=fexp["htf_enabled"],
        htf_ema_period=fexp.get("htf_period", 200),
        htf_timeframe=fexp.get("htf_tf", "15m"),
        adx_filter_enabled=fexp["adx_enabled"],
        adx_period=fexp.get("adx_period", 14),
        adx_threshold=fexp.get("adx_threshold", 25.0),
        hourly_filter_enabled=fexp["hourly_enabled"],
        hourly_blacklist_utc=fexp.get("hourly_bl", []),
        direction_bias=fexp["dir_bias"],
        save_reports=True,
        exp_dir=exp_dir
    )
    t_elapsed = time.time() - t0
    
    trades = metrics["total_trades"]
    wr = metrics["win_rate_pct"]
    pf = metrics["profit_factor"]
    pnl = metrics["net_pnl_usdt"]
    dd = metrics["max_drawdown_pct"]
    pnl_per_trade = (pnl / trades) if trades > 0 else 0.0
    
    print(f"{exp_id:<10} | {fexp['name']:<20} | {trades:<6} | {wr:>7.2f}% | {pf:>6.2f} | {pnl:>+9.4f}  | {dd:>6.2f}% | {pnl_per_trade:>+9.6f}")
    
    # Baseline comparison (EXP_0001: 3066 trades, PnL +0.2120 USDT, PF 1.29, WR 77.40%, DD 12.69%)
    decision = "PROMISING" if pnl > 0.22 and pf > 1.30 else ("REJECTED" if pnl < 0.15 else "INCONCLUSIVE")
    
    log_experiment({
        "experiment_id": exp_id,
        "date": "2026-09-06",
        "hypothesis": fexp["hypothesis"],
        "motivation": fexp["motivation"],
        "baseline": "EXP_0001",
        "code_changes": f"Active filters: {fexp['name']}",
        "parameters": f"strat=STOCH_RSI,filter={fexp['name']}",
        "symbol": "TRUMP_USDT",
        "strategy": "STOCH_RSI",
        "training_period": f"{DISCOVERY_START} to {DISCOVERY_END}",
        "validation_period": "2026-07-25 to 2026-08-15",
        "test_period": "2026-08-16 to 2026-08-31",
        "backtest_command": f"python BACKTESTER/run_backtest.py --symbol TRUMP_USDT --strategy STOCH_RSI --start {DISCOVERY_START} --end {DISCOVERY_END}",
        "result": decision,
        "PnL": pnl,
        "trade_count": trades,
        "win_rate": wr,
        "profit_factor": pf,
        "drawdown": dd,
        "interpretation": f"Trades: {trades} (vs 3066), WR: {wr:.2f}% (vs 77.40%), PF: {pf:.2f} (vs 1.29), PnL: {pnl:+.4f} (vs +0.2120), DD: {dd:.2f}%",
        "decision": decision,
        "next_action": "Evaluate counterfactual trade retention vs loss avoidance"
    })

print("\nRegime & Filter Pipeline Suite completed successfully.")
