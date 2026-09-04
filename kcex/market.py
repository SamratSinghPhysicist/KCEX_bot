"""
KCEX Market Data & Contract Specifications
==========================================
Provides access to public market data, contract specifications, order books,
candles (OHLCV), tickers, trade history, funding rates, and fiat exchange rates.
"""

import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from kcex.client import KCEXClient
from kcex.config import KCEXConfig

logger = logging.getLogger("KCEXMarket")


@dataclass
class ContractInfo:
    """
    Structured metadata for a KCEX futures trading pair.
    """
    symbol: str
    base_coin: str
    quote_coin: str
    contract_size: float           # 'cs': underlying token units per 1 contract (e.g. 0.1 for TRUMP, 10 for DOGE)
    price_unit: float              # 'pu': minimum price tick (e.g. 0.001)
    volume_unit: float             # 'vu': volume step (e.g. 1)
    price_precision: int           # 'ps': decimal places for price (e.g. 3)
    volume_precision: int          # 'vs': decimal places for volume (e.g. 0)
    min_volume: float              # 'minV': minimum order size in contract units (e.g. 1)
    max_volume: float              # 'maxV': maximum order size in contract units
    min_leverage: int              # 'minL': minimum leverage allowed (e.g. 1)
    max_leverage: int              # 'maxL': maximum leverage allowed (e.g. 75, 125, 200)
    maintenance_margin_ratio: float# 'mmr': MMR fraction (e.g. 0.0067)
    initial_margin_ratio: float    # 'imr': IMR fraction (e.g. 0.0133)
    maker_fee_rate: float          # 'mfr': base maker fee (e.g. 0.0)
    taker_fee_rate: float          # 'tfr': base taker fee (e.g. 0.0001)
    depth_steps: List[str]         # 'dsl': available orderbook depth step aggregations
    raw_data: Dict[str, Any]


class KCEXMarket:
    """
    Client for querying KCEX futures market data and symbol details.
    """

    def __init__(self, client: Optional[KCEXClient] = None):
        self.client = client or KCEXClient()
        self._contract_cache: Dict[str, ContractInfo] = {}
        self._all_contracts_loaded = False

    def ping(self) -> bool:
        """
        Tests connectivity to KCEX API.
        Endpoint: GET /fapi/v1/contract/ping
        """
        try:
            res = self.client.get_public(KCEXConfig.ENDPOINT_PING)
            return res.get("success") is True or res.get("code") == 0
        except Exception as e:
            logger.error("Ping failed: %s", e)
            return False

    def get_fiat_exchange_rates(self) -> Dict[str, float]:
        """
        Fetches real-time fiat exchange rates (e.g. USD, INR, EUR, GBP).
        Endpoint: GET https://www.kcex.com/api/platform/common/currency/exchange/rate
        
        Returns:
            Dict[str, float]: Currency code to rate per 1 USD (e.g. {"INR": 94.45, "USD": 1.0, ...}).
        """
        res = self.client.get_public(KCEXConfig.ENDPOINT_EXCHANGE_RATE, is_platform=True)
        data = res.get("data", {})
        rates: Dict[str, float] = {}
        for currency, val in data.items():
            try:
                rates[currency] = float(val)
            except (ValueError, TypeError):
                pass
        return rates

    def get_inr_rate(self) -> float:
        """
        Convenience helper to get the latest USD to INR exchange rate.
        Defaults to observed fallback ~94.45 if endpoint is temporarily unreachable.
        """
        try:
            rates = self.get_fiat_exchange_rates()
            if "INR" in rates:
                return rates["INR"]
        except Exception as e:
            logger.warning("Failed to fetch fresh INR rate, using fallback 94.45: %s", e)
        return 94.45

    def get_contracts(self, force_refresh: bool = False) -> Dict[str, ContractInfo]:
        """
        Retrieves contract metadata for all available futures trading pairs.
        Endpoint: GET /fapi/v1/contract/detailV2?client=web
        
        Returns:
            Dict[str, ContractInfo]: Dictionary mapping symbol name to ContractInfo object.
        """
        if self._all_contracts_loaded and not force_refresh:
            return self._contract_cache

        params = {"client": "web"}
        res = self.client.get_public(KCEXConfig.ENDPOINT_CONTRACT_DETAIL, params=params)
        raw_list = res.get("data", [])

        contracts: Dict[str, ContractInfo] = {}
        for item in raw_list:
            symbol = item.get("symbol", "")
            if not symbol:
                continue

            info = ContractInfo(
                symbol=symbol,
                base_coin=item.get("bc", ""),
                quote_coin=item.get("qc", ""),
                contract_size=float(item.get("cs", 1.0)),
                price_unit=float(item.get("pu", 0.001)),
                volume_unit=float(item.get("vu", 1.0)),
                price_precision=int(item.get("ps", 2)),
                volume_precision=int(item.get("vs", 0)),
                min_volume=float(item.get("minV", 1.0)),
                max_volume=float(item.get("maxV", 1000000.0)),
                min_leverage=int(item.get("minL", 1)),
                max_leverage=int(item.get("maxL", 100)),
                maintenance_margin_ratio=float(item.get("mmr", 0.005)),
                initial_margin_ratio=float(item.get("imr", 0.01)),
                maker_fee_rate=float(item.get("mfr", 0.0)),
                taker_fee_rate=float(item.get("tfr", 0.0001)),
                depth_steps=item.get("dsl", []),
                raw_data=item
            )
            contracts[symbol] = info

        self._contract_cache.update(contracts)
        self._all_contracts_loaded = True
        return self._contract_cache

    def get_symbols(self) -> List[str]:
        """Returns sorted list of all supported contract symbols."""
        contracts = self.get_contracts()
        return sorted(list(contracts.keys()))

    def get_contract_detail(self, symbol: str) -> ContractInfo:
        """
        Fetches detailed specifications for a specific trading pair.
        Endpoint: GET /fapi/v1/contract/detailV2?client=web&symbol={symbol}
        
        Args:
            symbol (str): e.g. "TRUMP_USDT", "DOGE_USDT", "BTC_USDT".
        """
        symbol_upper = symbol.upper()
        if symbol_upper in self._contract_cache:
            return self._contract_cache[symbol_upper]

        params = {"client": "web", "symbol": symbol_upper}
        res = self.client.get_public(KCEXConfig.ENDPOINT_CONTRACT_DETAIL, params=params)
        raw_list = res.get("data", [])
        if not raw_list:
            raise ValueError(f"Trading pair '{symbol}' not found on KCEX.")

        item = raw_list[0]
        info = ContractInfo(
            symbol=item.get("symbol", symbol_upper),
            base_coin=item.get("bc", ""),
            quote_coin=item.get("qc", ""),
            contract_size=float(item.get("cs", 1.0)),
            price_unit=float(item.get("pu", 0.001)),
            volume_unit=float(item.get("vu", 1.0)),
            price_precision=int(item.get("ps", 2)),
            volume_precision=int(item.get("vs", 0)),
            min_volume=float(item.get("minV", 1.0)),
            max_volume=float(item.get("maxV", 1000000.0)),
            min_leverage=int(item.get("minL", 1)),
            max_leverage=int(item.get("maxL", 100)),
            maintenance_margin_ratio=float(item.get("mmr", 0.005)),
            initial_margin_ratio=float(item.get("imr", 0.01)),
            maker_fee_rate=float(item.get("mfr", 0.0)),
            taker_fee_rate=float(item.get("tfr", 0.0001)),
            depth_steps=item.get("dsl", []),
            raw_data=item
        )
        self._contract_cache[symbol_upper] = info
        return info

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches the 24-hour ticker snapshot for a symbol.
        Endpoint: GET /fapi/v1/contract/ticker?symbol={symbol}
        
        Returns:
            Dict containing: lastPrice, fairPrice (mark price), indexPrice,
            bid1, ask1, volume24, amount24, fundingRate, high24Price, lower24Price.
        """
        params = {"symbol": symbol.upper()}
        res = self.client.get_public(KCEXConfig.ENDPOINT_CONTRACT_TICKER, params=params)
        return res.get("data", {})

    def get_order_book(self, symbol: str, step: Optional[str] = None) -> Dict[str, List[List[float]]]:
        """
        Fetches the L2 order book (depth) snapshot.
        Endpoint: GET /fapi/v1/contract/depth_step/{symbol}?step={step}
        
        Args:
            symbol (str): Trading pair, e.g. "TRUMP_USDT".
            step (str, optional): Aggregation price step. If None, uses smallest available step.
            
        Returns:
            Dict with "asks": [[price, volume, count], ...] and "bids": [[price, volume, count], ...]
        """
        symbol_upper = symbol.upper()
        if not step:
            # Look up available depth steps from contract detail
            try:
                contract = self.get_contract_detail(symbol_upper)
                step = contract.depth_steps[0] if contract.depth_steps else "0.001"
            except Exception:
                step = "0.001"

        endpoint = KCEXConfig.ENDPOINT_CONTRACT_DEPTH.format(symbol=symbol_upper)
        params = {"step": step}
        res = self.client.get_public(endpoint, params=params)
        data = res.get("data", {})
        return {
            "asks": data.get("asks", []),
            "bids": data.get("bids", []),
            "version": data.get("version", 0)
        }

    def get_klines(
        self,
        symbol: str,
        interval: str = "Min1",
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetches OHLCV candlestick candles.
        Endpoint: GET /fapi/v1/contract/kline/{symbol}?interval={interval}&start={start}&end={end}
        
        Args:
            symbol (str): Trading pair symbol.
            interval (str): 'Min1', 'Min5', 'Min15', 'Min30', 'Min60', 'Hour4', 'Day1', etc.
            start_time (int, optional): Start timestamp in seconds.
            end_time (int, optional): End timestamp in seconds.
            limit (int): Approximate count of bars to fetch if timestamps are omitted.

        Returns:
            List[Dict]: Standardized candle records with timestamp, open, high, low, close, volume.
        """
        now = int(time.time())
        if end_time is None:
            end_time = now
        if start_time is None:
            # Estimate interval span in seconds
            seconds_map = {
                "Min1": 60, "Min5": 300, "Min15": 900, "Min30": 1800,
                "Min60": 3600, "Hour4": 14400, "Day1": 86400
            }
            span = seconds_map.get(interval, 60) * limit
            start_time = end_time - span

        endpoint = KCEXConfig.ENDPOINT_CONTRACT_KLINES.format(symbol=symbol.upper())
        params = {
            "interval": interval,
            "start": start_time,
            "end": end_time
        }
        res = self.client.get_public(endpoint, params=params)
        data = res.get("data", {})

        # KCEX returns parallel arrays: 'time', 'open', 'close', 'high', 'low', 'vol', 'amount'
        times = data.get("time", [])
        opens = data.get("open", [])
        highs = data.get("high", [])
        lows = data.get("low", [])
        closes = data.get("close", [])
        vols = data.get("vol", [])
        amounts = data.get("amount", [])

        candles: List[Dict[str, Any]] = []
        for i in range(len(times)):
            candles.append({
                "timestamp": times[i],
                "open": opens[i] if i < len(opens) else 0.0,
                "high": highs[i] if i < len(highs) else 0.0,
                "low": lows[i] if i < len(lows) else 0.0,
                "close": closes[i] if i < len(closes) else 0.0,
                "volume": vols[i] if i < len(vols) else 0.0,
                "amount": amounts[i] if i < len(amounts) else 0.0
            })

        return candles

    def get_recent_trades(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetches recently executed public trades.
        Endpoint: GET /fapi/v1/contract/deals/{symbol}
        
        Returns:
            List of trade dictionaries with price ('p'), volume ('v'), side ('T': 1=Buy, 2=Sell), time ('t').
        """
        endpoint = KCEXConfig.ENDPOINT_CONTRACT_DEALS.format(symbol=symbol.upper())
        res = self.client.get_public(endpoint)
        return res.get("data", [])

    def get_funding_rate(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches the current funding rate and settlement schedule.
        Endpoint: GET /fapi/v1/contract/funding_rate/{symbol}
        """
        endpoint = KCEXConfig.ENDPOINT_FUNDING_RATE.format(symbol=symbol.upper())
        res = self.client.get_public(endpoint)
        return res.get("data", {})

    def get_account_tier_fees(self, symbol: str) -> Dict[str, float]:
        """
        Queries the user's effective maker and taker fee rates for a specific pair.
        Endpoint: GET /fapi/v1/private/account/tiered_fee_rate?symbol={symbol}
        (Requires authenticated session).
        
        Returns:
            Dict with 'makerFee' and 'takerFee'.
        """
        params = {"symbol": symbol.upper()}
        res = self.client.get_private(KCEXConfig.ENDPOINT_TIERED_FEE_RATE, params=params)
        data = res.get("data", {})
        return {
            "makerFee": float(data.get("makerFee", 0.0)),
            "takerFee": float(data.get("takerFee", 0.0)),
            "level": data.get("level", 0)
        }
