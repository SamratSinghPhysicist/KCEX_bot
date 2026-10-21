#!/usr/bin/env python3
"""
Quick Report Builder from Generated Results CSVs
================================================
Reads all existing `results_*.csv` files in the repository and generates
the complete `NO_STOP_LOSS_HYPOTHESIS_REPORT.md`.
"""

import os
import glob
import csv
from typing import List, Dict, Any

import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
REPORT_FILE = os.path.join(ROOT_DIR, "NO_STOP_LOSS_HYPOTHESIS_REPORT.md")


def parse_result_csv(filepath: str) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}
    monthly: List[Dict[str, Any]] = []

    section = None
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        monthly_header = None
        for row in reader:
            if not row:
                continue
            first = row[0].strip()
            if first == "# METRIC_SUMMARY":
                section = "summary"
                continue
            elif first == "# MONTHLY_PERFORMANCE_BREAKDOWN":
                section = "monthly"
                monthly_header = None
                continue
            elif first == "# DETAILED_TRADES":
                section = "trades"
                break

            if section == "summary":
                if len(row) >= 2:
                    k = row[0].strip()
                    v = row[1].strip()
                    try:
                        if "." in v:
                            metrics[k] = float(v)
                        else:
                            metrics[k] = int(v)
                    except ValueError:
                        metrics[k] = v
            elif section == "monthly":
                if monthly_header is None:
                    monthly_header = [c.strip() for c in row]
                else:
                    m_dict = dict(zip(monthly_header, row))
                    monthly.append(m_dict)

    return {"metrics": metrics, "monthly": monthly}


def build_report():
    csv_files = sorted(glob.glob(os.path.join(ROOT_DIR, "results_*.csv")))
    print(f"Found {len(csv_files)} results CSV files.")

    all_metrics = []
    all_monthly = []

    for f in csv_files:
        data = parse_result_csv(f)
        m = data["metrics"]
        if not m or "asset" not in m:
            continue
        all_metrics.append(m)
        for m_row in data["monthly"]:
            all_monthly.append({
                "asset": m.get("asset"),
                "direction": m.get("direction"),
                "tp_rule": m.get("tp_rule"),
                "strategy": m.get("strategy"),
                "month": m_row.get("month"),
                "trades": int(m_row.get("trades", 0)),
                "wins": int(m_row.get("wins", 0)),
                "losses": int(m_row.get("losses", 0)),
                "win_rate_pct": float(m_row.get("win_rate_pct", 0.0)),
                "net_pnl_usd": float(m_row.get("net_pnl_usd", 0.0)),
            })

    from experiments.run_comprehensive_matrix import build_master_markdown_report
    build_master_markdown_report(all_metrics, all_monthly, REPORT_FILE)
    print(f"[OK] Report successfully built and saved to: {REPORT_FILE}")


if __name__ == "__main__":
    build_report()
