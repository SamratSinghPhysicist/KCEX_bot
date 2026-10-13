import os
import sys
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

df = pd.read_csv("BACKTESTER/reports/custom_25k_1x_2x_sweep/custom_master_matrix.csv")

champs = [
    ("TRUMP_USDT", "15m"),
    ("TRUMP_USDT", "4h"),
    ("TRUMP_USDT", "1d"),
    ("DOGE_USDT", "1d"),
    ("ETH_USDT", "1d"),
    ("ETH_USDT", "4h"),
    ("1000000MOG_USDT", "15m"),
    ("CL_USDT", "4h"),
    ("XAU_USDT", "4h"),
    ("BTC_USDT", "4h"),
    ("SOL_USDT", "1d"),
    ("XAG_USDT", "1d")
]

print("=" * 110)
print(f"{'Asset':15} {'TF':4} {'Lev':3} {'Risk%':5} {'Slip':4} {'Trades':6} {'WR%':6} {'PF':5} {'Net PnL ($)':12} {'ROI%':7} {'Max DD%':7} {'Fees ($)':9} {'Final Bal ($)':13} {'Calmar':6}")
print("=" * 110)

for lev in [1, 2]:
    print(f"\n--- LEVERAGE {lev}X (Risk 20%, Slippage 1 Tick) ---")
    for sym, tf in champs:
        sub = df[(df["symbol"] == sym) & (df["timeframe"] == tf) & (df["leverage"] == lev) & (df["risk_pct"] == 20.0) & (df["slippage_ticks"] == 1)]
        if len(sub) == 0:
            continue
        r = sub.iloc[0]
        print(f"{r['symbol']:15} {r['timeframe']:4} {r['leverage']:2}x {r['risk_pct']:4.0f}% {r['slippage_ticks']:2}t {r['total_trades']:6} {r['win_rate_pct']:5.1f}% {r['profit_factor']:5.2f} ${r['net_pnl_usdt']:>10.2f} {r['net_roi_pct']:>6.2f}% {r['max_drawdown_pct']:>6.2f}% ${r['total_fees_usdt']:>7.2f} ${r['final_balance_usdt']:>11.2f} {r['calmar_ratio']:>6.2f}")

print("\n" + "=" * 110)
print(f"{'Asset':15} {'TF':4} {'Lev':3} {'Risk%':5} {'Slip':4} {'Trades':6} {'WR%':6} {'PF':5} {'Net PnL ($)':12} {'ROI%':7} {'Max DD%':7} {'Fees ($)':9} {'Final Bal ($)':13} {'Calmar':6}")
print("=" * 110)
for lev in [1, 2]:
    print(f"\n--- LEVERAGE {lev}X (Risk 10%, Slippage 1 Tick) ---")
    for sym, tf in champs:
        sub = df[(df["symbol"] == sym) & (df["timeframe"] == tf) & (df["leverage"] == lev) & (df["risk_pct"] == 10.0) & (df["slippage_ticks"] == 1)]
        if len(sub) == 0:
            continue
        r = sub.iloc[0]
        print(f"{r['symbol']:15} {r['timeframe']:4} {r['leverage']:2}x {r['risk_pct']:4.0f}% {r['slippage_ticks']:2}t {r['total_trades']:6} {r['win_rate_pct']:5.1f}% {r['profit_factor']:5.2f} ${r['net_pnl_usdt']:>10.2f} {r['net_roi_pct']:>6.2f}% {r['max_drawdown_pct']:>6.2f}% ${r['total_fees_usdt']:>7.2f} ${r['final_balance_usdt']:>11.2f} {r['calmar_ratio']:>6.2f}")
