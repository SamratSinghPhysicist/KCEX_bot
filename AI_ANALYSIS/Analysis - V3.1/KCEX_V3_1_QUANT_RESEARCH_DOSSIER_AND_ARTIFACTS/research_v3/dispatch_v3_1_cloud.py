"""
Dispatch V3.1 Pure Market Slippage Immunization Matrix to GitHub Actions
========================================================================
Offloads pure market taker slippage stress tests across TRUMP and DOGE
to GitHub Actions cloud runners with ticker trades enabled.
"""

import os
import sys
import time
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import GitHubBacktestRunner

def dispatch_cloud_v3_1():
    runner = GitHubBacktestRunner()
    print("=" * 80)
    print("[*] DISPATCHING V3.1 PURE MARKET SLIPPAGE CLOUD RUNS TO GITHUB ACTIONS")
    print(f"[*] Repository: {runner.owner}/{runner.repo}")
    print("=" * 80)

    # Matrix of Pure Market Taker permutations with slippage
    permutations = [
        # TRUMP Direct 8t/4t 1T Slippage
        {
            "symbol": "TRUMP_USDT", "strategy": "STOCH_RSI", "tp": 8, "sl": 4,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 1,
            "desc": "TRUMP Direct 8t/4t Market 1T Slippage"
        },
        # TRUMP Direct 8t/4t 2T Slippage
        {
            "symbol": "TRUMP_USDT", "strategy": "STOCH_RSI", "tp": 8, "sl": 4,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 2,
            "desc": "TRUMP Direct 8t/4t Market 2T Slippage"
        },
        # TRUMP Direct 8t/4t + Ratchet 1T Slippage
        {
            "symbol": "TRUMP_USDT", "strategy": "STOCH_RSI", "tp": 8, "sl": 4,
            "invert": False, "style": "PURE_MARKET", "ratchet": True, "slip": 1,
            "desc": "TRUMP Direct 8t/4t + Ratchet Market 1T Slippage"
        },
        # TRUMP EMA 5/13 8t/4t 1T Slippage
        {
            "symbol": "TRUMP_USDT", "strategy": "EMA_CROSSOVER", "tp": 8, "sl": 4,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 1,
            "desc": "TRUMP EMA 5/13 8t/4t Market 1T Slippage"
        },
        # DOGE Asymmetric 10t/2t 1T Slippage
        {
            "symbol": "DOGE_USDT", "strategy": "STOCH_RSI", "tp": 10, "sl": 2,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 1,
            "desc": "DOGE Direct Asymmetric 10t/2t Market 1T Slippage"
        },
        # DOGE Asymmetric 10t/2t 2T Slippage
        {
            "symbol": "DOGE_USDT", "strategy": "STOCH_RSI", "tp": 10, "sl": 2,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 2,
            "desc": "DOGE Direct Asymmetric 10t/2t Market 2T Slippage"
        },
        # DOGE Inverted 5t/2t + Ratchet 1T Slippage
        {
            "symbol": "DOGE_USDT", "strategy": "STOCH_RSI", "tp": 5, "sl": 2,
            "invert": True, "style": "PURE_MARKET", "ratchet": True, "slip": 1,
            "desc": "DOGE Inverted 5t/2t + Ratchet Market 1T Slippage"
        },
        # DOGE EMA 5/13 6t/2t 1T Slippage
        {
            "symbol": "DOGE_USDT", "strategy": "EMA_CROSSOVER", "tp": 6, "sl": 2,
            "invert": False, "style": "PURE_MARKET", "ratchet": False, "slip": 1,
            "desc": "DOGE EMA 5/13 6t/2t Market 1T Slippage"
        }
    ]

    dispatched = 0
    for p in permutations:
        vol_multiplier = "2.0" if "TRUMP" in p["symbol"] else "1.0"
        
        quant_dict = {
            "invert_signal": p["invert"],
            "enable_slippage": (p["slip"] > 0),
            "slippage_ticks": p["slip"],
            "ratchet": p["ratchet"],
            "ratchet_trigger_ticks": 2.0 if p["tp"] >= 6 else 1.0,
            "ratchet_stall_seconds": 10.0,
            "ratchet_tighten_ticks": 1.0,
            "ratchet_breakeven_ticks": 3.0 if p["tp"] >= 6 else 2.5,
            "execution_style": p["style"]
        }

        filters_dict = {
            "duration_filter": False,
            "duration_deep_monitor": 60.0,
            "duration_max_hold": 90.0,
            "duration_action": "CLOSE",
            "adx_filter": False,
            "htf_trend_filter": False,
            "hourly_filter": False,
            "direction_bias": "BOTH"
        }

        inputs = {
            "symbol": p["symbol"],
            "timeframe": "1m",
            "strategy": p["strategy"],
            "ema_preset": "5/13",
            "stoch_preset": "FAST_SCALP",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
            "use_ticks": "true",
            "fee_mode": "ZERO",
            "maker_fee": "0.0",
            "taker_fee": "0.0",
            "volume_mode": "MULTIPLIER",
            "volume_contracts": "2",
            "volume_multiplier": vol_multiplier,
            "tp_ticks": str(p["tp"]),
            "sl_mode": "TICKS",
            "sl_ticks": str(p["sl"]),
            "sl_roe": "25.0",
            "sl_price": "0.5",
            "leverage": "75",
            "capital": "100.0",
            "max_trades": "0",
            "filters_json": json.dumps(filters_dict),
            "quant_params_json": json.dumps(quant_dict)
        }

        print(f"[*] Dispatching: {p['desc']} ...")
        success = runner.dispatch_workflow(inputs)
        if success:
            print(f"    [+] Successfully dispatched to GitHub Actions runner.")
            dispatched += 1
        else:
            print(f"    [-] Failed to dispatch.")
        time.sleep(2)  # Prevent API rate limiting

    print(f"\n[OK] Completed dispatching {dispatched}/{len(permutations)} cloud runs to GitHub Actions.")

if __name__ == "__main__":
    dispatch_cloud_v3_1()
