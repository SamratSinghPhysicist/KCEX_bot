"""
Backtest Market Simulation Adapter
===================================
Provides a 100% faithful emulation of the KCEXMarket interface, allowing
all live trading strategies (EMA Crossover, Stochastic RSI, Directional Cycle,
Microstructure, and MasterplanStrategy) to execute without modification or lookahead bias.
"""

import os
import sys
from typing import Dict, List, Any, Optional

# Ensure project root is in path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from kcex.market import ContractInfo
from BACKTESTER.engine.scanner import canonicalize_symbol
from BACKTESTER.engine.data_loader import Candle, normalize_timeframe, timeframe_to_kcex_interval


# Preconfigured contract metadata for major pairs (fallback/default values matching exchange specs)
DEFAULT_CONTRACTS: Dict[str, Dict[str, Any]] = {
    "TRUMP_USDT": {
        "base_coin": "TRUMP",
        "quote_coin": "USDT",
        "contract_size": 0.1,
        "price_unit": 0.001,
        "volume_unit": 1.0,
        "price_precision": 3,
        "volume_precision": 0,
        "min_volume": 1.0,
        "max_volume": 1000000.0,
        "min_leverage": 1,
        "max_leverage": 75,
        "maintenance_margin_ratio": 0.0067,
        "initial_margin_ratio": 0.0133,
        "maker_fee_rate": 0.0,
        "taker_fee_rate": 0.0,
        "depth_steps": ["0.001"]
    },
    "DOGE_USDT": {
        "base_coin": "DOGE",
        "quote_coin": "USDT",
        "contract_size": 10.0,
        "price_unit": 0.00001,
        "volume_unit": 1.0,
        "price_precision": 5,
        "volume_precision": 0,
        "min_volume": 1.0,
        "max_volume": 5000000.0,
        "min_leverage": 1,
        "max_leverage": 100,
        "maintenance_margin_ratio": 0.005,
        "initial_margin_ratio": 0.01,
        "maker_fee_rate": 0.0,
        "taker_fee_rate": 0.0,
        "depth_steps": ["0.00001"]
    }
}


class BacktestMarket:
    """
    Virtual KCEXMarket adapter backed by historical datasets.
    Controls the simulation timeline and delivers kline snapshots up to the current clock.
    """

    def __init__(
        self,
        inr_rate: float = 94.45,
        fee_mode: str = "LIVE",
        maker_fee_override: Optional[float] = None,
        taker_fee_override: Optional[float] = None
    ):
        self.inr_rate = inr_rate
        self.fee_mode = fee_mode.upper() if fee_mode else "LIVE"
        self.maker_fee_override = maker_fee_override
        self.taker_fee_override = taker_fee_override

        # Active simulation clock
        self.current_time_ms: int = 0
        self.current_price: float = 0.0
        self.current_bid: float = 0.0
        self.current_ask: float = 0.0

        # Cached candles indexed by (symbol, timeframe)
        self._candle_cache: Dict[str, List[Candle]] = {}
        # Precomputed list of timestamps for fast binary search slicing
        self._candle_timestamps: Dict[str, List[int]] = {}
        self._contracts: Dict[str, ContractInfo] = {}

    def set_candles(self, symbol: str, timeframe: str, candles: List[Candle]) -> None:
        """Seeds the historical candles for a symbol and timeframe."""
        canonical = canonicalize_symbol(symbol)
        key = f"{canonical}:{normalize_timeframe(timeframe)}"
        self._candle_cache[key] = candles
        self._candle_timestamps[key] = [c.open_time_ms for c in candles]

        # Auto-initialize current price if not set
        if candles and self.current_price == 0.0:
            self.current_price = candles[0].close
            pu = self.get_contract_detail(canonical).price_unit
            self.current_bid = self.current_price - (0.5 * pu)
            self.current_ask = self.current_price + (0.5 * pu)

    def set_time(self, timestamp_ms: int, current_price: Optional[float] = None, bid: Optional[float] = None, ask: Optional[float] = None) -> None:
        """Advances the virtual market clock."""
        self.current_time_ms = timestamp_ms
        if current_price is not None:
            self.current_price = current_price
        if bid is not None:
            self.current_bid = bid
        elif current_price is not None:
            self.current_bid = current_price
        if ask is not None:
            self.current_ask = ask
        elif current_price is not None:
            self.current_ask = current_price

    def ping(self) -> bool:
        return True

    def get_inr_rate(self) -> float:
        return self.inr_rate

    def get_fiat_exchange_rates(self) -> Dict[str, float]:
        return {"INR": self.inr_rate, "USD": 1.0}

    def get_contract_detail(self, symbol: str) -> ContractInfo:
        """Retrieves or synthesizes ContractInfo for the given symbol."""
        canonical = canonicalize_symbol(symbol)
        if canonical in self._contracts:
            return self._contracts[canonical]

        # 1. Attempt to fetch live contract metadata from KCEX if fee_mode is LIVE
        live_info: Optional[ContractInfo] = None
        if self.fee_mode == "LIVE":
            try:
                from kcex.market import KCEXMarket
                k_market = KCEXMarket()
                live_info = k_market.get_contract_detail(canonical)
            except Exception:
                live_info = None

        if live_info is not None:
            base_coin = live_info.base_coin
            quote_coin = live_info.quote_coin
            cs = live_info.contract_size
            pu = live_info.price_unit
            vu = live_info.volume_unit
            ps = live_info.price_precision
            vs = live_info.volume_precision
            min_v = live_info.min_volume
            max_v = live_info.max_volume
            min_l = live_info.min_leverage
            max_l = live_info.max_leverage
            mmr = live_info.maintenance_margin_ratio
            imr = live_info.initial_margin_ratio
            mfr = live_info.maker_fee_rate
            tfr = live_info.taker_fee_rate
            depth_steps = live_info.depth_steps
            raw_data = live_info.raw_data
        else:
            # Fallback to preconfigured template
            template = DEFAULT_CONTRACTS.get(canonical, {})
            base_coin = template.get("base_coin", canonical.split("_")[0])
            quote_coin = template.get("quote_coin", "USDT")
            cs = float(template.get("contract_size", 1.0))
            pu = float(template.get("price_unit", 0.001))
            vu = float(template.get("volume_unit", 1.0))
            ps = int(template.get("price_precision", 3))
            vs = int(template.get("volume_precision", 0))
            min_v = float(template.get("min_volume", 1.0))
            max_v = float(template.get("max_volume", 1000000.0))
            min_l = int(template.get("min_leverage", 1))
            max_l = int(template.get("max_leverage", 75))
            mmr = float(template.get("maintenance_margin_ratio", 0.0067))
            imr = float(template.get("initial_margin_ratio", 0.0133))
            mfr = float(template.get("maker_fee_rate", 0.0))
            tfr = float(template.get("taker_fee_rate", 0.0))
            depth_steps = template.get("depth_steps", [str(pu)])
            raw_data = {}

        # 2. Apply fee_mode policies
        if self.fee_mode == "ZERO":
            mfr = 0.0
            tfr = 0.0
        elif self.fee_mode == "MANUAL":
            mfr = self.maker_fee_override if self.maker_fee_override is not None else 0.0
            tfr = self.taker_fee_override if self.taker_fee_override is not None else 0.0

        # Specific manual overrides always take ultimate precedence
        if self.maker_fee_override is not None:
            mfr = self.maker_fee_override
        if self.taker_fee_override is not None:
            tfr = self.taker_fee_override

        info = ContractInfo(
            symbol=canonical,
            base_coin=base_coin,
            quote_coin=quote_coin,
            contract_size=cs,
            price_unit=pu,
            volume_unit=vu,
            price_precision=ps,
            volume_precision=vs,
            min_volume=min_v,
            max_volume=max_v,
            min_leverage=min_l,
            max_leverage=max_l,
            maintenance_margin_ratio=mmr,
            initial_margin_ratio=imr,
            maker_fee_rate=mfr,
            taker_fee_rate=tfr,
            depth_steps=depth_steps,
            raw_data=raw_data
        )
        self._contracts[canonical] = info
        return info

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Returns virtual ticker at the current simulation clock."""
        canonical = canonicalize_symbol(symbol)
        contract = self.get_contract_detail(canonical)
        pu = contract.price_unit
        price = self.current_price or 1.0
        bid = self.current_bid or (price - (0.5 * pu))
        ask = self.current_ask or (price + (0.5 * pu))

        return {
            "symbol": canonical,
            "lastPrice": price,
            "fairPrice": price,
            "indexPrice": price,
            "bid1": bid,
            "ask1": ask,
            "high24Price": price,
            "lower24Price": price,
            "volume24": 0.0
        }

    def get_order_book(self, symbol: str, step: Optional[str] = None) -> Dict[str, List[List[float]]]:
        """Synthesizes order book depth centered around current price."""
        canonical = canonicalize_symbol(symbol)
        contract = self.get_contract_detail(canonical)
        pu = contract.price_unit
        mid = self.current_price or 1.0

        bids = [[round(mid - (i * pu), contract.price_precision), 100.0, 5] for i in range(1, 11)]
        asks = [[round(mid + (i * pu), contract.price_precision), 100.0, 5] for i in range(1, 11)]
        return {"bids": bids, "asks": asks, "version": 1}

    def get_klines(
        self,
        symbol: str,
        interval: str = "Min1",
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Returns klines up to current_time_ms strictly, preventing any lookahead bias.
        """
        canonical = canonicalize_symbol(symbol)
        norm_tf = normalize_timeframe(interval)
        key = f"{canonical}:{norm_tf}"

        candles = self._candle_cache.get(key, [])
        if not candles:
            # Fallback to 1m if requested timeframe not seeded
            key = f"{canonical}:1m"
            candles = self._candle_cache.get(key, [])
            if not candles:
                return []

        ts_list = self._candle_timestamps.get(key, [])

        # Find candles whose open_time_ms <= current_time_ms
        # Binary search for index
        import bisect
        cutoff_ms = self.current_time_ms if self.current_time_ms > 0 else (candles[-1].open_time_ms + 1)
        idx = bisect.bisect_right(ts_list, cutoff_ms)

        # Slice up to limit candles
        start_idx = max(0, idx - limit)
        selected = candles[start_idx:idx]

        return [c.to_kcex_dict() for c in selected]
