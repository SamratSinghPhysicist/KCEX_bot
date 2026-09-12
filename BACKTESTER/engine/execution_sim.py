"""
High-Fidelity Backtest Execution Engine
=======================================
Orchestrates virtual trade execution, dual-feed price monitoring (OHLCV + Ticks),
realistic fills, slippage, taker fees, TP/SL triggers, and wallet equity tracking.
Produces TradeOutcome records identical to the live trading engine.
"""

import os
import sys
import time
import math
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Generator, Tuple

# Ensure project root is in path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from kcex.engine.models import (
    OrderDirection,
    ExitReason,
    EngineMode,
    TradeSignal,
    TradeOutcome
)
from kcex.engine.strategy import (
    MasterplanStrategy,
    BaseStrategy,
    EMACrossoverStrategy,
    StochasticRSIStrategy,
    SmartStrategy,
    MLStrategy
)
from kcex.market import ContractInfo
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol, parse_timestamp_ms, format_ms_to_utc
from BACKTESTER.engine.data_loader import (
    OHLCVLoader,
    TickTradeStreamer,
    Candle,
    TradeTick,
    normalize_timeframe,
    timeframe_to_kcex_interval
)
from BACKTESTER.engine.market_sim import BacktestMarket

logger = logging.getLogger("BacktestEngine")


class VirtualClock:
    """
    Context manager that patches time.time() to follow the historical simulation clock.
    Ensures strategies and indicator calculations evaluate temporal cooldowns and timestamps accurately.
    """

    def __init__(self, initial_time_sec: float = 0.0):
        self.current_time_sec: float = initial_time_sec
        self._orig_time = time.time

    def set_time_sec(self, t: float):
        self.current_time_sec = t

    def __enter__(self):
        self._orig_time = time.time
        time.time = lambda: self.current_time_sec
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.time = self._orig_time


@dataclass
class EquityPoint:
    timestamp_ms: int
    timestamp_utc: str
    balance_usdt: float
    balance_inr: float
    trade_id: int
    realized_pnl_usdt: float


class BacktestExecutionEngine:
    """
    Executes historical backtests with dual-feed simulation.
    """

    def __init__(
        self,
        config: BacktestConfig,
        market: Optional[BacktestMarket] = None,
        strategy: Optional[MasterplanStrategy] = None,
        ohlcv_loader: Optional[OHLCVLoader] = None,
        tick_streamer: Optional[TickTradeStreamer] = None
    ):
        self.config = config
        self.symbol = canonicalize_symbol(config.symbol)
        self.ohlcv_loader = ohlcv_loader or OHLCVLoader(data_dir=config.ohlcv_data_dir)
        self.tick_streamer = tick_streamer or TickTradeStreamer(data_dir=config.trades_data_dir)
        self.market = market or BacktestMarket(
            inr_rate=config.inr_rate,
            fee_mode=getattr(config, "fee_mode", "LIVE"),
            maker_fee_override=config.maker_fee_override,
            taker_fee_override=config.taker_fee_override
        )
        self.contract = self.market.get_contract_detail(self.symbol)

        # Strategy setup
        self.strategy = strategy or self._create_default_strategy()

        # Virtual Wallet State
        self.wallet_balance_usdt: float = config.initial_balance_usdt
        self.outcomes: List[TradeOutcome] = []
        self.equity_curve: List[EquityPoint] = []
        self.trade_counter: int = 0
        self._interrupted: bool = False

        from strategies.filters import FilterPipeline
        self.filter_pipeline = FilterPipeline.from_config(self.config)

    def _create_default_strategy(self) -> MasterplanStrategy:
        """Instantiates the selected sub-strategy with auto_start_feed=False."""
        strat_mode = getattr(self.config, "strategy_mode", "STOCH_RSI") or "STOCH_RSI"
        strat_upper = str(strat_mode).upper()
        pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction

        if strat_upper in ("SMART", "SMART_STRATEGY"):
            sub_strat = SmartStrategy(
                market=self.market,
                symbol=self.symbol,
                interval=timeframe_to_kcex_interval(self.config.timeframe),
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                require_closed_candle=getattr(self.config, "smart_require_closed_candle", True),
                atr_filter_enabled=getattr(self.config, "smart_atr_filter_enabled", True),
                min_atr_ticks=getattr(self.config, "smart_min_atr_ticks", 2.5),
                chop_ceiling=getattr(self.config, "smart_chop_ceiling", 58.0),
                adx_trend_threshold=getattr(self.config, "smart_adx_trend_threshold", 26.0),
                use_ema200_filter=getattr(self.config, "smart_use_ema200_filter", False),
                climax_filter_enabled=getattr(self.config, "smart_climax_filter_enabled", True),
                max_atr_expansion=getattr(self.config, "smart_max_atr_expansion", 2.2),
                ema_preset=getattr(self.config, "smart_ema_preset", getattr(self.config, "ema_preset", "5/13")),
                stoch_preset=getattr(self.config, "smart_stoch_preset", getattr(self.config, "stoch_preset", "FAST_SCALP")),
                auto_start_feed=False
            )
        elif strat_upper in ("EMA", "EMA_CROSSOVER", "CROSSOVER"):
            sub_strat = EMACrossoverStrategy(
                market=self.market,
                symbol=self.symbol,
                fast_period=getattr(self.config, "ema_fast", 5),
                slow_period=getattr(self.config, "ema_slow", 13),
                ema_preset=getattr(self.config, "ema_preset", "5/13"),
                interval=timeframe_to_kcex_interval(self.config.timeframe),
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                require_closed_candle=getattr(self.config, "ema_require_closed_candle", True),
                auto_start_feed=False
            )
        elif strat_upper in ("ML", "ML_1M", "ML_MODEL", "ML_1M_MODEL"):
            sub_strat = MLStrategy(
                market=self.market,
                symbol=self.symbol,
                interval=timeframe_to_kcex_interval(self.config.timeframe),
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                auto_start_feed=False
            )
        elif strat_upper in ("ORDER_BLOCK_DEMAND", "ORDER_BOOK_DEMAND", "ORDER_BLOCK", "DEMAND_BLOCK", "SMC"):
            from strategies.order_block_demand import OrderBlockDemandStrategy
            sub_strat = OrderBlockDemandStrategy(
                market=self.market,
                symbol=self.symbol,
                interval=timeframe_to_kcex_interval(self.config.timeframe),
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                require_closed_candle=getattr(self.config, "smart_require_closed_candle", True),
                risk_reward_ratio=getattr(self.config, "risk_reward_ratio", 2.0),
                buffer_ticks=getattr(self.config, "buffer_ticks", 1),
                min_sl_ticks=getattr(self.config, "min_sl_ticks", 3),
                max_sl_ticks=getattr(self.config, "max_sl_ticks", 35),
                auto_start_feed=False
            )
        else:
            sub_strat = StochasticRSIStrategy(
                market=self.market,
                symbol=self.symbol,
                stoch_preset=getattr(self.config, "stoch_preset", "FAST_SCALP"),
                rsi_period=getattr(self.config, "stoch_rsi_period", 9),
                stoch_period=getattr(self.config, "stoch_period", 9),
                k_period=getattr(self.config, "stoch_k_period", 3),
                d_period=getattr(self.config, "stoch_d_period", 3),
                oversold=getattr(self.config, "stoch_oversold", 20.0),
                overbought=getattr(self.config, "stoch_overbought", 80.0),
                interval=timeframe_to_kcex_interval(self.config.timeframe),
                zone_filter=getattr(self.config, "stoch_zone_filter", True),
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                require_closed_candle=getattr(self.config, "stoch_require_closed_candle", True),
                auto_start_feed=False
            )

        return MasterplanStrategy(
            market=self.market,
            config=self.config,
            sub_strategy=sub_strat
        )

    def run(self) -> List[TradeOutcome]:
        """
        Executes the backtesting simulation over historical data.
        Returns the complete list of TradeOutcome records.
        """
        start_ms = parse_timestamp_ms(self.config.start_time)
        end_ms = parse_timestamp_ms(self.config.end_time)

        # 1. Load primary candles
        norm_tf = normalize_timeframe(self.config.timeframe)
        candles = self.ohlcv_loader.load_candles(
            symbol=self.symbol,
            timeframe=norm_tf,
            start_ms=start_ms,
            end_ms=end_ms
        )

        if not candles:
            # Automatically download from Binance Vision if data is not locally present
            try:
                from BACKTESTER.engine.downloader import ensure_market_data
                s_str = format_ms_to_utc(start_ms)[:10] if start_ms else "2026-07-01"
                e_str = format_ms_to_utc(end_ms)[:10] if end_ms else "2026-08-31"
                print(f"[*] Local data missing for {self.symbol} ({norm_tf}). Auto-downloading from Binance Vision ({s_str} to {e_str})...")
                ensure_market_data(
                    symbol=self.symbol,
                    timeframe=norm_tf,
                    start_date=s_str,
                    end_date=e_str,
                    download_trades=self.config.use_tick_data,
                    base_dir="BACKTESTER"
                )
                candles = self.ohlcv_loader.load_candles(
                    symbol=self.symbol,
                    timeframe=norm_tf,
                    start_ms=start_ms,
                    end_ms=end_ms
                )
            except Exception as e:
                logger.warning("Auto-download attempt failed: %s", e)

        if not candles:
            logger.warning(
                "No OHLCV candles found for %s (%s) within range [%s, %s]",
                self.symbol, norm_tf, format_ms_to_utc(start_ms), format_ms_to_utc(end_ms)
            )
            return []

        # Seed initial equity point
        self.equity_curve.append(EquityPoint(
            timestamp_ms=candles[0].open_time_ms,
            timestamp_utc=format_ms_to_utc(candles[0].open_time_ms),
            balance_usdt=self.wallet_balance_usdt,
            balance_inr=self.wallet_balance_usdt * self.config.inr_rate,
            trade_id=0,
            realized_pnl_usdt=0.0
        ))

        # Seed market historical candles
        self.market.set_candles(self.symbol, norm_tf, candles)

        clock = VirtualClock(initial_time_sec=candles[0].close_time_ms / 1000.0)

        with clock:
            candle_idx = 0
            total_candles = len(candles)

            while candle_idx < total_candles and not self._interrupted:
                cur_candle = candles[candle_idx]
                sim_time_sec = cur_candle.close_time_ms / 1000.0
                clock.set_time_sec(sim_time_sec)
                self.market.set_time(cur_candle.close_time_ms, current_price=cur_candle.close)

                # Check if strategy is ready for a new signal
                if not self.strategy.sub_strategy.trade_in_progress:
                    signal = self.strategy.get_signal()
                    if signal:
                        # Evaluate against Regime & Trend Filter Pipeline (with sufficient lookback for HTF resampling)
                        history_slice = candles[max(0, candle_idx - 4000):candle_idx + 1]
                        allowed, reject_reason = self.filter_pipeline.evaluate(
                            signal=signal,
                            candles=history_slice,
                            current_time=sim_time_sec
                        )
                        if not allowed:
                            if hasattr(self.strategy, "on_trade_rejected"):
                                self.strategy.on_trade_rejected()
                            elif hasattr(self.strategy.sub_strategy, "trade_in_progress"):
                                self.strategy.sub_strategy.trade_in_progress = False
                            candle_idx += 1
                            continue

                        self.trade_counter += 1
                        trade_id = self.trade_counter

                        # Execute the trade
                        outcome, exit_candle_idx = self._execute_simulated_trade(
                            trade_id=trade_id,
                            signal=signal,
                            entry_candle=cur_candle,
                            all_candles=candles,
                            entry_idx=candle_idx,
                            clock=clock
                        )

                        if outcome:
                            self.outcomes.append(outcome)
                            self.strategy.on_trade_completed(outcome)

                            # Record equity progression
                            self.wallet_balance_usdt = outcome.balance_after_trade_usdt or self.wallet_balance_usdt
                            self.equity_curve.append(EquityPoint(
                                timestamp_ms=int(outcome.close_time * 1000),
                                timestamp_utc=format_ms_to_utc(int(outcome.close_time * 1000)),
                                balance_usdt=self.wallet_balance_usdt,
                                balance_inr=self.wallet_balance_usdt * self.config.inr_rate,
                                trade_id=trade_id,
                                realized_pnl_usdt=outcome.realized_pnl_usdt
                            ))

                            # Advance candle index to when trade closed
                            if exit_candle_idx and exit_candle_idx > candle_idx:
                                candle_idx = exit_candle_idx
                            
                            # Realtime playback delay if requested
                            if self.config.playback_speed > 0:
                                sim_delay = max(0.01, min(1.0, outcome.duration_seconds / self.config.playback_speed))
                                time.sleep(sim_delay)

                            # Check max_trades limit
                            if self.config.max_trades > 0 and self.trade_counter >= self.config.max_trades:
                                break

                candle_idx += 1

        return self.outcomes

    def _execute_simulated_trade(
        self,
        trade_id: int,
        signal: TradeSignal,
        entry_candle: Candle,
        all_candles: List[Candle],
        entry_idx: int,
        clock: VirtualClock
    ) -> Tuple[TradeOutcome, int]:
        """
        Simulates entry execution, high-fidelity tick monitoring for TP/SL,
        and outcome reconciliation.
        """
        direction = signal.direction
        pu = self.contract.price_unit
        cs = self.contract.contract_size
        ps = self.contract.price_precision
        leverage = self.config.leverage

        # 1. Determine Entry Price (with slippage)
        # Entry happens at candle close (or next bar open)
        raw_entry = entry_candle.close
        is_maker = (getattr(self.config, "execution_style", "PURE_MARKET") == "MAKER_HYBRID") or (getattr(self.config, "order_type", "MARKET") == "LIMIT")
        apply_slip = getattr(self.config, "slippage_enabled", False) or getattr(self.config, "slippage_ticks", 0) > 0
        slippage_delta = (self.config.slippage_ticks * pu) if (apply_slip and not is_maker) else 0.0

        if direction == OrderDirection.LONG:
            entry_price = round(raw_entry + slippage_delta, ps)
        else:
            entry_price = round(raw_entry - slippage_delta, ps)

        # Queue dynamics check for maker limit orders (Research V3 Queue Dynamics)
        if is_maker and getattr(self.config, "queue_dynamics_enabled", False) and self.config.use_tick_data:
            timeout_s = float(getattr(self.config, "maker_queue_timeout_seconds", 10.0))
            entry_ms = entry_candle.close_time_ms
            tick_gen = self.tick_streamer.stream_ticks(self.symbol, start_ms=entry_ms)
            filled = False
            for tick in tick_gen:
                t_elapsed = (tick.timestamp_ms - entry_ms) / 1000.0
                if t_elapsed > timeout_s:
                    break
                if direction == OrderDirection.LONG and tick.price <= entry_price:
                    filled = True
                    break
                elif direction == OrderDirection.SHORT and tick.price >= entry_price:
                    filled = True
                    break
            if not filled:
                # Maker limit order timed out in queue without fill
                return None, entry_idx

        # 2. Sizing & Margin
        min_vol = int(self.contract.min_volume)
        vol_mode = (getattr(self.config, "volume_mode", "MULTIPLIER") or "MULTIPLIER").upper()
        if getattr(self.config, "volume_contracts", None) is not None:
            vol_contracts = max(min_vol, int(self.config.volume_contracts))
        elif vol_mode == "MIN":
            vol_contracts = min_vol
        else: # MULTIPLIER
            mult = max(1.0, float(getattr(self.config, "volume_multiplier", 1.0) or 1.0))
            vol_contracts = max(min_vol, int(math.ceil(min_vol * mult)))

        underlying_qty = vol_contracts * cs
        notional_usdt = underlying_qty * entry_price
        margin_usdt = notional_usdt / leverage if leverage > 0 else notional_usdt
        open_time_sec = entry_candle.close_time_ms / 1000.0

        # 3. Calculate Exact TP & SL (supports ATR Dynamic Volatility Targets)
        atr_val = None
        if getattr(self.config, "use_atr_targets", False):
            from strategies.filters import compute_atr_series
            history = all_candles[max(0, entry_idx - 30):entry_idx + 1]
            if len(history) >= 15:
                highs = [c.high for c in history]
                lows = [c.low for c in history]
                closes = [c.close for c in history]
                atrs = compute_atr_series(highs, lows, closes, period=14)
                if atrs and atrs[-1] > 0:
                    atr_val = atrs[-1]

        is_ml_sig = (signal.sub_strategy_name in ("ML_1M_MODEL", "MLStrategy")) or (getattr(self.config, "strategy_mode", "").upper() in ("ML", "ML_1M", "ML_MODEL", "ML_1M_MODEL")) or getattr(self.config, "dynamic_tp", False)
        is_smc_sig = ("ORDER_BLOCK" in str(signal.metadata.get("strategy_mode", "")).upper()) or ("OrderBlock" in signal.sub_strategy_name) or (getattr(self.config, "strategy_mode", "").upper() in ("ORDER_BLOCK_DEMAND", "ORDER_BOOK_DEMAND", "ORDER_BLOCK", "DEMAND_BLOCK", "SMC"))
        if (is_ml_sig or is_smc_sig) and signal.metadata and "target_ticks" in signal.metadata:
            effective_tp_ticks = int(signal.metadata["target_ticks"])
        else:
            effective_tp_ticks = self.config.tp_ticks

        if (is_ml_sig or is_smc_sig) and signal.metadata and "target_sl_ticks" in signal.metadata:
            effective_sl_ticks = int(signal.metadata["target_sl_ticks"])
            effective_sl_roe = None
        else:
            effective_sl_ticks = self.config.sl_ticks
            effective_sl_roe = self.config.sl_roe_pct

        exact_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=effective_tp_ticks,
            precision=ps,
            atr_value=atr_val
        )
        exact_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=effective_sl_roe,
            sl_ticks=effective_sl_ticks,
            sl_price_pct=self.config.sl_price_pct,
            price_unit=pu,
            precision=ps,
            atr_value=atr_val
        )
        initial_sl = exact_sl

        # SMC 1:1 Partial TP and Breakeven Runner state
        target_1to1 = float(signal.metadata.get("target_1to1_price", 0.0)) if (is_smc_sig and signal and signal.metadata) else None
        partial_tp_enabled = bool(signal.metadata.get("partial_tp_enabled", getattr(self.config, "partial_tp_enabled", True))) if is_smc_sig else False
        be_buf_ticks = int(signal.metadata.get("breakeven_buffer_ticks", getattr(self.config, "breakeven_buffer_ticks", 1))) if is_smc_sig else 1
        smc_1x_mode = str(getattr(self.config, "smc_1x_exit_mode", "1TO2_WITH_BE")).upper()
        partial_tp_executed = False
        partial_fill_price = None
        remaining_vol = vol_contracts

        exit_price = entry_price
        exit_reason = ExitReason.UNKNOWN
        exit_time_sec = open_time_sec
        exit_candle_idx = entry_idx

        # 4. Check immediate profit condition at fill
        if self.strategy.is_better_than_min_profit(direction, entry_price, exact_tp):
            exit_price = exact_tp
            exit_reason = ExitReason.IMMEDIATE_PROFIT_CLOSE
            exit_time_sec = open_time_sec + 0.1
        else:
            # 5. Active Position Monitoring
            entry_ms = entry_candle.close_time_ms

            # Attempt High-Fidelity Tick Stream Monitoring if enabled
            hit_via_ticks = False
            if self.config.use_tick_data:
                tick_gen = self.tick_streamer.stream_ticks(self.symbol, start_ms=entry_ms)
                for tick in tick_gen:
                    # Phase V2.2 Champion Micro-Excursion Tick Ratchet
                    if getattr(self.config, "ratchet_enabled", False):
                        favorable_ticks = (tick.price - entry_price) / pu if direction == OrderDirection.LONG else (entry_price - tick.price) / pu
                        elapsed_sec = (tick.timestamp_ms / 1000.0) - open_time_sec

                        # Tier 1: Stalled >= 10s at >= +1.0t -> Tighten SL to -1 tick
                        t1_trig = float(getattr(self.config, "ratchet_trigger_ticks", 1.0))
                        t1_stall = float(getattr(self.config, "ratchet_stall_seconds", 10.0))
                        t1_tight = float(getattr(self.config, "ratchet_tighten_ticks", 1.0))
                        if favorable_ticks >= t1_trig and elapsed_sec >= t1_stall:
                            new_sl = entry_price - (t1_tight * pu) if direction == OrderDirection.LONG else entry_price + (t1_tight * pu)
                            if (direction == OrderDirection.LONG and new_sl > exact_sl) or (direction == OrderDirection.SHORT and new_sl < exact_sl):
                                exact_sl = round(new_sl, ps)

                        # Tier 2: Favorable excursion >= +2.5t -> Lock at Breakeven (0.0t)
                        t2_trig = float(getattr(self.config, "ratchet_breakeven_ticks", 2.5))
                        if favorable_ticks >= t2_trig:
                            be_sl = round(entry_price, ps)
                            if (direction == OrderDirection.LONG and be_sl > exact_sl) or (direction == OrderDirection.SHORT and be_sl < exact_sl):
                                exact_sl = be_sl

                    # 75x Maintenance Margin Liquidation Barrier Check
                    if getattr(self.config, "simulate_intra_tick_liquidation", True) and leverage > 0:
                        mmr = float(getattr(self.contract, "maintenance_margin_ratio", 0.01) or 0.01)
                        if direction == OrderDirection.LONG:
                            liq_p = entry_price * (1.0 - (1.0 / float(leverage)) + mmr)
                            if tick.price <= liq_p:
                                exit_price = round(liq_p, ps)
                                exit_reason = ExitReason.LIQUIDATION_HIT
                                exit_time_sec = tick.timestamp_ms / 1000.0
                                hit_via_ticks = True
                                break
                        else:
                            liq_p = entry_price * (1.0 + (1.0 / float(leverage)) - mmr)
                            if tick.price >= liq_p:
                                exit_price = round(liq_p, ps)
                                exit_reason = ExitReason.LIQUIDATION_HIT
                                exit_time_sec = tick.timestamp_ms / 1000.0
                                hit_via_ticks = True
                                break

                    # Smart Money Concepts: 1:1 Partial TP & Breakeven Lock (Tick Stream)
                    if is_smc_sig and partial_tp_enabled and target_1to1 and not partial_tp_executed:
                        hit_1to1 = (tick.price >= target_1to1) if direction == OrderDirection.LONG else (tick.price <= target_1to1)
                        if hit_1to1:
                            if remaining_vol >= 2:
                                close_vol = remaining_vol // 2
                                partial_fill_price = target_1to1
                                partial_tp_executed = True
                                remaining_vol -= close_vol
                                new_be_sl = entry_price + (be_buf_ticks * pu) if direction == OrderDirection.LONG else entry_price - (be_buf_ticks * pu)
                                exact_sl = round(new_be_sl, ps)
                            else:
                                if smc_1x_mode == "1TO1_TP":
                                    exit_price = target_1to1
                                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                                    exit_time_sec = tick.timestamp_ms / 1000.0
                                    hit_via_ticks = True
                                    break
                                else:  # 1TO2_WITH_BE
                                    partial_tp_executed = True
                                    new_be_sl = entry_price + (be_buf_ticks * pu) if direction == OrderDirection.LONG else entry_price - (be_buf_ticks * pu)
                                    exact_sl = round(new_be_sl, ps)

                    if direction == OrderDirection.LONG:
                        # TP hit (Maker limit order fills at exact TP, 0 exit slippage)
                        if tick.price >= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                        # SL hit (Market stop order crosses spread)
                        elif tick.price <= exact_sl:
                            exit_price = exact_sl
                            if apply_slip and getattr(self.config, "slippage_ticks", 0) > 0:
                                exit_price = round(exact_sl - (self.config.slippage_ticks * pu), ps)

                            if abs(exact_sl - entry_price) <= (0.2 * pu):
                                exit_reason = ExitReason.RATCHET_BREAKEVEN_HIT
                            elif abs(exact_sl - entry_price) < abs(initial_sl - entry_price):
                                exit_reason = ExitReason.RATCHET_TIGHTEN_HIT
                            else:
                                exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                    else: # SHORT
                        # TP hit (Maker limit order fills at exact TP, 0 exit slippage)
                        if tick.price <= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                        # SL hit (Market stop order crosses spread)
                        elif tick.price >= exact_sl:
                            exit_price = exact_sl
                            if apply_slip and getattr(self.config, "slippage_ticks", 0) > 0:
                                exit_price = round(exact_sl + (self.config.slippage_ticks * pu), ps)

                            if abs(exact_sl - entry_price) <= (0.2 * pu):
                                exit_reason = ExitReason.RATCHET_BREAKEVEN_HIT
                            elif abs(exact_sl - entry_price) < abs(initial_sl - entry_price):
                                exit_reason = ExitReason.RATCHET_TIGHTEN_HIT
                            else:
                                exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break

                    # Duration Monitoring & Time-Decay Safeguard
                    if getattr(self.config, "duration_filter_enabled", False):
                        tick_time_sec = tick.timestamp_ms / 1000.0
                        elapsed_sec = tick_time_sec - open_time_sec
                        max_hold_s = float(getattr(self.config, "duration_max_hold_seconds", 90.0))
                        if elapsed_sec >= max_hold_s:
                            action = (getattr(self.config, "duration_action", "CLOSE") or "CLOSE").upper()
                            if action == "CLOSE":
                                exit_price = tick.price
                                exit_reason = ExitReason.TIMEOUT_CLOSE
                                exit_time_sec = tick_time_sec
                                hit_via_ticks = True
                                break
                            elif action == "SCRATCH_OR_MARKET":
                                u_diff = (tick.price - entry_price) if direction == OrderDirection.LONG else (entry_price - tick.price)
                                if u_diff >= -1.0 * pu:
                                    exit_price = tick.price
                                    exit_reason = ExitReason.DURATION_SCRATCH
                                    exit_time_sec = tick_time_sec
                                    hit_via_ticks = True
                                    break
                                else:
                                    if direction == OrderDirection.LONG:
                                        exact_sl = max(exact_sl, entry_price)
                                    else:
                                        exact_sl = min(exact_sl, entry_price)
                            elif action == "TIGHTEN_SL":
                                if direction == OrderDirection.LONG:
                                    exact_sl = max(exact_sl, entry_price)
                                else:
                                    exact_sl = min(exact_sl, entry_price)

                if hit_via_ticks:
                    # Find candle index matching exit_time_sec
                    exit_ms = int(exit_time_sec * 1000)
                    for idx in range(entry_idx, len(all_candles)):
                        if all_candles[idx].close_time_ms >= exit_ms:
                            exit_candle_idx = idx
                            break

            # If ticks not available or no hit found via ticks, use Candle High/Low Fallback
            if not hit_via_ticks and self.config.tick_fallback_to_candle:
                for idx in range(entry_idx + 1, len(all_candles)):
                    c = all_candles[idx]

                    # 75x Maintenance Margin Liquidation Check on Candle High/Low
                    if getattr(self.config, "simulate_intra_tick_liquidation", True) and leverage > 0:
                        mmr = float(getattr(self.contract, "maintenance_margin_ratio", 0.01) or 0.01)
                        if direction == OrderDirection.LONG:
                            liq_p = entry_price * (1.0 - (1.0 / float(leverage)) + mmr)
                            if c.low <= liq_p:
                                exit_price = round(liq_p, ps)
                                exit_reason = ExitReason.LIQUIDATION_HIT
                                exit_time_sec = c.close_time_ms / 1000.0
                                exit_candle_idx = idx
                                break
                        else:
                            liq_p = entry_price * (1.0 + (1.0 / float(leverage)) - mmr)
                            if c.high >= liq_p:
                                exit_price = round(liq_p, ps)
                                exit_reason = ExitReason.LIQUIDATION_HIT
                                exit_time_sec = c.close_time_ms / 1000.0
                                exit_candle_idx = idx
                                break

                    # Smart Money Concepts: 1:1 Partial TP & Breakeven Lock (Candle Fallback)
                    just_hit_1to1 = False
                    if is_smc_sig and partial_tp_enabled and target_1to1 and not partial_tp_executed:
                        hit_1to1 = (c.high >= target_1to1) if direction == OrderDirection.LONG else (c.low <= target_1to1)
                        if hit_1to1:
                            just_hit_1to1 = True
                            if remaining_vol >= 2:
                                close_vol = remaining_vol // 2
                                partial_fill_price = target_1to1
                                partial_tp_executed = True
                                remaining_vol -= close_vol
                                new_be_sl = entry_price + (be_buf_ticks * pu) if direction == OrderDirection.LONG else entry_price - (be_buf_ticks * pu)
                                exact_sl = round(new_be_sl, ps)
                            else:
                                if smc_1x_mode == "1TO1_TP":
                                    exit_price = target_1to1
                                    exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                                    exit_time_sec = c.close_time_ms / 1000.0
                                    exit_candle_idx = idx
                                    break
                                else:  # 1TO2_WITH_BE
                                    partial_tp_executed = True
                                    new_be_sl = entry_price + (be_buf_ticks * pu) if direction == OrderDirection.LONG else entry_price - (be_buf_ticks * pu)
                                    exact_sl = round(new_be_sl, ps)

                    if direction == OrderDirection.LONG:
                        if c.high >= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break
                        elif (c.close <= exact_sl if just_hit_1to1 else c.low <= exact_sl):
                            exit_price = exact_sl
                            if apply_slip and getattr(self.config, "slippage_ticks", 0) > 0:
                                exit_price = round(exact_sl - (self.config.slippage_ticks * pu), ps)
                            exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break
                    else: # SHORT
                        if c.low <= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break
                        elif (c.close >= exact_sl if just_hit_1to1 else c.high >= exact_sl):
                            exit_price = exact_sl
                            if apply_slip and getattr(self.config, "slippage_ticks", 0) > 0:
                                exit_price = round(exact_sl + (self.config.slippage_ticks * pu), ps)
                            exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break

                    # Duration Monitoring & Time-Decay Safeguard in candle fallback
                    if getattr(self.config, "duration_filter_enabled", False):
                        c_time_sec = c.close_time_ms / 1000.0
                        elapsed_sec = c_time_sec - open_time_sec
                        max_hold_s = float(getattr(self.config, "duration_max_hold_seconds", 90.0))
                        if elapsed_sec >= max_hold_s:
                            action = (getattr(self.config, "duration_action", "CLOSE") or "CLOSE").upper()
                            if action == "CLOSE":
                                exit_price = c.close
                                exit_reason = ExitReason.TIMEOUT_CLOSE
                                exit_time_sec = c_time_sec
                                exit_candle_idx = idx
                                break
                            elif action == "SCRATCH_OR_MARKET":
                                u_diff = (c.close - entry_price) if direction == OrderDirection.LONG else (entry_price - c.close)
                                if u_diff >= -1.0 * pu:
                                    exit_price = c.close
                                    exit_reason = ExitReason.DURATION_SCRATCH
                                    exit_time_sec = c_time_sec
                                    exit_candle_idx = idx
                                    break
                                else:
                                    if direction == OrderDirection.LONG:
                                        exact_sl = max(exact_sl, entry_price)
                                    else:
                                        exact_sl = min(exact_sl, entry_price)
                            elif action == "TIGHTEN_SL":
                                if direction == OrderDirection.LONG:
                                    exact_sl = max(exact_sl, entry_price)
                                else:
                                    exact_sl = min(exact_sl, entry_price)

            # If still open at end of data, close at final candle close
            if exit_reason == ExitReason.UNKNOWN:
                exit_price = all_candles[-1].close
                exit_reason = ExitReason.MANUAL_CLOSE
                exit_time_sec = all_candles[-1].close_time_ms / 1000.0
                exit_candle_idx = len(all_candles) - 1

        # 6. Financial Reconciliation
        duration = max(0.1, exit_time_sec - open_time_sec)

        # Blended outcome pricing if 50% was closed at 1:1 TP and runner exited separately
        if partial_tp_executed and partial_fill_price is not None and remaining_vol < vol_contracts:
            closed_partial_vol = vol_contracts - remaining_vol
            blended_exit_price = ((closed_partial_vol * partial_fill_price) + (remaining_vol * exit_price)) / vol_contracts
            exit_price = round(blended_exit_price, ps)

        price_diff = (exit_price - entry_price) if direction == OrderDirection.LONG else (entry_price - exit_price)

        fee_rate = self.contract.taker_fee_rate
        fee_open = notional_usdt * fee_rate
        fee_close = (underlying_qty * exit_price) * fee_rate
        fee_total = fee_open + fee_close
        fee_total_inr = fee_total * self.config.inr_rate

        realized_pnl_usdt = (underlying_qty * price_diff) - fee_total
        realized_pnl_inr = realized_pnl_usdt * self.config.inr_rate

        notional_inr = notional_usdt * self.config.inr_rate
        margin_inr = margin_usdt * self.config.inr_rate
        roe_pct = (realized_pnl_usdt / margin_usdt * 100.0) if margin_usdt > 0 else 0.0
        pnl_pct = (price_diff / entry_price * 100.0) if entry_price > 0 else 0.0

        new_balance_usdt = self.wallet_balance_usdt + realized_pnl_usdt
        new_balance_inr = new_balance_usdt * self.config.inr_rate

        outcome = TradeOutcome(
            trade_id=trade_id,
            symbol=self.symbol,
            direction=direction,
            sub_strategy_name=signal.sub_strategy_name,
            mode=EngineMode.DRY_RUN,
            leverage=leverage,
            vol_contracts=vol_contracts,
            contract_size=cs,
            underlying_quantity=underlying_qty,
            base_coin=self.contract.base_coin,
            entry_price=entry_price,
            exit_price=exit_price,
            min_profit_tp_price=exact_tp,
            stop_loss_price=exact_sl,
            price_unit=pu,
            price_precision=ps,
            open_time=open_time_sec,
            close_time=exit_time_sec,
            duration_seconds=duration,
            notional_value_usdt=notional_usdt,
            notional_value_inr=notional_inr,
            margin_used_usdt=margin_usdt,
            margin_used_inr=margin_inr,
            realized_pnl_usdt=realized_pnl_usdt,
            realized_pnl_inr=realized_pnl_inr,
            pnl_percentage=pnl_pct,
            roe_percentage=roe_pct,
            fee_open_usdt=fee_open,
            fee_close_usdt=fee_close,
            fee_total_usdt=fee_total,
            fee_total_inr=fee_total_inr,
            inr_rate=self.config.inr_rate,
            exit_reason=exit_reason,
            balance_after_trade_usdt=new_balance_usdt,
            balance_after_trade_inr=new_balance_inr,
            smc_zone_id=signal.metadata.get("zone_id") if (is_smc_sig and signal and signal.metadata) else None,
            smc_zone_type=signal.metadata.get("zone_type") if (is_smc_sig and signal and signal.metadata) else None,
            smc_zone_high=signal.metadata.get("zone_high") if (is_smc_sig and signal and signal.metadata) else None,
            smc_zone_low=signal.metadata.get("zone_low") if (is_smc_sig and signal and signal.metadata) else None,
            smc_fvg_size=signal.metadata.get("fvg_size") if (is_smc_sig and signal and signal.metadata) else None,
            smc_target_1to1=signal.metadata.get("target_1to1_price") if (is_smc_sig and signal and signal.metadata) else None,
            smc_target_1to2=signal.metadata.get("target_1to2_price") if (is_smc_sig and signal and signal.metadata) else None,
            smc_partial_tp_hit=partial_tp_executed if is_smc_sig else False,
            ml_confidence=signal.metadata.get("confidence") if (is_ml_sig and signal and signal.metadata) else None,
            ml_prob_buy=signal.metadata.get("prob_buy") if (is_ml_sig and signal and signal.metadata) else None,
            ml_prob_sell=signal.metadata.get("prob_sell") if (is_ml_sig and signal and signal.metadata) else None,
            ml_prob_wait=signal.metadata.get("prob_wait") if (is_ml_sig and signal and signal.metadata) else None,
            ml_tp_ticks=signal.metadata.get("target_ticks") if (is_ml_sig and signal and signal.metadata) else None,
            ml_sl_ticks=signal.metadata.get("target_sl_ticks") if (is_ml_sig and signal and signal.metadata) else None,
            ml_atr_14=signal.metadata.get("atr_14") if (is_ml_sig and signal and signal.metadata) else None
        )

        return outcome, exit_candle_idx
