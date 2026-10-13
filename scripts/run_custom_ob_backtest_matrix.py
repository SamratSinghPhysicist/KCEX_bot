"""
Custom Backtest Execution & Simulation Engine for OB + Demand Strategy
======================================================================
Evaluates the Order Block + Demand strategy under custom specifications:
- Capital: $25,000 USDT
- Leverages: 1x, 2x
- Fee Schedule: 0.015% Maker / 0.045% Taker (0.09% round-trip taker market orders)
- Risk / Margin Allocations: 1%, 2%, 3%, 4%, 5%, 10%, 15%, 20%
- Slippage Ticks: 1, 2, 3, 4, 5, 6, 7 ticks
- Evaluates across all 9 assets and timeframes: 15m, 1h, 4h, 1d
"""

import os
import sys
import math
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple

# Reconfigure stdout for utf-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.market_sim import DEFAULT_CONTRACTS

SUITE1_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "reports", "backtests_of_OB_and_demand_zone_strategy")
OUTPUT_DIR = os.path.join(ROOT_DIR, "BACKTESTER", "reports", "custom_25k_1x_2x_sweep")

SYMBOLS = [
    "TRUMP_USDT",
    "DOGE_USDT",
    "ETH_USDT",
    "1000000MOG_USDT",
    "CL_USDT",
    "XAU_USDT",
    "BTC_USDT",
    "SOL_USDT",
    "XAG_USDT"
]

TIMEFRAMES = ["15m", "1h", "4h", "1d"]
LEVERAGES = [1, 2]
MAKER_FEE_PCT = 0.015
TAKER_FEE_PCT = 0.045
MAKER_FEE_RATE = MAKER_FEE_PCT / 100.0  # 0.00015
TAKER_FEE_RATE = TAKER_FEE_PCT / 100.0  # 0.00045
INITIAL_CAPITAL = 25000.0
RISK_PCTS = [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0]
SLIPPAGES = [1, 2, 3, 4, 5, 6, 7]


def simulate_trade_sequence(
    trades_df: pd.DataFrame,
    contract_info: Dict[str, Any],
    initial_capital: float,
    leverage: int,
    risk_pct: float,
    taker_fee_rate: float
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Executes sequential compound portfolio simulation for a specific trade sequence.
    """
    cs = float(contract_info.get("contract_size", 1.0))
    min_vol = float(contract_info.get("min_volume", 1.0))
    max_vol = float(contract_info.get("max_volume", 10000000.0))

    wallet_balance = initial_capital
    peak_equity = initial_capital
    max_drawdown_usdt = 0.0
    max_drawdown_pct = 0.0

    winning_trades = 0
    losing_trades = 0
    scratch_trades = 0
    gross_profits = 0.0
    gross_losses = 0.0
    total_fees = 0.0

    pnl_series = []
    trade_outcomes = []

    for idx, row in trades_df.iterrows():
        entry_price = float(row["entry_price"])
        exit_price = float(row["exit_price"])
        direction = str(row["direction"]).upper()
        exit_reason = str(row["exit_reason"])
        entry_time = str(row["entry_time_utc"])
        exit_time = str(row["exit_time_utc"])
        duration_s = float(row.get("duration_seconds", 0.0))

        # Position Sizing: margin_pct of current wallet equity
        avail_margin = max(0.0, wallet_balance)
        desired_margin = (risk_pct / 100.0) * avail_margin
        target_notional = desired_margin * leverage if leverage > 0 else desired_margin
        one_contract_notional = cs * entry_price

        if one_contract_notional > 0:
            raw_contracts = target_notional / one_contract_notional
            vol_contracts = max(min_vol, round(raw_contracts))
            vol_contracts = min(max_vol, vol_contracts)
        else:
            vol_contracts = min_vol

        # Affordability cap
        if one_contract_notional > 0 and leverage > 0 and wallet_balance > 0:
            req_margin = (vol_contracts * one_contract_notional) / leverage
            if req_margin > wallet_balance and vol_contracts > min_vol:
                max_afford = int((wallet_balance * leverage) / one_contract_notional)
                vol_contracts = max(min_vol, max_afford)

        underlying_qty = vol_contracts * cs
        notional_entry = underlying_qty * entry_price
        notional_exit = underlying_qty * exit_price
        actual_margin = notional_entry / leverage if leverage > 0 else notional_entry

        # Fee calculations: market orders on open and close
        fee_open = notional_entry * taker_fee_rate
        fee_close = notional_exit * taker_fee_rate
        fee_total = fee_open + fee_close

        # PnL Calculation
        if "LONG" in direction:
            gross_pnl = underlying_qty * (exit_price - entry_price)
        else:
            gross_pnl = underlying_qty * (entry_price - exit_price)

        net_pnl = gross_pnl - fee_total
        wallet_balance += net_pnl
        pnl_series.append(net_pnl)

        total_fees += fee_total
        if net_pnl > 0.0001:
            winning_trades += 1
            gross_profits += net_pnl
        elif net_pnl < -0.0001:
            losing_trades += 1
            gross_losses += abs(net_pnl)
        else:
            scratch_trades += 1

        # Track Drawdown
        if wallet_balance > peak_equity:
            peak_equity = wallet_balance
        dd_usdt = peak_equity - wallet_balance
        dd_pct = (dd_usdt / peak_equity * 100.0) if peak_equity > 0 else 0.0
        if dd_usdt > max_drawdown_usdt:
            max_drawdown_usdt = dd_usdt
        if dd_pct > max_drawdown_pct:
            max_drawdown_pct = dd_pct

        trade_outcomes.append({
            "trade_id": len(trade_outcomes) + 1,
            "direction": direction,
            "entry_time_utc": entry_time,
            "exit_time_utc": exit_time,
            "duration_seconds": duration_s,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "vol_contracts": vol_contracts,
            "underlying_quantity": round(underlying_qty, 6),
            "margin_used_usdt": round(actual_margin, 2),
            "notional_value_usdt": round(notional_entry, 2),
            "fee_open_usdt": round(fee_open, 4),
            "fee_close_usdt": round(fee_close, 4),
            "fee_total_usdt": round(fee_total, 4),
            "gross_pnl_usdt": round(gross_pnl, 4),
            "net_pnl_usdt": round(net_pnl, 4),
            "balance_after_trade_usdt": round(wallet_balance, 2),
            "exit_reason": exit_reason
        })

    total_trades = len(pnl_series)
    net_pnl_total = wallet_balance - initial_capital
    net_roi_pct = (net_pnl_total / initial_capital) * 100.0

    win_rate_pct = (winning_trades / total_trades * 100.0) if total_trades > 0 else 0.0
    profit_factor = (gross_profits / gross_losses) if gross_losses > 0 else (999.0 if gross_profits > 0 else 0.0)
    profit_factor = min(999.0, round(profit_factor, 2))

    expectancy_usdt = (net_pnl_total / total_trades) if total_trades > 0 else 0.0
    avg_win = (gross_profits / winning_trades) if winning_trades > 0 else 0.0
    avg_loss = (gross_losses / losing_trades) if losing_trades > 0 else 0.0
    win_loss_payoff = (avg_win / avg_loss) if avg_loss > 0 else (999.0 if avg_win > 0 else 0.0)

    # Sharpe & Calmar
    if len(pnl_series) > 1 and np.std(pnl_series) > 0:
        sharpe = (np.mean(pnl_series) / np.std(pnl_series)) * np.sqrt(total_trades)
    else:
        sharpe = 0.0
    calmar = (net_roi_pct / max_drawdown_pct) if max_drawdown_pct > 0 else 0.0

    summary_metrics = {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "scratch_trades": scratch_trades,
        "win_rate_pct": round(win_rate_pct, 2),
        "profit_factor": profit_factor,
        "initial_capital_usdt": initial_capital,
        "final_balance_usdt": round(wallet_balance, 2),
        "net_pnl_usdt": round(net_pnl_total, 2),
        "net_roi_pct": round(net_roi_pct, 2),
        "total_fees_usdt": round(total_fees, 2),
        "max_drawdown_usdt": round(max_drawdown_usdt, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "expectancy_usdt": round(expectancy_usdt, 4),
        "avg_win_usdt": round(avg_win, 2),
        "avg_loss_usdt": round(avg_loss, 2),
        "win_loss_payoff": round(win_loss_payoff, 2),
        "sharpe_ratio": round(sharpe, 2),
        "calmar_ratio": round(calmar, 2)
    }

    return summary_metrics, trade_outcomes


def run_full_matrix():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    trades_dir = os.path.join(OUTPUT_DIR, "trades_csv")
    os.makedirs(trades_dir, exist_ok=True)

    master_matrix_rows = []
    print(f"🚀 INITIATING CUSTOM BACKTEST MATRIX SWEEP")
    print(f"   Initial Capital: ${INITIAL_CAPITAL:,.2f} USDT")
    print(f"   Leverages:       {LEVERAGES}")
    print(f"   Fees:            Maker {MAKER_FEE_PCT}% / Taker {TAKER_FEE_PCT}% (Round-trip Taker = 0.09%)")
    print(f"   Risk % List:     {RISK_PCTS}")
    print(f"   Slippages:       {SLIPPAGES} ticks")
    print(f"   Assets:          {SYMBOLS}")
    print(f"   Timeframes:      {TIMEFRAMES}")
    print("=" * 90)

    total_runs = 0
    t0 = pd.Timestamp.now()

    for sym in SYMBOLS:
        source_csv = os.path.join(SUITE1_DIR, f"{sym}_all_trades.csv")
        if not os.path.exists(source_csv):
            print(f"⚠️  Missing source trade file: {source_csv}")
            continue

        full_df = pd.read_csv(source_csv)
        contract = DEFAULT_CONTRACTS.get(sym, {
            "contract_size": 1.0,
            "min_volume": 1.0,
            "max_volume": 10000000.0,
            "price_unit": 0.001,
            "price_precision": 3
        })

        for tf in TIMEFRAMES:
            for slip in SLIPPAGES:
                # Extract sequence of trades for this asset, tf, and slip
                # Using taker_fee_pct==0.05 baseline sequence (as it was run with closest fee structure)
                sub_trades = full_df[(full_df["timeframe"] == tf) &
                                     (full_df["slippage_ticks"] == slip) &
                                     (full_df["taker_fee_pct"] == 0.05)].sort_values(by="trade_id").reset_index(drop=True)

                if len(sub_trades) == 0:
                    # Fallback to any fee tier for this tf and slip if 0.05 not present
                    sub_trades = full_df[(full_df["timeframe"] == tf) &
                                         (full_df["slippage_ticks"] == slip)].drop_duplicates(subset=["trade_id"]).sort_values(by="trade_id").reset_index(drop=True)

                if len(sub_trades) == 0:
                    continue

                for lev in LEVERAGES:
                    for risk in RISK_PCTS:
                        metrics, trade_logs = simulate_trade_sequence(
                            trades_df=sub_trades,
                            contract_info=contract,
                            initial_capital=INITIAL_CAPITAL,
                            leverage=lev,
                            risk_pct=risk,
                            taker_fee_rate=TAKER_FEE_RATE
                        )

                        row = {
                            "symbol": sym,
                            "timeframe": tf,
                            "leverage": lev,
                            "risk_pct": risk,
                            "slippage_ticks": slip,
                            "maker_fee_pct": MAKER_FEE_PCT,
                            "taker_fee_pct": TAKER_FEE_PCT,
                            "round_trip_fee_pct": TAKER_FEE_PCT * 2,
                            **metrics
                        }
                        master_matrix_rows.append(row)
                        total_runs += 1

                        # Save trade log if this is champion configuration (e.g. 1t slippage)
                        if slip == 1:
                            trade_log_fn = f"{sym}_{tf}_{lev}x_risk{int(risk)}pct_slip1t_trades.csv"
                            pd.DataFrame(trade_logs).to_csv(os.path.join(trades_dir, trade_log_fn), index=False)

    df_master = pd.DataFrame(master_matrix_rows)
    master_csv_path = os.path.join(OUTPUT_DIR, "custom_master_matrix.csv")
    df_master.to_csv(master_csv_path, index=False)
    print(f"\n[+] Executed {total_runs} backtest configurations successfully in {(pd.Timestamp.now()-t0).total_seconds():.2f}s!")
    print(f"[+] Master Matrix saved to: {master_csv_path}")

    # Generate Champion Matrix
    idx_champ = df_master.groupby(["symbol", "timeframe"])["net_roi_pct"].idxmax()
    df_champ = df_master.loc[idx_champ].sort_values(by="net_roi_pct", ascending=False).reset_index(drop=True)
    champ_csv_path = os.path.join(OUTPUT_DIR, "champion_configurations_matrix.csv")
    df_champ.to_csv(champ_csv_path, index=False)
    print(f"[+] Champion Configurations saved to: {champ_csv_path}")

    return df_master, df_champ


if __name__ == "__main__":
    run_full_matrix()
