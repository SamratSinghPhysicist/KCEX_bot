"""
Fast Targeted Pure Market Slippage Immunization Search
======================================================
Tests Pure Market Taker Execution under 0T, 1T, 2T Slippage
with safe stop buffers (SL >= 4t to 6t) and expanded targets (TP >= 8t to 12t)
at 75x leverage with zero fees.
"""

import os
import sys
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator

def run_targeted_search():
    start_date = "2026-07-01"
    end_date = "2026-07-05"  # 4 days of dense tick trades

    # Format: (Symbol, Strategy, TP, SL, Invert, Ratchet, VolMult, Label)
    candidates = [
        # --- TRUMP PURE MARKET CONFIGURATIONS ---
        ("TRUMP_USDT", "STOCH_RSI", 8, 5, True, False, 2.0, "TRUMP Inverted Stoch 8t/5t"),
        ("TRUMP_USDT", "STOCH_RSI", 10, 5, True, False, 2.0, "TRUMP Inverted Stoch 10t/5t"),
        ("TRUMP_USDT", "STOCH_RSI", 10, 5, True, True, 2.0, "TRUMP Inverted Stoch 10t/5t + Ratchet"),
        ("TRUMP_USDT", "STOCH_RSI", 8, 5, False, False, 2.0, "TRUMP Direct Stoch 8t/5t"),
        ("TRUMP_USDT", "STOCH_RSI", 10, 5, False, False, 2.0, "TRUMP Direct Stoch 10t/5t"),
        ("TRUMP_USDT", "EMA_CROSSOVER", 8, 5, False, False, 2.0, "TRUMP Direct EMA 5/13 8t/5t"),
        ("TRUMP_USDT", "EMA_CROSSOVER", 10, 5, False, True, 2.0, "TRUMP Direct EMA 5/13 10t/5t + Ratchet"),
        
        # --- DOGE PURE MARKET CONFIGURATIONS ---
        ("DOGE_USDT", "STOCH_RSI", 8, 4, True, False, 1.0, "DOGE Inverted Stoch 8t/4t"),
        ("DOGE_USDT", "STOCH_RSI", 10, 4, True, False, 1.0, "DOGE Inverted Stoch 10t/4t"),
        ("DOGE_USDT", "STOCH_RSI", 10, 4, True, True, 1.0, "DOGE Inverted Stoch 10t/4t + Ratchet"),
        ("DOGE_USDT", "STOCH_RSI", 10, 4, False, False, 1.0, "DOGE Direct Stoch 10t/4t"),
        ("DOGE_USDT", "EMA_CROSSOVER", 8, 4, False, False, 1.0, "DOGE Direct EMA 5/13 8t/4t"),
        ("DOGE_USDT", "EMA_CROSSOVER", 10, 4, False, True, 1.0, "DOGE Direct EMA 5/13 10t/4t + Ratchet"),
    ]

    print("=" * 105, flush=True)
    print(f"{'Configuration / Label':<40} | {'0T PnL':<8} {'0T PF':<6} | {'1T PnL':<8} {'1T PF':<6} | {'2T PnL':<8} {'2T PF':<6} | {'Liq':<4} {'1T WR%':<7}", flush=True)
    print("=" * 105, flush=True)

    for sym, strat, tp, sl, inv, ratch, vmult, label in candidates:
        tier_summaries = {}
        for slip in [0, 1, 2]:
            cfg = BacktestConfig(
                symbol=sym,
                timeframe="1m",
                strategy_mode=strat,
                ema_preset="5/13",
                stoch_preset="FAST_SCALP",
                start_time=start_date,
                end_time=end_date,
                volume_mode="MULTIPLIER",
                volume_multiplier=vmult,
                tp_ticks=tp,
                sl_mode="TICKS",
                sl_ticks=sl,
                leverage=75,
                fee_mode="ZERO",
                use_tick_data=True,
                execution_style="PURE_MARKET",  # Pure market taker
                queue_dynamics_enabled=False,   # No maker queue
                slippage_enabled=(slip > 0),
                slippage_ticks=slip,
                invert_signal=inv,
                ratchet_enabled=ratch,
                ratchet_trigger_ticks=3.0,
                ratchet_stall_seconds=10.0,
                ratchet_tighten_ticks=1.0,
                ratchet_breakeven_ticks=4.0
            )

            engine = BacktestExecutionEngine(config=cfg)
            outcomes = engine.run()
            summary = PerformanceCalculator.calculate(outcomes, initial_balance_usdt=100.0)
            tier_summaries[slip] = summary

        s0 = tier_summaries[0]
        s1 = tier_summaries[1]
        s2 = tier_summaries[2]

        print(
            f"{label:<40} | "
            f"{s0.net_pnl_usdt:>+7.4f} {s0.profit_factor:>6.2f} | "
            f"{s1.net_pnl_usdt:>+7.4f} {s1.profit_factor:>6.2f} | "
            f"{s2.net_pnl_usdt:>+7.4f} {s2.profit_factor:>6.2f} | "
            f"{s1.liquidations:>4} {s1.win_rate_pct:>6.1f}%",
            flush=True
        )

if __name__ == "__main__":
    run_targeted_search()
