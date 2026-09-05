"""
KCEX Automated Trade Execution Engine
=====================================
The core orchestrator that continuously runs the Masterplan strategy:
1. Connects to KCEX and validates pair specifications and fee status.
2. Generates signals via the active sub-strategy.
3. Sizes orders based on user configuration (multiplier, contracts, or minimum volume).
4. Submits market order with attached TP/SL in a single request.
5. Immediately reconciles fill:
   - If market price is already at or better than Min-Profit TP (entry + pu), closes immediately!
   - Otherwise, verifies/adjusts server-side TP to exact entry + pu and SL to requested risk limit.
6. Actively monitors the position until closed.
7. Logs detailed execution and outcome metrics in both USDT and INR.
8. Enforces configured cooldown before the next trade cycle.
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
from kcex.engine.strategy import (
    MasterplanStrategy,
    EMACrossoverStrategy,
    StochasticRSIStrategy
)
from strategies.filters import FilterPipeline


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

        # Strategy Selection
        if strategy is not None:
            self.strategy = strategy
        else:
            strat_mode = getattr(self.config, "strategy_mode", "STOCH_RSI") or "STOCH_RSI"
            strat_upper = str(strat_mode).upper()
            pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction
            if strat_upper in ("EMA", "EMA_CROSSOVER", "CROSSOVER"):
                sub_strat = EMACrossoverStrategy(
                    market=self.market,
                    symbol=self.config.symbol,
                    fast_period=getattr(self.config, "ema_fast", 5),
                    slow_period=getattr(self.config, "ema_slow", 13),
                    ema_preset=getattr(self.config, "ema_preset", "5/13"),
                    interval=getattr(self.config, "ema_interval", "Min1"),
                    preferred_direction=pref_dir,
                    cooldown_seconds=self.config.cooldown_seconds,
                    require_closed_candle=getattr(self.config, "ema_require_closed_candle", True)
                )
            else:
                sub_strat = StochasticRSIStrategy(
                    market=self.market,
                    symbol=self.config.symbol,
                    stoch_preset=getattr(self.config, "stoch_preset", "FAST_SCALP"),
                    rsi_period=getattr(self.config, "stoch_rsi_period", 9),
                    stoch_period=getattr(self.config, "stoch_period", 9),
                    k_period=getattr(self.config, "stoch_k_period", 3),
                    d_period=getattr(self.config, "stoch_d_period", 3),
                    oversold=getattr(self.config, "stoch_oversold", 20.0),
                    overbought=getattr(self.config, "stoch_overbought", 80.0),
                    interval=getattr(self.config, "stoch_interval", "Min1"),
                    zone_filter=getattr(self.config, "stoch_zone_filter", True),
                    preferred_direction=pref_dir,
                    cooldown_seconds=self.config.cooldown_seconds,
                    require_closed_candle=getattr(self.config, "stoch_require_closed_candle", True)
                )
            self.strategy = MasterplanStrategy(
                market=self.market,
                config=self.config,
                sub_strategy=sub_strat
            )

        self.filter_pipeline = FilterPipeline.from_config(self.config)

        self.running: bool = False
        self.trade_counter: int = 0
        self._current_position_id: Optional[int] = None
        self._shutdown_requested: bool = False
        self.simulated_balance_usdt: Optional[float] = None

    def stop(self) -> None:
        """Requests graceful engine stop."""
        self._shutdown_requested = True
        self.running = False
        try:
            self.strategy.stop()
        except Exception:
            pass
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
        vol_mode = (getattr(self.config, "volume_mode", "MULTIPLIER") or "MULTIPLIER").upper()
        if vol_mode == "CONTRACTS" and getattr(self.config, "volume_contracts", None):
            vol_summary = f"{self.config.volume_contracts} contract(s)"
        elif vol_mode == "MULTIPLIER" and getattr(self.config, "volume_multiplier", None):
            vol_summary = f"{self.config.volume_multiplier:g}x min quantity ({int(contract.min_volume)} min)"
        else:
            vol_summary = f"1x min quantity ({int(contract.min_volume)} min)"

        self.logger.info(f"Position Sizing: {vol_summary} [Trade Qty != Margin; Committed Margin = Trade Qty / {self.config.leverage}x leverage]")
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

        # Regime & Trend Filter Evaluation
        try:
            htf_tf = getattr(self.config, "htf_timeframe", "15m")
            tf_map = {
                "1m": "Min1", "3m": "Min3", "5m": "Min5", "15m": "Min15",
                "30m": "Min30", "1h": "Min60", "2h": "Hour2", "4h": "Hour4", "1d": "Day1"
            }
            kline_interval = tf_map.get(htf_tf, "Min15") if getattr(self.config, "htf_trend_filter_enabled", False) else "Min1"
            filter_candles = self.market.get_klines(contract.symbol, interval=kline_interval, limit=250)
        except Exception as e:
            self.logger.debug("Could not fetch candles for regime filter evaluation: %s", e)
            filter_candles = []

        allowed, reject_reason = self.filter_pipeline.evaluate(signal, filter_candles, time.time())
        if not allowed:
            self.logger.info(f"[REGIME FILTER] Signal {signal.direction.value} suppressed: {reject_reason}")
            if hasattr(self.strategy, "on_trade_rejected"):
                self.strategy.on_trade_rejected()
            elif hasattr(self.strategy.sub_strategy, "trade_in_progress"):
                self.strategy.sub_strategy.trade_in_progress = False
            return None

        self.trade_counter += 1
        trade_id = self.trade_counter
        symbol = contract.symbol
        direction = signal.direction
        is_long = (direction == OrderDirection.LONG)
        pu = contract.price_unit
        cs = contract.contract_size
        if self.config.leverage > contract.max_leverage:
            self.logger.warning(
                f"Notice: Configured leverage {self.config.leverage}x exceeds {symbol} max allowed ({contract.max_leverage}x). "
                f"Clamped to {contract.max_leverage}x."
            )
        leverage = min(self.config.leverage, contract.max_leverage)

        # Determine trade quantity (volume in contracts)
        # Note: Trade Quantity (Notional Value) is NOT the same as Margin!
        # Trade Quantity = Contracts * Contract Size * Price
        # Committed Margin = Trade Quantity / Leverage
        min_vol = int(contract.min_volume)
        vol_mode = (getattr(self.config, "volume_mode", "MULTIPLIER") or "MULTIPLIER").upper()
        if vol_mode == "CONTRACTS" and getattr(self.config, "volume_contracts", None):
            vol_contracts = max(min_vol, int(self.config.volume_contracts))
            vol_spec_desc = f"{vol_contracts} contract(s)"
        elif vol_mode == "MULTIPLIER" and getattr(self.config, "volume_multiplier", None):
            mult = float(self.config.volume_multiplier)
            vol_contracts = max(min_vol, int(round(min_vol * mult)))
            vol_spec_desc = f"{vol_contracts} contract(s) ({mult:g}x min)"
        else:
            vol_contracts = min_vol
            vol_spec_desc = f"{vol_contracts} contract(s) (1x min)"

        underlying_qty = vol_contracts * cs

        self.logger.section(f"EXECUTING TRADE #{trade_id} [{direction.value}] - {symbol}")

        # Determine effective TP ticks:
        # If dynamic_tp is enabled, use the signal's target_ticks (from confluence strength)
        # Otherwise, strictly enforce the user's configured tp_ticks (e.g. 1 pu)
        if getattr(self.config, "dynamic_tp", False) and "target_ticks" in signal.metadata:
            target_tp_ticks = int(signal.metadata["target_ticks"])
        else:
            target_tp_ticks = int(self.config.tp_ticks)

        if "agreeing_signals" in signal.metadata:
            agreeing = signal.metadata.get("agreeing_signals", [])
            obi_z = signal.metadata.get("obi_z", 0.0)
            delta_z = signal.metadata.get("delta_z", 0.0)
            vamp_z = signal.metadata.get("vamp_z", 0.0)
            rec = signal.metadata.get("delta_recency", 0.0)
            tp_desc = f"+{target_tp_ticks} pu ticks" if not getattr(self.config, "dynamic_tp", False) else f"+{target_tp_ticks} pu ticks (dynamic)"
            self.logger.info(
                f"[MICROSTRUCTURE TRIGGER] Confluence: {agreeing} | Target TP: {tp_desc} | "
                f"OBI z={obi_z:+.2f} | Delta z={delta_z:+.2f} (rec={rec:.2f}) | VAMP z={vamp_z:+.2f}"
            )

        # Get fresh market snapshot
        ticker = self.market.get_ticker(symbol)
        last_price = float(ticker.get("lastPrice", 0.0) or ticker.get("fairPrice", 1.0))
        ref_price = last_price
        inr_rate = self.market.get_inr_rate()
        self.logger.set_inr_rate(inr_rate)

        # Calculate estimated TP & SL prices
        ps = contract.price_precision
        base_coin = contract.base_coin or symbol.split('_')[0]

        est_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=ref_price,
            price_unit=pu,
            tp_ticks=target_tp_ticks,
            precision=ps
        )
        est_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=ref_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            sl_ticks=self.config.sl_ticks,
            sl_price_pct=self.config.sl_price_pct,
            price_unit=pu,
            precision=ps
        )

        notional_est_usdt = underlying_qty * ref_price
        notional_est_inr = notional_est_usdt * inr_rate
        margin_est_usdt = notional_est_usdt / leverage
        margin_est_inr = margin_est_usdt * inr_rate

        sl_desc = (
            f"-{self.config.sl_ticks} ticks" if self.config.sl_ticks
            else f"-{self.config.sl_price_pct}% price" if self.config.sl_price_pct
            else f"-{self.config.sl_roe_pct}% ROE"
        )

        self.logger.info(
            f"Pre-Trade Spec: Vol: {vol_spec_desc} ({underlying_qty:g} {base_coin}) | "
            f"Trade Qty (Notional): {self.logger.format_dual(notional_est_usdt)} | "
            f"Committed Margin (Qty/{leverage}x): {self.logger.format_dual(margin_est_usdt)}"
        )
        self.logger.info(
            f"Reference Price: {ref_price:.{ps}f} USDT | "
            f"Attached Min-Profit TP: {est_tp:.{ps}f} USDT (+{target_tp_ticks} pu) | "
            f"Attached SL: {est_sl:.{ps}f} USDT ({sl_desc})"
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
                sub_strategy_name=signal.sub_strategy_name,
                target_tp_ticks=target_tp_ticks
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

        self.logger.info("Submitting live MARKET order...")
        order_res = self.trader.create_order(
            symbol=symbol,
            side=side_str,
            vol_contracts=vol_contracts,
            order_type="MARKET",
            leverage=leverage,
            is_isolated=self.config.is_isolated
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
            sl_ticks=self.config.sl_ticks,
            sl_price_pct=self.config.sl_price_pct,
            price_unit=pu,
            precision=contract.price_precision
        )

        ps = contract.price_precision
        self.logger.info(
            f"Position Filled: Entry Price = {entry_price:.{ps}f} USDT | "
            f"Exact Min-Profit TP = {exact_tp:.{ps}f} USDT | Exact SL = {exact_sl:.{ps}f} USDT"
        )

        # Register server-side position TP/SL with exact prices
        if position_id:
            try:
                self.trader.set_position_tp_sl(
                    symbol=symbol,
                    position_id=position_id,
                    take_profit_price=exact_tp,
                    stop_loss_price=exact_sl
                )
                self.logger.info(f"Server-side position TP/SL registered: TP {exact_tp:.{ps}f}, SL {exact_sl:.{ps}f}")
            except Exception as e:
                self.logger.warning("Note: Server-side stoporder registration: %s", e)

        # Check immediate profit close condition using executable price (bid for LONG, ask for SHORT)
        ticker = self.market.get_ticker(symbol)
        last_p = float(ticker.get("lastPrice", entry_price))
        bid1 = float(ticker.get("bid1", 0.0))
        ask1 = float(ticker.get("ask1", 0.0))
        exec_price = (bid1 if bid1 > 0 else last_p) if direction == OrderDirection.LONG else (ask1 if ask1 > 0 else last_p)

        exit_price = last_p
        exit_reason = ExitReason.UNKNOWN
        close_order_id = None

        if self.strategy.is_better_than_min_profit(direction, exec_price, exact_tp, entry_price=entry_price):
            op_sym = ">=" if direction == OrderDirection.LONG else "<="
            self.logger.info(
                f"[IMMEDIATE PROFIT TRIGGER] Executable price ({exec_price:.{ps}f} USDT) is already {op_sym} "
                f"Min-Profit TP ({exact_tp:.{ps}f} USDT)! Closing immediately..."
            )
            close_res = self.trader.close_position(
                position_id=position_id or 0,
                symbol=symbol,
                side=side_str,
                vol_contracts=vol_contracts,
                leverage=leverage,
                is_isolated=self.config.is_isolated,
                is_market=True,
                price=exec_price
            )
            close_order_id = str(close_res.get("data", {}).get("orderId") or "")
            exit_price = exec_price
            exit_reason = ExitReason.IMMEDIATE_PROFIT_CLOSE
            time.sleep(0.5)
        else:
            # Active position monitoring loop
            self.logger.info("Entering active position monitoring loop...")
            exit_price, exit_reason, close_order_id = self._monitor_live_position(
                symbol=symbol,
                position_id=position_id,
                direction=direction,
                vol_contracts=vol_contracts,
                leverage=leverage,
                exact_tp=exact_tp,
                exact_sl=exact_sl,
                precision=ps,
                entry_price=entry_price,
                open_time=open_time
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
                initial_reason=exit_reason if exit_reason != ExitReason.UNKNOWN else None,
                open_time=open_time
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

        fee_open_usdt = notional_usdt * contract.taker_fee_rate
        fee_close_usdt = (underlying_qty * exit_price) * contract.taker_fee_rate
        fee_total_usdt = fee_open_usdt + fee_close_usdt
        fee_total_inr = fee_total_usdt * inr_rate

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
            base_coin=contract.base_coin or symbol.split('_')[0],
            entry_price=entry_price,
            exit_price=exit_price,
            min_profit_tp_price=exact_tp,
            stop_loss_price=exact_sl,
            price_unit=pu,
            price_precision=contract.price_precision,
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
            fee_open_usdt=fee_open_usdt,
            fee_close_usdt=fee_close_usdt,
            fee_total_usdt=fee_total_usdt,
            fee_total_inr=fee_total_inr,
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
        initial_reason: Optional[ExitReason] = None,
        open_time: Optional[float] = None
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
        min_ts = int((open_time - 5.0) * 1000) if open_time else 0

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
                    order_time = int(o.get("createTime", 0) or o.get("updateTime", 0))
                    if min_ts > 0 and order_time > 0 and order_time < min_ts:
                        continue
                    close_order_id = str(o.get("orderId"))
                    deal_price = float(o.get("dealAvgPrice") or o.get("price") or 0.0)
                    if deal_price > 0:
                        exit_price = deal_price
                    realized_pnl = float(o.get("profit", 0.0))
                    if o.get("positionId"):
                        reconciled_pos_id = int(o.get("positionId"))

                    external_oid = str(o.get("externalOid") or "")
                    if realized_pnl > 0:
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                    elif realized_pnl < 0:
                        exit_reason = ExitReason.STOP_LOSS_HIT
                    elif "TAKE_PROFIT" in external_oid:
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                    elif "STOP_LOSS" in external_oid:
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
        exact_sl: float,
        precision: int = 4,
        entry_price: Optional[float] = None,
        open_time: Optional[float] = None
    ) -> tuple[float, ExitReason, Optional[str]]:
        """
        Polls ticker and open positions until the position closes.
        Prioritizes server-side TP/SL stoporder execution, using executable bid/ask
        for immediate local profit close safeguards.
        """
        side_str = "LONG" if direction == OrderDirection.LONG else "SHORT"
        close_order_id = None
        last_seen_price = exact_tp
        exec_price = exact_tp
        deep_alert_logged = False
        monitor_start_time = open_time if open_time is not None else time.time()

        while not self._shutdown_requested:
            time.sleep(self.config.poll_interval_seconds)

            # 1. Fetch latest price & executable bid/ask prices
            try:
                ticker = self.market.get_ticker(symbol)
                current_price = float(ticker.get("lastPrice") or ticker.get("fairPrice", 0.0))
                bid1 = float(ticker.get("bid1", 0.0))
                ask1 = float(ticker.get("ask1", 0.0))
                last_seen_price = current_price
            except Exception as e:
                self.logger.debug("Ticker poll error: %s", e)
                continue

            # 2. Check if position closed via server-side attached TP or SL first
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

            # 3. Check if executable price reached Min-Profit TP (bid for LONG, ask for SHORT)
            exec_price = (bid1 if bid1 > 0 else current_price) if direction == OrderDirection.LONG else (ask1 if ask1 > 0 else current_price)
            if self.strategy.is_better_than_min_profit(direction, exec_price, exact_tp, entry_price=entry_price):
                op_sym = ">=" if direction == OrderDirection.LONG else "<="
                self.logger.info(
                    f"[IMMEDIATE PROFIT TRIGGER] Executable price ({exec_price:.{precision}f} USDT) reached Min-Profit TP: {op_sym} {exact_tp:.{precision}f} USDT. "
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
                        price=exec_price
                    )
                    close_order_id = str(res.get("data", {}).get("orderId") or "")
                    return exec_price, ExitReason.IMMEDIATE_PROFIT_CLOSE, close_order_id
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

            # 4. Duration-Based Monitoring & Time-Decay Exit Actions
            if getattr(self.config, "duration_filter_enabled", False):
                elapsed = time.time() - monitor_start_time
                deep_thresh = float(getattr(self.config, "duration_deep_monitor_seconds", 60.0))
                if elapsed >= deep_thresh and not deep_alert_logged:
                    deep_alert_logged = True
                    self.logger.info(
                        f"[LIVE DURATION IN-DEPTH MONITOR] Position open for {elapsed:.1f}s (threshold {deep_thresh:.0f}s). "
                        f"Close monitoring engaged..."
                    )

                max_hold = float(getattr(self.config, "duration_max_hold_seconds", 90.0))
                if elapsed >= max_hold:
                    action = (getattr(self.config, "duration_action", "CLOSE") or "CLOSE").upper()
                    if action in ("CLOSE", "SCRATCH_OR_MARKET"):
                        exit_reason = ExitReason.TIMEOUT_CLOSE if action == "CLOSE" else ExitReason.DURATION_SCRATCH
                        self.logger.warning(
                            f"[LIVE TIME-STOP TRIGGERED] Position open {elapsed:.1f}s >= max {max_hold:.0f}s. "
                            f"Action: {action}. Executing market close at {exec_price:.{precision}f} USDT..."
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
                                price=exec_price
                            )
                            close_order_id = str(res.get("data", {}).get("orderId") or "")
                            return exec_price, exit_reason, close_order_id
                        except Exception as e:
                            self.logger.warning("Error executing live time-stop close: %s", e)

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
        sub_strategy_name: str,
        target_tp_ticks: Optional[int] = None
    ) -> TradeOutcome:
        """
        High-fidelity DRY-RUN execution simulation using live market ticker data.
        """
        symbol = contract.symbol
        pu = contract.price_unit
        cs = contract.contract_size
        underlying_qty = vol_contracts * cs

        # 1. Realistic Entry Price from Orderbook Taker Fill:
        # Long market orders execute against best ask (ask1).
        # Short market orders execute against best bid (bid1).
        ticker = self.market.get_ticker(symbol)
        last_price = float(ticker.get("lastPrice", 0.0) or ticker.get("fairPrice", 1.0))
        ask1 = float(ticker.get("ask1", 0.0) or last_price)
        bid1 = float(ticker.get("bid1", 0.0) or last_price)

        if direction == OrderDirection.LONG:
            entry_price = ask1 if ask1 > 0 else last_price
        else:
            entry_price = bid1 if bid1 > 0 else last_price

        entry_price = round(entry_price, contract.price_precision)

        effective_tp_ticks = target_tp_ticks if target_tp_ticks is not None else self.config.tp_ticks
        exact_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=effective_tp_ticks,
            precision=contract.price_precision
        )
        exact_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            sl_ticks=self.config.sl_ticks,
            sl_price_pct=self.config.sl_price_pct,
            price_unit=pu,
            precision=contract.price_precision
        )

        sl_desc = (
            f"-{self.config.sl_ticks} ticks" if self.config.sl_ticks
            else f"-{self.config.sl_price_pct}% price" if self.config.sl_price_pct
            else f"-{self.config.sl_roe_pct}% ROE"
        )

        ps = contract.price_precision
        base_coin = contract.base_coin or symbol.split('_')[0]

        self.logger.info(
            f"[DRY-RUN] Simulated Order Filled: Entry = {entry_price:.{ps}f} USDT | "
            f"Min-Profit TP = {exact_tp:.{ps}f} USDT (+{effective_tp_ticks} pu) | SL = {exact_sl:.{ps}f} USDT ({sl_desc})"
        )


        # 2. Check immediate profit condition at fill
        if self.strategy.is_better_than_min_profit(direction, entry_price, exact_tp):
            op_sym = ">=" if direction == OrderDirection.LONG else "<="
            self.logger.info(
                f"[DRY-RUN] Immediate profit condition met at fill: {entry_price:.{ps}f} {op_sym} TP {exact_tp:.{ps}f}"
            )
            exit_price = exact_tp
            exit_reason = ExitReason.IMMEDIATE_PROFIT_CLOSE
        else:
            # 3. Active Real-Time Market Monitoring Loop
            self.logger.info(
                f"[DRY-RUN] Actively monitoring live market prices for TP ({exact_tp:.{ps}f}) or SL ({exact_sl:.{ps}f})..."
            )
            exit_price = entry_price
            exit_reason = ExitReason.UNKNOWN
            poll_count = 0
            deep_alert_logged = False

            while not self._shutdown_requested:
                time.sleep(self.config.poll_interval_seconds)
                poll_count += 1

                try:
                    cur_ticker = self.market.get_ticker(symbol)
                    cur_last = float(cur_ticker.get("lastPrice", 0.0) or cur_ticker.get("fairPrice", 0.0))
                    cur_bid = float(cur_ticker.get("bid1", 0.0) or cur_last)
                    cur_ask = float(cur_ticker.get("ask1", 0.0) or cur_last)
                except Exception as e:
                    self.logger.debug("Dry-run ticker fetch error: %s", e)
                    continue

                # For LONG: Close fills by selling at best bid (bid1) or last trade
                if direction == OrderDirection.LONG:
                    effective_close_price = cur_bid
                    # TP check
                    if effective_close_price >= exact_tp or cur_last >= exact_tp:
                        exit_price = exact_tp
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                        self.logger.info(
                            f"[DRY-RUN TARGET HIT] Market reached TP! Exit: {exit_price:.{ps}f} USDT (Market Bid: {cur_bid:.{ps}f}, Last: {cur_last:.{ps}f})"
                        )
                        break
                    # SL check
                    elif effective_close_price <= exact_sl or cur_last <= exact_sl:
                        exit_price = exact_sl
                        exit_reason = ExitReason.STOP_LOSS_HIT
                        self.logger.info(
                            f"[DRY-RUN STOP LOSS HIT] Market reached SL! Exit: {exit_price:.{ps}f} USDT (Market Bid: {cur_bid:.{ps}f}, Last: {cur_last:.{ps}f})"
                        )
                        break

                # For SHORT: Close fills by buying back at best ask (ask1) or last trade
                else:
                    effective_close_price = cur_ask
                    # TP check
                    if effective_close_price <= exact_tp or cur_last <= exact_tp:
                        exit_price = exact_tp
                        exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                        self.logger.info(
                            f"[DRY-RUN TARGET HIT] Market reached TP! Exit: {exit_price:.{ps}f} USDT (Market Ask: {cur_ask:.{ps}f}, Last: {cur_last:.{ps}f})"
                        )
                        break
                    # SL check
                    elif effective_close_price >= exact_sl or cur_last >= exact_sl:
                        exit_price = exact_sl
                        exit_reason = ExitReason.STOP_LOSS_HIT
                        self.logger.info(
                            f"[DRY-RUN STOP LOSS HIT] Market reached SL! Exit: {exit_price:.{ps}f} USDT (Market Ask: {cur_ask:.{ps}f}, Last: {cur_last:.{ps}f})"
                        )
                        break

                # Duration Monitoring & Time-Decay Safeguards
                if getattr(self.config, "duration_filter_enabled", False):
                    elapsed = time.time() - open_time
                    deep_thresh = float(getattr(self.config, "duration_deep_monitor_seconds", 60.0))
                    if elapsed >= deep_thresh and not deep_alert_logged:
                        deep_alert_logged = True
                        self.logger.info(
                            f"[DRY-RUN DURATION IN-DEPTH MONITOR] Trade has been open for {elapsed:.1f}s "
                            f"(threshold: {deep_thresh:.0f}s). Heightened monitoring active."
                        )

                    max_hold = float(getattr(self.config, "duration_max_hold_seconds", 90.0))
                    if elapsed >= max_hold:
                        action = (getattr(self.config, "duration_action", "CLOSE") or "CLOSE").upper()
                        if action == "CLOSE":
                            exit_price = effective_close_price
                            exit_reason = ExitReason.TIMEOUT_CLOSE
                            self.logger.warning(
                                f"[DRY-RUN TIME-STOP] Trade open {elapsed:.1f}s >= max {max_hold:.0f}s. "
                                f"Forced Market Exit at {exit_price:.{ps}f} USDT."
                            )
                            break
                        elif action == "SCRATCH_OR_MARKET":
                            u_diff = (effective_close_price - entry_price) if direction == OrderDirection.LONG else (entry_price - effective_close_price)
                            if u_diff >= -1.0 * pu:
                                exit_price = effective_close_price
                                exit_reason = ExitReason.DURATION_SCRATCH
                                self.logger.warning(
                                    f"[DRY-RUN DURATION SCRATCH] Trade open {elapsed:.1f}s >= max {max_hold:.0f}s. "
                                    f"Price near breakeven ({u_diff / pu:+.1f} pu). Scratching at {exit_price:.{ps}f} USDT."
                                )
                                break
                            else:
                                if direction == OrderDirection.LONG:
                                    exact_sl = max(exact_sl, entry_price)
                                else:
                                    exact_sl = min(exact_sl, entry_price)
                                self.logger.info(
                                    f"[DRY-RUN DURATION TIGHTEN] Trade open {elapsed:.1f}s. SL tightened to entry {exact_sl:.{ps}f} USDT."
                                )
                        elif action == "TIGHTEN_SL":
                            if direction == OrderDirection.LONG:
                                exact_sl = max(exact_sl, entry_price)
                            else:
                                exact_sl = min(exact_sl, entry_price)
                            self.logger.info(
                                f"[DRY-RUN DURATION TIGHTEN] Trade open {elapsed:.1f}s. SL tightened to entry {exact_sl:.{ps}f} USDT."
                            )

                # Periodic status report every ~4 seconds
                poll_interval = max(0.1, self.config.poll_interval_seconds)
                status_freq = int(max(1, 4.0 / poll_interval))
                if poll_count % status_freq == 0:
                    u_diff = (effective_close_price - entry_price) if direction == OrderDirection.LONG else (entry_price - effective_close_price)
                    u_pnl = underlying_qty * u_diff
                    self.logger.info(
                        f"[DRY-RUN MONITOR] Price: {effective_close_price:.{ps}f} USDT | TP: {exact_tp:.{ps}f} | SL: {exact_sl:.{ps}f} | "
                        f"Unrealized PnL: {'+' if u_pnl >= 0 else ''}{u_pnl:.6f} USDT"
                    )

            if self._shutdown_requested and exit_reason == ExitReason.UNKNOWN:
                exit_price = last_price
                exit_reason = ExitReason.MANUAL_CLOSE
                self.logger.warning("[DRY-RUN] Manual close requested during trade.")

        close_time = time.time()
        duration = max(0.1, close_time - open_time)

        price_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)

        inr_rate = self.market.get_inr_rate()
        notional_usdt = underlying_qty * entry_price
        notional_inr = notional_usdt * inr_rate
        margin_usdt = notional_usdt / leverage
        margin_inr = margin_usdt * inr_rate

        fee_open_usdt = notional_usdt * contract.taker_fee_rate
        fee_close_usdt = (underlying_qty * exit_price) * contract.taker_fee_rate
        fee_total_usdt = fee_open_usdt + fee_close_usdt
        fee_total_inr = fee_total_usdt * inr_rate

        realized_pnl_usdt = (underlying_qty * price_diff) - fee_total_usdt
        realized_pnl_inr = realized_pnl_usdt * inr_rate
        roe_pct = (realized_pnl_usdt / margin_usdt) * 100.0 if margin_usdt > 0 else 0.0
        pnl_pct = (price_diff / entry_price) * 100.0 if entry_price > 0 else 0.0

        # Virtual Simulated Balance Tracking:
        # Tracks realistic balance progression across simulation cycles
        if self.simulated_balance_usdt is None:
            if self.client.config.is_authenticated:
                try:
                    balances = self.trader.get_usdt_balance()
                    self.simulated_balance_usdt = float(balances.get("available_usdt", 10.0))
                except Exception:
                    self.simulated_balance_usdt = 10.0
            else:
                self.simulated_balance_usdt = 10.0

        self.simulated_balance_usdt += realized_pnl_usdt
        balance_after_usdt = self.simulated_balance_usdt
        balance_after_inr = balance_after_usdt * inr_rate
        self.logger.info(
            f"[SIMULATED WALLET] Balance: {balance_after_usdt:.4f} USDT (INR {balance_after_inr:.2f})"
        )

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
            base_coin=base_coin,
            entry_price=entry_price,
            exit_price=exit_price,
            min_profit_tp_price=exact_tp,
            stop_loss_price=exact_sl,
            price_unit=pu,
            price_precision=ps,
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
            fee_open_usdt=fee_open_usdt,
            fee_close_usdt=fee_close_usdt,
            fee_total_usdt=fee_total_usdt,
            fee_total_inr=fee_total_inr,
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

        self.strategy.start()
        self.logger.info("Starting Masterplan Automated Execution Loop...")
        self.logger.info(f"Target Trades: {self.config.max_trades if self.config.max_trades > 0 else 'Unlimited'}")

        last_diag_log = 0.0
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

                # Post-trade Cooldown
                if outcome:
                    cooldown = self.config.cooldown_seconds
                    self.logger.info(f"Initiating {cooldown:.0f}s cooldown before next trade cycle...")
                    start_cool = time.time()
                    while time.time() - start_cool < cooldown and not self._shutdown_requested:
                        remaining = int(cooldown - (time.time() - start_cool))
                        if remaining > 0 and remaining % 10 == 0:
                            self.logger.info(f"Cooldown active: {remaining}s remaining...")
                        time.sleep(1.0)
                else:
                    # Log periodic diagnostics while hunting for entry signal
                    now = time.time()
                    if now - last_diag_log >= 4.0:
                        last_diag_log = now
                        diag = self.strategy.get_diagnostics()
                        if diag and "fast_ema" in diag:
                            c_f = diag.get('fast_ema', 0.0)
                            c_s = diag.get('slow_ema', 0.0)
                            diff = diag.get('diff', 0.0)
                            diff_pct = diag.get('diff_pct', 0.0)
                            prec = contract.price_precision
                            self.logger.info(
                                f"[HUNTING ENTRY] EMA({diag.get('preset', '5/13')}) {diag.get('interval', 'Min1')} | "
                                f"Fast: {c_f:.{prec}f} | Slow: {c_s:.{prec}f} | "
                                f"Diff: {diff:+.{prec}f} ({diff_pct:+.2f}%) | "
                                f"Trend: {diag.get('trend', 'NEUTRAL')} | Bar Close In: {diag.get('time_to_bar_close_s', 0):.0f}s"
                            )
                        elif diag and (diag.get("strategy") == "STOCHASTIC_RSI" or ("k" in diag and "d" in diag)):
                            k_val = diag.get('k', 50.0)
                            d_val = diag.get('d', 50.0)
                            diff_kd = diag.get('diff', 0.0)
                            zone = diag.get('zone', 'NEUTRAL')
                            preset = diag.get('preset', 'FAST_SCALP')
                            inv = diag.get('interval', 'Min1')
                            self.logger.info(
                                f"[HUNTING ENTRY] StochRSI({preset}) {inv} | "
                                f"%K: {k_val:.1f} | %D: {d_val:.1f} | Diff: {diff_kd:+.1f} | "
                                f"Zone: {zone} | Trend: {diag.get('trend', 'NEUTRAL')} | Bar Close In: {diag.get('time_to_bar_close_s', 0):.0f}s"
                            )
                        elif diag and "obi_z" in diag:
                            feed_info = diag.get("feed", {})
                            ws_status = "LIVE WS" if feed_info.get("connected") else "CONNECTING"
                            b_bid = f"{diag.get('best_bid'):.{contract.price_precision}f}" if diag.get('best_bid') else "N/A"
                            b_ask = f"{diag.get('best_ask'):.{contract.price_precision}f}" if diag.get('best_ask') else "N/A"
                            self.logger.info(
                                f"[HUNTING ENTRY] {ws_status} | Bid/Ask: {b_bid} / {b_ask} (Spread: {diag.get('spread_ticks', 0):.1f} pu) | "
                                f"OBI z={diag.get('obi_z', 0):+.2f} | Delta z={diag.get('delta_z', 0):+.2f} | VAMP z={diag.get('vamp_z', 0):+.2f}"
                            )

                time.sleep(0.3)

        except Exception as e:
            self.logger.error("Unexpected error in execution loop: %s", e, exc_info=True)
        finally:
            self.running = False
            try:
                self.strategy.stop()
            except Exception:
                pass
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
