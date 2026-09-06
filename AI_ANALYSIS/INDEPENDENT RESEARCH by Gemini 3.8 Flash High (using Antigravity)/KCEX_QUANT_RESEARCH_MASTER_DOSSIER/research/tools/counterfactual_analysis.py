import os
import sys
import csv
import glob
import datetime
from typing import List, Dict, Any, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.data_loader import TickTradeStreamer

def parse_utc_str_to_ms(s: str) -> int:
    clean = s.replace(" UTC", "").strip()
    dt = datetime.datetime.strptime(clean, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)

def run_counterfactual_audit(
    trades_csv_path: str,
    trades_tick_dir: str = os.path.join(ROOT_DIR, "BACKTESTER", "Historical_Trades_Data_Binance"),
    symbol: str = "TRUMP_USDT"
):
    print(f"[*] Loading baseline trades from {trades_csv_path}...")
    trades = []
    with open(trades_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            trades.append(r)

    print(f"[*] Loaded {len(trades)} trades. Initializing TickStreamer...")
    streamer = TickTradeStreamer(data_dir=trades_tick_dir)
    pu = 0.001
    cs = 0.1
    vol_contracts = 2
    qty = vol_contracts * cs # 0.2 TRUMP

    # Counters for Breakeven-on-+1 rule
    be_avoided_losses = 0
    be_avoided_loss_pnl = 0.0
    be_sacrificed_wins = 0
    be_sacrificed_win_pnl = 0.0
    be_unaffected_wins = 0
    be_unaffected_losses = 0

    # Counters for Timeouts: 30s, 60s, 90s, 120s, 180s, 300s
    timeouts = [30, 45, 60, 90, 120, 180, 300]
    timeout_stats = {t: {"avoided_losses": 0, "saved_loss_pnl": 0.0, "killed_wins": 0, "lost_win_pnl": 0.0, "net_delta_pnl": 0.0} for t in timeouts}

    baseline_total_pnl = sum(float(t["realized_pnl_usdt"]) for t in trades)
    print(f"[*] Baseline Net PnL: {baseline_total_pnl:+.4f} USDT across {len(trades)} trades.")
    print(f"[*] Streaming ticks and performing counterfactual replay...")

    for i, tr in enumerate(trades):
        if (i + 1) % 500 == 0 or i == len(trades) - 1:
            print(f"    Progress: {i + 1}/{len(trades)} trades evaluated...")

        open_ms = parse_utc_str_to_ms(tr["open_time"])
        close_ms = parse_utc_str_to_ms(tr["close_time"])
        direction = tr["direction"].upper()
        entry_p = float(tr["entry_price"])
        exit_p = float(tr["exit_price"])
        tp_p = float(tr["min_profit_tp_price"])
        sl_p = float(tr["stop_loss_price"])
        orig_pnl = float(tr["realized_pnl_usdt"])
        orig_win = orig_pnl > 0
        orig_dur = float(tr["duration_seconds"])

        ticks = list(streamer.stream_ticks(symbol, start_ms=open_ms, end_ms=close_ms + 1000))
        if not ticks:
            continue

        # 1. Counterfactual Breakeven-on-+1 Rule Replay
        hit_plus_1 = False
        re_touched_entry_after_plus_1 = False
        be_rule_outcome_pnl = orig_pnl

        for tk in ticks:
            p = tk.price
            favorable_ticks = (p - entry_p) / pu if direction == "LONG" else (entry_p - p) / pu

            if not hit_plus_1:
                if favorable_ticks >= 1.0:
                    hit_plus_1 = True
            else:
                # We have touched +1 tick; check if it hits TP (+2) or retraces to entry (<= 0)
                if favorable_ticks >= 2.0:
                    # Hit TP!
                    break
                elif favorable_ticks <= 0.0:
                    # Retraced to entry! Breakeven exit triggers!
                    re_touched_entry_after_plus_1 = True
                    be_rule_outcome_pnl = 0.0 # Closed at entry price with zero fees
                    break

        if orig_win:
            if re_touched_entry_after_plus_1:
                be_sacrificed_wins += 1
                be_sacrificed_win_pnl += orig_pnl # Lost the +0.0004
            else:
                be_unaffected_wins += 1
        else:
            if re_touched_entry_after_plus_1:
                be_avoided_losses += 1
                be_avoided_loss_pnl += abs(orig_pnl) # Saved the loss!
            else:
                be_unaffected_losses += 1

        # 2. Counterfactual Duration Timeout Replay
        for t_limit in timeouts:
            if orig_dur > t_limit:
                limit_ms = open_ms + (t_limit * 1000)
                # Find price at limit_ms
                ticks_at_limit = [tk for tk in ticks if tk.timestamp_ms >= limit_ms]
                price_at_limit = ticks_at_limit[0].price if ticks_at_limit else exit_p
                
                # Realized PnL if closed at market at time t_limit
                diff = (price_at_limit - entry_p) if direction == "LONG" else (entry_p - price_at_limit)
                timeout_pnl = qty * diff

                if orig_win:
                    # We killed a winning trade that would have reached TP later
                    lost = orig_pnl - timeout_pnl
                    timeout_stats[t_limit]["killed_wins"] += 1
                    timeout_stats[t_limit]["lost_win_pnl"] += lost
                else:
                    # We intervened on a losing trade that would have hit full SL later
                    saved = timeout_pnl - orig_pnl
                    timeout_stats[t_limit]["avoided_losses"] += 1
                    timeout_stats[t_limit]["saved_loss_pnl"] += saved

    # Summaries
    print("\n" + "=" * 80)
    print("      COUNTERFACTUAL AUDIT 1: BREAKEVEN STOP ON +1 TICK EXCURSION")
    print("=" * 80)
    net_be_impact = be_avoided_loss_pnl - be_sacrificed_win_pnl
    counterfactual_be_pnl = baseline_total_pnl + net_be_impact
    print(f"Avoided Losses:            {be_avoided_losses} trades (Saved: +{be_avoided_loss_pnl:.4f} USDT)")
    print(f"Sacrificed Winners:        {be_sacrificed_wins} trades (Lost: -{be_sacrificed_win_pnl:.4f} USDT)")
    print(f"Unaffected Winners:        {be_unaffected_wins} trades")
    print(f"Unaffected Losses:         {be_unaffected_losses} trades")
    print(f"Net Economic Impact:       {net_be_impact:+.4f} USDT")
    print(f"Counterfactual Net PnL:    {counterfactual_be_pnl:+.4f} USDT vs Baseline {baseline_total_pnl:+.4f} USDT")

    print("\n" + "=" * 80)
    print("      COUNTERFACTUAL AUDIT 2: HARD TIME-BASED TIMEOUT EXITS (AT MARKET)")
    print("=" * 80)
    print(f"{'Timeout (s)':<12} | {'Avoided Losses':<15} | {'Saved PnL':<12} | {'Killed Wins':<12} | {'Lost PnL':<12} | {'Net Impact':<12} | {'New Net PnL':<12}")
    print("-" * 92)
    for t_limit in timeouts:
        st = timeout_stats[t_limit]
        net_imp = st["saved_loss_pnl"] - st["lost_win_pnl"]
        new_pnl = baseline_total_pnl + net_imp
        print(f"{t_limit:<12} | {st['avoided_losses']:<15} | {st['saved_loss_pnl']:>+10.4f}  | {st['killed_wins']:<12} | {st['lost_win_pnl']:>+10.4f} | {net_imp:>+10.4f}  | {new_pnl:>+10.4f}")

if __name__ == "__main__":
    csv_file = glob.glob(os.path.join(ROOT_DIR, "research", "experiments", "EXP_0001", "*.csv"))[0]
    run_counterfactual_audit(csv_file)
