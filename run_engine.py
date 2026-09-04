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
                                                                        
       AUTOMATED TRADE EXECUTION ENGINE - KCEX FUTURES
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
    default_tp = get_setting("TP_TICKS", 2)
    default_vol_mode = get_setting("VOLUME_MODE", "MULTIPLIER").upper()
    default_vol_mult = get_setting("VOLUME_MULTIPLIER", 1.0)
    default_vol_contracts = get_setting("VOLUME_CONTRACTS", 1)
    default_sl_mode = get_setting("SL_MODE", "TICKS").upper()
    default_sl_ticks = get_setting("SL_TICKS", 10)
    default_sl_roe = get_setting("SL_ROE_PCT", 25.0)
    default_sl_price = get_setting("SL_PRICE_PCT", 0.5)
    default_lev = get_setting("LEVERAGE", 30)
    default_cool = get_setting("COOLDOWN_SECONDS", 30.0)
    default_max = get_setting("MAX_TRADES", 3)

    print("\n" + "=" * 78)
    print("           INTERACTIVE SETUP WIZARD (Press [Enter] to keep defaults)")
    print("=" * 78)
    print("💡 Tip: Press [Enter] on any prompt to accept the default from settings.py.\n")

    # 1. Mode
    print("1. Execution Mode:")
    print("   [1] LIVE TRADING    -> Real orders submitted to KCEX using wallet balance.")
    print("   [2] SIMULATED (Dry) -> Virtual orders with real-time live ticker data (0 risk).")
    mode_str = input(f"   Select Mode [default: {'1 (LIVE)' if default_mode == 'live' else '2 (SIMULATED)'}]: ").strip()
    if mode_str == "2":
        mode_val = EngineMode.DRY_RUN
    elif mode_str == "1":
        mode_val = EngineMode.LIVE
    else:
        mode_val = EngineMode.LIVE if default_mode == "live" else EngineMode.DRY_RUN

    # 2. Direction
    print("\n2. Order Direction:")
    print("   [1] LONG  -> Profit when price rises.")
    print("   [2] SHORT -> Profit when price drops.")
    dir_str = input(f"   Select Direction [default: {'1 (LONG)' if default_dir == 'LONG' else '2 (SHORT)'}]: ").strip()
    if dir_str == "2" or dir_str.upper() == "SHORT":
        dir_val = OrderDirection.SHORT
    elif dir_str == "1" or dir_str.upper() == "LONG":
        dir_val = OrderDirection.LONG
    else:
        dir_val = OrderDirection.LONG if default_dir == "LONG" else OrderDirection.SHORT

    # 3. Trading Pair
    print("\n3. Trading Pair:")
    print("   Enter any KCEX futures pair (e.g. TRUMP_USDT, DOGE_USDT, BTC_USDT, ETH_USDT, SOL_USDT, etc.)")
    print("   Note: Pairs like TRUMP_USDT and DOGE_USDT enjoy 0% maker and 0% taker fees on KCEX.")
    sym_str = input(f"   Symbol [default: {default_sym}]: ").strip().upper()
    sym_val = sym_str if sym_str else default_sym

    # Attempt to dynamically inspect chosen pair
    contract = None
    last_snap_price = 0.0
    pu_val = 0.001
    ps_val = 4
    try:
        market_obj = KCEXMarket()
        contract = market_obj.get_contract_detail(sym_val)
        pu_val = contract.price_unit
        ps_val = contract.price_precision
        ticker_snap = market_obj.get_ticker(sym_val)
        last_snap_price = float(ticker_snap.get("lastPrice", 0.0) or ticker_snap.get("fairPrice", 1.0))
        fee_label = "0% (Zero-Fee Pair)" if (contract.maker_fee_rate == 0 and contract.taker_fee_rate == 0) else f"Maker {contract.maker_fee_rate*100:.2f}%, Taker {contract.taker_fee_rate*100:.2f}%"
        print(f"   ✅ Contract Verified: {contract.symbol} | Price: {last_snap_price:.{ps_val}f} USDT")
        print(f"      Tick Size (pu): {contract.price_unit} | Contract Size (cs): {contract.contract_size} {contract.base_coin} | Max Lev: {contract.max_leverage}x | Fees: {fee_label}")
    except Exception as e:
        print(f"   ℹ️  Note: Market preview skipped for {sym_val} ({e}).")

    # 4. Trade Quantity / Volume
    if default_vol_mode == "CONTRACTS":
        default_vol_hint = f"{default_vol_contracts} contract(s)"
    elif default_vol_mode == "MULTIPLIER":
        default_vol_hint = f"{default_vol_mult:g}x min quantity"
    else:
        default_vol_hint = "1x min quantity"

    print("\n4. Trade Quantity / Volume (Position Sizing):")
    print("   ⚠️ CRITICAL NOTE: Trade Quantity (Volume) is NOT the same as Margin!")
    print("      • Trade Quantity = Contracts * Contract Size * Price (total market exposure)")
    print("      • Margin Deducted = Trade Quantity / Leverage (actual cash deducted from wallet)")
    if contract and last_snap_price > 0:
        cs = contract.contract_size
        bcoin = contract.base_coin
        min_v = int(contract.min_volume)
        lev = min(default_lev, contract.max_leverage)
        min_notional = min_v * cs * last_snap_price
        min_margin = min_notional / lev
        print(f"      Example for {contract.symbol} (at {lev}x lev): {min_v} contract(s) ({min_v * cs:g} {bcoin}) = ~{min_notional:.4f} USDT exposure (~{min_margin:.4f} USDT margin)")
    else:
        print("      Example: 1 contract = (1 * contract_size * price) USDT exposure, margin = exposure / leverage")
    print("   Input Options:")
    print("      - Multiplier of min: Enter '1x', '2x', '5x' (times the minimum contract quantity)")
    print("      - Exact contracts  : Enter integer like '1', '2', '5' (absolute contracts)")
    vol_str = input(f"   Trade Quantity [default: {default_vol_hint}]: ").strip()

    vol_mode_val = default_vol_mode
    vol_mult_val = default_vol_mult if default_vol_mode == "MULTIPLIER" else 1.0
    vol_contracts_val = default_vol_contracts if default_vol_mode == "CONTRACTS" else None

    if vol_str:
        s_clean = vol_str.lower().strip()
        if "x" in s_clean:
            vol_mode_val = "MULTIPLIER"
            try:
                vol_mult_val = float(s_clean.replace("x", "").strip())
            except ValueError:
                vol_mult_val = default_vol_mult
            vol_contracts_val = None
        else:
            try:
                num = float(s_clean)
                if num.is_integer() and int(num) >= 1:
                    vol_mode_val = "CONTRACTS"
                    vol_contracts_val = int(num)
                    vol_mult_val = None
                else:
                    vol_mode_val = "MULTIPLIER"
                    vol_mult_val = num
                    vol_contracts_val = None
            except ValueError:
                pass

    # 5. Take-Profit rule (pu ticks)
    print("\n5. Guaranteed Min-Profit Take-Profit (TP):")
    print(f"   Distance in price units (pu). For {sym_val}, 1 pu = {pu_val:.{ps_val}f} USDT.")
    print(f"   {default_tp} pu = +{default_tp * pu_val:.{ps_val}f} USDT target offset.")
    tp_str = input(f"   TP Ticks [default: {default_tp} pu]: ").strip()
    try:
        tp_val = int(tp_str) if tp_str else default_tp
    except ValueError:
        tp_val = default_tp

    # 6. Stop Loss
    if default_sl_mode == "TICKS" and default_sl_ticks:
        default_sl_hint = f"{default_sl_ticks} ticks ({default_sl_ticks * pu_val:.{ps_val}f} USDT)"
    elif default_sl_mode == "PRICE_PCT" and default_sl_price:
        default_sl_hint = f"{default_sl_price}% price"
    else:
        default_sl_hint = f"{default_sl_roe}% ROE"

    print("\n6. Stop Loss (SL) Configuration:")
    print("   Format options:")
    print(f"     - By Ticks : Enter '10' or '10t' (e.g. 10 ticks = {10 * pu_val:.{ps_val}f} USDT) [Recommended]")
    print("     - By ROE % : Enter '25%' or '50roe' (percentage loss on margin)")
    print("     - By Price%: Enter '0.5p' or '0.5%' (percentage move of coin price)")
    sl_str = input(f"   Stop Loss [default: {default_sl_hint}]: ").strip()
    
    sl_mode_val = default_sl_mode
    sl_ticks_val = default_sl_ticks if default_sl_mode == "TICKS" else None
    sl_roe_val = default_sl_roe if default_sl_mode == "ROE" else 25.0
    sl_price_val = default_sl_price if default_sl_mode == "PRICE_PCT" else None

    if sl_str:
        s_clean = sl_str.lower().strip()
        if "%" in s_clean or "roe" in s_clean:
            sl_mode_val = "ROE"
            try:
                sl_roe_val = float(s_clean.replace("%", "").replace("roe", "").strip())
            except ValueError:
                sl_roe_val = default_sl_roe
            sl_ticks_val = None
            sl_price_val = None
        elif "p" in s_clean or "price" in s_clean:
            sl_mode_val = "PRICE_PCT"
            try:
                sl_price_val = float(s_clean.replace("p", "").replace("price", "").strip())
            except ValueError:
                sl_price_val = default_sl_price
            sl_ticks_val = None
            sl_roe_val = None
        elif "t" in s_clean or "tick" in s_clean:
            sl_mode_val = "TICKS"
            try:
                sl_ticks_val = int(s_clean.replace("ticks", "").replace("tick", "").replace("t", "").strip())
            except ValueError:
                sl_ticks_val = default_sl_ticks
            sl_roe_val = None
            sl_price_val = None
        else:
            try:
                num = float(s_clean)
                if num >= 1.0 and num.is_integer():
                    # Integer >= 1: treat as ticks
                    sl_mode_val = "TICKS"
                    sl_ticks_val = int(num)
                    sl_roe_val = None
                    sl_price_val = None
                else:
                    sl_mode_val = "PRICE_PCT"
                    sl_price_val = num
                    sl_ticks_val = None
                    sl_roe_val = None
            except ValueError:
                pass

    # 7. Leverage
    max_l = contract.max_leverage if contract else 75
    print(f"\n7. Position Leverage (Isolated Margin, Max allowed for {sym_val}: {max_l}x):")
    if contract and last_snap_price > 0 and pu_val > 0:
        pct_30 = (1.0 / min(30, max_l)) * 100
        ticks_30 = int((last_snap_price * (pct_30 / 100)) / pu_val)
        print("   ⚠️ Leverage & Liquidation Buffer Guide:")
        if max_l >= 75:
            pct_75 = (1.0 / 75) * 100
            ticks_75 = int((last_snap_price * (pct_75 / 100)) / pu_val)
            print(f"      75x -> Liquidation is ~{ticks_75} ticks away (~{pct_75:.2f}% price move).")
        print(f"      30x -> Liquidation is ~{ticks_30} ticks away (~{pct_30:.2f}% price move) [Recommended].")
    else:
        print("   ⚠️ Leverage & Liquidation Buffer Guide:")
        print("      30x -> Safe liquidation buffer (recommended).")
    lev_str = input(f"   Leverage Multiplier [default: {min(default_lev, max_l)}x]: ").strip()
    try:
        lev_val = int(lev_str) if lev_str else min(default_lev, max_l)
    except ValueError:
        lev_val = min(default_lev, max_l)

    # 8. Cooldown
    print("\n8. Post-Trade Cooldown:")
    print("   Seconds to pause after position closes before executing the next trade cycle.")
    cool_str = input(f"   Cooldown Seconds [default: {default_cool:.0f}s]: ").strip()
    try:
        cool_val = float(cool_str) if cool_str else default_cool
    except ValueError:
        cool_val = default_cool

    # 9. Max trades
    print("\n9. Session Trade Target:")
    print("   Total number of trades to execute before engine automatically stops (0 = unlimited).")
    max_str = input(f"   Max Trades [default: {default_max}]: ").strip()
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
        volume_mode=vol_mode_val,
        volume_multiplier=vol_mult_val or 1.0,
        volume_contracts=vol_contracts_val,
        tp_ticks=tp_val,
        sl_mode=sl_mode_val,
        sl_roe_pct=sl_roe_val,
        sl_ticks=sl_ticks_val,
        sl_price_pct=sl_price_val,
        max_trades=max_val,
        poll_interval_seconds=get_setting("POLL_INTERVAL_SECONDS", 0.3),
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
        help="Trading pair symbol (e.g. BTC_USDT, DOGE_USDT, TRUMP_USDT, default from settings.py)"
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
        "--volume-contracts", "--vol",
        type=int,
        default=None,
        help="Trade volume in exact number of contracts (e.g. 1, 2, 5)"
    )
    parser.add_argument(
        "--volume-multiplier", "--vol-mult",
        type=float,
        default=None,
        help="Trade volume multiplier of minimum volume (e.g. 1.0, 2.0, 5.0)"
    )
    parser.add_argument(
        "--volume-mode",
        type=str,
        choices=["MIN", "MULTIPLIER", "CONTRACTS", "min", "multiplier", "contracts"],
        default=None,
        help="Volume mode: 'MIN', 'MULTIPLIER', or 'CONTRACTS'"
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
        help="Take profit distance in price unit (pu) ticks (default: 2)"
    )
    parser.add_argument(
        "--sl-ticks",
        type=int,
        default=None,
        help="Stop loss distance in price unit ticks (e.g. 10)"
    )
    parser.add_argument(
        "--sl-price-pct",
        type=float,
        default=None,
        help="Stop loss distance by price percentage move (e.g. 0.5)"
    )
    parser.add_argument(
        "--sl-roe",
        type=float,
        default=None,
        help="Stop loss ROE percentage on margin (default: 25.0)"
    )
    parser.add_argument(
        "--sl-mode",
        type=str,
        choices=["TICKS", "ROE", "PRICE_PCT", "ticks", "roe", "price_pct"],
        default=None,
        help="Stop loss mode: TICKS, ROE, or PRICE_PCT"
    )
    parser.add_argument(
        "--leverage",
        type=int,
        default=None,
        help="Position leverage (default from settings.py: 30)"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=None,
        help="Live price polling interval in seconds (default: 0.3)"
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

        vol_mode = (args.volume_mode or get_setting("VOLUME_MODE", "MULTIPLIER")).upper()
        vol_mult = args.volume_multiplier if args.volume_multiplier is not None else get_setting("VOLUME_MULTIPLIER", 1.0)
        vol_contracts = args.volume_contracts if args.volume_contracts is not None else (get_setting("VOLUME_CONTRACTS", 1) if vol_mode == "CONTRACTS" else None)

        tp_ticks = args.tp_ticks if args.tp_ticks is not None else get_setting("TP_TICKS", 2)
        sl_mode = (args.sl_mode or get_setting("SL_MODE", "TICKS")).upper()
        sl_ticks = args.sl_ticks if args.sl_ticks is not None else (get_setting("SL_TICKS", 10) if sl_mode == "TICKS" else None)
        sl_price_pct = args.sl_price_pct if args.sl_price_pct is not None else (get_setting("SL_PRICE_PCT", 0.5) if sl_mode == "PRICE_PCT" else None)
        sl_roe = args.sl_roe if args.sl_roe is not None else get_setting("SL_ROE_PCT", 25.0)

        lev = args.leverage if args.leverage is not None else get_setting("LEVERAGE", 30)
        cooldown = args.cooldown if args.cooldown is not None else get_setting("COOLDOWN_SECONDS", 30.0)
        max_trades = args.max_trades if args.max_trades is not None else get_setting("MAX_TRADES", 3)
        poll_int = args.poll_interval if args.poll_interval is not None else get_setting("POLL_INTERVAL_SECONDS", 0.3)

        config = ExecutionConfig(
            symbol=sym,
            direction=dir_enum,
            mode=mode_enum,
            leverage=lev,
            is_isolated=get_setting("IS_ISOLATED", True),
            cooldown_seconds=cooldown,
            volume_mode=vol_mode,
            volume_multiplier=vol_mult or 1.0,
            volume_contracts=vol_contracts,
            tp_ticks=tp_ticks,
            sl_mode=sl_mode,
            sl_ticks=sl_ticks,
            sl_price_pct=sl_price_pct,
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

    vol_desc = (
        f"{config.volume_contracts} contract(s)" if config.volume_mode == "CONTRACTS" and config.volume_contracts
        else f"{config.volume_multiplier:g}x min quantity"
    )
    sl_desc = (
        f"{config.sl_ticks} ticks" if config.sl_ticks
        else f"{config.sl_price_pct}% coin price" if config.sl_price_pct
        else f"{config.sl_roe_pct}% ROE"
    )
    print("==============================================================================")
    print("                      CONFIGURED ENGINE PARAMETERS")
    print("==============================================================================")
    print(f"  • Symbol & Mode     : {config.symbol} | {config.mode.value.upper()} | Direction: {config.direction.value}")
    print(f"  • Target Leverage   : {config.leverage}x isolated")
    print(f"  • Trade Quantity    : {vol_desc}")
    print(f"    ⚠️  CRITICAL NOTE : Trade Quantity (Volume) != Margin!")
    print(f"                       Margin deducted = Trade Quantity / {config.leverage}x leverage")
    print(f"  • Min-Profit TP     : +{config.tp_ticks} pu ticks")
    print(f"  • Stop Loss         : -{sl_desc}")
    print(f"  • Cooldown          : {config.cooldown_seconds}s | Max Trades: {'Unlimited' if config.max_trades == 0 else config.max_trades}")
    print("==============================================================================\n")

    engine = TradeExecutionEngine(config=config)
    engine.run()


if __name__ == "__main__":
    main()
