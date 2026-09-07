"""
Market Slippage Immunization Quantitative Test
===============================================
Evaluates Pure Market Execution under 0T, 1T, 2T, 3T adverse slippage
to discover the parameter sets that remain profitable despite taker friction.
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

def test_permutations():
    start_date = "2026-07-01"
    end_date = "2026-07-08"  # 1 week representative tick slice

    # Test Matrix: (Symbol, Strategy, TP, SL, Invert, Ratchet, VolMult, Label)
    test_cases = [
        # --- TRUMP PURE MARKET ---
        ("TRUMP_USDT", "STOCH_RSI", 2, 5, False, False, 2.0, "TRUMP Baseline Direct 2t/5t"),
        ("TRUMP_USDT", "STOCH_RSI", 6, 3, False, False, 2.0, "TRUMP Direct 6t/3t (2:1 RR)"),
        ("TRUMP_USDT", "STOCH_RSI", 8, 4, False, False, 2.0, "TRUMP Direct 8t/4t (2:1 RR)"),
        ("TRUMP_USDT", "STOCH_RSI", 8, 4, False, True, 2.0, "TRUMP Direct 8t/4t + Ratchet"),
        ("TRUMP_USDT", "EMA_CROSSOVER", 6, 3, False, False, 2.0, "TRUMP EMA 5/13 6t/3t"),
        ("TRUMP_USDT", "EMA_CROSSOVER", 8, 4, False, True, 2.0, "TRUMP EMA 5/13 8t/4t + Ratchet"),
        
        # --- DOGE PURE MARKET ---
        ("DOGE_USDT", "STOCH_RSI", 2, 5, True, False, 1.0, "DOGE Baseline Inverted 2t/5t"),
        ("DOGE_USDT", "STOCH_RSI", 5, 2, True, False, 1.0, "DOGE Inverted 5t/2t (2.5:1 RR)"),
        ("DOGE_USDT", "STOCH_RSI", 5, 2, True, True, 1.0, "DOGE Inverted 5t/2t + Ratchet"),
        ("DOGE_USDT", "STOCH_RSI", 10, 2, False, False, 1.0, "DOGE Direct Asymmetric 10t/2t (5:1 RR)"),
        ("DOGE_USDT", "STOCH_RSI", 8, 3, False, True, 1.0, "DOGE Direct 8t/3t + Ratchet"),
        ("DOGE_USDT", "EMA_CROSSOVER", 6, 2, False, False, 1.0, "DOGE EMA 5/13 6t/2t"),
    ]

    print("=" * 100)
    print(f"{'Label':<35} | {'0T PnL':<8} {'0T PF':<6} | {'1T PnL':<8} {'1T PF':<6} | {'2T PnL':<8} {'2T PF':<6} | {'Liq':<4} {'WR%':<6}")
    print("=" * 100)

    for sym, strat, tp, sl, inv, ratch, vmult, label in test_cases:
        tier_res = {}
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
                execution_style="PURE_MARKET",  # PURE MARKET TAKER EXECUTION
                queue_dynamics_enabled=False,   # No maker limit orders
                slippage_enabled=(slip > 0),
                slippage_ticks=slip,
                invert_signal=inv,
                ratchet_enabled=ratch,
                ratchet_trigger_ticks=2.0 if tp >= 6 else 1.0,
                ratchet_stall_seconds=10.0,
                ratchet_tighten_ticks=1.0,
                ratchet_breakeven_ticks=3.0 if tp >= 6 else 2.5
            )

            engine = BacktestExecutionEngine(config=cfg)
            outcomes = engine.run()
            summary = PerformanceCalculator.calculate(outcomes, initial_balance_usdt=100.0)
            tier_res[slip] = summary

        s0 = tier_res[0]
        s1 = tier_res[1]
        s2 = tier_res[2]

        print(
            f"{label:<35} | "
            f"{s0.net_pnl_usdt:>+7.4f} {s0.profit_factor:>6.2f} | "
            f"{s1.net_pnl_usdt:>+7.4f} {s1.profit_factor:>6.2f} | "
            f"{s2.net_pnl_usdt:>+7.4f} {s2.profit_factor:>6.2f} | "
            f"{s1.liquidations:>4} {s1.win_rate_pct:>5.1f}%"
        )

if __name__ == "__main__":
    test_permutations()
