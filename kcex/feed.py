"""
KCEX Real-Time WebSocket Data Feed
==================================
Manages high-throughput, low-latency WebSocket subscriptions to KCEX Futures
market data channels:
- `push.depth.step`: L2 order book depth levels (bids & asks)
- `push.deal`: Real-time public trade prints (price, volume, aggressor side)

Runs inside a dedicated background daemon thread with automatic reconnection,
keepalive heartbeat pings, and thread-safe callbacks into the strategy engine.
"""

import asyncio
import gzip
import json
import logging
import threading
import time
from typing import Callable, List, Optional, Tuple, Any, Dict

import websockets

logger = logging.getLogger("KCEXFeed")


class KCEXWebSocketFeed:
    """
    High-performance WebSocket client streaming live depth and deals
    from wss://www.kcex.com/fapi/edge?platform=web.
    """

    DEFAULT_WS_URL = "wss://www.kcex.com/fapi/edge?platform=web"
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    )

    def __init__(
        self,
        symbol: str,
        depth_step: str = "0.001",
        ws_url: Optional[str] = None,
        on_depth: Optional[Callable[[List[Tuple[float, float]], List[Tuple[float, float]], float], None]] = None,
        on_deal: Optional[Callable[[float, float, str, float], None]] = None,
        ping_interval_s: float = 5.0
    ):
        self.symbol = symbol.upper()
        self.depth_step = str(depth_step)
        self.ws_url = ws_url or self.DEFAULT_WS_URL
        self.on_depth = on_depth
        self.on_deal = on_deal
        self.ping_interval_s = ping_interval_s

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connected = False
        self._last_msg_ts = 0.0
        self._depth_count = 0
        self._deal_count = 0

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "connected": self._connected,
            "depth_frames": self._depth_count,
            "deal_frames": self._deal_count,
            "last_msg_age_s": round(time.time() - self._last_msg_ts, 2) if self._last_msg_ts else None
        }

    def start(self) -> None:
        """Starts the WebSocket background listener thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._run_thread,
            name=f"KCEXFeed-{self.symbol}",
            daemon=True
        )
        self._thread.start()
        logger.info("KCEX WebSocket Feed thread started for %s", self.symbol)

    def stop(self) -> None:
        """Stops the WebSocket background listener thread."""
        self._running = False
        self._connected = False
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("KCEX WebSocket Feed stopped for %s", self.symbol)

    def _run_thread(self) -> None:
        """Entry point for background thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._connection_supervisor())
        except Exception as e:
            logger.debug("WebSocket loop terminated: %s", e)
        finally:
            try:
                pending = asyncio.all_tasks(self._loop)
                for task in pending:
                    task.cancel()
                if pending and not self._loop.is_closed():
                    self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass
            self._loop.close()

    async def _connection_supervisor(self) -> None:
        """Supervises connection lifecycle with backoff."""
        headers = {
            "User-Agent": self.DEFAULT_USER_AGENT,
            "Origin": "https://www.kcex.com",
        }

        backoff = 1.0
        while self._running:
            try:
                logger.info("Connecting to KCEX WebSocket: %s...", self.ws_url)
                async with websockets.connect(
                    self.ws_url,
                    additional_headers=headers,
                    open_timeout=10.0,
                    ping_interval=None  # We use application-level JSON ping
                ) as ws:
                    self._connected = True
                    backoff = 1.0
                    logger.info("WebSocket connected. Subscribing to %s depth and deal streams...", self.symbol)

                    # 1. Subscribe to deals (uncompressed raw JSON text)
                    deal_sub = {
                        "method": "sub.deal",
                        "param": {"symbol": self.symbol, "compress": False}
                    }
                    await ws.send(json.dumps(deal_sub))

                    # 2. Subscribe to depth step
                    depth_sub = {
                        "method": "sub.depth.step",
                        "param": {"symbol": self.symbol, "step": self.depth_step}
                    }
                    await ws.send(json.dumps(depth_sub))

                    # Spawn heartbeat pinger
                    pinger_task = asyncio.create_task(self._pinger(ws))

                    try:
                        # Message consumption loop
                        while self._running:
                            msg = await ws.recv()
                            self._handle_message(msg)
                    finally:
                        pinger_task.cancel()
                        await asyncio.gather(pinger_task, return_exceptions=True)

            except asyncio.CancelledError:
                break
            except Exception as e:
                self._connected = False
                if not self._running:
                    break
                logger.warning("WebSocket error (%s): %s. Reconnecting in %.1fs...", type(e).__name__, e, backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2.0, 15.0)

        self._connected = False

    async def _pinger(self, ws) -> None:
        """Sends periodic application heartbeat pings."""
        try:
            while self._running:
                await asyncio.sleep(self.ping_interval_s)
                if ws and not ws.closed:
                    await ws.send(json.dumps({"method": "ping"}))
        except asyncio.CancelledError:
            pass

    def _handle_message(self, raw_msg: Any) -> None:
        """Parses incoming WebSocket frame."""
        now = time.time()
        self._last_msg_ts = now

        # Decompress if binary gzip frame
        if isinstance(raw_msg, (bytes, bytearray)):
            try:
                text = gzip.decompress(raw_msg).decode("utf-8")
            except Exception:
                try:
                    text = raw_msg.decode("utf-8")
                except Exception:
                    return
        else:
            text = raw_msg

        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return

        channel = payload.get("channel", "")

        # 1. Deals / Tape stream
        if channel == "push.deal":
            self._deal_count += 1
            data = payload.get("data", {})
            trades = data if isinstance(data, list) else [data]
            for tr in trades:
                if not isinstance(tr, dict):
                    continue
                try:
                    price = float(tr.get("p", 0.0))
                    volume = float(tr.get("v", 0.0))
                    # T: 1 = Buyer Market Order ("buy"), 2 = Seller Market Order ("sell")
                    side_code = tr.get("T", 1)
                    side_str = "buy" if side_code == 1 else "sell"
                    t_ms = tr.get("t") or payload.get("ts") or (now * 1000)
                    trade_ts = float(t_ms) / 1000.0

                    if self.on_deal and price > 0:
                        self.on_deal(price, volume, side_str, trade_ts)
                except (ValueError, TypeError):
                    continue

        # 2. Depth / Order Book stream
        elif channel == "push.depth.step":
            self._depth_count += 1
            data = payload.get("data", {})
            raw_bids = data.get("bids", [])
            raw_asks = data.get("asks", [])
            ct_ms = data.get("ct") or payload.get("ts") or (now * 1000)
            depth_ts = float(ct_ms) / 1000.0

            bids: List[Tuple[float, float]] = []
            for b in raw_bids:
                try:
                    bids.append((float(b[0]), float(b[1])))
                except (IndexError, ValueError, TypeError):
                    continue

            asks: List[Tuple[float, float]] = []
            for a in raw_asks:
                try:
                    asks.append((float(a[0]), float(a[1])))
                except (IndexError, ValueError, TypeError):
                    continue

            if self.on_depth and (bids or asks):
                self.on_depth(bids, asks, depth_ts)
