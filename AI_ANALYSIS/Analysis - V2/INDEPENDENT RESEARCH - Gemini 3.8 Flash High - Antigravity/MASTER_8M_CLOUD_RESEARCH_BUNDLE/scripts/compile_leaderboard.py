import json
import re
from pathlib import Path
import pandas as pd

base = Path(r"d:\My_Bots\Trading\(COPY-SandBoxed) KCEX\ResearchV2\BACKTESTER\reports\matrix_runs")

def parse_report(md_file: Path):
    text = md_file.read_text(encoding="utf-8")
    
    def get_val(pattern: str, default="N/A"):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default

    # Extract metrics using precise regex
    pnl_match = re.search(r"\*\*Net Realized PnL\*\*\s*\|\s*[\*`]*([^\*`|\n]+)[\*`]*", text)
    net_pnl = pnl_match.group(1).replace("USDT", "").strip() if pnl_match else "N/A"

    pf_match = re.search(r"\*\*Profit Factor\*\*\s*\|\s*[\*`]*([^\*`|\n]+)[\*`]*", text)
    pf = pf_match.group(1).strip() if pf_match else "N/A"

    wr_match = re.search(r"\*\*Win Rate\*\*\s*\|\s*[\*`]*([^\*`|\n%]+)%?[\*`]*", text)
    wr = wr_match.group(1).strip() if wr_match else "N/A"

    dd_match = re.search(r"\*\*Max Drawdown\*\*\s*\|\s*`?([^`|\n]+)`?\s*\|\s*[^|]+\|\s*[\*`]*([^`|\n]+)[\*`]*", text)
    max_dd = dd_match.group(2).strip() if dd_match else get_val(r"\*\*Max Drawdown\*\*\s*\|\s*[\*`]*([^\*`|\n]+)[\*`]*")

    trades_match = re.search(r"(\d+)\s*Wins\s*/\s*(\d+)\s*Losses", text)
    wins = int(trades_match.group(1)) if trades_match else 0
    losses = int(trades_match.group(2)) if trades_match else 0

    sharpe = get_val(r"\*\*Sharpe Ratio[^\*]*\*\*\s*\|\s*`?([^`|\n]+)`?")
    sortino = get_val(r"\*\*Sortino Ratio\*\*\s*\|\s*`?([^`|\n]+)`?")
    calmar = get_val(r"\*\*Calmar Ratio\*\*\s*\|\s*`?([^`|\n]+)`?")

    return {
        "trades": wins + losses,
        "wins": wins,
        "losses": losses,
        "win_rate": wr,
        "profit_factor": pf,
        "net_pnl": net_pnl,
        "max_dd": max_dd,
        "sharpe": sharpe,
        "sortino": sortino,
        "calmar": calmar
    }

order = [
    "DOGE_E0_Base", "DOGE_E1_InvBase", "DOGE_E2_Sym1to1", "DOGE_E3_InvSym1to1",
    "DOGE_E4_Direct10t2t", "DOGE_E5_Inv10t2t", "DOGE_E6_Inv5t2t", "DOGE_E7_SmartSym", "DOGE_E8_SmartInvSym",
    "TRUMP_T0_Base", "TRUMP_T1_InvBase", "TRUMP_T2_Sym1to1", "TRUMP_T3_InvSym1to1", "TRUMP_T4_SmartSym"
]

configs = {
    "DOGE_E0_Base": {"sym": "DOGE", "strat": "STOCH", "inv": False, "tp": "2t", "sl": "25% ROE"},
    "DOGE_E1_InvBase": {"sym": "DOGE", "strat": "STOCH", "inv": True, "tp": "2t", "sl": "25% ROE"},
    "DOGE_E2_Sym1to1": {"sym": "DOGE", "strat": "STOCH", "inv": False, "tp": "2t", "sl": "2t"},
    "DOGE_E3_InvSym1to1": {"sym": "DOGE", "strat": "STOCH", "inv": True, "tp": "2t", "sl": "2t"},
    "DOGE_E4_Direct10t2t": {"sym": "DOGE", "strat": "STOCH", "inv": False, "tp": "10t", "sl": "2t"},
    "DOGE_E5_Inv10t2t": {"sym": "DOGE", "strat": "STOCH", "inv": True, "tp": "10t", "sl": "2t (User Hyp)"},
    "DOGE_E6_Inv5t2t": {"sym": "DOGE", "strat": "STOCH", "inv": True, "tp": "5t", "sl": "2t"},
    "DOGE_E7_SmartSym": {"sym": "DOGE", "strat": "SMART", "inv": False, "tp": "2t", "sl": "2t"},
    "DOGE_E8_SmartInvSym": {"sym": "DOGE", "strat": "SMART", "inv": True, "tp": "2t", "sl": "2t"},
    "TRUMP_T0_Base": {"sym": "TRUMP", "strat": "STOCH", "inv": False, "tp": "2t", "sl": "25% ROE"},
    "TRUMP_T1_InvBase": {"sym": "TRUMP", "strat": "STOCH", "inv": True, "tp": "2t", "sl": "25% ROE"},
    "TRUMP_T2_Sym1to1": {"sym": "TRUMP", "strat": "STOCH", "inv": False, "tp": "2t", "sl": "2t"},
    "TRUMP_T3_InvSym1to1": {"sym": "TRUMP", "strat": "STOCH", "inv": True, "tp": "2t", "sl": "2t"},
    "TRUMP_T4_SmartSym": {"sym": "TRUMP", "strat": "SMART", "inv": False, "tp": "2t", "sl": "2t"},
}

rows = []
for name in order:
    dir_path = base / name
    summary_file = dir_path / "summary.md"
    if not summary_file.exists():
        mds = list(dir_path.glob("*_summary.md"))
        if mds:
            summary_file = mds[0]
    if summary_file.exists():
        m = parse_report(summary_file)
        c = configs[name]
        row = {
            "Experiment": name,
            "Symbol": c["sym"],
            "Strategy": c["strat"],
            "Invert": c["inv"],
            "TP": c["tp"],
            "SL": c["sl"],
            "Trades": m["trades"],
            "Win Rate %": m["win_rate"],
            "Profit Factor": m["profit_factor"],
            "Net PnL (USDT)": m["net_pnl"],
            "Max DD": m["max_dd"],
            "Sharpe": m["sharpe"],
            "Sortino": m["sortino"],
            "Calmar": m["calmar"]
        }
        rows.append(row)

df = pd.DataFrame(rows)
pd.set_option("display.max_columns", 15)
pd.set_option("display.width", 1000)
print("\n" + "=" * 110)
print("             COMPLETE 8-MONTH MULTI-STRATEGY LEADERBOARD (CLOUD GITHUB ACTIONS)")
print("=" * 110)
print(df.to_string(index=False))

# Save json
out_json = base.parent / "complete_14_experiments_summary.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)
print(f"\n[+] Leaderboard saved to {out_json}")
