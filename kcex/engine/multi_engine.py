"""
KCEX Multi-Asset Concurrent Trading Engine
==========================================
Coordinates simultaneous autonomous trading across multiple assets on distinct timeframes:
- TRUMP_USDT (15m)
- ETH_USDT (4h)
- BTC_USDT (15m)
- DOGE_USDT (15m)

Features:
- Dedicated worker thread per asset for non-blocking concurrent scanning & execution
- Smart Money Concepts (Vivek Yadav): 1:1 partial TP (50%) + Breakeven stop lock + 1:2 runner
- Strict manual trade conflict prevention (direction-aware position checks, position ID tracking)
- Position concurrency rule: Never open a duplicate position in the same direction, allow opposite direction
- Throttled periodic status logging: Every 10 min if idle, every 5 min if in position (zero log spam on Railway)
- Real-time immediate logging for signals, orders, fills, TP/SL adjustments, and trade closes
- Thread-safe wallet margin sizing (10% available balance per trade @ 15x leverage)
"""

import os
import sys
import time
import math
import signal
import logging
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Set

from kcex.config import KCEXConfig
from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.risk import KCEXRiskCalculator
from kcex.trade import KCEXTrader
from kcex.engine.models import (
    OrderDirection,
    EngineMode,
    TradeOutcome,
    ExitReason,
    TradeSignal,
    ExecutionConfig
)
from kcex.engine.logger import DualCurrencyLogger, TradeOutcomeLogger
from kcex.engine.mongo_logger import MongoTradeLogger
from strategies.order_block_demand import OrderBlockDemandStrategy, ZoneStatus

logger = logging.getLogger("MultiAssetEngine")


class AssetWorker:
    """
    Dedicated worker thread managing market scanning, signal generation,
    order execution, and position lifecycle for a single asset.
    """

    def __init__(
        self,
        symbol: str,
        timeframe: str,
        pivot_len: int,
        leverage: int,
        margin_pct: float,
        risk_reward_ratio: float,
        mode: EngineMode,
        shared_logger: DualCurrencyLogger,
        shared_outcome_logger: TradeOutcomeLogger,
        shared_mongo_logger: Optional[MongoTradeLogger],
        order_lock: threading.Lock,
        cooldown_seconds: float = 30.0,
        buffer_ticks: int = 1,
        breakeven_buffer_ticks: int = 1
    ):
        self.symbol = symbol.upper()
        self.timeframe = timeframe
        self.pivot_len = pivot_len
        self.leverage = leverage
        self.margin_pct = margin_pct
        self.risk_reward_ratio = risk_reward_ratio
        self.mode = mode
        self.logger = shared_logger
        self.outcome_logger = shared_outcome_logger
        self.mongo_logger = shared_mongo_logger
        self.order_lock = order_lock
        self.cooldown_seconds = cooldown_seconds
        self.buffer_ticks = buffer_ticks
        self.breakeven_buffer_ticks = breakeven_buffer_ticks

        # Thread-safe private API clients
        self.client = KCEXClient()
        self.market = KCEXMarket(self.client)
        self.risk = KCEXRiskCalculator(self.market, self.client)
        self.trader = KCEXTrader(self.client, self.market, self.risk)

        # Strategy instance
        self.strategy = OrderBlockDemandStrategy(
            market=self.market,
            symbol=self.symbol,
            interval=self.timeframe,
            pivot_len=self.pivot_len,
            risk_reward_ratio=self.risk_reward_ratio,
            buffer_ticks=self.buffer_ticks,
            cooldown_seconds=self.cooldown_seconds,
            require_closed_candle=True
        )

        # Runtime worker state
        self.contract: Optional[ContractInfo] = None
        self.thread: Optional[threading.Thread] = None
        self.running: bool = False
        self.in_position: bool = False
        self.current_position_id: Optional[int] = None
        self.last_price: float = 0.0
        self.last_status_msg: str = "Initializing..."
        self.active_position_desc: str = ""
        self.trade_counter: int = 0
        self.last_cooldown_end: float = 0.0

    def start(self) -> None:
        """Starts worker background thread."""
        self.contract = self.market.get_contract_detail(self.symbol)
        self.strategy.start()
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True, name=f"Worker-{self.symbol}")
        self.thread.start()

    def stop(self) -> None:
        """Stops worker gracefully."""
        self.running = False
        try:
            self.strategy.stop()
        except Exception:
            pass

    def _run_loop(self) -> None:
        """Worker lifecycle loop: Scan -> Check Signal -> Execute -> Monitor -> Cooldown."""
        self.logger.info(f"[{self.symbol}] Worker thread started. Timeframe: {self.timeframe} | Leverage: {self.leverage}x | Target R:R: 1:{self.risk_reward_ratio:g}")

        while self.running:
            try:
                # 1. Update latest ticker price & diagnostics
                try:
                    ticker = self.market.get_ticker(self.symbol)
                    p = float(ticker.get("lastPrice") or ticker.get("fairPrice", 0.0))
                    if p > 0:
                        self.last_price = p
                except Exception:
                    pass

                # Cooldown check
                now = time.time()
                if now < self.last_cooldown_end:
                    rem = int(self.last_cooldown_end - now)
                    self.last_status_msg = f"Cooldown ({rem}s remaining)"
                    time.sleep(1.0)
                    continue

                # 2. Check for trade signal
                signal = None
                try:
                    signal = self.strategy.get_signal()
                except Exception as e:
                    self.logger.debug(f"[{self.symbol}] Signal fetch error: {e}")

                if signal is None:
                    # Update status diagnostics
                    diag = self.strategy.get_diagnostics() if hasattr(self.strategy, "get_diagnostics") else {}
                    rej = diag.get("last_rejection_reason", "Hunting setups")
                    zones = diag.get("zones", [])
                    active_ob_str = "None"
                    if zones:
                        z = zones[0]
                        active_ob_str = f"{z.get('type')} [{z.get('low')}-{z.get('high')}]"
                    self.last_status_msg = f"Zones: {len(zones)} | Active OB: {active_ob_str} | Status: {rej}"
                    time.sleep(2.0)
                    continue

                # 3. Valid Signal Received! Check position concurrency before executing
                direction = signal.direction
                self.logger.info(
                    f"⚡ [{self.symbol}] Valid {direction.value} Signal Detected! "
                    f"Zone: {signal.metadata.get('zone_type')} [{signal.metadata.get('zone_low')}-{signal.metadata.get('zone_high')}] | "
                    f"1:2 R:R Target: {signal.metadata.get('take_profit_price')} | SL: {signal.metadata.get('stop_loss_price')}"
                )

                # Acquire order lock to prevent multi-pair balance race conditions
                with self.order_lock:
                    can_execute = self._check_concurrency_and_balance(direction)
                    if not can_execute:
                        if hasattr(self.strategy, "on_trade_rejected"):
                            self.strategy.on_trade_rejected()
                        continue

                    # Execute entry order
                    outcome = self._execute_trade(signal)

                # If trade entered, monitor until close
                if outcome is not None:
                    self.last_cooldown_end = time.time() + self.cooldown_seconds

            except KCEXAPIError as ke:
                self.logger.warning(f"[{self.symbol}] KCEX API error in loop: {ke}")
                time.sleep(5.0)
            except Exception as e:
                self.logger.warning(f"[{self.symbol}] Unexpected worker loop error: {e}")
                time.sleep(3.0)

    def _check_concurrency_and_balance(self, direction: OrderDirection) -> bool:
        """
        Enforces concurrency rules & manual trade isolation:
        - Never open duplicate position in same direction
        - Allow opposite direction (Hedge Mode)
        - Never interfere with existing manual positions
        """
        if self.mode != EngineMode.LIVE:
            return True

        try:
            open_positions = self.trader.get_open_positions(self.symbol)
            for p in open_positions:
                h_vol = float(p.get("holdVol", 0) or p.get("vol", 0))
                if h_vol > 0:
                    p_type = p.get("positionType")
                    p_side = p.get("side")
                    is_pos_long = (p_type == 1 or str(p_side).upper() in ("1", "LONG", "BUY"))
                    if (direction == OrderDirection.LONG and is_pos_long):
                        self.logger.info(
                            f"[{self.symbol}] Active LONG position already exists (Hold: {h_vol:g} contracts). "
                            f"Skipping duplicate LONG signal."
                        )
                        return False
                    elif (direction == OrderDirection.SHORT and not is_pos_long):
                        self.logger.info(
                            f"[{self.symbol}] Active SHORT position already exists (Hold: {h_vol:g} contracts). "
                            f"Skipping duplicate SHORT signal."
                        )
                        return False
            return True
        except Exception as e:
            self.logger.warning(f"[{self.symbol}] Concurrency verification error: {e}")
            return False

    def _execute_trade(self, signal: TradeSignal) -> Optional[TradeOutcome]:
        """Sizes position to 10% available margin @ 15x leverage and enters trade."""
        direction = signal.direction
        is_long = (direction == OrderDirection.LONG)
        side_str = "LONG" if is_long else "SHORT"
        prec = self.contract.price_precision
        pu = self.contract.price_unit
        cs = self.contract.contract_size
        min_vol = int(self.contract.min_volume)

        # 1. Fetch available USDT margin
        avail_usdt = 100.0  # default for dry-run
        if self.mode == EngineMode.LIVE:
            try:
                balances = self.trader.get_usdt_balance()
                avail_usdt = balances.get("available_usdt", 0.0)
            except Exception as e:
                self.logger.warning(f"[{self.symbol}] Could not fetch balance: {e}")
                return None

        # 2. Position sizing: 10% available margin @ 15x leverage
        ticker = self.market.get_ticker(self.symbol)
        curr_price = float(ticker.get("lastPrice", 0.0) or ticker.get("fairPrice", 1.0))

        if curr_price <= 0:
            return None

        one_contract_margin = (min_vol * cs * curr_price) / self.leverage
        if avail_usdt < one_contract_margin and self.mode == EngineMode.LIVE:
            self.logger.warning(
                f"[{self.symbol}] Insufficient margin: Available: {avail_usdt} USDT, "
                f"minimum required for 1 contract ({min_vol * cs} {self.contract.base_coin}) is {one_contract_margin} USDT. Aborting trade."
            )
            return None

        margin_to_use = avail_usdt * (self.margin_pct / 100.0)
        notional_usdt = margin_to_use * self.leverage
        raw_contracts = notional_usdt / (curr_price * cs)
        vol_contracts = max(min_vol, int(raw_contracts))
        committed_margin = (vol_contracts * cs * curr_price) / self.leverage

        self.logger.info(
            f"🚀 [{self.symbol}] SIZING: Available: {avail_usdt} USDT -> 10% Margin: {margin_to_use} USDT | "
            f"{self.leverage}x Lev Notional: {notional_usdt} USDT -> Vol: {vol_contracts} contracts (Committed: {committed_margin} USDT)"
        )

        initial_sl = float(signal.metadata.get("stop_loss_price"))
        exact_tp = float(signal.metadata.get("take_profit_price"))
        target_1to1 = float(signal.metadata.get("target_1to1_price", curr_price))

        position_id = None
        entry_price = curr_price
        open_time = time.time()

        if self.mode == EngineMode.LIVE:
            try:
                # Market Entry Order
                order_res = self.trader.create_order(
                    symbol=self.symbol,
                    side="BUY" if is_long else "SELL",
                    vol_contracts=vol_contracts,
                    order_type="MARKET",
                    leverage=self.leverage,
                    stop_loss_price=initial_sl,
                    is_isolated=True
                )
                order_id = str((order_res.get("data") or {}).get("orderId", ""))
                self.logger.info(f"[{self.symbol}] Live entry order submitted (Order ID: {order_id})")

                # Wait 500ms and reconcile position
                time.sleep(0.5)
                open_pos = self.trader.get_open_positions(self.symbol)
                for p in open_pos:
                    h_vol = float(p.get("holdVol", 0) or p.get("vol", 0))
                    if h_vol > 0:
                        p_type = p.get("positionType")
                        p_side = p.get("side")
                        is_pos_long = (p_type == 1 or str(p_side).upper() in ("1", "LONG", "BUY"))
                        if (direction == OrderDirection.LONG and is_pos_long) or (direction == OrderDirection.SHORT and not is_pos_long):
                            position_id = int(p.get("positionId"))
                            entry_price = float(p.get("openAvgPrice") or p.get("holdAvgPrice") or curr_price)
                            break

                self.current_position_id = position_id
                self.in_position = True
                self.logger.info(f"[{self.symbol}] Position Confirmed! Entry: {entry_price:.{prec}f} USDT | Position ID: {position_id}")

            except Exception as e:
                self.logger.error(f"[{self.symbol}] Live order execution failed: {e}")
                return None
        else:
            # Dry-run execution
            self.in_position = True
            entry_price = curr_price

        # 3. Monitor Position until Exit
        exit_price, exit_reason = self._monitor_position(
            position_id=position_id,
            direction=direction,
            vol_contracts=vol_contracts,
            entry_price=entry_price,
            initial_sl=initial_sl,
            exact_tp=exact_tp,
            target_1to1=target_1to1,
            precision=prec,
            open_time=open_time
        )

        self.in_position = False
        self.current_position_id = None
        self.active_position_desc = ""

        # 4. Financial Reconciliation
        duration = max(0.1, time.time() - open_time)
        price_diff = (exit_price - entry_price) if is_long else (entry_price - exit_price)
        underlying_qty = vol_contracts * cs
        fee_rate = 0.0001  # KCEX 0.01% taker fee
        fee_total = (underlying_qty * entry_price * fee_rate) + (underlying_qty * exit_price * fee_rate)
        realized_pnl_usdt = (underlying_qty * price_diff) - fee_total
        margin_usdt = (underlying_qty * entry_price) / self.leverage
        roe_pct = (realized_pnl_usdt / margin_usdt * 100.0) if margin_usdt > 0 else 0.0

        outcome = TradeOutcome(
            trade_id=self.trade_counter,
            symbol=self.symbol,
            direction=direction,
            sub_strategy_name=f"OrderBlockDemand({self.timeframe})",
            mode=self.mode,
            leverage=self.leverage,
            vol_contracts=vol_contracts,
            contract_size=cs,
            underlying_quantity=underlying_qty,
            base_coin=self.contract.base_coin,
            entry_price=entry_price,
            exit_price=exit_price,
            notional_value_usdt=underlying_qty * entry_price,
            margin_used_usdt=margin_usdt,
            fee_total_usdt=fee_total,
            fee_open_usdt=fee_total / 2.0,
            fee_close_usdt=fee_total / 2.0,
            realized_pnl_usdt=realized_pnl_usdt,
            roe_percentage=roe_pct,
            pnl_percentage=(price_diff / entry_price * 100.0),
            open_timestamp=open_time,
            close_timestamp=time.time(),
            duration_seconds=duration,
            exit_reason=exit_reason,
            min_profit_tp_price=exact_tp,
            stop_loss_price=initial_sl,
            inr_rate=self.market.get_inr_rate()
        )

        self.trade_counter += 1
        self.outcome_logger.log_outcome(outcome)
        if self.mongo_logger and self.mode == EngineMode.LIVE:
            try:
                self.mongo_logger.log_trade(outcome, ExecutionConfig(symbol=self.symbol, leverage=self.leverage))
            except Exception:
                pass

        pnl_sign = "+" if realized_pnl_usdt >= 0 else ""
        self.logger.info(
            f"🏁 [{self.symbol}] TRADE COMPLETED: {direction.value} | Reason: {exit_reason.value} | "
            f"Entry: {entry_price:.{prec}f} -> Exit: {exit_price:.{prec}f} | Net PnL: {pnl_sign}{realized_pnl_usdt:.4f} USDT ({pnl_sign}{roe_pct:.2f}% ROE) | Hold: {duration/60:.1f}m"
        )
        return outcome

    def _monitor_position(
        self,
        position_id: Optional[int],
        direction: OrderDirection,
        vol_contracts: int,
        entry_price: float,
        initial_sl: float,
        exact_tp: float,
        target_1to1: float,
        precision: int,
        open_time: float
    ) -> tuple[float, ExitReason]:
        """Monitors active position for SMC 1:1 Partial TP + BE Lock + 1:2 Runner."""
        is_long = (direction == OrderDirection.LONG)
        pu = self.contract.price_unit
        exact_sl = initial_sl
        partial_tp_executed = False
        remaining_vol = vol_contracts
        partial_fill_price = None

        self.logger.info(
            f"🎯 [{self.symbol}] Monitoring: TP1 (1:1): {target_1to1:.{precision}f} | TP2 (1:2): {exact_tp:.{precision}f} | Initial SL: {exact_sl:.{precision}f}"
        )

        while self.running:
            time.sleep(0.5)
            # 1. Fetch executable price
            try:
                ticker = self.market.get_ticker(self.symbol)
                bid1 = float(ticker.get("bid1", 0.0))
                ask1 = float(ticker.get("ask1", 0.0))
                last_p = float(ticker.get("lastPrice", 0.0))
                exec_price = (bid1 if bid1 > 0 else last_p) if is_long else (ask1 if ask1 > 0 else last_p)
                self.last_price = last_p
            except Exception:
                continue

            # Update status string for dashboard
            u_diff = (exec_price - entry_price) if is_long else (entry_price - exec_price)
            u_roe = (u_diff / entry_price) * self.leverage * 100.0
            hold_sec = time.time() - open_time
            self.active_position_desc = f"{direction.value} @ {entry_price} ({u_roe:+.2f}% ROE) | Mark: {exec_price} | Hold: {hold_sec/60:.1f}m"

            # 2. Check if position closed on exchange (via server-side SL or TP)
            if self.mode == EngineMode.LIVE and position_id:
                try:
                    open_pos = self.trader.get_open_positions(self.symbol)
                    pos_still_open = False
                    for p in open_pos:
                        if int(p.get("positionId", 0)) == int(position_id):
                            h_vol = float(p.get("holdVol", 0) or p.get("vol", 0))
                            if h_vol > 0:
                                pos_still_open = True
                                break
                    if not pos_still_open:
                        self.logger.info(f"[{self.symbol}] Position closed on KCEX.")
                        if partial_tp_executed and partial_fill_price is not None:
                            blended = (partial_fill_price + exec_price) / 2.0
                            return blended, ExitReason.MIN_PROFIT_TP_HIT if exec_price >= exact_tp else ExitReason.RATCHET_BREAKEVEN_HIT
                        return exec_price, ExitReason.MIN_PROFIT_TP_HIT if (exec_price >= exact_tp if is_long else exec_price <= exact_tp) else ExitReason.STOP_LOSS_HIT
                except Exception:
                    pass

            # 3. Smart Money Concepts: 1:1 Partial TP & Breakeven Lock
            hit_1to1 = (exec_price >= target_1to1) if is_long else (exec_price <= target_1to1)
            if hit_1to1 and not partial_tp_executed:
                partial_tp_executed = True
                partial_fill_price = target_1to1
                close_vol = remaining_vol // 2

                if close_vol >= 1 and self.mode == EngineMode.LIVE and position_id:
                    self.logger.info(f"🎉 [{self.symbol}] 1:1 TARGET REACHED! Closing 50% ({close_vol} contracts) at market...")
                    try:
                        self.trader.close_position(
                            position_id=position_id,
                            symbol=self.symbol,
                            side="LONG" if is_long else "SHORT",
                            vol_contracts=close_vol,
                            leverage=self.leverage,
                            is_market=True,
                            price=exec_price
                        )
                        remaining_vol -= close_vol
                    except Exception as ce:
                        self.logger.warning(f"[{self.symbol}] Partial close error: {ce}")

                # Move Stop Loss to Breakeven (+1 tick buffer in profit)
                new_be_sl = entry_price + (self.breakeven_buffer_ticks * pu) if is_long else entry_price - (self.breakeven_buffer_ticks * pu)
                exact_sl = round(new_be_sl, precision)
                self.logger.info(
                    f"🔒 [{self.symbol}] BREAKEVEN SL LOCKED: Stop moved to {exact_sl:.{precision}f} USDT (+{self.breakeven_buffer_ticks}t buffer). "
                    f"Remaining runner is 100% risk-free towards 1:2 target ({exact_tp:.{precision}f} USDT)!"
                )
                if self.mode == EngineMode.LIVE and position_id:
                    try:
                        self.trader.set_position_tp_sl(
                            symbol=self.symbol,
                            position_id=position_id,
                            take_profit_price=exact_tp,
                            stop_loss_price=exact_sl
                        )
                    except Exception:
                        pass

            # 4. Check Final 1:2 Take Profit Hit
            hit_tp2 = (exec_price >= exact_tp) if is_long else (exec_price <= exact_tp)
            if hit_tp2:
                self.logger.info(f"🎯 [{self.symbol}] 1:2 TAKE PROFIT HIT at {exec_price:.{precision}f} USDT!")
                if self.mode == EngineMode.LIVE and position_id:
                    try:
                        self.trader.close_position(
                            position_id=position_id,
                            symbol=self.symbol,
                            side="LONG" if is_long else "SHORT",
                            vol_contracts=remaining_vol,
                            leverage=self.leverage,
                            is_market=True,
                            price=exec_price
                        )
                    except Exception:
                        pass
                if partial_tp_executed and partial_fill_price is not None:
                    blended = (partial_fill_price + exact_tp) / 2.0
                    return blended, ExitReason.MIN_PROFIT_TP_HIT
                return exact_tp, ExitReason.MIN_PROFIT_TP_HIT

            # 5. Check Stop Loss Hit (Initial SL or Breakeven SL)
            hit_sl = (exec_price <= exact_sl) if is_long else (exec_price >= exact_sl)
            if hit_sl:
                reason = ExitReason.RATCHET_BREAKEVEN_HIT if partial_tp_executed else ExitReason.STOP_LOSS_HIT
                self.logger.info(f"🛑 [{self.symbol}] {'BREAKEVEN' if partial_tp_executed else 'STOP LOSS'} HIT at {exec_price:.{precision}f} USDT!")
                if self.mode == EngineMode.LIVE and position_id:
                    try:
                        self.trader.close_position(
                            position_id=position_id,
                            symbol=self.symbol,
                            side="LONG" if is_long else "SHORT",
                            vol_contracts=remaining_vol,
                            leverage=self.leverage,
                            is_market=True,
                            price=exec_price
                        )
                    except Exception:
                        pass
                if partial_tp_executed and partial_fill_price is not None:
                    blended = (partial_fill_price + exact_sl) / 2.0
                    return blended, reason
                return exact_sl, reason

        return exec_price, ExitReason.MANUAL_CLOSE


class MultiAssetExecutionEngine:
    """
    Master coordinator managing concurrent asset workers and providing
    consolidated, throttled portfolio logging (10 min idle, 5 min active position).
    """

    def __init__(
        self,
        assets: Optional[List[Dict[str, Any]]] = None,
        mode: EngineMode = EngineMode.LIVE,
        leverage: int = 15,
        margin_pct: float = 10.0,
        risk_reward_ratio: float = 2.0,
        mongo_logger: Optional[MongoTradeLogger] = None
    ):
        self.mode = mode
        self.leverage = leverage
        self.margin_pct = margin_pct
        self.risk_reward_ratio = risk_reward_ratio
        self.mongo_logger = mongo_logger
        self.running: bool = False
        self._shutdown_requested: bool = False

        # Shared loggers
        self.logger = DualCurrencyLogger(log_file="logs/engine_realtime.log")
        self.outcome_logger = TradeOutcomeLogger(
            txt_file="logs/trade_outcomes.txt",
            jsonl_file="logs/trade_outcomes.jsonl"
        )

        # Thread synchronization
        self.order_lock = threading.Lock()

        # Target portfolio configuration
        self.asset_configs = assets or [
            {"symbol": "TRUMP_USDT", "timeframe": "Min15", "pivot_len": 3, "leverage": self.leverage},
            {"symbol": "ETH_USDT",   "timeframe": "Hour4", "pivot_len": 5, "leverage": self.leverage},
            {"symbol": "BTC_USDT",   "timeframe": "Min15", "pivot_len": 5, "leverage": self.leverage},
            {"symbol": "DOGE_USDT",  "timeframe": "Min15", "pivot_len": 5, "leverage": self.leverage},
        ]

        # Initialize workers
        self.workers: Dict[str, AssetWorker] = {}
        for cfg in self.asset_configs:
            sym = cfg["symbol"]
            tf = cfg["timeframe"]
            plen = cfg.get("pivot_len", 5)
            lev = cfg.get("leverage", self.leverage)

            worker = AssetWorker(
                symbol=sym,
                timeframe=tf,
                pivot_len=plen,
                leverage=lev,
                margin_pct=self.margin_pct,
                risk_reward_ratio=self.risk_reward_ratio,
                mode=self.mode,
                shared_logger=self.logger,
                shared_outcome_logger=self.outcome_logger,
                shared_mongo_logger=self.mongo_logger,
                order_lock=self.order_lock
            )
            self.workers[sym] = worker

    def run(self) -> None:
        """Starts all asset workers and runs the central throttled dashboard loop."""
        self.running = True
        self._shutdown_requested = False

        # Signal handling
        def handle_sigint(signum, frame):
            self.logger.warning("\n[STOP] Caught SIGINT / SIGTERM. Stopping all workers...")
            self.stop()

        signal.signal(signal.SIGINT, handle_sigint)
        signal.signal(signal.SIGTERM, handle_sigint)

        self._print_startup_banner()

        # Start all workers
        for sym, worker in self.workers.items():
            worker.start()
            time.sleep(0.5)

        self.logger.info("All 4 asset workers running concurrently. Telemetry throttled (10m idle / 5m active)...")

        last_dashboard_time = 0.0

        while self.running and not self._shutdown_requested:
            try:
                now = time.time()
                # Check active positions across all workers
                any_in_pos = any(w.in_position for w in self.workers.values())
                self.logger.set_has_active_positions(any_in_pos)

                # Required interval: 5m (300s) if in position, 10m (600s) if idle
                dashboard_interval = 300.0 if any_in_pos else 600.0

                if now - last_dashboard_time >= dashboard_interval:
                    last_dashboard_time = now
                    self._print_portfolio_dashboard()

                time.sleep(1.0)

            except Exception as e:
                self.logger.warning(f"Coordinator error: {e}")
                time.sleep(2.0)

        # Graceful shutdown of workers
        for sym, worker in self.workers.items():
            worker.stop()
        self.logger.info("Multi-Asset Engine stopped successfully.")

    def stop(self) -> None:
        """Stops coordinator and workers."""
        self._shutdown_requested = True
        self.running = False

    def _print_startup_banner(self) -> None:
        self.logger.section("KCEX MULTI-ASSET AUTONOMOUS TRADING ENGINE")
        self.logger.info("  Strategy: Vivek Yadav Smart Money Concepts (OB + Demand/Supply)")
        self.logger.info("  Exit Plan: 50% partial TP at 1:1, Breakeven SL (+1t), 1:2 Runner")
        self.logger.info(f"  Target Leverage: {self.leverage}x isolated | Margin Allocation: {self.margin_pct}% per trade")
        self.logger.info(f"  Execution Mode: {self.mode.value.upper()}")
        self.logger.info("  Configured Asset Portfolio:")
        for cfg in self.asset_configs:
            self.logger.info(f"    • {cfg['symbol']:<12s} [{cfg['timeframe']:<6s}] @ {cfg.get('leverage', self.leverage)}x lev (Pivot Len: {cfg.get('pivot_len', 5)})")
        self.logger.info("  Logging Policy: 10-minute idle status / 5-minute active trade status (Railway log-flood prevention)")
        self.logger.info("  Manual Trading Isolation: Enabled (Direction-aware duplicate protection & position ID isolation)")
        self.logger.section("INITIALIZATION COMPLETE - WORKERS LAUNCHING")

    def _print_portfolio_dashboard(self) -> None:
        """Prints consolidated portfolio status block."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_count = sum(1 for w in self.workers.values() if w.in_position)

        # Get latest available balance
        bal_str = "N/A"
        try:
            worker0 = list(self.workers.values())[0]
            bals = worker0.trader.get_usdt_balance()
            avail = bals.get("available_usdt", 0.0)
            equity = bals.get("equity_usdt", 0.0)
            bal_str = f"Avail: {avail} USDT | Equity: {equity} USDT"
        except Exception:
            pass

        border = "=" * 80
        self.logger.info(border)
        self.logger.info(f"[PORTFOLIO STATUS] {now_str} | Active Bot Trades: {active_count} | {bal_str}")
        for sym, w in self.workers.items():
            p_str = f"{w.last_price} USDT" if w.last_price > 0 else "Querying..."
            if w.in_position:
                state_str = f"🔥 IN POSITION: {w.active_position_desc}"
            else:
                state_str = f"Scanning | {w.last_status_msg}"
            self.logger.info(f"  • {sym:<12s} [{w.timeframe:<6s}]: Price: {p_str} | {state_str}")
        self.logger.info(border)
