"""
Cloud Matrix Dispatcher for KCEX Research Engine V3
===================================================
Automates dispatching multi-parameter permutations to GitHub Actions cloud runners
via the authenticated GitHub REST API, monitoring execution, and archiving reports.
"""

import os
import sys
import time
import json
from typing import List, Dict, Any, Optional

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import GitHubBacktestRunner


class CloudMatrixDispatcher:
    """Dispatches and tracks parameter permutation batches on GitHub Actions."""

    def __init__(self, token: Optional[str] = None):
        self.runner = GitHubBacktestRunner(token=token)
        self.dispatched_runs: List[Dict[str, Any]] = []

    def dispatch_permutation(
        self,
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
        leverage: int = 75,
        fee_mode: str = "ZERO"
    ) -> bool:
        """Constructs workflow inputs and dispatches a single permutation run."""
        vol_multiplier = "2.0" if "TRUMP" in symbol.upper() else "1.0"

        quant_dict = {
            "invert_signal": invert_signal,
            "enable_slippage": False,
            "slippage_ticks": 0,
            "ratchet": ratchet,
            "ratchet_trigger_ticks": 1.0,
            "ratchet_stall_seconds": 10.0,
            "ratchet_tighten_ticks": 1.0,
            "ratchet_breakeven_ticks": 2.5,
            "execution_style": execution_style
        }

        filters_dict = {
            "duration_filter": duration_filter,
            "duration_deep_monitor": 60.0,
            "duration_max_hold": 90.0,
            "duration_action": "CLOSE",
            "adx_filter": False,
            "htf_trend_filter": False,
            "hourly_filter": False,
            "direction_bias": "BOTH"
        }

        inputs = {
            "symbol": symbol.upper(),
            "timeframe": "1m",
            "strategy": strategy,
            "ema_preset": ema_preset,
            "stoch_preset": stoch_preset,
            "start_date": start_date,
            "end_date": end_date,
            "use_ticks": "true",
            "fee_mode": fee_mode,
            "maker_fee": "0.0",
            "taker_fee": "0.0",
            "volume_mode": "MULTIPLIER",
            "volume_contracts": "2",
            "volume_multiplier": vol_multiplier,
            "tp_ticks": str(tp_ticks),
            "sl_mode": "TICKS",
            "sl_ticks": str(sl_ticks),
            "sl_roe": "25.0",
            "sl_price": "0.5",
            "leverage": str(leverage),
            "capital": "100.0",
            "max_trades": "0",
            "filters_json": json.dumps(filters_dict),
            "quant_params_json": json.dumps(quant_dict)
        }

        print(f"[*] Dispatching cloud backtest: {symbol} | {strategy} | TP={tp_ticks} SL={sl_ticks} | Inv={invert_signal} | Exec={execution_style} ...")
        success = self.runner.dispatch_workflow(inputs)
        if success:
            print(f"[+] Successfully queued on GitHub Actions: {symbol} ({strategy})")
            self.dispatched_runs.append({
                "symbol": symbol,
                "strategy": strategy,
                "inputs": inputs,
                "dispatched_at": time.time()
            })
            return True
        else:
            print(f"[!] Dispatch failed for {symbol} ({strategy})")
            return False

    def list_recent_cloud_runs(self, count: int = 5):
        """Displays recent GitHub Actions runs."""
        import requests
        url = f"{self.runner.api_base}/actions/runs?per_page={count}"
        try:
            resp = requests.get(url, headers=self.runner.headers, timeout=10)
            if resp.status_code == 200:
                runs = resp.json().get("workflow_runs", [])
                print("\n" + "=" * 80)
                print(f"RECENT GITHUB ACTIONS CLOUD RUNS ({len(runs)} found)")
                print("=" * 80)
                for r in runs:
                    print(f"• ID: {r['id']} | Status: {r['status']} | Conclusion: {r.get('conclusion')} | Name: {r.get('display_title')} | Created: {r.get('created_at')}")
                print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] Error querying cloud runs: {e}")


if __name__ == "__main__":
    dispatcher = CloudMatrixDispatcher()
    dispatcher.list_recent_cloud_runs()
