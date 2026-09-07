"""
KCEX Live Trading Analytics Dashboard
======================================
Interactive terminal script to view comprehensive analytics of all live bot
trades stored in MongoDB. Also displays live KCEX account balance.

Usage:
    python run_live_analytics.py

Features:
- Complete Trade Telemetry: Entry/Exit times, Margin used, Quantity, TP/SL set,
  Leverage, Sub-Strategy name, PnL (USDT & INR), ROE%, Wallet Balance before/after.
- Interactive Deep-Dive Trade Inspector for individual trade inspection.
- Strategy & Multi-Factor Performance Breakdown.
- Comprehensive CSV Export with all fields.
- Real-time KCEX Balance viewer.
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

def parse_dt(dt: Any) -> Optional[datetime]:
    """Parse a datetime object or ISO string."""
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt
    if isinstance(dt, str):
        try:
            return datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except Exception:
            return None
    return None

def fmt_time(dt: Any, short: bool = False) -> str:
    d = parse_dt(dt)
    if d is None:
        return "N/A"
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    ist = d + timedelta(hours=5, minutes=30)
    if short:
        return ist.strftime("%m-%d %H:%M:%S")
    return ist.strftime("%Y-%m-%d %H:%M:%S IST")

def fmt_duration(seconds: float) -> str:
    """Format duration into human readable string."""
    if seconds <= 0:
        return "0.0s"
    if seconds < 60:
        return f"{seconds:.1f}s"
    m = int(seconds // 60)
    s = seconds % 60
    return f"{seconds:.1f}s ({m}m {s:.0f}s)"


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


def print_separator(char: str = "─", width: int = 80):
    print(char * width)


def print_header(title: str, width: int = 80):
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
    total_volume_usdt = sum(t.get("notional_value_usdt", 0) for t in trades)
    total_volume_inr = sum(t.get("notional_value_inr", 0) for t in trades)
    total_margin_usdt = sum(t.get("margin_used_usdt", 0) for t in trades)
    total_margin_inr = sum(t.get("margin_used_inr", 0) for t in trades)

    pnl_list = [t.get("realized_pnl_usdt", 0) for t in trades]
    best_trade = max(pnl_list) if pnl_list else 0
    worst_trade = min(pnl_list) if pnl_list else 0

    # Win rate
    win_rate = (len(wins) / total * 100) if total > 0 else 0

    # Profit factor
    gross_profit = sum(t.get("realized_pnl_usdt", 0) for t in wins) if wins else 0
    gross_loss = abs(sum(t.get("realized_pnl_usdt", 0) for t in losses)) if losses else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf') if gross_profit > 0 else 0

    # Expectancy & Average Metrics
    expectancy_usdt = total_pnl_usdt / total if total > 0 else 0
    avg_margin_usdt = total_margin_usdt / total if total > 0 else 0
    avg_margin_inr = total_margin_inr / total if total > 0 else 0
    roes = [t.get("roe_percentage", 0) for t in trades]
    avg_roe = sum(roes) / len(roes) if roes else 0

    # Average trade duration
    durations = [t.get("duration_seconds", 0) for t in trades if t.get("duration_seconds")]
    avg_duration = sum(durations) / len(durations) if durations else 0

    # Max drawdown (sequential PnL curve)
    cumulative = 0
    peak = 0
    max_drawdown_usdt = 0
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

    # Strategy breakdown
    strategies = {}
    for t in trades:
        strat = t.get("sub_strategy_name") or "Standard"
        if strat not in strategies:
            strategies[strat] = {"count": 0, "wins": 0, "pnl_usdt": 0, "pnl_inr": 0}
        strategies[strat]["count"] += 1
        strategies[strat]["pnl_usdt"] += t.get("realized_pnl_usdt", 0)
        strategies[strat]["pnl_inr"] += t.get("realized_pnl_inr", 0)
        if t.get("realized_pnl_usdt", 0) > 0:
            strategies[strat]["wins"] += 1

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
    entry_times = [parse_dt(t.get("entry_time")) for t in trades if t.get("entry_time")]
    entry_times = [dt for dt in entry_times if dt is not None]
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
        "total_volume_usdt": total_volume_usdt,
        "total_volume_inr": total_volume_inr,
        "total_margin_usdt": total_margin_usdt,
        "total_margin_inr": total_margin_inr,
        "avg_margin_usdt": avg_margin_usdt,
        "avg_margin_inr": avg_margin_inr,
        "avg_roe": avg_roe,
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
        # Strategies
        "strategies": strategies,
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
        ("Avg Yield / ROE%",       fmt_pct(a["avg_roe"])),
        ("",                       ""),
        (f"{pnl_emoji} Net Realized PnL", fmt_dual(a["total_pnl_usdt"], a["total_pnl_inr"])),
        ("Gross Profit",           fmt_usdt(a["gross_profit_usdt"])),
        ("Gross Loss",             fmt_usdt(-a["gross_loss_usdt"])),
        ("Profit Factor",          f"{a['profit_factor']:.2f}" if a["profit_factor"] != float('inf') else "∞"),
        ("Expectancy / Trade",     fmt_usdt(a["expectancy_usdt"])),
        ("Total Fees Paid",        fmt_dual(a["total_fees_usdt"], a["total_fees_inr"], sign=False)),
        ("",                       ""),
        ("Total Volume Traded",    fmt_dual(a["total_volume_usdt"], a["total_volume_inr"], sign=False)),
        ("Total Margin Deployed",  fmt_dual(a["total_margin_usdt"], a["total_margin_inr"], sign=False)),
        ("Avg Margin / Trade",     fmt_dual(a["avg_margin_usdt"], a["avg_margin_inr"], sign=False)),
        ("",                       ""),
        ("Best Trade",             fmt_usdt(a["best_trade_usdt"])),
        ("Worst Trade",            fmt_usdt(a["worst_trade_usdt"])),
        ("Max Drawdown",           fmt_usdt(-a["max_drawdown_usdt"])),
        ("Max Losing Streak",      f"{a['max_loss_streak']} trades"),
        ("Avg Trade Duration",     fmt_duration(a["avg_duration_seconds"])),
        ("",                       ""),
        ("LONG Trades",            f"{a['long_trades']} | WR: {a['long_win_rate']:.1f}% | PnL: {fmt_usdt(a['long_pnl_usdt'])}"),
        ("SHORT Trades",           f"{a['short_trades']} | WR: {a['short_win_rate']:.1f}% | PnL: {fmt_usdt(a['short_pnl_usdt'])}"),
        ("",                       ""),
        ("Local Trades",           f"{a['local_trades']} | PnL: {fmt_usdt(a['local_pnl_usdt'])}"),
        ("GitHub Actions Trades",  f"{a['github_trades']} | PnL: {fmt_usdt(a['github_pnl_usdt'])}"),
    ]

    if a["first_trade_time"]:
        rows.append(("", ""))
        rows.append(("First Trade Time", fmt_time(a["first_trade_time"])))
        rows.append(("Last Trade Time",  fmt_time(a["last_trade_time"])))

    for label, value in rows:
        if not label and not value:
            print_separator("─")
        else:
            print(f"  {label:<25s} : {value}")
    print()

    # Strategy Breakdown
    if a.get("strategies"):
        print_header("🧠 STRATEGY PERFORMANCE BREAKDOWN")
        print(f"  {'Strategy':<35s} {'Trades':>7s} {'WR%':>7s} {'PnL (USDT)':>15s} {'PnL (INR)':>12s}")
        print_separator("─")
        for strat, data in sorted(a["strategies"].items(), key=lambda x: -x[1]["pnl_usdt"]):
            wr = (data["wins"] / data["count"] * 100) if data["count"] > 0 else 0
            pnl_s = fmt_usdt(data["pnl_usdt"])
            pnl_i = fmt_inr(data["pnl_inr"])
            print(f"  {strat:<35s} {data['count']:>7d} {wr:>6.1f}% {pnl_s:>15s} {pnl_i:>12s}")
        print()

    # Exit Reason Breakdown
    if a.get("exit_reasons"):
        print_header("📈 EXIT REASON BREAKDOWN")
        print(f"  {'Reason':<30s} {'Count':>6s} {'PnL (USDT)':>15s}")
        print_separator("─")
        for reason, data in sorted(a["exit_reasons"].items(), key=lambda x: -x[1]["count"]):
            pnl_str = fmt_usdt(data["pnl_usdt"])
            print(f"  {reason:<30s} {data['count']:>6d} {pnl_str:>15s}")
        print()


def display_trade_history(trades: List[Dict[str, Any]]):
    """Display rich trade history table with all key telemetry."""
    print_header(f"📋 TRADE HISTORY ({len(trades)} trades)")

    if not trades:
        print("\n  ⚠️  No trades found.\n")
        return

    print("\n  Format: Entry & Exit times (IST), Sizing, Margin, TP/SL, PnL, ROE% & Strategy")
    print_separator("═", width=110)

    for i, t in enumerate(trades, 1):
        trade_id = t.get("trade_id", i)
        symbol = t.get("symbol", "?")
        direction = t.get("direction", "?")
        leverage = t.get("leverage", "?")
        vol = t.get("vol_contracts", 0)
        qty = t.get("underlying_quantity", 0)
        base_coin = t.get("base_coin", "")
        
        entry_time_str = fmt_time(t.get("entry_time"))
        exit_time_str = fmt_time(t.get("exit_time"))
        duration_str = fmt_duration(t.get("duration_seconds", 0))

        entry_p = t.get("entry_price", 0)
        exit_p = t.get("exit_price", 0)
        tp_set = t.get("tp_set", 0)
        sl_set = t.get("sl_set", 0)

        margin_u = t.get("margin_used_usdt", 0)
        margin_i = t.get("margin_used_inr", 0)
        pnl_u = t.get("realized_pnl_usdt", 0)
        pnl_i = t.get("realized_pnl_inr", 0)
        roe = t.get("roe_percentage", 0)

        strategy = t.get("sub_strategy_name") or "Standard"
        reason = t.get("exit_reason", "UNKNOWN")
        env = "GH Actions" if t.get("execution_env") == "github_actions" else "Local PC"
        verified = "✅ Verified" if t.get("verified_from_kcex") else "⚠️ Unverified"

        pnl_sign = "+" if pnl_u > 0 else ""
        roe_sign = "+" if roe > 0 else ""
        dir_emoji = "🟢 LONG" if direction == "LONG" else "🔴 SHORT"

        print(f"  ─── Trade #{trade_id} │ {symbol} │ {dir_emoji} │ {leverage}x Lev │ {env} │ {verified} ───")
        print(f"    • Entry Time : {entry_time_str:<26s} │ Entry Price : {entry_p:.4f} USDT")
        print(f"    • Exit Time  : {exit_time_str:<26s} │ Exit Price  : {exit_p:.4f} USDT  (Duration: {duration_str})")
        print(f"    • Target TP  : {tp_set:.4f} USDT {'🎯 (Hit!)' if reason == 'MIN_PROFIT_TP_HIT' else ''} │ Stop Loss SL: {sl_set:.4f} USDT")
        print(f"    • Sizing     : {vol} contracts ({qty:.4f} {base_coin}) │ Margin Used : {margin_u:.6f} USDT (₹{margin_i:.4f})")
        print(f"    • Outcome    : {pnl_sign}{pnl_u:.6f} USDT ({pnl_sign}₹{pnl_i:.4f}) │ ROE/Yield   : {roe_sign}{roe:.2f}%")
        print(f"    • Strategy   : {strategy:<32s} │ Exit Reason : {reason}")
        print_separator("─", width=110)

    total_pnl_u = sum(t.get("realized_pnl_usdt", 0) for t in trades)
    total_pnl_i = sum(t.get("realized_pnl_inr", 0) for t in trades)
    total_margin = sum(t.get("margin_used_usdt", 0) for t in trades)
    pnl_sign = "+" if total_pnl_u > 0 else ""

    print(f"  TOTAL NET PnL: {pnl_sign}{total_pnl_u:.6f} USDT ({pnl_sign}₹{total_pnl_i:.4f}) │ Total Margin Deployed: {total_margin:.6f} USDT")
    print_separator("═", width=110)
    print()


def display_single_trade_card(trade: Dict[str, Any]):
    """Display comprehensive deep-dive card for a single trade."""
    trade_id = trade.get("trade_id", "?")
    symbol = trade.get("symbol", "?")
    direction = trade.get("direction", "?")
    base_coin = trade.get("base_coin", "")
    sub_strategy = trade.get("sub_strategy_name") or "Standard"
    verified = "✅ Verified on KCEX Account" if trade.get("verified_from_kcex") else "⚠️ Simulated / Unverified"
    order_id = trade.get("order_id", "N/A")
    close_order_id = trade.get("close_order_id", "N/A")
    position_id = trade.get("position_id", "N/A")

    entry_time_str = fmt_time(trade.get("entry_time"))
    exit_time_str = fmt_time(trade.get("exit_time"))
    duration_str = fmt_duration(trade.get("duration_seconds", 0))

    leverage = trade.get("leverage", 1)
    vol = trade.get("vol_contracts", 0)
    contract_size = trade.get("contract_size", 0)
    qty = trade.get("underlying_quantity", 0)
    notional_u = trade.get("notional_value_usdt", 0)
    notional_i = trade.get("notional_value_inr", 0)
    margin_u = trade.get("margin_used_usdt", 0)
    margin_i = trade.get("margin_used_inr", 0)

    entry_p = trade.get("entry_price", 0)
    exit_p = trade.get("exit_price", 0)
    tp_set = trade.get("tp_set", 0)
    sl_set = trade.get("sl_set", 0)
    precision = trade.get("price_precision", 4)

    pnl_u = trade.get("realized_pnl_usdt", 0)
    pnl_i = trade.get("realized_pnl_inr", 0)
    roe = trade.get("roe_percentage", 0)
    pnl_pct = trade.get("pnl_percentage", 0)
    fees_u = trade.get("fee_total_usdt", 0)
    fees_i = trade.get("fee_total_inr", 0)
    reason = trade.get("exit_reason", "UNKNOWN")

    bal_before_u = trade.get("balance_before_trade_usdt")
    bal_before_i = trade.get("balance_before_trade_inr")
    bal_after_u = trade.get("balance_after_trade_usdt")
    bal_after_i = trade.get("balance_after_trade_inr")

    env = trade.get("execution_env", "local")
    gh_run_id = trade.get("github_run_id", "")
    gh_run_num = trade.get("github_run_number", "")
    session_id = trade.get("session_id", "N/A")
    config_snap = trade.get("config_snapshot", {})

    dir_emoji = "🟢 LONG" if direction == "LONG" else "🔴 SHORT"
    pnl_sign = "+" if pnl_u > 0 else ""
    roe_sign = "+" if roe > 0 else ""

    print_header(f"🔍 DETAILED TRADE CARD: #{trade_id} ({symbol} - {direction})", width=84)

    print("  📋 IDENTIFICATION & EXECUTION")
    print(f"    • Trade ID             : #{trade_id}")
    print(f"    • Symbol / Coin        : {symbol} ({base_coin})")
    print(f"    • Direction            : {dir_emoji}")
    print(f"    • Sub-Strategy         : {sub_strategy}")
    print(f"    • KCEX Verification    : {verified}")
    print(f"    • Order IDs            : Open: {order_id} │ Close: {close_order_id}")
    print(f"    • Position ID          : {position_id}")
    print(f"    • Execution Env        : {env.upper()}" + (f" (Run ID: {gh_run_id}, #{gh_run_num})" if gh_run_id else ""))
    print(f"    • Session ID           : {session_id}")
    print()

    print("  ⏰ TIMING & DURATION")
    print(f"    • Entry Time (IST)     : {entry_time_str}")
    print(f"    • Exit Time (IST)      : {exit_time_str}")
    print(f"    • Hold Duration        : {duration_str}")
    print()

    print("  📐 SIZING & LEVERAGE")
    print(f"    • Leverage             : {leverage}x Isolated")
    print(f"    • Volume (Contracts)   : {vol} contracts (Size: {contract_size})")
    print(f"    • Underlying Quantity  : {qty:.4f} {base_coin}")
    print(f"    • Notional Value       : {fmt_dual(notional_u, notional_i, sign=False)}")
    print(f"    • Margin Used          : {fmt_dual(margin_u, margin_i, sign=False)}")
    print()

    print("  🎯 PRICE TARGETS & EXECUTION")
    print(f"    • Entry Price          : {entry_p:.{precision}f} USDT")
    print(f"    • Exit Price           : {exit_p:.{precision}f} USDT")
    print(f"    • Take-Profit (TP) Set : {tp_set:.{precision}f} USDT" + (" 🎯 (Target Reached!)" if reason == "MIN_PROFIT_TP_HIT" else ""))
    print(f"    • Stop-Loss (SL) Set   : {sl_set:.{precision}f} USDT")
    print(f"    • Exit Reason          : {reason}")
    print()

    print("  💰 PnL, YIELD & FEES")
    print(f"    • Realized Net PnL     : {fmt_dual(pnl_u, pnl_i)}")
    print(f"    • Yield / ROE%         : {roe_sign}{roe:.2f}%")
    print(f"    • Price Move PnL%      : {pnl_sign}{pnl_pct:.4f}%")
    print(f"    • Trading Fees Paid    : {fmt_dual(fees_u, fees_i, sign=False)}")
    print()

    if bal_before_u is not None and bal_after_u is not None:
        bal_diff = bal_after_u - bal_before_u
        diff_pct = (bal_diff / bal_before_u * 100) if bal_before_u > 0 else 0
        diff_sign = "+" if bal_diff > 0 else ""
        print("  💼 WALLET BALANCE IMPACT")
        print(f"    • Balance Before Trade : {bal_before_u:.6f} USDT (₹{bal_before_i:.4f})")
        print(f"    • Balance After Trade  : {bal_after_u:.6f} USDT (₹{bal_after_i:.4f})")
        print(f"    • Net Wallet Change    : {diff_sign}{bal_diff:.6f} USDT ({diff_sign}{diff_pct:.2f}%)")
        print()

    if config_snap:
        print("  ⚙️ STRATEGY CONFIG SNAPSHOT")
        strat_mode = config_snap.get("strategy_mode", "N/A")
        exec_style = config_snap.get("execution_style", "N/A")
        stoch_preset = config_snap.get("stoch_preset", "N/A")
        ema_preset = config_snap.get("ema_preset", "N/A")
        tp_ticks = config_snap.get("tp_ticks", "N/A")
        sl_mode = config_snap.get("sl_mode", "N/A")
        sl_ticks = config_snap.get("sl_ticks", "N/A")
        atr_filter = config_snap.get("smart_atr_filter_enabled", False)
        min_atr = config_snap.get("smart_min_atr_ticks", "N/A")
        chop_ceil = config_snap.get("smart_chop_ceiling", "N/A")

        print(f"    • Strategy Mode        : {strat_mode} (Preset: {stoch_preset or ema_preset})")
        print(f"    • Execution Style      : {exec_style}")
        print(f"    • Take-Profit / SL     : TP: {tp_ticks} ticks │ SL Mode: {sl_mode} ({sl_ticks} ticks)")
        print(f"    • Smart ATR Filter     : {'Enabled' if atr_filter else 'Disabled'} (Min ATR: {min_atr} ticks, Chop ceiling: {chop_ceil})")
        print()

    print_separator("═", width=84)
    print()


def display_strategy_breakdown(trades: List[Dict[str, Any]]):
    """Display deep strategy and multi-factor performance breakdown."""
    print_header("🧠 STRATEGY & MULTI-FACTOR BREAKDOWN")

    if not trades:
        print("\n  ⚠️  No trades found.\n")
        return

    # Group by Sub-Strategy
    by_strat = {}
    by_dir = {}
    by_coin = {}
    by_reason = {}

    for t in trades:
        s = t.get("sub_strategy_name") or "Standard"
        d = t.get("direction", "OTHER")
        c = t.get("symbol", "OTHER")
        r = t.get("exit_reason", "UNKNOWN")
        pnl = t.get("realized_pnl_usdt", 0)
        pnl_inr = t.get("realized_pnl_inr", 0)
        vol = t.get("notional_value_usdt", 0)
        margin = t.get("margin_used_usdt", 0)

        for group_dict, key in [(by_strat, s), (by_dir, d), (by_coin, c), (by_reason, r)]:
            if key not in group_dict:
                group_dict[key] = {"trades": 0, "wins": 0, "pnl_usdt": 0.0, "pnl_inr": 0.0, "volume": 0.0, "margin": 0.0}
            group_dict[key]["trades"] += 1
            group_dict[key]["pnl_usdt"] += pnl
            group_dict[key]["pnl_inr"] += pnl_inr
            group_dict[key]["volume"] += vol
            group_dict[key]["margin"] += margin
            if pnl > 0:
                group_dict[key]["wins"] += 1

    # 1. By Sub-Strategy
    print("\n  ▶ 1. Performance by Sub-Strategy:")
    print(f"    {'Sub-Strategy':<35s} {'Trades':>6s} {'Wins':>5s} {'WR%':>6s} {'Net PnL (USDT)':>16s} {'Net PnL (INR)':>14s}")
    print_separator("─", width=90)
    for k, v in sorted(by_strat.items(), key=lambda x: -x[1]["pnl_usdt"]):
        wr = (v["wins"] / v["trades"] * 100) if v["trades"] > 0 else 0
        pnl_s = fmt_usdt(v["pnl_usdt"])
        pnl_i = fmt_inr(v["pnl_inr"])
        print(f"    {k:<35s} {v['trades']:>6d} {v['wins']:>5d} {wr:>5.1f}% {pnl_s:>16s} {pnl_i:>14s}")

    # 2. By Direction
    print("\n  ▶ 2. Performance by Direction (LONG vs SHORT):")
    print(f"    {'Direction':<15s} {'Trades':>6s} {'Wins':>5s} {'WR%':>6s} {'Net PnL (USDT)':>16s} {'Net PnL (INR)':>14s}")
    print_separator("─", width=90)
    for k, v in sorted(by_dir.items(), key=lambda x: -x[1]["pnl_usdt"]):
        wr = (v["wins"] / v["trades"] * 100) if v["trades"] > 0 else 0
        pnl_s = fmt_usdt(v["pnl_usdt"])
        pnl_i = fmt_inr(v["pnl_inr"])
        print(f"    {k:<15s} {v['trades']:>6d} {v['wins']:>5d} {wr:>5.1f}% {pnl_s:>16s} {pnl_i:>14s}")

    # 3. By Exit Reason
    print("\n  ▶ 3. Performance by Exit Reason:")
    print(f"    {'Exit Reason':<30s} {'Trades':>6s} {'Wins':>5s} {'WR%':>6s} {'Net PnL (USDT)':>16s}")
    print_separator("─", width=90)
    for k, v in sorted(by_reason.items(), key=lambda x: -x[1]["pnl_usdt"]):
        wr = (v["wins"] / v["trades"] * 100) if v["trades"] > 0 else 0
        pnl_s = fmt_usdt(v["pnl_usdt"])
        print(f"    {k:<30s} {v['trades']:>6d} {v['wins']:>5d} {wr:>5.1f}% {pnl_s:>16s}")
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
        entry_time = parse_dt(t.get("entry_time"))
        if entry_time:
            if entry_time.tzinfo is None:
                entry_time = entry_time.replace(tzinfo=timezone.utc)
            ist_time = entry_time + timedelta(hours=5, minutes=30)
            day_key = ist_time.strftime("%Y-%m-%d")
        else:
            day_key = "Unknown"
        if day_key not in daily:
            daily[day_key] = {"trades": 0, "wins": 0, "pnl_usdt": 0, "pnl_inr": 0, "volume": 0, "margin": 0}
        daily[day_key]["trades"] += 1
        pnl = t.get("realized_pnl_usdt", 0)
        daily[day_key]["pnl_usdt"] += pnl
        daily[day_key]["pnl_inr"] += t.get("realized_pnl_inr", 0)
        daily[day_key]["volume"] += t.get("notional_value_usdt", 0)
        daily[day_key]["margin"] += t.get("margin_used_usdt", 0)
        if pnl > 0:
            daily[day_key]["wins"] += 1

    print(f"  {'Date':<12s} {'Trades':>7s} {'Wins':>5s} {'WR%':>6s} {'PnL (USDT)':>14s} {'PnL (INR)':>12s} {'Volume ($)':>12s}")
    print_separator("─", width=80)

    for day in sorted(daily.keys()):
        d = daily[day]
        wr = (d["wins"] / d["trades"] * 100) if d["trades"] > 0 else 0
        pnl_sign = "+" if d["pnl_usdt"] > 0 else ""
        print(f"  {day:<12s} {d['trades']:>7d} {d['wins']:>5d} {wr:>5.1f}% {pnl_sign}{d['pnl_usdt']:>13.6f} {pnl_sign}₹{d['pnl_inr']:>10.4f} {d['volume']:>11.4f}")
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
    """Export trade data to CSV files with all 25+ telemetry fields."""
    print_header("📤 EXPORT TO CSV")

    # Export trades
    if trades:
        filename = "live_trades_export.csv"
        fields = [
            "trade_id", "entry_time", "exit_time", "duration_seconds", "symbol", "base_coin",
            "direction", "sub_strategy_name", "leverage", "vol_contracts", "contract_size",
            "underlying_quantity", "entry_price", "exit_price", "tp_set", "sl_set",
            "notional_value_usdt", "notional_value_inr", "margin_used_usdt", "margin_used_inr",
            "realized_pnl_usdt", "realized_pnl_inr", "roe_percentage", "pnl_percentage",
            "fee_total_usdt", "fee_total_inr", "exit_reason", "balance_before_trade_usdt",
            "balance_after_trade_usdt", "order_id", "close_order_id", "position_id",
            "execution_env", "session_id", "github_run_id"
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
            "timeout_seconds", "cancel_reason", "execution_env", "session_id"
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
        print("  [1] 📊 Full Summary Dashboard (with Strategy & Margin stats)")
        print("  [2] 📋 Trade History Table (all trade cards & telemetry)")
        print("  [3] 🔍 Deep-Dive Single Trade Inspector (view full trade details)")
        print("  [4] 🧠 Strategy & Multi-Factor Performance Breakdown")
        print("  [5] ❌ Cancelled Orders Log")
        print("  [6] 📅 Daily PnL Breakdown")
        print("  [7] 💰 Live KCEX Account Balance")
        print("  [8] 📤 Export to CSV (all 25+ fields)")
        print("  [9] 🔄 Refresh Data from MongoDB")
        print("  [0] 🚪 Exit")
        print()

        try:
            choice = input("  Select option [0-9]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye! 👋\n")
            break

        if choice == "1":
            display_full_summary(analytics)
        elif choice == "2":
            display_trade_history(trades)
        elif choice == "3":
            if not trades:
                print("\n  ⚠️  No trades available to inspect.\n")
            else:
                try:
                    inp = input(f"  Enter Trade ID or index (1 to {len(trades)}): ").strip()
                    if inp:
                        target = None
                        for t in trades:
                            if str(t.get("trade_id")) == inp:
                                target = t
                                break
                        if not target:
                            try:
                                idx = int(inp) - 1
                                if 0 <= idx < len(trades):
                                    target = trades[idx]
                            except ValueError:
                                pass
                        if target:
                            display_single_trade_card(target)
                        else:
                            print(f"\n  ⚠️  Trade '{inp}' not found.\n")
                except (KeyboardInterrupt, EOFError):
                    print()
        elif choice == "4":
            display_strategy_breakdown(trades)
        elif choice == "5":
            display_cancelled_orders(cancelled)
        elif choice == "6":
            display_daily_breakdown(trades)
        elif choice == "7":
            display_live_balance()
        elif choice == "8":
            export_to_csv(trades, cancelled)
        elif choice == "9":
            print("\n  🔄 Refreshing data from MongoDB...")
            trades = mongo.get_all_trades(mode_filter="live")
            cancelled = mongo.get_all_cancelled_orders()
            analytics = compute_analytics(trades)
            print(f"  ✅ Refreshed | {len(trades)} executed trades | {len(cancelled)} cancelled orders\n")
        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option. Please enter 0-9.\n")

    mongo.close()


if __name__ == "__main__":
    main()
