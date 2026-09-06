import os
import sys
import time
import json
import zipfile
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
import pandas as pd

research_dir = Path(r"d:\My_Bots\Trading\(COPY-SandBoxed) KCEX\ResearchV2")
sys.path.insert(0, str(research_dir))

from BACKTESTER.engine.github_runner import resolve_github_token, get_git_remote_repo

TOKEN = resolve_github_token()
OWNER, REPO = get_git_remote_repo()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
REPORTS_DIR = research_dir / "BACKTESTER" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 14 System Experiments
EXPERIMENTS: Dict[str, Dict[str, Any]] = {
    # Phase 2.1: DOGE 8-Month Sweep
    "DOGE_E0_Base": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "ROE",
        "sl_roe": "25.0",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "DOGE_E1_InvBase": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "ROE",
        "sl_roe": "25.0",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "DOGE_E2_Sym1to1": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "DOGE_E3_InvSym1to1": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "DOGE_E4_Direct10t2t": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "10",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "DOGE_E5_Inv10t2t": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "10",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "DOGE_E6_Inv5t2t": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "5",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "DOGE_E7_SmartSym": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "SMART_STRATEGY",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "DOGE_E8_SmartInvSym": {
        "symbol": "DOGE_USDT",
        "timeframe": "1m",
        "strategy": "SMART_STRATEGY",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "1.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },

    # Phase 2.2: TRUMP 8-Month Sweep
    "TRUMP_T0_Base": {
        "symbol": "TRUMP_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "2.0",
        "tp_ticks": "2",
        "sl_mode": "ROE",
        "sl_roe": "25.0",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "TRUMP_T1_InvBase": {
        "symbol": "TRUMP_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "2.0",
        "tp_ticks": "2",
        "sl_mode": "ROE",
        "sl_roe": "25.0",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "TRUMP_T2_Sym1to1": {
        "symbol": "TRUMP_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "2.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    },
    "TRUMP_T3_InvSym1to1": {
        "symbol": "TRUMP_USDT",
        "timeframe": "1m",
        "strategy": "STOCH_RSI",
        "stoch_preset": "FAST_SCALP",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "2.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "true"
    },
    "TRUMP_T4_SmartSym": {
        "symbol": "TRUMP_USDT",
        "timeframe": "1m",
        "strategy": "SMART_STRATEGY",
        "start_date": "2026-01-01",
        "end_date": "2026-08-31",
        "use_ticks": "false",
        "fee_mode": "ZERO",
        "volume_mode": "MULTIPLIER",
        "volume_multiplier": "2.0",
        "tp_ticks": "2",
        "sl_mode": "TICKS",
        "sl_ticks": "2",
        "leverage": "75",
        "capital": "100.0",
        "max_trades": "0",
        "slippage": "0",
        "invert_signal": "false"
    }
}

def dispatch_workflow(exp_name: str, inputs: Dict[str, Any], ref: str = "main") -> Optional[int]:
    """Sends workflow_dispatch and returns run ID."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/backtest.yml/dispatches"
    payload = {"ref": ref, "inputs": inputs}
    r = requests.post(url, headers=HEADERS, json=payload, timeout=15)
    if r.status_code != 204:
        print(f"[!] Dispatch failed for {exp_name}: HTTP {r.status_code} - {r.text}")
        return None
    
    print(f"[*] Dispatched {exp_name} on {REPO}:{ref}. Waiting for run ID...")
    for _ in range(12):
        time.sleep(2.5)
        runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs?per_page=10"
        rr = requests.get(runs_url, headers=HEADERS, timeout=15)
        if rr.status_code == 200:
            for run in rr.json().get("workflow_runs", []):
                if run.get("head_branch") == ref and run.get("status") in ("queued", "in_progress"):
                    run_id = run["id"]
                    print(f"[+] {exp_name} assigned Run #{run_id}: {run['html_url']}")
                    return run_id
    print(f"[!] Could not locate run ID immediately for {exp_name}")
    return None

def check_run(run_id: int) -> Dict[str, Any]:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        d = r.json()
        return {"id": run_id, "status": d.get("status"), "conclusion": d.get("conclusion"), "url": d.get("html_url")}
    return {"id": run_id, "status": "unknown", "conclusion": None}

def download_run_artifact(run_id: int, exp_name: str) -> Optional[Path]:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/artifacts"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None
    artifacts = r.json().get("artifacts", [])
    if not artifacts:
        print(f"[!] No artifacts found for Run #{run_id}")
        return None
    art = artifacts[0]
    dl_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts/{art['id']}/zip"
    dest_zip = REPORTS_DIR / f"{exp_name}_run{run_id}.zip"
    dl = requests.get(dl_url, headers=HEADERS, stream=True, timeout=60)
    if dl.status_code == 200:
        with open(dest_zip, "wb") as f:
            for chunk in dl.iter_content(65536):
                if chunk:
                    f.write(chunk)
        print(f"[+] Downloaded artifact: {dest_zip.name} ({dest_zip.stat().st_size / 1024:.1f} KB)")
        with zipfile.ZipFile(dest_zip, "r") as z:
            z.extractall(REPORTS_DIR)
        return dest_zip
    return None

def parse_report_summary(md_path: Path) -> Dict[str, Any]:
    """Parses key metrics from generated markdown summary report."""
    text = md_path.read_text(encoding="utf-8")
    
    def extract_val(pattern: str, default: str = "N/A") -> str:
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default

    pnl_m = re.search(r"\*\*Net Realized PnL\*\*\s*\|\s*\*\*`([^`]+)`\*\*", text)
    net_pnl = pnl_m.group(1) if pnl_m else extract_val(r"\*\*Net Realized PnL\*\*\s*\|\s*`?([^`|\n]+)`?")
    
    pf_m = re.search(r"\*\*Profit Factor\*\*\s*\|\s*\*\*`?([^`|\n]+)`?\*\*", text)
    profit_factor = pf_m.group(1) if pf_m else extract_val(r"\*\*Profit Factor\*\*\s*\|\s*`?([^`|\n]+)`?")
    
    wr_m = re.search(r"\*\*Win Rate\*\*\s*\|\s*\*\*`?([^`|\n%]+)%?`?\*\*", text)
    win_rate = wr_m.group(1) if wr_m else extract_val(r"\*\*Win Rate\*\*\s*\|\s*`?([^`|\n%]+)%?`?")
    
    dd_m = re.search(r"\*\*Max Drawdown\*\*\s*\|\s*`?[^`|\n]+`?\s*\|\s*[^|]+\|\s*\*\*`?([^`|\n]+)`?\*\*", text)
    max_dd = dd_m.group(1) if dd_m else extract_val(r"\*\*Max Drawdown\*\*\s*\|\s*`?([^`|\n]+)`?")
    
    trades_m = re.search(r"`(\d+)\s*Wins\s*/\s*(\d+)\s*Losses", text)
    wins = int(trades_m.group(1)) if trades_m else 0
    losses = int(trades_m.group(2)) if trades_m else 0
    total_trades = wins + losses
    
    sharpe = extract_val(r"\*\*Sharpe Ratio[^\*]*\*\*\s*\|\s*`?([^`|\n]+)`?")
    sortino = extract_val(r"\*\*Sortino Ratio\*\*\s*\|\s*`?([^`|\n]+)`?")
    calmar = extract_val(r"\*\*Calmar Ratio\*\*\s*\|\s*`?([^`|\n]+)`?")

    return {
        "trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate.replace("%", "").strip(),
        "profit_factor": profit_factor.strip(),
        "net_pnl": net_pnl.replace("USDT", "").strip(),
        "max_dd": max_dd.strip(),
        "sharpe": sharpe.strip(),
        "sortino": sortino.strip(),
        "calmar": calmar.strip()
    }

def run_matrix_campaign(existing_runs: Optional[Dict[str, int]] = None):
    """Dispatches all 14 experiments and monitors to completion."""
    active_runs: Dict[str, int] = dict(existing_runs or {})
    
    print("=" * 80)
    print("   DISPATCHING 14-EXPERIMENT MATRIX TO GITHUB ACTIONS (KCEX_BOT_SANDBOX)")
    print("=" * 80)
    
    for exp_id, inputs in EXPERIMENTS.items():
        if exp_id in active_runs:
            print(f"[[OK]] {exp_id} already registered as Run #{active_runs[exp_id]}")
            continue
        print(f"[*] Dispatching {exp_id}...")
        run_id = dispatch_workflow(exp_id, inputs, ref="main")
        if run_id:
            active_runs[exp_id] = run_id
            print(f"[+] {exp_id} -> Run #{run_id}")
        else:
            print(f"[!] Warning: Could not dispatch {exp_id} immediately.")
        time.sleep(2) # Slight stagger to allow GitHub Actions to register each run
        
    print("\n" + "=" * 80)
    print(f"[*] Total active experiments registered: {len(active_runs)}/{len(EXPERIMENTS)}")
    for name, rid in active_runs.items():
        print(f"    - {name}: Run #{rid}")
    print("=" * 80)
    
    # Monitor loop
    pending = dict(active_runs)
    results = {}
    
    print("\n[*] Monitoring cloud backtest execution on GitHub Actions...")
    while pending:
        for name, rid in list(pending.items()):
            st = check_run(rid)
            if st["status"] == "completed":
                print(f"\n[[OK]] {name} (Run #{rid}) COMPLETED: {st['conclusion']}")
                del pending[name]
                if st["conclusion"] == "success":
                    zip_path = download_run_artifact(rid, name)
                    if zip_path:
                        # Find latest summary report
                        md_files = list(REPORTS_DIR.glob(f"backtest_{EXPERIMENTS[name]['symbol']}_*_summary.md"))
                        if md_files:
                            latest_md = max(md_files, key=lambda f: f.stat().st_mtime)
                            metrics = parse_report_summary(latest_md)
                            metrics["exp_id"] = name
                            metrics["symbol"] = EXPERIMENTS[name]["symbol"]
                            metrics["strategy"] = EXPERIMENTS[name]["strategy"]
                            metrics["invert"] = EXPERIMENTS[name]["invert_signal"]
                            metrics["tp_ticks"] = EXPERIMENTS[name]["tp_ticks"]
                            metrics["sl_val"] = f"{EXPERIMENTS[name].get('sl_ticks', '')}t" if EXPERIMENTS[name]["sl_mode"] == "TICKS" else f"{EXPERIMENTS[name].get('sl_roe', '')}% ROE"
                            results[name] = metrics
                            print(f"[[METRICS]] {name} Metrics: WR: {metrics['win_rate']}% | PF: {metrics['profit_factor']} | PnL: {metrics['net_pnl']} USDT | DD: {metrics['max_dd']}")
            else:
                pass
        if pending:
            time.sleep(12)
            
    print("\n" + "=" * 80)
    print("                    FINAL CROSS-EXPERIMENT LEADERBOARD")
    print("=" * 80)
    if results:
        df = pd.DataFrame(list(results.values()))
        cols = ["exp_id", "symbol", "strategy", "invert", "tp_ticks", "sl_val", "trades", "win_rate", "profit_factor", "net_pnl", "max_dd", "sharpe"]
        avail_cols = [c for c in cols if c in df.columns]
        pd.set_option('display.max_columns', 15)
        pd.set_option('display.width', 1000)
        print(df[avail_cols].to_string(index=False))
        
        # Save to JSON
        out_json = REPORTS_DIR / "matrix_results.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\n[+] Results saved to {out_json}")
    return results

if __name__ == "__main__":
    # Check if run 34034929008 is known
    run_matrix_campaign(existing_runs={"DOGE_E0_Base": 34034929008})
