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
    default_vol_mult = get_setting("VOLUME_MULTIPLIER", 2.0)
    default_vol_contracts = get_setting("VOLUME_CONTRACTS", 2)
    default_sl_mode = get_setting("SL_MODE", "ROE").upper()
    default_sl_ticks = get_setting("SL_TICKS", 10)
    default_sl_roe = get_setting("SL_ROE_PCT", 25.0)
    default_sl_price = get_setting("SL_PRICE_PCT", 0.5)
    default_lev = get_setting("LEVERAGE", 75)
    default_cool = get_setting("COOLDOWN_SECONDS", 30.0)
    default_max = get_setting("MAX_TRADES", 3)

    print("\n" + "=" * 78)
    print("           INTERACTIVE SETUP WIZARD (Press [Enter] to keep defaults)")
    print("=" * 78)
    print("💡 Tip: Press [Enter] on any prompt to accept the default from settings.py.\n")

    # 0. Quantitative Strategy Preset Selection
    active_preset_name = get_setting("ACTIVE_PRESET", "DOGE_V2_2_RATCHET_CHAMPION").upper()
    print("0. Strategy Preset Selection:")
    print("   [1] DOGE_V2_2_RATCHET_CHAMPION     -> Phase V2.2 Deep Dive Champion (5t TP / 2t SL + Ratchet + Inverted + Maker)")
    print("   [2] DOGE_ASYMMETRIC_MOMENTUM_10T2T -> Asymmetric Momentum Scalp (10t TP / 2t SL + Direct Momentum)")
    print("   [3] TRUMP_LEGACY_BASELINE          -> Original Baseline (2t TP / 25% ROE SL + Market Order)")
    print("   [4] CUSTOM / MANUAL SETUP          -> Step-by-step custom wizard configuration")

    def_preset_choice = "1"
    if active_preset_name == "DOGE_ASYMMETRIC_MOMENTUM_10T2T":
        def_preset_choice = "2"
    elif active_preset_name == "TRUMP_LEGACY_BASELINE":
        def_preset_choice = "3"
    elif active_preset_name == "CUSTOM":
        def_preset_choice = "4"

    preset_choice = input(f"   Select Preset [default: {def_preset_choice} ({active_preset_name})]: ").strip()
    if not preset_choice:
        preset_choice = def_preset_choice

    if preset_choice in ("1", "2", "3"):
        preset_map = {
            "1": "DOGE_V2_2_RATCHET_CHAMPION",
            "2": "DOGE_ASYMMETRIC_MOMENTUM_10T2T",
            "3": "TRUMP_LEGACY_BASELINE"
        }
        chosen_preset = preset_map[preset_choice]
        preset_cfg = settings.get_active_preset_config(chosen_preset) if hasattr(settings, "get_active_preset_config") else {}
        print(f"\n   ✅ Loaded Preset: {preset_cfg.get('name', chosen_preset)}")
        print(f"      • Symbol: {preset_cfg.get('symbol')}")
        print(f"      • Take Profit: +{preset_cfg.get('tp_ticks')} ticks | Stop Loss: {preset_cfg.get('sl_ticks')} ticks ({preset_cfg.get('sl_mode')})")
        print(f"      • Signal Mode: {'INVERTED (Exhaustion Fading)' if preset_cfg.get('invert_signal') else 'DIRECT (Momentum)'}")
        print(f"      • Execution Style: {preset_cfg.get('execution_style')}")
        print(f"      • Tick Ratchet: {'ENABLED' if preset_cfg.get('ratchet_enabled') else 'DISABLED'}")

        # Prompt for mode
        print("\n1. Execution Mode:")
        print("   [1] LIVE TRADING    -> Real orders submitted to KCEX using wallet balance.")
        print("   [2] SIMULATED (Dry) -> Virtual orders with real-time live ticker data (0 risk).")
        mode_str = input(f"   Select Mode [default: {'1 (LIVE)' if default_mode == 'live' else '2 (SIMULATED)'}]: ").strip()
        mode_val = EngineMode.DRY_RUN if mode_str == "2" else (EngineMode.LIVE if mode_str == "1" else (EngineMode.LIVE if default_mode == "live" else EngineMode.DRY_RUN))

        sym_p = preset_cfg.get("symbol", "DOGE_USDT")
        v_mode, v_mult = ("MULTIPLIER", 1.0) if "DOGE" in sym_p else ("MULTIPLIER", 2.0)

        print("=" * 78 + "\n")
        return ExecutionConfig(
            symbol=sym_p,
            direction=OrderDirection.LONG,
            mode=mode_val,
            leverage=75,
            is_isolated=True,
            cooldown_seconds=default_cool,
            volume_mode=v_mode,
            volume_multiplier=v_mult,
            tp_ticks=preset_cfg.get("tp_ticks", 5),
            dynamic_tp=False,
            sl_mode=preset_cfg.get("sl_mode", "TICKS"),
            sl_ticks=preset_cfg.get("sl_ticks", 2),
            sl_roe_pct=preset_cfg.get("sl_roe_pct", 25.0),
            max_trades=default_max,
            strategy_mode=preset_cfg.get("strategy_mode", "STOCH_RSI"),
            bi_directional=True,
            invert_signal=preset_cfg.get("invert_signal", True),
            dynamic_regime_fading=preset_cfg.get("dynamic_regime_fading", False),
            adx_fading_cutoff=preset_cfg.get("adx_fading_cutoff", 25.0),
            execution_style=preset_cfg.get("execution_style", "MAKER_HYBRID"),
            maker_queue_timeout_seconds=preset_cfg.get("maker_queue_timeout_seconds", 10.0),
            resting_limit_tp=preset_cfg.get("resting_limit_tp", True),
            ratchet_enabled=preset_cfg.get("ratchet_enabled", True),
            ratchet_trigger_ticks=preset_cfg.get("ratchet_trigger_ticks", 1.0),
            ratchet_stall_seconds=preset_cfg.get("ratchet_stall_seconds", 10.0),
            ratchet_tighten_ticks=preset_cfg.get("ratchet_tighten_ticks", 1.0),
            ratchet_breakeven_ticks=preset_cfg.get("ratchet_breakeven_ticks", 2.5),
            slippage_enabled=preset_cfg.get("slippage_enabled", False),
            slippage_ticks=preset_cfg.get("slippage_ticks", 0),
            poll_interval_seconds=get_setting("POLL_INTERVAL_SECONDS", 0.3),
            logs_dir=get_setting("LOGS_DIR", "logs"),
            realtime_log_file=get_setting("REALTIME_LOG_FILE", "engine_realtime.log"),
            outcomes_log_file=get_setting("OUTCOMES_LOG_FILE", "trade_outcomes.txt"),
            outcomes_jsonl_file=get_setting("OUTCOMES_JSONL_FILE", "trade_outcomes.jsonl")
        )

    # 1. Mode (Custom Manual Configuration)
    print("\n1. Execution Mode:")
    print("   [1] LIVE TRADING    -> Real orders submitted to KCEX using wallet balance.")
    print("   [2] SIMULATED (Dry) -> Virtual orders with real-time live ticker data (0 risk).")
    mode_str = input(f"   Select Mode [default: {'1 (LIVE)' if default_mode == 'live' else '2 (SIMULATED)'}]: ").strip()
    if mode_str == "2":
        mode_val = EngineMode.DRY_RUN
    elif mode_str == "1":
        mode_val = EngineMode.LIVE
    else:
        mode_val = EngineMode.LIVE if default_mode == "live" else EngineMode.DRY_RUN

    # 2. Trading Pair
    print("\n2. Trading Pair:")
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

    # Dynamic default volume per symbol: 2x min for TRUMP, 1x min for DOGE
    if hasattr(settings, "get_default_quantity_for_symbol"):
        default_vol_mode, default_vol_mult = settings.get_default_quantity_for_symbol(sym_val)
    elif "TRUMP" in sym_val:
        default_vol_mode, default_vol_mult = "MULTIPLIER", 2.0
    elif "DOGE" in sym_val:
        default_vol_mode, default_vol_mult = "MULTIPLIER", 1.0

    # 3. Strategy Engine Selection & Directional Flow
    default_strat = get_setting("STRATEGY_MODE", "STOCH_RSI").upper()
    default_ema_preset = get_setting("EMA_PRESET", "5/13")
    default_ema_fast = get_setting("EMA_FAST", 5)
    default_ema_slow = get_setting("EMA_SLOW", 13)
    default_ema_interval = get_setting("EMA_INTERVAL", "Min1")
    default_ema_bi = get_setting("EMA_BI_DIRECTIONAL", True)
    default_stoch_preset = get_setting("STOCH_PRESET", "FAST_SCALP")
    default_stoch_rsi_p = get_setting("STOCH_RSI_PERIOD", 9)
    default_stoch_p = get_setting("STOCH_PERIOD", 9)
    default_stoch_k = get_setting("STOCH_K_PERIOD", 3)
    default_stoch_d = get_setting("STOCH_D_PERIOD", 3)
    default_stoch_os = get_setting("STOCH_OVERSOLD", 20.0)
    default_stoch_ob = get_setting("STOCH_OVERBOUGHT", 80.0)
    default_stoch_interval = get_setting("STOCH_INTERVAL", "Min1")
    default_stoch_bi = get_setting("STOCH_BI_DIRECTIONAL", True)
    default_stoch_zone = get_setting("STOCH_ZONE_FILTER", True)
    default_dir = get_setting("DIRECTION", "LONG").upper()
    invert_signal_val = get_setting("INVERT_SIGNAL", True)
    execution_style_val = get_setting("EXECUTION_STYLE", "MAKER_HYBRID")
    ratchet_enabled_val = get_setting("RATCHET_ENABLED", True)
    slippage_enabled_val = get_setting("SLIPPAGE_ENABLED", False)
    slippage_ticks_val = get_setting("SLIPPAGE_TICKS", 0)

    print("\n3. Strategy & Signal Engine:")
    print("   [1] EMA CROSSOVER     -> Fast/Slow EMA Crossover (5/13, 9/21, 3/8)")
    print("   [2] STOCHASTIC RSI    -> Fast Scalp & Mean Reversion (%K/%D cross in Oversold/Overbought zones) [Default]")
    print("   [3] SMART STRATEGY    -> Autonomous Regime-Adaptive Engine (Auto-routes between EMA & Stoch RSI)")

    default_strat_choice = "2"
    if default_strat in ("EMA", "EMA_CROSSOVER", "CROSSOVER"):
        default_strat_choice = "1"
    elif default_strat in ("SMART", "SMART_STRATEGY"):
        default_strat_choice = "3"
    else:
        default_strat_choice = "2"

    strat_str = input(f"   Select Strategy [default: {default_strat_choice} ({default_strat})]: ").strip()
    if not strat_str:
        strat_str = default_strat_choice

    ema_preset_val = default_ema_preset
    ema_fast_val = default_ema_fast
    ema_slow_val = default_ema_slow
    ema_interval_val = default_ema_interval

    stoch_preset_val = default_stoch_preset
    stoch_rsi_p_val = default_stoch_rsi_p
    stoch_p_val = default_stoch_p
    stoch_k_val = default_stoch_k
    stoch_d_val = default_stoch_d
    stoch_os_val = default_stoch_os
    stoch_ob_val = default_stoch_ob
    stoch_interval_val = default_stoch_interval
    stoch_zone_val = default_stoch_zone

    if strat_str in ("1", "EMA", "EMA_CROSSOVER", "CROSSOVER", "ema", "ema_crossover"):
        strat_mode_val = "EMA_CROSSOVER"
        print("\n   EMA Crossover Preset:")
        print("   [1] 5 / 13  -> Fibonacci Scalp (Fast: 5, Slow: 13) [Default / Recommended]")
        print("   [2] 9 / 21  -> Momentum / Intraday Trend Scalp (Fast: 9, Slow: 21)")
        print("   [3] 3 / 8   -> Ultra-Fast Micro-Scalp (Fast: 3, Slow: 8)")
        print("   [4] CUSTOM  -> Specify custom fast and slow periods")
        preset_choice = input(f"   Select Preset [default: 1 ({default_ema_preset})]: ").strip()
        if preset_choice == "2":
            ema_preset_val = "9/21"
            ema_fast_val = 9
            ema_slow_val = 21
        elif preset_choice == "3":
            ema_preset_val = "3/8"
            ema_fast_val = 3
            ema_slow_val = 8
        elif preset_choice == "4":
            ema_preset_val = "custom"
            try:
                ema_fast_val = int(input("      Fast EMA Period: ").strip() or "5")
                ema_slow_val = int(input("      Slow EMA Period: ").strip() or "13")
            except ValueError:
                ema_fast_val = 5
                ema_slow_val = 13
        else:
            ema_preset_val = "5/13"
            ema_fast_val = 5
            ema_slow_val = 13

        print(f"   ✅ Active EMA Config: Fast={ema_fast_val}, Slow={ema_slow_val} (Preset: {ema_preset_val})")

        print("\n   EMA Directional Flow:")
        print("   [1] AUTONOMOUS BI-DIRECTIONAL -> Scalp both LONG (Golden Cross) & SHORT (Death Cross) [Recommended]")
        print("   [2] SINGLE DIRECTION ONLY     -> Scalp only one chosen direction")
        bi_str = input(f"   Select Flow [default: {'1 (BI-DIRECTIONAL)' if default_ema_bi else '2 (SINGLE)'}]: ").strip()
        if bi_str == "2":
            bi_directional_val = False
            print("\n   Order Direction for EMA Scalps:")
            print("   [1] LONG  -> Profit when price rises.")
            print("   [2] SHORT -> Profit when price drops.")
            dir_str = input(f"   Select Direction [default: {'1 (LONG)' if default_dir == 'LONG' else '2 (SHORT)'}]: ").strip()
            if dir_str == "2" or dir_str.upper() == "SHORT":
                dir_val = OrderDirection.SHORT
            else:
                dir_val = OrderDirection.LONG
        else:
            bi_directional_val = True
            dir_val = OrderDirection.LONG
            print("   ℹ️  Order Direction: Autonomous (Strategy dynamically enters LONG on Golden Cross and SHORT on Death Cross).")

    elif strat_str in ("3", "SMART", "SMART_STRATEGY", "smart", "smart_strategy"):
        strat_mode_val = "SMART_STRATEGY"
        bi_directional_val = True
        dir_val = OrderDirection.LONG
        print("\n   ✅ Active Smart Strategy: Autonomous Multi-Regime Micro-Scalping")
        print("      • Classifies 1m candles into 5 microstructure regimes")
        print("      • Strong Momentum Trends -> Routes to EMA Crossover (5/13)")
        print("      • Balanced Ranges        -> Routes to Stoch RSI (Fast Scalp)")
        print("      • Sub-ATR Compression    -> Pauses safely until volatility recovers")
        print("      • Climax Volatility      -> Pauses safely to avoid spread sweeps")
        print("      • 200 EMA Filter         -> OFF (Mean-reversion enabled per empirical research)")

    else:
        # Default: STOCH_RSI
        strat_mode_val = "STOCH_RSI"
        print("\n   Stochastic RSI Preset:")
        print("   [1] FAST_SCALP   -> 9/9/3/3 (OS: 20, OB: 80) [Default / Recommended for HFT]")
        print("   [2] STANDARD     -> 14/14/3/3 (OS: 20, OB: 80) [Balanced Trend/Momentum]")
        print("   [3] MICRO_BURST  -> 7/7/3/3 (OS: 15, OB: 85) [Ultra-Responsive Scalp]")
        print("   [4] CUSTOM       -> Specify custom periods & zones")
        preset_choice = input(f"   Select Preset [default: 1 ({default_stoch_preset})]: ").strip()
        if preset_choice == "2":
            stoch_preset_val = "STANDARD"
            stoch_rsi_p_val, stoch_p_val, stoch_k_val, stoch_d_val = 14, 14, 3, 3
            stoch_os_val, stoch_ob_val = 20.0, 80.0
        elif preset_choice == "3":
            stoch_preset_val = "MICRO_BURST"
            stoch_rsi_p_val, stoch_p_val, stoch_k_val, stoch_d_val = 7, 7, 3, 3
            stoch_os_val, stoch_ob_val = 15.0, 85.0
        elif preset_choice == "4":
            stoch_preset_val = "custom"
            try:
                stoch_rsi_p_val = int(input("      RSI Period [default 9]: ").strip() or "9")
                stoch_p_val = int(input("      Stoch Lookback [default 9]: ").strip() or "9")
                stoch_k_val = int(input("      %K Smoothing [default 3]: ").strip() or "3")
                stoch_d_val = int(input("      %D Smoothing [default 3]: ").strip() or "3")
                stoch_os_val = float(input("      Oversold Threshold [default 20.0]: ").strip() or "20.0")
                stoch_ob_val = float(input("      Overbought Threshold [default 80.0]: ").strip() or "80.0")
            except ValueError:
                stoch_rsi_p_val, stoch_p_val, stoch_k_val, stoch_d_val = 9, 9, 3, 3
                stoch_os_val, stoch_ob_val = 20.0, 80.0
        else:
            stoch_preset_val = "FAST_SCALP"
            stoch_rsi_p_val, stoch_p_val, stoch_k_val, stoch_d_val = 9, 9, 3, 3
            stoch_os_val, stoch_ob_val = 20.0, 80.0

        print(f"   ✅ Active StochRSI Config: Preset={stoch_preset_val} (RSI={stoch_rsi_p_val}, Stoch={stoch_p_val}, %K={stoch_k_val}, %D={stoch_d_val}, OS={stoch_os_val}, OB={stoch_ob_val})")

        print("\n   Stochastic RSI Directional Flow:")
        print("   [1] AUTONOMOUS BI-DIRECTIONAL -> Scalp both LONG (Oversold Bullish Cross) & SHORT (Overbought Bearish Cross) [Recommended]")
        print("   [2] SINGLE DIRECTION ONLY     -> Scalp only one chosen direction")
        bi_str = input(f"   Select Flow [default: {'1 (BI-DIRECTIONAL)' if default_stoch_bi else '2 (SINGLE)'}]: ").strip()
        if bi_str == "2":
            bi_directional_val = False
            print("\n   Order Direction for StochRSI Scalps:")
            print("   [1] LONG  -> Profit when price rises (Oversold Bullish Cross).")
            print("   [2] SHORT -> Profit when price drops (Overbought Bearish Cross).")
            dir_str = input(f"   Select Direction [default: {'1 (LONG)' if default_dir == 'LONG' else '2 (SHORT)'}]: ").strip()
            if dir_str == "2" or dir_str.upper() == "SHORT":
                dir_val = OrderDirection.SHORT
            else:
                dir_val = OrderDirection.LONG
        else:
            bi_directional_val = True
            dir_val = OrderDirection.LONG
            print("   ℹ️  Order Direction: Autonomous (Strategy dynamically enters LONG on oversold cross and SHORT on overbought cross).")

        print("\n   Signal Direction Mode (Paradigm):")
        print("   [1] DIRECT MOMENTUM            -> Oversold Long / Overbought Short [Default]")
        print("   [2] INVERTED EXHAUSTION FADING  -> Overbought Long / Oversold Short (Phase V2.1/V2.2 Discovery)")
        def_inv_choice = "2" if get_setting("INVERT_SIGNAL", True) else "1"
        inv_str = input(f"   Select Signal Mode [default: {def_inv_choice}]: ").strip()
        invert_signal_val = True if (inv_str in ("2", "inv", "inverted", "fading") or (not inv_str and def_inv_choice == "2")) else False
        print(f"   ✓ Signal Mode: {'INVERTED (Exhaustion Fading)' if invert_signal_val else 'DIRECT (Momentum)'}")

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

    default_dyn_tp = get_setting("DYNAMIC_TP", False)
    print("   Take-Profit Sizing Mode:")
    print(f"   [1] FIXED TP   -> Strictly exit at exactly {tp_val} pu tick(s) [Recommended]")
    print(f"   [2] DYNAMIC TP -> Allow signal strength to dynamically scale TP (1 to 3 pu)")
    tp_mode_str = input(f"   Select TP Mode [default: {'1 (FIXED)' if not default_dyn_tp else '2 (DYNAMIC)'}]: ").strip()
    dynamic_tp_val = (tp_mode_str == "2") if tp_mode_str else default_dyn_tp

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
    mmr_ratio = contract.maintenance_margin_ratio if contract and contract.maintenance_margin_ratio > 0 else 0.01

    print(f"\n7. Position Leverage (Isolated Margin, Max allowed for {sym_val}: {max_l}x):")
    if contract and last_snap_price > 0 and pu_val > 0:
        pct_30 = max(0.001, (1.0 / min(30, max_l) - mmr_ratio)) * 100
        ticks_30 = int((last_snap_price * (pct_30 / 100)) / pu_val)
        print("   ⚠️ True Liquidation Buffer Guide (Including Maintenance Margin):")
        if max_l >= 75:
            pct_75 = max(0.001, (1.0 / 75 - mmr_ratio)) * 100
            ticks_75 = int((last_snap_price * (pct_75 / 100)) / pu_val)
            print(f"      75x -> Liquidation is ONLY ~{ticks_75} ticks away (~{pct_75:.2f}% price move). Max safe SL: ~{int(ticks_75*0.8)} ticks. [EXTREME RISK]")
        print(f"      30x -> Liquidation is ~{ticks_30} ticks away (~{pct_30:.2f}% price move). Max safe SL: ~{int(ticks_30*0.8)} ticks. [RECOMMENDED]")
    else:
        print("   ⚠️ True Liquidation Buffer Guide:")
        print("      30x -> Safe liquidation buffer (recommended).")

    lev_str = input(f"   Leverage Multiplier [default: {min(default_lev, max_l)}x]: ").strip()
    try:
        lev_val = int(lev_str) if lev_str else min(default_lev, max_l)
    except ValueError:
        lev_val = min(default_lev, max_l)

    # Validate Stop Loss distance against chosen leverage
    if last_snap_price > 0 and pu_val > 0:
        cur_buf_pct = max(0.001, (1.0 / lev_val - mmr_ratio)) * 100
        cur_buf_ticks = int((last_snap_price * (cur_buf_pct / 100)) / pu_val)
        max_safe_sl_ticks = max(2, int(cur_buf_ticks * 0.80))

        user_sl_ticks = None
        if sl_mode_val == "TICKS" and sl_ticks_val:
            user_sl_ticks = sl_ticks_val
        elif sl_mode_val == "PRICE_PCT" and sl_price_val:
            user_sl_ticks = int((last_snap_price * (sl_price_val / 100.0)) / pu_val)
        elif sl_mode_val == "ROE" and sl_roe_val:
            user_sl_ticks = int((last_snap_price * ((sl_roe_val / lev_val) / 100.0)) / pu_val)

        if user_sl_ticks and user_sl_ticks >= cur_buf_ticks:
            print(f"\n   ⚠️  CRITICAL CONFLICT: STOP LOSS BEYOND LIQUIDATION!")
            print(f"   At {lev_val}x leverage, the total liquidation distance is only ~{cur_buf_ticks} ticks!")
            print(f"   Your requested Stop Loss of {user_sl_ticks} ticks cannot be placed without being liquidated first.")
            print(f"   Max safe Stop Loss at {lev_val}x leverage is {max_safe_sl_ticks} ticks.")

            denom = (user_sl_ticks * pu_val / last_snap_price) / 0.80 + mmr_ratio
            safe_lev_for_sl = max(1, min(max_l, int(1.0 / denom))) if denom > 0 else 20
            rec_lev = min(30, max(1, safe_lev_for_sl))
            print(f"   To keep your {user_sl_ticks}-tick Stop Loss, leverage must be reduced to <= {safe_lev_for_sl}x (e.g. {rec_lev}x).")

            print("\n   Resolution Options:")
            print(f"   [1] Keep {lev_val}x leverage and tighten SL to safe max ({max_safe_sl_ticks} ticks) [Recommended]")
            print(f"   [2] Reduce leverage to {rec_lev}x (keeps your full {user_sl_ticks}-tick SL)")
            res_choice = input(f"   Select option [default: 1 (Keep {lev_val}x leverage)]: ").strip()
            if res_choice == "2":
                lev_val = rec_lev
                print(f"   ✓ Leverage set to {lev_val}x (retaining your {user_sl_ticks}-tick Stop Loss with safe buffer).")
            else:
                sl_mode_val = "TICKS"
                sl_ticks_val = max_safe_sl_ticks
                sl_roe_val = None
                sl_price_val = None
                print(f"   ✓ Kept {lev_val}x leverage! Stop loss safely clamped to {max_safe_sl_ticks} ticks.")

    # 7b. Order Execution Style, Ratchet & Slippage Protection
    default_exec_style = get_setting("EXECUTION_STYLE", "MAKER_HYBRID").upper()
    print("\n7b. Order Execution Style & Slippage Protection:")
    print("   [1] MAKER_HYBRID -> Post-Only Maker limit at bid1/ask1 (10s timeout) + Resting Limit TP [Default]")
    print("   [2] PURE_MARKET  -> Immediate taker execution")
    def_exec_num = "1" if default_exec_style == "MAKER_HYBRID" else "2"
    ot_str = input(f"   Select Execution Style [default: {def_exec_num} ({default_exec_style})]: ").strip()
    if ot_str in ("2", "market", "pure_market"):
        execution_style_val = "PURE_MARKET"
        order_type_val = "MARKET"
    else:
        execution_style_val = "MAKER_HYBRID"
        order_type_val = "LIMIT"

    # Tick Ratchet
    default_ratchet = get_setting("RATCHET_ENABLED", True)
    print("\n   Phase V2.2 Champion Micro-Excursion Tick Ratchet:")
    print("   • Dynamic in-position trailing protection based on millisecond excursion (MFE)")
    print("   • Tier 1: When MFE >= +1.0t and position stalls >= 10s -> Tightens SL to -1.0t")
    print("   • Tier 2: When MFE >= +2.5t -> Locks SL to Breakeven (0.0t)")
    def_r_str = "Y/n" if default_ratchet else "y/N"
    r_in = input(f"   Enable Tick Ratchet? [{def_r_str}]: ").strip().lower()
    if r_in in ("y", "yes", "1"):
        ratchet_enabled_val = True
    elif r_in in ("n", "no", "0"):
        ratchet_enabled_val = False
    else:
        ratchet_enabled_val = default_ratchet

    # Slippage simulation (primarily for Dry-Run)
    default_slip_en = get_setting("SLIPPAGE_ENABLED", False)
    default_slip_t = get_setting("SLIPPAGE_TICKS", 0)
    print("\n   Adverse Slippage Simulation Engine:")
    print("   Simulates realistic microsecond spread crossing & queue latency penalties (useful in Dry-Run).")
    def_slip_str = "Y/n" if default_slip_en else "y/N"
    s_in = input(f"   Enable Adverse Slippage Engine? [{def_slip_str}]: ").strip().lower()
    if s_in in ("y", "yes", "1"):
        slippage_enabled_val = True
        st_in = input(f"   Adverse slippage distance in ticks [default: {default_slip_t or 1}]: ").strip()
        slippage_ticks_val = int(st_in) if st_in.isdigit() else (default_slip_t or 1)
    elif s_in in ("n", "no", "0"):
        slippage_enabled_val = False
        slippage_ticks_val = 0
    else:
        slippage_enabled_val = default_slip_en
        slippage_ticks_val = default_slip_t

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

    # 10. Trade Optimization & Regime Filters
    print("\n10. Trade Optimization & Regime Filters:")
    print("   [1] Baseline / Disabled (Standard raw strategy execution) [Default]")
    print("   [2] Enable Duration Time-Stop (Monitor >60s, Auto-Exit at 90s)")
    print("   [3] Enable Full Institutional Safeguards (Duration + HTF 200 EMA + ADX + Hourly)")
    print("   [4] Custom Filter Configuration")
    filter_choice = input("   Select Filter Mode [default: 1 (Baseline / Disabled)]: ").strip()

    dur_enabled = get_setting("DURATION_FILTER_ENABLED", False)
    dur_deep_s = get_setting("DURATION_DEEP_MONITOR_SECONDS", 60.0)
    dur_max_s = get_setting("DURATION_MAX_HOLD_SECONDS", 90.0)
    dur_act = get_setting("DURATION_ACTION", "CLOSE")
    adx_enabled = get_setting("ADX_FILTER_ENABLED", False)
    adx_per = get_setting("ADX_PERIOD", 14)
    adx_thresh = get_setting("ADX_THRESHOLD", 25.0)
    htf_enabled = get_setting("HTF_TREND_FILTER_ENABLED", False)
    htf_per = get_setting("HTF_EMA_PERIOD", 200)
    htf_tf = get_setting("HTF_TIMEFRAME", "15m")
    hourly_enabled = get_setting("HOURLY_FILTER_ENABLED", False)
    hourly_bl = get_setting("HOURLY_BLACKLIST_UTC", [2, 3, 4, 5, 17])
    dir_bias = get_setting("DIRECTION_BIAS", "BOTH")

    if filter_choice == "2":
        dur_enabled = True
    elif filter_choice == "3":
        dur_enabled = True
        adx_enabled = True
        htf_enabled = True
        hourly_enabled = True
        hourly_bl = [2, 3, 4, 5, 17]
    elif filter_choice == "4":
        d_in = input("   Enable Duration Filter? [y/N]: ").strip().lower()
        if d_in in ("y", "yes", "1"):
            dur_enabled = True
            hold_in = input(f"   Max hold seconds [default: {dur_max_s}]: ").strip()
            dur_max_s = float(hold_in) if hold_in else dur_max_s
            act_in = input(f"   Action on timeout (CLOSE / SCRATCH_OR_MARKET / TIGHTEN_SL) [default: {dur_act}]: ").strip().upper()
            dur_act = act_in if act_in in ("CLOSE", "SCRATCH_OR_MARKET", "TIGHTEN_SL") else dur_act
        h_in = input("   Enable HTF 200 EMA Trend Filter? [y/N]: ").strip().lower()
        if h_in in ("y", "yes", "1"):
            htf_enabled = True
        a_in = input("   Enable ADX Chop Filter? [y/N]: ").strip().lower()
        if a_in in ("y", "yes", "1"):
            adx_enabled = True
        hr_in = input("   Enable Hourly Session Blacklist? [y/N]: ").strip().lower()
        if hr_in in ("y", "yes", "1"):
            hourly_enabled = True
            bl_in = input("   Comma-separated UTC hours to block [default: 2,3,4,5,17]: ").strip()
            hourly_bl = [int(x.strip()) for x in bl_in.split(",") if x.strip().isdigit()] if bl_in else [2, 3, 4, 5, 17]
        bias_in = input(f"   Directional Bias (BOTH / LONG_ONLY / SHORT_ONLY) [default: {dir_bias}]: ").strip().upper()
        if bias_in in ("LONG_ONLY", "SHORT_ONLY", "BOTH"):
            dir_bias = bias_in

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
        dynamic_tp=dynamic_tp_val,
        sl_mode=sl_mode_val,
        sl_roe_pct=sl_roe_val,
        sl_ticks=sl_ticks_val,
        sl_price_pct=sl_price_val,
        max_trades=max_val,
        strategy_mode=strat_mode_val,
        bi_directional=bi_directional_val,
        ema_preset=ema_preset_val,
        ema_fast=ema_fast_val,
        ema_slow=ema_slow_val,
        ema_interval=ema_interval_val,
        ema_require_closed_candle=get_setting("EMA_REQUIRE_CLOSED_CANDLE", True),
        stoch_preset=stoch_preset_val,
        stoch_rsi_period=stoch_rsi_p_val,
        stoch_period=stoch_p_val,
        stoch_k_period=stoch_k_val,
        stoch_d_period=stoch_d_val,
        stoch_oversold=stoch_os_val,
        stoch_overbought=stoch_ob_val,
        stoch_interval=stoch_interval_val,
        stoch_zone_filter=stoch_zone_val,
        stoch_require_closed_candle=get_setting("STOCH_REQUIRE_CLOSED_CANDLE", True),
        duration_filter_enabled=dur_enabled,
        duration_deep_monitor_seconds=dur_deep_s,
        duration_max_hold_seconds=dur_max_s,
        duration_action=dur_act,
        adx_filter_enabled=adx_enabled,
        adx_period=adx_per,
        adx_threshold=adx_thresh,
        htf_trend_filter_enabled=htf_enabled,
        htf_timeframe=htf_tf,
        htf_ema_period=htf_per,
        hourly_filter_enabled=hourly_enabled,
        hourly_blacklist_utc=hourly_bl,
        direction_bias=dir_bias,
        order_type=order_type_val,
        limit_order_timeout_seconds=get_setting("LIMIT_ORDER_TIMEOUT_SECONDS", 10.0),
        smart_atr_filter_enabled=get_setting("SMART_ATR_FILTER_ENABLED", True),
        smart_min_atr_ticks=get_setting("SMART_MIN_ATR_TICKS", 2.5),
        smart_chop_ceiling=get_setting("SMART_CHOP_CEILING", 58.0),
        smart_adx_trend_threshold=get_setting("SMART_ADX_TREND_THRESHOLD", 26.0),
        smart_use_ema200_filter=get_setting("SMART_USE_EMA200_FILTER", False),
        smart_climax_filter_enabled=get_setting("SMART_CLIMAX_FILTER_ENABLED", True),
        smart_max_atr_expansion=get_setting("SMART_MAX_ATR_EXPANSION", 2.2),
        smart_ema_preset=get_setting("SMART_EMA_PRESET", "5/13"),
        smart_stoch_preset=get_setting("SMART_STOCH_PRESET", "FAST_SCALP"),
        smart_interval=get_setting("SMART_INTERVAL", "Min1"),
        smart_require_closed_candle=get_setting("SMART_REQUIRE_CLOSED_CANDLE", True),
        invert_signal=invert_signal_val,
        dynamic_regime_fading=get_setting("DYNAMIC_REGIME_FADING", False),
        adx_fading_cutoff=get_setting("ADX_FADING_CUTOFF", 25.0),
        execution_style=execution_style_val,
        maker_queue_timeout_seconds=get_setting("MAKER_QUEUE_TIMEOUT_SECONDS", 10.0),
        resting_limit_tp=(execution_style_val == "MAKER_HYBRID"),
        ratchet_enabled=ratchet_enabled_val,
        ratchet_trigger_ticks=get_setting("RATCHET_TRIGGER_TICKS", 1.0),
        ratchet_stall_seconds=get_setting("RATCHET_STALL_SECONDS", 10.0),
        ratchet_tighten_ticks=get_setting("RATCHET_TIGHTEN_TICKS", 1.0),
        ratchet_breakeven_ticks=get_setting("RATCHET_BREAKEVEN_TICKS", 2.5),
        slippage_enabled=slippage_enabled_val,
        slippage_ticks=slippage_ticks_val,
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
        "--strategy",
        type=str,
        choices=[
            "ema", "ema_crossover", "EMA", "EMA_CROSSOVER",
            "stoch_rsi", "stochastic_rsi", "STOCH_RSI", "STOCHASTIC_RSI", "stoch", "STOCH",
            "smart", "smart_strategy", "SMART", "SMART_STRATEGY",
            "microstructure", "cycle", "MICROSTRUCTURE", "CYCLE"
        ],
        default=None,
        help="Strategy type: 'smart_strategy' [3], 'ema_crossover' [1], 'stoch_rsi' [2]"
    )
    parser.add_argument(
        "--order-type",
        type=str,
        choices=["MARKET", "LIMIT", "market", "limit"],
        default=None,
        help="Order execution type: 'MARKET' (taker fill) or 'LIMIT' (post-only maker fill)"
    )
    parser.add_argument(
        "--limit-timeout",
        type=float,
        default=None,
        help="Timeout in seconds for unfilled limit order cancellation (default: 10.0)"
    )
    parser.add_argument(
        "--smart-atr-filter",
        action="store_true",
        default=None,
        help="Enable/disable Smart Strategy ATR compression filter"
    )
    parser.add_argument(
        "--smart-min-atr-ticks",
        type=float,
        default=None,
        help="Minimum ATR in ticks for Smart Strategy entry (default: 2.5)"
    )
    parser.add_argument(
        "--smart-chop-ceiling",
        type=float,
        default=None,
        help="Choppiness Index ceiling for Smart Strategy (default: 58.0)"
    )
    parser.add_argument(
        "--smart-adx-trend-threshold",
        type=float,
        default=None,
        help="ADX momentum threshold for Smart Strategy (default: 26.0)"
    )
    parser.add_argument(
        "--smart-ema200-filter",
        action="store_true",
        default=None,
        help="Enable 200 EMA direction lock on Smart Strategy (default: False)"
    )
    parser.add_argument(
        "--smart-climax-filter",
        action="store_true",
        default=None,
        help="Enable volatility climax filter on Smart Strategy (default: True)"
    )
    parser.add_argument(
        "--smart-max-atr-expansion",
        type=float,
        default=None,
        help="Max candle range expansion vs ATR for climax filter (default: 2.2)"
    )
    parser.add_argument(
        "--ema-preset",
        type=str,
        choices=["5/13", "9/21", "3/8", "custom"],
        default=None,
        help="EMA Crossover Preset: '5/13' (Fibonacci scalp, default), '9/21' (momentum/trend), or '3/8' (ultra-fast micro-scalp)"
    )
    parser.add_argument(
        "--ema-fast",
        type=int,
        default=None,
        help="Fast EMA period length (default: 5 or derived from --ema-preset)"
    )
    parser.add_argument(
        "--ema-slow",
        type=int,
        default=None,
        help="Slow EMA period length (default: 13 or derived from --ema-preset)"
    )
    parser.add_argument(
        "--ema-interval",
        type=str,
        default=None,
        help="Candle timeframe for EMA: 'Min1' (default), 'Min5', 'Min15', etc."
    )
    parser.add_argument(
        "--stoch-preset",
        type=str,
        choices=["FAST_SCALP", "STANDARD", "MICRO_BURST", "custom", "fast_scalp", "standard", "micro_burst"],
        default=None,
        help="Stochastic RSI Preset: 'FAST_SCALP' (9/9/3/3, default), 'STANDARD' (14/14/3/3), or 'MICRO_BURST' (7/7/3/3)"
    )
    parser.add_argument(
        "--stoch-rsi-period",
        type=int,
        default=None,
        help="Stochastic RSI - RSI calculation period (default: 9)"
    )
    parser.add_argument(
        "--stoch-period",
        type=int,
        default=None,
        help="Stochastic RSI - Stochastic lookback period (default: 9)"
    )
    parser.add_argument(
        "--stoch-k",
        type=int,
        default=None,
        help="Stochastic RSI - %%K smoothing period (default: 3)"
    )
    parser.add_argument(
        "--stoch-d",
        type=int,
        default=None,
        help="Stochastic RSI - %%D smoothing period (default: 3)"
    )
    parser.add_argument(
        "--stoch-oversold",
        type=float,
        default=None,
        help="Stochastic RSI - Oversold zone threshold (default: 20.0)"
    )
    parser.add_argument(
        "--stoch-overbought",
        type=float,
        default=None,
        help="Stochastic RSI - Overbought zone threshold (default: 80.0)"
    )
    parser.add_argument(
        "--stoch-interval",
        type=str,
        default=None,
        help="Candle timeframe for StochRSI: 'Min1' (default), 'Min5', 'Min15', etc."
    )
    parser.add_argument(
        "--no-stoch-zone-filter",
        action="store_true",
        help="Disable StochRSI oversold/overbought zone filter (trade all crossovers)"
    )
    parser.add_argument(
        "--intra-bar-ema",
        action="store_true",
        help="Evaluate EMA crossover in real-time mid-bar instead of requiring closed candle confirmation"
    )
    parser.add_argument(
        "--require-closed-candle",
        action="store_true",
        default=None,
        help="Strictly confirm EMA crossover on closed candle (prevents false whipsaw repainting, default: True)"
    )
    parser.add_argument(
        "--bi-directional",
        action="store_true",
        default=None,
        help="Enable autonomous bi-directional trading (LONG and SHORT) for EMA or microstructure strategy"
    )
    parser.add_argument(
        "--single-direction",
        action="store_true",
        help="Restrict trading strictly to --direction"
    )
    parser.add_argument(
        "--dynamic-tp",
        action="store_true",
        default=None,
        help="Enable dynamic Take-Profit scaling (1 to 3 pu ticks based on signal strength)"
    )
    parser.add_argument(
        "--fixed-tp",
        action="store_true",
        help="Strictly lock Take-Profit to --tp-ticks (disable dynamic scaling)"
    )
    # Trade Optimization & Regime Filter Flags
    parser.add_argument(
        "--duration-filter",
        action="store_true",
        default=None,
        help="Enable trade duration monitoring and time-decay exits"
    )
    parser.add_argument(
        "--duration-deep-monitor",
        type=float,
        default=None,
        help="Seconds before deep monitoring engages (default: 60.0)"
    )
    parser.add_argument(
        "--duration-max-hold",
        type=float,
        default=None,
        help="Maximum allowed trade hold duration in seconds (default: 90.0)"
    )
    parser.add_argument(
        "--duration-action",
        type=str,
        choices=["CLOSE", "SCRATCH_OR_MARKET", "TIGHTEN_SL"],
        default=None,
        help="Action on max duration timeout (default: CLOSE)"
    )
    parser.add_argument(
        "--adx-filter",
        action="store_true",
        default=None,
        help="Enable ADX chop suppression filter"
    )
    parser.add_argument(
        "--adx-threshold",
        type=float,
        default=None,
        help="Minimum ADX required to allow trade entry (default: 25.0)"
    )
    parser.add_argument(
        "--htf-trend-filter",
        action="store_true",
        default=None,
        help="Enable Higher-Timeframe 200 EMA trend baseline filter"
    )
    parser.add_argument(
        "--hourly-filter",
        action="store_true",
        default=None,
        help="Enable UTC hourly session blacklist"
    )
    parser.add_argument(
        "--direction-bias",
        type=str,
        choices=["BOTH", "LONG_ONLY", "SHORT_ONLY"],
        default=None,
        help="Enforce directional bias: BOTH, LONG_ONLY, or SHORT_ONLY"
    )
    # Phase V2.1 & V2.2 Quantitative Research Presets & Toggles
    parser.add_argument(
        "--preset",
        type=str,
        default=None,
        help="Strategy Preset: 'DOGE_V2_2_RATCHET_CHAMPION', 'DOGE_ASYMMETRIC_MOMENTUM_10T2T', 'TRUMP_LEGACY_BASELINE', or 'CUSTOM'"
    )
    parser.add_argument(
        "--invert-signal",
        action="store_true",
        default=None,
        help="Invert Stoch RSI signal direction (Exhaustion Fading mode)"
    )
    parser.add_argument(
        "--no-invert-signal",
        action="store_false",
        dest="invert_signal",
        help="Use direct Stoch RSI signal direction (Momentum Breakout mode)"
    )
    parser.add_argument(
        "--ratchet",
        action="store_true",
        dest="ratchet_enabled",
        default=None,
        help="Enable Phase V2.2 Champion Micro-Excursion Tick Ratchet (+1.0t/10s -> -1t, +2.5t -> BE)"
    )
    parser.add_argument(
        "--no-ratchet",
        action="store_false",
        dest="ratchet_enabled",
        help="Disable Tick Ratchet trailing stop"
    )
    parser.add_argument(
        "--ratchet-trigger-ticks",
        type=float,
        default=None,
        help="MFE in ticks required for Ratchet Tier 1 tightening (default: 1.0)"
    )
    parser.add_argument(
        "--ratchet-stall-seconds",
        type=float,
        default=None,
        help="Hold duration stall in seconds for Ratchet Tier 1 tightening (default: 10.0)"
    )
    parser.add_argument(
        "--ratchet-tighten-ticks",
        type=float,
        default=None,
        help="Tightened SL distance in ticks (default: 1.0)"
    )
    parser.add_argument(
        "--ratchet-breakeven-ticks",
        type=float,
        default=None,
        help="MFE in ticks required for Ratchet Tier 2 Breakeven lock (default: 2.5)"
    )
    parser.add_argument(
        "--execution-style",
        type=str,
        choices=["PURE_MARKET", "MAKER_HYBRID", "pure_market", "maker_hybrid"],
        default=None,
        help="Execution style: 'MAKER_HYBRID' (maker limit entry + resting TP) or 'PURE_MARKET' (taker)"
    )
    parser.add_argument(
        "--enable-slippage",
        action="store_true",
        dest="slippage_enabled",
        default=None,
        help="Enable adverse order execution slippage engine"
    )
    parser.add_argument(
        "--disable-slippage",
        action="store_false",
        dest="slippage_enabled",
        help="Disable adverse order execution slippage engine"
    )
    parser.add_argument(
        "--slippage-ticks",
        type=int,
        default=None,
        help="Integer ticks of adverse friction (e.g. 1, 2, 3)"
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
        # Resolve active strategy preset
        active_preset_name = (args.preset or get_setting("ACTIVE_PRESET", "DOGE_V2_2_RATCHET_CHAMPION")).upper()
        preset_cfg = {}
        if hasattr(settings, "get_active_preset_config"):
            preset_cfg = settings.get_active_preset_config(active_preset_name)

        # Read from flags or fall back to preset / settings.py
        sym = (args.symbol or preset_cfg.get("symbol") or get_setting("SYMBOL", "TRUMP_USDT")).upper()
        dir_raw = (args.direction or get_setting("DIRECTION", "LONG")).upper()
        mode_raw = (args.mode or get_setting("MODE", "live")).lower()

        dir_enum = OrderDirection.LONG if dir_raw == "LONG" else OrderDirection.SHORT
        mode_enum = EngineMode.LIVE if mode_raw == "live" else EngineMode.DRY_RUN

        vol_mode = (args.volume_mode or get_setting("VOLUME_MODE", "MULTIPLIER")).upper()
        if args.volume_multiplier is not None:
            vol_mult = args.volume_multiplier
        elif hasattr(settings, "get_default_quantity_for_symbol"):
            _, vol_mult = settings.get_default_quantity_for_symbol(sym)
        elif "TRUMP" in sym:
            vol_mult = 2.0
        elif "DOGE" in sym:
            vol_mult = 1.0
        else:
            vol_mult = get_setting("VOLUME_MULTIPLIER", 2.0)

        vol_contracts = args.volume_contracts if args.volume_contracts is not None else (get_setting("VOLUME_CONTRACTS", 2) if vol_mode == "CONTRACTS" else None)

        tp_ticks = args.tp_ticks if args.tp_ticks is not None else (preset_cfg.get("tp_ticks") if "tp_ticks" in preset_cfg else get_setting("TP_TICKS", 2))
        if args.fixed_tp:
            dynamic_tp = False
        elif args.dynamic_tp:
            dynamic_tp = True
        else:
            dynamic_tp = get_setting("DYNAMIC_TP", False)

        sl_mode = (args.sl_mode or preset_cfg.get("sl_mode") or get_setting("SL_MODE", "ROE")).upper()
        sl_ticks = args.sl_ticks if args.sl_ticks is not None else (preset_cfg.get("sl_ticks") if "sl_ticks" in preset_cfg else (get_setting("SL_TICKS", 10) if sl_mode == "TICKS" else None))
        sl_price_pct = args.sl_price_pct if args.sl_price_pct is not None else (get_setting("SL_PRICE_PCT", 0.5) if sl_mode == "PRICE_PCT" else None)
        sl_roe = args.sl_roe if args.sl_roe is not None else (preset_cfg.get("sl_roe_pct") if "sl_roe_pct" in preset_cfg else get_setting("SL_ROE_PCT", 25.0))

        lev = args.leverage if args.leverage is not None else get_setting("LEVERAGE", 75)
        cooldown = args.cooldown if args.cooldown is not None else get_setting("COOLDOWN_SECONDS", 30.0)
        max_trades = args.max_trades if args.max_trades is not None else get_setting("MAX_TRADES", 3)
        poll_int = args.poll_interval if args.poll_interval is not None else get_setting("POLL_INTERVAL_SECONDS", 0.3)

        strat_raw = (args.strategy or preset_cfg.get("strategy_mode") or get_setting("STRATEGY_MODE", "STOCH_RSI")).upper()
        if args.single_direction:
            bi_directional = False
        elif args.bi_directional:
            bi_directional = True
        else:
            if strat_raw in ("EMA", "EMA_CROSSOVER"):
                bi_directional = get_setting("EMA_BI_DIRECTIONAL", True)
            elif strat_raw in ("STOCH_RSI", "STOCHASTIC_RSI", "STOCH"):
                bi_directional = get_setting("STOCH_BI_DIRECTIONAL", True)
            elif strat_raw in ("SMART", "SMART_STRATEGY"):
                bi_directional = True
            else:
                bi_directional = get_setting("MICRO_BI_DIRECTIONAL", True)

        # Quantitative parameters resolution
        inv_sig = args.invert_signal if args.invert_signal is not None else preset_cfg.get("invert_signal", get_setting("INVERT_SIGNAL", False))
        dyn_fading = preset_cfg.get("dynamic_regime_fading", get_setting("DYNAMIC_REGIME_FADING", False))
        adx_cutoff = preset_cfg.get("adx_fading_cutoff", get_setting("ADX_FADING_CUTOFF", 25.0))
        exec_style = (args.execution_style or preset_cfg.get("execution_style") or get_setting("EXECUTION_STYLE", "PURE_MARKET")).upper()
        maker_timeout = preset_cfg.get("maker_queue_timeout_seconds", get_setting("MAKER_QUEUE_TIMEOUT_SECONDS", 10.0))
        resting_tp = preset_cfg.get("resting_limit_tp", get_setting("RESTING_LIMIT_TP", True))
        ratch_en = args.ratchet_enabled if args.ratchet_enabled is not None else preset_cfg.get("ratchet_enabled", get_setting("RATCHET_ENABLED", False))
        ratch_trig = args.ratchet_trigger_ticks if args.ratchet_trigger_ticks is not None else preset_cfg.get("ratchet_trigger_ticks", get_setting("RATCHET_TRIGGER_TICKS", 1.0))
        ratch_stall = args.ratchet_stall_seconds if args.ratchet_stall_seconds is not None else preset_cfg.get("ratchet_stall_seconds", get_setting("RATCHET_STALL_SECONDS", 10.0))
        ratch_tight = args.ratchet_tighten_ticks if args.ratchet_tighten_ticks is not None else preset_cfg.get("ratchet_tighten_ticks", get_setting("RATCHET_TIGHTEN_TICKS", 1.0))
        ratch_be = args.ratchet_breakeven_ticks if args.ratchet_breakeven_ticks is not None else preset_cfg.get("ratchet_breakeven_ticks", get_setting("RATCHET_BREAKEVEN_TICKS", 2.5))
        slip_en = args.slippage_enabled if args.slippage_enabled is not None else preset_cfg.get("slippage_enabled", get_setting("SLIPPAGE_ENABLED", False))
        slip_ticks = args.slippage_ticks if args.slippage_ticks is not None else preset_cfg.get("slippage_ticks", get_setting("SLIPPAGE_TICKS", 0))

        ema_preset = args.ema_preset or get_setting("EMA_PRESET", "5/13")
        if ema_preset == "9/21":
            def_fast, def_slow = 9, 21
        elif ema_preset == "3/8":
            def_fast, def_slow = 3, 8
        else:
            def_fast, def_slow = 5, 13

        ema_fast = args.ema_fast if args.ema_fast is not None else get_setting("EMA_FAST", def_fast)
        ema_slow = args.ema_slow if args.ema_slow is not None else get_setting("EMA_SLOW", def_slow)
        ema_interval = args.ema_interval or get_setting("EMA_INTERVAL", "Min1")

        if args.intra_bar_ema:
            ema_closed = False
        elif args.require_closed_candle:
            ema_closed = True
        else:
            ema_closed = get_setting("EMA_REQUIRE_CLOSED_CANDLE", True)

        stoch_preset = (args.stoch_preset or get_setting("STOCH_PRESET", "FAST_SCALP")).upper()
        if stoch_preset == "STANDARD":
            def_rsi, def_stoch, def_k, def_d = 14, 14, 3, 3
            def_os, def_ob = 20.0, 80.0
        elif stoch_preset == "MICRO_BURST":
            def_rsi, def_stoch, def_k, def_d = 7, 7, 3, 3
            def_os, def_ob = 15.0, 85.0
        else:
            def_rsi, def_stoch, def_k, def_d = 9, 9, 3, 3
            def_os, def_ob = 20.0, 80.0

        stoch_rsi_period = args.stoch_rsi_period if args.stoch_rsi_period is not None else get_setting("STOCH_RSI_PERIOD", def_rsi)
        stoch_period = args.stoch_period if args.stoch_period is not None else get_setting("STOCH_PERIOD", def_stoch)
        stoch_k_period = args.stoch_k if args.stoch_k is not None else get_setting("STOCH_K_PERIOD", def_k)
        stoch_d_period = args.stoch_d if args.stoch_d is not None else get_setting("STOCH_D_PERIOD", def_d)
        stoch_oversold = args.stoch_oversold if args.stoch_oversold is not None else get_setting("STOCH_OVERSOLD", def_os)
        stoch_overbought = args.stoch_overbought if args.stoch_overbought is not None else get_setting("STOCH_OVERBOUGHT", def_ob)
        stoch_interval = args.stoch_interval or get_setting("STOCH_INTERVAL", "Min1")
        stoch_zone = False if args.no_stoch_zone_filter else get_setting("STOCH_ZONE_FILTER", True)

        order_type_val = (args.order_type or get_setting("ORDER_TYPE", "MARKET")).upper()
        limit_timeout_val = args.limit_timeout if args.limit_timeout is not None else get_setting("LIMIT_ORDER_TIMEOUT_SECONDS", 10.0)

        smart_atr_filter_val = args.smart_atr_filter if args.smart_atr_filter is not None else get_setting("SMART_ATR_FILTER_ENABLED", True)
        smart_min_atr_ticks_val = args.smart_min_atr_ticks if args.smart_min_atr_ticks is not None else get_setting("SMART_MIN_ATR_TICKS", 2.5)
        smart_chop_ceiling_val = args.smart_chop_ceiling if args.smart_chop_ceiling is not None else get_setting("SMART_CHOP_CEILING", 58.0)
        smart_adx_trend_val = args.smart_adx_trend_threshold if args.smart_adx_trend_threshold is not None else get_setting("SMART_ADX_TREND_THRESHOLD", 26.0)
        smart_ema200_val = args.smart_ema200_filter if args.smart_ema200_filter is not None else get_setting("SMART_USE_EMA200_FILTER", False)
        smart_climax_val = args.smart_climax_filter if args.smart_climax_filter is not None else get_setting("SMART_CLIMAX_FILTER_ENABLED", True)
        smart_max_exp_val = args.smart_max_atr_expansion if args.smart_max_atr_expansion is not None else get_setting("SMART_MAX_ATR_EXPANSION", 2.2)
        smart_ema_preset_val = get_setting("SMART_EMA_PRESET", "5/13")
        smart_stoch_preset_val = get_setting("SMART_STOCH_PRESET", "FAST_SCALP")
        smart_interval_val = get_setting("SMART_INTERVAL", "Min1")
        smart_req_closed_val = get_setting("SMART_REQUIRE_CLOSED_CANDLE", True)

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
            dynamic_tp=dynamic_tp,
            sl_mode=sl_mode,
            sl_ticks=sl_ticks,
            sl_price_pct=sl_price_pct,
            sl_roe_pct=sl_roe,
            max_trades=max_trades,
            strategy_mode=strat_raw,
            bi_directional=bi_directional,
            ema_preset=ema_preset,
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            ema_interval=ema_interval,
            ema_require_closed_candle=ema_closed,
            stoch_preset=stoch_preset,
            stoch_rsi_period=stoch_rsi_period,
            stoch_period=stoch_period,
            stoch_k_period=stoch_k_period,
            stoch_d_period=stoch_d_period,
            stoch_oversold=stoch_oversold,
            stoch_overbought=stoch_overbought,
            stoch_interval=stoch_interval,
            stoch_zone_filter=stoch_zone,
            stoch_require_closed_candle=get_setting("STOCH_REQUIRE_CLOSED_CANDLE", True),
            order_type=order_type_val,
            limit_order_timeout_seconds=limit_timeout_val,
            smart_atr_filter_enabled=smart_atr_filter_val,
            smart_min_atr_ticks=smart_min_atr_ticks_val,
            smart_chop_ceiling=smart_chop_ceiling_val,
            smart_adx_trend_threshold=smart_adx_trend_val,
            smart_use_ema200_filter=smart_ema200_val,
            smart_climax_filter_enabled=smart_climax_val,
            smart_max_atr_expansion=smart_max_exp_val,
            smart_ema_preset=smart_ema_preset_val,
            smart_stoch_preset=smart_stoch_preset_val,
            smart_interval=smart_interval_val,
            smart_require_closed_candle=smart_req_closed_val,
            invert_signal=inv_sig,
            dynamic_regime_fading=dyn_fading,
            adx_fading_cutoff=adx_cutoff,
            execution_style=exec_style,
            maker_queue_timeout_seconds=maker_timeout,
            resting_limit_tp=resting_tp,
            ratchet_enabled=ratch_en,
            ratchet_trigger_ticks=ratch_trig,
            ratchet_stall_seconds=ratch_stall,
            ratchet_tighten_ticks=ratch_tight,
            ratchet_breakeven_ticks=ratch_be,
            slippage_enabled=slip_en,
            slippage_ticks=slip_ticks,
            duration_filter_enabled=args.duration_filter if args.duration_filter is not None else get_setting("DURATION_FILTER_ENABLED", False),
            duration_deep_monitor_seconds=args.duration_deep_monitor if args.duration_deep_monitor is not None else get_setting("DURATION_DEEP_MONITOR_SECONDS", 60.0),
            duration_max_hold_seconds=args.duration_max_hold if args.duration_max_hold is not None else get_setting("DURATION_MAX_HOLD_SECONDS", 90.0),
            duration_action=args.duration_action or get_setting("DURATION_ACTION", "CLOSE"),
            adx_filter_enabled=args.adx_filter if args.adx_filter is not None else get_setting("ADX_FILTER_ENABLED", False),
            adx_period=get_setting("ADX_PERIOD", 14),
            adx_threshold=args.adx_threshold if args.adx_threshold is not None else get_setting("ADX_THRESHOLD", 25.0),
            htf_trend_filter_enabled=args.htf_trend_filter if args.htf_trend_filter is not None else get_setting("HTF_TREND_FILTER_ENABLED", False),
            htf_timeframe=get_setting("HTF_TIMEFRAME", "15m"),
            htf_ema_period=get_setting("HTF_EMA_PERIOD", 200),
            hourly_filter_enabled=args.hourly_filter if args.hourly_filter is not None else get_setting("HOURLY_FILTER_ENABLED", False),
            hourly_blacklist_utc=get_setting("HOURLY_BLACKLIST_UTC", [2, 3, 4, 5, 17]),
            direction_bias=args.direction_bias or get_setting("DIRECTION_BIAS", "BOTH"),
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
    is_ema = config.strategy_mode in ("EMA", "EMA_CROSSOVER")
    is_stoch = config.strategy_mode in ("STOCH_RSI", "STOCHASTIC_RSI", "STOCH")
    is_micro = config.strategy_mode == "MICROSTRUCTURE"

    if is_ema:
        preset_info = getattr(config, "ema_preset", "5/13")
        interval_info = getattr(config, "ema_interval", "Min1")
        if config.bi_directional:
            strat_desc = f"EMA Crossover ({preset_info}, {interval_info}) [Autonomous Bi-Directional: LONG & SHORT]"
            bias_desc = "Autonomous (Bi-Directional)"
        else:
            strat_desc = f"EMA Crossover ({preset_info}, {interval_info}) [{config.direction.value} only]"
            bias_desc = config.direction.value
    elif is_stoch:
        preset_info = getattr(config, "stoch_preset", "FAST_SCALP")
        interval_info = getattr(config, "stoch_interval", "Min1")
        os_ob = f"OS:{getattr(config, 'stoch_oversold', 20.0):.0f}/OB:{getattr(config, 'stoch_overbought', 80.0):.0f}"
        if config.bi_directional:
            strat_desc = f"Stochastic RSI ({preset_info}, {interval_info}, {os_ob}) [Autonomous Bi-Directional: LONG & SHORT]"
            bias_desc = "Autonomous (Bi-Directional)"
        else:
            strat_desc = f"Stochastic RSI ({preset_info}, {interval_info}, {os_ob}) [{config.direction.value} only]"
            bias_desc = config.direction.value
    elif is_micro:
        if config.bi_directional:
            strat_desc = "Microstructure (Autonomous Bi-Directional: LONG & SHORT)"
            bias_desc = "Autonomous (Bi-Directional)"
        else:
            strat_desc = f"Microstructure ({config.direction.value} only)"
            bias_desc = config.direction.value
    else:
        strat_desc = f"Directional Cycle ({config.direction.value})"
        bias_desc = config.direction.value

    tp_mode_desc = "(Dynamic via signals: 1-3 pu)" if config.dynamic_tp else f"(Fixed: strictly {config.tp_ticks} pu)"

    print("==============================================================================")
    print("                      CONFIGURED ENGINE PARAMETERS")
    print("==============================================================================")
    preset_label = f"{active_preset_name}" if "active_preset_name" in locals() else get_setting("ACTIVE_PRESET", "DOGE_V2_2_RATCHET_CHAMPION")
    print(f"  • Strategy Preset   : {preset_label}")
    print(f"  • Symbol & Mode     : {config.symbol} | {config.mode.value.upper()} | Direction: {bias_desc}")
    print(f"  • Strategy Engine   : {strat_desc}")
    sig_mode_str = "INVERTED (Exhaustion Fading)" if getattr(config, "invert_signal", False) else "DIRECT (Momentum)"
    print(f"  • Signal Paradigm   : {sig_mode_str}")
    print(f"  • Execution Style   : {getattr(config, 'execution_style', 'PURE_MARKET')}")
    ratch_desc = (
        f"ENABLED (T1: +{config.ratchet_trigger_ticks:g}t/{config.ratchet_stall_seconds:.0f}s -> -{config.ratchet_tighten_ticks:g}t, T2: +{config.ratchet_breakeven_ticks:g}t -> BE)"
        if getattr(config, "ratchet_enabled", False)
        else "DISABLED"
    )
    print(f"  • Tick Ratchet      : {ratch_desc}")
    slip_desc = (
        f"ENABLED ({config.slippage_ticks} ticks adverse)"
        if (getattr(config, "slippage_enabled", False) and config.slippage_ticks > 0)
        else "DISABLED (0 ticks)"
    )
    print(f"  • Slippage Engine   : {slip_desc}")
    print(f"  • Target Leverage   : {config.leverage}x isolated")
    print(f"  • Trade Quantity    : {vol_desc}")
    print(f"    ⚠️  CRITICAL NOTE : Trade Quantity (Volume) != Margin!")
    print(f"                       Margin deducted = Trade Quantity / {config.leverage}x leverage")
    print(f"  • Min-Profit TP     : +{config.tp_ticks} pu ticks {tp_mode_desc}")
    print(f"  • Stop Loss         : -{sl_desc}")
    print(f"  • Cooldown          : {config.cooldown_seconds}s | Max Trades: {'Unlimited' if config.max_trades == 0 else config.max_trades}")
    print("==============================================================================\n")


    engine = TradeExecutionEngine(config=config)
    engine.run()


if __name__ == "__main__":
    main()
