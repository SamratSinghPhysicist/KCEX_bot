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
    BaseSubStrategy,
    DirectionalCycleSubStrategy,
    EMACrossoverSubStrategy,
    StochasticRSISubStrategy,
    MicrostructureSubStrategy
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

    def _create_default_strategy(self) -> MasterplanStrategy:
        """Instantiates the selected sub-strategy with auto_start_feed=False."""
        strat_mode = getattr(self.config, "strategy_mode", "EMA_CROSSOVER") or "EMA_CROSSOVER"
        strat_upper = str(strat_mode).upper()
        pref_dir = None if getattr(self.config, "bi_directional", True) else self.config.direction

        if strat_upper in ("EMA", "EMA_CROSSOVER", "CROSSOVER"):
            sub_strat = EMACrossoverSubStrategy(
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
        elif strat_upper in ("STOCH_RSI", "STOCHASTIC_RSI", "STOCH"):
            sub_strat = StochasticRSISubStrategy(
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
        elif strat_upper == "MICROSTRUCTURE":
            sub_strat = MicrostructureSubStrategy(
                market=self.market,
                symbol=self.symbol,
                preferred_direction=pref_dir,
                cooldown_seconds=self.config.cooldown_seconds,
                tp_ticks=self.config.tp_ticks,
                dynamic_tp=getattr(self.config, "dynamic_tp", False),
                auto_start_feed=False
            )
        else:
            sub_strat = DirectionalCycleSubStrategy(
                direction=self.config.direction,
                cooldown_seconds=self.config.cooldown_seconds
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
        slippage = self.config.slippage_ticks * pu
        if direction == OrderDirection.LONG:
            entry_price = round(raw_entry + slippage, ps)
        else:
            entry_price = round(raw_entry - slippage, ps)

        # 2. Sizing & Margin
        if self.config.volume_mode == "CONTRACTS" and self.config.volume_contracts:
            vol_contracts = self.config.volume_contracts
        elif self.config.volume_mode == "MIN":
            vol_contracts = int(self.contract.min_volume)
        else: # MULTIPLIER
            mult = max(1.0, self.config.volume_multiplier)
            vol_contracts = int(math.ceil(self.contract.min_volume * mult))

        underlying_qty = vol_contracts * cs
        notional_usdt = underlying_qty * entry_price
        margin_usdt = notional_usdt / leverage if leverage > 0 else notional_usdt
        open_time_sec = entry_candle.close_time_ms / 1000.0

        # 3. Calculate Exact TP & SL
        exact_tp = self.strategy.calculate_min_profit_tp(
            direction=direction,
            entry_price=entry_price,
            price_unit=pu,
            tp_ticks=self.config.tp_ticks,
            precision=ps
        )
        exact_sl = self.strategy.calculate_stop_loss(
            direction=direction,
            entry_price=entry_price,
            leverage=leverage,
            sl_roe_pct=self.config.sl_roe_pct,
            sl_ticks=self.config.sl_ticks,
            sl_price_pct=self.config.sl_price_pct,
            price_unit=pu,
            precision=ps
        )

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
                    if direction == OrderDirection.LONG:
                        # TP hit
                        if tick.price >= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                        # SL hit
                        elif tick.price <= exact_sl:
                            exit_price = exact_sl
                            exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                    else: # SHORT
                        # TP hit
                        if tick.price <= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break
                        # SL hit
                        elif tick.price >= exact_sl:
                            exit_price = exact_sl
                            exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = tick.timestamp_ms / 1000.0
                            hit_via_ticks = True
                            break

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
                    if direction == OrderDirection.LONG:
                        if c.high >= exact_tp:
                            exit_price = exact_tp
                            exit_reason = ExitReason.MIN_PROFIT_TP_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break
                        elif c.low <= exact_sl:
                            exit_price = exact_sl
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
                        elif c.high >= exact_sl:
                            exit_price = exact_sl
                            exit_reason = ExitReason.STOP_LOSS_HIT
                            exit_time_sec = c.close_time_ms / 1000.0
                            exit_candle_idx = idx
                            break

            # If still open at end of data, close at final candle close
            if exit_reason == ExitReason.UNKNOWN:
                exit_price = all_candles[-1].close
                exit_reason = ExitReason.MANUAL_CLOSE
                exit_time_sec = all_candles[-1].close_time_ms / 1000.0
                exit_candle_idx = len(all_candles) - 1

        # 6. Financial Reconciliation
        duration = max(0.1, exit_time_sec - open_time_sec)
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
            balance_after_trade_inr=new_balance_inr
        )

        return outcome, exit_candle_idx
