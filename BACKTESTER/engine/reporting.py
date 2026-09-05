"""
Backtest Reporting & Outcome Exporters
======================================
Produces colorized terminal summary cards, dual-currency trade tables,
ASCII equity charts, and exports full trade outcomes to CSV, JSONL, and Markdown.
"""

import os
import csv
import json
import datetime
from typing import List, Dict, Any, Optional

from kcex.engine.models import TradeOutcome
from BACKTESTER.engine.metrics import PerformanceSummary
from BACKTESTER.engine.scanner import format_ms_to_utc


class BacktestReporter:
    """
    Renders formatted terminal cards and exports trade history reports.
    """

    def __init__(self, reports_dir: str = os.path.join("BACKTESTER", "reports")):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def print_summary(self, summary: PerformanceSummary) -> None:
        """Prints an executive summary card of backtest performance."""
        sep = "=" * 80
        sub_sep = "-" * 80

        print("\n" + sep)
        print(f"        BACKTEST PERFORMANCE REPORT - {summary.symbol}")
        print(sep)

        # Overview
        pnl_sign = "+" if summary.net_pnl_usdt >= 0 else ""
        roi_sign = "+" if summary.net_roi_pct >= 0 else ""
        print(f"Total Trades:           {summary.total_trades:<6} | Win Rate:             {summary.win_rate_pct:.2f}%")
        print(f"Wins / Losses / Scratch: {summary.winning_trades} / {summary.losing_trades} / {summary.scratch_trades}")
        print(sub_sep)

        # Financials
        print(f"Initial Capital:        {summary.initial_balance_usdt:>12.4f} USDT  (INR {summary.initial_balance_inr:>10.2f})")
        print(f"Final Balance:          {summary.final_balance_usdt:>12.4f} USDT  (INR {summary.final_balance_inr:>10.2f})")
        print(f"Net Realized PnL:       {pnl_sign}{summary.net_pnl_usdt:>11.4f} USDT  ({roi_sign}{summary.net_roi_pct:.2f}%)")
        print(f"Net Realized PnL (INR): {pnl_sign}{summary.net_pnl_inr:>11.2f} INR")
        print(f"Total Taker Fees Paid:  {summary.total_fees_usdt:>12.4f} USDT  (INR {summary.total_fees_inr:>10.2f})")
        print(f"Profit Factor:          {summary.profit_factor:>12.2f}  | Win/Loss Payoff:      {summary.win_loss_ratio:>6.2f}")
        print(sub_sep)

        # Risk & Drawdown
        print(f"Max Drawdown:           {summary.max_drawdown_usdt:>12.4f} USDT  (-{summary.max_drawdown_pct:.2f}%)")
        print(f"Sharpe Ratio (est):     {summary.sharpe_ratio:>12.2f}  | Sortino Ratio:        {summary.sortino_ratio:>6.2f}")
        print(f"Calmar Ratio:           {summary.calmar_ratio:>12.2f}")
        print(sub_sep)

        # Execution Stats
        print(f"Avg Trade PnL:          {pnl_sign}{summary.avg_trade_pnl_usdt:>11.4f} USDT  | Avg Duration:         {summary.avg_duration_seconds:.1f}s")
        print(f"Avg Winning Trade:      +{summary.avg_win_pnl_usdt:>11.4f} USDT  | Avg Losing Trade:     -{summary.avg_loss_pnl_usdt:>6.4f} USDT")
        print(f"Max Consecutive Wins:   {summary.max_consecutive_wins:<6}       | Max Consecutive Losses: {summary.max_consecutive_losses}")
        print(f"Long Trades:            {summary.long_trades:<6} (Win: {summary.long_win_rate_pct:.1f}%) | Short Trades:         {summary.short_trades:<6} (Win: {summary.short_win_rate_pct:.1f}%)")
        print(sub_sep)

        # Exit Reasons Breakdown
        print("Exit Triggers Breakdown:")
        for r_name, count in summary.exit_reasons.items():
            pct = (count / summary.total_trades * 100.0) if summary.total_trades > 0 else 0.0
            print(f"  +-- {r_name:<26}: {count:>4} trades ({pct:>5.1f}%)")
        print(sep + "\n")

    def print_trades_table(self, outcomes: List[TradeOutcome], limit: int = 15) -> None:
        """Prints a tabular log of the recent trades."""
        if not outcomes:
            return

        print(f"--- RECENT TRADES (Showing {min(len(outcomes), limit)} of {len(outcomes)}) ---")
        header = f"{'#':<4} | {'Dir':<5} | {'Entry Price':<11} | {'Exit Price':<11} | {'PnL (USDT)':<12} | {'ROE %':<8} | {'Exit Reason':<22} | {'Duration':<8}"
        print(header)
        print("-" * len(header))

        # Show first few or last few
        display_items = outcomes[-limit:] if len(outcomes) > limit else outcomes
        for o in display_items:
            pnl_str = f"{'+' if o.realized_pnl_usdt >= 0 else ''}{o.realized_pnl_usdt:.4f}"
            roe_str = f"{'+' if o.roe_percentage >= 0 else ''}{o.roe_percentage:.1f}%"
            reason_str = o.exit_reason.value if hasattr(o.exit_reason, "value") else str(o.exit_reason)
            dur_str = f"{o.duration_seconds:.1f}s"
            print(f"{o.trade_id:<4} | {o.direction.value:<5} | {o.entry_price:<11.4f} | {o.exit_price:<11.4f} | {pnl_str:<12} | {roe_str:<8} | {reason_str:<22} | {dur_str:<8}")
        print("-" * len(header) + "\n")

    def export_all(self, outcomes: List[TradeOutcome], summary: PerformanceSummary, prefix: str = "backtest") -> Dict[str, str]:
        """
        Exports full trade journals to CSV, JSONL, and summary Markdown.
        """
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = f"{prefix}_{summary.symbol}_{now_str}"

        csv_path = os.path.join(self.reports_dir, f"{run_name}_trades.csv")
        jsonl_path = os.path.join(self.reports_dir, f"{run_name}_trades.jsonl")
        md_path = os.path.join(self.reports_dir, f"{run_name}_summary.md")

        # 1. Export CSV
        if outcomes:
            keys = [
                "trade_id", "symbol", "direction", "sub_strategy_name", "vol_contracts",
                "underlying_quantity", "entry_price", "exit_price", "min_profit_tp_price",
                "stop_loss_price", "open_time", "close_time", "duration_seconds",
                "notional_value_usdt", "margin_used_usdt", "fee_total_usdt",
                "realized_pnl_usdt", "realized_pnl_inr", "roe_percentage", "exit_reason",
                "balance_after_trade_usdt"
            ]
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(keys)
                for o in outcomes:
                    row = [
                        o.trade_id,
                        o.symbol,
                        o.direction.value if hasattr(o.direction, "value") else str(o.direction),
                        o.sub_strategy_name,
                        o.vol_contracts,
                        o.underlying_quantity,
                        o.entry_price,
                        o.exit_price,
                        o.min_profit_tp_price,
                        o.stop_loss_price,
                        format_ms_to_utc(int(o.open_time * 1000)),
                        format_ms_to_utc(int(o.close_time * 1000)),
                        round(o.duration_seconds, 2),
                        round(o.notional_value_usdt, 4),
                        round(o.margin_used_usdt, 4),
                        round(o.fee_total_usdt, 6),
                        round(o.realized_pnl_usdt, 6),
                        round(o.realized_pnl_inr, 2),
                        round(o.roe_percentage, 2),
                        o.exit_reason.value if hasattr(o.exit_reason, "value") else str(o.exit_reason),
                        round(o.balance_after_trade_usdt or 0.0, 4)
                    ]
                    writer.writerow(row)

        # 2. Export JSONL
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for o in outcomes:
                d = {
                    "trade_id": o.trade_id,
                    "symbol": o.symbol,
                    "direction": o.direction.value if hasattr(o.direction, "value") else str(o.direction),
                    "sub_strategy_name": o.sub_strategy_name,
                    "entry_price": o.entry_price,
                    "exit_price": o.exit_price,
                    "min_profit_tp_price": o.min_profit_tp_price,
                    "stop_loss_price": o.stop_loss_price,
                    "open_time_utc": format_ms_to_utc(int(o.open_time * 1000)),
                    "close_time_utc": format_ms_to_utc(int(o.close_time * 1000)),
                    "duration_seconds": o.duration_seconds,
                    "realized_pnl_usdt": o.realized_pnl_usdt,
                    "realized_pnl_inr": o.realized_pnl_inr,
                    "roe_percentage": o.roe_percentage,
                    "exit_reason": o.exit_reason.value if hasattr(o.exit_reason, "value") else str(o.exit_reason),
                    "balance_after_trade_usdt": o.balance_after_trade_usdt
                }
                f.write(json.dumps(d) + "\n")

        # 3. Export Markdown Summary
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Backtest Performance Report: {summary.symbol}\n\n")
            f.write(f"Generated on: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"- **Total Trades**: {summary.total_trades}\n")
            f.write(f"- **Win Rate**: {summary.win_rate_pct:.2f}%\n")
            f.write(f"- **Initial Capital**: {summary.initial_balance_usdt:.2f} USDT (INR {summary.initial_balance_inr:.2f})\n")
            f.write(f"- **Final Balance**: {summary.final_balance_usdt:.2f} USDT (INR {summary.final_balance_inr:.2f})\n")
            f.write(f"- **Net Profit**: {summary.net_pnl_usdt:+.4f} USDT ({summary.net_roi_pct:+.2f}%)\n")
            f.write(f"- **Profit Factor**: {summary.profit_factor:.2f}\n")
            f.write(f"- **Max Drawdown**: {summary.max_drawdown_usdt:.4f} USDT ({summary.max_drawdown_pct:.2f}%)\n")
            f.write(f"- **Sharpe Ratio**: {summary.sharpe_ratio:.2f}\n\n")
            f.write("## Exit Breakdown\n\n")
            f.write("| Exit Reason | Count | Percentage |\n")
            f.write("| :--- | :--- | :--- |\n")
            for r_name, count in summary.exit_reasons.items():
                pct = (count / summary.total_trades * 100.0) if summary.total_trades > 0 else 0.0
                f.write(f"| {r_name} | {count} | {pct:.1f}% |\n")

        print(f"[+] Reports generated successfully in '{self.reports_dir}':")
        print(f"    - CSV:  {csv_path}")
        print(f"    - JSON: {jsonl_path}")
        print(f"    - MD:   {md_path}\n")

        return {
            "csv": csv_path,
            "jsonl": jsonl_path,
            "markdown": md_path
        }
