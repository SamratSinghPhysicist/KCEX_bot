"""
Dual-Account Reverse Trading Experiment Engine
==============================================
Core backtesting and analytics engine implementing:
1. Two independent accounts (starting $1000 USDT each).
2. Account A trades exclusively BTCUSDT.
3. Account B trades exclusively ETHUSDT.
4. Simultaneous entry with 100% current capital and 2x leverage.
5. Reverse trading:
   - Case 1: Always Buy BTC (Long), Sell ETH (Short)
   - Case 2: Always Sell BTC (Short), Buy ETH (Long)
6. Configurations:
   - Config 1: TP = 3.0%, SL = 3.0%
   - Config 2: TP = 1.5%, SL = 1.5%
   - Config 3: TP = 1.5%, SL = 3.0%
   - Config 4: TP = 0.75%, SL = 1.5%
7. Strict synchronization: Next trade takes place only when AND as soon as
   BOTH accounts become free.
8. 1-minute candle dispute resolution when TP and SL are hit in the same candle;
   if both hit within 1m candle, declares SL.
9. Comprehensive metrics: PnL, Win/Loss, Win Rate, Win/Loss streak distributions,
   trades to reach net profit of +10% or net loss of -3%, drawdowns, and pair hedge stats.
"""

from __future__ import annotations
import os
import csv
import glob
import time
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class CandleData:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time_ms: int


@dataclass
class TP_SL_Config:
    name: str
    tp_pct: float
    sl_pct: float
    description: str


CONFIGS = [
    TP_SL_Config(name="TP3.0_SL3.0", tp_pct=3.0, sl_pct=3.0, description="TP 3.0% | SL 3.0%"),
    TP_SL_Config(name="TP1.5_SL1.5", tp_pct=1.5, sl_pct=1.5, description="TP 1.5% | SL 1.5%"),
    TP_SL_Config(name="TP1.5_SL3.0", tp_pct=1.5, sl_pct=3.0, description="TP 1.5% | SL 3.0%"),
    TP_SL_Config(name="TP0.75_SL1.5", tp_pct=0.75, sl_pct=1.5, description="TP 0.75% | SL 1.5%"),
]


@dataclass
class SingleTrade:
    trade_id: int
    cycle_id: int
    account: str           # "ACCOUNT_A_BTC" or "ACCOUNT_B_ETH"
    symbol: str            # "BTCUSDT" or "ETHUSDT"
    case: str              # "Case 1" or "Case 2"
    direction: str         # "LONG" or "SHORT"
    config_name: str
    tp_pct: float
    sl_pct: float
    entry_time_ms: int
    entry_time_iso: str
    entry_price: float
    exit_time_ms: int
    exit_time_iso: str
    exit_price: float
    exit_reason: str       # "TP", "SL", or "END_OF_DATA"
    duration_candles: int
    duration_seconds: float
    initial_trade_capital: float
    notional_value: float
    quantity: float
    gross_pnl: float
    fees: float
    net_pnl: float
    pnl_pct: float
    balance_after: float
    is_win: bool


@dataclass
class PairTradeCycle:
    cycle_id: int
    case: str
    timeframe: str
    config_name: str
    entry_time_iso: str
    entry_time_ms: int
    btc_exit_time_iso: str
    eth_exit_time_iso: str
    cycle_exit_time_iso: str
    cycle_exit_time_ms: int
    holding_candles: int
    btc_trade: SingleTrade
    eth_trade: SingleTrade
    combined_net_pnl: float
    combined_balance: float
    pair_win: bool


@dataclass
class AccountPerformance:
    account: str
    symbol: str
    case: str
    timeframe: str
    config_name: str
    tp_pct: float
    sl_pct: float
    initial_balance: float
    final_balance: float
    net_pnl: float
    net_roi_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate_pct: float
    gross_profit: float
    gross_loss: float
    profit_factor: float
    max_drawdown_usd: float
    max_drawdown_pct: float
    max_win_streak: int
    max_loss_streak: int
    win_streak_distribution: Dict[int, int]
    loss_streak_distribution: Dict[int, int]
    trades_to_reach_plus_10_pct: Optional[int]
    date_reached_plus_10_pct: Optional[str]
    trades_to_reach_minus_3_pct: Optional[int]
    date_reached_minus_3_pct: Optional[str]
    avg_trade_pnl: float
    avg_win_pnl: float
    avg_loss_pnl: float
    avg_duration_minutes: float


def format_ms(ts_ms: int) -> str:
    """Formats epoch ms to ISO UTC string."""
    dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_date_to_ms(d_str: str) -> int:
    """Parses YYYY-MM-DD or YYYY-MM-DD HH:MM:SS to epoch ms."""
    s = d_str.strip()
    if len(s) == 10:
        dt = datetime.datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    else:
        dt = datetime.datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)


def load_candles_from_dir(
    symbol: str,
    timeframe: str,
    data_dir: str = "BACKTESTER/OHLCV_Data_Binance",
    start_ms: Optional[int] = None,
    end_ms: Optional[int] = None
) -> List[CandleData]:
    """Loads and sorts candles from monthly CSV files."""
    sym_clean = symbol.replace("_", "").upper()
    folder = os.path.join(data_dir, sym_clean, timeframe)
    if not os.path.exists(folder):
        return []

    pattern = os.path.join(folder, f"{sym_clean}-{timeframe}-*.csv")
    files = sorted(glob.glob(pattern))

    candles: List[CandleData] = []
    seen_times = set()

    for fpath in files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                continue

            for row in reader:
                if len(row) < 6:
                    continue
                try:
                    open_time = int(float(row[0]))
                    if start_ms and open_time < start_ms:
                        continue
                    if end_ms and open_time > end_ms:
                        break
                    if open_time in seen_times:
                        continue
                    seen_times.add(open_time)

                    o = float(row[1])
                    h = float(row[2])
                    l = float(row[3])
                    c = float(row[4])
                    v = float(row[5])
                    close_time = int(float(row[6])) if len(row) > 6 else (open_time + 59999)

                    candles.append(CandleData(
                        open_time_ms=open_time,
                        open=o,
                        high=h,
                        low=l,
                        close=c,
                        volume=v,
                        close_time_ms=close_time
                    ))
                except (ValueError, IndexError):
                    continue

    candles.sort(key=lambda c: c.open_time_ms)
    return candles


def evaluate_candle_tp_sl(
    direction: str,
    entry_price: float,
    tp_price: float,
    sl_price: float,
    candle: CandleData,
    sub_1m_map: Optional[Dict[int, List[CandleData]]] = None,
    timeframe: str = "1m"
) -> Tuple[Optional[str], float]:
    """
    Evaluates whether a candle hits TP or SL.
    Resolves simultaneous TP & SL disputes:
    1. Checks if candle Open immediately breached a level.
    2. If timeframe > 1m, checks 1m sub-candles chronologically.
    3. If 1m sub-candle breaches both, declares SL.
    4. If timeframe is 1m and both breached without open gap, declares SL.

    Returns: (exit_reason, exit_price) where exit_reason is "TP", "SL", or None.
    """
    if direction == "LONG":
        tp_breached = (candle.high >= tp_price)
        sl_breached = (candle.low <= sl_price)

        if not tp_breached and not sl_breached:
            return None, 0.0

        if tp_breached and not sl_breached:
            return "TP", tp_price

        if sl_breached and not tp_breached:
            return "SL", sl_price

        # Dispute: Both breached!
        # Step 1: Open gap
        if candle.open >= tp_price:
            return "TP", tp_price
        elif candle.open <= sl_price:
            return "SL", sl_price

        # Step 2: Timeframe resolution
        if timeframe == "1m":
            return "SL", sl_price

        if sub_1m_map and candle.open_time_ms in sub_1m_map:
            sub_candles = sub_1m_map[candle.open_time_ms]
            for sc in sub_candles:
                sc_tp = (sc.high >= tp_price)
                sc_sl = (sc.low <= sl_price)
                if sc_tp and sc_sl:
                    return "SL", sl_price
                elif sc_tp:
                    return "TP", tp_price
                elif sc_sl:
                    return "SL", sl_price

        return "SL", sl_price

    else: # SHORT
        tp_breached = (candle.low <= tp_price)
        sl_breached = (candle.high >= sl_price)

        if not tp_breached and not sl_breached:
            return None, 0.0

        if tp_breached and not sl_breached:
            return "TP", tp_price

        if sl_breached and not tp_breached:
            return "SL", sl_price

        # Dispute: Both breached!
        # Step 1: Open gap
        if candle.open <= tp_price:
            return "TP", tp_price
        elif candle.open >= sl_price:
            return "SL", sl_price

        # Step 2: Timeframe resolution
        if timeframe == "1m":
            return "SL", sl_price

        if sub_1m_map and candle.open_time_ms in sub_1m_map:
            sub_candles = sub_1m_map[candle.open_time_ms]
            for sc in sub_candles:
                sc_tp = (sc.low <= tp_price)
                sc_sl = (sc.high >= sl_price)
                if sc_tp and sc_sl:
                    return "SL", sl_price
                elif sc_tp:
                    return "TP", tp_price
                elif sc_sl:
                    return "SL", sl_price

        return "SL", sl_price


def build_sub_1m_map(
    higher_tf_candles: List[CandleData],
    sub_1m_candles: List[CandleData]
) -> Dict[int, List[CandleData]]:
    """Builds a map from higher_tf_candle.open_time_ms to list of 1m sub-candles."""
    sub_map: Dict[int, List[CandleData]] = {}
    if not sub_1m_candles or not higher_tf_candles:
        return sub_map

    idx_1m = 0
    len_1m = len(sub_1m_candles)

    for h_candle in higher_tf_candles:
        h_open = h_candle.open_time_ms
        h_close = h_candle.close_time_ms

        while idx_1m < len_1m and sub_1m_candles[idx_1m].open_time_ms < h_open:
            idx_1m += 1

        matches = []
        curr = idx_1m
        while curr < len_1m and sub_1m_candles[curr].open_time_ms <= h_close:
            matches.append(sub_1m_candles[curr])
            curr += 1

        if matches:
            sub_map[h_open] = matches

    return sub_map


def compute_account_metrics(
    trades: List[SingleTrade],
    account_name: str,
    symbol: str,
    case_name: str,
    timeframe: str,
    config: TP_SL_Config,
    initial_balance: float = 1000.0
) -> AccountPerformance:
    """Computes exhaustive statistical metrics for a single account sequence."""
    total_trades = len(trades)
    if total_trades == 0:
        return AccountPerformance(
            account=account_name,
            symbol=symbol,
            case=case_name,
            timeframe=timeframe,
            config_name=config.name,
            tp_pct=config.tp_pct,
            sl_pct=config.sl_pct,
            initial_balance=initial_balance,
            final_balance=initial_balance,
            net_pnl=0.0,
            net_roi_pct=0.0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate_pct=0.0,
            gross_profit=0.0,
            gross_loss=0.0,
            profit_factor=0.0,
            max_drawdown_usd=0.0,
            max_drawdown_pct=0.0,
            max_win_streak=0,
            max_loss_streak=0,
            win_streak_distribution={},
            loss_streak_distribution={},
            trades_to_reach_plus_10_pct=None,
            date_reached_plus_10_pct=None,
            trades_to_reach_minus_3_pct=None,
            date_reached_minus_3_pct=None,
            avg_trade_pnl=0.0,
            avg_win_pnl=0.0,
            avg_loss_pnl=0.0,
            avg_duration_minutes=0.0
        )

    winning_trades = sum(1 for t in trades if t.is_win)
    losing_trades = total_trades - winning_trades
    win_rate = (winning_trades / total_trades) * 100.0

    gross_profit = sum(t.net_pnl for t in trades if t.net_pnl > 0)
    gross_loss = abs(sum(t.net_pnl for t in trades if t.net_pnl < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 1.0)

    final_balance = trades[-1].balance_after
    net_pnl = final_balance - initial_balance
    net_roi_pct = (net_pnl / initial_balance) * 100.0

    # Drawdown calculation
    peak = initial_balance
    max_dd_usd = 0.0
    max_dd_pct = 0.0
    running_bal = initial_balance

    for t in trades:
        running_bal = t.balance_after
        if running_bal > peak:
            peak = running_bal
        dd_usd = peak - running_bal
        dd_pct = (dd_usd / peak * 100.0) if peak > 0 else 0.0
        if dd_usd > max_dd_usd:
            max_dd_usd = dd_usd
        if dd_pct > max_dd_pct:
            max_dd_pct = dd_pct

    # Milestones: +10% net profit ($1100) and -3% net loss ($970)
    target_profit_balance = initial_balance * 1.10
    target_loss_balance = initial_balance * 0.97

    trades_to_plus_10 = None
    date_to_plus_10 = None
    trades_to_minus_3 = None
    date_to_minus_3 = None

    for i, t in enumerate(trades, start=1):
        if trades_to_plus_10 is None and t.balance_after >= target_profit_balance:
            trades_to_plus_10 = i
            date_to_plus_10 = t.exit_time_iso

        if trades_to_minus_3 is None and t.balance_after <= target_loss_balance:
            trades_to_minus_3 = i
            date_to_minus_3 = t.exit_time_iso

    # Streaks calculation and distributions
    curr_win_streak = 0
    curr_loss_streak = 0
    max_win_streak = 0
    max_loss_streak = 0

    win_streaks: List[int] = []
    loss_streaks: List[int] = []

    for t in trades:
        if t.is_win:
            if curr_loss_streak > 0:
                loss_streaks.append(curr_loss_streak)
                curr_loss_streak = 0
            curr_win_streak += 1
            if curr_win_streak > max_win_streak:
                max_win_streak = curr_win_streak
        else:
            if curr_win_streak > 0:
                win_streaks.append(curr_win_streak)
                curr_win_streak = 0
            curr_loss_streak += 1
            if curr_loss_streak > max_loss_streak:
                max_loss_streak = curr_loss_streak

    if curr_win_streak > 0:
        win_streaks.append(curr_win_streak)
    if curr_loss_streak > 0:
        loss_streaks.append(curr_loss_streak)

    win_streak_dist: Dict[int, int] = {}
    for s in win_streaks:
        win_streak_dist[s] = win_streak_dist.get(s, 0) + 1

    loss_streak_dist: Dict[int, int] = {}
    for s in loss_streaks:
        loss_streak_dist[s] = loss_streak_dist.get(s, 0) + 1

    avg_trade_pnl = net_pnl / total_trades if total_trades > 0 else 0.0
    wins_list = [t.net_pnl for t in trades if t.is_win]
    loss_list = [t.net_pnl for t in trades if not t.is_win]
    avg_win_pnl = sum(wins_list) / len(wins_list) if wins_list else 0.0
    avg_loss_pnl = sum(loss_list) / len(loss_list) if loss_list else 0.0
    avg_duration_min = sum(t.duration_seconds for t in trades) / (60.0 * total_trades) if total_trades > 0 else 0.0

    return AccountPerformance(
        account=account_name,
        symbol=symbol,
        case=case_name,
        timeframe=timeframe,
        config_name=config.name,
        tp_pct=config.tp_pct,
        sl_pct=config.sl_pct,
        initial_balance=initial_balance,
        final_balance=round(final_balance, 2),
        net_pnl=round(net_pnl, 2),
        net_roi_pct=round(net_roi_pct, 2),
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        win_rate_pct=round(win_rate, 2),
        gross_profit=round(gross_profit, 2),
        gross_loss=round(gross_loss, 2),
        profit_factor=round(profit_factor, 2),
        max_drawdown_usd=round(max_dd_usd, 2),
        max_drawdown_pct=round(max_dd_pct, 2),
        max_win_streak=max_win_streak,
        max_loss_streak=max_loss_streak,
        win_streak_distribution=win_streak_dist,
        loss_streak_distribution=loss_streak_dist,
        trades_to_reach_plus_10_pct=trades_to_plus_10,
        date_reached_plus_10_pct=date_to_plus_10,
        trades_to_reach_minus_3_pct=trades_to_minus_3,
        date_reached_minus_3_pct=date_to_minus_3,
        avg_trade_pnl=round(avg_trade_pnl, 2),
        avg_win_pnl=round(avg_win_pnl, 2),
        avg_loss_pnl=round(avg_loss_pnl, 2),
        avg_duration_minutes=round(avg_duration_min, 1)
    )


def run_dual_account_simulation(
    btc_candles: List[CandleData],
    eth_candles: List[CandleData],
    btc_sub_1m: Optional[Dict[int, List[CandleData]]],
    eth_sub_1m: Optional[Dict[int, List[CandleData]]],
    case_name: str,          # "Case 1" or "Case 2"
    timeframe: str,
    config: TP_SL_Config,
    initial_balance_each: float = 1000.0,
    leverage: float = 2.0,
    fee_rate: float = 0.0004 # 0.04% total roundtrip fee
) -> Tuple[List[PairTradeCycle], AccountPerformance, AccountPerformance]:
    """
    Simulates the synchronized dual-account reverse trading logic.
    - Case 1: Account A = LONG BTC, Account B = SHORT ETH
    - Case 2: Account A = SHORT BTC, Account B = LONG ETH
    """
    # 1. Align candles by timestamp
    btc_dict = {c.open_time_ms: c for c in btc_candles}
    eth_dict = {c.open_time_ms: c for c in eth_candles}

    common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))
    if not common_times:
        empty_perf_a = compute_account_metrics([], "Account A (BTC)", "BTCUSDT", case_name, timeframe, config, initial_balance_each)
        empty_perf_b = compute_account_metrics([], "Account B (ETH)", "ETHUSDT", case_name, timeframe, config, initial_balance_each)
        return [], empty_perf_a, empty_perf_b

    # Directions per case
    if case_name == "Case 1":
        btc_dir = "LONG"
        eth_dir = "SHORT"
    else:
        btc_dir = "SHORT"
        eth_dir = "LONG"

    balance_a = initial_balance_each
    balance_b = initial_balance_each

    pair_cycles: List[PairTradeCycle] = []
    btc_trades: List[SingleTrade] = []
    eth_trades: List[SingleTrade] = []

    total_candles = len(common_times)
    i = 0
    cycle_counter = 1

    while i < total_candles:
        # Check if any account is bankrupt (<= $10 USDT)
        if balance_a <= 10.0 or balance_b <= 10.0:
            break

        entry_ts = common_times[i]
        c_btc_entry = btc_dict[entry_ts]
        c_eth_entry = eth_dict[entry_ts]

        p_btc_entry = c_btc_entry.open
        p_eth_entry = c_eth_entry.open

        # Both take trades simultaneously with 100% current capital and 2x leverage
        cap_a = balance_a
        cap_b = balance_b

        notional_a = cap_a * leverage
        notional_b = cap_b * leverage

        qty_a = notional_a / p_btc_entry
        qty_b = notional_b / p_eth_entry

        # Calculate TP and SL prices
        if btc_dir == "LONG":
            btc_tp = p_btc_entry * (1.0 + (config.tp_pct / 100.0))
            btc_sl = p_btc_entry * (1.0 - (config.sl_pct / 100.0))
        else:
            btc_tp = p_btc_entry * (1.0 - (config.tp_pct / 100.0))
            btc_sl = p_btc_entry * (1.0 + (config.sl_pct / 100.0))

        if eth_dir == "LONG":
            eth_tp = p_eth_entry * (1.0 + (config.tp_pct / 100.0))
            eth_sl = p_eth_entry * (1.0 - (config.sl_pct / 100.0))
        else:
            eth_tp = p_eth_entry * (1.0 - (config.tp_pct / 100.0))
            eth_sl = p_eth_entry * (1.0 + (config.sl_pct / 100.0))

        btc_exit_idx: Optional[int] = None
        btc_exit_price: Optional[float] = None
        btc_exit_reason: Optional[str] = None

        eth_exit_idx: Optional[int] = None
        eth_exit_price: Optional[float] = None
        eth_exit_reason: Optional[str] = None

        # Step forward candle by candle until BOTH accounts exit
        j = i
        while j < total_candles:
            curr_ts = common_times[j]
            c_btc = btc_dict[curr_ts]
            c_eth = eth_dict[curr_ts]

            # Check BTC if still open
            if btc_exit_idx is None:
                b_res, b_px = evaluate_candle_tp_sl(
                    direction=btc_dir,
                    entry_price=p_btc_entry,
                    tp_price=btc_tp,
                    sl_price=btc_sl,
                    candle=c_btc,
                    sub_1m_map=btc_sub_1m,
                    timeframe=timeframe
                )
                if b_res:
                    btc_exit_idx = j
                    btc_exit_price = b_px
                    btc_exit_reason = b_res

            # Check ETH if still open
            if eth_exit_idx is None:
                e_res, e_px = evaluate_candle_tp_sl(
                    direction=eth_dir,
                    entry_price=p_eth_entry,
                    tp_price=eth_tp,
                    sl_price=eth_sl,
                    candle=c_eth,
                    sub_1m_map=eth_sub_1m,
                    timeframe=timeframe
                )
                if e_res:
                    eth_exit_idx = j
                    eth_exit_price = e_px
                    eth_exit_reason = e_res

            # When BOTH accounts are free, cycle is complete!
            if btc_exit_idx is not None and eth_exit_idx is not None:
                break

            j += 1

        # Handle end of data if positions didn't hit TP/SL before data ran out
        if btc_exit_idx is None:
            btc_exit_idx = total_candles - 1
            btc_exit_price = btc_dict[common_times[btc_exit_idx]].close
            btc_exit_reason = "END_OF_DATA"

        if eth_exit_idx is None:
            eth_exit_idx = total_candles - 1
            eth_exit_price = eth_dict[common_times[eth_exit_idx]].close
            eth_exit_reason = "END_OF_DATA"

        # Calculate PnLs
        # BTC Trade
        if btc_dir == "LONG":
            gross_pnl_a = qty_a * (btc_exit_price - p_btc_entry)
        else:
            gross_pnl_a = qty_a * (p_btc_entry - btc_exit_price)
        fees_a = notional_a * fee_rate
        net_pnl_a = gross_pnl_a - fees_a
        balance_a = max(0.0, balance_a + net_pnl_a)

        # ETH Trade
        if eth_dir == "LONG":
            gross_pnl_b = qty_b * (eth_exit_price - p_eth_entry)
        else:
            gross_pnl_b = qty_b * (p_eth_entry - eth_exit_price)
        fees_b = notional_b * fee_rate
        net_pnl_b = gross_pnl_b - fees_b
        balance_b = max(0.0, balance_b + net_pnl_b)

        btc_exit_ts = common_times[btc_exit_idx]
        eth_exit_ts = common_times[eth_exit_idx]
        free_idx = max(btc_exit_idx, eth_exit_idx)
        free_ts = common_times[free_idx]

        dur_candles_a = (btc_exit_idx - i) + 1
        dur_candles_b = (eth_exit_idx - i) + 1
        dur_sec_a = (btc_dict[btc_exit_ts].close_time_ms - c_btc_entry.open_time_ms) / 1000.0
        dur_sec_b = (eth_dict[eth_exit_ts].close_time_ms - c_eth_entry.open_time_ms) / 1000.0

        trade_a = SingleTrade(
            trade_id=cycle_counter,
            cycle_id=cycle_counter,
            account="Account A (BTC)",
            symbol="BTCUSDT",
            case=case_name,
            direction=btc_dir,
            config_name=config.name,
            tp_pct=config.tp_pct,
            sl_pct=config.sl_pct,
            entry_time_ms=entry_ts,
            entry_time_iso=format_ms(entry_ts),
            entry_price=p_btc_entry,
            exit_time_ms=btc_exit_ts,
            exit_time_iso=format_ms(btc_exit_ts),
            exit_price=btc_exit_price,
            exit_reason=btc_exit_reason,
            duration_candles=dur_candles_a,
            duration_seconds=dur_sec_a,
            initial_trade_capital=cap_a,
            notional_value=notional_a,
            quantity=qty_a,
            gross_pnl=gross_pnl_a,
            fees=fees_a,
            net_pnl=net_pnl_a,
            pnl_pct=(net_pnl_a / cap_a * 100.0) if cap_a > 0 else 0.0,
            balance_after=balance_a,
            is_win=(net_pnl_a > 0.0)
        )
        btc_trades.append(trade_a)

        trade_b = SingleTrade(
            trade_id=cycle_counter,
            cycle_id=cycle_counter,
            account="Account B (ETH)",
            symbol="ETHUSDT",
            case=case_name,
            direction=eth_dir,
            config_name=config.name,
            tp_pct=config.tp_pct,
            sl_pct=config.sl_pct,
            entry_time_ms=entry_ts,
            entry_time_iso=format_ms(entry_ts),
            entry_price=p_eth_entry,
            exit_time_ms=eth_exit_ts,
            exit_time_iso=format_ms(eth_exit_ts),
            exit_price=eth_exit_price,
            exit_reason=eth_exit_reason,
            duration_candles=dur_candles_b,
            duration_seconds=dur_sec_b,
            initial_trade_capital=cap_b,
            notional_value=notional_b,
            quantity=qty_b,
            gross_pnl=gross_pnl_b,
            fees=fees_b,
            net_pnl=net_pnl_b,
            pnl_pct=(net_pnl_b / cap_b * 100.0) if cap_b > 0 else 0.0,
            balance_after=balance_b,
            is_win=(net_pnl_b > 0.0)
        )
        eth_trades.append(trade_b)

        cycle = PairTradeCycle(
            cycle_id=cycle_counter,
            case=case_name,
            timeframe=timeframe,
            config_name=config.name,
            entry_time_iso=format_ms(entry_ts),
            entry_time_ms=entry_ts,
            btc_exit_time_iso=format_ms(btc_exit_ts),
            eth_exit_time_iso=format_ms(eth_exit_ts),
            cycle_exit_time_iso=format_ms(free_ts),
            cycle_exit_time_ms=free_ts,
            holding_candles=(free_idx - i) + 1,
            btc_trade=trade_a,
            eth_trade=trade_b,
            combined_net_pnl=(net_pnl_a + net_pnl_b),
            combined_balance=(balance_a + balance_b),
            pair_win=((net_pnl_a + net_pnl_b) > 0.0)
        )
        pair_cycles.append(cycle)

        cycle_counter += 1
        # Synchronization Rule: As soon as both accounts become free (free_idx),
        # take another trade at the very next candle (free_idx + 1)!
        i = free_idx + 1

    perf_a = compute_account_metrics(
        btc_trades,
        account_name="Account A (BTC)",
        symbol="BTCUSDT",
        case_name=case_name,
        timeframe=timeframe,
        config=config,
        initial_balance=initial_balance_each
    )
    perf_b = compute_account_metrics(
        eth_trades,
        account_name="Account B (ETH)",
        symbol="ETHUSDT",
        case_name=case_name,
        timeframe=timeframe,
        config=config,
        initial_balance=initial_balance_each
    )

    return pair_cycles, perf_a, perf_b
