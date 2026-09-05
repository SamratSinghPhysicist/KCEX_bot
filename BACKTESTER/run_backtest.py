"""
BACKTESTER Runner & Interactive Wizard
======================================
Command-line interface and interactive wizard for running high-fidelity backtests
on historical OHLCV and tick trade data using the exact same strategy and execution
logic as the live trading engine.

Supports:
1. Cloud execution on GitHub Actions (free cloud compute, auto-downloads artifact ZIP)
2. Local execution directly on this machine
"""

import sys
import os
import time
import argparse
import datetime
from typing import Tuple

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is in path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import DataScanner, canonicalize_symbol, format_ms_to_utc
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator
from BACKTESTER.engine.reporting import BacktestReporter
from BACKTESTER.engine.github_runner import GitHubBacktestRunner
from kcex.engine.models import OrderDirection


def print_banner():
    banner = r"""
==============================================================================
   ____          _____ _  _______ ______ _____ _______ ______ _____  
  |  _ \   /\   / ____| |/ /__   __|  ____|/ ____|__   __|  ____|  __ \ 
  | |_) | /  \ | |    | ' /   | |  | |__  | (___    | |  | |__  | |__) |
  |  _ < / /\ \| |    |  <    | |  |  __|  \___ \   | |  |  __| |  _  / 
  | |_) / ____ \ |____| . \   | |  | |____ ____) |  | |  | |____| | \ \ 
  |____/_/    \_\_____|_|\_\  |_|  |______|_____/   |_|  |______|_|  \_\
                                                                        
       HIGH-FIDELITY DUAL-FEED STRATEGY BACKTESTING ENGINE
=============================================================================="""
    print(banner)


def run_interactive_wizard(scanner: DataScanner) -> Tuple[BacktestConfig, str]:
    """
    Prompts the user interactively to configure their backtest run.
    Returns (BacktestConfig, target) where target is 'github' or 'local'.
    """
    print("\n" + "=" * 78)
    print("          INTERACTIVE BACKTEST WIZARD (Press [Enter] for defaults)")
    print("=" * 78)

    catalog = scanner.scan()
    available_symbols = list(catalog.keys())

    # 1. Execution Target Selection
    print("\n1. Select Execution Target:")
    print("   [1] GitHub Actions Cloud -> Free cloud runner, no CPU lag, auto-downloads artifact ZIP [Recommended]")
    print("   [2] Locally              -> Run directly on this computer")
    target_choice = input("   Select target [default: 1 (GitHub Actions Cloud)]: ").strip()
    target = "local" if target_choice in ("2", "local", "l") else "github"

    # 2. Symbol Selection
    print("\n2. Select Trading Pair:")
    default_sym = "TRUMP_USDT"
    if available_symbols:
        for i, s in enumerate(available_symbols, 1):
            item = catalog[s]
            tf_count = len(item.ohlcv_timeframes)
            trades_note = "With Tick Trades" if item.has_trades else "OHLCV Only"
            is_def = " [Default]" if s == default_sym else ""
            print(f"   [{i}] {s:<12} ({tf_count} timeframes, {trades_note}){is_def}")
        print("   Or enter any other pair (e.g. DOGE_USDT, BTC_USDT, SOL_USDT)")
        def_idx = available_symbols.index(default_sym) + 1 if default_sym in available_symbols else 1
        sym_choice = input(f"   Select pair [default: {def_idx} ({available_symbols[def_idx-1]})]: ").strip()
        if sym_choice.isdigit() and 1 <= int(sym_choice) <= len(available_symbols):
            selected_symbol = available_symbols[int(sym_choice) - 1]
        elif sym_choice:
            selected_symbol = canonicalize_symbol(sym_choice)
        else:
            selected_symbol = available_symbols[def_idx-1]
    else:
        sym_choice = input(f"   Enter symbol [default: {default_sym}]: ").strip()
        selected_symbol = canonicalize_symbol(sym_choice or default_sym)

    sym_catalog = catalog.get(selected_symbol)

    # 3. Timeframe Selection
    if sym_catalog and sym_catalog.ohlcv_timeframes:
        available_tfs = sorted(sym_catalog.ohlcv_timeframes.keys())
    else:
        available_tfs = ["1m", "3m", "5m", "15m", "1h", "1d"]

    default_tf = "1m" if "1m" in available_tfs else available_tfs[0]
    print(f"\n3. Select Strategy Candle Timeframe for {selected_symbol}:")
    for i, tf in enumerate(available_tfs, 1):
        info = sym_catalog.ohlcv_timeframes[tf] if (sym_catalog and tf in sym_catalog.ohlcv_timeframes) else None
        d_range = f" | {format_ms_to_utc(info.start_time_ms)[:10]} to {format_ms_to_utc(info.end_time_ms)[:10]}" if info else ""
        print(f"   [{i}] {tf:<6}{d_range}")

    tf_choice = input(f"   Select timeframe [default: {default_tf}]: ").strip()
    if tf_choice.isdigit() and 1 <= int(tf_choice) <= len(available_tfs):
        selected_tf = available_tfs[int(tf_choice) - 1]
    elif tf_choice in available_tfs:
        selected_tf = tf_choice
    else:
        selected_tf = default_tf

    # 4. Strategy Selection
    print("\n4. Select Strategy:")
    print("   [1] Stochastic RSI       (Fast Scalp & Reversals in extreme zones) [Default / Recommended]")
    print("   [2] EMA Crossover        (Trend-following Golden/Death Crosses)")
    strat_choice = input("   Select Strategy [default: 1 (Stochastic RSI)]: ").strip()
    if strat_choice == "2":
        strategy_mode = "EMA_CROSSOVER"
    else:
        strategy_mode = "STOCH_RSI"

    # Strategy Parameters
    ema_preset = "5/13"
    stoch_preset = "FAST_SCALP"
    if strategy_mode == "EMA_CROSSOVER":
        print("\n   EMA Length Preset:")
        print("   [1] 5 / 13 (Fast Scalp) [Default]")
        print("   [2] 9 / 21 (Standard Momentum)")
        print("   [3] 3 / 8  (Micro Burst)")
        ep_choice = input("   Select preset [default: 1 (5/13)]: ").strip()
        if ep_choice == "2":
            ema_preset = "9/21"
        elif ep_choice == "3":
            ema_preset = "3/8"
    elif strategy_mode == "STOCH_RSI":
        print("\n   Stochastic RSI Preset:")
        print("   [1] FAST_SCALP   (9/9/3/3, OS: 20, OB: 80) [Default / Recommended for HFT]")
        print("   [2] STANDARD     (14/14/3/3, OS: 20, OB: 80)")
        print("   [3] MICRO_BURST  (7/7/3/3, OS: 15, OB: 85)")
        sp_choice = input("   Select preset [default: 1 (FAST_SCALP)]: ").strip()
        if sp_choice == "2":
            stoch_preset = "STANDARD"
        elif sp_choice == "3":
            stoch_preset = "MICRO_BURST"

    # 5. Date Range Selection
    start_val = "2026-01-01"
    end_val = "2026-08-31"
    if sym_catalog:
        ov_s, ov_e = sym_catalog.get_overlap_range(selected_tf)
        o_s, o_e = sym_catalog.get_timeframe_range(selected_tf)
        print("\n5. Select Historical Date Range:")
        if ov_s and ov_e:
            print(f"   [1] High-Fidelity Overlap Range (with tick trades): {format_ms_to_utc(ov_s)[:10]} to {format_ms_to_utc(ov_e)[:10]}")
        if o_s and o_e:
            print(f"   [2] Entire OHLCV Range: {format_ms_to_utc(o_s)[:10]} to {format_ms_to_utc(o_e)[:10]}")
        print("   [3] Custom Date Range (Default: 2026-01-01 to 2026-08-31)")
        default_range_opt = "1" if (ov_s and ov_e) else "2"
        range_choice = input(f"   Select Range [default: {default_range_opt}]: ").strip() or default_range_opt
        if range_choice == "1" and ov_s and ov_e:
            start_val = format_ms_to_utc(ov_s)[:10]
            end_val = format_ms_to_utc(ov_e)[:10]
        elif range_choice == "2" and o_s and o_e:
            start_val = format_ms_to_utc(o_s)[:10]
            end_val = format_ms_to_utc(o_e)[:10]
        elif range_choice == "3":
            start_val = input("   Enter Start Date (YYYY-MM-DD) [default: 2026-01-01]: ").strip() or "2026-01-01"
            end_val = input("   Enter End Date (YYYY-MM-DD) [default: 2026-08-31]: ").strip() or "2026-08-31"
    else:
        print("\n5. Select Historical Date Range:")
        start_val = input("   Enter Start Date (YYYY-MM-DD) [default: 2026-01-01]: ").strip() or "2026-01-01"
        end_val = input("   Enter End Date (YYYY-MM-DD) [default: 2026-08-31]: ").strip() or "2026-08-31"

    # 6. TP & SL Parameters
    print("\n6. Execution & Risk Parameters:")
    tp_input = input("   Take Profit Ticks (pu away from entry) [default: 2]: ").strip()
    tp_ticks = int(tp_input) if tp_input.isdigit() else 2

    sl_mode_input = input("   Stop Loss Mode ([1] ROE % on margin, [2] TICKS, [3] PRICE %) [default: 1 (ROE %)]: ").strip()
    if sl_mode_input == "2":
        sl_mode = "TICKS"
        sl_t_input = input("   Stop Loss Ticks [default: 10]: ").strip()
        sl_ticks = int(sl_t_input) if sl_t_input.isdigit() else 10
        sl_roe = 25.0
    elif sl_mode_input == "3":
        sl_mode = "PRICE_PCT"
        sl_p_input = input("   Stop Loss Price % [default: 0.5]: ").strip()
        sl_price = float(sl_p_input) if sl_p_input else 0.5
        sl_ticks = None
        sl_roe = 25.0
    else:
        sl_mode = "ROE"
        sl_roe_input = input("   Stop Loss ROE % on margin [default: 25.0%]: ").strip()
        sl_roe = float(sl_roe_input) if sl_roe_input else 25.0
        sl_ticks = None

    lev_input = input("   Leverage Multiplier [default: 75]: ").strip()
    leverage = int(lev_input) if lev_input.isdigit() else 75

    cap_input = input("   Initial Wallet Capital (USDT) [default: 100.0]: ").strip()
    capital = float(cap_input) if cap_input else 100.0

    max_input = input("   Max Trades limit (0 = run entire period) [default: 0]: ").strip()
    max_trades = int(max_input) if max_input.isdigit() else 0

    # 7. Trade Volume / Quantity Sizing (2x min for TRUMP, 1x min for DOGE)
    def_mult = 2.0 if "TRUMP" in selected_symbol else 1.0
    print("\n7. Trade Volume / Quantity Sizing:")
    print("   [1] Multiplier of Minimum Contract Volume (e.g. 2x min, 1x min) [Default]")
    print("   [2] Exact Number of Contracts (e.g. 2, 5, 10)")
    print("   [3] Minimum Volume (1x min contract)")
    vol_choice = input(f"   Select sizing mode [default: 1 (Multiplier {def_mult:g}x min)]: ").strip()
    vol_mode = "MULTIPLIER"
    vol_contracts = None
    vol_multiplier = def_mult
    if vol_choice == "2":
        vol_mode = "CONTRACTS"
        c_input = input(f"   Enter number of contracts per trade [default: {int(def_mult)}]: ").strip()
        vol_contracts = int(c_input) if c_input.isdigit() else int(def_mult)
        vol_multiplier = None
    elif vol_choice == "3":
        vol_mode = "MIN"
        vol_multiplier = 1.0
        vol_contracts = None
    else:
        vol_mode = "MULTIPLIER"
        m_input = input(f"   Enter Volume Multiplier [default: {def_mult:g}x min]: ").strip()
        vol_multiplier = float(m_input) if m_input else def_mult
        vol_contracts = None

    # 8. Fee Schedule Configuration
    print("\n8. Fee Schedule Configuration:")
    print("   [1] Live KCEX API (0% for TRUMP/DOGE zero-fee pairs) [Default]")
    print("   [2] Zero Fees (0.0% Maker / 0.0% Taker)")
    print("   [3] Manual Custom Rates")
    fee_choice = input("   Select Fee Mode [default: 1 (Live KCEX API)]: ").strip()
    maker_fee = None
    taker_fee = None
    if fee_choice == "2":
        fee_mode = "ZERO"
        maker_fee = 0.0
        taker_fee = 0.0
    elif fee_choice == "3":
        fee_mode = "MANUAL"
        m_input = input("   Enter Maker Fee % [default: 0.0]: ").strip()
        t_input = input("   Enter Taker Fee % [default: 0.05]: ").strip()
        maker_fee = (float(m_input) / 100.0) if m_input else 0.0
        taker_fee = (float(t_input) / 100.0) if t_input else 0.0005
    else:
        fee_mode = "LIVE"

    config = BacktestConfig(
        symbol=selected_symbol,
        timeframe=selected_tf,
        strategy_mode=strategy_mode,
        ema_preset=ema_preset,
        stoch_preset=stoch_preset,
        start_time=start_val,
        end_time=end_val,
        volume_mode=vol_mode,
        volume_contracts=vol_contracts,
        volume_multiplier=vol_multiplier,
        tp_ticks=tp_ticks,
        sl_mode=sl_mode,
        sl_ticks=sl_ticks,
        sl_roe_pct=sl_roe,
        leverage=leverage,
        initial_balance_usdt=capital,
        max_trades=max_trades,
        use_tick_data=True,
        fee_mode=fee_mode,
        maker_fee_override=maker_fee,
        taker_fee_override=taker_fee
    )
    return config, target


def main():
    parser = argparse.ArgumentParser(
        description="KCEX & Binance High-Fidelity Dual-Feed Strategy Backtester"
    )
    parser.add_argument("--scan", action="store_true", help="Scan and display historical data catalog and exit")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive setup wizard")
    parser.add_argument("--target", type=str, default=None, choices=["local", "github"], help="Target execution engine: 'github' or 'local'")
    parser.add_argument("--github", action="store_true", help="Run backtest on GitHub Actions cloud runner and auto-download artifact ZIP")
    parser.add_argument("--github-token", type=str, default=None, help="GitHub Personal Access Token for workflow dispatch")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol (e.g. TRUMP_USDT, DOGE_USDT)")
    parser.add_argument("--timeframe", type=str, default="1m", help="Strategy candle timeframe (e.g. 1m, 5m, 15m, 1h, 1d)")
    parser.add_argument("--strategy", type=str, default="STOCH_RSI", choices=["STOCH_RSI", "EMA_CROSSOVER"], help="Strategy to evaluate")
    parser.add_argument("--ema-preset", type=str, default="5/13", help="EMA preset (5/13, 9/21, 3/8)")
    parser.add_argument("--stoch-preset", type=str, default="FAST_SCALP", help="Stoch RSI preset")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--ticks", dest="use_tick_data", action="store_true", default=True, help="Enable tick-by-tick simulation")
    parser.add_argument("--no-ticks", dest="use_tick_data", action="store_false", help="Disable tick-by-tick simulation (candle high/low only)")
    parser.add_argument("--fee-mode", type=str, default="LIVE", choices=["LIVE", "ZERO", "MANUAL"], help="Fee mode: LIVE, ZERO, or MANUAL")
    parser.add_argument("--maker-fee", type=float, default=None, help="Maker fee rate or percent (e.g. 0.0 or 0.02)")
    parser.add_argument("--taker-fee", type=float, default=None, help="Taker fee rate or percent (e.g. 0.0 or 0.05)")
    parser.add_argument("--tp-ticks", type=int, default=2, help="Take profit ticks away from entry")
    parser.add_argument("--sl-mode", type=str, default="ROE", choices=["ROE", "TICKS", "PRICE_PCT"], help="Stop loss mode")
    parser.add_argument("--volume-mode", type=str, default=None, choices=["MULTIPLIER", "CONTRACTS", "MIN"], help="Volume sizing mode: MULTIPLIER, CONTRACTS, or MIN")
    parser.add_argument("--contracts", "--volume-contracts", dest="volume_contracts", type=int, default=None, help="Number of contracts per trade (e.g. 2, 5, 10)")
    parser.add_argument("--volume-multiplier", type=float, default=None, help="Multiplier of minimum contract volume (e.g. 2.0 = 2x min, 1.0 = 1x min)")
    parser.add_argument("--sl-ticks", type=int, default=10, help="Stop loss ticks away from entry")
    parser.add_argument("--sl-roe", type=float, default=25.0, help="Stop loss ROE percent (e.g. 25.0)")
    parser.add_argument("--leverage", type=int, default=75, help="Leverage multiplier")
    parser.add_argument("--capital", type=float, default=100.0, help="Initial wallet balance in USDT")
    parser.add_argument("--max-trades", type=int, default=0, help="Max trades to execute (0 = unlimited)")
    parser.add_argument("--speed", type=float, default=0.0, help="Simulated real-time playback speed (0 = max batch speed)")
    parser.add_argument("--slippage", type=int, default=0, help="Slippage in ticks")

    args = parser.parse_args()
    print_banner()

    scanner = DataScanner()

    # If --scan flag requested
    if args.scan:
        scanner.print_summary_table()
        return

    # If run with no arguments or with --interactive flag
    if args.symbol is None or args.interactive:
        config, target = run_interactive_wizard(scanner)
        # Override target if explicit flag provided on CLI
        if args.github or args.target == "github":
            target = "github"
        elif args.target == "local":
            target = "local"
    else:
        target = "github" if (args.github or args.target == "github") else "local"

        maker_fee = None
        if args.maker_fee is not None:
            maker_fee = args.maker_fee / 100.0 if args.maker_fee > 0.01 else args.maker_fee

        taker_fee = None
        if args.taker_fee is not None:
            taker_fee = args.taker_fee / 100.0 if args.taker_fee > 0.01 else args.taker_fee

        sym = canonicalize_symbol(args.symbol)
        vol_mode = args.volume_mode or "MULTIPLIER"
        vol_contracts = args.volume_contracts
        if args.volume_multiplier is not None:
            vol_mult = args.volume_multiplier
        else:
            vol_mult = 2.0 if "TRUMP" in sym else 1.0

        config = BacktestConfig(
            symbol=sym,
            timeframe=args.timeframe,
            strategy_mode=args.strategy,
            ema_preset=args.ema_preset,
            stoch_preset=args.stoch_preset,
            start_time=args.start,
            end_time=args.end,
            volume_mode=vol_mode,
            volume_contracts=vol_contracts,
            volume_multiplier=vol_mult,
            tp_ticks=args.tp_ticks,
            sl_mode=args.sl_mode,
            sl_ticks=args.sl_ticks,
            sl_roe_pct=args.sl_roe,
            leverage=args.leverage,
            initial_balance_usdt=args.capital,
            max_trades=args.max_trades,
            use_tick_data=args.use_tick_data,
            playback_speed=args.speed,
            slippage_ticks=args.slippage,
            fee_mode=args.fee_mode,
            maker_fee_override=maker_fee,
            taker_fee_override=taker_fee
        )

    # Dispatch to appropriate execution target
    if target == "github":
        runner = GitHubBacktestRunner(token=args.github_token)
        reports_dir = os.path.join(ROOT_DIR, "BACKTESTER", "reports")
        success = runner.run_cloud_backtest(config=config, output_dir=reports_dir)
        if not success:
            sys.exit(1)
        return

    # LOCAL EXECUTION
    engine = BacktestExecutionEngine(config=config)
    contract = engine.contract
    m_pct = contract.maker_fee_rate * 100.0
    t_pct = contract.taker_fee_rate * 100.0
    if contract.maker_fee_rate == 0.0 and contract.taker_fee_rate == 0.0:
        fee_summary = f"Maker {m_pct:.2f}% / Taker {t_pct:.2f}% (ZERO FEES CONFIRMED)"
    else:
        fee_summary = f"Maker {m_pct:.3f}% / Taker {t_pct:.3f}% ({config.fee_mode})"

    vol_desc = f"{config.volume_contracts} contracts" if config.volume_contracts else f"{config.volume_multiplier}x min volume"

    print("\n" + "=" * 78)
    print("                    STARTING LOCAL BACKTEST EXECUTION")
    print("=" * 78)
    print(f"Symbol:           {config.symbol}")
    print(f"Timeframe:        {config.timeframe}")
    print(f"Strategy:         {config.strategy_mode}")
    print(f"Date Range:       {config.start_time or 'Earliest'} -> {config.end_time or 'Latest'}")
    print(f"Trade Volume:     {vol_desc} ({config.volume_mode})")
    print(f"High-Fid Ticks:   {'ENABLED (Streaming tick trades)' if config.use_tick_data else 'DISABLED (Candle High/Low)'}")
    print(f"Fee Schedule:     {fee_summary}")
    print(f"Initial Capital:  {config.initial_balance_usdt:.2f} USDT")
    print(f"Leverage:         {config.leverage}x")
    print(f"Take Profit:      +{config.tp_ticks} ticks")
    print(f"Stop Loss:        {config.sl_ticks} ticks" if config.sl_mode == "TICKS" else f"-{config.sl_roe_pct}% ROE")
    print("=" * 78 + "\n")

    t_start = time.time()

    print("[*] Processing historical data...")
    outcomes = engine.run()
    elapsed = time.time() - t_start

    print(f"[*] Simulation completed in {elapsed:.2f} seconds ({len(outcomes)} trades executed).")

    # Metrics & Reporting
    summary = PerformanceCalculator.calculate(
        outcomes=outcomes,
        initial_balance_usdt=config.initial_balance_usdt,
        inr_rate=config.inr_rate
    )

    reporter = BacktestReporter()
    reporter.print_summary(summary)
    reporter.print_trades_table(outcomes, limit=15)
    reporter.export_all(outcomes=outcomes, summary=summary, config=config, contract=contract)


if __name__ == "__main__":
    main()
