"""
Stock Backtest Artifacts Downloader & Local Organizer
=====================================================
Downloads all artifact zips from a completed GitHub Actions stock backtest run,
extracts them locally, and organizes trades CSVs, JSON summaries, and consolidated reports
into a dedicated local directory.

Usage:
  python scripts/download_stock_matrix_results.py --run-id <RUN_ID>
  python scripts/download_stock_matrix_results.py --latest
"""

from __future__ import annotations
import os
import sys
import json
import zipfile
import shutil
import subprocess
import urllib.request
import argparse
from typing import Optional, Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_SLUG = "SamratSinghPhysicist/KCEX_bot"
DEFAULT_TARGET_DIR = "stock_backtest_local_results"


def get_latest_workflow_run_id() -> Optional[int]:
    """Uses gh CLI or GitHub REST API to get latest run ID of stock_backtest_matrix.yml."""
    try:
        cmd = ["gh", "run", "list", "--workflow=stock_backtest_matrix.yml", "--limit=1", "--json=databaseId,status,conclusion"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        if data and len(data) > 0:
            return data[0]["databaseId"]
    except Exception:
        pass

    # Public REST API fallback
    try:
        url = f"https://api.github.com/repos/{REPO_SLUG}/actions/workflows/stock_backtest_matrix.yml/runs?per_page=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            runs = data.get("workflow_runs", [])
            if runs:
                return runs[0]["id"]
    except Exception as e:
        print(f"[!] Could not query latest run from GitHub: {e}")

    return None


def download_run_artifacts(run_id: int, target_dir: str = DEFAULT_TARGET_DIR) -> None:
    """Downloads all artifacts for a run using gh CLI."""
    os.makedirs(target_dir, exist_ok=True)
    temp_zip_dir = os.path.join(target_dir, "_raw_zips")
    os.makedirs(temp_zip_dir, exist_ok=True)

    print(f"[*] Downloading artifacts for GitHub Actions Run #{run_id}...")

    # Attempt download via gh CLI
    download_success = False
    try:
        cmd = ["gh", "run", "download", str(run_id), "--dir", temp_zip_dir]
        subprocess.run(cmd, check=True)
        download_success = True
    except Exception as e:
        print(f"[!] 'gh run download' encountered an error: {e}")

    if not download_success:
        try:
            from scripts.trigger_stock_matrix_github import GitHubStockMatrixRunner
            runner = GitHubStockMatrixRunner()
            runner.download_and_extract_artifacts(run_id, target_dir)
            return
        except Exception as e:
            print(f"[!] Please ensure GitHub CLI ('gh') is authenticated, or GITHUB_TOKEN is set: {e}")
            print(f"    Manual download URL: https://github.com/{REPO_SLUG}/actions/runs/{run_id}")
            return

    # Organize files
    trades_dir = os.path.join(target_dir, "trades_csv")
    summaries_dir = os.path.join(target_dir, "summaries")
    reports_dir = os.path.join(target_dir, "consolidated_reports")

    os.makedirs(trades_dir, exist_ok=True)
    os.makedirs(summaries_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    extracted_count = 0
    for root, _, files in os.walk(temp_zip_dir):
        for f in files:
            src = os.path.join(root, f)
            if f.endswith(".zip"):
                try:
                    with zipfile.ZipFile(src, 'r') as zf:
                        zf.extractall(temp_zip_dir)
                    extracted_count += 1
                except Exception:
                    pass

    # Copy categorized files
    csv_count = 0
    json_count = 0
    report_count = 0

    for root, _, files in os.walk(temp_zip_dir):
        for f in files:
            src = os.path.join(root, f)
            if f.startswith("trades_") and f.endswith(".csv"):
                shutil.copy2(src, os.path.join(trades_dir, f))
                csv_count += 1
            elif f.startswith("summary_") and f.endswith(".json"):
                shutil.copy2(src, os.path.join(summaries_dir, f))
                json_count += 1
            elif "matrix" in f or "report" in f or "champion" in f:
                shutil.copy2(src, os.path.join(reports_dir, f))
                report_count += 1

    # Cleanup raw folder
    shutil.rmtree(temp_zip_dir, ignore_errors=True)

    print(f"\n[🎉] Artifacts successfully organized in '{target_dir}':")
    print(f"     Trades CSVs:        {csv_count} files -> {trades_dir}")
    print(f"     JSON Summaries:     {json_count} files -> {summaries_dir}")
    print(f"     Consolidated Reports: {report_count} files -> {reports_dir}\n")


def main():
    parser = argparse.ArgumentParser(description="Download GitHub Actions Stock Matrix Results")
    parser.add_argument("--run-id", type=int, default=None, help="GitHub Actions Run ID")
    parser.add_argument("--latest", action="store_true", help="Download from latest workflow run")
    parser.add_argument("--target-dir", type=str, default=DEFAULT_TARGET_DIR, help="Local directory to store results")

    args = parser.parse_args()

    run_id = args.run_id
    if not run_id or args.latest:
        run_id = get_latest_workflow_run_id()

    if not run_id:
        print("[!] No Run ID provided and could not auto-detect latest run.")
        print("    Usage: python scripts/download_stock_matrix_results.py --run-id <RUN_ID>")
        sys.exit(1)

    download_run_artifacts(run_id, target_dir=args.target_dir)


if __name__ == "__main__":
    main()
