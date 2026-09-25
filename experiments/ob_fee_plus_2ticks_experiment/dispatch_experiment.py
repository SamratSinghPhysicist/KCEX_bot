"""
Experiment GitHub Actions Dispatcher & Monitor
===============================================
Dispatches the Fee Coverage + 2 Ticks OB Experiment workflows on GitHub Actions,
monitors parallel worker execution in real-time, and automatically downloads and
consolidates the detailed matrix CSVs, markdown reports, and detailed trades CSVs.
"""

from __future__ import annotations
import os
import sys
import time
import json
import zipfile
import argparse
import requests
from typing import List, Dict, Any, Optional

# Ensure utf-8 output encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import (
    resolve_github_token,
    get_git_remote_repo,
    Style
)

WORKFLOW_SINGLE_PAIR = "experiment_fee_plus_2ticks.yml"
WORKFLOW_ALL_COINS = "experiment_fee_plus_2ticks_all_coins.yml"

TARGET_COINS = [
    "BTC_USDT",
    "TRUMP_USDT",
    "1000000MOG_USDT",
    "DOGE_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XAU_USDT",
    "XAG_USDT",
    "CL_USDT",
    "XRP_USDT"
]

REPORTS_DIR = os.path.join(EXPERIMENT_DIR, "reports")


class ExperimentGitHubDispatcher:
    def __init__(self, token: Optional[str] = None):
        self.owner, self.repo = get_git_remote_repo()
        self.token = resolve_github_token(token)
        self.api_base = f"https://api.github.com/repos/{self.owner}/{self.repo}"

    @property
    def headers(self) -> Dict[str, str]:
        hdrs = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KCEX-Experiment-Dispatcher"
        }
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        return hdrs

    def dispatch_single_coin(
        self,
        symbol: str,
        start_date: str = "2026-01-01",
        end_date: str = "2026-08-31",
        extra_ticks: int = 2,
        capital: float = 100.0,
        leverage: int = 10,
        margin_pct: float = 10.0,
        ref: str = "main"
    ) -> Optional[int]:
        """Dispatches a deep 7-worker workflow run for a single coin."""
        url = f"{self.api_base}/actions/workflows/{WORKFLOW_SINGLE_PAIR}/dispatches"
        payload = {
            "ref": ref,
            "inputs": {
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "extra_ticks": str(extra_ticks),
                "capital": str(capital),
                "leverage": str(leverage),
                "margin_pct": str(margin_pct)
            }
        }
        resp = requests.post(url, headers=self.headers, json=payload, timeout=15)
        if resp.status_code != 204:
            print(f"{Style.RED}[!] Dispatch failed for {symbol}: HTTP {resp.status_code} - {resp.text}{Style.RESET}")
            return None

        time.sleep(2)
        runs_url = f"{self.api_base}/actions/workflows/{WORKFLOW_SINGLE_PAIR}/runs?event=workflow_dispatch&per_page=5"
        for _ in range(8):
            try:
                r = requests.get(runs_url, headers=self.headers, timeout=10)
                if r.status_code == 200:
                    runs = r.json().get("workflow_runs", [])
                    if runs:
                        latest = runs[0]
                        run_id = latest.get("id")
                        print(f"  {Style.GREEN}✓ Dispatched {symbol:15s} -> Run #{run_id} ({latest.get('html_url')}){Style.RESET}")
                        return run_id
            except Exception:
                pass
            time.sleep(1.5)

        print(f"  {Style.YELLOW}⚠️ Dispatched {symbol} but could not immediately capture Run ID.{Style.RESET}")
        return None

    def dispatch_all_coins(
        self,
        start_date: str = "2026-01-01",
        end_date: str = "2026-08-31",
        extra_ticks: int = 2,
        timeframes: str = "1m,5m,15m,1h,4h,1d",
        capital: float = 100.0,
        leverage: int = 10,
        margin_pct: float = 10.0,
        ref: str = "main"
    ) -> Optional[int]:
        """Dispatches the 10-coin parallel matrix workflow."""
        url = f"{self.api_base}/actions/workflows/{WORKFLOW_ALL_COINS}/dispatches"
        payload = {
            "ref": ref,
            "inputs": {
                "start_date": start_date,
                "end_date": end_date,
                "extra_ticks": str(extra_ticks),
                "timeframes": timeframes,
                "capital": str(capital),
                "leverage": str(leverage),
                "margin_pct": str(margin_pct)
            }
        }
        resp = requests.post(url, headers=self.headers, json=payload, timeout=15)
        if resp.status_code != 204:
            print(f"{Style.RED}[!] Dispatch failed for all coins: HTTP {resp.status_code} - {resp.text}{Style.RESET}")
            return None

        time.sleep(2)
        runs_url = f"{self.api_base}/actions/workflows/{WORKFLOW_ALL_COINS}/runs?event=workflow_dispatch&per_page=5"
        for _ in range(8):
            try:
                r = requests.get(runs_url, headers=self.headers, timeout=10)
                if r.status_code == 200:
                    runs = r.json().get("workflow_runs", [])
                    if runs:
                        latest = runs[0]
                        run_id = latest.get("id")
                        print(f"  {Style.GREEN}✓ Dispatched All-Coins Matrix -> Run #{run_id} ({latest.get('html_url')}){Style.RESET}")
                        return run_id
            except Exception:
                pass
            time.sleep(1.5)

        return None

    def monitor_and_download(
        self,
        run_id: int,
        dest_dir: str = REPORTS_DIR,
        poll_interval: int = 15
    ) -> bool:
        """Monitors a single workflow run and downloads its artifacts."""
        os.makedirs(dest_dir, exist_ok=True)
        t_start = time.time()
        print(f"\n{Style.CYAN}▶ Monitoring Workflow Run #{run_id}...{Style.RESET}\n")

        while True:
            time.sleep(poll_interval)
            elapsed = time.time() - t_start
            m = int(elapsed // 60)
            s = int(elapsed % 60)

            try:
                r = requests.get(f"{self.api_base}/actions/runs/{run_id}", headers=self.headers, timeout=10)
                if r.status_code == 200:
                    d = r.json()
                    status = d.get("status")
                    conclusion = d.get("conclusion")
                    print(f"\r  [{m:02d}:{s:02d}] Status: {status} | Conclusion: {conclusion or 'in_progress'}", end="", flush=True)

                    if status == "completed":
                        print(f"\n{Style.GREEN}✓ Run #{run_id} completed with status: {conclusion}{Style.RESET}")
                        self._download_run_artifacts(run_id, dest_dir)
                        return conclusion == "success"
            except Exception as e:
                print(f"\n[!] Error polling run #{run_id}: {e}")

    def _download_run_artifacts(self, run_id: int, dest_dir: str) -> None:
        """Downloads and extracts all artifacts for a run."""
        art_url = f"{self.api_base}/actions/runs/{run_id}/artifacts"
        r = requests.get(art_url, headers=self.headers, timeout=15)
        if r.status_code != 200:
            print(f"[!] Could not list artifacts: HTTP {r.status_code}")
            return

        artifacts = r.json().get("artifacts", [])
        print(f"\n[*] Found {len(artifacts)} artifact packages for run #{run_id}.")

        for art in artifacts:
            name = art["name"]
            dl_url = art["archive_download_url"]
            print(f"  Downloading artifact: {name} ...")
            ar = requests.get(dl_url, headers=self.headers, timeout=60)
            if ar.status_code == 200:
                import io
                with zipfile.ZipFile(io.BytesIO(ar.content)) as zf:
                    zf.extractall(dest_dir)
                print(f"    {Style.GREEN}✓ Extracted {name} to {dest_dir}{Style.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Experiment GitHub Actions Dispatcher")
    parser.add_argument("--symbol", type=str, default="ALL", help="Target coin symbol or 'ALL'")
    parser.add_argument("--start", type=str, default="2026-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2026-08-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--extra-ticks", type=int, default=2, help="Extra profit ticks")
    parser.add_argument("--timeframes", type=str, default="1m,5m,15m,1h,4h,1d", help="Timeframes")
    parser.add_argument("--capital", type=float, default=100.0, help="Initial capital in USDT")
    parser.add_argument("--leverage", type=int, default=10, help="Leverage multiplier")
    parser.add_argument("--margin-pct", type=float, default=10.0, help="Margin % per trade")
    parser.add_argument("--monitor", action="store_true", help="Monitor workflow until completion and download artifacts")
    parser.add_argument("--token", type=str, default=None, help="GitHub Personal Access Token")

    args = parser.parse_args()

    dispatcher = ExperimentGitHubDispatcher(token=args.token)

    if args.symbol.upper() == "ALL":
        print(f"\n[*] Dispatching All-Coins Parallel Matrix...")
        run_id = dispatcher.dispatch_all_coins(
            start_date=args.start,
            end_date=args.end,
            extra_ticks=args.extra_ticks,
            timeframes=args.timeframes,
            capital=args.capital,
            leverage=args.leverage,
            margin_pct=args.margin_pct
        )
        if run_id and args.monitor:
            dispatcher.monitor_and_download(run_id)
    else:
        print(f"\n[*] Dispatching Single Coin Deep Split for {args.symbol}...")
        run_id = dispatcher.dispatch_single_coin(
            symbol=args.symbol,
            start_date=args.start,
            end_date=args.end,
            extra_ticks=args.extra_ticks,
            capital=args.capital,
            leverage=args.leverage,
            margin_pct=args.margin_pct
        )
        if run_id and args.monitor:
            dispatcher.monitor_and_download(run_id)


if __name__ == "__main__":
    main()
