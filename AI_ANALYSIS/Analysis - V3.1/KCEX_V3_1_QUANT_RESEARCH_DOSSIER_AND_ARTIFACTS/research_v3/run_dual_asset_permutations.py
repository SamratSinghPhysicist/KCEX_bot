"""
Dual-Asset (TRUMP & DOGE) Comprehensive Permutation Research Suite
==================================================================
Formulates, dispatches to GitHub Actions cloud runners, and empirically
evaluates an exhaustive permutation matrix across TRUMP_USDT and DOGE_USDT
using high-fidelity millisecond tick trade streams under 75x leverage and zero fees.
"""

import os
import sys
import time
import json
from typing import Dict, Any, List

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from research_v3.master_research_v3 import MasterQuantResearchEngineV3, ExperimentResult
from research_v3.cloud_matrix_dispatcher import CloudMatrixDispatcher


def build_config(
    symbol: str,
    strategy: str,
    tp_ticks: int,
    sl_ticks: int,
    invert_signal: bool = False,
    execution_style: str = "MAKER_HYBRID",
    ratchet: bool = False,
    duration_filter: bool = False,
    start_date: str = "2026-07-01",
    end_date: str = "2026-07-14",
    ema_preset: str = "5/13",
    stoch_preset: str = "FAST_SCALP",
    leverage: int = 75
) -> BacktestConfig:
    vol_mult = 2.0 if "TRUMP" in symbol.upper() else 1.0

    return BacktestConfig(
        symbol=symbol,
        timeframe="1m",
        strategy_mode=strategy,
        ema_preset=ema_preset,
        stoch_preset=stoch_preset,
        start_time=start_date,
        end_time=end_date,
        use_tick_data=True,
        fee_mode="ZERO",
        maker_fee_override=0.0,
        taker_fee_override=0.0,
        volume_mode="MULTIPLIER",
        volume_multiplier=vol_mult,
        tp_ticks=tp_ticks,
        sl_mode="TICKS",
        sl_ticks=sl_ticks,
        leverage=leverage,
        initial_balance_usdt=100.0,
        invert_signal=invert_signal,
        execution_style=execution_style,
        queue_dynamics_enabled=True if execution_style == "MAKER_HYBRID" else False,
        maker_queue_timeout_seconds=10.0,
        maker_queue_timeout_action="CANCEL",
        maker_latency_ms=100.0,
        ratchet_enabled=ratchet,
        duration_filter_enabled=duration_filter,
        duration_max_hold_seconds=90.0,
        duration_action="CLOSE"
    )


def run_dual_asset_permutations(skip_cloud: bool = False):
    print("=" * 80)
    print("[*] INITIATING DUAL-ASSET QUANTITATIVE RESEARCH ENGINE V3: TRUMP & DOGE")
    print("=" * 80)

    # 1. DISPATCH REPRESENTATIVE CLOUD JOBS TO GITHUB ACTIONS
    if not skip_cloud:
        print("\n[*] Initializing GitHub Actions Cloud Offloading...")
        dispatcher = CloudMatrixDispatcher()

        cloud_dispatches = [
            # DOGE Key Permutations in Cloud
            ("DOGE_USDT", "STOCH_RSI", 5, 2, True, "MAKER_HYBRID", True),     # DOGE Inverted + Ratchet
            ("DOGE_USDT", "STOCH_RSI", 2, 5, True, "MAKER_HYBRID", False),    # DOGE Inverted 2t/5t
            ("DOGE_USDT", "STOCH_RSI", 10, 2, False, "MAKER_HYBRID", False),  # DOGE Momentum 10t/2t
            ("DOGE_USDT", "EMA_CROSSOVER", 5, 2, False, "MAKER_HYBRID", False), # DOGE EMA 5/13
            # TRUMP Key Permutations in Cloud
            ("TRUMP_USDT", "STOCH_RSI", 2, 5, True, "MAKER_HYBRID", False),   # TRUMP Inverted 2t/5t
            ("TRUMP_USDT", "EMA_CROSSOVER", 2, 5, False, "MAKER_HYBRID", False), # TRUMP EMA 5/13
        ]

        for sym, strat, tp, sl, inv, ex_style, ratch in cloud_dispatches:
            try:
                dispatcher.dispatch_permutation(
                    symbol=sym,
                    strategy=strat,
                    tp_ticks=tp,
                    sl_ticks=sl,
                    invert_signal=inv,
                    execution_style=ex_style,
                    ratchet=ratch,
                    start_date="2026-07-01",
                    end_date="2026-07-14"
                )
                time.sleep(1.5)  # slight pause between dispatch calls
            except Exception as e:
                print(f"[!] Warning on cloud dispatch: {e}")

    # 2. RUN LOCAL HIGH-SPEED EMPIRICAL PERMUTATION ENGINE
    engine = MasterQuantResearchEngineV3()
    is_dates = ("2026-07-01", "2026-07-10")
    oos_dates = ("2026-07-11", "2026-07-14")

    # Output directory for permutation reports
    perms_dir = os.path.join(ROOT_DIR, "AI_ANALYSIS", "Analysis - V3", "permutations")
    os.makedirs(perms_dir, exist_ok=True)
    engine.experiments_dir = perms_dir

    permutations = [
        # --- TRUMP_USDT PERMUTATIONS ---
        {
            "id": "PERM-TRUMP-01",
            "title": "TRUMP Inverted Stoch RSI (2t TP / 5t SL) Maker Hybrid",
            "symbol": "TRUMP_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": True, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-TRUMP-02",
            "title": "TRUMP Direct Stoch RSI Momentum (2t TP / 5t SL) Maker Hybrid",
            "symbol": "TRUMP_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": False, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-TRUMP-03",
            "title": "TRUMP Inverted Stoch RSI Asymmetric (5t TP / 2t SL) Maker Hybrid",
            "symbol": "TRUMP_USDT",
            "strategy": "STOCH_RSI",
            "tp": 5, "sl": 2, "inv": True, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-TRUMP-04",
            "title": "TRUMP EMA Crossover (5/13) (2t TP / 5t SL) Maker Hybrid",
            "symbol": "TRUMP_USDT",
            "strategy": "EMA_CROSSOVER",
            "tp": 2, "sl": 5, "inv": False, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-TRUMP-05",
            "title": "TRUMP Inverted Stoch RSI with Micro-Excursion Tick Ratchet",
            "symbol": "TRUMP_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": True, "exec": "MAKER_HYBRID", "ratchet": True, "dur": False
        },
        {
            "id": "PERM-TRUMP-06",
            "title": "TRUMP Inverted Stoch RSI Pure Market Spread-Crossing Baseline",
            "symbol": "TRUMP_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": True, "exec": "PURE_MARKET", "ratchet": False, "dur": False
        },

        # --- DOGE_USDT PERMUTATIONS ---
        {
            "id": "PERM-DOGE-01",
            "title": "DOGE Inverted Stoch RSI (5t TP / 2t SL) Maker Hybrid Ratchet (V2.2 Spec)",
            "symbol": "DOGE_USDT",
            "strategy": "STOCH_RSI",
            "tp": 5, "sl": 2, "inv": True, "exec": "MAKER_HYBRID", "ratchet": True, "dur": False
        },
        {
            "id": "PERM-DOGE-02",
            "title": "DOGE Inverted Stoch RSI (2t TP / 5t SL) Maker Hybrid (V3 Geometry)",
            "symbol": "DOGE_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": True, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-DOGE-03",
            "title": "DOGE Direct Stoch RSI Momentum Asymmetric (10t TP / 2t SL) Maker Hybrid",
            "symbol": "DOGE_USDT",
            "strategy": "STOCH_RSI",
            "tp": 10, "sl": 2, "inv": False, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-DOGE-04",
            "title": "DOGE Direct Stoch RSI Momentum (2t TP / 5t SL) Maker Hybrid",
            "symbol": "DOGE_USDT",
            "strategy": "STOCH_RSI",
            "tp": 2, "sl": 5, "inv": False, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-DOGE-05",
            "title": "DOGE EMA Crossover (5/13) (5t TP / 2t SL) Maker Hybrid",
            "symbol": "DOGE_USDT",
            "strategy": "EMA_CROSSOVER",
            "tp": 5, "sl": 2, "inv": False, "exec": "MAKER_HYBRID", "ratchet": False, "dur": False
        },
        {
            "id": "PERM-DOGE-06",
            "title": "DOGE Inverted Stoch RSI (5t TP / 2t SL) Pure Market Taker Baseline",
            "symbol": "DOGE_USDT",
            "strategy": "STOCH_RSI",
            "tp": 5, "sl": 2, "inv": True, "exec": "PURE_MARKET", "ratchet": False, "dur": False
        }
    ]

    all_results: List[ExperimentResult] = []

    for p in permutations:
        print("\n" + "=" * 80)
        print(f"[*] EXECUTING PERMUTATION: {p['id']} - {p['title']}")
        print("=" * 80)

        cfg = build_config(
            symbol=p["symbol"],
            strategy=p["strategy"],
            tp_ticks=p["tp"],
            sl_ticks=p["sl"],
            invert_signal=p["inv"],
            execution_style=p["exec"],
            ratchet=p["ratchet"],
            duration_filter=p["dur"]
        )

        math_def = f"""**Permutation Configuration:**
- Asset: `{p['symbol']}` | Strategy: `{p['strategy']}` | Polarity: `{'Inverted (Fade)' if p['inv'] else 'Direct (Momentum)'}`
- Target: `{p['tp']} ticks TP` | Stop: `{p['sl']} ticks SL`
- Execution Style: `{p['exec']}` | Ratchet: `{p['ratchet']}` | Duration Safeguard: `{p['dur']}`
- Leverage: Exactly `75x` | Fee Mode: `0.00% Maker & Taker Zero Fees`
- Tick Trades Data: `Millisecond Tick Trades Stream ENABLED`
"""

        res = engine.execute_experiment(
            experiment_id=p["id"],
            title=p["title"],
            domain=f"Dual-Asset Permutation Matrix: {p['symbol']}",
            mathematical_definition=math_def,
            config=cfg,
            key_insights=[
                f"Evaluated on {p['symbol']} across 14 days of real millisecond tick trades.",
                f"Tested against 4-tier slippage stress matrix with intra-millisecond 75x liquidation checks.",
                f"Walk-forward partitioned into 70% In-Sample and 30% Out-of-Sample."
            ],
            next_mutation=f"Compare {p['symbol']} results against cross-asset baseline.",
            is_date_range=is_dates,
            oos_date_range=oos_dates
        )
        all_results.append(res)

    # 3. PRINT MASTER COMPARATIVE SCORECARD TABLE
    print("\n" + "=" * 100)
    print("[*] MASTER DUAL-ASSET (TRUMP & DOGE) PERMUTATION SCORECARD")
    print("=" * 100)
    print(f"{'Permutation ID':<15} | {'Symbol':<10} | {'Trades':<7} | {'0T PnL':<10} | {'0T WR%':<8} | {'0T PF':<6} | {'0T Sharpe':<9} | {'Liq':<4} | {'OOS PF':<7} | {'RDI':<6}")
    print("-" * 100)

    for r in all_results:
        t0 = r.tier_results["0T (Maker)"]
        sym = r.parameters.get("symbol", "")
        oos_pf = r.oos_metrics.get("pf", 0.0)
        print(f"{r.experiment_id:<15} | {sym:<10} | {t0.total_trades:<7} | {t0.net_pnl_usdt:+10.4f} | {t0.win_rate_pct:7.2f}% | {t0.profit_factor:6.2f} | {t0.sharpe_ratio:9.2f} | {t0.liquidations:<4} | {oos_pf:7.2f} | {r.rdi:6.2f}")

    print("=" * 100)
    print(f"[+] All permutation reports successfully written to: {perms_dir}")


if __name__ == "__main__":
    skip = "--skip-cloud" in sys.argv
    run_dual_asset_permutations(skip_cloud=skip)
