"""
BACKTESTER Runner & Interactive Wizard
======================================
Command-line interface and interactive wizard for running high-fidelity backtests
on historical OHLCV and tick trade data using the exact same strategy and execution
logic as the live trading engine.
"""

import sys
import os
import time
import argparse
import datetime

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


def run_interactive_wizard(scanner: DataScanner) -> BacktestConfig:
    """Prompts the user interactively to configure their backtest run."""
    print("\n" + "=" * 78)
    print("          INTERACTIVE BACKTEST WIZARD (Press [Enter] for defaults)")
    print("=" * 78)

    catalog = scanner.scan()
    available_symbols = list(catalog.keys())
    if not available_symbols:
        print("[!] No historical data found in BACKTESTER directories.")
        sys.exit(1)

    # 1. Symbol Selection
    print("\n1. Select Trading Pair:")
    for i, s in enumerate(available_symbols, 1):
        item = catalog[s]
        tf_count = len(item.ohlcv_timeframes)
        trades_note = "With Tick Trades" if item.has_trades else "OHLCV Only"
        print(f"   [{i}] {s:<12} ({tf_count} timeframes, {trades_note})")
    
    sym_choice = input(f"   Select pair [default: 1 ({available_symbols[0]})]: ").strip()
    if sym_choice.isdigit() and 1 <= int(sym_choice) <= len(available_symbols):
        selected_symbol = available_symbols[int(sym_choice) - 1]
    else:
        selected_symbol = available_symbols[0]

    sym_catalog = catalog[selected_symbol]

    # 2. Timeframe Selection
    available_tfs = sorted(sym_catalog.ohlcv_timeframes.keys())
    default_tf = "1m" if "1m" in available_tfs else available_tfs[0]
    print(f"\n2. Select Strategy Candle Timeframe for {selected_symbol}:")
    for i, tf in enumerate(available_tfs, 1):
        info = sym_catalog.ohlcv_timeframes[tf]
        d_range = f"{format_ms_to_utc(info.start_time_ms)[:10]} to {format_ms_to_utc(info.end_time_ms)[:10]}"
        print(f"   [{i}] {tf:<6} ({info.total_files} files | {d_range})")

    tf_choice = input(f"   Select timeframe [default: {default_tf}]: ").strip()
    if tf_choice.isdigit() and 1 <= int(tf_choice) <= len(available_tfs):
        selected_tf = available_tfs[int(tf_choice) - 1]
    elif tf_choice in available_tfs:
        selected_tf = tf_choice
    else:
        selected_tf = default_tf

    # 3. Strategy Selection
    print("\n3. Select Strategy:")
    print("   [1] EMA Crossover        (Trend-following Golden/Death Crosses)")
    print("   [2] Stochastic RSI       (Momentum reversals in Overbought/Oversold zones)")
    print("   [3] Directional Cycle    (Continuous trade cycling with cooldown)")
    print("   [4] Microstructure       (Order book imbalance & trade delta bursts)")
    strat_choice = input("   Select Strategy [default: 1 (EMA Crossover)]: ").strip()
    if strat_choice == "2":
        strategy_mode = "STOCH_RSI"
    elif strat_choice == "3":
        strategy_mode = "CYCLE"
    elif strat_choice == "4":
        strategy_mode = "MICROSTRUCTURE"
    else:
        strategy_mode = "EMA_CROSSOVER"

    # 4. Strategy Parameters
    ema_preset = "5/13"
    stoch_preset = "FAST_SCALP"
    if strategy_mode == "EMA_CROSSOVER":
        print("\n4. EMA Length Preset:")
        print("   [1] 5 / 13 (Fast Scalp)")
        print("   [2] 9 / 21 (Standard Momentum)")
        print("   [3] 3 / 8  (Micro Burst)")
        ep_choice = input("   Select preset [default: 1 (5/13)]: ").strip()
        if ep_choice == "2":
            ema_preset = "9/21"
        elif ep_choice == "3":
            ema_preset = "3/8"

    # 5. Date Range Selection
    ov_s, ov_e = sym_catalog.get_overlap_range(selected_tf)
    o_s, o_e = sym_catalog.get_timeframe_range(selected_tf)

    print("\n5. Select Historical Date Range:")
    if ov_s and ov_e:
        print(f"   [1] High-Fidelity Overlap Range (with full tick trades):")
        print(f"       {format_ms_to_utc(ov_s)[:10]} to {format_ms_to_utc(ov_e)[:10]}")
    if o_s and o_e:
        print(f"   [2] Entire Available OHLCV Range:")
        print(f"       {format_ms_to_utc(o_s)[:10]} to {format_ms_to_utc(o_e)[:10]}")
    print("   [3] Custom Date Range")

    default_range_opt = "1" if (ov_s and ov_e) else "2"
    range_choice = input(f"   Select Range [default: {default_range_opt}]: ").strip() or default_range_opt

    start_val = None
    end_val = None
    if range_choice == "1" and ov_s and ov_e:
        start_val = format_ms_to_utc(ov_s)[:10]
        end_val = format_ms_to_utc(ov_e)[:10]
    elif range_choice == "3":
        start_val = input("   Enter Start Date (YYYY-MM-DD): ").strip()
        end_val = input("   Enter End Date (YYYY-MM-DD): ").strip()
    else:
        if o_s and o_e:
            start_val = format_ms_to_utc(o_s)[:10]
            end_val = format_ms_to_utc(o_e)[:10]

    # 6. TP & SL Parameters
    print("\n6. Execution & Risk Parameters:")
    tp_input = input("   Take Profit Ticks (pu away from entry) [default: 2]: ").strip()
    tp_ticks = int(tp_input) if tp_input.isdigit() else 2

    sl_mode_input = input("   Stop Loss Mode ([1] TICKS, [2] ROE %, [3] PRICE %) [default: 1]: ").strip()
    if sl_mode_input == "2":
        sl_mode = "ROE"
        sl_roe_input = input("   Stop Loss ROE % [default: 25.0]: ").strip()
        sl_roe = float(sl_roe_input) if sl_roe_input else 25.0
        sl_ticks = None
    elif sl_mode_input == "3":
        sl_mode = "PRICE_PCT"
        sl_p_input = input("   Stop Loss Price % [default: 0.5]: ").strip()
        sl_price = float(sl_p_input) if sl_p_input else 0.5
        sl_ticks = None
        sl_roe = 25.0
    else:
        sl_mode = "TICKS"
        sl_t_input = input("   Stop Loss Ticks [default: 10]: ").strip()
        sl_ticks = int(sl_t_input) if sl_t_input.isdigit() else 10
        sl_roe = 25.0

    lev_input = input("   Leverage [default: 30]: ").strip()
    leverage = int(lev_input) if lev_input.isdigit() else 30

    cap_input = input("   Initial Wallet Capital (USDT) [default: 100.0]: ").strip()
    capital = float(cap_input) if cap_input else 100.0

    max_input = input("   Max Trades limit (0 = run entire period) [default: 0]: ").strip()
    max_trades = int(max_input) if max_input.isdigit() else 0

    # 7. Fee Schedule Configuration
    print("\n7. Fee Schedule Configuration:")
    print("   [1] Live KCEX API (Fetch live fee rate from KCEX - 0% for zero-fee pairs)")
    print("   [2] Zero Fees (0.0% Maker / 0.0% Taker)")
    print("   [3] Manual Custom Rates (Enter custom Maker & Taker percentages)")
    fee_choice = input("   Select Fee Mode [default: 1 (Live KCEX API)]: ").strip()
    maker_fee = None
    taker_fee = None
    if fee_choice == "2":
        fee_mode = "ZERO"
        maker_fee = 0.0
        taker_fee = 0.0
    elif fee_choice == "3":
        fee_mode = "MANUAL"
        m_input = input("   Enter Maker Fee % (e.g. 0.0 or 0.02) [default: 0.0]: ").strip()
        t_input = input("   Enter Taker Fee % (e.g. 0.0 or 0.05) [default: 0.05]: ").strip()
        maker_fee = (float(m_input) / 100.0) if m_input else 0.0
        taker_fee = (float(t_input) / 100.0) if t_input else 0.0005
    else:
        fee_mode = "LIVE"

    return BacktestConfig(
        symbol=selected_symbol,
        timeframe=selected_tf,
        strategy_mode=strategy_mode,
        ema_preset=ema_preset,
        stoch_preset=stoch_preset,
        start_time=start_val,
        end_time=end_val,
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


def main():
    parser = argparse.ArgumentParser(
        description="KCEX & Binance High-Fidelity Dual-Feed Strategy Backtester"
    )
    parser.add_argument("--scan", action="store_true", help="Scan and display historical data catalog and exit")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive setup wizard")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol (e.g. TRUMP_USDT, DOGE_USDT)")
    parser.add_argument("--timeframe", type=str, default="1m", help="Strategy candle timeframe (e.g. 1m, 5m, 15m, 1h, 1d)")
    parser.add_argument("--strategy", type=str, default="EMA_CROSSOVER", choices=["EMA_CROSSOVER", "STOCH_RSI", "CYCLE", "MICROSTRUCTURE"], help="Strategy to evaluate")
    parser.add_argument("--ema-preset", type=str, default="5/13", help="EMA preset (5/13, 9/21, 3/8)")
    parser.add_argument("--stoch-preset", type=str, default="FAST_SCALP", help="Stoch RSI preset")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--ticks", dest="use_tick_data", action="store_true", default=True, help="Enable tick-by-tick simulation")
    parser.add_argument("--no-ticks", dest="use_tick_data", action="store_false", help="Disable tick-by-tick simulation (candle high/low only)")
    parser.add_argument("--fee-mode", type=str, default="LIVE", choices=["LIVE", "ZERO", "MANUAL"], help="Fee mode: LIVE, ZERO, or MANUAL")
    parser.add_argument("--maker-fee", type=float, default=None, help="Maker fee rate or %% (e.g. 0.0 or 0.02)")
    parser.add_argument("--taker-fee", type=float, default=None, help="Taker fee rate or %% (e.g. 0.0 or 0.05)")
    parser.add_argument("--tp-ticks", type=int, default=2, help="Take profit ticks away from entry")
    parser.add_argument("--sl-mode", type=str, default="TICKS", choices=["TICKS", "ROE", "PRICE_PCT"], help="Stop loss mode")
    parser.add_argument("--sl-ticks", type=int, default=10, help="Stop loss ticks away from entry")
    parser.add_argument("--sl-roe", type=float, default=25.0, help="Stop loss ROE %")
    parser.add_argument("--leverage", type=int, default=30, help="Leverage multiplier")
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
        config = run_interactive_wizard(scanner)
    else:
        maker_fee = None
        if args.maker_fee is not None:
            maker_fee = args.maker_fee / 100.0 if args.maker_fee > 0.01 else args.maker_fee

        taker_fee = None
        if args.taker_fee is not None:
            taker_fee = args.taker_fee / 100.0 if args.taker_fee > 0.01 else args.taker_fee

        config = BacktestConfig(
            symbol=args.symbol,
            timeframe=args.timeframe,
            strategy_mode=args.strategy,
            ema_preset=args.ema_preset,
            stoch_preset=args.stoch_preset,
            start_time=args.start,
            end_time=args.end,
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

    engine = BacktestExecutionEngine(config=config)
    contract = engine.contract
    m_pct = contract.maker_fee_rate * 100.0
    t_pct = contract.taker_fee_rate * 100.0
    if contract.maker_fee_rate == 0.0 and contract.taker_fee_rate == 0.0:
        fee_summary = f"Maker {m_pct:.2f}% / Taker {t_pct:.2f}% (ZERO FEES CONFIRMED)"
    else:
        fee_summary = f"Maker {m_pct:.3f}% / Taker {t_pct:.3f}% ({config.fee_mode})"

    print("\n" + "=" * 78)
    print("                    STARTING BACKTEST EXECUTION")
    print("=" * 78)
    print(f"Symbol:           {config.symbol}")
    print(f"Timeframe:        {config.timeframe}")
    print(f"Strategy:         {config.strategy_mode}")
    print(f"Date Range:       {config.start_time or 'Earliest'} -> {config.end_time or 'Latest'}")
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
    reporter.export_all(outcomes, summary)


if __name__ == "__main__":
    main()
