"""
KCEX Manual Trade Execution & Testing Suite
===========================================
Interactive CLI and test runner to manually verify and manage KCEX futures trades.

Features:
1. Connectivity & Live Fiat Exchange Rates (USD -> INR)
2. Pair Explorer & Coin Specifications (cs, minV, maxL, fees, mmr, etc.)
3. Real-Time Market Data (Ticker, L2 Order Book, OHLCV Candles, Recent Trades)
4. Pre-Trade Risk Calculator (Dual Currency USDT & INR, Liquidation, Fees, TP/SL by Price/ROE/Absolute)
5. Account Balances & Portfolio (USDT & INR Available, Equity, Unrealized PnL)
6. Live Order Execution (Market/Limit, Long/Short with attached TP/SL)
7. Post-Trade Management (Set/Modify TP/SL on open positions, Partial & Full Closes)
8. Automated Self-Test Mode (--test flag)

Usage:
    Interactive Menu:  python test_trade_execution.py
    Automated Tests:   python test_trade_execution.py --test
"""

import sys
import os
import time
import argparse
from typing import Optional

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure package root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kcex.config import KCEXConfig
from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator
from kcex.trade import KCEXTrader
from kcex.signer import KCEXSigner


def print_banner():
    print("=" * 70)
    print("      [KCEX FUTURES BOT] - TRADE MANAGEMENT & TESTING SUITE")
    print("=" * 70)


def format_inr(usdt_val: float, inr_rate: float) -> str:
    return f"{usdt_val:.4f} USDT (INR {usdt_val * inr_rate:.2f})"


def run_automated_tests():
    """
    Runs automated non-destructive tests for public endpoints,
    calculations, signature generation, and data structures.
    """
    print_banner()
    print("Running Automated Non-Destructive Self-Tests...\n")
    passed = 0
    total = 0

    def assert_test(name: str, cond: bool, detail: str = ""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {name} {detail}")
        else:
            print(f"  [FAIL] {name} - {detail}")

    # 1. Test Client & Ping
    config = KCEXConfig()
    client = KCEXClient(config)
    market = KCEXMarket(client)
    risk = KCEXRiskCalculator(market, client)

    print("1. Connectivity & Public Endpoints:")
    ping_ok = market.ping()
    assert_test("KCEX Ping Probe", ping_ok)

    # 2. Exchange Rate (INR)
    inr_rate = market.get_inr_rate()
    assert_test("Real-time INR Rate", inr_rate > 50, f"Rate: INR {inr_rate:.2f}")

    # 3. Contract Detail (TRUMP_USDT)
    try:
        trump = market.get_contract_detail("TRUMP_USDT")
        assert_test("TRUMP Contract Metadata", trump.contract_size == 0.1, f"cs={trump.contract_size}, minV={trump.min_volume}, maxL={trump.max_leverage}")
    except Exception as e:
        assert_test("TRUMP Contract Metadata", False, str(e))

    # 4. Ticker Snapshot
    try:
        ticker = market.get_ticker("TRUMP_USDT")
        last_p = float(ticker.get("lastPrice", 0))
        assert_test("TRUMP Ticker Snapshot", last_p > 0, f"lastPrice={last_p}, fairPrice={ticker.get('fairPrice')}")
    except Exception as e:
        assert_test("TRUMP Ticker Snapshot", False, str(e))

    # 5. L2 Order Book Depth
    try:
        depth = market.get_order_book("TRUMP_USDT")
        asks_len = len(depth.get("asks", []))
        bids_len = len(depth.get("bids", []))
        assert_test("Order Book Depth", asks_len > 0 and bids_len > 0, f"Asks: {asks_len}, Bids: {bids_len}")
    except Exception as e:
        assert_test("Order Book Depth", False, str(e))

    # 6. OHLCV Klines
    try:
        candles = market.get_klines("TRUMP_USDT", interval="Min1", limit=10)
        assert_test("OHLCV Candles", len(candles) > 0, f"Fetched {len(candles)} 1-minute bars")
    except Exception as e:
        assert_test("OHLCV Candles", False, str(e))

    # 7. Reverse-Engineered Signer Test
    print("\n2. Request Signing Verification:")
    test_config = KCEXConfig(auth_token="test_token_123456")
    signer = KCEXSigner(test_config)
    test_payload = {"symbol": "TRUMP_USDT", "vol": 1}
    headers = signer.sign_request(method="POST", body=test_payload, timestamp_ms=1788487268389)
    has_sign = bool(headers.get("Content-Sign"))
    has_time = headers.get("Content-time") == "1788487268389"
    has_auth = headers.get("Authorization") == "test_token_123456"
    assert_test("Signature Generation", has_sign and has_time and has_auth, f"Sign: {headers.get('Content-Sign')}")

    # 8. Risk & Liquidation Math Tests
    print("\n3. Risk & Math Calculator Verification:")
    # Test volume conversion
    vol = risk.convert_usdt_to_contracts("TRUMP_USDT", target_usdt=0.3, price=2.34)
    assert_test("USDT to Contracts Conversion", vol >= 1, f"0.3 USDT -> {vol} contract(s)")

    # Test Liquidation formula for 75x Long at price 2.344 with MMR 0.0067:
    # Liq = 2.344 * (1 - 1/75 + 0.0067) = 2.344 * (1 - 0.01333 + 0.0067) = 2.344 * 0.99336 = 2.328
    liq = risk.calculate_liquidation_price("TRUMP_USDT", "LONG", entry_price=2.344, leverage=75, is_isolated=True)
    assert_test("Liquidation Price Formula", 2.30 <= liq <= 2.38, f"Calc Liq: {liq:.4f}")

    # Test TP/SL by Price %
    targets = risk.calculate_tp_sl_from_price_pct("LONG", 2.0, tp_pct=10.0, sl_pct=5.0)
    assert_test("TP/SL from Price %", targets["take_profit_price"] == 2.2 and targets["stop_loss_price"] == 1.9)

    # Test TP/SL by ROE % (e.g. 50% ROE with 50x leverage = 1% price change)
    targets_roe = risk.calculate_tp_sl_from_roe_pct("LONG", 100.0, leverage=50, tp_roe_pct=50.0, sl_roe_pct=25.0)
    assert_test("TP/SL from ROE %", targets_roe["take_profit_price"] == 101.0 and targets_roe["stop_loss_price"] == 99.5)

    # Test Full Risk Report Generation
    report = risk.analyze_order_risk(
        symbol="TRUMP_USDT",
        direction="LONG",
        vol_contracts=1,
        entry_price=2.35,
        leverage=75,
        tp_roe_pct=20.0,
        sl_roe_pct=10.0
    )
    assert_test("Pre-Trade Risk Report", report.notional_value_usdt > 0 and report.notional_value_inr > 0)

    print(f"\nResults: {passed}/{total} tests passed.")
    if passed == total:
        print("[OK] ALL TESTS PASSED SUCCESSFULLY!\n")
    else:
        print("[WARNING] Some tests failed. Check output above.\n")


def interactive_cli():
    """Main interactive menu for manual checking and trading."""
    config = KCEXConfig()
    client = KCEXClient(config)
    market = KCEXMarket(client)
    risk = KCEXRiskCalculator(market, client)
    trader = KCEXTrader(client, market, risk)

    active_symbol = "TRUMP_USDT"

    while True:
        inr_rate = market.get_inr_rate()
        print_banner()
        auth_status = "[AUTH] AUTHENTICATED" if config.is_authenticated else "[READ-ONLY] READ-ONLY (No Token Set)"
        print(f"Status: {auth_status}  |  Active Pair: {active_symbol}  |  USD/INR: INR {inr_rate:.2f}")
        print("=" * 70)
        print("1. Select Trading Pair")
        print("2. View Pair Specifications (cs, minV, maxL, fees, mmr, etc.)")
        print("3. View Live Market Data (Ticker, Orderbook, Candles, Deals)")
        print("4. Pre-Trade Risk Calculator (Dual Currency USDT & INR)")
        print("5. Account Balances & Portfolio (USDT & INR)")
        print("6. View Open Positions & Stop Orders")
        print("7. Execute Trade (Market / Limit, Long / Short with attached TP/SL)")
        print("8. Add / Modify TP/SL on Open Position")
        print("9. Partially Close Position (e.g. 50%) or Full Close")
        print("10. Cancel Orders")
        print("11. Run Automated Diagnostics / Self-Tests")
        print("0. Exit")
        print("=" * 70)

        choice = input("Select an option (0-11): ").strip()

        if choice == "0":
            print("Exiting KCEX Trading Bot Suite. Happy trading!")
            break

        elif choice == "1":
            print("\n--- SELECT TRADING PAIR ---")
            query = input("Search coin/pair (e.g. TRUMP, DOGE, BTC, ETH) [Enter for popular]: ").strip().upper()
            all_symbols = market.get_symbols()
            if query:
                matched = [s for s in all_symbols if query in s]
            else:
                popular = ["TRUMP_USDT", "DOGE_USDT", "BTC_USDT", "ETH_USDT", "SOL_USDT", "PEPE_USDT", "XRP_USDT"]
                matched = [s for s in popular if s in all_symbols]

            if not matched:
                print(f"No pairs matching '{query}' found.")
                continue

            print("\nAvailable pairs:")
            for i, sym in enumerate(matched[:15], 1):
                print(f"  {i}. {sym}")
            idx_str = input("\nEnter number to select (or enter symbol name directly): ").strip()
            if idx_str.isdigit() and 1 <= int(idx_str) <= len(matched[:15]):
                active_symbol = matched[int(idx_str) - 1]
            elif idx_str.upper() in all_symbols:
                active_symbol = idx_str.upper()
            print(f"Active pair set to: {active_symbol}")

        elif choice == "2":
            print(f"\n--- SPECIFICATIONS FOR {active_symbol} ---")
            try:
                info = market.get_contract_detail(active_symbol)
                ticker = market.get_ticker(active_symbol)
                last_p = float(ticker.get("lastPrice", 0.0))
                min_usdt = info.min_volume * info.contract_size * last_p
                min_inr = min_usdt * inr_rate

                print(f"Symbol                  : {info.symbol}")
                print(f"Base / Quote Coin       : {info.base_coin} / {info.quote_coin}")
                print(f"Contract Size (cs)      : {info.contract_size} {info.base_coin} per contract")
                print(f"Price Tick Size (pu)    : {info.price_unit} (precision: {info.price_precision} decimals)")
                print(f"Volume Step (vu)        : {info.volume_unit} (precision: {info.volume_precision} decimals)")
                print(f"Min Volume (minV)       : {info.min_volume} contract(s)")
                print(f"Max Volume (maxV)       : {info.max_volume:,.0f} contracts")
                print(f"Min / Max Leverage      : {info.min_leverage}x - {info.max_leverage}x")
                print(f"Maintenance Margin (MMR): {info.maintenance_margin_ratio * 100:.2f}%")
                print(f"Initial Margin (IMR)    : {info.initial_margin_ratio * 100:.2f}%")
                print(f"Base Maker Fee Rate     : {info.maker_fee_rate * 100:.4f}%")
                print(f"Base Taker Fee Rate     : {info.taker_fee_rate * 100:.4f}%")
                print(f"Current Last Price      : {last_p:.4f} USDT")
                print(f"Min Order Requirement   : {info.min_volume} contract(s) = {format_inr(min_usdt, inr_rate)}")

                if config.is_authenticated:
                    try:
                        tier = market.get_account_tier_fees(active_symbol)
                        print(f"Your Effective Fees     : Maker {tier['makerFee']*100:.4f}% / Taker {tier['takerFee']*100:.4f}%")
                    except Exception as e:
                        print(f"Could not load account tier fee: {e}")
            except Exception as e:
                print(f"Error fetching contract detail: {e}")

        elif choice == "3":
            print(f"\n--- LIVE MARKET DATA: {active_symbol} ---")
            try:
                ticker = market.get_ticker(active_symbol)
                print(f"Last Price   : {ticker.get('lastPrice')} USDT  (INR {float(ticker.get('lastPrice', 0)) * inr_rate:.2f})")
                print(f"Mark / Fair  : {ticker.get('fairPrice')} USDT  |  Index: {ticker.get('indexPrice')} USDT")
                print(f"Best Bid/Ask : Bid {ticker.get('bid1')} / Ask {ticker.get('ask1')}")
                print(f"24h High/Low : High {ticker.get('high24Price')} / Low {ticker.get('lower24Price')}")
                print(f"24h Volume   : {float(ticker.get('volume24', 0)):,.0f} contracts")
                print(f"Funding Rate : {float(ticker.get('fundingRate', 0)) * 100:.4f}%")

                view_more = input("\nView (B)ook depth, (C)andles, (T)rades, or (Enter) to skip? ").strip().upper()
                if view_more == "B":
                    ob = market.get_order_book(active_symbol)
                    print("\n--- ORDER BOOK (Top 5) ---")
                    print("ASKS (Sells):")
                    for p, v, _ in reversed(ob.get("asks", [])[:5]):
                        print(f"  {p:.4f} USDT  |  {v:,.0f} contracts")
                    print("  -----------------------")
                    print("BIDS (Buys):")
                    for p, v, _ in ob.get("bids", [])[:5]:
                        print(f"  {p:.4f} USDT  |  {v:,.0f} contracts")
                elif view_more == "C":
                    kl = market.get_klines(active_symbol, interval="Min1", limit=5)
                    print("\n--- RECENT 1-MIN CANDLES ---")
                    for c in kl[-5:]:
                        ts_str = time.strftime('%H:%M:%S', time.localtime(c['timestamp']))
                        print(f"  [{ts_str}] O: {c['open']:.4f} H: {c['high']:.4f} L: {c['low']:.4f} C: {c['close']:.4f} Vol: {c['volume']:,.0f}")
                elif view_more == "T":
                    trades = market.get_recent_trades(active_symbol)
                    print("\n--- RECENT TRADES ---")
                    for t in trades[:5]:
                        side_str = "BUY " if t.get("T") == 1 else "SELL"
                        print(f"  {side_str} {t.get('p')} USDT  |  Qty: {t.get('v')}")
            except Exception as e:
                print(f"Market data error: {e}")

        elif choice == "4":
            print(f"\n--- PRE-TRADE RISK & MARGIN CALCULATOR: {active_symbol} ---")
            try:
                contract = market.get_contract_detail(active_symbol)
                ticker = market.get_ticker(active_symbol)
                cur_price = float(ticker.get("lastPrice", 1.0))

                dir_in = input("Direction (1: LONG, 2: SHORT) [1]: ").strip()
                direction = "SHORT" if dir_in == "2" else "LONG"

                lev_in = input(f"Leverage (1 - {contract.max_leverage}) [{min(20, contract.max_leverage)}]: ").strip()
                leverage = int(lev_in) if lev_in.isdigit() else min(20, contract.max_leverage)

                print("\nHow would you like to specify position size?")
                print("1. Contracts volume directly (vol)")
                print("2. USDT notional amount (e.g. 5 USDT)")
                print("3. INR notional amount (e.g. 500 INR)")
                print(f"4. Underlying coins (e.g. 5 {contract.base_coin})")
                size_choice = input("Choice [1]: ").strip()

                if size_choice == "2":
                    usdt_amt = float(input("Enter USDT notional amount: ").strip())
                    vol_contracts = risk.convert_usdt_to_contracts(active_symbol, usdt_amt, cur_price)
                elif size_choice == "3":
                    inr_amt = float(input("Enter INR amount: ").strip())
                    vol_contracts = risk.convert_inr_to_contracts(active_symbol, inr_amt, cur_price)
                elif size_choice == "4":
                    coin_amt = float(input(f"Enter {contract.base_coin} amount: ").strip())
                    vol_contracts = risk.convert_coin_qty_to_contracts(active_symbol, coin_amt)
                else:
                    vol_contracts = int(input(f"Enter volume in contracts (min {contract.min_volume}) [{contract.min_volume}]: ").strip() or contract.min_volume)

                print("\nTP/SL Target Options:")
                print("1. By Price Movement % (e.g. +3% TP, -1.5% SL)")
                print("2. By ROE / Margin Gain % (e.g. +25% ROE TP, -10% ROE SL)")
                print("3. By Absolute Price levels (e.g. $2.40 TP, $2.30 SL)")
                print("4. Skip TP/SL")
                tp_sl_choice = input("Choice [4]: ").strip()

                tp_price, sl_price = None, None
                tp_pct, sl_pct = None, None
                tp_roe, sl_roe = None, None

                if tp_sl_choice == "1":
                    tp_str = input("Take Profit Price % (+): ").strip()
                    sl_str = input("Stop Loss Price % (-): ").strip()
                    tp_pct = float(tp_str) if tp_str else None
                    sl_pct = float(sl_str) if sl_str else None
                elif tp_sl_choice == "2":
                    tp_str = input("Take Profit ROE % (+): ").strip()
                    sl_str = input("Stop Loss ROE % (-): ").strip()
                    tp_roe = float(tp_str) if tp_str else None
                    sl_roe = float(sl_str) if sl_str else None
                elif tp_sl_choice == "3":
                    tp_str = input("Absolute Take Profit Price: ").strip()
                    sl_str = input("Absolute Stop Loss Price: ").strip()
                    tp_price = float(tp_str) if tp_str else None
                    sl_price = float(sl_str) if sl_str else None

                report = risk.analyze_order_risk(
                    symbol=active_symbol,
                    direction=direction,
                    vol_contracts=vol_contracts,
                    entry_price=cur_price,
                    leverage=leverage,
                    tp_price=tp_price,
                    sl_price=sl_price,
                    tp_pct=tp_pct,
                    sl_pct=sl_pct,
                    tp_roe_pct=tp_roe,
                    sl_roe_pct=sl_roe
                )

                print("\n" + report.format_summary())
            except Exception as e:
                print(f"Risk calculation error: {e}")

        elif choice == "5":
            print("\n--- ACCOUNT BALANCES & PORTFOLIO ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing. Please set KCEX_AUTH_TOKEN in environment or .env file.")
                continue
            try:
                bal = trader.get_usdt_balance()
                print(f"Available Balance : {bal['available_usdt']:.4f} USDT  (INR {bal['available_inr']:.2f} INR)")
                print(f"Total Equity      : {bal['equity_usdt']:.4f} USDT  (INR {bal['equity_inr']:.2f} INR)")
                print(f"Unrealized PnL    : {bal['unrealized_pnl_usdt']:.4f} USDT  (INR {bal['unrealized_pnl_inr']:.2f} INR)")
            except Exception as e:
                print(f"Error fetching balance: {e}")

        elif choice == "6":
            print("\n--- OPEN POSITIONS & ORDERS ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing. Please set KCEX_AUTH_TOKEN in environment or .env file.")
                continue
            try:
                positions = trader.get_open_positions()
                print(f"\nActive Open Positions: {len(positions)}")
                for p in positions:
                    print(
                        f"  * ID: {p.get('positionId')} | {p.get('symbol')} {p.get('positionType')} {p.get('leverage')}x | "
                        f"HoldVol: {p.get('holdVol')} contracts | Entry: {p.get('openAvgPrice')} | "
                        f"Liq: {p.get('liquidatePrice')} | Unrealized: {p.get('unrealisedPnl')} USDT"
                    )

                orders = trader.get_open_orders()
                print(f"\nActive Limit/Market Orders: {len(orders)}")
                for o in orders:
                    print(f"  * OrderID: {o.get('orderId')} | {o.get('symbol')} | Vol: {o.get('vol')} | Price: {o.get('price')}")

                stops = trader.get_open_stop_orders()
                print(f"\nActive Stop/Plan Orders: {len(stops)}")
                for s in stops:
                    tp_str = f"TP: {s.get('takeProfitPrice')}" if s.get('takeProfitPrice') else ""
                    sl_str = f"SL: {s.get('stopLossPrice')}" if s.get('stopLossPrice') else ""
                    trigger_str = f"Trigger: {s.get('triggerPrice')}" if s.get('triggerPrice') else ""
                    levels = " | ".join(filter(None, [tp_str, sl_str, trigger_str])) or "Attached"
                    print(f"  * PlanID: {s.get('id')} | {s.get('symbol')} | PosID: {s.get('positionId')} | {levels}")
            except Exception as e:
                print(f"Error fetching positions: {e}")

        elif choice == "7":
            print(f"\n--- EXECUTE TRADE ON {active_symbol} ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing. Please set KCEX_AUTH_TOKEN in environment or .env file.")
                continue

            try:
                contract = market.get_contract_detail(active_symbol)
                ticker = market.get_ticker(active_symbol)
                cur_price = float(ticker.get("lastPrice", 1.0))

                side_in = input("Side (1: BUY/LONG, 2: SELL/SHORT) [1]: ").strip()
                side = "LONG" if side_in != "2" else "SHORT"

                type_in = input("Order Type (1: MARKET, 2: LIMIT) [1]: ").strip()
                order_type = "LIMIT" if type_in == "2" else "MARKET"

                limit_price = None
                if order_type == "LIMIT":
                    limit_price = float(input(f"Enter Limit Price (Current ~{cur_price:.4f}): ").strip())

                vol = int(input(f"Enter volume in contracts (min {contract.min_volume}) [{contract.min_volume}]: ").strip() or contract.min_volume)
                lev = int(input(f"Leverage (1 - {contract.max_leverage}) [{min(20, contract.max_leverage)}]: ").strip() or min(20, contract.max_leverage))

                attach_tp_sl = input("Attach TP/SL with this order? (y/N): ").strip().upper() == "Y"
                tp_val, sl_val = None, None
                if attach_tp_sl:
                    tp_in = input("Take Profit Price: ").strip()
                    sl_in = input("Stop Loss Price: ").strip()
                    tp_val = float(tp_in) if tp_in else None
                    sl_val = float(sl_in) if sl_in else None

                # Safety confirmation
                notional_usdt = vol * contract.contract_size * cur_price
                print("\n[WARNING] ORDER SUMMARY FOR CONFIRMATION:")
                print(f"  Symbol: {active_symbol} | Side: {side} | Type: {order_type} | Vol: {vol} contract(s)")
                print(f"  Exposure: {format_inr(notional_usdt, inr_rate)} | Margin: {format_inr(notional_usdt/lev, inr_rate)}")
                if tp_val: print(f"  Attached TP: {tp_val}")
                if sl_val: print(f"  Attached SL: {sl_val}")

                confirm = input("\nAre you SURE you want to submit this order to KCEX? (yes/NO): ").strip()
                if confirm.lower() != "yes":
                    print("Order cancelled by user.")
                    continue

                res = trader.create_order(
                    symbol=active_symbol,
                    side=side,
                    vol_contracts=vol,
                    order_type=order_type,
                    price=limit_price,
                    leverage=lev,
                    take_profit_price=tp_val,
                    stop_loss_price=sl_val
                )
                print(f"[OK] Order submitted successfully! Response: {res}")
            except Exception as e:
                print(f"[ERROR] Order submission failed: {e}")

        elif choice == "8":
            print(f"\n--- ADD / MODIFY TP/SL ON OPEN POSITION ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing.")
                continue

            try:
                positions = trader.get_open_positions(active_symbol)
                if not positions:
                    # If none on active symbol, search all
                    positions = trader.get_open_positions()
                if not positions:
                    print(f"No open positions found on {active_symbol} or other pairs.")
                    continue

                stops = trader.get_open_stop_orders()

                print(f"Found {len(positions)} open position(s):")
                for i, p in enumerate(positions):
                    pos_id = p.get('positionId')
                    linked_stop = next((s for s in stops if s.get('positionId') == pos_id or s.get('symbol') == p.get('symbol')), None)
                    current_tp = linked_stop.get('takeProfitPrice') if linked_stop else None
                    current_sl = linked_stop.get('stopLossPrice') if linked_stop else None
                    tp_sl_info = f"Current TP: {current_tp or 'None'} | Current SL: {current_sl or 'None'}"
                    side_label = "LONG" if p.get('positionType', 1) == 1 else "SHORT"
                    print(f"  {i+1}. PosID: {pos_id} | {p.get('symbol')} {side_label} | Vol: {p.get('holdVol')} | Entry: {p.get('openAvgPrice')} | {tp_sl_info}")

                p_idx = int(input("Select position number [1]: ").strip() or "1") - 1
                pos = positions[p_idx]
                pos_id = pos.get("positionId")
                sym = pos.get("symbol", active_symbol)

                linked_stop = next((s for s in stops if s.get('positionId') == pos_id or s.get('symbol') == sym), None)
                stop_plan_id = linked_stop.get('id') if linked_stop else None

                print("\nEnter target prices (press Enter without typing to keep current/blank):")
                tp_in = input("New Take Profit Price: ").strip()
                sl_in = input("New Stop Loss Price: ").strip()

                tp_val = float(tp_in) if tp_in else (float(linked_stop.get('takeProfitPrice')) if linked_stop and linked_stop.get('takeProfitPrice') else None)
                sl_val = float(sl_in) if sl_in else (float(linked_stop.get('stopLossPrice')) if linked_stop and linked_stop.get('stopLossPrice') else None)

                res = trader.set_position_tp_sl(
                    symbol=sym,
                    position_id=pos_id,
                    take_profit_price=tp_val,
                    stop_loss_price=sl_val,
                    stop_plan_order_id=stop_plan_id
                )
                print(f"[OK] TP/SL updated successfully! Response: {res}")
            except Exception as e:
                print(f"[ERROR] Failed to set TP/SL: {e}")

        elif choice == "9":
            print(f"\n--- PARTIAL OR FULL POSITION CLOSE ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing.")
                continue

            try:
                positions = trader.get_open_positions(active_symbol)
                if not positions:
                    positions = trader.get_open_positions()
                if not positions:
                    print(f"No open positions found on {active_symbol}.")
                    continue

                for i, p in enumerate(positions):
                    print(f"  {i+1}. ID: {p.get('positionId')} | HoldVol: {p.get('holdVol')} contracts | Entry: {p.get('openAvgPrice')}")

                p_idx = int(input("Select position number [1]: ").strip() or "1") - 1
                pos = positions[p_idx]
                pos_id = pos.get("positionId")
                hold_vol = int(pos.get("holdVol", 1))
                lev = int(pos.get("leverage", 20))
                side = "LONG" if pos.get("positionType", 1) == 1 else "SHORT"

                close_mode = input("Close percentage (50 for 50%, 100 for Full Market Close) [100]: ").strip() or "100"
                close_pct = float(close_mode)

                confirm = input(f"Confirm closing {close_pct}% of position {pos_id}? (yes/NO): ").strip()
                if confirm.lower() != "yes":
                    print("Close cancelled.")
                    continue

                if close_pct >= 100:
                    res = trader.close_position(
                        position_id=pos_id,
                        symbol=active_symbol,
                        side=side,
                        vol_contracts=hold_vol,
                        leverage=lev,
                        is_market=True
                    )
                else:
                    res = trader.close_partial_position(
                        position_id=pos_id,
                        symbol=active_symbol,
                        side=side,
                        total_vol=hold_vol,
                        leverage=lev,
                        close_percentage=close_pct
                    )
                print(f"[OK] Close order submitted! Response: {res}")
            except Exception as e:
                print(f"[ERROR] Close failed: {e}")

        elif choice == "10":
            print(f"\n--- ORDER & POSITION MANAGEMENT (CANCEL / CLOSE) ---")
            if not config.is_authenticated:
                print("[ERROR] Authentication token missing.")
                continue
            try:
                orders = trader.get_open_orders()
                stops = trader.get_open_stop_orders()
                positions = trader.get_open_positions()

                print(f"\n1. Active Limit/Market Orders: {len(orders)}")
                if not orders:
                    print("   (None - Note: Market orders fill instantly upon creation and become Open Positions)")
                for idx, o in enumerate(orders):
                    print(f"   [{idx+1}] OrderID: {o.get('orderId')} | {o.get('symbol')} | Vol: {o.get('vol')} | Price: {o.get('price')}")

                print(f"\n2. Active Stop/Plan Orders (TP/SL): {len(stops)}")
                if not stops:
                    print("   (None)")
                for idx, s in enumerate(stops):
                    tp_str = f"TP: {s.get('takeProfitPrice')}" if s.get('takeProfitPrice') else ""
                    sl_str = f"SL: {s.get('stopLossPrice')}" if s.get('stopLossPrice') else ""
                    trigger_str = f"Trigger: {s.get('triggerPrice')}" if s.get('triggerPrice') else ""
                    levels = " | ".join(filter(None, [tp_str, sl_str, trigger_str])) or "Attached"
                    print(f"   [{idx+1}] PlanID: {s.get('id')} | {s.get('symbol')} | PosID: {s.get('positionId')} | {levels}")

                print(f"\n3. Active Open Positions: {len(positions)}")
                if not positions:
                    print("   (None)")
                for idx, p in enumerate(positions):
                    side_label = "LONG" if p.get('positionType', 1) == 1 else "SHORT"
                    print(f"   [{idx+1}] PosID: {p.get('positionId')} | {p.get('symbol')} {side_label} {p.get('leverage')}x | Vol: {p.get('holdVol')} | Entry: {p.get('openAvgPrice')}")

                if not orders and not stops and not positions:
                    print("\nNo active orders, stop orders, or positions to manage.")
                    continue

                print("\nOptions:")
                print("1. Cancel an Ordinary Limit/Market Order (by index or OrderID)")
                print("2. Cancel a Stop / Plan Order (TP/SL) (by index or PlanID)")
                print("3. Emergency Close an Open Position (Market Close)")
                print("4. Cancel ALL Orders (Ordinary + Stop Orders)")
                print("0. Back to Menu")
                act = input("Select an action [0]: ").strip()

                if act == "1":
                    if not orders:
                        print("[NOTE] There are currently 0 active unfilled limit orders.")
                        print("       - Market orders execute immediately and become Open Positions.")
                        print("       - To exit/close an open position, use Action 3 below or Option 9 from the main menu.")
                        continue
                    oid_in = input(f"Select order number [1-{len(orders)}] or enter OrderID: ").strip()
                    if oid_in.isdigit() and 1 <= int(oid_in) <= len(orders):
                        oid = str(orders[int(oid_in) - 1].get("orderId"))
                    else:
                        oid = oid_in
                    if oid:
                        matched_pos = next((p for p in positions if str(p.get("positionId")) == oid), None)
                        if matched_pos:
                            print(f"[NOTE] {oid} is a Position ID, not an unfilled order.")
                            print("       In futures trading, open positions cannot be 'cancelled'; they must be 'closed'.")
                            print("       Use Action 3 to close this position at market price.")
                            continue
                        res = trader.cancel_order(order_id=oid)
                        print(f"[OK] Cancel order sent: {res}")
                elif act == "2":
                    if not stops:
                        print("[NOTE] There are currently 0 active stop/plan orders to cancel.")
                        continue
                    pid_in = input(f"Select stop order number [1-{len(stops)}] or enter PlanID: ").strip()
                    if pid_in.isdigit() and 1 <= int(pid_in) <= len(stops):
                        pid = stops[int(pid_in) - 1].get("id")
                    else:
                        pid = pid_in
                    if pid:
                        res = trader.cancel_stop_order(stop_plan_order_id=int(pid))
                        print(f"[OK] Cancel stop order sent: {res}")
                elif act == "3":
                    if not positions:
                        print("[NOTE] No active open positions to close.")
                        continue
                    if len(positions) == 1:
                        target_pos = positions[0]
                        side = "LONG" if target_pos.get('positionType', 1) == 1 else "SHORT"
                        c_in = input(f"Confirm 100% market close of position {target_pos['positionId']} ({target_pos.get('symbol', active_symbol)} {side})? (yes/NO): ").strip()
                        if c_in.lower() != "yes":
                            print("Close cancelled.")
                            continue
                    else:
                        p_sel = input(f"Select position number to close [1-{len(positions)}] or enter PosID: ").strip()
                        if p_sel.isdigit() and 1 <= int(p_sel) <= len(positions):
                            target_pos = positions[int(p_sel) - 1]
                        else:
                            target_pos = next((p for p in positions if str(p.get("positionId")) == p_sel), None)
                        if not target_pos:
                            print("Position not found.")
                            continue
                        side = "LONG" if target_pos.get('positionType', 1) == 1 else "SHORT"

                    res = trader.close_position(
                        position_id=int(target_pos["positionId"]),
                        symbol=target_pos.get("symbol", active_symbol),
                        side=side,
                        vol_contracts=int(target_pos.get("holdVol", 1)),
                        leverage=int(target_pos.get("leverage", 20)),
                        is_market=True
                    )
                    print(f"[OK] Position closed: {res}")
                elif act == "4":
                    sym_filter = input(f"Filter by active pair {active_symbol}? (y/N): ").strip().upper() == "Y"
                    target_sym = active_symbol if sym_filter else None
                    res = trader.cancel_all_orders(symbol=target_sym)
                    print(f"[OK] Cancel all completed: {res}")
            except Exception as e:
                print(f"[ERROR] Action failed: {e}")

        elif choice == "11":
            run_automated_tests()

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KCEX Futures Trade Management & Testing")
    parser.add_argument("--test", action="store_true", help="Run automated non-destructive self-tests")
    args = parser.parse_args()

    if args.test:
        run_automated_tests()
    else:
        interactive_cli()
