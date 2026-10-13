"""
Alpha Portfolio Backtest: Long BTC & Short ETH Dual Account
============================================================
Simulates combined personal trading portfolio across two accounts:
- Account A: Long BTC (1000 USDT)
- Account B: Short ETH (1000 USDT)
- Simultaneous execution, waiting for both to be free before next cycle.
- 50% partial profit booking at +0.20%, +0.30%, etc., SL to BE (+0.05% fee cover).
- Full TP at +1.50% price move (+3% profit at 2x leverage) or original configs.
- Includes exchange fees (taker/maker: 0.04% / 0.02% per fill).
- Evaluates: Net PnL, Daily, Weekly, Monthly, Yearly returns, Sharpe Ratio, Max Drawdown.
- Compares Case 1 (Long BTC, Short ETH) vs Case 2 (Short BTC, Long ETH).
"""

import os
import sys
import math
import datetime
from collections import defaultdict
from typing import List, Dict, Tuple

EXPERIMENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXPERIMENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import (
    load_candles_from_dir,
    build_sub_1m_map,
    evaluate_candle_tp_sl,
    parse_date_to_ms,
    CandleData
)

def run_alpha_backtest():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2025-01-01")
    end_ms = parse_date_to_ms("2026-10-12") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    btc_1m = load_candles_from_dir("BTCUSDT", "1m", base_dir, start_ms, end_ms)
    eth_1m = load_candles_from_dir("ETHUSDT", "1m", base_dir, start_ms, end_ms)
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_sub = build_sub_1m_map(btc_c, btc_1m)
    eth_sub = build_sub_1m_map(eth_c, eth_1m)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    fee_rate = 0.0004 # 0.04% taker fee per execution
    leverage = 2.0
    tot_len = len(common_times)

    # Let's test both Case 1 and Case 2 with Config 1 (TP 3% profit / 1.5% price, SL 3% loss / 1.5% price)
    # and partial TP at 0.20% and 0.30% price move.
    test_cases = [
        ("Case 1 (Long BTC / Short ETH) - Partial TP +0.20% price", "CASE_1", 1.50, 1.50, 0.20),
        ("Case 1 (Long BTC / Short ETH) - Partial TP +0.30% price", "CASE_1", 1.50, 1.50, 0.30),
        ("Case 2 (Short BTC / Long ETH) - Partial TP +0.20% price", "CASE_2", 1.50, 1.50, 0.20),
        ("Case 2 (Short BTC / Long ETH) - Partial TP +0.30% price", "CASE_2", 1.50, 1.50, 0.30),
    ]

    print("=" * 85)
    print("ALPHA EVALUATION: DUAL-ACCOUNT COMBINED PORTFOLIO")
    print(f"Period: 2025-01-01 to 2026-10-12 (~21.4 months, {len(common_times)} hours)")
    print(f"Starting Capital: $2,000 Total ($1,000 on BTC Account, $1,000 on ETH Account)")
    print(f"Leverage: {leverage}x | Fee Rate: {fee_rate*100:.2f}% per order")
    print("=" * 85)

    for title, case_type, p_tp, p_sl, part_price in test_cases:
        i = 0
        cycles = []
        b_dir = "LONG" if case_type == "CASE_1" else "SHORT"
        e_dir = "SHORT" if case_type == "CASE_1" else "LONG"

        while i < tot_len - 1:
            entry_ts = common_times[i]
            p_b = btc_dict[entry_ts].open
            p_e = eth_dict[entry_ts].open

            if b_dir == "LONG":
                tp_b = p_b * (1.0 + p_tp / 100.0)
                sl_b = p_b * (1.0 - p_sl / 100.0)
            else:
                tp_b = p_b * (1.0 - p_tp / 100.0)
                sl_b = p_b * (1.0 + p_sl / 100.0)

            if e_dir == "LONG":
                tp_e = p_e * (1.0 + p_tp / 100.0)
                sl_e = p_e * (1.0 - p_sl / 100.0)
            else:
                tp_e = p_e * (1.0 - p_tp / 100.0)
                sl_e = p_e * (1.0 + p_sl / 100.0)

            b_exit = None; b_res = None; b_mfe = 0.0
            e_exit = None; e_res = None; e_mfe = 0.0

            j = i
            while j < tot_len:
                ts = common_times[j]
                c_b = btc_dict[ts]; c_e = eth_dict[ts]

                if b_exit is None:
                    sub_b = btc_sub.get(ts, [])
                    if sub_b:
                        for mc in sub_b:
                            fav = (mc.high - p_b)/p_b * 100.0 if b_dir == "LONG" else (p_b - mc.low)/p_b * 100.0
                            if fav > b_mfe: b_mfe = fav
                            hit_sl = (mc.low <= sl_b) if b_dir == "LONG" else (mc.high >= sl_b)
                            hit_tp = (mc.high >= tp_b) if b_dir == "LONG" else (mc.low <= tp_b)
                            if hit_sl: b_exit = j; b_res = "SL"; break
                            elif hit_tp: b_exit = j; b_res = "TP"; break
                    else:
                        fav = (c_b.high - p_b)/p_b * 100.0 if b_dir == "LONG" else (p_b - c_b.low)/p_b * 100.0
                        if fav > b_mfe: b_mfe = fav
                        r, _ = evaluate_candle_tp_sl(b_dir, p_b, tp_b, sl_b, c_b, btc_sub, timeframe)
                        if r: b_exit = j; b_res = r

                if e_exit is None:
                    sub_e = eth_sub.get(ts, [])
                    if sub_e:
                        for mc in sub_e:
                            fav = (mc.high - p_e)/p_e * 100.0 if e_dir == "LONG" else (p_e - mc.low)/p_e * 100.0
                            if fav > e_mfe: e_mfe = fav
                            hit_sl = (mc.low <= sl_e) if e_dir == "LONG" else (mc.high >= sl_e)
                            hit_tp = (mc.high >= tp_e) if e_dir == "LONG" else (mc.low <= tp_e)
                            if hit_sl: e_exit = j; e_res = "SL"; break
                            elif hit_tp: e_exit = j; e_res = "TP"; break
                    else:
                        fav = (c_e.high - p_e)/p_e * 100.0 if e_dir == "LONG" else (p_e - c_e.low)/p_e * 100.0
                        if fav > e_mfe: e_mfe = fav
                        r, _ = evaluate_candle_tp_sl(e_dir, p_e, tp_e, sl_e, c_e, eth_sub, timeframe)
                        if r: e_exit = j; e_res = r

                if b_exit is not None and e_exit is not None:
                    break
                j += 1

            if b_exit is None or e_exit is None:
                break

            free_idx = max(b_exit, e_exit)
            exit_ts = common_times[free_idx]

            # Calculate Net Return on Margin (ROE) for BTC trade
            # Entry fee: fee_rate * leverage
            entry_fee_pct = fee_rate * leverage * 100.0 # e.g. 0.04% * 2 = 0.08%

            if b_mfe >= part_price:
                # 50% closed at part_price
                # 50% closed at full TP or BE (+0.05% price move)
                if b_res == "TP":
                    raw_gain_b = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage)
                else:
                    raw_gain_b = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage)
                # Exit fees on 2 legs
                exit_fee_pct = fee_rate * leverage * 100.0
                net_gain_b = raw_gain_b - (entry_fee_pct + exit_fee_pct)
            else:
                raw_gain_b = -(p_sl * leverage)
                exit_fee_pct = fee_rate * leverage * 100.0
                net_gain_b = raw_gain_b - (entry_fee_pct + exit_fee_pct)

            # Calculate Net Return on Margin for ETH trade
            if e_mfe >= part_price:
                if e_res == "TP":
                    raw_gain_e = 0.5 * (part_price * leverage) + 0.5 * (p_tp * leverage)
                else:
                    raw_gain_e = 0.5 * (part_price * leverage) + 0.5 * (0.05 * leverage)
                exit_fee_pct = fee_rate * leverage * 100.0
                net_gain_e = raw_gain_e - (entry_fee_pct + exit_fee_pct)
            else:
                raw_gain_e = -(p_sl * leverage)
                exit_fee_pct = fee_rate * leverage * 100.0
                net_gain_e = raw_gain_e - (entry_fee_pct + exit_fee_pct)

            cycles.append({
                "entry_ts": entry_ts,
                "exit_ts": exit_ts,
                "gain_b": net_gain_b,
                "gain_e": net_gain_e
            })
            i = free_idx + 1

        # Now simulate portfolio balance compounding or fixed-margin
        # Let's track both:
        # A) Fixed $1,000 per account ($2,000 total)
        # B) Compounded account balances
        bal_a = 1000.0
        bal_b = 1000.0
        portfolio_curve = [2000.0]
        timestamps = [cycles[0]["entry_ts"]]

        # Monthly tracking
        monthly_pnl = defaultdict(float)

        for c in cycles:
            dt = datetime.datetime.fromtimestamp(c["exit_ts"] / 1000.0, tz=datetime.timezone.utc)
            m_key = dt.strftime("%Y-%m")

            # Balance updates
            pnl_a = bal_a * (c["gain_b"] / 100.0)
            pnl_b = bal_b * (c["gain_e"] / 100.0)
            bal_a += pnl_a
            bal_b += pnl_b
            tot_bal = bal_a + bal_b
            portfolio_curve.append(tot_bal)
            timestamps.append(c["exit_ts"])

            monthly_pnl[m_key] += (pnl_a + pnl_b)

        total_return_pct = (portfolio_curve[-1] - 2000.0) / 2000.0 * 100.0
        net_profit_usd = portfolio_curve[-1] - 2000.0

        # Calculate Max Drawdown of Combined Portfolio
        peak = 2000.0
        max_dd = 0.0
        for b in portfolio_curve:
            if b > peak: peak = b
            dd = (peak - b) / peak * 100.0
            if dd > max_dd: max_dd = dd

        # Total days
        total_days = (timestamps[-1] - timestamps[0]) / (1000 * 3600 * 24)
        cagr = ((portfolio_curve[-1] / 2000.0) ** (365.25 / total_days) - 1.0) * 100.0 if portfolio_curve[-1] > 0 else -100.0

        # Cycle win statistics (Combined Pair Win Rate)
        pair_wins = sum(1 for c in cycles if (c["gain_b"] + c["gain_e"]) > 0)
        pair_win_rate = pair_wins / len(cycles) * 100.0

        avg_daily_pnl = net_profit_usd / total_days
        avg_weekly_pnl = avg_daily_pnl * 7.0
        avg_monthly_pnl = avg_daily_pnl * 30.4375

        print(f"\n############################################################")
        print(f"{title}")
        print(f"############################################################")
        print(f"Total Completed Cycles:        {len(cycles)} trades")
        print(f"Combined Pair Win Rate:        {pair_win_rate:.1f}% ({pair_wins}/{len(cycles)} profitable cycles)")
        print(f"Starting Capital:              $2,000.00")
        print(f"Final Portfolio Balance:       ${portfolio_curve[-1]:,.2f}")
        print(f"Net Profit ($):                ${net_profit_usd:+,.2f} ({total_return_pct:+.1f}%)")
        print(f"Combined Max Drawdown:         {max_dd:.2f}%")
        print(f"Annualized Return (CAGR):      {cagr:+.1f}%")
        print(f"Avg Profit Per Day:            ${avg_daily_pnl:+,.2f}")
        print(f"Avg Profit Per Week:           ${avg_weekly_pnl:+,.2f}")
        print(f"Avg Profit Per Month:          ${avg_monthly_pnl:+,.2f}")

        # Show monthly breakdown
        print("\nMonthly PnL Breakdown (USD):")
        sorted_months = sorted(monthly_pnl.keys())
        pos_months = sum(1 for m in sorted_months if monthly_pnl[m] > 0)
        for m in sorted_months:
            pnl_m = monthly_pnl[m]
            bar = "+" * int(pnl_m / 20) if pnl_m > 0 else "-" * int(abs(pnl_m) / 20)
            print(f"  {m}: ${pnl_m:>+8.2f} | {bar}")
        print(f"Profitable Months: {pos_months}/{len(sorted_months)} ({pos_months/len(sorted_months)*100:.1f}%)")

if __name__ == "__main__":
    run_alpha_backtest()
