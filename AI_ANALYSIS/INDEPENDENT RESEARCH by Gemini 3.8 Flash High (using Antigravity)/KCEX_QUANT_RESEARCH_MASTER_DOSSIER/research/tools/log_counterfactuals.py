import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import log_experiment

log_experiment({
    "experiment_id": "EXP_0013",
    "date": "2026-09-06",
    "hypothesis": "Moving stop to breakeven after touching +1 tick excursion will protect the 188 near-TP losing trades.",
    "motivation": "Counterfactual test of breakeven stop rule to avoid near-TP reversals.",
    "baseline": "EXP_0001",
    "code_changes": "None (Counterfactual Replay)",
    "parameters": "strat=STOCH_RSI,tp=2,sl=ROE:25,rule=BE_ON_PLUS_1",
    "symbol": "TRUMP_USDT",
    "strategy": "STOCH_RSI",
    "training_period": "2026-07-01 to 2026-07-24",
    "validation_period": "2026-07-25 to 2026-08-15",
    "test_period": "2026-08-16 to 2026-08-31",
    "backtest_command": "python research/tools/counterfactual_analysis.py",
    "result": "REJECTED",
    "PnL": 0.0118,
    "trade_count": 3066,
    "win_rate": 44.88,
    "profit_factor": 1.02,
    "drawdown": 16.5,
    "interpretation": "Avoided 188 losses (+0.1986 USDT) but prematurely killed 997 winners (-0.3988 USDT). Net impact: -0.2002 USDT.",
    "decision": "REJECTED",
    "next_action": "Abandon breakeven trailing stop on +1 tick"
})

log_experiment({
    "experiment_id": "EXP_0014",
    "date": "2026-09-06",
    "hypothesis": "Closing trades at market after 60 seconds (duration filter) cuts time-decay drift and saves losses.",
    "motivation": "Test the widely cited duration time-decay hypothesis via exact counterfactual tick replay.",
    "baseline": "EXP_0001",
    "code_changes": "None (Counterfactual Replay)",
    "parameters": "strat=STOCH_RSI,tp=2,sl=ROE:25,rule=TIMEOUT_60S",
    "symbol": "TRUMP_USDT",
    "strategy": "STOCH_RSI",
    "training_period": "2026-07-01 to 2026-07-24",
    "validation_period": "2026-07-25 to 2026-08-15",
    "test_period": "2026-08-16 to 2026-08-31",
    "backtest_command": "python research/tools/counterfactual_analysis.py",
    "result": "REJECTED",
    "PnL": 0.0600,
    "trade_count": 3066,
    "win_rate": 29.48,
    "profit_factor": 1.05,
    "drawdown": 22.1,
    "interpretation": "Survivorship bias debunked: Saved +0.5312 USDT on 625 losses but killed 1469 winning trades (-0.6832 USDT). Net impact: -0.1520 USDT.",
    "decision": "REJECTED",
    "next_action": "Do not use hard 60s duration exits"
})

log_experiment({
    "experiment_id": "EXP_0015",
    "date": "2026-09-06",
    "hypothesis": "Closing trades at market after 90 seconds (duration filter) balances drift avoidance with trade resolution.",
    "motivation": "Test 90s timeout duration filter counterfactually.",
    "baseline": "EXP_0001",
    "code_changes": "None (Counterfactual Replay)",
    "parameters": "strat=STOCH_RSI,tp=2,sl=ROE:25,rule=TIMEOUT_90S",
    "symbol": "TRUMP_USDT",
    "strategy": "STOCH_RSI",
    "training_period": "2026-07-01 to 2026-07-24",
    "validation_period": "2026-07-25 to 2026-08-15",
    "test_period": "2026-08-16 to 2026-08-31",
    "backtest_command": "python research/tools/counterfactual_analysis.py",
    "result": "REJECTED",
    "PnL": 0.1054,
    "trade_count": 3066,
    "win_rate": 37.87,
    "profit_factor": 1.10,
    "drawdown": 18.4,
    "interpretation": "Saved +0.4768 USDT on 586 losses but killed 1212 winning trades (-0.5834 USDT). Net impact: -0.1066 USDT.",
    "decision": "REJECTED",
    "next_action": "Do not use hard 90s duration exits"
})
print("Logged EXP_0013, EXP_0014, EXP_0015.")
