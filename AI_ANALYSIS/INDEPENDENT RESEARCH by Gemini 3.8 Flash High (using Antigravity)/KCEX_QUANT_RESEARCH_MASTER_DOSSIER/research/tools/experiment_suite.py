import os
import sys
import csv
import json
import time
import math
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol
from BACKTESTER.engine.data_loader import OHLCVLoader, TickTradeStreamer, normalize_timeframe
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator, PerformanceSummary
from BACKTESTER.engine.reporting import BacktestReporter

LEDGER_PATH = os.path.join(ROOT_DIR, "research", "EXPERIMENT_LEDGER.csv")
OUTPUT_LEDGER_PATH = os.path.join(ROOT_DIR, "research_agent_output", "03_EXPERIMENT_LEDGER.csv")
EXPERIMENTS_DIR = os.path.join(ROOT_DIR, "research", "experiments")

LEDGER_FIELDS = [
    "experiment_id",
    "date",
    "hypothesis",
    "motivation",
    "baseline",
    "code_changes",
    "parameters",
    "symbol",
    "strategy",
    "training_period",
    "validation_period",
    "test_period",
    "backtest_command",
    "result",
    "PnL",
    "trade_count",
    "win_rate",
    "profit_factor",
    "drawdown",
    "interpretation",
    "decision",
    "next_action"
]

def init_ledger():
    for p in [LEDGER_PATH, OUTPUT_LEDGER_PATH]:
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
                writer.writeheader()

def log_experiment(row: Dict[str, Any]):
    init_ledger()
    clean_row = {}
    for k in LEDGER_FIELDS:
        v = row.get(k, "")
        if isinstance(v, float):
            clean_row[k] = f"{v:.6f}" if abs(v) < 0.01 else f"{v:.4f}"
        else:
            clean_row[k] = str(v)
    for p in [LEDGER_PATH, OUTPUT_LEDGER_PATH]:
        with open(p, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
            writer.writerow(clean_row)

def run_backtest_direct(
    symbol: str = "TRUMP_USDT",
    timeframe: str = "1m",
    strategy_mode: str = "STOCH_RSI",
    stoch_preset: str = "FAST_SCALP",
    ema_preset: str = "5/13",
    start_time: str = "2026-07-01",
    end_time: str = "2026-07-24",
    tp_ticks: int = 2,
    sl_mode: str = "ROE",
    sl_roe_pct: float = 25.0,
    sl_ticks: Optional[int] = None,
    sl_price_pct: Optional[float] = None,
    volume_mode: str = "MULTIPLIER",
    volume_contracts: Optional[int] = None,
    volume_multiplier: float = 2.0,
    leverage: int = 75,
    capital: float = 0.07,
    use_tick_data: bool = True,
    slippage_ticks: int = 0,
    duration_filter_enabled: bool = False,
    duration_deep_monitor_seconds: float = 60.0,
    duration_max_hold_seconds: float = 90.0,
    duration_action: str = "CLOSE",
    adx_filter_enabled: bool = False,
    adx_period: int = 14,
    adx_threshold: float = 25.0,
    htf_trend_filter_enabled: bool = False,
    htf_ema_period: int = 200,
    htf_timeframe: str = "15m",
    hourly_filter_enabled: bool = False,
    hourly_blacklist_utc: Optional[List[int]] = None,
    direction_bias: str = "BOTH",
    save_reports: bool = False,
    exp_dir: Optional[str] = None
) -> Tuple[Dict[str, Any], List[Any]]:
    cfg = BacktestConfig(
        symbol=symbol,
        timeframe=timeframe,
        strategy_mode=strategy_mode,
        stoch_preset=stoch_preset,
        ema_preset=ema_preset,
        start_time=start_time,
        end_time=end_time,
        tp_ticks=tp_ticks,
        sl_mode=sl_mode,
        sl_roe_pct=sl_roe_pct,
        sl_ticks=sl_ticks,
        sl_price_pct=sl_price_pct,
        volume_mode=volume_mode,
        volume_contracts=volume_contracts,
        volume_multiplier=volume_multiplier,
        leverage=leverage,
        initial_balance_usdt=capital,
        use_tick_data=use_tick_data,
        slippage_ticks=slippage_ticks,
        fee_mode="ZERO",
        duration_filter_enabled=duration_filter_enabled,
        duration_deep_monitor_seconds=duration_deep_monitor_seconds,
        duration_max_hold_seconds=duration_max_hold_seconds,
        duration_action=duration_action,
        adx_filter_enabled=adx_filter_enabled,
        adx_period=adx_period,
        adx_threshold=adx_threshold,
        htf_trend_filter_enabled=htf_trend_filter_enabled,
        htf_ema_period=htf_ema_period,
        htf_timeframe=htf_timeframe,
        hourly_filter_enabled=hourly_filter_enabled,
        hourly_blacklist_utc=hourly_blacklist_utc or [],
        direction_bias=direction_bias
    )
    
    market = BacktestMarket(
        inr_rate=cfg.inr_rate,
        fee_mode="ZERO",
        maker_fee_override=0.0,
        taker_fee_override=0.0
    )
    engine = BacktestExecutionEngine(config=cfg, market=market)
    outcomes = engine.run()
    
    summary = PerformanceCalculator.calculate(
        outcomes=outcomes,
        initial_balance_usdt=capital,
        inr_rate=cfg.inr_rate
    )
    metrics = asdict(summary)
    
    if save_reports and exp_dir:
        os.makedirs(exp_dir, exist_ok=True)
        rep = BacktestReporter(reports_dir=exp_dir)
        rep.export_all(
            outcomes=outcomes,
            summary=summary,
            config=cfg,
            contract=engine.contract,
            prefix="report"
        )
        
    return metrics, outcomes

if __name__ == "__main__":
    print("Testing experiment_suite direct execution with export...")
    metrics, outcomes = run_backtest_direct(
        start_time="2026-07-01",
        end_time="2026-07-02",
        tp_ticks=2,
        sl_mode="TICKS",
        sl_ticks=2,
        save_reports=True,
        exp_dir=os.path.join(EXPERIMENTS_DIR, "test_exp")
    )
    print(f"Executed {len(outcomes)} trades. Win rate: {metrics.get('win_rate_pct'):.2f}%. PnL: {metrics.get('net_pnl_usdt'):.4f}")
