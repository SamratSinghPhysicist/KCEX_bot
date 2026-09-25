"""
High-Throughput Single Asset/Timeframe Backtest Worker
=====================================================
Executes an institutional Order Book + Demand/Supply Block Strategy backtest
for a single (pair, timeframe) combination. Designed for distributed parallel
matrix execution on GitHub Actions runners and local testing.

Features:
- Automated OHLCV data retrieval from Binance Futures REST / CCXT / local cache.
- Exact KCEX contract specifications and zero-fee promotional awareness.
- 10% equity compounding model with 15x isolated leverage.
- Calibrated adverse slippage (0.05% for top 10/majors, 0.10%-0.15% for meme/micro coins).
- Dual export: Standardized results_${PAIR}_${TIMEFRAME}.json & .csv.
"""

from __future__ import annotations
import os
import sys
import json
import csv
import time
import math
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple

# Ensure utf-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.scanner import canonicalize_symbol, format_ms_to_utc, parse_timestamp_ms
from BACKTESTER.engine.data_loader import OHLCVLoader, Candle, normalize_timeframe, timeframe_to_kcex_interval
from BACKTESTER.engine.market_sim import BacktestMarket, DEFAULT_CONTRACTS
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator, PerformanceSummary
from kcex.market import ContractInfo


# ---------------------------------------------------------------------------
# Asset Classification & Slippage / Binance Mapping
# ---------------------------------------------------------------------------

TOP_MAJORS_PAIRS = {
    "BTC_USDT", "ETH_USDT", "SOL_USDT", "XRP_USDT", "AVAX_USDT",
    "TRX_USDT", "LTC_USDT", "XMR_USDT", "HYPE_USDT", "WIF_USDT"
}

BINANCE_SYMBOL_OVERRIDE = {
    "MOG_USDT": "1000000MOGUSDT",
    "MOGUSDT": "1000000MOGUSDT",
    "1000000MOG_USDT": "1000000MOGUSDT",
    "1000000MOGUSDT": "1000000MOGUSDT",
    "1000MOG_USDT": "1000000MOGUSDT"
}

ZERO_FEE_PAIRS = {
    "MELANIA_USDT", "DOGS_USDT", "MEME_USDT", "BOME_USDT", "ACT_USDT",
    "AVAAI_USDT", "MOG_USDT", "1000000MOG_USDT", "CHILLGUY_USDT",
    "GOAT_USDT", "PIPPIN_USDT", "WIF_USDT", "KOMA_USDT", "TRUMP_USDT",
    "AIXBT_USDT", "DOGE_USDT"
}


def resolve_binance_symbol(pair: str) -> str:
    """Maps KCEX pair symbol to Binance Futures symbol."""
    canonical = canonicalize_symbol(pair)
    if canonical in BINANCE_SYMBOL_OVERRIDE:
        return BINANCE_SYMBOL_OVERRIDE[canonical]
    return canonical.replace("_", "").upper()


def get_default_slippage_pct(pair: str) -> float:
    """
    Returns adverse slippage percentage based on asset tier:
    - Top 10 / High-Cap / Layer-1: 0.05% (0.0005)
    - Micro / Meme coins: 0.10% (0.0010)
    """
    canonical = canonicalize_symbol(pair)
    if canonical in TOP_MAJORS_PAIRS:
        return 0.0005
    return 0.0010


# ---------------------------------------------------------------------------
# High-Speed Historical OHLCV Fetcher
# ---------------------------------------------------------------------------

def fetch_binance_futures_klines(
    binance_symbol: str,
    timeframe: str,
    start_ms: int,
    end_ms: int,
    max_retries: int = 4
) -> List[List[Any]]:
    """
    Paginates Binance Futures REST endpoint /fapi/v1/klines to retrieve
    historical candlesticks. Fast, lightweight, and requires no API keys.
    """
    base_url = "https://fapi.binance.com/fapi/v1/klines"
    all_klines: List[List[Any]] = []
    curr_ms = start_ms
    limit = 1500

    print(f"[*] Querying Binance Futures REST API for {binance_symbol} ({timeframe}) from {format_ms_to_utc(start_ms)} to {format_ms_to_utc(end_ms)}...")

    while curr_ms < end_ms:
        url = f"{base_url}?symbol={binance_symbol}&interval={timeframe}&startTime={curr_ms}&endTime={end_ms}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (KCEX-Backtester-Matrix)"})
        
        success = False
        for attempt in range(1, max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode())
                        if not data:
                            curr_ms = end_ms # No further data
                            success = True
                            break
                        all_klines.extend(data)
                        last_ts = int(data[-1][0])
                        if last_ts <= curr_ms:
                            curr_ms = end_ms
                            success = True
                            break
                        curr_ms = last_ts + 1
                        if len(data) < limit:
                            curr_ms = end_ms
                        success = True
                        break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    sleep_time = attempt * 3.0
                    print(f"    [!] Rate limited (429). Backing off {sleep_time:.1f}s (attempt {attempt}/{max_retries})...")
                    time.sleep(sleep_time)
                else:
                    print(f"    [!] HTTP {e.code} fetching klines for {binance_symbol}: {e.reason}")
                    time.sleep(1.0)
            except Exception as e:
                print(f"    [!] Network error on attempt {attempt}: {e}")
                time.sleep(1.0)

        if not success:
            print(f"[!] Warning: Terminating pagination early for {binance_symbol} at timestamp {curr_ms}.")
            break

        # Mild throttle to prevent burst IP rate limits
        time.sleep(0.04)

    return all_klines


def fetch_ccxt_klines(
    binance_symbol: str,
    timeframe: str,
    start_ms: int,
    end_ms: int
) -> List[List[Any]]:
    """Fallback fetcher using CCXT library if available."""
    try:
        import ccxt
        exchange = ccxt.binanceusdm({"enableRateLimit": True, "timeout": 20000})
        market_symbol = f"{binance_symbol[:-4]}/{binance_symbol[-4:]}:USDT"
        all_candles = []
        curr_ms = start_ms
        while curr_ms < end_ms:
            batch = exchange.fetch_ohlcv(market_symbol, timeframe=timeframe, since=curr_ms, limit=1000)
            if not batch:
                break
            all_candles.extend(batch)
            last_ts = batch[-1][0]
            if last_ts <= curr_ms:
                break
            curr_ms = last_ts + 1
            if len(batch) < 1000:
                break
        return all_candles
    except Exception as e:
        print(f"[!] CCXT fetcher fallback failed: {e}")
        return []


def ensure_and_load_ohlcv(
    canonical_pair: str,
    binance_symbol: str,
    timeframe: str,
    start_ms: int,
    end_ms: int,
    data_dir: str
) -> List[Candle]:
    """
    Loads candles from local cache or downloads from Binance and caches to disk.
    """
    loader = OHLCVLoader(data_dir=data_dir)
    candles = loader.load_candles(
        symbol=binance_symbol,
        timeframe=timeframe,
        start_ms=start_ms,
        end_ms=end_ms
    )

    # Check if local candles are sufficiently dense (> 50 bars)
    if len(candles) >= 50:
        print(f"[+] Loaded {len(candles)} cached candles from {data_dir} for {binance_symbol} ({timeframe})")
        return candles

    print(f"[*] Incomplete local cache for {binance_symbol} ({timeframe}). Downloading historical bars...")
    raw_data = fetch_binance_futures_klines(binance_symbol, timeframe, start_ms, end_ms)
    
    if not raw_data:
        # Try CCXT fallback
        raw_data = fetch_ccxt_klines(binance_symbol, timeframe, start_ms, end_ms)

    if not raw_data:
        print(f"[!] Critical Error: Unable to fetch historical OHLCV data for {binance_symbol} ({timeframe})")
        return []

    # Convert to Candle objects
    converted: List[Candle] = []
    for row in raw_data:
        try:
            o_time = int(row[0])
            c_open = float(row[1])
            c_high = float(row[2])
            c_low = float(row[3])
            c_close = float(row[4])
            c_vol = float(row[5])
            c_time = int(row[6]) if len(row) > 6 else (o_time + 60000)
            q_vol = float(row[7]) if len(row) > 7 else 0.0
            n_trades = int(row[8]) if len(row) > 8 else 0

            converted.append(Candle(
                open_time_ms=o_time,
                open=c_open,
                high=c_high,
                low=c_low,
                close=c_close,
                volume=c_vol,
                close_time_ms=c_time,
                quote_volume=q_vol,
                trades_count=n_trades
            ))
        except (ValueError, IndexError):
            continue

    # Save to local cache directory as CSV so actions/cache or repeated runs reuse it
    sym_dir = os.path.join(data_dir, binance_symbol, timeframe)
    os.makedirs(sym_dir, exist_ok=True)
    save_path = os.path.join(sym_dir, f"{binance_symbol}-{timeframe}-consolidated.csv")
    try:
        with open(save_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count"])
            for c in converted:
                writer.writerow([c.open_time_ms, c.open, c.high, c.low, c.close, c.volume, c.close_time_ms, c.quote_volume, c.trades_count])
        print(f"[+] Saved {len(converted)} candles to {save_path}")
    except Exception as e:
        print(f"[!] Warning: Could not cache CSV to disk: {e}")

    return converted


# ---------------------------------------------------------------------------
# Single Backtest Runner Core
# ---------------------------------------------------------------------------

def run_single_backtest(
    pair: str,
    timeframe: str,
    months: int = 6,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    leverage: int = 15,
    margin_pct: float = 10.0,
    capital: float = 100.0,
    strategy: str = "ORDER_BLOCK_DEMAND",
    maker_fee: Optional[float] = None,
    taker_fee: Optional[float] = None,
    slippage_pct: Optional[float] = None,
    output_dir: str = "artifacts",
    data_dir: str = "BACKTESTER/OHLCV_Data_Binance"
) -> Dict[str, Any]:
    """
    Executes a complete backtest for one (pair, timeframe) pair and writes artifacts.
    """
    canonical = canonicalize_symbol(pair)
    binance_sym = resolve_binance_symbol(canonical)
    norm_tf = normalize_timeframe(timeframe)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Date range resolution
    now_utc = datetime.now(timezone.utc)
    if end_date:
        e_dt = datetime.strptime(end_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        e_dt = now_utc

    if start_date:
        s_dt = datetime.strptime(start_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        s_dt = e_dt - timedelta(days=int(months * 30.5))

    start_ms = int(s_dt.timestamp() * 1000)
    end_ms = int(e_dt.timestamp() * 1000)

    # 2. Fee Model Configuration
    is_zero_fee = canonical in ZERO_FEE_PAIRS
    if maker_fee is None:
        eff_maker_fee = 0.0
    else:
        eff_maker_fee = maker_fee

    if taker_fee is None:
        eff_taker_fee = 0.0 if is_zero_fee else 0.0002  # 0.02% taker fee
    else:
        eff_taker_fee = taker_fee

    # 3. Slippage Configuration
    eff_slippage_pct = slippage_pct if slippage_pct is not None else get_default_slippage_pct(canonical)

    print("\n" + "=" * 80)
    print(f"🚀 RUNNING DISTRIBUTED MATRIX BACKTEST: {canonical} [{norm_tf.upper()}]")
    print(f"   Binance Symbol:   {binance_sym}")
    print(f"   Date Window:      {s_dt.strftime('%Y-%m-%d')} to {e_dt.strftime('%Y-%m-%d')} ({months} months)")
    print(f"   Strategy:         {strategy} (Vivek Yadav SMC 1:2 RR)")
    print(f"   Capital:          ${capital:.2f} USDT | Leverage: {leverage}x Isolated")
    print(f"   Compounding Sizing: {margin_pct}% Available Equity")
    print(f"   Fee Schedule:     Maker {eff_maker_fee*100:.2f}% / Taker {eff_taker_fee*100:.3f}% ({'ZERO-FEE' if is_zero_fee else 'STANDARD'})")
    print(f"   Adverse Slippage: {eff_slippage_pct*100:.2f}%")
    print("=" * 80)

    # 4. Fetch / Load primary candles
    candles = ensure_and_load_ohlcv(
        canonical_pair=canonical,
        binance_symbol=binance_sym,
        timeframe=norm_tf,
        start_ms=start_ms,
        end_ms=end_ms,
        data_dir=data_dir
    )

    if not candles:
        err_msg = f"Zero candle data available for {canonical} ({norm_tf})"
        print(f"[!] {err_msg}")
        return {
            "pair": canonical,
            "binance_symbol": binance_sym,
            "timeframe": norm_tf,
            "status": "FAILED",
            "error": err_msg
        }

    # Load 1m sub-candles for disambiguation if timeframe > 1m and mode is 5m
    sub_1m_candles = None
    if norm_tf == "5m":
        print(f"[*] Ensuring 1m disambiguation candles for 5m precision...")
        sub_1m_candles = ensure_and_load_ohlcv(
            canonical_pair=canonical,
            binance_symbol=binance_sym,
            timeframe="1m",
            start_ms=start_ms,
            end_ms=end_ms,
            data_dir=data_dir
        )

    # 5. Contract Info & Precision Calculation
    market = BacktestMarket(
        fee_mode="MANUAL",
        maker_fee_override=eff_maker_fee,
        taker_fee_override=eff_taker_fee
    )
    market.register_candles(canonical, norm_tf, candles)
    contract = market.get_contract_detail(canonical)

    pu = contract.price_unit if contract.price_unit > 0 else 0.0001
    sample_price = candles[0].close
    # Translate slippage percentage to integer ticks
    slip_ticks = max(1, int(round((sample_price * eff_slippage_pct) / pu)))

    # 6. Initialize Engine & Config
    config = BacktestConfig(
        symbol=canonical,
        timeframe=norm_tf,
        strategy_mode=strategy,
        start_time=s_dt.strftime("%Y-%m-%d"),
        end_time=e_dt.strftime("%Y-%m-%d"),
        volume_mode="MARGIN_PCT",
        margin_pct=margin_pct,
        leverage=leverage,
        initial_balance_usdt=capital,
        fee_mode="MANUAL",
        maker_fee_override=eff_maker_fee,
        taker_fee_override=eff_taker_fee,
        slippage_enabled=True,
        slippage_ticks=slip_ticks,
        risk_reward_ratio=2.0,
        pivot_len=5,
        use_tick_data=False
    )

    engine = BacktestExecutionEngine(config=config, market=market)
    
    t_start = time.time()
    outcomes = engine.run(
        preloaded_candles=candles,
        preloaded_sub_candles_1m=sub_1m_candles if norm_tf == "5m" else []
    )
    runtime_sec = time.time() - t_start

    # 7. Calculate Institutional Performance Metrics
    summary: PerformanceSummary = PerformanceCalculator.calculate(
        outcomes=outcomes,
        initial_balance_usdt=capital,
        inr_rate=94.45
    )

    # Monthly trade frequency
    timespan_days = max(1, (candles[-1].close_time_ms - candles[0].open_time_ms) / (1000 * 86400))
    monthly_freq = round((len(outcomes) / (timespan_days / 30.4375)), 2) if timespan_days > 0 else 0.0

    # 8. Construct Output Data Structure
    result_payload: Dict[str, Any] = {
        "pair": canonical,
        "binance_symbol": binance_sym,
        "timeframe": norm_tf,
        "strategy": strategy,
        "date_range": {
            "start": format_ms_to_utc(candles[0].open_time_ms),
            "end": format_ms_to_utc(candles[-1].close_time_ms),
            "total_candles": len(candles),
            "timespan_days": round(timespan_days, 1)
        },
        "parameters": {
            "leverage": leverage,
            "margin_pct": margin_pct,
            "initial_capital_usdt": capital,
            "risk_reward_ratio": 2.0,
            "maker_fee_rate": eff_maker_fee,
            "taker_fee_rate": eff_taker_fee,
            "is_zero_fee": is_zero_fee,
            "slippage_pct": eff_slippage_pct,
            "slippage_ticks": slip_ticks,
            "contract_size": contract.contract_size,
            "min_contracts": contract.min_volume,
            "price_unit": contract.price_unit
        },
        "metrics": {
            "total_trades": summary.total_trades,
            "winning_trades": summary.winning_trades,
            "losing_trades": summary.losing_trades,
            "scratch_trades": summary.scratch_trades,
            "win_rate_pct": round(summary.win_rate_pct, 2),
            "profit_factor": round(summary.profit_factor, 2) if not math.isinf(summary.profit_factor) else 999.0,
            "initial_balance_usdt": round(summary.initial_balance_usdt, 2),
            "final_balance_usdt": round(summary.final_balance_usdt, 2),
            "net_pnl_usdt": round(summary.net_pnl_usdt, 2),
            "total_roi_pct": round(summary.net_roi_pct, 2),
            "max_drawdown_usdt": round(summary.max_drawdown_usdt, 2),
            "max_drawdown_pct": round(summary.max_drawdown_pct, 2),
            "sharpe_ratio": round(summary.sharpe_ratio, 2),
            "sortino_ratio": round(summary.sortino_ratio, 2),
            "calmar_ratio": round(summary.calmar_ratio, 2),
            "monthly_signal_frequency": monthly_freq,
            "avg_trade_pnl_usdt": round(summary.avg_trade_pnl_usdt, 3),
            "avg_win_usdt": round(summary.avg_win_pnl_usdt, 3),
            "avg_loss_usdt": round(summary.avg_loss_pnl_usdt, 3),
            "win_loss_ratio": round(summary.win_loss_ratio, 2),
            "total_fees_usdt": round(summary.total_fees_usdt, 3),
            "long_trades": summary.long_trades,
            "long_wins": summary.long_wins,
            "long_win_rate_pct": round(summary.long_win_rate_pct, 2),
            "short_trades": summary.short_trades,
            "short_wins": summary.short_wins,
            "short_win_rate_pct": round(summary.short_win_rate_pct, 2),
            "runtime_seconds": round(runtime_sec, 2)
        },
        "execution_status": "SUCCESS"
    }

    # 9. Write JSON Artifact
    json_path = os.path.join(output_dir, f"results_{canonical}_{norm_tf}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_payload, f, indent=2)
    print(f"[+] Output JSON Artifact: {json_path}")

    # 10. Write CSV Trades Artifact
    csv_path = os.path.join(output_dir, f"results_{canonical}_{norm_tf}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "trade_id", "entry_time_utc", "exit_time_utc", "symbol", "direction",
            "entry_price", "exit_price", "contracts", "margin_usdt",
            "gross_pnl_usdt", "fee_open_usdt", "fee_close_usdt", "total_fee_usdt",
            "net_pnl_usdt", "roe_pct", "exit_reason", "duration_seconds", "wallet_balance_usdt"
        ])
        running_bal = capital
        for o in outcomes:
            running_bal += o.realized_pnl_usdt
            open_ts = getattr(o, "open_time", 0.0)
            close_ts = getattr(o, "close_time", 0.0)
            e_str = datetime.fromtimestamp(open_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if open_ts > 0 else ""
            x_str = datetime.fromtimestamp(close_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if close_ts > 0 else ""
            exit_r = o.exit_reason.value if hasattr(o.exit_reason, "value") else str(o.exit_reason)
            f_open = round(getattr(o, "fee_open_usdt", 0.0), 5)
            f_close = round(getattr(o, "fee_close_usdt", 0.0), 5)
            f_total = round(getattr(o, "fee_total_usdt", 0.0), 5)
            net_pnl = round(o.realized_pnl_usdt, 4)
            gross_pnl = round(net_pnl + f_total, 4)
            writer.writerow([
                o.trade_id, e_str, x_str, o.symbol, o.direction.value if hasattr(o.direction, "value") else str(o.direction),
                o.entry_price, o.exit_price, getattr(o, "vol_contracts", 1), round(getattr(o, "margin_used_usdt", 0.0), 2),
                gross_pnl, f_open, f_close, f_total, net_pnl,
                round(getattr(o, "roe_percentage", 0.0), 2), exit_r,
                round(o.duration_seconds, 1), round(running_bal, 2)
            ])
    print(f"[+] Output CSV Trades Artifact: {csv_path}")

    # Console Summary Table
    gross_total = summary.net_pnl_usdt + summary.total_fees_usdt
    print("\n" + "-" * 80)
    print(f"📊 SUMMARY: {canonical} [{norm_tf.upper()}]")
    print(f"   Trades:        {summary.total_trades} (W: {summary.winning_trades} / L: {summary.losing_trades})")
    print(f"   Win Rate:      {summary.win_rate_pct:.2f}%")
    print(f"   Profit Factor: {summary.profit_factor:.2f}")
    print(f"   Fee Schedule:  {'0.00% Maker / 0.00% Taker (ZERO-FEE)' if is_zero_fee else f'0.00% Maker / {eff_taker_fee*100:.2f}% Taker'}")
    print(f"   Gross PnL:     ${gross_total:+.2f}")
    print(f"   Total Fees:    ${summary.total_fees_usdt:.4f}")
    print(f"   Net PnL / ROI: ${summary.net_pnl_usdt:+.2f} ({summary.net_roi_pct:+.2f}%)")
    print(f"   Max Drawdown:  {summary.max_drawdown_pct:.2f}% (${summary.max_drawdown_usdt:.2f})")
    print(f"   Sharpe Ratio:  {summary.sharpe_ratio:.2f}")
    print(f"   Monthly Freq:  {monthly_freq:.1f} trades/month")
    print(f"   Completed in:  {runtime_sec:.2f}s")
    print("-" * 80 + "\n")

    return result_payload


def main():
    parser = argparse.ArgumentParser(description="Distributed Single Asset/Timeframe Backtester")
    parser.add_argument("--pair", "--symbol", type=str, required=True, help="Trading pair (e.g. MELANIA_USDT, XRP_USDT)")
    parser.add_argument("--timeframe", "--tf", type=str, required=True, choices=["5m", "15m", "1h", "4h", "1d"], help="Candle timeframe")
    parser.add_argument("--months", type=int, default=6, help="Historical lookback in months (default: 6)")
    parser.add_argument("--start-date", type=str, default=None, help="Explicit start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default=None, help="Explicit end date (YYYY-MM-DD)")
    parser.add_argument("--leverage", type=int, default=15, help="Leverage multiplier (default: 15)")
    parser.add_argument("--margin-pct", type=float, default=10.0, help="Compounding margin percentage (default: 10.0)")
    parser.add_argument("--capital", type=float, default=100.0, help="Initial wallet capital (default: 100.0)")
    parser.add_argument("--strategy", type=str, default="ORDER_BLOCK_DEMAND", help="Strategy (default: ORDER_BLOCK_DEMAND)")
    parser.add_argument("--maker-fee", type=float, default=None, help="Maker fee override rate")
    parser.add_argument("--taker-fee", type=float, default=None, help="Taker fee override rate")
    parser.add_argument("--slippage-pct", type=float, default=None, help="Adverse slippage percentage override (e.g. 0.0005 for 0.05%)")
    parser.add_argument("--output-dir", type=str, default="artifacts", help="Directory for output artifacts")
    parser.add_argument("--data-dir", type=str, default="BACKTESTER/OHLCV_Data_Binance", help="Local directory for OHLCV candlestick cache")

    args = parser.parse_args()

    res = run_single_backtest(
        pair=args.pair,
        timeframe=args.timeframe,
        months=args.months,
        start_date=args.start_date,
        end_date=args.end_date,
        leverage=args.leverage,
        margin_pct=args.margin_pct,
        capital=args.capital,
        strategy=args.strategy,
        maker_fee=args.maker_fee,
        taker_fee=args.taker_fee,
        slippage_pct=args.slippage_pct,
        output_dir=args.output_dir,
        data_dir=args.data_dir
    )

    if res.get("execution_status") != "SUCCESS":
        sys.exit(1)


if __name__ == "__main__":
    main()
