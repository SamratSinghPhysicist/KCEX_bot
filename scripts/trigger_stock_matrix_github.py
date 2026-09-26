"""
GitHub Actions Stock Matrix Workflow Dispatcher, Live Monitor & Local Downloader
================================================================================
Automates the complete cloud backtesting pipeline for Top 50 US Equities:
1. Dispatches the GitHub Actions distributed workflow (`stock_backtest_matrix.yml`).
2. Streams live progress of parallel matrix workers across GitHub cloud runners.
3. Automatically downloads and unpacks all worker artifacts (trades CSVs, JSONs).
4. Organizes everything locally into `stock_backtest_local_results/`.

Usage:
  # Trigger full 50-stock matrix backtest (or specific batch) and auto-download results:
  python scripts/trigger_stock_matrix_github.py --stocks BATCH_1 --auto-download
  python scripts/trigger_stock_matrix_github.py --stocks ALL --auto-download
  python scripts/trigger_stock_matrix_github.py --stocks AAPL,TSLA,NVDA --auto-download
"""

from __future__ import annotations
import os
import sys
import io
import time
import json
import zipfile
import shutil
import argparse
import requests
from typing import Optional, Dict, Any, List

# Reconfigure stdout/stderr for utf-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import (
    resolve_github_token,
    get_git_remote_repo,
    Style
)

WORKFLOW_FILENAME = "stock_backtest_matrix.yml"
DEFAULT_TARGET_DIR = "stock_backtest_local_results"


class GitHubStockMatrixRunner:
    def __init__(self, token: Optional[str] = None):
        self.owner, self.repo = get_git_remote_repo()
        self.token = resolve_github_token(token)
        if not self.token:
            print(f"{Style.RED}[!] Error: No GitHub Personal Access Token found.{Style.RESET}")
            print("    Please set GITHUB_TOKEN in your environment or in KCEX .env file.")
            sys.exit(1)
        self.api_base = f"https://api.github.com/repos/{self.owner}/{self.repo}"

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "KCEX-Stock-Matrix-Runner"
        }

    def get_default_branch(self) -> str:
        """Fetches default branch of the repository."""
        url = self.api_base
        resp = requests.get(url, headers=self.headers, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("default_branch", "main")
        return "main"

    def dispatch(
        self,
        stocks: str = "ALL",
        timeframes: str = "ALL",
        fees: str = "ALL",
        slippages: str = "ALL",
        leverage: str = "15",
        margin_pct: str = "10.0",
        capital: str = "100.0",
        lookback_years: str = "15",
        ref: Optional[str] = None
    ) -> Optional[int]:
        """Dispatches workflow_dispatch event and returns the triggered run ID."""
        branch = ref or self.get_default_branch()
        url = f"{self.api_base}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"

        inputs = {
            "stocks": stocks,
            "timeframes": timeframes,
            "fees": fees,
            "slippages": slippages,
            "leverage": str(leverage),
            "margin_pct": str(margin_pct),
            "capital": str(capital),
            "lookback_years": str(lookback_years)
        }

        print(f"\n{Style.BOLD}{Style.CYAN}{'=' * 80}{Style.RESET}")
        print(f"{Style.BOLD}🚀 DISPATCHING TOP 50 US EQUITIES BACKTEST MATRIX TO GITHUB ACTIONS{Style.RESET}")
        print(f"   Repository:      {self.owner}/{self.repo} (Branch: {branch})")
        print(f"   Target Stocks:   {stocks}")
        print(f"   Timeframes:      {timeframes}")
        print(f"   Fee Schedules:   {fees}")
        print(f"   Slippages:       {slippages}")
        print(f"   Leverage:        {leverage}x Isolated | Margin: {margin_pct}% Compounding")
        print(f"   Lookback:        {lookback_years} years (Daily)")
        print(f"{Style.BOLD}{Style.CYAN}{'=' * 80}{Style.RESET}\n")

        t_dispatch = time.time()
        resp = requests.post(url, headers=self.headers, json={"ref": branch, "inputs": inputs}, timeout=20)

        if resp.status_code not in (204, 201, 200):
            print(f"{Style.RED}[!] Failed to dispatch workflow: HTTP {resp.status_code} - {resp.text}{Style.RESET}")
            return None

        print(f"{Style.GREEN}[+] Workflow successfully dispatched! Locating run ID...{Style.RESET}")

        # Poll for newest run ID created within last 60s
        for _ in range(15):
            time.sleep(3.0)
            runs_url = f"{self.api_base}/actions/workflows/{WORKFLOW_FILENAME}/runs?per_page=5"
            r_resp = requests.get(runs_url, headers=self.headers, timeout=15)
            if r_resp.status_code == 200:
                runs = r_resp.json().get("workflow_runs", [])
                for run in runs:
                    created_at_s = run.get("created_at")
                    # Match recently created run
                    run_id = run.get("id")
                    status = run.get("status")
                    if status in ("queued", "in_progress", "waiting"):
                        print(f"{Style.GREEN}[+] Detected active Run #{run_id} ({run.get('html_url')}){Style.RESET}")
                        return run_id

        print(f"{Style.YELLOW}[!] Workflow triggered, but could not automatically detect Run ID. Please check repository Actions tab.{Style.RESET}")
        return None

    def monitor(self, run_id: int, poll_interval_sec: int = 30) -> bool:
        """Polls run progress and prints live matrix status."""
        run_url = f"{self.api_base}/actions/runs/{run_id}"
        jobs_url = f"{self.api_base}/actions/runs/{run_id}/jobs?per_page=100"

        print(f"\n[*] Monitoring execution for Run #{run_id} (polling every {poll_interval_sec}s)...")
        start_time = time.time()
        last_completed = -1
        last_status = ""
        last_print_time = 0.0

        while True:
            try:
                r_resp = requests.get(run_url, headers=self.headers, timeout=15)
                if r_resp.status_code != 200:
                    time.sleep(poll_interval_sec)
                    continue

                run_data = r_resp.json()
                status = run_data.get("status")
                conclusion = run_data.get("conclusion")
                elapsed = int(time.time() - start_time)

                # Fetch jobs
                j_resp = requests.get(jobs_url, headers=self.headers, timeout=15)
                jobs = j_resp.json().get("jobs", []) if j_resp.status_code == 200 else []

                completed_jobs = sum(1 for j in jobs if j.get("status") == "completed")
                total_jobs = len(jobs)

                now = time.time()
                if (completed_jobs != last_completed or 
                    status != last_status or 
                    now - last_print_time >= 60.0 or 
                    status == "completed"):
                    print(f"[{elapsed//60:02d}:{elapsed%60:02d}] Run Status: {status.upper()} | Jobs Completed: {completed_jobs}/{total_jobs}")
                    last_completed = completed_jobs
                    last_status = status
                    last_print_time = now

                if status == "completed":
                    if conclusion == "success":
                        print(f"\n{Style.GREEN}{Style.BOLD}🎉 ALL CLOUD BACKTEST RUNNERS COMPLETED SUCCESSFULLY!{Style.RESET}")
                        return True
                    else:
                        print(f"\n{Style.YELLOW}{Style.BOLD}[!] Workflow completed with conclusion: {conclusion.upper()}{Style.RESET}")
                        return True

            except Exception as e:
                print(f"    [!] Error during polling: {e}")

            time.sleep(poll_interval_sec)

    def download_and_extract_artifacts(self, run_id: int, target_dir: str = DEFAULT_TARGET_DIR) -> None:
        """Downloads all artifact ZIPs via GitHub REST API, extracts and organizes them locally."""
        url = f"{self.api_base}/actions/runs/{run_id}/artifacts?per_page=100"
        resp = requests.get(url, headers=self.headers, timeout=15)
        if resp.status_code != 200:
            print(f"{Style.RED}[!] Could not fetch artifacts list: HTTP {resp.status_code} - {resp.text}{Style.RESET}")
            return

        artifacts = resp.json().get("artifacts", [])
        if not artifacts:
            print(f"{Style.YELLOW}[!] No artifacts found for Run #{run_id}.{Style.RESET}")
            return

        print(f"\n{Style.CYAN}[*] Discovered {len(artifacts)} artifact archives for Run #{run_id}. Downloading...{Style.RESET}")

        trades_dir = os.path.join(target_dir, "trades_csv")
        summaries_dir = os.path.join(target_dir, "summaries")
        reports_dir = os.path.join(target_dir, "consolidated_reports")

        os.makedirs(trades_dir, exist_ok=True)
        os.makedirs(summaries_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)

        csv_count = 0
        json_count = 0
        report_count = 0

        for art in artifacts:
            name = art.get("name")
            download_url = art.get("archive_download_url")
            size_mb = art.get("size_in_bytes", 0) / (1024 * 1024)

            print(f"    ⬇️ Downloading '{name}' ({size_mb:.2f} MB)...", end="", flush=True)
            dl_resp = requests.get(download_url, headers=self.headers, stream=True, timeout=60)
            if dl_resp.status_code != 200:
                print(f" ❌ HTTP {dl_resp.status_code}")
                continue

            try:
                with zipfile.ZipFile(io.BytesIO(dl_resp.content)) as zf:
                    for filename in zf.namelist():
                        file_data = zf.read(filename)
                        base_fn = os.path.basename(filename)

                        if base_fn.startswith("trades_") and base_fn.endswith(".csv"):
                            dest = os.path.join(trades_dir, base_fn)
                            with open(dest, "wb") as f_out:
                                f_out.write(file_data)
                            csv_count += 1

                        elif base_fn.startswith("summary_") and base_fn.endswith(".json"):
                            dest = os.path.join(summaries_dir, base_fn)
                            with open(dest, "wb") as f_out:
                                f_out.write(file_data)
                            json_count += 1

                        elif "matrix" in base_fn or "report" in base_fn or "champion" in base_fn:
                            dest = os.path.join(reports_dir, base_fn)
                            with open(dest, "wb") as f_out:
                                f_out.write(file_data)
                            report_count += 1
                print(" ✅")
            except Exception as e:
                print(f" ❌ Error unzipping: {e}")

        print(f"\n{Style.GREEN}{Style.BOLD}[🎉] All artifacts downloaded and organized locally in '{target_dir}':{Style.RESET}")
        print(f"     📊 Detailed Trades CSVs:  {csv_count} files -> {trades_dir}")
        print(f"     📋 Scenario JSON Summaries: {json_count} files -> {summaries_dir}")
        print(f"     🏛️ Consolidated Reports:   {report_count} files -> {reports_dir}\n")


def main():
    parser = argparse.ArgumentParser(description="Trigger & Monitor GitHub Actions Stock Matrix Backtest")
    parser.add_argument("--stocks", type=str, default="ALL",
                        help="Target stocks: 'ALL', 'BATCH_1'..'BATCH_5', or comma-separated e.g. 'AAPL,NVDA,TSLA'")
    parser.add_argument("--timeframes", type=str, default="ALL",
                        help="Timeframes: 'ALL' or comma-separated e.g. '1m,3m,5m,15m,30m,1h,4h,1d'")
    parser.add_argument("--fees", type=str, default="ALL",
                        help="Fee tiers: 'ALL' or comma-separated e.g. 'tier1,tier2,tier3'")
    parser.add_argument("--slippages", type=str, default="ALL",
                        help="Slippages in ticks: 'ALL' (1-7) or comma-separated e.g. '1,2,3'")
    parser.add_argument("--leverage", type=str, default="15", help="Leverage multiplier (default: 15)")
    parser.add_argument("--margin-pct", type=str, default="10.0", help="Compounding margin percentage (default: 10.0)")
    parser.add_argument("--capital", type=str, default="100.0", help="Initial capital in USDT (default: 100.0)")
    parser.add_argument("--lookback-years", type=str, default="15", help="Max lookback years (default: 15)")
    parser.add_argument("--auto-download", action="store_true", help="Automatically monitor and download artifacts")
    parser.add_argument("--download-only", type=int, default=None, help="Download artifacts for an existing run ID")
    parser.add_argument("--target-dir", type=str, default=DEFAULT_TARGET_DIR, help="Local directory for downloaded results")

    args = parser.parse_args()

    runner = GitHubStockMatrixRunner()

    if args.download_only:
        runner.download_and_extract_artifacts(args.download_only, target_dir=args.target_dir)
        return

    run_id = runner.dispatch(
        stocks=args.stocks,
        timeframes=args.timeframes,
        fees=args.fees,
        slippages=args.slippages,
        leverage=args.leverage,
        margin_pct=args.margin_pct,
        capital=args.capital,
        lookback_years=args.lookback_years
    )

    if not run_id:
        sys.exit(1)

    if args.auto_download:
        success = runner.monitor(run_id)
        if success:
            runner.download_and_extract_artifacts(run_id, target_dir=args.target_dir)


if __name__ == "__main__":
    main()
