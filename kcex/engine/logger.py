"""
KCEX Dual-Currency & Trade Outcome Loggers
==========================================
Provides real-time beautifully formatted logging with dual-currency (USDT & INR)
reporting, plus a dedicated trade outcome journal that records detailed execution
cards and cumulative performance statistics.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from typing import Optional, Any
from kcex.engine.models import TradeOutcome, CumulativeStats


class DualCurrencyLogger:
    """
    Real-time logger that outputs to both console and a realtime log file.
    Includes built-in dual-currency conversion helpers (USDT <-> INR).
    """

    def __init__(
        self,
        log_file: str = "logs/engine_realtime.log",
        inr_rate: float = 94.45,
        log_level: int = logging.INFO
    ):
        self.log_file = log_file
        self.inr_rate = inr_rate
        self._ensure_dir()

        # Set up standard logger
        self.logger = logging.getLogger("KCEXEngine")
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        # Clear existing handlers if re-initialized
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_fmt = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_fmt)
        self.logger.addHandler(console_handler)

        # File Handler (UTF-8, immediate flush)
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8", mode="a")
        file_handler.setLevel(log_level)
        file_fmt = logging.Formatter(
            fmt="%(asctime)s [%(levelname)-7s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_fmt)
        self.logger.addHandler(file_handler)

    def _ensure_dir(self) -> None:
        directory = os.path.dirname(self.log_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def set_inr_rate(self, rate: float) -> None:
        """Updates the current exchange rate."""
        if rate > 0:
            self.inr_rate = rate

    def format_dual(self, usdt_val: float, precision: int = 4) -> str:
        """Formats a value in both USDT and INR."""
        inr_val = usdt_val * self.inr_rate
        sign = "+" if usdt_val > 0 else ""
        return f"{sign}{usdt_val:.{precision}f} USDT ({sign}INR {inr_val:.2f})"

    def format_price(self, price: float, precision: int = 4) -> str:
        """Formats a price in USDT and INR equivalent."""
        inr_val = price * self.inr_rate
        return f"{price:.{precision}f} USDT (INR {inr_val:.2f})"

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.exception(msg, *args, **kwargs)

    def section(self, title: str) -> None:
        border = "=" * 76
        self.logger.info(border)
        self.logger.info(f"   {title}")
        self.logger.info(border)


class TradeOutcomeLogger:
    """
    Dedicated logger that records every closed trade outcome to both
    a human-readable text file and a structured JSONL file.
    Tracks and displays running cumulative performance statistics.
    """

    def __init__(
        self,
        txt_file: str = "logs/trade_outcomes.txt",
        jsonl_file: str = "logs/trade_outcomes.jsonl"
    ):
        self.txt_file = txt_file
        self.jsonl_file = jsonl_file
        self.cumulative = CumulativeStats()
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        for f in (self.txt_file, self.jsonl_file):
            d = os.path.dirname(f)
            if d:
                os.makedirs(d, exist_ok=True)

    def log_outcome(self, outcome: TradeOutcome) -> str:
        """
        Appends trade outcome to files and returns formatted text card.
        """
        self.cumulative.update(outcome)
        timestamp_str = datetime.fromtimestamp(outcome.close_time).strftime("%Y-%m-%d %H:%M:%S")
        open_time_str = datetime.fromtimestamp(outcome.open_time).strftime("%Y-%m-%d %H:%M:%S")

        pnl_sign = "+" if outcome.realized_pnl_usdt > 0 else ""
        roe_sign = "+" if outcome.roe_percentage > 0 else ""

        mode_badge = "[🔴 LIVE TRADING]" if outcome.mode.value == "live" else "[🟢 SIMULATED / DRY-RUN]"

        tp_offset = abs(outcome.min_profit_tp_price - outcome.entry_price)
        tp_ticks = round(tp_offset / outcome.price_unit) if outcome.price_unit > 0 else 1
        sl_offset = abs(outcome.stop_loss_price - outcome.entry_price)

        sl_ticks = round(sl_offset / outcome.price_unit) if outcome.price_unit > 0 else 0
        sl_pct = (sl_offset / outcome.entry_price * 100.0) if outcome.entry_price > 0 else 0.0
        sl_roe = sl_pct * outcome.leverage

        card_lines = [
            "=" * 78,
            f"TRADE #{outcome.trade_id} OUTCOME JOURNAL | Closed at: {timestamp_str} | {mode_badge}",
            "=" * 78,
            f"Execution Mode     : {mode_badge}",
            f"Symbol & Direction : {outcome.symbol} [{outcome.direction.value}] ({outcome.leverage}x isolated)",
            f"Strategy Name      : {outcome.sub_strategy_name}",
            f"Volume Executed    : {outcome.vol_contracts} contract(s) ({outcome.underlying_quantity:.4f} coins)",
            f"Trade Quantity     : {outcome.notional_value_usdt:.4f} USDT (INR {outcome.notional_value_inr:.2f}) [Notional exposure]",
            f"Margin Committed   : {outcome.margin_used_usdt:.4f} USDT (INR {outcome.margin_used_inr:.2f}) [Trade Qty / {outcome.leverage}x leverage]",
            f"Entry Price        : {outcome.entry_price:.4f} USDT (Opened: {open_time_str})",
            f"Exit Price         : {outcome.exit_price:.4f} USDT (Duration: {outcome.duration_seconds:.2f}s)",
            f"Tick Size (pu)     : {outcome.price_unit:.4f} USDT",
            f"Min-Profit TP Target: {outcome.min_profit_tp_price:.4f} USDT (Offset: +{tp_ticks} pu / +{tp_offset:.4f} USDT)",
            f"Stop Loss Level    : {outcome.stop_loss_price:.4f} USDT (Offset: -{sl_ticks} pu / -{sl_offset:.4f} USDT | -{sl_pct:.3f}% price | -{sl_roe:.1f}% ROE)",
            f"Exit Reason        : {outcome.exit_reason.value}",
            "------------------------------------------------------------------------------",
            f"REALIZED PnL       : {pnl_sign}{outcome.realized_pnl_usdt:.6f} USDT ({pnl_sign}INR {outcome.realized_pnl_inr:.4f})",
            f"Return on Equity   : {roe_sign}{outcome.roe_percentage:.2f}% (Price move: {pnl_sign}{outcome.pnl_percentage:.3f}%)",
            f"Trading Fees       : {outcome.fee_total_usdt:.6f} USDT (INR {outcome.fee_total_inr:.4f}) [Zero-Fee Pair]",
        ]

        if outcome.balance_after_trade_usdt is not None:
            card_lines.append(
                f"ACCOUNT BALANCE    : {outcome.balance_after_trade_usdt:.4f} USDT (INR {outcome.balance_after_trade_inr:.2f})"
            )

        card_lines.extend([
            "------------------------------------------------------------------------------",
            f"CUMULATIVE STATS   : Total Trades: {self.cumulative.total_trades} | Wins: {self.cumulative.winning_trades} | Losses: {self.cumulative.losing_trades} | Scratch: {self.cumulative.scratch_trades}",
            f"Win Rate           : {self.cumulative.win_rate_pct:.1f}%",
            f"Net Cumulative PnL : {'+' if self.cumulative.total_pnl_usdt >= 0 else ''}{self.cumulative.total_pnl_usdt:.6f} USDT ({'+' if self.cumulative.total_pnl_inr >= 0 else ''}INR {self.cumulative.total_pnl_inr:.4f})",
            f"Live USD/INR Rate  : INR {outcome.inr_rate:.2f} per USD",
            "=" * 78,
            ""
        ])

        card_text = "\n".join(card_lines)

        # Write to human-readable TXT file
        try:
            with open(self.txt_file, "a", encoding="utf-8") as f:
                f.write(card_text)
        except Exception as e:
            logging.getLogger("KCEXEngine").error("Failed to write to %s: %s", self.txt_file, e)

        # Write to JSONL file
        try:
            json_record = {
                "trade_id": outcome.trade_id,
                "close_time": outcome.close_time,
                "timestamp_str": timestamp_str,
                "symbol": outcome.symbol,
                "direction": outcome.direction.value,
                "sub_strategy": outcome.sub_strategy_name,
                "mode": outcome.mode.value,
                "vol_contracts": outcome.vol_contracts,
                "underlying_quantity": outcome.underlying_quantity,
                "entry_price": outcome.entry_price,
                "exit_price": outcome.exit_price,
                "min_profit_tp_price": outcome.min_profit_tp_price,
                "stop_loss_price": outcome.stop_loss_price,
                "price_unit": outcome.price_unit,
                "duration_seconds": outcome.duration_seconds,
                "notional_value_usdt": outcome.notional_value_usdt,
                "notional_value_inr": outcome.notional_value_inr,
                "margin_used_usdt": outcome.margin_used_usdt,
                "margin_used_inr": outcome.margin_used_inr,
                "realized_pnl_usdt": outcome.realized_pnl_usdt,
                "realized_pnl_inr": outcome.realized_pnl_inr,
                "roe_percentage": outcome.roe_percentage,
                "pnl_percentage": outcome.pnl_percentage,
                "fee_total_usdt": outcome.fee_total_usdt,
                "fee_total_inr": outcome.fee_total_inr,
                "exit_reason": outcome.exit_reason.value,
                "balance_after_trade_usdt": outcome.balance_after_trade_usdt,
                "balance_after_trade_inr": outcome.balance_after_trade_inr,
                "inr_rate": outcome.inr_rate,
                "order_id": outcome.order_id,
                "position_id": outcome.position_id,
                "cumulative_trades": self.cumulative.total_trades,
                "cumulative_win_rate": self.cumulative.win_rate_pct,
                "cumulative_net_pnl_usdt": self.cumulative.total_pnl_usdt,
                "cumulative_net_pnl_inr": self.cumulative.total_pnl_inr
            }
            with open(self.jsonl_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(json_record) + "\n")
        except Exception as e:
            logging.getLogger("KCEXEngine").error("Failed to write to %s: %s", self.jsonl_file, e)

        return card_text
