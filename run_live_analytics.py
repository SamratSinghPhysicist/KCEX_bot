"""
KCEX Live Trading Analytics Dashboard
======================================
Interactive terminal script to view comprehensive analytics of all live bot
trades stored in MongoDB. Also displays live KCEX account balance.

Usage:
    python run_live_analytics.py

Note: For bot performance analytics, this relies exclusively on verified
trade logs in MongoDB (not KCEX account history, which includes manual trades).
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Automatically load .env file
try:
    from kcex.config import load_env_file
    load_env_file()
except Exception:
    pass


# =========================================================================
# FORMATTING HELPERS
# =========================================================================

def fmt_usdt(val: float, sign: bool = True) -> str:
    s = "+" if val > 0 and sign else ""
    return f"{s}{val:.6f} USDT"

def fmt_inr(val: float, sign: bool = True) -> str:
    s = "+" if val > 0 and sign else ""
    return f"{s}₹{val:.4f}"

def fmt_dual(usdt: float, inr: float, sign: bool = True) -> str:
    return f"{fmt_usdt(usdt, sign)} ({fmt_inr(inr, sign)})"

def fmt_pct(val: float, sign: bool = True) -> str:
    s = "+" if val > 0 and sign else ""
    return f"{s}{val:.2f}%"

def fmt_time(dt: Optional[datetime]) -> str:
    if dt is None:
        return "N/A"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ist = dt + timedelta(hours=5, minutes=30)
    return ist.strftime("%Y-%m-%d %H:%M:%S IST")


BANNER = r"""
==============================================================================
   _  _______ _______  __    _              _         _   _
  | |/ / ____|  ____| \ \  | |    (_)      / \   _ _ | | | |_   _
  | ' / |    | |__     \ \ | |     _  __ _/  _\ | '_\| |_| | | | |
  |  <| |    |  __|     > \| |___ | |/ _/ /| |  | | ||  _  | |_| |
  | . \ |____| |____   / . \_   _|| |  V /\| |  |_| ||_| |_|\__, |
  |_|\_\_____|______|_/_/ \_\|_|  |_|\_/   |_|            \  |___/
                                                 LIVE BOT ANALYTICS
=============================================================================="""


def print_separator(char: str = "─", width: int = 78):
    print(char * width)


def print_header(title: str, width: int = 78):
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


# =========================================================================
# ANALYTICS COMPUTATIONS
# =========================================================================

def compute_analytics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute comprehensive analytics from MongoDB trade documents."""
    if not trades:
        return {"total_trades": 0}

    total = len(trades)
    wins = [t for t in trades if t.get("realized_pnl_usdt", 0) > 0]
    losses = [t for t in trades if t.get("realized_pnl_usdt", 0) < -1e-8]
    scratches = [t for t in trades if abs(t.get("realized_pnl_usdt", 0)) <= 1e-8]

    total_pnl_usdt = sum(t.get("realized_pnl_usdt", 0) for t in trades)
    total_pnl_inr = sum(t.get("realized_pnl_inr", 0) for t in trades)
    total_fees_usdt = sum(t.get("fee_total_usdt", 0) for t in trades)
    total_fees_inr = sum(t.get("fee_total_inr", 0) for t in trades)

    pnl_list = [t.get("realized_pnl_usdt", 0) for t in trades]
    best_trade = max(pnl_list) if pnl_list else 0
    worst_trade = min(pnl_list) if pnl_list else 0

    # Win rate
    win_rate = (len(wins) / total * 100) if total > 0 else 0

    # Profit factor
    gross_profit = sum(t.get("realized_pnl_usdt", 0) for t in wins) if wins else 0
    gross_loss = abs(sum(t.get("realized_pnl_usdt", 0) for t in losses)) if losses else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf') if gross_profit > 0 else 0

    # Expectancy
    expectancy_usdt = total_pnl_usdt / total if total > 0 else 0

    # Average trade duration
    durations = [t.get("duration_seconds", 0) for t in trades if t.get("duration_seconds")]
    avg_duration = sum(durations) / len(durations) if durations else 0

    # Max drawdown (sequential PnL curve)
    cumulative = 0
    peak = 0
    max_drawdown_usdt = 0
    drawdown_trades = 0
    current_dd_streak = 0
    max_dd_streak = 0
    for pnl in pnl_list:
        cumulative += pnl
        if cumulative > peak:
            peak = cumulative
            current_dd_streak = 0
        dd = peak - cumulative
        if dd > max_drawdown_usdt:
            max_drawdown_usdt = dd
        if pnl < 0:
            current_dd_streak += 1
            max_dd_streak = max(max_dd_streak, current_dd_streak)
        else:
            current_dd_streak = 0

    # Direction breakdown
    longs = [t for t in trades if t.get("direction") == "LONG"]
    shorts = [t for t in trades if t.get("direction") == "SHORT"]
    long_pnl = sum(t.get("realized_pnl_usdt", 0) for t in longs)
    short_pnl = sum(t.get("realized_pnl_usdt", 0) for t in shorts)
    long_wins = len([t for t in longs if t.get("realized_pnl_usdt", 0) > 0])
    short_wins = len([t for t in shorts if t.get("realized_pnl_usdt", 0) > 0])

    # Exit reason breakdown
    exit_reasons = {}
    for t in trades:
        reason = t.get("exit_reason", "UNKNOWN")
        if reason not in exit_reasons:
            exit_reasons[reason] = {"count": 0, "pnl_usdt": 0}
        exit_reasons[reason]["count"] += 1
        exit_reasons[reason]["pnl_usdt"] += t.get("realized_pnl_usdt", 0)

    # Environment breakdown
    local_trades = [t for t in trades if t.get("execution_env") == "local"]
    gh_trades = [t for t in trades if t.get("execution_env") == "github_actions"]

    # Time range
    entry_times = [t.get("entry_time") for t in trades if t.get("entry_time")]
    first_trade = min(entry_times) if entry_times else None
    last_trade = max(entry_times) if entry_times else None

    return {
        "total_trades": total,
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "scratch_trades": len(scratches),
        "win_rate": win_rate,
        "total_pnl_usdt": total_pnl_usdt,
        "total_pnl_inr": total_pnl_inr,
        "total_fees_usdt": total_fees_usdt,
        "total_fees_inr": total_fees_inr,
        "best_trade_usdt": best_trade,
        "worst_trade_usdt": worst_trade,
        "profit_factor": profit_factor,
        "expectancy_usdt": expectancy_usdt,
        "avg_duration_seconds": avg_duration,
        "max_drawdown_usdt": max_drawdown_usdt,
        "max_loss_streak": max_dd_streak,
        "gross_profit_usdt": gross_profit,
        "gross_loss_usdt": gross_loss,
        # Direction
        "long_trades": len(longs),
        "short_trades": len(shorts),
        "long_pnl_usdt": long_pnl,
        "short_pnl_usdt": short_pnl,
        "long_win_rate": (long_wins / len(longs) * 100) if longs else 0,
        "short_win_rate": (short_wins / len(shorts) * 100) if shorts else 0,
        # Exit reasons
        "exit_reasons": exit_reasons,
        # Environment
        "local_trades": len(local_trades),
        "github_trades": len(gh_trades),
        "local_pnl_usdt": sum(t.get("realized_pnl_usdt", 0) for t in local_trades),
        "github_pnl_usdt": sum(t.get("realized_pnl_usdt", 0) for t in gh_trades),
        # Time range
        "first_trade_time": first_trade,
        "last_trade_time": last_trade,
    }


# =========================================================================
# DISPLAY FUNCTIONS
# =========================================================================

def display_full_summary(analytics: Dict[str, Any]):
    """Display comprehensive analytics summary."""
    print_header("📊 LIVE BOT PERFORMANCE SUMMARY")

    if analytics["total_trades"] == 0:
        print("\n  ⚠️  No trades found in MongoDB.\n")
        return

    a = analytics
    pnl_emoji = "🟢" if a["total_pnl_usdt"] >= 0 else "🔴"

    rows = [
        ("Total Trades",           f"{a['total_trades']}"),
        ("Wins / Losses / Scratch", f"{a['winning_trades']} / {a['losing_trades']} / {a['scratch_trades']}"),
        ("Win Rate",               fmt_pct(a["win_rate"], sign=False)),
        ("",                       ""),
        (f"{pnl_emoji} Net PnL",   fmt_dual(a["total_pnl_usdt"], a["total_pnl_inr"])),
        ("Gross Profit",           fmt_usdt(a["gross_profit_usdt"])),
        ("Gross Loss",             fmt_usdt(-a["gross_loss_usdt"])),
        ("Profit Factor",          f"{a['profit_factor']:.2f}" if a["profit_factor"] != float('inf') else "∞"),
        ("Expectancy / Trade",     fmt_usdt(a["expectancy_usdt"])),
        ("Total Fees",             fmt_dual(a["total_fees_usdt"], a["total_fees_inr"], sign=False)),
        ("",                       ""),
        ("Best Trade",             fmt_usdt(a["best_trade_usdt"])),
        ("Worst Trade",            fmt_usdt(a["worst_trade_usdt"])),
        ("Max Drawdown",           fmt_usdt(-a["max_drawdown_usdt"])),
        ("Max Losing Streak",      f"{a['max_loss_streak']} trades"),
        ("Avg Trade Duration",     f"{a['avg_duration_seconds']:.1f}s"),
        ("",                       ""),
        ("LONG Trades",            f"{a['long_trades']} | WR: {a['long_win_rate']:.1f}% | PnL: {fmt_usdt(a['long_pnl_usdt'])}"),
        ("SHORT Trades",           f"{a['short_trades']} | WR: {a['short_win_rate']:.1f}% | PnL: {fmt_usdt(a['short_pnl_usdt'])}"),
        ("",                       ""),
        ("Local Trades",           f"{a['local_trades']} | PnL: {fmt_usdt(a['local_pnl_usdt'])}"),
        ("GitHub Actions Trades",  f"{a['github_trades']} | PnL: {fmt_usdt(a['github_pnl_usdt'])}"),
    ]

    if a["first_trade_time"]:
        rows.append(("", ""))
        rows.append(("First Trade", fmt_time(a["first_trade_time"])))
        rows.append(("Last Trade",  fmt_time(a["last_trade_time"])))

    for label, value in rows:
        if not label and not value:
            print_separator("─")
        else:
            print(f"  {label:<25s} : {value}")
    print()

    # Exit Reason Breakdown
    if a["exit_reasons"]:
        print_header("📈 EXIT REASON BREAKDOWN")
        print(f"  {'Reason':<30s} {'Count':>6s} {'PnL (USDT)':>15s}")
        print_separator("─")
        for reason, data in sorted(a["exit_reasons"].items(), key=lambda x: -x[1]["count"]):
            pnl_str = fmt_usdt(data["pnl_usdt"])
            print(f"  {reason:<30s} {data['count']:>6d} {pnl_str:>15s}")
        print()


def display_trade_history(trades: List[Dict[str, Any]]):
    """Display detailed trade history table."""
    print_header(f"📋 TRADE HISTORY ({len(trades)} trades)")

    if not trades:
        print("\n  ⚠️  No trades found.\n")
        return

    print(f"  {'#':>4s} {'Time (IST)':<22s} {'Dir':<6s} {'Entry':>10s} {'Exit':>10s} {'PnL (USDT)':>14s} {'ROE%':>8s} {'Reason':<25s} {'Dur':>6s} {'Env':<5s}")
    print_separator("─")

    for t in trades:
        trade_id = t.get("trade_id", "?")
        entry_time = t.get("entry_time")
        time_str = fmt_time(entry_time) if entry_time else "N/A"
        direction = t.get("direction", "?")
        entry = t.get("entry_price", 0)
        exit_p = t.get("exit_price", 0)
        pnl = t.get("realized_pnl_usdt", 0)
        roe = t.get("roe_percentage", 0)
        reason = t.get("exit_reason", "UNKNOWN")
        duration = t.get("duration_seconds", 0)
        env = "GH" if t.get("execution_env") == "github_actions" else "LOC"

        pnl_sign = "+" if pnl > 0 else ""
        roe_sign = "+" if roe > 0 else ""
        dur_str = f"{duration:.1f}s"

        pnl_str = f"{pnl_sign}{pnl:.6f}"
        roe_str = f"{roe_sign}{roe:.1f}%"

        print(f"  {trade_id:>4} {time_str:<22s} {direction:<6s} {entry:>10.4f} {exit_p:>10.4f} {pnl_str:>14s} {roe_str:>8s} {reason:<25s} {dur_str:>6s} {env:<5s}")

    print()
    total_pnl = sum(t.get("realized_pnl_usdt", 0) for t in trades)
    pnl_sign = "+" if total_pnl > 0 else ""
    print(f"  {'Total':>4s} {'':<22s} {'':<6s} {'':>10s} {'':>10s} {pnl_sign + f'{total_pnl:.6f}':>14s}")
    print()


def display_cancelled_orders(orders: List[Dict[str, Any]]):
    """Display cancelled limit orders."""
    print_header(f"❌ CANCELLED ORDERS LOG ({len(orders)} orders)")

    if not orders:
        print("\n  ✅ No cancelled orders recorded.\n")
        return

    print(f"  {'Time (IST)':<22s} {'Symbol':<12s} {'Dir':<6s} {'Price':>10s} {'Timeout':>8s} {'Reason':<25s} {'Env':<5s}")
    print_separator("─")

    for o in orders:
        ts = o.get("timestamp")
        time_str = fmt_time(ts) if ts else "N/A"
        symbol = o.get("symbol", "?")
        direction = o.get("direction", "?")
        price = o.get("intended_entry_price", 0)
        timeout = o.get("timeout_seconds", 0)
        reason = o.get("cancel_reason", "UNKNOWN")
        env = "GH" if o.get("execution_env") == "github_actions" else "LOC"

        print(f"  {time_str:<22s} {symbol:<12s} {direction:<6s} {price:>10.4f} {timeout:>7.1f}s {reason:<25s} {env:<5s}")
    print()


def display_daily_breakdown(trades: List[Dict[str, Any]]):
    """Display daily PnL breakdown."""
    print_header("📅 DAILY PnL BREAKDOWN")

    if not trades:
        print("\n  ⚠️  No trades found.\n")
        return

    daily = {}
    for t in trades:
        entry_time = t.get("entry_time")
        if entry_time:
            if entry_time.tzinfo is None:
                entry_time = entry_time.replace(tzinfo=timezone.utc)
            ist_time = entry_time + timedelta(hours=5, minutes=30)
            day_key = ist_time.strftime("%Y-%m-%d")
        else:
            day_key = "Unknown"
        if day_key not in daily:
            daily[day_key] = {"trades": 0, "wins": 0, "pnl_usdt": 0, "pnl_inr": 0}
        daily[day_key]["trades"] += 1
        pnl = t.get("realized_pnl_usdt", 0)
        daily[day_key]["pnl_usdt"] += pnl
        daily[day_key]["pnl_inr"] += t.get("realized_pnl_inr", 0)
        if pnl > 0:
            daily[day_key]["wins"] += 1

    print(f"  {'Date':<12s} {'Trades':>7s} {'Wins':>5s} {'WR%':>6s} {'PnL (USDT)':>14s} {'PnL (INR)':>12s}")
    print_separator("─")

    for day in sorted(daily.keys()):
        d = daily[day]
        wr = (d["wins"] / d["trades"] * 100) if d["trades"] > 0 else 0
        pnl_sign = "+" if d["pnl_usdt"] > 0 else ""
        print(f"  {day:<12s} {d['trades']:>7d} {d['wins']:>5d} {wr:>5.1f}% {pnl_sign}{d['pnl_usdt']:>13.6f} {pnl_sign}₹{d['pnl_inr']:>10.4f}")
    print()


def display_live_balance():
    """Fetch and display current KCEX account balance."""
    print_header("💰 LIVE KCEX ACCOUNT BALANCE")

    try:
        from kcex.trade import KCEXTrader
        from kcex.market import KCEXMarket

        trader = KCEXTrader()
        market = KCEXMarket(trader.client)

        if not trader.client.config.is_authenticated:
            print("\n  ⚠️  KCEX_AUTH_TOKEN not configured in .env. Cannot fetch live balance.\n")
            return

        balances = trader.get_usdt_balance()
        inr_rate = market.get_inr_rate()

        avail_usdt = balances.get("available_usdt", 0.0)
        avail_inr = balances.get("available_inr", 0.0)
        equity_usdt = balances.get("equity_usdt", 0.0)
        equity_inr = balances.get("equity_inr", 0.0)
        unrealized = balances.get("unrealized_pnl_usdt", 0.0)
        unrealized_inr = balances.get("unrealized_pnl_inr", 0.0)

        print(f"  Available Balance : {avail_usdt:.4f} USDT (₹{avail_inr:.2f})")
        print(f"  Equity            : {equity_usdt:.4f} USDT (₹{equity_inr:.2f})")
        if abs(unrealized) > 1e-8:
            ur_sign = "+" if unrealized > 0 else ""
            print(f"  Unrealized PnL    : {ur_sign}{unrealized:.6f} USDT ({ur_sign}₹{unrealized_inr:.4f})")
        print(f"  USD/INR Rate      : ₹{inr_rate:.2f}")
        print()

        print("  ⚠️  Note: This balance includes both manual and bot trading activity.")
        print("       For bot-only PnL, refer to the MongoDB analytics above.\n")

    except Exception as e:
        print(f"\n  ❌ Error fetching KCEX balance: {e}\n")


def export_to_csv(trades: List[Dict[str, Any]], cancelled: List[Dict[str, Any]]):
    """Export trade data to CSV files."""
    print_header("📤 EXPORT TO CSV")

    # Export trades
    if trades:
        filename = "live_trades_export.csv"
        fields = [
            "trade_id", "entry_time", "exit_time", "symbol", "direction",
            "entry_price", "exit_price", "realized_pnl_usdt", "realized_pnl_inr",
            "roe_percentage", "pnl_percentage", "leverage", "vol_contracts",
            "margin_used_usdt", "fee_total_usdt", "exit_reason", "duration_seconds",
            "execution_env", "balance_before_trade_usdt", "balance_after_trade_usdt"
        ]
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(",".join(fields) + "\n")
                for t in trades:
                    row = []
                    for field in fields:
                        val = t.get(field, "")
                        if isinstance(val, datetime):
                            val = val.isoformat()
                        row.append(str(val) if val is not None else "")
                    f.write(",".join(row) + "\n")
            print(f"  ✅ Trades exported to: {os.path.abspath(filename)} ({len(trades)} records)")
        except Exception as e:
            print(f"  ❌ Failed to export trades: {e}")
    else:
        print("  ⚠️  No trades to export.")

    # Export cancelled orders
    if cancelled:
        filename = "cancelled_orders_export.csv"
        fields = [
            "timestamp", "symbol", "direction", "intended_entry_price",
            "timeout_seconds", "cancel_reason", "execution_env"
        ]
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(",".join(fields) + "\n")
                for o in cancelled:
                    row = []
                    for field in fields:
                        val = o.get(field, "")
                        if isinstance(val, datetime):
                            val = val.isoformat()
                        row.append(str(val) if val is not None else "")
                    f.write(",".join(row) + "\n")
            print(f"  ✅ Cancelled orders exported to: {os.path.abspath(filename)} ({len(cancelled)} records)")
        except Exception as e:
            print(f"  ❌ Failed to export cancelled orders: {e}")
    print()


# =========================================================================
# MAIN
# =========================================================================

def main():
    print(BANNER)

    # Connect to MongoDB
    print("\n  Connecting to MongoDB Atlas...")
    try:
        from kcex.engine.mongo_logger import MongoTradeLogger
        mongo = MongoTradeLogger()
        if not mongo.ping():
            print("  ❌ Failed to connect to MongoDB. Check MONGODB_URI in .env.")
            print("     Ensure pymongo and dnspython are installed: pip install pymongo dnspython\n")
            sys.exit(1)
    except ImportError:
        print("  ❌ pymongo not installed. Run: pip install pymongo dnspython")
        sys.exit(1)

    # Fetch data
    trades = mongo.get_all_trades(mode_filter="live")
    cancelled = mongo.get_all_cancelled_orders()
    trade_count = len(trades)
    cancel_count = len(cancelled)

    print(f"  ✅ Connected | {trade_count} executed trades | {cancel_count} cancelled orders\n")

    # Compute analytics
    analytics = compute_analytics(trades)

    while True:
        print_separator("═")
        print("  KCEX LIVE BOT ANALYTICS - MAIN MENU")
        print_separator("═")
        print()
        print("  [1] 📊 Full Summary Dashboard")
        print("  [2] 📋 Trade History (detailed table)")
        print("  [3] ❌ Cancelled Orders Log")
        print("  [4] 📅 Daily PnL Breakdown")
        print("  [5] 💰 Live KCEX Account Balance")
        print("  [6] 📤 Export to CSV")
        print("  [7] 🔄 Refresh Data from MongoDB")
        print("  [0] 🚪 Exit")
        print()

        try:
            choice = input("  Select option [0-7]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye! 👋\n")
            break

        if choice == "1":
            display_full_summary(analytics)
        elif choice == "2":
            display_trade_history(trades)
        elif choice == "3":
            display_cancelled_orders(cancelled)
        elif choice == "4":
            display_daily_breakdown(trades)
        elif choice == "5":
            display_live_balance()
        elif choice == "6":
            export_to_csv(trades, cancelled)
        elif choice == "7":
            print("\n  🔄 Refreshing data from MongoDB...")
            trades = mongo.get_all_trades(mode_filter="live")
            cancelled = mongo.get_all_cancelled_orders()
            analytics = compute_analytics(trades)
            print(f"  ✅ Refreshed | {len(trades)} executed trades | {len(cancelled)} cancelled orders\n")
        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option. Please enter 0-7.\n")

    mongo.close()


if __name__ == "__main__":
    main()
