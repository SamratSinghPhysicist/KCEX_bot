import os
import sys
import csv
import glob
from typing import List, Dict, Any

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.forensics_analyzer import analyze_trade_forensics

csv_file = glob.glob(os.path.join(ROOT_DIR, "research", "experiments", "EXP_0001", "*.csv"))[0]
print("[*] Running feature threshold scan on EXP_0001 trades...")
rep, trades = analyze_trade_forensics(csv_file)

baseline_trades = len(trades)
baseline_pnl = sum(t["pnl"] for t in trades)
baseline_wins = sum(1 for t in trades if t["is_win"])
baseline_wr = (baseline_wins / baseline_trades) * 100.0
baseline_gp = sum(t["pnl"] for t in trades if t["is_win"])
baseline_gl = abs(sum(t["pnl"] for t in trades if not t["is_win"]))
baseline_pf = baseline_gp / baseline_gl if baseline_gl > 0 else 0.0

print(f"[*] Baseline: {baseline_trades} trades, WR: {baseline_wr:.2f}%, PF: {baseline_pf:.2f}, PnL: {baseline_pnl:+.4f} USDT")

candidate_features = [
    ("ret_60s_ticks", "Pre-Entry 60s Momentum"),
    ("ret_30s_ticks", "Pre-Entry 30s Momentum"),
    ("ret_10s_ticks", "Pre-Entry 10s Momentum"),
    ("range_60s_ticks", "Pre-Entry 60s Range (Volatility)"),
    ("dir_eff_60s", "Pre-Entry 60s Directional Efficiency"),
    ("reversals_60s", "Pre-Entry 60s Tick Reversals"),
    ("pre_ticks_count", "Pre-Entry 60s Tick Density")
]

best_results = []

for feat, label in candidate_features:
    vals = [t[feat] for t in trades]
    min_v = min(vals)
    max_v = max(vals)
    
    # Generate 30 percentile cuts
    sorted_vals = sorted(vals)
    test_cuts = [sorted_vals[int(len(sorted_vals) * p / 100)] for p in range(5, 96, 3)]
    test_cuts = sorted(list(set(test_cuts)))

    # Test both excluding > threshold and excluding < threshold
    for cut in test_cuts:
        for mode in ["LESS_THAN", "GREATER_THAN"]:
            if mode == "LESS_THAN":
                # Keep trades where feature >= cut (reject if < cut)
                kept = [t for t in trades if t[feat] >= cut]
                rule_desc = f"{feat} >= {cut:.2f}"
            else:
                # Keep trades where feature <= cut (reject if > cut)
                kept = [t for t in trades if t[feat] <= cut]
                rule_desc = f"{feat} <= {cut:.2f}"

            k_count = len(kept)
            if k_count < 500: # Need reasonable sample size
                continue

            k_wins = sum(1 for t in kept if t["is_win"])
            k_losses = sum(1 for t in kept if not t["is_win"])
            k_wr = (k_wins / k_count) * 100.0
            k_gp = sum(t["pnl"] for t in kept if t["is_win"])
            k_gl = abs(sum(t["pnl"] for t in kept if not t["is_win"]))
            k_pf = (k_gp / k_gl) if k_gl > 0 else 0.0
            k_pnl = sum(t["pnl"] for t in kept)
            delta_pnl = k_pnl - baseline_pnl

            best_results.append({
                "feature": feat,
                "rule": rule_desc,
                "trades": k_count,
                "rejected_trades": baseline_trades - k_count,
                "win_rate": round(k_wr, 2),
                "profit_factor": round(k_pf, 2),
                "net_pnl": round(k_pnl, 4),
                "delta_pnl": round(delta_pnl, 4)
            })

# Sort by delta_pnl descending
best_results.sort(key=lambda x: x["delta_pnl"], reverse=True)

print("\n================ TOP 10 FEATURE THRESHOLD RULES BY NET PnL ================")
print(f"{'Rule':<30} | {'Trades':<7} | {'Win Rate':<9} | {'PF':<6} | {'Net PnL':<10} | {'Delta PnL':<10}")
print("-" * 80)
for r in best_results[:10]:
    print(f"{r['rule']:<30} | {r['trades']:<7} | {r['win_rate']:>7.2f}% | {r['profit_factor']:>6.2f} | {r['net_pnl']:>+9.4f}  | {r['delta_pnl']:>+9.4f}")

print("\n================ WORST 5 RULES (MAX VALUE DESTRUCTION) ================")
for r in best_results[-5:]:
    print(f"{r['rule']:<30} | {r['trades']:<7} | {r['win_rate']:>7.2f}% | {r['profit_factor']:>6.2f} | {r['net_pnl']:>+9.4f}  | {r['delta_pnl']:>+9.4f}")
