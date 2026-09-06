import os
import sys
import csv
import time
from typing import List, Dict, Any

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol, parse_timestamp_ms, format_ms_to_utc
from BACKTESTER.engine.data_loader import OHLCVLoader, TickTradeStreamer, normalize_timeframe
from BACKTESTER.engine.market_sim import BacktestMarket
from BACKTESTER.engine.execution_sim import VirtualClock
from kcex.engine.models import OrderDirection, EngineMode
from strategies.filters import FilterPipeline

OUT_CSV = os.path.join(ROOT_DIR, "research_agent_phase2", "07_COUNTERFACTUAL_MATRIX.csv")

def run_counterfactual_matrix():
    print("=== BUILDING PER-TRADE COUNTERFACTUAL MATRIX (July 1 - July 24, 2026) ===")
    
    cfg = BacktestConfig(
        symbol="TRUMP_USDT",
        timeframe="1m",
        strategy_mode="STOCH_RSI",
        stoch_preset="FAST_SCALP",
        start_time="2026-07-01",
        end_time="2026-07-24",
        tp_ticks=2,
        sl_mode="TICKS",
        sl_ticks=5,
        use_tick_data=True,
        fee_mode="ZERO"
    )
    
    market = BacktestMarket(fee_mode="ZERO")
    contract = market.get_contract_detail(cfg.symbol)
    pu = contract.price_unit
    ps = contract.price_precision
    
    ohlcv_loader = OHLCVLoader(data_dir=cfg.ohlcv_data_dir)
    tick_streamer = TickTradeStreamer(data_dir=cfg.trades_data_dir)
    
    start_ms = parse_timestamp_ms(cfg.start_time)
    end_ms = parse_timestamp_ms(cfg.end_time)
    candles = ohlcv_loader.load_candles(cfg.symbol, "1m", start_ms, end_ms)
    
    from kcex.engine.strategy import MasterplanStrategy
    strategy = MasterplanStrategy(config=cfg, market=market)
    filter_pipeline = FilterPipeline.from_config(cfg)
    
    # We collect all valid strategy entry signals
    # To ensure identical signal sequence to live engine without path divergence from trade length,
    # we can simulate the signals when strategy is ready.
    clock = VirtualClock(initial_time_sec=candles[0].close_time_ms / 1000.0)
    market.set_candles(cfg.symbol, "1m", candles)
    
    STOPS = [2, 3, 4, 5, 6, 7, 10]
    
    fields = [
        "signal_id", "timestamp_utc", "direction", "entry_price",
        "MFE_ticks", "MAE_ticks",
        "outcome_sl2", "outcome_sl3", "outcome_sl4", "outcome_sl5",
        "outcome_sl6", "outcome_sl7", "outcome_sl10",
        "classification", "time_to_tp_sec", "time_to_sl5_sec"
    ]
    
    matrix_rows = []
    
    class_counts = {
        "WIN_ALL": 0,
        "LOSS_ALL": 0,
        "SAVED_BY_SL5": 0,       # Lose at SL=2, Win at SL=5
        "EXTRA_DAMAGE_SL5": 0,   # Lose at SL=2 and Lose at SL=5 (cost -5 vs -2)
        "SAVED_BY_SL10": 0,      # Lose at SL=5, Win at SL=10
        "OTHER": 0
    }
    
    with clock:
        candle_idx = 0
        total_candles = len(candles)
        signal_counter = 0
        
        while candle_idx < total_candles:
            c = candles[candle_idx]
            clock.set_time_sec(c.close_time_ms / 1000.0)
            market.set_time(c.close_time_ms, current_price=c.close)
            
            strategy.sub_strategy.trade_in_progress = False
            signal = strategy.get_signal()
            if signal:
                signal_counter += 1
                entry_price = c.close
                direction = signal.direction
                open_ms = c.close_time_ms
                
                # Stream forward ticks to evaluate counterfactuals
                # Look up to 3600 seconds forward
                tick_gen = tick_streamer.stream_ticks(cfg.symbol, start_ms=open_ms, end_ms=open_ms + 3600000)
                
                max_fav_ticks = 0.0
                max_adv_ticks = 0.0
                time_to_tp = None
                time_to_sl5 = None
                
                # Tracking which stops have been hit: {sl: ('WIN'/'LOSS', exit_time)}
                stop_outcomes = {}
                
                for tick in tick_gen:
                    t_sec = (tick.timestamp_ms - open_ms) / 1000.0
                    p = tick.price
                    
                    if direction == OrderDirection.LONG:
                        fav = (p - entry_price) / pu
                        adv = (entry_price - p) / pu
                    else:
                        fav = (entry_price - p) / pu
                        adv = (p - entry_price) / pu
                        
                    if fav > max_fav_ticks:
                        max_fav_ticks = fav
                    if adv > max_adv_ticks:
                        max_adv_ticks = adv
                        
                    # Evaluate for each stop
                    for sl in STOPS:
                        if sl in stop_outcomes:
                            continue
                        if fav >= 2.0:
                            stop_outcomes[sl] = ("WIN", t_sec)
                            if time_to_tp is None:
                                time_to_tp = t_sec
                        elif adv >= float(sl):
                            stop_outcomes[sl] = ("LOSS", t_sec)
                            if sl == 5 and time_to_sl5 is None:
                                time_to_sl5 = t_sec
                                
                    if len(stop_outcomes) == len(STOPS):
                        break
                        
                # Fill any unresolved with current state
                for sl in STOPS:
                    if sl not in stop_outcomes:
                        # If reached 2 ticks fav before sl, it's a win
                        if max_fav_ticks >= 2.0 and max_adv_ticks < float(sl):
                            stop_outcomes[sl] = ("WIN", 3600.0)
                        else:
                            stop_outcomes[sl] = ("LOSS", 3600.0)
                            
                sl2_win = (stop_outcomes[2][0] == "WIN")
                sl5_win = (stop_outcomes[5][0] == "WIN")
                sl10_win = (stop_outcomes[10][0] == "WIN")
                
                if sl2_win and sl5_win and sl10_win:
                    classification = "WIN_ALL"
                    class_counts["WIN_ALL"] += 1
                elif not sl2_win and not sl5_win and not sl10_win:
                    classification = "LOSS_ALL"
                    class_counts["LOSS_ALL"] += 1
                elif not sl2_win and sl5_win:
                    classification = "SAVED_BY_SL5"
                    class_counts["SAVED_BY_SL5"] += 1
                elif not sl2_win and not sl5_win and sl10_win:
                    classification = "SAVED_BY_SL10"
                    class_counts["SAVED_BY_SL10"] += 1
                else:
                    classification = "OTHER"
                    class_counts["OTHER"] += 1
                    
                if not sl2_win and not sl5_win:
                    class_counts["EXTRA_DAMAGE_SL5"] += 1
                    
                row = {
                    "signal_id": signal_counter,
                    "timestamp_utc": format_ms_to_utc(open_ms),
                    "direction": direction.value if hasattr(direction, "value") else str(direction),
                    "entry_price": f"{entry_price:.4f}",
                    "MFE_ticks": f"{max_fav_ticks:.1f}",
                    "MAE_ticks": f"{max_adv_ticks:.1f}",
                    "outcome_sl2": stop_outcomes[2][0],
                    "outcome_sl3": stop_outcomes[3][0],
                    "outcome_sl4": stop_outcomes[4][0],
                    "outcome_sl5": stop_outcomes[5][0],
                    "outcome_sl6": stop_outcomes[6][0],
                    "outcome_sl7": stop_outcomes[7][0],
                    "outcome_sl10": stop_outcomes[10][0],
                    "classification": classification,
                    "time_to_tp_sec": f"{time_to_tp:.1f}" if time_to_tp else "N/A",
                    "time_to_sl5_sec": f"{time_to_sl5:.1f}" if time_to_sl5 else "N/A"
                }
                matrix_rows.append(row)
                
                if signal_counter % 500 == 0:
                    print(f"Processed {signal_counter} signals... Current breakdown: {class_counts}")
                    
            candle_idx += 1
            
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(matrix_rows)
        
    print("\n=== FINAL COUNTERFACTUAL MATRIX BREAKDOWN ===")
    print(f"Total Signals Evaluated: {len(matrix_rows)}")
    for k, v in class_counts.items():
        pct = (v / len(matrix_rows)) * 100.0 if matrix_rows else 0.0
        print(f"  {k:<20}: {v:5d} ({pct:5.2f}%)")
        
    # Economics calculation:
    # Win = +2 ticks (+0.0004 USDT)
    # Loss at SL=2 = -2 ticks (-0.0004 USDT)
    # Loss at SL=5 = -5 ticks (-0.0010 USDT)
    # Extra gain from saved trades: saved * (+2 - (-2)) = saved * 4 ticks (+0.0008 USDT per saved trade)
    # Extra loss from damaged trades: damaged * (-5 - (-2)) = damaged * (-3 ticks) (-0.0006 USDT per damaged trade)
    saved = class_counts["SAVED_BY_SL5"]
    damaged = class_counts["EXTRA_DAMAGE_SL5"]
    net_ticks_diff = (saved * 4) - (damaged * 3)
    net_usdt_diff = net_ticks_diff * 0.0002
    print("\n=== THE EXACT ARITHMETIC OF SL=5 vs SL=2 ===")
    print(f"Saved Trades (SL=2 loss -> SL=5 win):       {saved} trades  -> +{saved*4} ticks (+{saved*0.0008:.4f} USDT)")
    print(f"Damaged Trades (SL=2 loss -> SL=5 loss):     {damaged} trades -> -{damaged*3} ticks (-{damaged*0.0006:.4f} USDT)")
    print(f"Net Economic Difference (SL=5 vs SL=2):      {net_ticks_diff:+d} ticks ({net_usdt_diff:+.4f} USDT)")
    print(f"Saved to {OUT_CSV}")

if __name__ == "__main__":
    run_counterfactual_matrix()
