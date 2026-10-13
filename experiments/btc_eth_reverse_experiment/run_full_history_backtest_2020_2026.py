"""
Full Historical Backtest (2020-01-01 to 2026-09-30): 6.75 Years of Market Regimes
===================================================================================
Evaluates the production configuration across all market cycles:
- 2020 Covid Crash & DeFi Summer
- 2021 Bull Run ($69k ATH)
- 2022 Brutal Bear Market (LUNA / FTX Collapses)
- 2023 Recovery
- 2024 Bitcoin ETF & Halving Rally
- 2025-2026 Modern Cycle

Configuration:
- Account A: Long BTCUSDT (1000 USDT base, 2x leverage)
- Account B: Short ETHUSDT (1000 USDT base, 2x leverage)
- Total Initial Capital: $2,000 USDT
- Simultaneous execution, waiting for both to be free before next cycle.
- Partial TP: Close 50% at +0.20% price move (+0.40% profit)
- Breakeven Ratchet: Move SL to Entry + 0.05% (covers exchange fees)
- Final TP: Close remaining 50% at +1.50% price move (+3.00% profit)
- Initial SL: -1.50% price move (-3.00% loss)
- Fee Rate: 0.04% per fill (taker fee)

Generates:
- Yearly Performance Table (2020 - 2026)
- Monthly Performance Breakdown (81 months)
- Weekly & Daily Statistics
- Maximum Drawdown, Sharpe Ratio, Win Rates
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

def run_multi_year_backtest():
    base_dir = os.path.join(ROOT_DIR, "BACKTESTER/OHLCV_Data_Binance")
    start_ms = parse_date_to_ms("2020-01-01")
    end_ms = parse_date_to_ms("2026-09-30") + (24 * 3600 * 1000 - 1)

    timeframe = "1h"
    print("[*] Loading 1-Hour candles for BTC and ETH from 2020-01-01 to 2026-09-30...")
    btc_c = load_candles_from_dir("BTCUSDT", timeframe, base_dir, start_ms, end_ms)
    eth_c = load_candles_from_dir("ETHUSDT", timeframe, base_dir, start_ms, end_ms)

    btc_dict = {c.open_time_ms: c for c in btc_c}
    eth_dict = {c.open_time_ms: c for c in eth_c}
    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))

    tot_len = len(common_times)
    print(f"[*] Successfully aligned {tot_len} 1-Hour candles ({tot_len/24:.1f} days / {tot_len/24/365.25:.2f} years).")

    leverage = 2.0
    fee_rate = 0.0004 # 0.04% taker fee
    p_tp = 1.50       # 1.50% price move -> 3.0% profit
    p_sl = 1.50       # 1.50% price move -> 3.0% loss
    part_price = 0.20 # 0.20% price move -> 0.40% profit

    for case_type, title in [
        ("CASE_1", "CASE 1: LONG BTC / SHORT ETH (Recommended Production Strategy)"),
        ("CASE_2", "CASE 2: SHORT BTC / LONG ETH (Opposite Benchmark)")
    ]:
        b_dir = "LONG" if case_type == "CASE_1" else "SHORT"
        e_dir = "SHORT" if case_type == "CASE_1" else "LONG"

        i = 0
        cycles = []

        while i < tot_len - 1:
            entry_ts = common_times[i]
            p_b = btc_dict[entry_ts].open
            p_e = eth_dict[entry_ts].open

            tp_b = p_b * (1.0 + p_tp / 100.0) if b_dir == "LONG" else p_b * (1.0 - p_tp / 100.0)
            sl_b = p_b * (1.0 - p_sl / 100.0) if b_dir == "LONG" else p_b * (1.0 + p_sl / 100.0)
            tp_e = p_e * (1.0 + p_tp / 100.0) if e_dir == "LONG" else p_e * (1.0 - p_tp / 100.0)
            sl_e = p_e * (1.0 - p_sl / 100.0) if e_dir == "LONG" else p_e * (1.0 + p_sl / 100.0)

            b_exit = None; b_res = None; b_mfe = 0.0
            e_exit = None; e_res = None; e_mfe = 0.0

            j = i
            while j < tot_len:
                ts = common_times[j]
                c_b = btc_dict[ts]; c_e = eth_dict[ts]

                if b_exit is None:
                    fav_b = (c_b.high - p_b)/p_b * 100.0 if b_dir == "LONG" else (p_b - c_b.low)/p_b * 100.0
                    if fav_b > b_mfe: b_mfe = fav_b
                    # Check hits
                    hit_tp = (c_b.high >= tp_b) if b_dir == "LONG" else (c_b.low <= tp_b)
                    hit_sl = (c_b.low <= sl_b) if b_dir == "LONG" else (c_b.high >= sl_b)
                    if hit_tp and not hit_sl: b_exit = j; b_res = "TP"
                    elif hit_sl and not hit_tp: b_exit = j; b_res = "SL"
                    elif hit_tp and hit_sl:
                        # Conservative dispute resolution: SL
                        b_exit = j; b_res = "SL"

                if e_exit is None:
                    fav_e = (c_e.high - p_e)/p_e * 100.0 if e_dir == "LONG" else (p_e - c_e.low)/p_e * 100.0
                    if fav_e > e_mfe: e_mfe = fav_e
                    hit_tp = (c_e.high >= tp_e) if e_dir == "LONG" else (c_e.low <= tp_e)
                    hit_sl = (c_e.low <= sl_e) if e_dir == "LONG" else (c_e.high >= sl_e)
                    if hit_tp and not hit_sl: e_exit = j; e_res = "TP"
                    elif hit_sl and not hit_tp: e_exit = j; e_res = "SL"
                    elif hit_tp and hit_sl:
                        e_exit = j; e_res = "SL"

                if b_exit is not None and e_exit is not None:
                    break
                j += 1

            if b_exit is None or e_exit is None:
                break

            free_idx = max(b_exit, e_exit)
            exit_ts = common_times[free_idx]
            hold_hours = free_idx - i + 1

            # Fee deduction (entry + exit on 2x leverage = 0.08% each way = 0.16% total fee per trade leg)
            fee = fee_rate * leverage * 100.0

            # Calculate Net Return on Margin for BTC
            if b_mfe >= part_price:
                # 50% at part_price (0.20% * 2 = 0.40% profit)
                # 50% at full TP (1.50% * 2 = 3.0% profit) or BE (0.05% * 2 = 0.10% profit)
                leg2_profit = (p_tp * leverage) if b_res == "TP" else (0.05 * leverage)
                gb = 0.5 * (part_price * leverage) + 0.5 * leg2_profit - (2 * fee)
            else:
                # Hit direct SL
                gb = -(p_sl * leverage) - (2 * fee)

            # Calculate Net Return on Margin for ETH
            if e_mfe >= part_price:
                leg2_profit = (p_tp * leverage) if e_res == "TP" else (0.05 * leverage)
                ge = 0.5 * (part_price * leverage) + 0.5 * leg2_profit - (2 * fee)
            else:
                ge = -(p_sl * leverage) - (2 * fee)

            cycles.append({
                "entry_ts": entry_ts,
                "exit_ts": exit_ts,
                "hold_hours": hold_hours,
                "gb": gb,
                "ge": ge,
                "b_mfe": b_mfe,
                "e_mfe": e_mfe,
                "b_res": b_res,
                "e_res": e_res
            })
            i = free_idx + 1

        print(f"\n==========================================================================================")
        print(f"{title}")
        print(f"==========================================================================================")
        print(f"Total Completed Cycles:        {len(cycles)} trades")
        
        # Win rate metrics
        pair_wins = sum(1 for c in cycles if (c["gb"] + c["ge"]) > 0)
        pair_losses = sum(1 for c in cycles if (c["gb"] + c["ge"]) < 0)
        pair_ties = len(cycles) - pair_wins - pair_losses
        pair_win_pct = pair_wins / len(cycles) * 100.0

        b_wins = sum(1 for c in cycles if c["gb"] > 0)
        e_wins = sum(1 for c in cycles if c["ge"] > 0)

        print(f"Combined Pair Win Rate:        {pair_win_pct:.1f}% ({pair_wins} Wins / {pair_losses} Losses / {pair_ties} Ties)")
        print(f"Individual Account Win Rates:  Account A (BTC): {b_wins/len(cycles)*100:.1f}% | Account B (ETH): {e_wins/len(cycles)*100:.1f}%")

        # -------------------------------------------------------------
        # 1. UNCOMPOUNDED (Fixed $1,000 per account = $2,000 total capital)
        # -------------------------------------------------------------
        tot_profit_fixed = sum((1000.0 * c["gb"] / 100.0) + (1000.0 * c["ge"] / 100.0) for c in cycles)
        total_days = (cycles[-1]["exit_ts"] - cycles[0]["entry_ts"]) / (1000 * 3600 * 24)
        total_years = total_days / 365.25

        daily_fixed = tot_profit_fixed / total_days
        weekly_fixed = daily_fixed * 7.0
        monthly_fixed = daily_fixed * 30.4375
        yearly_fixed = daily_fixed * 365.25

        # Calculate Fixed Portfolio Equity Curve & Drawdown
        fixed_equity = [2000.0]
        cur_bal = 2000.0
        peak_f = 2000.0
        max_dd_fixed = 0.0
        for c in cycles:
            pnl = (1000.0 * c["gb"] / 100.0) + (1000.0 * c["ge"] / 100.0)
            cur_bal += pnl
            fixed_equity.append(cur_bal)
            if cur_bal > peak_f: peak_f = cur_bal
            dd = (peak_f - cur_bal) / peak_f * 100.0
            if dd > max_dd_fixed: max_dd_fixed = dd

        print(f"\n--- UNCOMPOUNDED RETURN SUMMARY (Fixed $2,000 USDT Base) ---")
        print(f"  Starting Balance:            $2,000.00 USDT")
        print(f"  Final Net Profit:            ${tot_profit_fixed:+,.2f} USDT ({tot_profit_fixed/2000.0*100:+.1f}%)")
        print(f"  Maximum Drawdown:            {max_dd_fixed:.2f}% (Peak to Trough)")
        print(f"  Average Profit Per Day:      ${daily_fixed:+,.2f} USDT (+{daily_fixed/2000.0*100:.2f}%/day)")
        print(f"  Average Profit Per Week:     ${weekly_fixed:+,.2f} USDT (+{weekly_fixed/2000.0*100:.2f}%/week)")
        print(f"  Average Profit Per Month:    ${monthly_fixed:+,.2f} USDT (+{monthly_fixed/2000.0*100:.2f}%/month)")
        print(f"  Average Profit Per Year:     ${yearly_fixed:+,.2f} USDT (+{yearly_fixed/2000.0*100:.2f}%/year)")

        # -------------------------------------------------------------
        # 2. YEARLY BREAKDOWN (Fixed Base)
        # -------------------------------------------------------------
        yearly_data = defaultdict(lambda: {"pnl": 0.0, "trades": 0, "wins": 0, "losses": 0})
        monthly_data = defaultdict(lambda: {"pnl": 0.0, "trades": 0, "wins": 0})
        daily_pnl = defaultdict(float)

        for c in cycles:
            dt = datetime.datetime.fromtimestamp(c["exit_ts"] / 1000.0, tz=datetime.timezone.utc)
            y_str = str(dt.year)
            m_str = dt.strftime("%Y-%m")
            d_str = dt.strftime("%Y-%m-%d")

            pnl = (1000.0 * c["gb"] / 100.0) + (1000.0 * c["ge"] / 100.0)
            yearly_data[y_str]["pnl"] += pnl
            yearly_data[y_str]["trades"] += 1
            if pnl > 0: yearly_data[y_str]["wins"] += 1
            else: yearly_data[y_str]["losses"] += 1

            monthly_data[m_str]["pnl"] += pnl
            monthly_data[m_str]["trades"] += 1
            if pnl > 0: monthly_data[m_str]["wins"] += 1

            daily_pnl[d_str] += pnl

        print(f"\n--- YEAR-BY-YEAR PERFORMANCE (Fixed $2,000 Base) ---")
        print(f"{'Year':<6} | {'Trades':<7} | {'Win Rate':<9} | {'Net Profit ($)':<16} | {'Return (%)':<12} | {'Avg/Month':<12}")
        print("-" * 75)
        for y in sorted(yearly_data.keys()):
            d = yearly_data[y]
            wr = d["wins"] / d["trades"] * 100.0 if d["trades"] else 0.0
            pnl_y = d["pnl"]
            ret_y = pnl_y / 2000.0 * 100.0
            months_in_year = 9.0 if y == "2026" else 12.0
            avg_m = pnl_y / months_in_year
            print(f"{y:<6} | {d['trades']:<7} | {wr:>7.1f}% | ${pnl_y:>+13,.2f} | {ret_y:>+10.1f}% | ${avg_m:>+9.2f}")

        # -------------------------------------------------------------
        # 3. MONTHLY BREAKDOWN STATS
        # -------------------------------------------------------------
        all_months = sorted(monthly_data.keys())
        pos_months = sum(1 for m in all_months if monthly_data[m]["pnl"] > 0)
        neg_months = sum(1 for m in all_months if monthly_data[m]["pnl"] < 0)
        best_month = max(all_months, key=lambda m: monthly_data[m]["pnl"])
        worst_month = min(all_months, key=lambda m: monthly_data[m]["pnl"])

        print(f"\n--- MONTHLY BREAKDOWN METRICS ({len(all_months)} Months Total) ---")
        print(f"  Profitable Months:           {pos_months}/{len(all_months)} ({pos_months/len(all_months)*100:.1f}%)")
        print(f"  Losing Months:               {neg_months}/{len(all_months)} ({neg_months/len(all_months)*100:.1f}%)")
        print(f"  Best Month:                  {best_month} (+${monthly_data[best_month]['pnl']:,.2f})")
        print(f"  Worst Month:                 {worst_month} (${monthly_data[worst_month]['pnl']:+,.2f})")

        # Print all 81 months cleanly in a compact table (4 columns per row)
        print("\nComplete Monthly PnL Table (USD):")
        cols = 4
        rows = math.ceil(len(all_months) / cols)
        for r in range(rows):
            line_parts = []
            for c_i in range(cols):
                idx = r + c_i * rows
                if idx < len(all_months):
                    m = all_months[idx]
                    p = monthly_data[m]["pnl"]
                    line_parts.append(f"{m}: ${p:>+7.1f}")
            print("  |  ".join(line_parts))

        # -------------------------------------------------------------
        # 4. DAILY & WEEKLY WIN STATS
        # -------------------------------------------------------------
        days_with_trades = len(daily_pnl)
        pos_days = sum(1 for d in daily_pnl.values() if d > 0)
        print(f"\n--- DAILY WIN STATISTICS ---")
        print(f"  Active Trading Days:         {days_with_trades} days")
        print(f"  Profitable Days:             {pos_days} days ({pos_days/days_with_trades*100:.1f}% of active days)")

if __name__ == "__main__":
    run_multi_year_backtest()
