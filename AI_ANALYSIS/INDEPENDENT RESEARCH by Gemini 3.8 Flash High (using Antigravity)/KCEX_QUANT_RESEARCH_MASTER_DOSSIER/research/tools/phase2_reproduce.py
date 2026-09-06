import os
import sys
import json
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from research.tools.experiment_suite import run_backtest_direct

def test_reproduce():
    print("=== REPRODUCING CLAIM: July 1 to July 24, 2026 ===")
    
    # 1. Baseline: SL = 25% ROE
    t0 = time.time()
    m_base, o_base = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        stoch_preset="FAST_SCALP",
        start_time="2026-07-01",
        end_time="2026-07-24",
        tp_ticks=2,
        sl_mode="ROE",
        sl_roe_pct=25.0,
        sl_ticks=None,
        use_tick_data=True
    )
    t_base = time.time() - t0
    
    print("\n--- BASELINE (SL = 25% ROE) ---")
    print(f"Total Trades:      {m_base['total_trades']}")
    print(f"Win Rate:          {m_base['win_rate_pct']:.4f}%")
    print(f"Profit Factor:     {m_base['profit_factor']:.4f}")
    print(f"Net PnL (USDT):    {m_base['net_pnl_usdt']:.6f}")
    print(f"Max Drawdown:      {m_base['max_drawdown_pct']:.4f}%")
    print(f"Avg Win (USDT):    {m_base['avg_win_pnl_usdt']:.6f}")
    print(f"Avg Loss (USDT):   {m_base['avg_loss_pnl_usdt']:.6f}")
    print(f"Avg Duration (s):  {m_base['avg_duration_seconds']:.2f}s")
    print(f"Long Trades:       {m_base['long_trades']}, Wins: {m_base['long_wins']} ({m_base['long_win_rate_pct']:.2f}%)")
    print(f"Short Trades:      {m_base['short_trades']}, Wins: {m_base['short_wins']} ({m_base['short_win_rate_pct']:.2f}%)")
    print(f"Sim Time:          {t_base:.2f}s")

    # 2. Candidate: SL = 5 ticks
    t0 = time.time()
    m_cand, o_cand = run_backtest_direct(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        stoch_preset="FAST_SCALP",
        start_time="2026-07-01",
        end_time="2026-07-24",
        tp_ticks=2,
        sl_mode="TICKS",
        sl_ticks=5,
        use_tick_data=True
    )
    t_cand = time.time() - t0
    
    print("\n--- CANDIDATE (SL = 5 TICKS) ---")
    print(f"Total Trades:      {m_cand['total_trades']}")
    print(f"Win Rate:          {m_cand['win_rate_pct']:.4f}%")
    print(f"Profit Factor:     {m_cand['profit_factor']:.4f}")
    print(f"Net PnL (USDT):    {m_cand['net_pnl_usdt']:.6f}")
    print(f"Max Drawdown:      {m_cand['max_drawdown_pct']:.4f}%")
    print(f"Avg Win (USDT):    {m_cand['avg_win_pnl_usdt']:.6f}")
    print(f"Avg Loss (USDT):   {m_cand['avg_loss_pnl_usdt']:.6f}")
    print(f"Avg Duration (s):  {m_cand['avg_duration_seconds']:.2f}s")
    print(f"Long Trades:       {m_cand['long_trades']}, Wins: {m_cand['long_wins']} ({m_cand['long_win_rate_pct']:.2f}%)")
    print(f"Short Trades:      {m_cand['short_trades']}, Wins: {m_cand['short_wins']} ({m_cand['short_win_rate_pct']:.2f}%)")
    print(f"Sim Time:          {t_cand:.2f}s")

if __name__ == "__main__":
    test_reproduce()
