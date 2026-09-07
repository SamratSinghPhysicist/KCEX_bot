"""
Cloud Artifacts Downloader & Parser for GitHub Actions Runs
============================================================
Downloads, extracts, and summarizes artifacts from completed GitHub Actions runs.
"""

import os
import sys
import io
import zipfile
import requests

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.github_runner import GitHubBacktestRunner


def download_all_recent_artifacts(count: int = 10, output_dir: str = "BACKTESTER/cloud_reports"):
    runner = GitHubBacktestRunner()
    os.makedirs(output_dir, exist_ok=True)

    # 1. Fetch recent runs
    runs_url = f"{runner.api_base}/actions/runs?per_page={count}"
    runs_resp = requests.get(runs_url, headers=runner.headers, timeout=10)
    if runs_resp.status_code != 200:
        print(f"[!] Failed to fetch runs: HTTP {runs_resp.status_code}")
        return

    runs = runs_resp.json().get("workflow_runs", [])
    print(f"[*] Found {len(runs)} recent workflow runs.")

    for r in runs:
        rid = r["id"]
        status = r["status"]
        conclusion = r.get("conclusion")
        title = r.get("display_title")
        created = r.get("created_at")

        print(f"\n--- Workflow Run #{rid} ({title}) | {status} ({conclusion}) ---")
        if conclusion != "success":
            print(f"    Skipping non-successful run.")
            continue

        arts_url = f"{runner.api_base}/actions/runs/{rid}/artifacts"
        arts_resp = requests.get(arts_url, headers=runner.headers, timeout=10)
        if arts_resp.status_code != 200:
            continue

        artifacts = arts_resp.json().get("artifacts", [])
        if not artifacts:
            print(f"    No artifacts uploaded for run #{rid}")
            continue

        for a in artifacts:
            aid = a["id"]
            aname = a["name"]
            asize = a["size_in_bytes"]
            print(f"    Artifact: {aname} ({asize/1024:.1f} KB)")

            dl_url = f"{runner.api_base}/actions/artifacts/{aid}/zip"
            dl_resp = requests.get(dl_url, headers=runner.headers, stream=True, timeout=60)
            if dl_resp.status_code == 200:
                extract_target = os.path.join(output_dir, f"run_{rid}")
                os.makedirs(extract_target, exist_ok=True)
                with zipfile.ZipFile(io.BytesIO(dl_resp.content)) as zf:
                    zf.extractall(extract_target)
                    print(f"    [+] Extracted {len(zf.namelist())} files to: {extract_target}")
                    for fname in zf.namelist():
                        print(f"        • {fname}")
            else:
                print(f"    [!] Failed to download artifact: HTTP {dl_resp.status_code}")


if __name__ == "__main__":
    download_all_recent_artifacts()
