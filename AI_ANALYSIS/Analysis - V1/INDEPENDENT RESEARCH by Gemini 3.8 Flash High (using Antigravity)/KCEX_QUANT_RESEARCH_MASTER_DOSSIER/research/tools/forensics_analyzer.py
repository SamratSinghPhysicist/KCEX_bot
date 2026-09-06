import os
import sys
import csv
import math
import glob
import datetime
from typing import List, Dict, Any, Tuple
from collections import defaultdict

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.data_loader import TickTradeStreamer, TradeTick

def parse_utc_str_to_ms(s: str) -> int:
    clean = s.replace(" UTC", "").strip()
    dt = datetime.datetime.strptime(clean, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)

def analyze_trade_forensics(
    trades_csv_path: str,
    trades_tick_dir: str = os.path.join(ROOT_DIR, "BACKTESTER", "Historical_Trades_Data_Binance"),
    symbol: str = "TRUMP_USDT",
    max_trades: int = 0
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    print(f"[*] Reading trades from {trades_csv_path}...")
    trades = []
    with open(trades_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            trades.append(r)
            if max_trades > 0 and len(trades) >= max_trades:
                break

    print(f"[*] Loaded {len(trades)} trades. Initializing TickStreamer...")
    streamer = TickTradeStreamer(data_dir=trades_tick_dir)
    pu = 0.001

    analyzed_trades = []
    print(f"[*] Processing trade excursions and pre-entry dynamics...")

    for i, tr in enumerate(trades):
        if (i + 1) % 500 == 0 or i == len(trades) - 1:
            print(f"    Progress: {i + 1}/{len(trades)} trades processed...")

        open_ms = parse_utc_str_to_ms(tr["open_time"])
        close_ms = parse_utc_str_to_ms(tr["close_time"])
        direction = tr["direction"].upper()
        entry_p = float(tr["entry_price"])
        exit_p = float(tr["exit_price"])
        is_win = float(tr["realized_pnl_usdt"]) > 0
        duration = float(tr["duration_seconds"])

        # Stream ticks from 60s before entry to close
        pre_start_ms = open_ms - 60_000
        ticks = list(streamer.stream_ticks(symbol, start_ms=pre_start_ms, end_ms=close_ms + 1000))

        pre_ticks = [tk for tk in ticks if tk.timestamp_ms < open_ms]
        post_ticks = [tk for tk in ticks if open_ms <= tk.timestamp_ms <= close_ms]

        # 1. Pre-entry features
        pre_10s_ticks = [tk for tk in pre_ticks if tk.timestamp_ms >= open_ms - 10_000]
        pre_30s_ticks = [tk for tk in pre_ticks if tk.timestamp_ms >= open_ms - 30_000]

        p_t0 = pre_ticks[-1].price if pre_ticks else entry_p
        p_m10 = pre_10s_ticks[0].price if pre_10s_ticks else p_t0
        p_m30 = pre_30s_ticks[0].price if pre_30s_ticks else p_t0
        p_m60 = pre_ticks[0].price if pre_ticks else p_t0

        ret_10s_ticks = (p_t0 - p_m10) / pu if direction == "LONG" else (p_m10 - p_t0) / pu
        ret_30s_ticks = (p_t0 - p_m30) / pu if direction == "LONG" else (p_m30 - p_t0) / pu
        ret_60s_ticks = (p_t0 - p_m60) / pu if direction == "LONG" else (p_m60 - p_t0) / pu

        if len(pre_ticks) >= 2:
            prices_60 = [tk.price for tk in pre_ticks]
            range_60s_ticks = (max(prices_60) - min(prices_60)) / pu
            path_len = sum(abs(prices_60[k] - prices_60[k-1]) for k in range(1, len(prices_60)))
            displacement = abs(prices_60[-1] - prices_60[0])
            dir_eff_60s = (displacement / path_len) if path_len > 1e-8 else 1.0
            
            signs = []
            for k in range(1, len(prices_60)):
                diff = prices_60[k] - prices_60[k-1]
                if diff > 0: signs.append(1)
                elif diff < 0: signs.append(-1)
            reversals_60s = sum(1 for k in range(1, len(signs)) if signs[k] != signs[k-1])
        else:
            range_60s_ticks = 0.0
            dir_eff_60s = 1.0
            reversals_60s = 0

        # 2. Post-entry excursion metrics
        if post_ticks:
            post_prices = [tk.price for tk in post_ticks]
            if direction == "LONG":
                mfe_ticks = (max(post_prices) - entry_p) / pu
                mae_ticks = (entry_p - min(post_prices)) / pu
            else:
                mfe_ticks = (entry_p - min(post_prices)) / pu
                mae_ticks = (max(post_prices) - entry_p) / pu
        else:
            mfe_ticks = (exit_p - entry_p)/pu if direction == "LONG" else (entry_p - exit_p)/pu
            mae_ticks = -mfe_ticks

        loss_cat = "WIN"
        if not is_win:
            if duration <= 15.0:
                loss_cat = "IMMEDIATE_REVERSAL"
            elif mfe_ticks >= 1.0:
                loss_cat = "NEAR_TP_REVERSAL"
            elif duration >= 60.0:
                loss_cat = "SLOW_DRIFT"
            else:
                loss_cat = "CHOP_FAILURE"

        analyzed_trades.append({
            "trade_id": tr["trade_id"],
            "direction": direction,
            "is_win": is_win,
            "duration": duration,
            "pnl": float(tr["realized_pnl_usdt"]),
            "mfe_ticks": round(mfe_ticks, 2),
            "mae_ticks": round(mae_ticks, 2),
            "ret_10s_ticks": round(ret_10s_ticks, 2),
            "ret_30s_ticks": round(ret_30s_ticks, 2),
            "ret_60s_ticks": round(ret_60s_ticks, 2),
            "range_60s_ticks": round(range_60s_ticks, 2),
            "dir_eff_60s": round(dir_eff_60s, 3),
            "reversals_60s": reversals_60s,
            "pre_ticks_count": len(pre_ticks),
            "loss_cat": loss_cat
        })

    total_count = len(analyzed_trades)
    win_trades = [t for t in analyzed_trades if t["is_win"]]
    loss_trades = [t for t in analyzed_trades if not t["is_win"]]

    def mean(lst):
        return sum(lst)/len(lst) if lst else 0.0

    report = {
        "total_trades": total_count,
        "wins": len(win_trades),
        "losses": len(loss_trades),
        "win_rate": len(win_trades)/total_count*100 if total_count else 0,
        "loss_breakdown": {},
        "feature_comparison": {}
    }

    for cat in ["IMMEDIATE_REVERSAL", "NEAR_TP_REVERSAL", "SLOW_DRIFT", "CHOP_FAILURE"]:
        cat_trades = [t for t in loss_trades if t["loss_cat"] == cat]
        report["loss_breakdown"][cat] = {
            "count": len(cat_trades),
            "pct_of_losses": (len(cat_trades)/len(loss_trades)*100) if loss_trades else 0,
            "pct_of_all": (len(cat_trades)/total_count*100) if total_count else 0,
            "avg_duration": round(mean([t["duration"] for t in cat_trades]), 1),
            "avg_mfe": round(mean([t["mfe_ticks"] for t in cat_trades]), 2),
            "avg_mae": round(mean([t["mae_ticks"] for t in cat_trades]), 2),
            "avg_pnl": round(mean([t["pnl"] for t in cat_trades]), 6)
        }

    features = [
        "ret_10s_ticks", "ret_30s_ticks", "ret_60s_ticks",
        "range_60s_ticks", "dir_eff_60s", "reversals_60s", "pre_ticks_count"
    ]
    for feat in features:
        w_vals = [t[feat] for t in win_trades]
        l_vals = [t[feat] for t in loss_trades]
        w_mean = mean(w_vals)
        l_mean = mean(l_vals)
        diff = l_mean - w_mean
        report["feature_comparison"][feat] = {
            "winner_mean": round(w_mean, 3),
            "loser_mean": round(l_mean, 3),
            "difference": round(diff, 3)
        }

    return report, analyzed_trades

if __name__ == "__main__":
    csv_file = glob.glob(os.path.join(ROOT_DIR, "research", "experiments", "EXP_0001", "*.csv"))[0]
    rep, detailed = analyze_trade_forensics(csv_file)
    print("\n================ FORENSIC REPORT: EXP_0001 (STOCH_RSI) ================")
    print(f"Total Trades: {rep['total_trades']} | Wins: {rep['wins']} ({rep['win_rate']:.1f}%) | Losses: {rep['losses']}")
    print("\n--- LOSS CATEGORY BREAKDOWN ---")
    for k, v in rep["loss_breakdown"].items():
        print(f"{k:<22}: {v['count']:>4} ({v['pct_of_losses']:>5.1f}% of losses) | Avg MFE: {v['avg_mfe']:>4.1f}t | Avg Dur: {v['avg_duration']:>5.1f}s | Avg PnL: {v['avg_pnl']:>8.4f}")

    print("\n--- PRE-ENTRY FEATURE COMPARISON (WINNERS vs LOSERS) ---")
    print(f"{'Feature':<25} | {'Winners Mean':<12} | {'Losers Mean':<12} | {'Diff (L - W)':<12}")
    print("-" * 68)
    for feat, vals in rep["feature_comparison"].items():
        print(f"{feat:<25} | {vals['winner_mean']:<12.3f} | {vals['loser_mean']:<12.3f} | {vals['difference']:<+12.3f}")
