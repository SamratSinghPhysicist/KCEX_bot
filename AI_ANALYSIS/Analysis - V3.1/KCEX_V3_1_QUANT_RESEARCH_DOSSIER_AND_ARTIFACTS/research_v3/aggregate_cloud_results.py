"""
Aggregate Cloud Backtest Results across TRUMP and DOGE
======================================================
Parses all institutional backtest summary reports downloaded from GitHub Actions
and compiles an executive cross-asset comparative matrix.
"""

import os
import sys
import glob
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "cloud_reports")

def parse_markdown_summary(fpath: str):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    data = {"file": fpath}
    
    # Extract symbol
    m_sym = re.search(r"Institutional Backtest Performance Report:\s*([A-Z0-9_]+)", text)
    data["symbol"] = m_sym.group(1) if m_sym else "UNKNOWN"

    # Strategy
    m_strat = re.search(r"\*\*Strategy Evaluated\*\*\s*\|\s*`([^`]+)`", text)
    data["strategy"] = m_strat.group(1) if m_strat else "UNKNOWN"

    # Slippage
    m_slip = re.search(r"\*\*Slippage Tolerance\*\*\s*\|\s*`([^`]+)`", text)
    data["slippage"] = m_slip.group(1) if m_slip else "0 ticks"

    # TP & SL
    m_tp = re.search(r"\*\*Take Profit Target\*\*\s*\|\s*`([^`]+)`", text)
    data["tp"] = m_tp.group(1) if m_tp else "N/A"

    m_sl = re.search(r"\*\*Stop Loss Rule\*\*\s*\|\s*`([^`]+)`", text)
    data["sl"] = m_sl.group(1) if m_sl else "N/A"

    # Net PnL
    m_pnl = re.search(r"\*\*Net Realized PnL\*\*\s*\|\s*\*\*`([^`]+)`\*\*", text)
    data["net_pnl"] = m_pnl.group(1) if m_pnl else "0.0 USDT"

    # Profit Factor
    m_pf = re.search(r"\*\*Profit Factor\*\*\s*\|\s*\*\*`([^`]+)`\*\*", text)
    data["profit_factor"] = m_pf.group(1) if m_pf else "N/A"

    # Win Rate
    m_wr = re.search(r"\*\*Win Rate\*\*\s*\|\s*\*\*`([^`]+)`\*\*", text)
    data["win_rate"] = m_wr.group(1) if m_wr else "N/A"

    # Trades count
    m_tr = re.search(r"\*\*Total Trades Executed\*\*\s*\|\s*`([^`]+)`", text)
    data["trades"] = m_tr.group(1) if m_tr else "N/A"

    # Sharpe & Sortino
    m_sh = re.search(r"\*\*Sharpe Ratio[^\*]*\*\*\s*\|\s*`([^`]+)`", text)
    data["sharpe"] = m_sh.group(1) if m_sh else "N/A"

    m_so = re.search(r"\*\*Sortino Ratio\*\*\s*\|\s*`([^`]+)`", text)
    data["sortino"] = m_so.group(1) if m_so else "N/A"

    # Max DD
    m_dd = re.search(r"\*\*Max Drawdown\*\*\s*\|\s*`([^`]+)`", text)
    data["max_dd"] = m_dd.group(1) if m_dd else "N/A"

    return data

def aggregate_all():
    summary_files = glob.glob(os.path.join(REPORTS_DIR, "run_*", "*summary.md"))
    print(f"[*] Found {len(summary_files)} cloud backtest summary files in {REPORTS_DIR}\n")

    results = []
    for f in summary_files:
        run_id = os.path.basename(os.path.dirname(f))
        res = parse_markdown_summary(f)
        res["run_id"] = run_id
        results.append(res)

    # Sort by symbol, then Net PnL descending
    print("=" * 115)
    print(f"{'Run ID':<16} | {'Symbol':<10} | {'Strategy':<14} | {'TP / SL':<18} | {'Slip':<8} | {'Net PnL':<12} | {'PF':<6} | {'WR%':<7} | {'Sharpe':<8}")
    print("=" * 115)

    for r in results:
        tp_sl = f"{r['tp'][:8]} / {r['sl'][:8]}"
        print(
            f"{r['run_id']:<16} | "
            f"{r['symbol']:<10} | "
            f"{r['strategy']:<14} | "
            f"{tp_sl:<18} | "
            f"{r['slippage']:<8} | "
            f"{r['net_pnl']:<12} | "
            f"{r['profit_factor']:<6} | "
            f"{r['win_rate']:<7} | "
            f"{r['sharpe']:<8}"
        )

if __name__ == "__main__":
    aggregate_all()
