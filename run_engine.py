"""
KCEX Automated Trade Execution Engine - "Masterplan" Runner
===========================================================
Interactive terminal CLI runner for the Masterplan Automated Trading Engine.

Features:
- Reads default settings from settings.py
- Interactive Terminal Setup (asks settings when run with no arguments)
- Full CLI flag support for scripting and automation
- Highly visible LIVE vs SIMULATED mode indicators
- Live wallet balance displayed at startup and after every trade cycle
"""

import sys
import os
import argparse

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load defaults from settings.py
try:
    import settings
except ImportError:
    settings = None

from kcex import (
    TradeExecutionEngine,
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    KCEXConfig,
    KCEXTrader,
    KCEXMarket
)


def print_banner(mode: EngineMode):
    banner_art = r"""
==============================================================================
  __  __         _____ _______ ______ _____  _____  _            _   _ 
 |  \/  |   /\  / ____|__   __|  ____|  __ \|  __ \| |   /\     | \ | |
 | \  / |  /  \| (___    | |  | |__  | |__) | |__) | |  /  \    |  \| |
 | |\/| | / /\ \\___ \   | |  |  __| |  _  /|  ___/| | / /\ \   | . ` |
 | |  | |/ ____ \___) |  | |  | |____| | \ \| |    | |/ ____ \  | |\  |
 |_|  |_/_/    \_\_____/  |_|  |______|_|  \_\_|    |_/_/    \_\_|_| \_|
                                                                        
       AUTOMATED TRADE EXECUTION ENGINE - KCEX ZERO-FEE FUTURES
=============================================================================="""
    print(banner_art)

    if mode == EngineMode.LIVE:
        print("""
##############################################################################
###                      🔴 LIVE REAL TRADING MODE                         ###
###     REAL CAPITAL AT RISK | REAL ORDERS SUBMITTING TO KCEX              ###
##############################################################################
""")
    else:
        print("""
******************************************************************************
***                  🟢 SIMULATED / DRY-RUN MODE                           ***
***    REAL-TIME LIVE MARKET PRICES | VIRTUAL ORDERS | ZERO RISK           ***
******************************************************************************
""")


def get_setting(name: str, fallback):
    if settings and hasattr(settings, name):
        return getattr(settings, name)
    return fallback


def prompt_user_settings():
    """
    Interactive prompt asking user for configuration when run without flags.
    Defaults to values from settings.py.
    """
    default_mode = get_setting("MODE", "live").lower()
    default_dir = get_setting("DIRECTION", "LONG").upper()
    default_sym = get_setting("SYMBOL", "TRUMP_USDT").upper()
    default_tp = get_setting("TP_TICKS", 1)
    default_sl = get_setting("SL_ROE_PCT", 10.0)
    default_lev = get_setting("LEVERAGE", 75)
    default_cool = get_setting("COOLDOWN_SECONDS", 30.0)
    default_max = get_setting("MAX_TRADES", 0)

    print("\n" + "=" * 78)
    print("           INTERACTIVE SETUP WIZARD (Press [Enter] to keep defaults)")
    print("=" * 78)

    # 1. Mode
    mode_str = input(f"1. Execution Mode ([1] LIVE Trading, [2] SIMULATED Dry-Run) [default: {'1 (LIVE)' if default_mode == 'live' else '2 (SIMULATED)'}]: ").strip()
    if mode_str == "2":
        mode_val = EngineMode.DRY_RUN
    elif mode_str == "1":
        mode_val = EngineMode.LIVE
    else:
        mode_val = EngineMode.LIVE if default_mode == "live" else EngineMode.DRY_RUN

    # 2. Direction
    dir_str = input(f"2. Order Direction ([1] LONG, [2] SHORT) [default: {'1 (LONG)' if default_dir == 'LONG' else '2 (SHORT)'}]: ").strip()
    if dir_str == "2" or dir_str.upper() == "SHORT":
        dir_val = OrderDirection.SHORT
    elif dir_str == "1" or dir_str.upper() == "LONG":
        dir_val = OrderDirection.LONG
    else:
        dir_val = OrderDirection.LONG if default_dir == "LONG" else OrderDirection.SHORT

    # 3. Trading Pair
    sym_str = input(f"3. Trading Pair [default: {default_sym}]: ").strip().upper()
    sym_val = sym_str if sym_str else default_sym

    # 4. Take-Profit rule (pu ticks)
    tp_str = input(f"4. Min-Profit TP distance in ticks (pu) [default: {default_tp} pu]: ").strip()
    try:
        tp_val = int(tp_str) if tp_str else default_tp
    except ValueError:
        tp_val = default_tp

    # 5. Stop Loss ROE %
    sl_str = input(f"5. Stop Loss -ROE % [default: {default_sl}%]: ").strip()
    try:
        sl_val = float(sl_str) if sl_str else default_sl
    except ValueError:
        sl_val = default_sl

    # 6. Leverage
    lev_str = input(f"6. Leverage multiplier [default: {default_lev}x]: ").strip()
    try:
        lev_val = int(lev_str) if lev_str else default_lev
    except ValueError:
        lev_val = default_lev

    # 7. Cooldown
    cool_str = input(f"7. Cooldown between trades in seconds [default: {default_cool:.0f}s]: ").strip()
    try:
        cool_val = float(cool_str) if cool_str else default_cool
    except ValueError:
        cool_val = default_cool

    # 8. Max trades
    max_str = input(f"8. Max trades to execute (0 = unlimited) [default: {default_max}]: ").strip()
    try:
        max_val = int(max_str) if max_str else default_max
    except ValueError:
        max_val = default_max

    print("=" * 78 + "\n")

    return ExecutionConfig(
        symbol=sym_val,
        direction=dir_val,
        mode=mode_val,
        leverage=lev_val,
        is_isolated=True,
        cooldown_seconds=cool_val,
        tp_ticks=tp_val,
        sl_roe_pct=sl_val,
        max_trades=max_val,
        poll_interval_seconds=get_setting("POLL_INTERVAL_SECONDS", 0.5),
        logs_dir=get_setting("LOGS_DIR", "logs"),
        realtime_log_file=get_setting("REALTIME_LOG_FILE", "engine_realtime.log"),
        outcomes_log_file=get_setting("OUTCOMES_LOG_FILE", "trade_outcomes.txt"),
        outcomes_jsonl_file=get_setting("OUTCOMES_JSONL_FILE", "trade_outcomes.jsonl")
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="KCEX Automated Trade Execution Engine - Masterplan Strategy"
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default=None,
        help="Trading pair symbol (default from settings.py: TRUMP_USDT)"
    )
    parser.add_argument(
        "--direction",
        type=str,
        choices=["LONG", "SHORT", "long", "short"],
        default=None,
        help="Order direction: LONG or SHORT (default from settings.py: LONG)"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["dry-run", "live"],
        default=None,
        help="Execution mode: 'dry-run' or 'live' (default from settings.py)"
    )
    parser.add_argument(
        "--cooldown",
        type=float,
        default=None,
        help="Cooldown in seconds between trades (default from settings.py: 30)"
    )
    parser.add_argument(
        "--max-trades",
        type=int,
        default=None,
        help="Maximum trades to execute (0 for unlimited, default: 0)"
    )
    parser.add_argument(
        "--tp-ticks",
        type=int,
        default=None,
        help="Take profit distance in price unit (pu) ticks (default: 1)"
    )
    parser.add_argument(
        "--sl-roe",
        type=float,
        default=None,
        help="Stop loss ROE percentage (default: 10.0)"
    )
    parser.add_argument(
        "--leverage",
        type=int,
        default=None,
        help="Position leverage (default: 75)"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=None,
        help="Live price polling interval in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Bypass interactive wizard and use default settings immediately"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine if we should prompt interactively:
    # If no flags passed on CLI and not explicitly flagged non-interactive
    is_interactive = (len(sys.argv) == 1) and not args.non_interactive

    if is_interactive:
        # Initial banner in neutral mode before wizard
        print_banner(EngineMode.LIVE if get_setting("MODE", "live") == "live" else EngineMode.DRY_RUN)
        config = prompt_user_settings()
    else:
        # Read from flags or fall back to settings.py
        sym = (args.symbol or get_setting("SYMBOL", "TRUMP_USDT")).upper()
        dir_raw = (args.direction or get_setting("DIRECTION", "LONG")).upper()
        mode_raw = (args.mode or get_setting("MODE", "live")).lower()

        dir_enum = OrderDirection.LONG if dir_raw == "LONG" else OrderDirection.SHORT
        mode_enum = EngineMode.LIVE if mode_raw == "live" else EngineMode.DRY_RUN

        tp_ticks = args.tp_ticks if args.tp_ticks is not None else get_setting("TP_TICKS", 1)
        sl_roe = args.sl_roe if args.sl_roe is not None else get_setting("SL_ROE_PCT", 10.0)
        lev = args.leverage if args.leverage is not None else get_setting("LEVERAGE", 75)
        cooldown = args.cooldown if args.cooldown is not None else get_setting("COOLDOWN_SECONDS", 30.0)
        max_trades = args.max_trades if args.max_trades is not None else get_setting("MAX_TRADES", 0)
        poll_int = args.poll_interval if args.poll_interval is not None else get_setting("POLL_INTERVAL_SECONDS", 0.5)

        config = ExecutionConfig(
            symbol=sym,
            direction=dir_enum,
            mode=mode_enum,
            leverage=lev,
            is_isolated=get_setting("IS_ISOLATED", True),
            cooldown_seconds=cooldown,
            tp_ticks=tp_ticks,
            sl_roe_pct=sl_roe,
            max_trades=max_trades,
            poll_interval_seconds=poll_int,
            logs_dir=get_setting("LOGS_DIR", "logs"),
            realtime_log_file=get_setting("REALTIME_LOG_FILE", "engine_realtime.log"),
            outcomes_log_file=get_setting("OUTCOMES_LOG_FILE", "trade_outcomes.txt"),
            outcomes_jsonl_file=get_setting("OUTCOMES_JSONL_FILE", "trade_outcomes.jsonl")
        )
        print_banner(config.mode)

    # Show live wallet balance at start
    cfg = KCEXConfig()
    if config.mode == EngineMode.LIVE and not cfg.is_authenticated:
        print("[ERROR] LIVE mode requires KCEX_AUTH_TOKEN in .env!")
        print("Please configure credentials or use SIMULATED / dry-run mode.")
        sys.exit(1)

    try:
        trader = KCEXTrader()
        market = KCEXMarket(trader.client)
        inr_rate = market.get_inr_rate()
        if cfg.is_authenticated:
            balances = trader.get_usdt_balance()
            avail_u = balances.get("available_usdt", 0.0)
            avail_i = balances.get("available_inr", 0.0)
            equity_u = balances.get("equity_usdt", 0.0)
            equity_i = balances.get("equity_inr", 0.0)
            print("------------------------------------------------------------------------------")
            print(f"CURRENT KCEX WALLET BALANCE:")
            print(f"Available : {avail_u:.4f} USDT (INR {avail_i:.2f})")
            print(f"Equity    : {equity_u:.4f} USDT (INR {equity_i:.2f})")
            print(f"USD/INR   : INR {inr_rate:.2f} per USD")
            print("------------------------------------------------------------------------------\n")
    except Exception as e:
        print(f"[Notice] Balance check skipped: {e}\n")

    engine = TradeExecutionEngine(config=config)
    engine.run()


if __name__ == "__main__":
    main()
