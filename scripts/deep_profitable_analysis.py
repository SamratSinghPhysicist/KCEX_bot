"""
Deep Quantitative Data Analysis for Profitable KCEX Backtest Configurations
===========================================================================
Analyzes all profitable configurations across 20 pairs and 5 timeframes:
- Deep performance metrics
- Granular month-by-month financial breakdown
- Granular week-by-week financial breakdown
- Statistical significance evaluation (sample size, win/loss ratio, streaks)
- Production recommendations for live bot deployment
"""

import os
import sys
import glob
import json
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_all_profitable_configurations(artifacts_dir: str = "local_matrix_artifacts") -> List[Dict[str, Any]]:
    json_files = glob.glob(os.path.join(artifacts_dir, "results_*.json"))
    profitable = []

    for fpath in json_files:
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            metrics = data.get("metrics", {})
            params = data.get("parameters", {})
            roi = metrics.get("total_roi_pct", 0.0)

            if roi > 0:
                pair = data["pair"]
                tf = data["timeframe"]
                csv_path = os.path.join(artifacts_dir, f"results_{pair}_{tf}.csv")
                profitable.append({
                    "pair": pair,
                    "binance_symbol": data.get("binance_symbol", pair.replace("_", "")),
                    "timeframe": tf,
                    "roi_pct": roi,
                    "net_pnl": metrics.get("net_pnl_usdt", 0.0),
                    "fees": metrics.get("total_fees_usdt", 0.0),
                    "gross_pnl": metrics.get("net_pnl_usdt", 0.0) + metrics.get("total_fees_usdt", 0.0),
                    "trades": metrics.get("total_trades", 0),
                    "wins": metrics.get("winning_trades", 0),
                    "losses": metrics.get("losing_trades", 0),
                    "win_rate": metrics.get("win_rate_pct", 0.0),
                    "profit_factor": metrics.get("profit_factor", 0.0),
                    "max_drawdown_pct": metrics.get("max_drawdown_pct", 0.0),
                    "max_drawdown_usdt": metrics.get("max_drawdown_usdt", 0.0),
                    "sharpe": metrics.get("sharpe_ratio", 0.0),
                    "sortino": metrics.get("sortino_ratio", 0.0),
                    "calmar": metrics.get("calmar_ratio", 0.0),
                    "monthly_freq": metrics.get("monthly_signal_frequency", 0.0),
                    "avg_trade_pnl": metrics.get("avg_trade_pnl_usdt", 0.0),
                    "avg_win": metrics.get("avg_win_usdt", 0.0),
                    "avg_loss": metrics.get("avg_loss_usdt", 0.0),
                    "win_loss_ratio": metrics.get("win_loss_ratio", 0.0),
                    "is_zero_fee": params.get("is_zero_fee", False),
                    "taker_fee_rate": params.get("taker_fee_rate", 0.0),
                    "csv_path": csv_path
                })
        except Exception as e:
            print(f"[!] Error loading {fpath}: {e}")

    profitable.sort(key=lambda x: x["roi_pct"], reverse=True)
    return profitable


def parse_trades_csv(csv_path: str) -> List[Dict[str, Any]]:
    trades = []
    if not os.path.exists(csv_path):
        return trades

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Handle possible varying headers
                net_pnl = float(row.get("net_pnl_usdt", row.get("realized_pnl_usdt", 0.0)))
                fee_total = float(row.get("total_fee_usdt", 0.0))
                gross_pnl = float(row.get("gross_pnl_usdt", net_pnl + fee_total))
                entry_time_str = row.get("entry_time_utc", "")
                exit_time_str = row.get("exit_time_utc", "")
                
                dt_entry = None
                if entry_time_str:
                    try:
                        dt_entry = datetime.strptime(entry_time_str[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    except Exception:
                        pass

                trades.append({
                    "trade_id": int(row.get("trade_id", 0)),
                    "entry_time": dt_entry,
                    "entry_str": entry_time_str,
                    "exit_str": exit_time_str,
                    "direction": row.get("direction", ""),
                    "entry_price": float(row.get("entry_price", 0.0)),
                    "exit_price": float(row.get("exit_price", 0.0)),
                    "contracts": float(row.get("contracts", 1.0)),
                    "margin_usdt": float(row.get("margin_usdt", 0.0)),
                    "gross_pnl_usdt": gross_pnl,
                    "fee_total_usdt": fee_total,
                    "net_pnl_usdt": net_pnl,
                    "roe_pct": float(row.get("roe_pct", 0.0)),
                    "exit_reason": row.get("exit_reason", ""),
                    "duration_seconds": float(row.get("duration_seconds", 0.0)),
                    "wallet_balance_usdt": float(row.get("wallet_balance_usdt", 100.0))
                })
            except Exception as e:
                continue

    return trades


def analyze_monthly_breakdown(trades: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    monthly = defaultdict(lambda: {
        "trades": 0, "wins": 0, "losses": 0, "gross_pnl": 0.0, "fees": 0.0, "net_pnl": 0.0
    })

    for t in trades:
        dt = t["entry_time"]
        if not dt:
            continue
        m_key = dt.strftime("%Y-%m")
        monthly[m_key]["trades"] += 1
        pnl = t["net_pnl_usdt"]
        if pnl > 0.0001:
            monthly[m_key]["wins"] += 1
        elif pnl < -0.0001:
            monthly[m_key]["losses"] += 1
        monthly[m_key]["gross_pnl"] += t["gross_pnl_usdt"]
        monthly[m_key]["fees"] += t["fee_total_usdt"]
        monthly[m_key]["net_pnl"] += pnl

    # compute win rates
    res = {}
    for m in sorted(monthly.keys()):
        d = monthly[m]
        tr = d["trades"]
        wr = (d["wins"] / tr * 100.0) if tr > 0 else 0.0
        res[m] = {
            "trades": tr,
            "wins": d["wins"],
            "losses": d["losses"],
            "win_rate_pct": round(wr, 1),
            "gross_pnl_usdt": round(d["gross_pnl"], 2),
            "fees_usdt": round(d["fees"], 3),
            "net_pnl_usdt": round(d["net_pnl"], 2)
        }
    return res


def analyze_weekly_breakdown(trades: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    weekly = defaultdict(lambda: {
        "trades": 0, "wins": 0, "losses": 0, "net_pnl": 0.0, "fees": 0.0
    })

    for t in trades:
        dt = t["entry_time"]
        if not dt:
            continue
        # ISO calendar: (year, week_num, weekday)
        iso_year, iso_week, _ = dt.isocalendar()
        w_key = f"{iso_year}-W{iso_week:02d}"
        weekly[w_key]["trades"] += 1
        pnl = t["net_pnl_usdt"]
        if pnl > 0.0001:
            weekly[w_key]["wins"] += 1
        elif pnl < -0.0001:
            weekly[w_key]["losses"] += 1
        weekly[w_key]["net_pnl"] += pnl
        weekly[w_key]["fees"] += t["fee_total_usdt"]

    res = {}
    for w in sorted(weekly.keys()):
        d = weekly[w]
        tr = d["trades"]
        wr = (d["wins"] / tr * 100.0) if tr > 0 else 0.0
        res[w] = {
            "trades": tr,
            "wins": d["wins"],
            "losses": d["losses"],
            "win_rate_pct": round(wr, 1),
            "net_pnl_usdt": round(d["net_pnl"], 2),
            "fees_usdt": round(d["fees"], 3)
        }
    return res


def compute_trade_streaks(trades: List[Dict[str, Any]]) -> Dict[str, int]:
    max_win_streak = 0
    max_loss_streak = 0
    curr_wins = 0
    curr_losses = 0

    for t in trades:
        pnl = t["net_pnl_usdt"]
        if pnl > 0.0001:
            curr_wins += 1
            curr_losses = 0
            if curr_wins > max_win_streak:
                max_win_streak = curr_wins
        elif pnl < -0.0001:
            curr_losses += 1
            curr_wins = 0
            if curr_losses > max_loss_streak:
                max_loss_streak = curr_losses
        else:
            curr_wins = 0
            curr_losses = 0

    return {
        "max_consecutive_wins": max_win_streak,
        "max_consecutive_losses": max_loss_streak
    }


def main():
    profitable = load_all_profitable_configurations()
    print("=" * 100)
    print(f"📊 DEEP QUANTITATIVE DATA ANALYSIS ON {len(profitable)} PROFITABLE CONFIGURATIONS")
    print("=" * 100)

    all_detailed = []

    for item in profitable:
        trades = parse_trades_csv(item["csv_path"])
        monthly = analyze_monthly_breakdown(trades)
        weekly = analyze_weekly_breakdown(trades)
        streaks = compute_trade_streaks(trades)

        # Count profitable months and weeks
        pos_months = sum(1 for m, d in monthly.items() if d["net_pnl_usdt"] > 0)
        tot_months = len(monthly)
        month_win_rate = (pos_months / tot_months * 100.0) if tot_months > 0 else 0.0

        pos_weeks = sum(1 for w, d in weekly.items() if d["net_pnl_usdt"] > 0)
        tot_weeks = len(weekly)
        week_win_rate = (pos_weeks / tot_weeks * 100.0) if tot_weeks > 0 else 0.0

        item["trades_data"] = trades
        item["monthly_breakdown"] = monthly
        item["weekly_breakdown"] = weekly
        item["streaks"] = streaks
        item["profitable_months_ratio"] = f"{pos_months}/{tot_months} ({month_win_rate:.0f}%)"
        item["profitable_weeks_ratio"] = f"{pos_weeks}/{tot_weeks} ({week_win_rate:.0f}%)"

        # Statistical significance classification
        tr = item["trades"]
        if tr >= 40:
            stat_tier = "HIGH_CONFIDENCE (Robust Sample >= 40 trades)"
        elif tr >= 10:
            stat_tier = "MEDIUM_CONFIDENCE (Moderate Sample 10-39 trades)"
        elif tr >= 4:
            stat_tier = "EMERGING_ALPHA (Low Sample 4-9 trades)"
        else:
            stat_tier = "SAMPLE_SIZE_WARNING (Sparse Sample <= 3 trades)"
        item["statistical_tier"] = stat_tier

        all_detailed.append(item)

    # Export comprehensive analysis JSON
    out_json = "final_matrix_reports/profitable_deep_analysis.json"
    with open(out_json, "w", encoding="utf-8") as f:
        # omit raw trades_data for compactness
        export_payload = []
        for x in all_detailed:
            d = dict(x)
            d.pop("trades_data", None)
            export_payload.append(d)
        json.dump(export_payload, f, indent=2)
    print(f"[+] Exported detailed analysis JSON: {out_json}")

    # Print Summary Table
    print("\n" + "-" * 115)
    print(f"{'Pair':<15} | {'TF':<4} | {'ROI (%)':<9} | {'Net PnL':<9} | {'Trades':<6} | {'WR (%)':<6} | {'PF':<5} | {'Max DD':<7} | {'Win Months':<12} | {'Confidence Tier'}")
    print("-" * 115)
    for p in all_detailed:
        print(f"{p['pair']:<15} | {p['timeframe'].upper():<4} | {p['roi_pct']:+7.2f}% | ${p['net_pnl']:>7.2f} | {p['trades']:<6} | {p['win_rate']:5.1f}% | {p['profit_factor']:4.2f} | {p['max_drawdown_pct']:5.1f}% | {p['profitable_months_ratio']:<12} | {p['statistical_tier'].split()[0]}")
    print("-" * 115)


if __name__ == "__main__":
    main()
