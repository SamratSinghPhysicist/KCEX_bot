import os
import sys
import time
import json
from pathlib import Path
import pandas as pd

# Set working dir to ResearchV2
research_dir = Path(r"d:\My_Bots\Trading\(COPY-SandBoxed) KCEX\ResearchV2")
sys.path.insert(0, str(research_dir))

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator

def run_experiment(
    exp_id: str,
    symbol: str,
    strategy: str,
    start_date: str,
    end_date: str,
    tp_ticks: int,
    sl_mode: str,
    sl_ticks: int = 2,
    sl_roe: float = 25.0,
    invert_signal: bool = False,
    leverage: int = 75,
    stoch_preset: str = "FAST_SCALP",
    ema_preset: str = "5/13",
    smart_atr_filter: bool = True,
    smart_min_atr_ticks: float = 2.5
) -> dict:
    t0 = time.time()
    config = BacktestConfig(
        symbol=symbol,
        timeframe="1m",
        strategy_mode=strategy,
        ema_preset=ema_preset,
        stoch_preset=stoch_preset,
        start_time=start_date,
        end_time=end_date,
        tp_ticks=tp_ticks,
        sl_mode=sl_mode,
        sl_ticks=sl_ticks if sl_mode == "TICKS" else None,
        sl_roe_pct=sl_roe,
        leverage=leverage,
        initial_balance_usdt=100.0,
        use_tick_data=False, # Use fast candle high/low across full 8 months
        fee_mode="ZERO",
        maker_fee_override=0.0,
        taker_fee_override=0.0,
        invert_signal=invert_signal,
        smart_atr_filter_enabled=smart_atr_filter,
        smart_min_atr_ticks=smart_min_atr_ticks
    )
    
    engine = BacktestExecutionEngine(config=config)
    outcomes = engine.run()
    elapsed = time.time() - t0
    
    summary = PerformanceCalculator.calculate(
        outcomes=outcomes,
        initial_balance_usdt=100.0,
        inr_rate=94.45
    )
    
    res = {
        "exp_id": exp_id,
        "symbol": symbol,
        "strategy": strategy,
        "invert": invert_signal,
        "date_range": f"{start_date} to {end_date}",
        "tp_ticks": tp_ticks,
        "sl_mode": sl_mode,
        "sl_val": f"{sl_ticks}t" if sl_mode == "TICKS" else f"{sl_roe}% ROE",
        "trades": summary.total_trades,
        "wins": summary.winning_trades,
        "losses": summary.losing_trades,
        "win_rate": round(summary.win_rate_pct, 2),
        "profit_factor": round(summary.profit_factor, 2),
        "net_pnl": round(summary.net_pnl_usdt, 4),
        "max_dd": round(summary.max_drawdown_usdt, 4),
        "max_dd_pct": round(summary.max_drawdown_pct, 2),
        "sharpe": round(summary.sharpe_ratio, 2),
        "sortino": round(summary.sortino_ratio, 2),
        "calmar": round(summary.calmar_ratio, 2),
        "elapsed_sec": round(elapsed, 2)
    }
    print(f"[{exp_id}] {symbol} | {strategy} | Inv: {invert_signal} | TP:{tp_ticks}t SL:{res['sl_val']} | Trades: {res['trades']} | WR: {res['win_rate']}% | PF: {res['profit_factor']} | PnL: {res['net_pnl']:+,.4f} USDT | DD: -{res['max_dd']:.4f} | Time: {res['elapsed_sec']}s")
    return res

if __name__ == "__main__":
    results = []
    
    # 1. Full 8-Month DOGE Sweep (2026-01-01 to 2026-08-31)
    print("================================================================================")
    print("                  PHASE 2.1: DOGE_USDT 8-MONTH SYSTEMATIC SWEEP")
    print("================================================================================")
    
    # E0: Baseline (TP 2t, SL 25% ROE)
    results.append(run_experiment("DOGE_E0_Base", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "ROE", sl_roe=25.0, invert_signal=False))
    
    # E1: Pure Inverted Baseline (Invert=True, TP 2t, SL 25% ROE)
    results.append(run_experiment("DOGE_E1_InvBase", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "ROE", sl_roe=25.0, invert_signal=True))
    
    # E2: Direct Symmetric 1:1 (TP 2t, SL 2t)
    results.append(run_experiment("DOGE_E2_Sym1to1", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=False))
    
    # E3: Inverted Symmetric 1:1 (Invert=True, TP 2t, SL 2t)
    results.append(run_experiment("DOGE_E3_InvSym1to1", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=True))
    
    # E4: Direct 5:1 Payoff (TP 10t, SL 2t)
    results.append(run_experiment("DOGE_E4_Direct10t2t", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 10, "TICKS", sl_ticks=2, invert_signal=False))
    
    # E5: Inverted 5:1 Payoff (Invert=True, TP 10t, SL 2t - User Hypothesis 1B)
    results.append(run_experiment("DOGE_E5_Inv10t2t", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 10, "TICKS", sl_ticks=2, invert_signal=True))
    
    # E6: Inverted 2.5:1 Payoff (Invert=True, TP 5t, SL 2t)
    results.append(run_experiment("DOGE_E6_Inv5t2t", "DOGE_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 5, "TICKS", sl_ticks=2, invert_signal=True))

    # E7: Smart Strategy on DOGE (Direct, TP 2t, SL 2t)
    results.append(run_experiment("DOGE_E7_SmartSym", "DOGE_USDT", "SMART_STRATEGY", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=False))

    # E8: Smart Strategy on DOGE (Inverted, TP 2t, SL 2t)
    results.append(run_experiment("DOGE_E8_SmartInvSym", "DOGE_USDT", "SMART_STRATEGY", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=True))

    print("\n================================================================================")
    print("                  PHASE 2.2: TRUMP_USDT 8-MONTH SYSTEMATIC SWEEP")
    print("================================================================================")
    
    # T0: Baseline (TP 2t, SL 25% ROE)
    results.append(run_experiment("TRUMP_T0_Base", "TRUMP_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "ROE", sl_roe=25.0, invert_signal=False))
    
    # T1: Inverted Baseline (Invert=True, TP 2t, SL 25% ROE)
    results.append(run_experiment("TRUMP_T1_InvBase", "TRUMP_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "ROE", sl_roe=25.0, invert_signal=True))

    # T2: Direct Symmetric 1:1 (TP 2t, SL 2t)
    results.append(run_experiment("TRUMP_T2_Sym1to1", "TRUMP_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=False))

    # T3: Inverted Symmetric 1:1 (Invert=True, TP 2t, SL 2t)
    results.append(run_experiment("TRUMP_T3_InvSym1to1", "TRUMP_USDT", "STOCH_RSI", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=True))

    # T4: Smart Strategy on TRUMP (Direct, TP 2t, SL 2t)
    results.append(run_experiment("TRUMP_T4_SmartSym", "TRUMP_USDT", "SMART_STRATEGY", "2026-01-01", "2026-08-31", 2, "TICKS", sl_ticks=2, invert_signal=False))

    # Save results to json
    out_file = Path(r"C:\Users\Samrat Singh\.gemini\antigravity\brain\a8f292b9-9fdf-473b-bbc4-a8f2b9814c29\scratch\sweep_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    df = pd.DataFrame(results)
    print("\n================================================================================")
    print("                    FINAL CROSS-EXPERIMENT LEADERBOARD")
    print("================================================================================")
    pd.set_option('display.max_columns', 15)
    pd.set_option('display.width', 1000)
    print(df[["exp_id", "symbol", "strategy", "invert", "tp_ticks", "sl_val", "trades", "win_rate", "profit_factor", "net_pnl", "max_dd_pct", "sharpe"]].to_string(index=False))
