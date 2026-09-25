import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

with open("final_matrix_reports/profitable_deep_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total Profitable Configurations: {len(data)}\n")

for i, item in enumerate(data, 1):
    pair = item["pair"]
    tf = item["timeframe"].upper()
    roi = item["roi_pct"]
    net = item["net_pnl"]
    fees = item["fees"]
    gross = item["gross_pnl"]
    trades = item["trades"]
    wr = item["win_rate"]
    pf = item["profit_factor"]
    dd = item["max_drawdown_pct"]
    streaks = item["streaks"]
    tier = item["statistical_tier"]
    zero_fee = "0.00% Zero-Fee" if item["is_zero_fee"] else f"{item['taker_fee_rate']*100:.2f}% Taker"

    print("=" * 90)
    print(f"#{i} {pair} [{tf}] | ROI: {roi:+.2f}% | Net PnL: ${net:+.2f} | Fees: ${fees:.2f} | Gross: ${gross:+.2f}")
    print(f"    Trades: {trades} | WR: {wr:.1f}% | PF: {pf:.2f} | Max DD: {dd:.1f}% | Streaks (Max W: {streaks['max_consecutive_wins']}, Max L: {streaks['max_consecutive_losses']})")
    print(f"    Fee Schedule: {zero_fee} | Confidence: {tier}")
    print("    MONTHLY BREAKDOWN:")
    for m, d in item["monthly_breakdown"].items():
        print(f"      {m}: Trades={d['trades']:<2} | Wins={d['wins']:<2} | Losses={d['losses']:<2} | WR={d['win_rate_pct']:>5.1f}% | Net PnL=${d['net_pnl_usdt']:>7.2f} | Fees=${d['fees_usdt']:>6.3f}")
    
    print("    WEEKLY BREAKDOWN:")
    weeks = item["weekly_breakdown"]
    for w, d in sorted(weeks.items()):
        print(f"      {w}: Trades={d['trades']:<2} | WR={d['win_rate_pct']:>5.1f}% | Net PnL=${d['net_pnl_usdt']:>7.2f} | Fees=${d['fees_usdt']:>6.3f}")
    print()
