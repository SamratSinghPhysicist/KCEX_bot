"""
Unit Tests for KCEX Error 510 Rate-Limit Handling, Try-Catch Resilience & WebSocket Feed
"""

import os
import sys
import time
import json
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kcex.client import KCEXClient, KCEXAPIError
from kcex.market import KCEXMarket, ContractInfo
from kcex.feed import KCEXWebSocketFeed
from kcex.engine.models import OrderDirection, TradeSignal, ExecutionConfig
from kcex.engine.strategy import MasterplanStrategy
from kcex.engine.executor import TradeExecutionEngine
from strategies.ml_strategy import MLStrategy


class TestErrorHandlingAndWebsocket(unittest.TestCase):

    def test_client_retry_on_rate_limit_510(self):
        """Verifies that KCEXClient.request retries on code 510 and succeeds on subsequent attempt."""
        client = KCEXClient()

        # Mock opener.open
        # Attempt 1: returns code 510
        # Attempt 2: returns code 0 (success)
        mock_resp_fail = MagicMock()
        mock_resp_fail.read.return_value = json.dumps({
            "code": 510,
            "success": False,
            "msg": "Request frequency limit exceeded for API"
        }).encode("utf-8")
        mock_resp_fail.headers = {}
        mock_resp_fail.__enter__.return_value = mock_resp_fail

        mock_resp_success = MagicMock()
        mock_resp_success.read.return_value = json.dumps({
            "code": 0,
            "success": True,
            "data": {"result": "ok"}
        }).encode("utf-8")
        mock_resp_success.headers = {}
        mock_resp_success.__enter__.return_value = mock_resp_success

        with patch.object(client.opener, "open", side_effect=[mock_resp_fail, mock_resp_success]) as mock_open:
            with patch("time.sleep") as mock_sleep:
                res = client.request(method="GET", endpoint="/test/endpoint", max_retries=2)
                self.assertEqual(res.get("code"), 0)
                self.assertEqual(res.get("data", {}).get("result"), "ok")
                self.assertEqual(mock_open.call_count, 2)
                self.assertTrue(mock_sleep.called)

    def test_client_retry_exhausted_raises_kcex_api_error(self):
        """Verifies that KCEXClient.request raises KCEXAPIError if code 510 persists past max_retries."""
        client = KCEXClient()

        mock_resp_fail = MagicMock()
        mock_resp_fail.read.return_value = json.dumps({
            "code": 510,
            "success": False,
            "msg": "Request frequency limit exceeded for API"
        }).encode("utf-8")
        mock_resp_fail.headers = {}
        mock_resp_fail.__enter__.return_value = mock_resp_fail

        with patch.object(client.opener, "open", return_value=mock_resp_fail) as mock_open:
            with patch("time.sleep"):
                with self.assertRaises(KCEXAPIError) as ctx:
                    client.request(method="GET", endpoint="/test/endpoint", max_retries=1)
                self.assertEqual(ctx.exception.code, 510)
                self.assertEqual(mock_open.call_count, 2)

    def test_market_get_klines_catches_error_510(self):
        """Verifies that KCEXMarket.get_klines catches KCEXAPIError and returns empty list [] without crashing."""
        mock_client = MagicMock()
        mock_client.get_public.side_effect = KCEXAPIError(code=510, message="Request frequency limit exceeded for API")
        market = KCEXMarket(client=mock_client)

        candles = market.get_klines("TRUMP_USDT", interval="Min1", limit=100)
        self.assertEqual(candles, [])

    def test_websocket_feed_handles_push_kline(self):
        """Verifies that KCEXWebSocketFeed parses push.kline frames according to Network_logs_by_codex schema."""
        captured_klines = []

        def on_kline(k):
            captured_klines.append(k)

        feed = KCEXWebSocketFeed(
            symbol="TRUMP_USDT",
            kline_interval="Min1",
            on_kline=on_kline,
            subscribe_kline=True
        )

        sample_frame = json.dumps({
            "channel": "push.kline",
            "symbol": "TRUMP_USDT",
            "data": {
                "interval": "Min1",
                "o": 2.324,
                "c": 2.320,
                "h": 2.325,
                "l": 2.319,
                "a": 1041331.0357,
                "q": 4486304,
                "t": 1788494400000
            }
        })

        feed._handle_message(sample_frame)
        self.assertEqual(len(captured_klines), 1)
        k = captured_klines[0]
        self.assertEqual(k["open"], 2.324)
        self.assertEqual(k["close"], 2.320)
        self.assertEqual(k["high"], 2.325)
        self.assertEqual(k["low"], 2.319)
        self.assertEqual(k["volume"], 4486304)
        self.assertEqual(k["amount"], 1041331.0357)

    def test_ml_strategy_in_memory_websocket_candles_prevents_rest_calls(self):
        """Verifies that MLStrategy uses in-memory candles from WebSocket, avoiding any REST calls to get_klines."""
        mock_market = MagicMock()
        mock_market.get_klines.return_value = []

        strat = MLStrategy(
            market=mock_market,
            symbol="TRUMP_USDT",
            auto_start_feed=False
        )

        # Populate in-memory candles as if received via WebSocket
        now_sec = int(time.time())
        fake_candles = [
            {
                "timestamp": now_sec - (i * 60),
                "open": 2.0, "high": 2.05, "low": 1.95, "close": 2.01,
                "volume": 1000.0, "taker_buy_volume": 500.0
            }
            for i in range(100, 0, -1)
        ]
        mock_market.get_tick_size.return_value = 0.001
        with strat._candles_lock:
            strat.candles = fake_candles

        mock_market.get_klines.reset_mock()

        # Mock model prediction
        strat.model = MagicMock()
        strat.model.is_trained = True
        strat.model.predict_decision.return_value = [{
            "action": "WAIT",
            "confidence": 0.55,
            "prob_buy": 0.20,
            "prob_sell": 0.25,
            "prob_wait": 0.55
        }]

        sig = strat.generate_signal("TRUMP_USDT")
        self.assertIsNone(sig)
        # Verifies that get_klines was NEVER called because in-memory WS candles were used!
        mock_market.get_klines.assert_not_called()

    def test_ml_strategy_handles_rate_limit_gracefully(self):
        """Verifies that MLStrategy.generate_signal handles KCEXAPIError(510) without raising."""
        mock_market = MagicMock()
        mock_market.get_klines.side_effect = KCEXAPIError(code=510, message="Request frequency limit exceeded for API")

        strat = MLStrategy(
            market=mock_market,
            symbol="TRUMP_USDT",
            auto_start_feed=False
        )

        sig = strat.generate_signal("TRUMP_USDT")
        self.assertIsNone(sig)
        # Should engage rate limit backoff
        self.assertGreater(strat._rate_limit_backoff_until, time.time())

    def test_masterplan_strategy_catches_sub_strategy_exception(self):
        """Verifies that MasterplanStrategy.get_signal traps sub-strategy exceptions safely."""
        mock_sub = MagicMock()
        mock_sub.generate_signal.side_effect = RuntimeError("Simulated sub-strategy crash")
        mock_sub.name = "CRASHING_SUB"
        mock_market = MagicMock()

        cfg = ExecutionConfig(symbol="TRUMP_USDT")
        strat = MasterplanStrategy(config=cfg, sub_strategy=mock_sub, market=mock_market)

        # Must return None instead of raising
        sig = strat.get_signal()
        self.assertIsNone(sig)

    def test_executor_loop_survives_api_error(self):
        """Verifies that TradeExecutionEngine.run does NOT shutdown when execute_single_trade_cycle raises KCEXAPIError."""
        mock_market = MagicMock()
        mock_trader = MagicMock()
        mock_contract = ContractInfo(
            symbol="TRUMP_USDT",
            base_coin="TRUMP",
            quote_coin="USDT",
            contract_size=0.1,
            price_unit=0.001,
            volume_unit=1.0,
            price_precision=3,
            volume_precision=0,
            min_volume=1.0,
            max_volume=10000.0,
            min_leverage=1,
            max_leverage=75,
            maintenance_margin_ratio=0.01,
            initial_margin_ratio=0.02,
            maker_fee_rate=0.0,
            taker_fee_rate=0.0001,
            depth_steps=["0.001"],
            raw_data={}
        )
        mock_market.get_contract_detail.return_value = mock_contract
        mock_market.get_inr_rate.return_value = 88.0

        engine = TradeExecutionEngine(
            config=ExecutionConfig(symbol="TRUMP_USDT", max_trades=1),
            market=mock_market,
            trader=mock_trader
        )

        call_count = 0

        def fake_cycle(contract):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First iteration raises rate limit 510
                raise KCEXAPIError(code=510, message="Request frequency limit exceeded for API")
            # Second iteration stops engine
            engine._shutdown_requested = True
            return None

        engine.execute_single_trade_cycle = fake_cycle
        engine.pre_flight_checks = MagicMock(return_value=mock_contract)

        with patch("time.sleep"):
            engine.run()

        # Engine successfully executed cycle 1 (caught 510), engaged backoff, and executed cycle 2
        self.assertEqual(call_count, 2)

    def test_signer_signs_get_requests_with_content_sign_and_time(self):
        """Verifies that KCEXSigner produces Content-Sign and Content-time headers for GET requests."""
        from kcex.signer import KCEXSigner
        from kcex.config import KCEXConfig

        cfg = KCEXConfig(auth_token="dummy_token_abcdef")
        signer = KCEXSigner(cfg)
        headers = signer.sign_request(method="GET", body=None, timestamp_ms=1726000000000)

        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "dummy_token_abcdef")
        self.assertIn("Content-Sign", headers)
        self.assertIn("Content-time", headers)
        self.assertEqual(headers["Content-time"], "1726000000000")
        self.assertIn("User-Device", headers)

    def test_pre_flight_checks_handles_401_gracefully(self):
        """Verifies that pre_flight_checks intercepts 401 Unauthorized cleanly with sys.exit(1)."""
        from kcex.engine.executor import TradeExecutionEngine, ExecutionConfig, EngineMode
        from kcex.market import ContractInfo

        mock_market = MagicMock()
        mock_trader = MagicMock()
        mock_client = MagicMock()
        mock_client.config.is_authenticated = True
        mock_trader.client = mock_client
        mock_market.client = mock_client

        mock_contract = MagicMock()
        mock_contract.price_unit = 0.001
        mock_contract.contract_size = 0.1
        mock_contract.min_volume = 1.0
        mock_contract.maker_fee_rate = 0.0
        mock_contract.taker_fee_rate = 0.0
        mock_market.get_contract_detail.return_value = mock_contract
        mock_market.get_account_tier_fees.return_value = {"makerFee": 0.0, "takerFee": 0.0}
        mock_market.get_inr_rate.return_value = 95.0

        # Simulate 401 on get_usdt_balance
        mock_trader.get_usdt_balance.side_effect = KCEXAPIError(code=401, message="No authority!")

        engine = TradeExecutionEngine(
            config=ExecutionConfig(symbol="TRUMP_USDT", mode=EngineMode.LIVE),
            market=mock_market,
            trader=mock_trader
        )

        with patch("time.sleep"), self.assertRaises(SystemExit) as cm:
            engine.pre_flight_checks()

        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
