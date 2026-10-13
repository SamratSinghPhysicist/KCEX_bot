"""
GitHub Actions Dispatcher for Dual-Account Reverse Trading Experiment
====================================================================
Dispatches the GitHub Actions workflow `experiment_btc_eth_reverse.yml`,
monitors its progress in real-time, and downloads resulting artifacts.
"""

from __future__ import annotations
import os
import sys
import time
import argparse
import requests
from typing import Optional, Dict, Any

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import (
    resolve_github_token,
    get_git_remote_repo,
    Style
)

WORKFLOW_FILE = "experiment_btc_eth_reverse.yml"


class ReverseExperimentDispatcher:
    def __init__(self, token: Optional[str] = None):
        self.owner, self.repo = get_git_remote_repo()
        self.token = resolve_github_token(token)
        self.api_base = f"https://api.github.com/repos/{self.owner}/{self.repo}"

    @property
    def headers(self) -> Dict[str, str]:
        hdrs = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KCEX-Reverse-Experiment-Dispatcher"
        }
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        return hdrs

    def dispatch(
        self,
        start_date: str = "2025-01-01",
        end_date: str = "2026-08-31",
        capital: float = 1000.0,
        leverage: float = 2.0,
        fee_rate: float = 0.0004,
        timeframes: str = "1m,5m,15m,1h,4h,1d",
        cases: str = "Case 1,Case 2",
        ref: str = "main"
    ) -> bool:
        """Triggers the workflow via GitHub Actions REST API."""
        url = f"{self.api_base}/actions/workflows/{WORKFLOW_FILE}/dispatches"
        payload = {
            "ref": ref,
            "inputs": {
                "start_date": start_date,
                "end_date": end_date,
                "capital": str(capital),
                "leverage": str(leverage),
                "fee_rate": str(fee_rate),
                "timeframes": timeframes,
                "cases": cases
            }
        }
        print(f"[*] Dispatching workflow '{WORKFLOW_FILE}' to {self.owner}/{self.repo} on branch '{ref}'...")
        resp = requests.post(url, headers=self.headers, json=payload, timeout=15)
        if resp.status_code == 204:
            print(f"{Style.GREEN}[+] Successfully dispatched workflow run on GitHub Actions!{Style.RESET}")
            return True
        else:
            print(f"{Style.RED}[!] Failed to dispatch workflow: HTTP {resp.status_code} - {resp.text}{Style.RESET}")
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dispatch Reverse Experiment on GitHub Actions")
    parser.add_argument("--start-date", type=str, default="2025-01-01")
    parser.add_argument("--end-date", type=str, default="2026-08-31")
    parser.add_argument("--capital", type=float, default=1000.0)
    parser.add_argument("--leverage", type=float, default=2.0)
    parser.add_argument("--timeframes", type=str, default="1m,5m,15m,1h,4h,1d")
    parser.add_argument("--cases", type=str, default="Case 1,Case 2")
    parser.add_argument("--ref", type=str, default="main")
    args = parser.parse_args()

    dispatcher = ReverseExperimentDispatcher()
    dispatcher.dispatch(
        start_date=args.start_date,
        end_date=args.end_date,
        capital=args.capital,
        leverage=args.leverage,
        timeframes=args.timeframes,
        cases=args.cases,
        ref=args.ref
    )
