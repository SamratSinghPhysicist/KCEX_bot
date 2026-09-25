import glob
import json
import os

files = glob.glob("local_matrix_artifacts/*.json")
pair_summary = {}

for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    p = data["pair"]
    tf = data["timeframe"]
    params = data.get("parameters", {})
    metrics = data.get("metrics", {})
    is_zf = params.get("is_zero_fee")
    tfr = params.get("taker_fee_rate")
    fees = metrics.get("total_fees_usdt", 0.0)
    net_pnl = metrics.get("net_pnl_usdt", 0.0)
    trades = metrics.get("total_trades", 0)

    if p not in pair_summary:
        pair_summary[p] = {
            "is_zero_fee": is_zf,
            "tfr": tfr,
            "total_fees": 0.0,
            "total_trades": 0,
            "total_net_pnl": 0.0,
            "runs": {}
        }
    pair_summary[p]["total_fees"] += fees
    pair_summary[p]["total_trades"] += trades
    pair_summary[p]["total_net_pnl"] += net_pnl
    pair_summary[p]["runs"][tf] = {
        "trades": trades,
        "fees": fees,
        "net_pnl": net_pnl
    }

print(f"Total pairs audited: {len(pair_summary)}")
print("-" * 90)
print(f"{'Pair':<16} | {'Zero-Fee':<8} | {'Taker Rate':<10} | {'Trades':<8} | {'Fees Paid':<14} | {'Net PnL':<12}")
print("-" * 90)
for p in sorted(pair_summary.keys()):
    info = pair_summary[p]
    zf_str = "YES (0%)" if info["is_zero_fee"] else "NO"
    tfr_str = f"{info['tfr']*100:.2f}%" if info['tfr'] is not None else "N/A"
    fees_str = f"${info['total_fees']:>9.2f}"
    pnl_str = f"${info['total_net_pnl']:>9.2f}"
    print(f"{p:<16} | {zf_str:<8} | {tfr_str:<10} | {info['total_trades']:<8} | {fees_str:<14} | {pnl_str:<12}")

print("-" * 90)
print("\nDetail of non-zero fee pairs by timeframe:")
for p in sorted(pair_summary.keys()):
    if not pair_summary[p]["is_zero_fee"]:
        print(f"\n[{p}] (Taker Fee = {pair_summary[p]['tfr']*100:.2f}%):")
        for tf in ["5m", "15m", "1h", "4h", "1d"]:
            r = pair_summary[p]["runs"].get(tf, {})
            print(f"  {tf:>3}: Trades={r.get('trades', 0):<5} | Fees Paid=${r.get('fees', 0.0):<7.2f} | Net PnL=${r.get('net_pnl', 0.0):<8.2f}")
