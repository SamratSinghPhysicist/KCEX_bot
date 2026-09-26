import csv
import os

filepath = "Network_logs_by_codex/ALL_PAIRS_DETAILS_18Sep2026/kcex_all_pairs_detailed.csv"
active = [
    "BTC_USDT", "ETH_USDT", "DOGE_USDT", "TRUMP_USDT",
    "TRX_USDT", "AVAX_USDT", "KOMA_USDT", "AIXBT_USDT", "XMR_USDT"
]

with open(filepath, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    header_idx = {name.strip(): i for i, name in enumerate(header)}
    
    rows = []
    for row in reader:
        sym = row[header_idx.get("symbol", 0)]
        if sym in active:
            price = float(row[header_idx["current_price"]] or 0.0)
            cs = float(row[header_idx["contract_size"]] or 1.0)
            min_v = float(row[header_idx["min_contracts"]] or 1.0)
            min_notional = float(row[header_idx["min_notional_usdt"]] or (price * cs * min_v))
            min_margin = float(row[header_idx["min_margin_usdt"]] or (min_notional / 15.0))
            max_lev = int(float(row[header_idx["max_leverage"]] or 50))
            rows.append({
                "symbol": sym,
                "price": price,
                "cs": cs,
                "min_v": min_v,
                "min_notional": min_notional,
                "min_margin_live": min_margin,
                "margin_15x": min_notional / 15.0,
                "max_lev": max_lev
            })

rows.sort(key=lambda x: x["min_notional"])

print(f"{'Symbol':<12} | {'Price':<10} | {'CS':<6} | {'Min Notional':<14} | {'Margin @ 15x':<14} | {'Min Balance for 10% Risk'}")
print("-" * 85)
for r in rows:
    min_bal_10pct = r['margin_15x'] / 0.10
    print(f"{r['symbol']:<12} | ${r['price']:<9.4f} | {r['cs']:<6} | ${r['min_notional']:<13.4f} | ${r['margin_15x']:<13.6f} | ${min_bal_10pct:<8.2f}")
