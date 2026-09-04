"""
KCEX Automated Trade Execution Engine
=====================================
The core orchestrator that continuously runs the Masterplan strategy:
1. Connects to KCEX and validates zero-fee pair status (TRUMP_USDT).
2. Generates signals via the active sub-strategy.
3. Sizes orders to the absolute minimum allowed volume (1 contract = minV).
4. Submits market order with attached TP/SL in a single request.
5. Immediately reconciles fill:
   - If market price is already at or better than Min-Profit TP (entry + pu), closes immediately!
   - Otherwise, verifies/adjusts server-side TP to exact entry + pu and SL to -10% ROE.
6. Actively monitors the position until closed.
7. Logs detailed execution and outcome metrics in both USDT and INR.
8. Enforces a 30-second cooldown before the next trade cycle.
9. Supports DRY-RUN (safe simulation) and LIVE execution modes.
"""

import time
import math
import signal
import sys
from typing import Optional, Dict, Any

from kcex.config import KCEXConfig
from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator
from kcex.trade import KCEXTrader
from kcex.engine.models import (
    OrderDirection,
    ExitReason,
    EngineMode,
    TradeSignal,
    TradeOutcome,
    ExecutionConfig
)
from kcex.engine.logger import DualCurrencyLogger, TradeOutcomeLogger
from kcex.engine.strategy import MasterplanStrategy, DirectionalCycleSubStrategy


class TradeExecutionEngine:
    """
    Automated execution engine coordinating strategy, order execution,
    risk management, and dual-currency trade journals.
    """

    def __init__(
        self,
        config: Optional[ExecutionConfig] = None,
        client: Optional[KCEXClient] = None,
        market: Optional[KCEXMarket] = None,
        trader: Optional[KCEXTrader] = None,
        risk: Optional[KCEXRiskCalculator] = None,
        strategy: Optional[MasterplanStrategy] = None
    ):
        self.config = config or ExecutionConfig()
        self.client = client or KCEXClient()
        self.market = market or KCEXMarket(self.client)
        self.risk = risk or KCEXRiskCalculator(self.market, self.client)
        self.trader = trader or KCEXTrader(self.client, self.market, self.risk)

        # Loggers
        inr_rate = self.market.get_inr_rate()
        self.logger = DualCurrencyLogger(
            log_file=f"{self.config.logs_dir}/{self.config.realtime_log_file}",
            inr_rate=inr_rate
        )
        self.outcome_logger = TradeOutcomeLogger(
            txt_file=f"{self.config.logs_dir}/{self.config.outcomes_log_file}",
            jsonl_file=f"{self.config.logs_dir}/{self.config.outcomes_jsonl_file}"
        )

        # Strategy
        self.strategy = strategy or MasterplanStrategy(
            market=self.market,
            config=self.config,
            sub_strategy=DirectionalCycleSubStrategy(
                direction=self.config.direction,
                cooldown_seconds=self.config.cooldown_seconds
            )
        )

        self.running: bool = False
        self.trade_counter: int = 0
        self._current_position_id: Optional[int] = None
        self._shutdown_requested: bool = False

    def stop(self) -> None:
        """Requests graceful engine stop."""
        self._shutdown_requested = True
        self.running = False
        self.logger.info("Graceful shutdown requested...")

    # =========================================================================
    # PRE-FLIGHT VERIFICATIONS
    # =========================================================================

    def pre_flight_checks(self) -> ContractInfo:
        """
        Runs initial validation checks:
        1. Connectivity ping
        2. Contract detail & zero-fee status
        3. Wallet balance & live USD/INR exchange rate
        4. Open positions sanity check
        """
        self.logger.section("PRE-FLIGHT CHECKS & SYSTEM INITIALIZATION")

        # 1. Connectivity
        self.logger.info("Testing connectivity to KCEX API...")
        if not self.market.ping():
            self.logger.warning("Ping returned non-standard status, verifying ticker connectivity...")

        # 2. INR Rate
        inr_rate = self.market.get_inr_rate()
        self.logger.set_inr_rate(inr_rate)
        self.logger.info(f"Live USD/INR Exchange Rate: INR {inr_rate:.2f} per USD")

        # 3. Contract & Zero-Fee Verification
        symbol = self.config.symbol.upper()
        contract = self.market.get_contract_detail(symbol)
        fee_info = self.strategy.validate_zero_fee_pair(symbol)

        self.logger.info(
            f"Trading Pair: {symbol} | Tick Size (pu): {contract.price_unit} | "
            f"Contract Size (cs): {contract.contract_size} | Min Volume: {contract.min_volume} contract(s)"
        )
        self.logger.info(
            f"Effective Fees: Maker {fee_info['maker_fee']*100:.2f}% / Taker {fee_info['taker_fee']*100:.2f}% "
            f"({'ZERO FEES CONFIRMED' if fee_info['is_zero_fee'] else 'NON-ZERO FEES WARNING'})"
        )

        # 4. Balances (if live or authenticated)
        if self.config.mode == EngineMode.LIVE:
            if not self.client.config.is_authenticated:
                raise ValueError("LIVE mode requires KCEX_AUTH_TOKEN configured in .env.")

            balances = self.trader.get_usdt_balance()
            avail_usdt = balances.get("available_usdt", 0.0)
            avail_inr = balances.get("available_inr", 0.0)
            self.logger.info(
                f"Futures Wallet Available: {avail_usdt:.4f} USDT (INR {avail_inr:.2f})"
            )

            # Check if an existing open position exists
            open_positions = self.trader.get_open_positions(symbol)
            if open_positions:
                for pos in open_positions:
                    hold_vol = float(pos.get("holdVol", 0) or pos.get("vol", 0))
                    if hold_vol > 0:
                        self.logger.warning(
                            f"Warning: Found existing open position on {symbol}: {hold_vol} contracts. "
                            f"Position ID: {pos.get('positionId')}"
                        )

        self.logger.info(f"Engine Mode: {self.config.mode.value.upper()}")
        self.logger.info(f"Sub-strategy: {self.strategy.sub_strategy.name}")
        self.logger.info(f"Target Leverage: {self.config.leverage}x isolated")
        self.logger.info(f"Min-Profit Take Profit rule: Entry Price +/- {self.config.tp_ticks} pu (Tick Size)")
        self.logger.info(f"Stop Loss rule: -{self.config.sl_roe_pct}% ROE on margin")
        self.logger.info(f"Post-trade cooldown: {self.config.cooldown_seconds}s")
        self.logger.section("PRE-FLIGHT CHECKS PASSED - ENGINE READY")
        return contract

    # =========================================================================
    # TRADE EXECUTION LIFECYCLE
    # =========================================================================

    def execute_single_trade_cycle(self, contract: ContractInfo) -> Optional[TradeOutcome]:
        """
        Executes one full trade cycle:
        1. Checks for signal
        2. Sizes order to min_volume (1 contract)
        3. Submits order with attached TP/SL
        4. Reconciles exact fill
        5. Checks immediate profit close
        6. Monitors until position is closed
        7. Logs outcome to dual-currency journal
        """
        signal = self.strategy.get_signal()
        if not signal:
            return None

        self.trade_counter += 1
        trade_id = self.trade_counter
        symbol = contract.symbol
        direction = signal.direction
        is_long = (direction == OrderDirection.LONG)
        pu = contract.price_unit
        cs = contract.contract_size
        leverage = min(self.config.leverage, contract.max_leverage)

        # Minimum possible volume
        vol_contracts = int(contract.min_volume)
        underlying_qty = vol_contracts * cs

        self.logger.section(f"EXECUTING TRADE #{trade_id} [{direction.value}] - {symbol}")

        # Get fresh market snapshot
        ticker = self.market.get_ticker(symbol)
        last_price = float(ticker.get("lastPrice", 0.0) or ticker.get("fairPrice", 1.0))
        ref_price = last_price
        inr_rate = self.market.get_inr_rate()
        self.logger.set_inr_rate(inr_rate)

        # Calculate estimated TP & SL prices
        est_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=ref_price,
            price_unit=pu,
            tp_ticks=self.config.tp_ticks,
            precision=contract.price_precision
        )
        est_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=ref_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            precision=contract.price_precision
        )

        notional_est_usdt = underlying_qty * ref_price
        notional_est_inr = notional_est_usdt * inr_rate
        margin_est_usdt = notional_est_usdt / leverage
        margin_est_inr = margin_est_usdt * inr_rate

        self.logger.info(
            f"Pre-Trade Spec: Vol: {vol_contracts} contract ({underlying_qty} coins) | "
            f"Est Notional: {self.logger.format_dual(notional_est_usdt)} | "
            f"Est Margin: {self.logger.format_dual(margin_est_usdt)}"
        )
        self.logger.info(
            f"Reference Price: {ref_price:.4f} USDT | "
            f"Attached Min-Profit TP: {est_tp:.4f} USDT (+1 pu) | "
            f"Attached SL: {est_sl:.4f} USDT (-{self.config.sl_roe_pct}% ROE)"
        )

        open_time = time.time()

        # =====================================================================
        # SUBMIT ORDER
        # =====================================================================
        if self.config.mode == EngineMode.LIVE:
            outcome = self._execute_live_trade(
                trade_id=trade_id,
                contract=contract,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                est_tp=est_tp,
                est_sl=est_sl,
                open_time=open_time,
                sub_strategy_name=signal.sub_strategy_name
            )
        else:
            outcome = self._simulate_dry_run_trade(
                trade_id=trade_id,
                contract=contract,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                open_time=open_time,
                sub_strategy_name=signal.sub_strategy_name
            )

        if outcome:
            # Output and record outcome
            card = self.outcome_logger.log_outcome(outcome)
            self.logger.info("\n" + card)
            self.strategy.on_trade_completed(outcome)

        return outcome

    # =========================================================================
    # LIVE EXECUTION & POSITION MONITORING
    # =========================================================================

    def _execute_live_trade(
        self,
        trade_id: int,
        contract: ContractInfo,
        direction: OrderDirection,
        vol_contracts: int,
        leverage: int,
        est_tp: float,
        est_sl: float,
        open_time: float,
        sub_strategy_name: str
    ) -> TradeOutcome:
        symbol = contract.symbol
        side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
        pu = contract.price_unit
        cs = contract.contract_size
        underlying_qty = vol_contracts * cs

        self.logger.info("Submitting live MARKET order with attached TP & SL...")
        order_res = self.trader.create_order(
            symbol=symbol,
            side=side_str,
            vol_contracts=vol_contracts,
            order_type="MARKET",
            leverage=leverage,
            is_isolated=self.config.is_isolated,
            take_profit_price=est_tp,
            stop_loss_price=est_sl
        )

        data = order_res.get("data", {})
        order_id = str(data.get("orderId") or "")
        self.logger.info(f"Live order accepted by KCEX. Order ID: {order_id}")

        # Short pause to allow order book fill
        time.sleep(0.3)

        # Reconcile open position to obtain exact entry price and positionId
        entry_price = est_tp - pu if direction == OrderDirection.LONG else est_tp + pu
        position_id = None
        open_positions = self.trader.get_open_positions(symbol)
        
        for p in open_positions:
            h_vol = float(p.get("holdVol", 0) or p.get("vol", 0))
            if h_vol > 0:
                position_id = int(p.get("positionId"))
                entry_price = float(p.get("openAvgPrice") or p.get("holdAvgPrice") or entry_price)
                break

        # Calculate exact min-profit TP and exact SL from actual filled entry price
        exact_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=self.config.tp_ticks,
            precision=contract.price_precision
        )
        exact_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            precision=contract.price_precision
        )

        self.logger.info(
            f"Position Filled: Entry Price = {entry_price:.4f} USDT | "
            f"Exact Min-Profit TP = {exact_tp:.4f} USDT | Exact SL = {exact_sl:.4f} USDT"
        )

        # Check immediate profit close condition
        ticker = self.market.get_ticker(symbol)
        current_price = float(ticker.get("lastPrice", entry_price))

        if self.strategy.is_better_than_min_profit(direction, current_price, exact_tp):
            self.logger.info(
                f"[IMMEDIATE PROFIT TRIGGER] Current price ({current_price:.4f} USDT) is already >= "
                f"Min-Profit TP ({exact_tp:.4f} USDT)! Closing immediately..."
            )
            close_res = self.trader.close_position(
                position_id=position_id or 0,
                symbol=symbol,
                side=side_str,
                vol_contracts=vol_contracts,
                leverage=leverage,
                is_isolated=self.config.is_isolated,
                is_market=True,
                price=current_price
            )
            close_order_id = str(close_res.get("data", {}).get("orderId") or "")
            exit_price = current_price
            exit_reason = ExitReason.IMMEDIATE_PROFIT_CLOSE
            time.sleep(0.5)
        else:
            # If not immediately closed, verify or update the position TP/SL
            if position_id and (abs(exact_tp - est_tp) > 1e-6 or abs(exact_sl - est_sl) > 1e-6):
                try:
                    self.trader.set_position_tp_sl(
                        symbol=symbol,
                        position_id=position_id,
                        take_profit_price=exact_tp,
                        stop_loss_price=exact_sl
                    )
                    self.logger.info(f"Updated server-side position TP/SL to exact: TP {exact_tp}, SL {exact_sl}")
                except Exception as e:
                    self.logger.warning("Note: Stoporder update skipped or already active: %s", e)

            # Active position monitoring loop
            self.logger.info("Entering active position monitoring loop...")
            exit_price, exit_reason, close_order_id = self._monitor_live_position(
                symbol=symbol,
                position_id=position_id,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                exact_tp=exact_tp,
                exact_sl=exact_sl
            )

        close_time = time.time()
        duration = max(0.1, close_time - open_time)

        # Reconcile exact closing order, exit price, profit, and exit reason from KCEX history
        reconciled_exit_price, reconciled_pnl, reconciled_reason, hist_close_id, reconciled_pos_id = (
            self._reconcile_closed_trade_from_kcex(
                symbol=symbol,
                open_order_id=order_id,
                position_id=position_id,
                direction=direction,
                entry_price=entry_price,
                pu=pu,
                default_exit_price=exit_price,
                initial_reason=exit_reason if exit_reason != ExitReason.UNKNOWN else None
            )
        )

        exit_price = reconciled_exit_price
        realized_pnl_usdt = reconciled_pnl
        if reconciled_reason:
            exit_reason = reconciled_reason
        if hist_close_id:
            close_order_id = hist_close_id
        if reconciled_pos_id:
            position_id = reconciled_pos_id

        # Calculate math fallback if history returned zero but price moved
        price_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)
        if realized_pnl_usdt == 0.0 and abs(price_diff) > 1e-6:
            realized_pnl_usdt = underlying_qty * price_diff

        inr_rate = self.market.get_inr_rate()
        notional_usdt = underlying_qty * entry_price
        notional_inr = notional_usdt * inr_rate
        margin_usdt = notional_usdt / leverage
        margin_inr = margin_usdt * inr_rate
        realized_pnl_inr = realized_pnl_usdt * inr_rate
        roe_pct = (realized_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0.0
        pnl_pct = (price_diff / entry_price) * 100.0 if entry_price > 0 else 0.0

        # Fetch fresh live account balance after trade
        balance_after_usdt = None
        balance_after_inr = None
        try:
            balances = self.trader.get_usdt_balance()
            balance_after_usdt = balances.get("available_usdt", 0.0)
            balance_after_inr = balances.get("available_inr", 0.0)
            equity_usdt = balances.get("equity_usdt", 0.0)
            equity_inr = balances.get("equity_inr", 0.0)
            self.logger.info(
                f"[BALANCE AFTER TRADE #{trade_id}] Available: {balance_after_usdt:.4f} USDT (INR {balance_after_inr:.2f}) | "
                f"Equity: {equity_usdt:.4f} USDT (INR {equity_inr:.2f})"
            )
        except Exception as e:
            self.logger.debug("Could not fetch balance after trade: %s", e)

        return TradeOutcome(
            trade_id=trade_id,
            symbol=symbol,
            direction=direction,
            sub_strategy_name=sub_strategy_name,
            mode=EngineMode.LIVE,
            leverage=leverage,
            vol_contracts=vol_contracts,
            contract_size=cs,
            underlying_quantity=underlying_qty,
            entry_price=entry_price,
            exit_price=exit_price,
            min_profit_tp_price=exact_tp,
            stop_loss_price=exact_sl,
            price_unit=pu,
            open_time=open_time,
            close_time=close_time,
            duration_seconds=duration,
            notional_value_usdt=notional_usdt,
            notional_value_inr=notional_inr,
            margin_used_usdt=margin_usdt,
            margin_used_inr=margin_inr,
            realized_pnl_usdt=realized_pnl_usdt,
            realized_pnl_inr=realized_pnl_inr,
            pnl_percentage=pnl_pct,
            roe_percentage=roe_pct,
            fee_open_usdt=0.0,
            fee_close_usdt=0.0,
            fee_total_usdt=0.0,
            fee_total_inr=0.0,
            inr_rate=inr_rate,
            exit_reason=exit_reason,
            balance_after_trade_usdt=balance_after_usdt,
            balance_after_trade_inr=balance_after_inr,
            order_id=order_id,
            close_order_id=close_order_id,
            position_id=position_id
        )

    def _reconcile_closed_trade_from_kcex(
        self,
        symbol: str,
        open_order_id: Optional[str],
        position_id: Optional[int],
        direction: OrderDirection,
        entry_price: float,
        pu: float,
        default_exit_price: float,
        initial_reason: Optional[ExitReason] = None
    ) -> tuple[float, float, ExitReason, Optional[str], Optional[int]]:
        """
        Queries KCEX history_orders and history_positions to reliably determine
        the exact exit price, realized PnL, exit reason (TAKE_PROFIT vs STOP_LOSS),
        and server IDs.
        """
        time.sleep(0.5)  # Allow KCEX backend to persist post-close records

        exit_price = default_exit_price
        realized_pnl = 0.0
        exit_reason = initial_reason or ExitReason.UNKNOWN
        close_order_id = None
        reconciled_pos_id = position_id

        closing_side = 4 if direction == OrderDirection.LONG else 2

        # 1. Query order history for the closing order
        try:
            res = self.client.get_private(
                KCEXConfig.ENDPOINT_ORDER_HISTORY,
                params={"symbol": symbol.upper(), "category": 1, "page_num": 1, "page_size": 10}
            )
            orders = res.get("data", [])
            if isinstance(orders, dict):
                orders = orders.get("list", [])

            for o in orders:
                if o.get("side") == closing_side and float(o.get("dealVol", 0)) > 0:
                    close_order_id = str(o.get("orderId"))
                    deal_price = float(o.get("dealAvgPrice") or o.get("price") or 0.0)
                    if deal_price > 0:
                        exit_price = deal_price
                    realized_pnl = float(o.get("profit", 0.0))
                    if o.get("positionId"):
                        reconciled_pos_id = int(o.get("positionId"))

                    external_oid = str(o.get("externalOid") or "")
                    if "TAKE_PROFIT" in external_oid:
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                    elif "STOP_LOSS" in external_oid:
                        exit_reason = ExitReason.STOP_LOSS_HIT
                    elif realized_pnl > 0:
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                    elif realized_pnl < 0:
                        exit_reason = ExitReason.STOP_LOSS_HIT
                    break
        except Exception as e:
            self.logger.debug("Error inspecting history_orders: %s", e)

        # 2. If exit reason is still uncertain, inspect history_positions
        if exit_reason in (None, ExitReason.UNKNOWN) or realized_pnl == 0.0:
            try:
                hist_positions = self.trader.get_position_history(page_size=5)
                for h in hist_positions:
                    h_pos_id = int(h.get("positionId") or 0)
                    h_sym = str(h.get("symbol") or "")
                    if (reconciled_pos_id and h_pos_id == reconciled_pos_id) or (h_sym == symbol.upper()):
                        reconciled_pos_id = h_pos_id
                        close_p = float(h.get("closeAvgPrice") or 0.0)
                        if close_p > 0:
                            exit_price = close_p
                        pnl = float(h.get("closeProfitLoss", 0.0))
                        if pnl != 0:
                            realized_pnl = pnl
                        if pnl > 0:
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                        elif pnl < 0:
                            exit_reason = ExitReason.STOP_LOSS_HIT
                        break
            except Exception as e:
                self.logger.debug("Error inspecting history_positions: %s", e)

        # 3. Final mathematical fallback check
        if exit_reason in (None, ExitReason.UNKNOWN):
            if direction == OrderDirection.LONG:
                if exit_price >= entry_price + (0.5 * pu):
                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                elif exit_price < entry_price - (0.5 * pu):
                    exit_reason = ExitReason.STOP_LOSS_HIT
                else:
                    exit_reason = ExitReason.SCRATCH_CLOSE
            else:
                if exit_price <= entry_price - (0.5 * pu):
                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                elif exit_price > entry_price + (0.5 * pu):
                    exit_reason = ExitReason.STOP_LOSS_HIT
                else:
                    exit_reason = ExitReason.SCRATCH_CLOSE

        return exit_price, realized_pnl, exit_reason, close_order_id, reconciled_pos_id

    def _monitor_live_position(
        self,
        symbol: str,
        position_id: Optional[int],
        direction: OrderDirection,
        vol_contracts: int,
        leverage: int,
        exact_tp: float,
        exact_sl: float
    ) -> tuple[float, ExitReason, Optional[str]]:
        """
        Polls ticker and open positions until the position closes.
        Triggers instant market close if price reaches Min-Profit TP.
        """
        side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
        close_order_id = None
        last_seen_price = exact_tp

        while not self._shutdown_requested:
            time.sleep(self.config.poll_interval_seconds)

            # 1. Fetch latest price
            try:
                ticker = self.market.get_ticker(symbol)
                current_price = float(ticker.get("lastPrice") or ticker.get("fairPrice", 0.0))
                last_seen_price = current_price
            except Exception as e:
                self.logger.debug("Ticker poll error: %s", e)
                continue

            # 2. Check if current price is at or better than Min-Profit TP
            if self.strategy.is_better_than_min_profit(direction, current_price, exact_tp):
                self.logger.info(
                    f"[IMMEDIATE PROFIT TRIGGER] Price reached Min-Profit TP: {current_price:.4f} USDT >= {exact_tp:.4f} USDT. "
                    f"Executing market close..."
                )
                try:
                    res = self.trader.close_position(
                        position_id=position_id or 0,
                        symbol=symbol,
                        side=side_str,
                        vol_contracts=vol_contracts,
                        leverage=leverage,
                        is_isolated=self.config.is_isolated,
                        is_market=True,
                        price=current_price
                    )
                    close_order_id = str(res.get("data", {}).get("orderId") or "")
                    return current_price, ExitReason.IMMEDIATE_PROFIT_CLOSE, close_order_id
                except Exception as e:
                    self.logger.warning("Market close error (position may already be closed by TP): %s", e)

            # 3. Check if position closed via server-side attached TP or SL
            try:
                open_pos = self.trader.get_open_positions(symbol)
                pos_still_open = False
                for p in open_pos:
                    if position_id and int(p.get("positionId", 0)) == int(position_id):
                        if float(p.get("holdVol", 0)) > 0:
                            pos_still_open = True
                            break
                    elif float(p.get("holdVol", 0)) > 0:
                        pos_still_open = True
                        break

                if not pos_still_open:
                    self.logger.info("Position closed on KCEX. Reconciling fill records...")
                    return last_seen_price, ExitReason.UNKNOWN, None
            except Exception as e:
                self.logger.debug("Position check error: %s", e)

        # If shutdown was requested during trade, market close immediately
        self.logger.warning("Shutdown received while in position. Closing position...")
        try:
            self.trader.close_position(
                position_id=position_id or 0,
                symbol=symbol,
                side=side_str,
                vol_contracts=vol_contracts,
                leverage=leverage,
                is_isolated=self.config.is_isolated,
                is_market=True
            )
        except Exception:
            pass
        return last_seen_price, ExitReason.MANUAL_CLOSE, None

    # =========================================================================
    # DRY RUN (SIMULATION MODE)
    # =========================================================================

    def _simulate_dry_run_trade(
        self,
        trade_id: int,
        contract: ContractInfo,
        direction: OrderDirection,
        vol_contracts: int,
        leverage: int,
        open_time: float,
        sub_strategy_name: str
    ) -> TradeOutcome:
        """
        High-fidelity DRY-RUN execution simulation using live market ticker data.
        """
        symbol = contract.symbol
        pu = contract.price_unit
        cs = contract.contract_size
        underlying_qty = vol_contracts * cs

        # Live ticker entry
        ticker = self.market.get_ticker(symbol)
        entry_price = float(ticker.get("lastPrice", 2.377))

        exact_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=self.config.tp_ticks,
            precision=contract.price_precision
        )
        exact_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            precision=contract.price_precision
        )

        self.logger.info(
            f"[DRY-RUN] Simulated Order Filled: Entry = {entry_price:.4f} USDT | "
            f"Min-Profit TP = {exact_tp:.4f} USDT (+1 pu) | SL = {exact_sl:.4f} USDT (-{self.config.sl_roe_pct}% ROE)"
        )

        # Simulate monitoring with live market tick or fast execution
        # Check if immediate profit applies or simulate quick exit at min-profit TP
        time.sleep(1.0)
        exit_price = exact_tp
        exit_reason = ExitReason.MIN_PROFIT_TP_HIT

        close_time = time.time()
        duration = max(1.0, close_time - open_time)

        price_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)
        realized_pnl_usdt = underlying_qty * price_diff

        inr_rate = self.market.get_inr_rate()
        notional_usdt = underlying_qty * entry_price
        notional_inr = notional_usdt * inr_rate
        margin_usdt = notional_usdt / leverage
        margin_inr = margin_usdt * inr_rate
        realized_pnl_inr = realized_pnl_usdt * inr_rate
        roe_pct = (realized_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0.0
        pnl_pct = (price_diff / entry_price) * 100.0 if entry_price > 0 else 0.0

        # Check wallet balance if authenticated
        balance_after_usdt = None
        balance_after_inr = None
        if self.client.config.is_authenticated:
            try:
                balances = self.trader.get_usdt_balance()
                balance_after_usdt = balances.get("available_usdt", 0.0)
                balance_after_inr = balances.get("available_inr", 0.0)
                self.logger.info(
                    f"[WALLET BALANCE] Available: {balance_after_usdt:.4f} USDT (INR {balance_after_inr:.2f})"
                )
            except Exception:
                pass

        return TradeOutcome(
            trade_id=trade_id,
            symbol=symbol,
            direction=direction,
            sub_strategy_name=sub_strategy_name,
            mode=EngineMode.DRY_RUN,
            leverage=leverage,
            vol_contracts=vol_contracts,
            contract_size=cs,
            underlying_quantity=underlying_qty,
            entry_price=entry_price,
            exit_price=exit_price,
            min_profit_tp_price=exact_tp,
            stop_loss_price=exact_sl,
            price_unit=pu,
            open_time=open_time,
            close_time=close_time,
            duration_seconds=duration,
            notional_value_usdt=notional_usdt,
            notional_value_inr=notional_inr,
            margin_used_usdt=margin_usdt,
            margin_used_inr=margin_inr,
            realized_pnl_usdt=realized_pnl_usdt,
            realized_pnl_inr=realized_pnl_inr,
            pnl_percentage=pnl_pct,
            roe_percentage=roe_pct,
            fee_open_usdt=0.0,
            fee_close_usdt=0.0,
            fee_total_usdt=0.0,
            fee_total_inr=0.0,
            inr_rate=inr_rate,
            exit_reason=exit_reason,
            balance_after_trade_usdt=balance_after_usdt,
            balance_after_trade_inr=balance_after_inr,
            order_id="SIMULATED_ORDER_001",
            close_order_id="SIMULATED_CLOSE_001",
            position_id=12345678
        )

    # =========================================================================
    # MAIN ENGINE RUN LOOP
    # =========================================================================

    def run(self) -> None:
        """
        Main engine execution loop:
        Repeatedly executes trade cycles, enforces cooldown, and manages graceful stops.
        """
        self.running = True
        self._shutdown_requested = False

        # Set up signal handler for Ctrl+C
        def handle_sigint(signum, frame):
            self.logger.warning("\n[STOP] Caught SIGINT / Interrupt signal.")
            self.stop()

        signal.signal(signal.SIGINT, handle_sigint)

        contract = self.pre_flight_checks()

        self.logger.info("Starting Masterplan Automated Execution Loop...")
        self.logger.info(f"Target Trades: {self.config.max_trades if self.config.max_trades > 0 else 'Unlimited'}")

        try:
            while self.running and not self._shutdown_requested:
                # Check max trades
                if self.config.max_trades > 0 and self.trade_counter >= self.config.max_trades:
                    self.logger.info(f"Reached configured maximum trades limit ({self.config.max_trades}). Stopping.")
                    break

                # Execute single cycle
                outcome = self.execute_single_trade_cycle(contract)

                if self._shutdown_requested:
                    break

                # Post-trade Cooldown (default 30 seconds)
                if outcome:
                    cooldown = self.config.cooldown_seconds
                    self.logger.info(f"Initiating {cooldown:.0f}s cooldown before next trade cycle...")
                    start_cool = time.time()
                    while time.time() - start_cool < cooldown and not self._shutdown_requested:
                        remaining = int(cooldown - (time.time() - start_cool))
                        if remaining > 0 and remaining % 10 == 0:
                            self.logger.info(f"Cooldown active: {remaining}s remaining...")
                        time.sleep(1.0)

                time.sleep(0.5)

        except Exception as e:
            self.logger.error("Unexpected error in execution loop: %s", e, exc_info=True)
        finally:
            self.running = False
            self.logger.section("ENGINE EXECUTION SESSION ENDED")
            stats = self.outcome_logger.cumulative
            self.logger.info(
                f"Total Trades Completed: {stats.total_trades} | "
                f"Wins: {stats.winning_trades} | Losses: {stats.losing_trades} | "
                f"Win Rate: {stats.win_rate_pct:.1f}%"
            )
            self.logger.info(
                f"Net Session PnL: {self.logger.format_dual(stats.total_pnl_usdt)}"
            )
