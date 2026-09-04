#!/usr/bin/env python3
"""
KCEX Semi-Autonomous Trade Execution Script
===========================================
Interactive, semi-automated trading tool for KCEX Futures contracts.

Workflow:
1. Interactive Setup: Select pair, direction (Long/Short), position size (contracts,
   margin, notional, or coins), and TP/SL (ticks, ROI %, price %, or absolute price).
2. Autonomous Trade Execution & Monitoring:
   - Submits the order to KCEX (Live or Dry-Run).
   - Monitors the position in real time with a live animated terminal dashboard.
   - Ensures TP hit: executes an immediate market close when target price is touched.
   - Monitors server-side stop orders and position status.
   - Emergency hotkey: press 'C' to instantly market close at any time.
3. Post-Trade Reporting:
   - Dual-currency (USDT & INR) PnL calculation, ROE %, duration, and exit reason.
   - Live balance updates.
4. Fast Next-Trade Presets:
   - Remembers all settings (symbol, leverage, quantity, TP, SL).
   - For consecutive trades, choose to continue with previous settings and simply
     select the Direction (Long/Short), or tweak any parameter.

Usage:
    python semi_auto_trader.py
    python semi_auto_trader.py --mode dry-run
    python semi_auto_trader.py --mode live
"""

import os
import sys
import time
import math
import argparse
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple

# Enable utf-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load defaults from settings.py if available
try:
    import settings
except ImportError:
    settings = None

from kcex.config import KCEXConfig
from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator
from kcex.trade import KCEXTrader
from kcex.engine.models import OrderDirection, ExitReason, EngineMode

# Non-blocking keyboard check for Windows
try:
    import msvcrt
except ImportError:
    msvcrt = None


# =============================================================================
# TERMINAL COLORS & FORMATTING
# =============================================================================

class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_GREEN = "\033[42m\033[30m"
    BG_RED = "\033[41m\033[37m"
    BG_CYAN = "\033[46m\033[30m"


def colorize(text: str, color_code: str) -> str:
    return f"{color_code}{text}{Style.RESET}"


def print_banner(mode: EngineMode):
    banner = (
        f"{Style.CYAN}{Style.BOLD}==============================================================================\n"
        r"   _  _______ _______  __  ____ _____ __  __ ___      ___  __  ___________  ____" "\n"
        r"  / |/ / ___// __/ _ \/ / / / // / _ / / / // _ \    / _ \/ / / /_  __/ _ \/ __/" "\n"
        r" /    / /__ / _// // / /_/ / _  / __ / /_/ // // /_  / ___/ /_/ / / / / // /\ \  " "\n"
        r"/_/|_/\___//___/____/\____/_//_/_/ |_\____//____/(_) /_/   \____/ /_/  \___/___/  " "\n"
        "        SEMI-AUTONOMOUS TRADE EXECUTION SUITE - KCEX FUTURES\n"
        f"=============================================================================={Style.RESET}"
    )
    print(banner)

    if mode == EngineMode.LIVE:
        print(f"{Style.BG_RED}  🔴 LIVE REAL TRADING MODE  {Style.RESET} {Style.RED}{Style.BOLD}- Real funds at risk on KCEX exchange!{Style.RESET}\n")
    else:
        print(f"{Style.BG_GREEN}  🟢 SIMULATED DRY-RUN MODE  {Style.RESET} {Style.GREEN}{Style.BOLD}- Zero risk, real-time live market feed.{Style.RESET}\n")


# =============================================================================
# DATA STRUCTURES & SESSION PRESETS
# =============================================================================

@dataclass
class TradePreset:
    """Stores trade configuration for fast presets in consecutive trades."""
    symbol: str = "TRUMP_USDT"
    leverage: int = 30
    is_isolated: bool = True
    # Quantity configuration:
    # "CONTRACTS", "MARGIN_USDT", "NOTIONAL_USDT", "COIN_QTY"
    qty_mode: str = "CONTRACTS"
    qty_val: float = 1.0
    # TP configuration:
    # "TICKS", "ROE_PCT", "PRICE_PCT", "ABSOLUTE"
    tp_mode: str = "TICKS"
    tp_val: float = 3.0
    # SL configuration:
    # "ROE_PCT", "TICKS", "PRICE_PCT", "ABSOLUTE", "NONE"
    sl_mode: str = "ROE_PCT"
    sl_val: Optional[float] = 15.0
    # Execution mode
    mode: EngineMode = EngineMode.LIVE

    def summary_lines(self) -> list[str]:
        tp_desc = f"{self.tp_val:g} ticks" if self.tp_mode == "TICKS" else f"{self.tp_val:g}% ROE" if self.tp_mode == "ROE_PCT" else f"{self.tp_val:g}% price move" if self.tp_mode == "PRICE_PCT" else f"{self.tp_val:g} USDT"
        sl_desc = f"{self.sl_val:g}% ROE" if self.sl_mode == "ROE_PCT" else f"{self.sl_val:g} ticks" if self.sl_mode == "TICKS" else f"{self.sl_val:g}% price move" if self.sl_mode == "PRICE_PCT" else f"{self.sl_val:g} USDT" if self.sl_mode == "ABSOLUTE" else "None"
        
        qty_desc = f"{int(self.qty_val)} contract(s)" if self.qty_mode == "CONTRACTS" else f"{self.qty_val:g} USDT Margin" if self.qty_mode == "MARGIN_USDT" else f"{self.qty_val:g} USDT Notional" if self.qty_mode == "NOTIONAL_USDT" else f"{self.qty_val:g} Coins"

        return [
            f"  • Pair / Symbol : {colorize(self.symbol, Style.BOLD)}",
            f"  • Leverage      : {colorize(f'{self.leverage}x Isolated', Style.YELLOW)}",
            f"  • Position Size : {colorize(qty_desc, Style.CYAN)}",
            f"  • Take Profit   : {colorize(tp_desc, Style.GREEN)} ({self.tp_mode})",
            f"  • Stop Loss     : {colorize(sl_desc, Style.RED)} ({self.sl_mode})"
        ]


# =============================================================================
# INTERACTIVE SETUP HELPERS
# =============================================================================

def get_setting_default(name: str, fallback: Any) -> Any:
    if settings and hasattr(settings, name):
        return getattr(settings, name)
    return fallback


def init_default_preset(config: KCEXConfig) -> TradePreset:
    """Generates initial preset from settings.py or smart defaults."""
    default_mode_str = str(get_setting_default("MODE", "live")).lower()
    mode = EngineMode.LIVE if (default_mode_str == "live" and config.is_authenticated) else EngineMode.DRY_RUN

    default_sym = str(get_setting_default("SYMBOL", "TRUMP_USDT")).upper()
    default_lev = int(get_setting_default("LEVERAGE", 30))
    default_tp = float(get_setting_default("TP_TICKS", 3))
    
    # Qty defaults
    vol_mode = str(get_setting_default("VOLUME_MODE", "CONTRACTS")).upper()
    if vol_mode == "CONTRACTS":
        qty_mode = "CONTRACTS"
        qty_val = float(get_setting_default("VOLUME_CONTRACTS", 1))
    elif vol_mode == "MULTIPLIER":
        qty_mode = "CONTRACTS"
        qty_val = float(get_setting_default("VOLUME_MULTIPLIER", 1.0))
    else:
        qty_mode = "CONTRACTS"
        qty_val = 1.0

    # SL defaults
    sl_mode = str(get_setting_default("SL_MODE", "ROE")).upper()
    if sl_mode == "TICKS":
        sl_m = "TICKS"
        sl_v = float(get_setting_default("SL_TICKS", 10))
    elif sl_mode in ("PRICE_PCT", "PRICE"):
        sl_m = "PRICE_PCT"
        sl_v = float(get_setting_default("SL_PRICE_PCT", 0.5))
    elif sl_mode == "NONE":
        sl_m = "NONE"
        sl_v = None
    else:
        sl_m = "ROE_PCT"
        sl_v = float(get_setting_default("SL_ROE_PCT", 15.0))

    return TradePreset(
        symbol=default_sym,
        leverage=default_lev,
        is_isolated=True,
        qty_mode=qty_mode,
        qty_val=qty_val,
        tp_mode="TICKS",
        tp_val=default_tp,
        sl_mode=sl_m,
        sl_val=sl_v,
        mode=mode
    )


# =============================================================================
# INPUT PROMPT FUNCTIONS
# =============================================================================

def prompt_direction() -> OrderDirection:
    """Prompts for trade direction (LONG / SHORT)."""
    print(f"\n{Style.BOLD}[1] Select Direction:{Style.RESET}")
    print(f"    {Style.GREEN}1. LONG  (BUY){Style.RESET}   - Profit as market moves UP")
    print(f"    {Style.RED}2. SHORT (SELL){Style.RESET}  - Profit as market moves DOWN")
    while True:
        choice = input(f"Select direction [1/2] (Default 1: LONG): ").strip()
        if choice in ("", "1", "long", "LONG", "l", "L", "b", "B", "buy", "BUY"):
            return OrderDirection.LONG
        if choice in ("2", "short", "SHORT", "s", "S", "sell", "SELL"):
            return OrderDirection.SHORT
        print(colorize("Invalid choice. Please enter 1 for LONG or 2 for SHORT.", Style.YELLOW))


def prompt_symbol(market: KCEXMarket, current_symbol: str) -> str:
    """Prompts for trading symbol and validates against KCEX contracts."""
    print(f"\n{Style.BOLD}[2] Trading Pair:{Style.RESET}")
    print(f"    (Examples: TRUMP_USDT, DOGE_USDT, BTC_USDT, ETH_USDT, SOL_USDT, PEPE_USDT)")
    while True:
        val = input(f"Trading Symbol [{current_symbol}]: ").strip().upper()
        sym = val if val else current_symbol
        try:
            contract = market.get_contract_detail(sym)
            fee_tag = f"{Style.GREEN}(0% Fee Pair!){Style.RESET}" if (contract.maker_fee_rate == 0 and contract.taker_fee_rate == 0) else f"(Maker: {contract.maker_fee_rate*100:.2f}%, Taker: {contract.taker_fee_rate*100:.2f}%)"
            print(f"    {Style.GREEN}✓ Verified {sym}{Style.RESET} | Min Vol: {contract.min_volume} contracts | 1 contract = {contract.contract_size} {contract.base_coin} | Tick (pu): {contract.price_unit} USDT {fee_tag}")
            return sym
        except Exception as e:
            print(colorize(f"Invalid symbol or failed to fetch contract info for '{sym}': {e}. Try again.", Style.YELLOW))


def prompt_leverage(contract: ContractInfo, current_leverage: int) -> int:
    """Prompts for leverage, constrained to contract limits."""
    print(f"\n{Style.BOLD}[3] Leverage Multiplier:{Style.RESET}")
    print(f"    Allowed range for {contract.symbol}: {contract.min_leverage}x to {contract.max_leverage}x")
    safe_default = min(max(contract.min_leverage, current_leverage), contract.max_leverage)
    while True:
        val = input(f"Leverage Multiplier [{safe_default}]: ").strip()
        if not val:
            return safe_default
        try:
            lev = int(val)
            if contract.min_leverage <= lev <= contract.max_leverage:
                return lev
            print(colorize(f"Leverage must be between {contract.min_leverage} and {contract.max_leverage}.", Style.YELLOW))
        except ValueError:
            print(colorize("Please enter a valid integer for leverage.", Style.YELLOW))


def prompt_quantity(
    contract: ContractInfo,
    market: KCEXMarket,
    risk: KCEXRiskCalculator,
    leverage: int,
    current_qty_mode: str,
    current_qty_val: float
) -> Tuple[str, float, int]:
    """
    Prompts for position quantity via multiple options:
    Returns (qty_mode, qty_val, computed_vol_contracts).
    """
    ticker = market.get_ticker(contract.symbol)
    cur_price = float(ticker.get("lastPrice", 1.0) or 1.0)
    inr_rate = market.get_inr_rate()
    one_contract_notional = contract.contract_size * cur_price
    one_contract_margin = one_contract_notional / leverage

    print(f"\n{Style.BOLD}[4] Position Size / Quantity:{Style.RESET}")
    print(f"    Live Reference Price: {cur_price:.{contract.price_precision}f} USDT | USD/INR: {inr_rate:.2f}")
    print(f"    1 contract = {contract.contract_size} {contract.base_coin} (~{one_contract_notional:.4f} USDT exposure, ~{one_contract_margin:.4f} USDT margin / INR {one_contract_margin*inr_rate:.2f})")
    print(f"    Select sizing method:")
    print(f"      1. Exact Contracts (e.g. 1, 2, 5 contracts)")
    print(f"      2. Target Margin in USDT (e.g. 1.0 USDT margin)")
    print(f"      3. Target Exposure / Notional in USDT (e.g. 10.0 USDT total value)")
    print(f"      4. Target Underlying Coin Qty (e.g. 50 {contract.base_coin})")

    mode_map = {"1": "CONTRACTS", "2": "MARGIN_USDT", "3": "NOTIONAL_USDT", "4": "COIN_QTY"}
    inv_mode_map = {v: k for k, v in mode_map.items()}
    default_choice = inv_mode_map.get(current_qty_mode, "1")

    while True:
        c_in = input(f"Choose sizing method [1-4] (Default {default_choice}): ").strip()
        chosen_mode = mode_map.get(c_in if c_in in mode_map else default_choice, "CONTRACTS")

        prompt_label = {
            "CONTRACTS": f"Number of contracts (min {contract.min_volume}) [{int(current_qty_val)}]: ",
            "MARGIN_USDT": f"Target margin in USDT [{current_qty_val:.2f}]: ",
            "NOTIONAL_USDT": f"Target notional exposure in USDT [{current_qty_val:.2f}]: ",
            "COIN_QTY": f"Target amount of {contract.base_coin} [{current_qty_val:.2f}]: "
        }[chosen_mode]

        val_in = input(prompt_label).strip()
        try:
            val = float(val_in) if val_in else current_qty_val
            if val <= 0:
                print(colorize("Quantity must be positive.", Style.YELLOW))
                continue

            # Compute contracts
            if chosen_mode == "CONTRACTS":
                vol = max(int(round(val)), int(contract.min_volume))
            elif chosen_mode == "MARGIN_USDT":
                target_notional = val * leverage
                vol = risk.convert_usdt_to_contracts(contract.symbol, target_notional, price=cur_price)
            elif chosen_mode == "NOTIONAL_USDT":
                vol = risk.convert_usdt_to_contracts(contract.symbol, val, price=cur_price)
            else:  # COIN_QTY
                vol = risk.convert_coin_qty_to_contracts(contract.symbol, val)

            vol = max(vol, int(contract.min_volume))
            notional = vol * contract.contract_size * cur_price
            margin = notional / leverage

            print(f"    {Style.GREEN}✓ Resolved to {vol} contract(s){Style.RESET} ({vol * contract.contract_size} {contract.base_coin})")
            print(f"      Total Exposure: {notional:.4f} USDT (INR {notional * inr_rate:.2f})")
            print(f"      Required Margin: {margin:.4f} USDT (INR {margin * inr_rate:.2f})")
            return chosen_mode, val, vol
        except ValueError:
            print(colorize("Please enter a valid numeric value.", Style.YELLOW))


def prompt_take_profit(
    contract: ContractInfo,
    direction: OrderDirection,
    leverage: int,
    market: KCEXMarket,
    current_mode: str,
    current_val: float
) -> Tuple[str, float]:
    """
    Prompts for Take-Profit rule (Ticks, ROI %, Price %, or Absolute Price).
    Returns (tp_mode, tp_val).
    """
    ticker = market.get_ticker(contract.symbol)
    cur_price = float(ticker.get("lastPrice", 1.0) or 1.0)
    bid1 = float(ticker.get("bid1", 0.0) or cur_price)
    ask1 = float(ticker.get("ask1", 0.0) or cur_price)
    pu = contract.price_unit
    ps = contract.price_precision
    spread_usdt = max(0.0, ask1 - bid1)
    spread_ticks = max(1, int(round(spread_usdt / pu))) if pu > 0 else 1
    safe_min_ticks = max(3, spread_ticks + 1)

    print(f"\n{Style.BOLD}[5] Take Profit (TP) Rule:{Style.RESET}")
    print(f"    Tick size (1 pu) for {contract.symbol} = {pu} USDT")
    print(f"    Order Book: Bid: {bid1:.{ps}f} | Ask: {ask1:.{ps}f} | Spread: {spread_ticks} tick(s) ({spread_usdt:.{ps}f} USDT)")
    print(f"    {Style.YELLOW}⚠️  Spread Notice: Market closes execute against opposite book (Bids for Long, Asks for Short).{Style.RESET}")
    print(f"       To clear the spread and guarantee NET PROFIT on market exit, TP should be >= {safe_min_ticks} ticks.")
    print(f"    Select TP method:")
    print(f"      1. Ticks / pu (e.g. {safe_min_ticks} ticks = {safe_min_ticks*pu:.{ps}f} USDT move) [RECOMMENDED]")
    print(f"      2. ROI / ROE % (Return on Margin, e.g. 15.0 for +15% ROE)")
    print(f"      3. Price Movement % (e.g. 0.5 for +0.5% price movement)")
    print(f"      4. Absolute Price Target (e.g. {cur_price + safe_min_ticks*pu if direction == OrderDirection.LONG else cur_price - safe_min_ticks*pu:.{ps}f})")

    mode_map = {"1": "TICKS", "2": "ROE_PCT", "3": "PRICE_PCT", "4": "ABSOLUTE"}
    inv_map = {v: k for k, v in mode_map.items()}
    default_choice = inv_map.get(current_mode, "1")

    # Ensure tick default is at least safe_min_ticks to prevent spread loss
    default_tick_val = max(int(current_val), safe_min_ticks)

    while True:
        c_in = input(f"Choose TP method [1-4] (Default {default_choice}): ").strip()
        chosen_mode = mode_map.get(c_in if c_in in mode_map else default_choice, "TICKS")

        prompt_label = {
            "TICKS": f"TP distance in ticks / pu [{default_tick_val}]: ",
            "ROE_PCT": f"TP target in ROE % (e.g. 15.0 for +15% ROE) [{current_val:g}%]: ",
            "PRICE_PCT": f"TP price movement % (e.g. 0.5 for +0.5%) [{current_val:g}%]: ",
            "ABSOLUTE": f"Absolute TP Price [{cur_price + default_tick_val*pu if direction == OrderDirection.LONG else cur_price - default_tick_val*pu:.{ps}f}]: "
        }[chosen_mode]

        val_in = input(prompt_label).strip()
        try:
            if chosen_mode == "TICKS":
                val = float(val_in) if val_in else float(default_tick_val)
            else:
                val = float(val_in) if val_in else current_val

            if val <= 0:
                print(colorize("TP value must be positive.", Style.YELLOW))
                continue

            if chosen_mode == "TICKS" and val <= spread_ticks:
                print(f"    {Style.RED}⚠️  CAUTION: {int(val)} tick(s) is within/equal to the bid-ask spread ({spread_ticks} ticks)!{Style.RESET}")
                print(f"       Market close will likely execute at or below entry price due to the spread.")
                confirm = input(f"       Proceed with {int(val)} tick(s) anyway? (y/N): ").strip().lower()
                if confirm not in ("y", "yes"):
                    continue

            # Preview target price
            if chosen_mode == "TICKS":
                dist = val * pu
                target_p = cur_price + dist if direction == OrderDirection.LONG else cur_price - dist
            elif chosen_mode == "ROE_PCT":
                price_pct = val / leverage
                target_p = cur_price * (1.0 + price_pct / 100.0) if direction == OrderDirection.LONG else cur_price * (1.0 - price_pct / 100.0)
            elif chosen_mode == "PRICE_PCT":
                target_p = cur_price * (1.0 + val / 100.0) if direction == OrderDirection.LONG else cur_price * (1.0 - val / 100.0)
            else:
                target_p = val

            print(f"    {Style.GREEN}✓ TP Target Price: {target_p:.{ps}f} USDT{Style.RESET} (At current ref price {cur_price:.{ps}f})")
            return chosen_mode, val
        except ValueError:
            print(colorize("Please enter a valid numeric value.", Style.YELLOW))


def prompt_stop_loss(
    contract: ContractInfo,
    direction: OrderDirection,
    leverage: int,
    market: KCEXMarket,
    current_mode: str,
    current_val: Optional[float]
) -> Tuple[str, Optional[float]]:
    """
    Prompts for Stop-Loss rule (ROI %, Ticks, Price %, Absolute Price, or None).
    Returns (sl_mode, sl_val).
    """
    ticker = market.get_ticker(contract.symbol)
    cur_price = float(ticker.get("lastPrice", 1.0) or 1.0)
    pu = contract.price_unit
    ps = contract.price_precision

    print(f"\n{Style.BOLD}[6] Stop Loss (SL) Rule:{Style.RESET}")
    print(f"    At {leverage}x leverage: 10% ROE loss = {10.0/leverage:.3f}% price move (~{math.ceil((10.0/leverage/100.0*cur_price)/pu)} ticks)")
    print(f"    Select SL method:")
    print(f"      1. ROI / ROE % (e.g. 15.0 for -15% ROE loss) [RECOMMENDED]")
    print(f"      2. Ticks / pu (e.g. 10 ticks away from entry)")
    print(f"      3. Price Movement % (e.g. 0.8 for -0.8% price move)")
    print(f"      4. Absolute Price Target")
    print(f"      5. None / Disabled")

    mode_map = {"1": "ROE_PCT", "2": "TICKS", "3": "PRICE_PCT", "4": "ABSOLUTE", "5": "NONE"}
    inv_map = {v: k for k, v in mode_map.items()}
    default_choice = inv_map.get(current_mode, "1")

    while True:
        c_in = input(f"Choose SL method [1-5] (Default {default_choice}): ").strip()
        chosen_mode = mode_map.get(c_in if c_in in mode_map else default_choice, "ROE_PCT")

        if chosen_mode == "NONE":
            print(f"    {Style.YELLOW}⚠ Stop Loss Disabled! Position will rely on TP or liquidation.{Style.RESET}")
            return "NONE", None

        default_v = current_val if current_val is not None else 15.0
        prompt_label = {
            "ROE_PCT": f"SL loss in ROE % (e.g. 15.0 for -15% ROE) [{default_v:g}%]: ",
            "TICKS": f"SL distance in ticks / pu [{int(default_v)}]: ",
            "PRICE_PCT": f"SL price drop % (e.g. 0.8 for -0.8%) [{default_v:g}%]: ",
            "ABSOLUTE": f"Absolute SL Price [{default_v:.{ps}f}]: "
        }[chosen_mode]

        val_in = input(prompt_label).strip()
        try:
            val = float(val_in) if val_in else default_v
            if val <= 0:
                print(colorize("SL value must be positive.", Style.YELLOW))
                continue

            # Preview target price
            if chosen_mode == "TICKS":
                dist = val * pu
                target_p = cur_price - dist if direction == OrderDirection.LONG else cur_price + dist
            elif chosen_mode == "ROE_PCT":
                price_pct = val / leverage
                target_p = cur_price * (1.0 - price_pct / 100.0) if direction == OrderDirection.LONG else cur_price * (1.0 + price_pct / 100.0)
            elif chosen_mode == "PRICE_PCT":
                target_p = cur_price * (1.0 - val / 100.0) if direction == OrderDirection.LONG else cur_price * (1.0 + val / 100.0)
            else:
                target_p = val

            # Check liquidation conflict
            mmr = contract.maintenance_margin_ratio if contract.maintenance_margin_ratio > 0 else 0.01
            buf_pct = max(0.0001, (1.0 / leverage) - mmr)
            buf_ticks = int(round((cur_price * buf_pct) / pu))
            sl_dist_ticks = abs(cur_price - target_p) / pu
            if sl_dist_ticks >= buf_ticks:
                print(f"    {Style.BG_RED}{Style.BOLD} ⚠️ CONFLICT: Requested SL is beyond Liquidation (~{buf_ticks} ticks away at {leverage}x)! {Style.RESET}")
                print(f"    {Style.RED}   At {leverage}x leverage, max possible SL is ~{int(buf_ticks * 0.8)} ticks before liquidation occurs.{Style.RESET}")
                retry = input("    Do you want to re-enter a tighter SL? [Y/n]: ").strip().lower()
                if retry not in ("n", "no"):
                    continue

            print(f"    {Style.RED}✓ SL Target Price: {target_p:.{ps}f} USDT{Style.RESET} (At current ref price {cur_price:.{ps}f})")
            return chosen_mode, val
        except ValueError:
            print(colorize("Please enter a valid numeric value.", Style.YELLOW))


# =============================================================================
# PRICE CALCULATION HELPERS
# =============================================================================

def compute_target_prices(
    direction: OrderDirection,
    entry_price: float,
    pu: float,
    precision: int,
    leverage: int,
    tp_mode: str,
    tp_val: float,
    sl_mode: str,
    sl_val: Optional[float],
    liq_price: Optional[float] = None
) -> Tuple[float, Optional[float]]:
    """
    Calculates absolute TP and SL prices given actual fill or reference price.
    Enforces minimum 1-tick safety distance and clamps SL within liquidation threshold.
    """
    # 1. Take Profit Calculation
    if tp_mode == "TICKS":
        dist = max(1.0, float(tp_val)) * pu
        tp_price = entry_price + dist if direction == OrderDirection.LONG else entry_price - dist
    elif tp_mode == "ROE_PCT":
        pct = (tp_val / leverage) / 100.0
        tp_price = entry_price * (1.0 + pct) if direction == OrderDirection.LONG else entry_price * (1.0 - pct)
    elif tp_mode == "PRICE_PCT":
        pct = tp_val / 100.0
        tp_price = entry_price * (1.0 + pct) if direction == OrderDirection.LONG else entry_price * (1.0 - pct)
    else:
        tp_price = tp_val

    # Guarantee TP is at least 1 tick away in profit direction
    if direction == OrderDirection.LONG:
        min_tp = round(entry_price + pu, precision)
        tp_price = max(tp_price, min_tp)
    else:
        min_tp = round(entry_price - pu, precision)
        tp_price = min(tp_price, min_tp)

    tp_price = round(tp_price, precision)

    # 2. Stop Loss Calculation
    sl_price = None
    if sl_mode != "NONE" and sl_val is not None:
        if sl_mode == "TICKS":
            dist = max(1.0, float(sl_val)) * pu
            sl_price = entry_price - dist if direction == OrderDirection.LONG else entry_price + dist
        elif sl_mode == "ROE_PCT":
            pct = (sl_val / leverage) / 100.0
            sl_price = entry_price * (1.0 - pct) if direction == OrderDirection.LONG else entry_price * (1.0 + pct)
        elif sl_mode == "PRICE_PCT":
            pct = sl_val / 100.0
            sl_price = entry_price * (1.0 - pct) if direction == OrderDirection.LONG else entry_price * (1.0 + pct)
        else:
            sl_price = sl_val

        # Guarantee SL is at least 1 tick away in loss direction
        if direction == OrderDirection.LONG:
            max_sl = round(entry_price - pu, precision)
            sl_price = min(sl_price, max_sl)
            # If liquidation price provided, clamp SL safely before liquidation (85% buffer)
            if liq_price and liq_price > 0 and sl_price <= liq_price:
                sl_price = round(entry_price - (entry_price - liq_price) * 0.85, precision)
        else:
            max_sl = round(entry_price + pu, precision)
            sl_price = max(sl_price, max_sl)
            # If liquidation price provided, clamp SL safely before liquidation (85% buffer)
            if liq_price and liq_price > 0 and sl_price >= liq_price:
                sl_price = round(entry_price + (liq_price - entry_price) * 0.85, precision)

        sl_price = round(sl_price, precision)

    return tp_price, sl_price


# =============================================================================
# PRE-TRADE CONFIRMATION REPORT
# =============================================================================

def print_pre_trade_report(
    contract: ContractInfo,
    direction: OrderDirection,
    vol_contracts: int,
    leverage: int,
    ref_price: float,
    tp_price: float,
    sl_price: Optional[float],
    tp_desc: str,
    sl_desc: str,
    inr_rate: float,
    risk: KCEXRiskCalculator
) -> bool:
    """Displays comprehensive pre-trade summary and prompts for user confirmation."""
    ps = contract.price_precision
    underlying_qty = vol_contracts * contract.contract_size
    notional_usdt = underlying_qty * ref_price
    notional_inr = notional_usdt * inr_rate
    margin_usdt = notional_usdt / leverage
    margin_inr = margin_usdt * inr_rate

    liq_price = risk.calculate_liquidation_price(
        symbol=contract.symbol,
        direction=direction.value,
        entry_price=ref_price,
        leverage=leverage,
        is_isolated=True
    )

    if direction == OrderDirection.LONG:
        dist_liq_pct = ((ref_price - liq_price) / ref_price) * 100.0 if ref_price > 0 else 0
        tp_diff = tp_price - ref_price
        sl_diff = (ref_price - sl_price) if sl_price else 0
    else:
        dist_liq_pct = ((liq_price - ref_price) / ref_price) * 100.0 if ref_price > 0 else 0
        tp_diff = ref_price - tp_price
        sl_diff = (sl_price - ref_price) if sl_price else 0

    tp_pnl_usdt = underlying_qty * tp_diff
    tp_roe_pct = (tp_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0

    sl_pnl_usdt = underlying_qty * sl_diff if sl_price else 0
    sl_roe_pct = (sl_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0

    dir_color = Style.GREEN if direction == OrderDirection.LONG else Style.RED
    dir_badge = f"{dir_color}{Style.BOLD}[{direction.value}]{Style.RESET}"

    print(f"\n{Style.CYAN}{Style.BOLD}" + "=" * 70)
    print(f"              PRE-TRADE EXECUTION SUMMARY & RISK CHECK")
    print("=" * 70 + f"{Style.RESET}")
    print(f"  • Contract / Pair    : {Style.BOLD}{contract.symbol}{Style.RESET} ({contract.base_coin}/{contract.quote_coin})")
    print(f"  • Direction          : {dir_badge}")
    print(f"  • Leverage           : {Style.YELLOW}{leverage}x Isolated{Style.RESET}")
    print(f"  • Order Size         : {vol_contracts} contract(s) = {underlying_qty:g} {contract.base_coin}")
    print(f"  • Reference Price    : {ref_price:.{ps}f} USDT")
    print(f"  • Position Exposure  : {notional_usdt:.4f} USDT (INR {notional_inr:.2f})")
    print(f"  • Required Margin    : {Style.BOLD}{margin_usdt:.4f} USDT (INR {margin_inr:.2f}){Style.RESET}")
    print(f"  • Est. Liquidation   : {liq_price:.{ps}f} USDT ({dist_liq_pct:.2f}% buffer)")
    print("-" * 70)
    print(f"  • Take Profit (TP)   : {Style.GREEN}{tp_price:.{ps}f} USDT{Style.RESET} ({tp_desc})")
    print(f"    Expected Profit    : {Style.GREEN}+{tp_pnl_usdt:.4f} USDT (+INR {tp_pnl_usdt * inr_rate:.2f}) | +{tp_roe_pct:.2f}% ROE{Style.RESET}")
    if sl_price:
        print(f"  • Stop Loss (SL)     : {Style.RED}{sl_price:.{ps}f} USDT{Style.RESET} ({sl_desc})")
        print(f"    Expected Loss      : {Style.RED}-{sl_pnl_usdt:.4f} USDT (-INR {sl_pnl_usdt * inr_rate:.2f}) | -{sl_roe_pct:.2f}% ROE{Style.RESET}")
        
        # Check if SL exceeds liquidation
        sl_beyond_liq = False
        if direction == OrderDirection.LONG and sl_price <= liq_price:
            sl_beyond_liq = True
        elif direction == OrderDirection.SHORT and sl_price >= liq_price:
            sl_beyond_liq = True
        if sl_beyond_liq:
            print(f"  {Style.BG_RED}{Style.BOLD} ⚠️ CAUTION: Stop Loss is beyond Liquidation Price ({liq_price:.{ps}f})! {Style.RESET}")
            print(f"  {Style.RED}   Position will liquidate before reaching SL. The bot will automatically protect against this.{Style.RESET}")
    else:
        print(f"  • Stop Loss (SL)     : {Style.YELLOW}None (Disabled){Style.RESET}")
    print("=" * 70)

    confirm = input(f"\n{Style.BOLD}Ready to execute this trade on KCEX? (Y/n) [Y]: {Style.RESET}").strip().lower()
    return confirm in ("", "y", "yes")


# =============================================================================
# HOTKEY HELPER (NON-BLOCKING KEYBOARD CHECK)
# =============================================================================

def check_manual_close_hotkey() -> bool:
    """
    Checks if user pressed 'c' or 'C' in Windows terminal without blocking.
    Returns True if manual close was requested.
    """
    if msvcrt and msvcrt.kbhit():
        try:
            ch = msvcrt.getch()
            # Handle special characters or letters
            if ch in (b'c', b'C'):
                return True
        except Exception:
            pass
    return False


# =============================================================================
# MARKET CLOSE VERIFICATION & HISTORY RECONCILIATION
# =============================================================================

def execute_market_close_and_verify(
    trader: KCEXTrader,
    market: KCEXMarket,
    symbol: str,
    position_id: Optional[int],
    direction: OrderDirection,
    vol_contracts: int,
    leverage: int,
    contract: ContractInfo,
    is_live: bool,
    max_wait_seconds: float = 8.0
) -> Tuple[float, Optional[str]]:
    """
    Submits a guaranteed market close order and actively polls KCEX until
    the position is 100% verified to be CLOSED (holdVol == 0).
    Returns (exit_price, close_order_id).
    """
    side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
    close_oid = None

    if not is_live:
        ticker = market.get_ticker(symbol)
        price = float(ticker.get("lastPrice", 0.0) or 1.0)
        return price, "simulated_close_id"

    # 1. Cancel any active stop orders to avoid locked position volume
    try:
        trader.cancel_all_orders(symbol=symbol)
    except Exception:
        pass

    # Fetch fresh price
    ticker = market.get_ticker(symbol)
    cur_p = float(ticker.get("lastPrice", 0.0) or 1.0)

    # 2. Send market close order (type=5)
    try:
        res = trader.close_position(
            position_id=position_id or 0,
            symbol=symbol,
            side=side_str,
            vol_contracts=vol_contracts,
            leverage=leverage,
            is_market=True,
            price=cur_p
        )
        close_oid = str(res.get("data", {}).get("orderId") or "")
    except Exception as e:
        print(f"\n{Style.YELLOW}Market close attempt 1 returned: {e}{Style.RESET}")

    # 3. Actively poll until position is confirmed closed
    start_t = time.time()
    is_open = True
    while time.time() - start_t < max_wait_seconds:
        time.sleep(0.35)
        try:
            open_pos = trader.get_open_positions(symbol)
            is_open = False
            for p in open_pos:
                if position_id:
                    if int(p.get("positionId", 0)) == int(position_id) and float(p.get("holdVol", 0) or 0) > 0:
                        is_open = True
                        break
                else:
                    if float(p.get("holdVol", 0) or 0) > 0:
                        is_open = True
                        break

            if not is_open:
                # Position confirmed closed on exchange!
                break
            else:
                # If still open after 1.5s, refresh price and retry close
                if time.time() - start_t > 1.5:
                    ticker = market.get_ticker(symbol)
                    cur_p = float(ticker.get("lastPrice", 0.0) or cur_p)
                    try:
                        res = trader.close_position(
                            position_id=position_id or 0,
                            symbol=symbol,
                            side=side_str,
                            vol_contracts=vol_contracts,
                            leverage=leverage,
                            is_market=True,
                            price=cur_p
                        )
                        close_oid = str(res.get("data", {}).get("orderId") or close_oid)
                    except Exception:
                        pass
        except Exception:
            pass

    # If still open after max_wait_seconds, do emergency retries
    if is_open:
        print(f"\n{Style.BG_RED}{Style.BOLD} ⚠️ POSITION STILL OPEN! Sending emergency market close... {Style.RESET}")
        for _ in range(3):
            time.sleep(0.5)
            ticker = market.get_ticker(symbol)
            cur_p = float(ticker.get("lastPrice", 0.0) or cur_p)
            try:
                trader.close_position(
                    position_id=position_id or 0,
                    symbol=symbol,
                    side=side_str,
                    vol_contracts=vol_contracts,
                    leverage=leverage,
                    is_market=True,
                    price=cur_p
                )
            except Exception:
                pass
            open_pos = trader.get_open_positions(symbol)
            still_there = any(
                float(p.get("holdVol", 0) or 0) > 0 for p in open_pos
                if not position_id or int(p.get("positionId", 0)) == int(position_id)
            )
            if not still_there:
                break

    # Clean up any lingering orders
    try:
        trader.cancel_all_orders(symbol=symbol)
    except Exception:
        pass

    # 4. Fetch exact exit price from KCEX history orders
    exit_price = cur_p
    time.sleep(0.35)
    try:
        hist = trader.client.get_private(
            KCEXConfig.ENDPOINT_ORDER_HISTORY,
            params={"symbol": symbol.upper(), "category": 1, "page_num": 1, "page_size": 10}
        )
        orders = hist.get("data", [])
        if isinstance(orders, dict):
            orders = orders.get("list", [])
        closing_side = 4 if direction == OrderDirection.LONG else 2
        for o in orders:
            if position_id and o.get("positionId") and int(o.get("positionId")) != int(position_id):
                continue
            if o.get("side") == closing_side and float(o.get("dealVol", 0)) > 0:
                p = float(o.get("dealAvgPrice") or o.get("price") or 0.0)
                if p > 0:
                    exit_price = p
                    break
    except Exception:
        pass

    return exit_price, close_oid


def reconcile_exit_from_kcex(
    trader: KCEXTrader,
    symbol: str,
    position_id: Optional[int],
    direction: OrderDirection,
    entry_price: float,
    fallback_price: float,
    open_time: Optional[float] = None
) -> Tuple[float, float, ExitReason]:
    """
    Inspects KCEX history_orders and history_positions to reliably determine
    the exact exit price, realized PnL, and whether it was TP or SL.
    Filters by position_id and open_time to prevent cross-trade contamination.
    """
    time.sleep(0.4)
    exit_price = fallback_price
    realized_pnl = 0.0
    exit_reason = ExitReason.UNKNOWN
    closing_side = 4 if direction == OrderDirection.LONG else 2

    # 1. Inspect history_orders
    try:
        res = trader.client.get_private(
            KCEXConfig.ENDPOINT_ORDER_HISTORY,
            params={"symbol": symbol.upper(), "category": 1, "page_num": 1, "page_size": 10}
        )
        orders = res.get("data", [])
        if isinstance(orders, dict):
            orders = orders.get("list", [])
        for o in orders:
            if open_time:
                o_time = float(o.get("createTime", 0) or 0) / 1000.0
                if o_time > 0 and o_time < open_time - 5.0:
                    continue
            if position_id and o.get("positionId") and int(o.get("positionId")) != int(position_id):
                continue
            if o.get("side") == closing_side and float(o.get("dealVol", 0)) > 0:
                p = float(o.get("dealAvgPrice") or o.get("price") or 0.0)
                if p > 0:
                    exit_price = p
                realized_pnl = float(o.get("profit", 0.0))
                ext_oid = str(o.get("externalOid") or "")
                if realized_pnl > 0:
                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                elif realized_pnl < 0:
                    exit_reason = ExitReason.STOP_LOSS_HIT
                elif "TAKE_PROFIT" in ext_oid:
                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                elif "STOP_LOSS" in ext_oid:
                    exit_reason = ExitReason.STOP_LOSS_HIT
                else:
                    exit_reason = ExitReason.SCRATCH_CLOSE
                return exit_price, realized_pnl, exit_reason
    except Exception:
        pass

    # 2. Inspect history_positions
    try:
        hist_pos = trader.get_position_history(page_size=5)
        for h in hist_pos:
            if open_time:
                h_time = float(h.get("createTime", 0) or 0) / 1000.0
                if h_time > 0 and h_time < open_time - 5.0:
                    continue
            if position_id and int(h.get("positionId", 0)) != int(position_id):
                continue
            if (position_id and int(h.get("positionId", 0)) == int(position_id)) or (not position_id and h.get("symbol") == symbol.upper()):
                close_p = float(h.get("closeAvgPrice") or 0.0)
                if close_p > 0:
                    exit_price = close_p
                pnl = float(h.get("closeProfitLoss", 0.0))
                realized_pnl = pnl
                if pnl > 0:
                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                elif pnl < 0:
                    exit_reason = ExitReason.STOP_LOSS_HIT
                else:
                    exit_reason = ExitReason.SCRATCH_CLOSE
                return exit_price, realized_pnl, exit_reason
    except Exception:
        pass

    # 3. Fallback based on price difference
    p_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)
    if p_diff > 0:
        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
    elif p_diff < 0:
        exit_reason = ExitReason.STOP_LOSS_HIT
    return exit_price, realized_pnl, exit_reason


# =============================================================================
# AUTONOMOUS POSITION MONITORING & TP/SL ENFORCER
# =============================================================================

def monitor_position_until_closed(
    trader: KCEXTrader,
    market: KCEXMarket,
    symbol: str,
    position_id: Optional[int],
    direction: OrderDirection,
    vol_contracts: int,
    leverage: int,
    entry_price: float,
    exact_tp: float,
    exact_sl: Optional[float],
    contract: ContractInfo,
    is_live: bool = True
) -> Tuple[float, ExitReason, Optional[str]]:
    """
    Autonomous Bot Monitor:
    - Displays real-time live terminal dashboard.
    - Guarantees TP execution: triggers immediate market close when target price is touched.
    - Guarantees SL execution: triggers emergency market close if price crosses SL.
    - Listens for server-side order fills with multi-check confirmation.
    - Listens for manual hotkey press ('C' to market close anytime).
    """
    ps = contract.price_precision
    pu = contract.price_unit
    cs = contract.contract_size
    underlying_qty = vol_contracts * cs
    inr_rate = market.get_inr_rate()
    notional_usdt = underlying_qty * entry_price
    margin_usdt = notional_usdt / leverage if leverage > 0 else 1.0

    side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
    start_time = time.time()
    last_seen_price = entry_price
    peak_profit_usdt = 0.0
    consecutive_not_found = 0
    tp_hit_first_seen: Optional[float] = None

    print(f"\n{Style.CYAN}{Style.BOLD}>>> AUTONOMOUS POSITION MONITOR ACTIVE <<<{Style.RESET}")
    print(f"Target TP: {Style.GREEN}{exact_tp:.{ps}f} USDT{Style.RESET} | Target SL: {Style.RED}{exact_sl:.{ps}f} USDT{Style.RESET}" if exact_sl else f"Target TP: {Style.GREEN}{exact_tp:.{ps}f} USDT{Style.RESET} | Target SL: None")
    print(f"{Style.DIM}Hotkeys: Press [C] to instantly Market Close now | Ctrl+C to abort{Style.RESET}\n")

    poll_count = 0
    while True:
        time.sleep(0.35)
        poll_count += 1
        elapsed = time.time() - start_time

        # 1. Hotkey check: Did user press 'C' for immediate manual market close?
        if check_manual_close_hotkey():
            print(f"\n{Style.YELLOW}⚡ [MANUAL HOTKEY TRIGGERED] 'C' key detected! Market closing position immediately...{Style.RESET}")
            exit_p, close_oid = execute_market_close_and_verify(
                trader=trader,
                market=market,
                symbol=symbol,
                position_id=position_id,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                contract=contract,
                is_live=is_live
            )
            return exit_p, ExitReason.MANUAL_CLOSE, close_oid

        # 2. Fetch fresh ticker & order book (bid1, ask1, lastPrice)
        try:
            ticker = market.get_ticker(symbol)
            cur_price = float(ticker.get("lastPrice", 0.0) or ticker.get("fairPrice", 0.0) or last_seen_price)
            bid1 = float(ticker.get("bid1", 0.0) or cur_price)
            ask1 = float(ticker.get("ask1", 0.0) or cur_price)
            if cur_price > 0:
                last_seen_price = cur_price
        except Exception:
            cur_price = last_seen_price
            bid1 = last_seen_price
            ask1 = last_seen_price

        # 3. Determine real executable price
        # For LONG: to exit via market order, you SELL into the Best Bid (bid1)
        # For SHORT: to exit via market order, you BUY from the Best Ask (ask1)
        exec_price = bid1 if direction == OrderDirection.LONG else ask1

        # 4. Compute realistic mark-to-market unrealized PnL & ROE %
        price_diff = (bid1 - entry_price) if direction == OrderDirection.LONG else (entry_price - ask1)
        unrealized_pnl_usdt = underlying_qty * price_diff
        unrealized_pnl_inr = unrealized_pnl_usdt * inr_rate
        live_roe_pct = (unrealized_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0.0

        if unrealized_pnl_usdt > peak_profit_usdt:
            peak_profit_usdt = unrealized_pnl_usdt

        # 5. Check if KCEX server closed position via server-side TP/SL (Every 2 polls in live mode)
        if is_live and (poll_count % 2 == 0):
            try:
                open_positions = trader.get_open_positions(symbol)
                pos_still_open = False
                for p in open_positions:
                    if position_id:
                        if int(p.get("positionId", 0)) == int(position_id) and float(p.get("holdVol", 0) or 0) > 0:
                            pos_still_open = True
                            break
                    else:
                        if float(p.get("holdVol", 0) or 0) > 0:
                            pos_still_open = True
                            break

                if not pos_still_open:
                    consecutive_not_found += 1
                    # Require 2 consecutive polls to confirm position is closed (prevents transient API blip)
                    if consecutive_not_found >= 2:
                        print(f"\n\n{Style.CYAN}{Style.BOLD}✓ Position filled & closed on KCEX exchange!{Style.RESET}")
                        try:
                            trader.cancel_all_orders(symbol=symbol)
                        except Exception:
                            pass
                        hist_exit_p, hist_pnl, hist_reason = reconcile_exit_from_kcex(
                            trader=trader,
                            symbol=symbol,
                            position_id=position_id,
                            direction=direction,
                            entry_price=entry_price,
                            fallback_price=exec_price,
                            open_time=start_time
                        )
                        return hist_exit_p, hist_reason, None
                else:
                    consecutive_not_found = 0
            except Exception:
                pass

        # 6. Evaluate Target Distances & Trigger Conditions
        if direction == OrderDirection.LONG:
            ticks_to_tp = int(round((exact_tp - exec_price) / pu))
            # CRITICAL: TP can ONLY trigger if the Best Bid is >= TP target AND strictly above entry price!
            can_tp = (bid1 >= exact_tp) and (bid1 > entry_price)
            sl_hit = (exact_sl is not None) and (bid1 <= exact_sl)
        else:
            ticks_to_tp = int(round((exec_price - exact_tp) / pu))
            # CRITICAL: TP can ONLY trigger if the Best Ask is <= TP target AND strictly below entry price!
            can_tp = (ask1 <= exact_tp) and (ask1 < entry_price)
            sl_hit = (exact_sl is not None) and (ask1 >= exact_sl)

        # 7. Format Live Dashboard Status Line (Showing Real Bid / Ask Spread!)
        pnl_color = Style.GREEN if unrealized_pnl_usdt >= 0 else Style.RED
        pnl_sign = "+" if unrealized_pnl_usdt >= 0 else ""
        tp_tag = f"{ticks_to_tp} ticks to TP" if ticks_to_tp > 0 else f"{Style.GREEN}AT/PAST TP TARGET!{Style.RESET}"

        status_line = (
            f"\r⏱ {elapsed:4.1f}s | Price: {cur_price:.{ps}f} (Bid: {bid1:.{ps}f} | Ask: {ask1:.{ps}f}) | "
            f"PnL: {pnl_color}{pnl_sign}{unrealized_pnl_usdt:.4f} USDT ({pnl_sign}INR {unrealized_pnl_inr:.2f}){Style.RESET} | "
            f"ROE: {pnl_color}{pnl_sign}{live_roe_pct:.2f}%{Style.RESET} | "
            f"[{tp_tag}]   "
        )
        sys.stdout.write(status_line)
        sys.stdout.flush()

        # 8. STOP LOSS HIT CHECK (Emergency capital preservation)
        if sl_hit:
            print(f"\n\n{Style.BG_RED}{Style.BOLD} 🛑 STOP LOSS LEVEL REACHED! {Style.RESET} "
                  f"Executable Price: {exec_price:.{ps}f} (SL: {exact_sl:.{ps}f}). Executing emergency Market Close...")
            exit_p, close_oid = execute_market_close_and_verify(
                trader=trader,
                market=market,
                symbol=symbol,
                position_id=position_id,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                contract=contract,
                is_live=is_live
            )
            if is_live:
                hist_exit_p, hist_pnl, hist_reason = reconcile_exit_from_kcex(
                    trader=trader,
                    symbol=symbol,
                    position_id=position_id,
                    direction=direction,
                    entry_price=entry_price,
                    fallback_price=exit_p,
                    open_time=start_time
                )
                return hist_exit_p, hist_reason, close_oid
            return exit_p, ExitReason.STOP_LOSS_HIT, close_oid

        # 9. TAKE PROFIT HIT CHECK
        if can_tp:
            if not is_live:
                # Dry-run: immediate simulated TP execution
                print(f"\n\n{Style.BG_GREEN}{Style.BOLD} 🎯 [DRY-RUN] TAKE PROFIT TARGET REACHED! {Style.RESET} "
                      f"Simulated Exec Price: {exec_price:.{ps}f} (Target: {exact_tp:.{ps}f})")
                return exec_price, ExitReason.MIN_PROFIT_TP_HIT, "dry_run_tp"
            else:
                # Live mode: KCEX server-side stop order is active.
                # Allow KCEX native stop order 1.5 seconds of sustained executable TP to fill on exchange first.
                if tp_hit_first_seen is None:
                    tp_hit_first_seen = time.time()
                elif time.time() - tp_hit_first_seen >= 1.5:
                    # KCEX server stop order lagged or was missing -> execute guaranteed market close in profit
                    print(f"\n\n{Style.BG_GREEN}{Style.BOLD} 🎯 TAKE PROFIT TARGET REACHED! {Style.RESET} "
                          f"Executable Price: {exec_price:.{ps}f} (Target: {exact_tp:.{ps}f}). Executing guaranteed Market Close...")
                    exit_p, close_oid = execute_market_close_and_verify(
                        trader=trader,
                        market=market,
                        symbol=symbol,
                        position_id=position_id,
                        direction=direction,
                        vol_contracts=vol_contracts,
                        leverage=leverage,
                        contract=contract,
                        is_live=is_live
                    )
                    hist_exit_p, hist_pnl, hist_reason = reconcile_exit_from_kcex(
                        trader=trader,
                        symbol=symbol,
                        position_id=position_id,
                        direction=direction,
                        entry_price=entry_price,
                        fallback_price=exit_p,
                        open_time=start_time
                    )
                    return hist_exit_p, hist_reason, close_oid
        else:
            tp_hit_first_seen = None


# =============================================================================
# RECONCILIATION & POST-TRADE REPORT CARD
# =============================================================================

def print_trade_outcome_card(
    trade_num: int,
    symbol: str,
    direction: OrderDirection,
    vol_contracts: int,
    leverage: int,
    entry_price: float,
    exit_price: float,
    exit_reason: ExitReason,
    open_time: float,
    close_time: float,
    contract: ContractInfo,
    market: KCEXMarket,
    trader: Optional[KCEXTrader] = None,
    position_id: Optional[int] = None,
    is_live: bool = True
):
    """Prints a beautiful post-trade card with realized PnL in USDT & INR, and updated balance."""
    ps = contract.price_precision
    pu = contract.price_unit
    cs = contract.contract_size
    underlying_qty = vol_contracts * cs
    duration = max(0.1, close_time - open_time)
    inr_rate = market.get_inr_rate()

    price_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)
    realized_pnl_usdt = underlying_qty * price_diff
    realized_pnl_inr = realized_pnl_usdt * inr_rate
    notional_usdt = underlying_qty * entry_price
    margin_usdt = notional_usdt / leverage if leverage > 0 else 1.0
    roe_pct = (realized_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0.0

    # Query KCEX history if live to obtain exact exchange-settled numbers
    if is_live and trader:
        time.sleep(0.4)
        try:
            hist_orders = trader.client.get_private(
                KCEXConfig.ENDPOINT_ORDER_HISTORY,
                params={"symbol": symbol.upper(), "category": 1, "page_num": 1, "page_size": 10}
            )
            orders = hist_orders.get("data", [])
            if isinstance(orders, dict):
                orders = orders.get("list", [])
            closing_side = 4 if direction == OrderDirection.LONG else 2
            for o in orders:
                if open_time:
                    o_time = float(o.get("createTime", 0) or 0) / 1000.0
                    if o_time > 0 and o_time < open_time - 5.0:
                        continue
                if position_id and o.get("positionId") and int(o.get("positionId")) != int(position_id):
                    continue
                if o.get("side") == closing_side and float(o.get("dealVol", 0)) > 0:
                    deal_p = float(o.get("dealAvgPrice") or o.get("price") or 0.0)
                    if deal_p > 0:
                        exit_price = deal_p
                    pnl_val = float(o.get("profit", 0.0))
                    if pnl_val != 0.0:
                        realized_pnl_usdt = pnl_val
                        realized_pnl_inr = realized_pnl_usdt * inr_rate
                        roe_pct = (realized_pnl_usdt / margin_usdt) * 100.0
                    break
        except Exception:
            pass

    pnl_color = Style.GREEN if realized_pnl_usdt >= 0 else Style.RED
    pnl_sign = "+" if realized_pnl_usdt >= 0 else ""
    win_tag = "WIN" if realized_pnl_usdt > 0 else "LOSS" if realized_pnl_usdt < 0 else "EVEN"
    badge_bg = Style.BG_GREEN if realized_pnl_usdt >= 0 else Style.BG_RED

    print(f"\n{pnl_color}" + "=" * 70)
    print(f"                   TRADE #{trade_num} OUTCOME REPORT [{win_tag}]")
    print("=" * 70 + f"{Style.RESET}")
    print(f"  • Pair & Direction : {Style.BOLD}{symbol}{Style.RESET} {direction.value} ({leverage}x Isolated)")
    print(f"  • Position Size    : {vol_contracts} contract(s) ({underlying_qty:g} {contract.base_coin})")
    print(f"  • Entry Price      : {entry_price:.{ps}f} USDT")
    print(f"  • Exit Price       : {exit_price:.{ps}f} USDT")
    print(f"  • Duration         : {duration:.1f} seconds")
    print(f"  • Exit Reason      : {exit_reason.value}")
    print("-" * 70)
    print(f"  • {Style.BOLD}Realized PnL (USDT): {pnl_color}{Style.BOLD}{pnl_sign}{realized_pnl_usdt:.4f} USDT{Style.RESET}")
    print(f"  • {Style.BOLD}Realized PnL (INR) : {pnl_color}{Style.BOLD}{pnl_sign}INR {realized_pnl_inr:.2f}{Style.RESET}")
    print(f"  • {Style.BOLD}Return on Equity   : {badge_bg} {pnl_sign}{roe_pct:.2f}% ROE {Style.RESET}")
    print("=" * 70)

    # Balance display
    if is_live and trader:
        try:
            bal = trader.get_usdt_balance()
            avail = bal.get("available_usdt", 0.0)
            avail_inr = bal.get("available_inr", 0.0)
            equity = bal.get("equity_usdt", 0.0)
            equity_inr = bal.get("equity_inr", 0.0)
            print(f"  💰 {Style.BOLD}Updated Balance{Style.RESET} : {avail:.4f} USDT (INR {avail_inr:.2f}) | Equity: {equity:.4f} USDT (INR {equity_inr:.2f})\n")
        except Exception:
            pass


# =============================================================================
# SINGLE TRADE LIFECYCLE
# =============================================================================

def execute_single_trade_cycle(
    preset: TradePreset,
    direction: OrderDirection,
    trade_num: int,
    market: KCEXMarket,
    trader: KCEXTrader,
    risk: KCEXRiskCalculator
) -> bool:
    """
    Executes one complete trade:
    1. Pre-trade calculation & confirmation.
    2. Order submission.
    3. Live monitoring & TP/SL enforcement.
    4. Post-trade report & balance update.
    Returns True if trade executed and closed, False if aborted by user.
    """
    contract = market.get_contract_detail(preset.symbol)
    pu = contract.price_unit
    ps = contract.price_precision
    inr_rate = market.get_inr_rate()
    ticker = market.get_ticker(preset.symbol)
    ref_price = float(ticker.get("lastPrice", 1.0) or 1.0)

    # Compute volume contracts
    if preset.qty_mode == "CONTRACTS":
        vol_contracts = max(int(round(preset.qty_val)), int(contract.min_volume))
    elif preset.qty_mode == "MARGIN_USDT":
        target_notional = preset.qty_val * preset.leverage
        vol_contracts = risk.convert_usdt_to_contracts(preset.symbol, target_notional, price=ref_price)
    elif preset.qty_mode == "NOTIONAL_USDT":
        vol_contracts = risk.convert_usdt_to_contracts(preset.symbol, preset.qty_val, price=ref_price)
    else:  # COIN_QTY
        vol_contracts = risk.convert_coin_qty_to_contracts(preset.symbol, preset.qty_val)

    vol_contracts = max(vol_contracts, int(contract.min_volume))

    # Calculate liquidation price for preview
    est_liq = risk.calculate_liquidation_price(
        symbol=preset.symbol,
        direction=direction.value,
        entry_price=ref_price,
        leverage=preset.leverage,
        is_isolated=preset.is_isolated
    )

    # Compute estimated TP and SL from reference price for the preview
    est_tp, est_sl = compute_target_prices(
        direction=direction,
        entry_price=ref_price,
        pu=pu,
        precision=ps,
        leverage=preset.leverage,
        tp_mode=preset.tp_mode,
        tp_val=preset.tp_val,
        sl_mode=preset.sl_mode,
        sl_val=preset.sl_val,
        liq_price=est_liq
    )

    tp_desc = f"{preset.tp_val:g} ticks" if preset.tp_mode == "TICKS" else f"{preset.tp_val:g}% ROE" if preset.tp_mode == "ROE_PCT" else f"{preset.tp_val:g}% price" if preset.tp_mode == "PRICE_PCT" else f"{preset.tp_val:g} USDT"
    sl_desc = f"{preset.sl_val:g}% ROE" if preset.sl_mode == "ROE_PCT" else f"{preset.sl_val:g} ticks" if preset.sl_mode == "TICKS" else f"{preset.sl_val:g}% price" if preset.sl_mode == "PRICE_PCT" else f"{preset.sl_val:g} USDT" if preset.sl_mode == "ABSOLUTE" else "None"

    # Pre-trade confirmation
    confirmed = print_pre_trade_report(
        contract=contract,
        direction=direction,
        vol_contracts=vol_contracts,
        leverage=preset.leverage,
        ref_price=ref_price,
        tp_price=est_tp,
        sl_price=est_sl,
        tp_desc=tp_desc,
        sl_desc=sl_desc,
        inr_rate=inr_rate,
        risk=risk
    )

    if not confirmed:
        print(f"{Style.YELLOW}Trade #{trade_num} cancelled by user.{Style.RESET}")
        return False

    # Submit Order
    is_live = (preset.mode == EngineMode.LIVE)
    open_time = time.time()
    side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
    position_id = None
    actual_entry_price = ref_price
    actual_vol = vol_contracts

    if is_live:
        print(f"\n{Style.CYAN}Submitting live MARKET order to KCEX...{Style.RESET}")
        try:
            # Note: Do not attach pre-trade TP/SL. Fill price must be captured first so TP/SL are 100% exact!
            res = trader.create_order(
                symbol=preset.symbol,
                side=side_str,
                vol_contracts=vol_contracts,
                order_type="MARKET",
                leverage=preset.leverage,
                is_isolated=preset.is_isolated
            )
            order_id = res.get("data", {}).get("orderId")
            print(f"{Style.GREEN}✓ Order accepted by KCEX! Order ID: {order_id}{Style.RESET}")
        except Exception as e:
            print(f"{Style.RED}✗ Order placement failed: {e}{Style.RESET}")
            return False

        # Actively poll to verify fill and get actual openAvgPrice & positionId
        print("Verifying position fill on KCEX...")
        for attempt in range(25):
            time.sleep(0.2)
            try:
                positions = trader.get_open_positions(preset.symbol)
                for p in positions:
                    h_vol = float(p.get("holdVol", 0) or p.get("vol", 0))
                    if h_vol > 0:
                        position_id = int(p.get("positionId"))
                        actual_entry_price = float(p.get("openAvgPrice") or p.get("holdAvgPrice") or ref_price)
                        actual_vol = int(h_vol)
                        break
                if position_id:
                    break
            except Exception:
                pass

        # If not confirmed in open_positions, inspect history_orders to see if order was cancelled or rejected
        if not position_id and order_id:
            time.sleep(0.3)
            try:
                hist_res = trader.client.get_private(
                    KCEXConfig.ENDPOINT_ORDER_HISTORY,
                    params={"symbol": preset.symbol.upper(), "category": 1, "page_num": 1, "page_size": 10}
                )
                orders = hist_res.get("data", [])
                if isinstance(orders, dict):
                    orders = orders.get("list", [])
                for o in orders:
                    if str(o.get("orderId")) == str(order_id):
                        state = o.get("state")
                        deal_vol = float(o.get("dealVol", 0) or 0)
                        err_code = o.get("errorCode", 0)
                        if state == 4 or deal_vol == 0:
                            err_reasons = {
                                6: "Market price exceeds exchange liquidation / fair-price risk collar",
                                10: "Order cancelled by exchange matching engine"
                            }
                            reason_msg = err_reasons.get(err_code, f"Exchange Error Code {err_code}")
                            print(f"\n{Style.BG_RED}{Style.BOLD} ❌ ORDER CANCELLED BY KCEX EXCHANGE! {Style.RESET}")
                            print(f"{Style.RED}Order ID {order_id} was rejected/cancelled by KCEX: {reason_msg}.{Style.RESET}")
                            print(f"{Style.YELLOW}The position was NOT opened. No funds were used or lost.{Style.RESET}")
                            if preset.leverage >= 50:
                                print(f"{Style.YELLOW}💡 Note: At extreme leverage ({preset.leverage}x), market orders are easily cancelled if the ask spread exceeds the fair-price safety collar. Try setting leverage to 30x - 50x.{Style.RESET}\n")
                            return False
                        elif state == 3 and deal_vol > 0:
                            position_id = int(o.get("positionId", 0)) or None
                            actual_entry_price = float(o.get("dealAvgPrice") or ref_price)
                            actual_vol = int(deal_vol)
                            break
            except Exception:
                pass

        if not position_id:
            print(f"\n{Style.RED}✗ Could not confirm position fill on KCEX (position was NOT opened). Aborting trade.{Style.RESET}\n")
            return False
    else:
        print(f"\n{Style.GREEN}✓ [DRY-RUN] Simulated MARKET order executed at current market price!{Style.RESET}")
        actual_entry_price = ref_price

    # Calculate actual liquidation price on filled entry
    actual_liq = risk.calculate_liquidation_price(
        symbol=preset.symbol,
        direction=direction.value,
        entry_price=actual_entry_price,
        leverage=preset.leverage,
        is_isolated=preset.is_isolated
    )

    # Recalculate exact TP/SL from actual filled entry price
    exact_tp, exact_sl = compute_target_prices(
        direction=direction,
        entry_price=actual_entry_price,
        pu=pu,
        precision=ps,
        leverage=preset.leverage,
        tp_mode=preset.tp_mode,
        tp_val=preset.tp_val,
        sl_mode=preset.sl_mode,
        sl_val=preset.sl_val,
        liq_price=actual_liq
    )

    print(f"Entry Filled at: {Style.BOLD}{actual_entry_price:.{ps}f} USDT{Style.RESET} | Exact TP: {Style.GREEN}{exact_tp:.{ps}f}{Style.RESET} | Exact SL: {Style.RED}{exact_sl or 'None'}{Style.RESET}")

    # Set KCEX Server-Side TP/SL on the open position
    if is_live and position_id:
        try:
            trader.set_position_tp_sl(
                symbol=preset.symbol,
                position_id=position_id,
                take_profit_price=exact_tp,
                stop_loss_price=exact_sl
            )
            print(f"{Style.GREEN}✓ Native KCEX Server-Side TP/SL Stoporder Activated!{Style.RESET}")
        except Exception as e:
            print(f"{Style.YELLOW}⚠ Warning activating server stoporder: {e} (Bot local monitor will enforce TP/SL){Style.RESET}")

    # Enter Autonomous Monitor Loop
    try:
        exit_price, exit_reason, close_oid = monitor_position_until_closed(
            trader=trader,
            market=market,
            symbol=preset.symbol,
            position_id=position_id,
            direction=direction,
            vol_contracts=actual_vol,
            leverage=preset.leverage,
            entry_price=actual_entry_price,
            exact_tp=exact_tp,
            exact_sl=exact_sl,
            contract=contract,
            is_live=is_live
        )
    except KeyboardInterrupt:
        print(f"\n\n{Style.YELLOW}⚠ User interrupted monitor loop (Ctrl+C).{Style.RESET}")
        if is_live:
            close_now = input("Close this position now on KCEX? (Y/n) [Y]: ").strip().lower()
            if close_now in ("", "y", "yes"):
                execute_market_close_and_verify(
                    trader=trader,
                    market=market,
                    symbol=preset.symbol,
                    position_id=position_id,
                    direction=direction,
                    vol_contracts=actual_vol,
                    leverage=preset.leverage,
                    contract=contract,
                    is_live=is_live
                )
                print(f"{Style.GREEN}✓ Position market closed.{Style.RESET}")
        return False

    close_time = time.time()

    # Post-Trade Outcome Report
    print_trade_outcome_card(
        trade_num=trade_num,
        symbol=preset.symbol,
        direction=direction,
        vol_contracts=vol_contracts,
        leverage=preset.leverage,
        entry_price=actual_entry_price,
        exit_price=exit_price,
        exit_reason=exit_reason,
        open_time=open_time,
        close_time=close_time,
        contract=contract,
        market=market,
        trader=trader if is_live else None,
        position_id=position_id,
        is_live=is_live
    )

    return True


# =============================================================================
# MAIN INTERACTIVE SEMI-AUTONOMOUS ENGINE LOOP
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="KCEX Semi-Autonomous Trade Execution Script")
    parser.add_argument("--mode", choices=["live", "dry-run"], default=None, help="Execution mode ('live' or 'dry-run')")
    parser.add_argument("--symbol", default=None, help="Initial trading pair (e.g. TRUMP_USDT)")
    args = parser.parse_args()

    config = KCEXConfig()
    client = KCEXClient(config)
    market = KCEXMarket(client)
    risk = KCEXRiskCalculator(market, client)
    trader = KCEXTrader(client, market, risk)

    # Initialize preset with defaults
    preset = init_default_preset(config)

    # Handle mode CLI flag or auth status
    if args.mode:
        preset.mode = EngineMode.LIVE if args.mode == "live" else EngineMode.DRY_RUN
    elif not config.is_authenticated:
        preset.mode = EngineMode.DRY_RUN

    if args.symbol:
        preset.symbol = args.symbol.upper()

    print_banner(preset.mode)

    # Account Balance Check
    if preset.mode == EngineMode.LIVE:
        try:
            bal = trader.get_usdt_balance()
            avail = bal.get("available_usdt", 0.0)
            avail_inr = bal.get("available_inr", 0.0)
            equity = bal.get("equity_usdt", 0.0)
            equity_inr = bal.get("equity_inr", 0.0)
            print(f"💼 {Style.BOLD}Connected Wallet Balance{Style.RESET}: Available: {Style.GREEN}{avail:.4f} USDT (INR {avail_inr:.2f}){Style.RESET} | Equity: {equity:.4f} USDT (INR {equity_inr:.2f})\n")
        except Exception as e:
            print(colorize(f"Warning: Could not fetch wallet balance: {e}", Style.YELLOW))
    else:
        print(f"ℹ️  Dry-Run Mode: Real orders will {Style.BOLD}NOT{Style.RESET} be sent to the exchange. Simulated with real-time ticker.\n")

    trade_count = 0

    # Main semi-autonomous trading session loop
    while True:
        trade_count += 1
        print(f"\n{Style.CYAN}{Style.BOLD}==============================================================================")
        print(f"                   SETUP FOR TRADE #{trade_count}")
        print(f"=============================================================================={Style.RESET}")

        # If trade #2 or higher: Prompt whether to continue with previous settings
        if trade_count > 1:
            print(f"\n{Style.BOLD}Previous Trade Settings:{Style.RESET}")
            for line in preset.summary_lines():
                print(line)

            use_prev = input(f"\n{Style.BOLD}Continue with previous settings? (Y/n) [Y]: {Style.RESET}").strip().lower()
            if use_prev in ("", "y", "yes"):
                print(f"{Style.GREEN}✓ Reusing previous settings! Only direction required.{Style.RESET}")
                direction = prompt_direction()
                executed = execute_single_trade_cycle(
                    preset=preset,
                    direction=direction,
                    trade_num=trade_count,
                    market=market,
                    trader=trader,
                    risk=risk
                )

                # Prompt for next trade
                print("\n" + "-" * 70)
                next_trade = input(f"{Style.BOLD}Take the next trade? (Y/n) [Y]: {Style.RESET}").strip().lower()
                if next_trade not in ("", "y", "yes"):
                    print(f"\n{Style.CYAN}Exiting Semi-Autonomous Trading Session. Good luck!{Style.RESET}")
                    break
                continue
            else:
                print(f"\n{Style.YELLOW}Modifying settings (press Enter to keep any previous value):{Style.RESET}")

        # Fresh or edited configuration setup
        direction = prompt_direction()
        preset.symbol = prompt_symbol(market, preset.symbol)
        contract = market.get_contract_detail(preset.symbol)
        preset.leverage = prompt_leverage(contract, preset.leverage)
        preset.qty_mode, preset.qty_val, _ = prompt_quantity(
            contract=contract,
            market=market,
            risk=risk,
            leverage=preset.leverage,
            current_qty_mode=preset.qty_mode,
            current_qty_val=preset.qty_val
        )
        preset.tp_mode, preset.tp_val = prompt_take_profit(
            contract=contract,
            direction=direction,
            leverage=preset.leverage,
            market=market,
            current_mode=preset.tp_mode,
            current_val=preset.tp_val
        )
        preset.sl_mode, preset.sl_val = prompt_stop_loss(
            contract=contract,
            direction=direction,
            leverage=preset.leverage,
            market=market,
            current_mode=preset.sl_mode,
            current_val=preset.sl_val
        )

        # Execute Trade
        executed = execute_single_trade_cycle(
            preset=preset,
            direction=direction,
            trade_num=trade_count,
            market=market,
            trader=trader,
            risk=risk
        )

        # Prompt for next trade
        print("\n" + "-" * 70)
        next_trade = input(f"{Style.BOLD}Take the next trade? (Y/n) [Y]: {Style.RESET}").strip().lower()
        if next_trade not in ("", "y", "yes"):
            print(f"\n{Style.CYAN}Exiting Semi-Autonomous Trading Session. Good luck!{Style.RESET}")
            break


if __name__ == "__main__":
    main()
