import pytest
from unittest.mock import MagicMock, patch
import time

from kcex.engine.executor import TradeExecutionEngine
from kcex.engine.models import (
    ExecutionConfig,
    OrderDirection,
    TradeSignal,
    ExitReason,
    EngineMode
)
from kcex.market import ContractInfo


@pytest.fixture
def mock_engine():
    mock_client = MagicMock()
    config = ExecutionConfig(
        symbol="TRUMP_USDT",
        poll_interval_seconds=0.001,
        mode=EngineMode.LIVE,
        strategy_mode="ORDER_BLOCK_DEMAND",
        partial_tp_enabled=True,
        breakeven_buffer_ticks=1,
        smc_1x_exit_mode="1TO1_TP",
        tp_ticks=40,
        sl_ticks=20
    )
    mock_strategy = MagicMock()
    mock_strategy.is_better_than_min_profit.return_value = False
    mock_strategy.is_worse_than_stop_loss.return_value = False
    mock_market = MagicMock()
    mock_trader = MagicMock()

    engine = TradeExecutionEngine(
        config=config,
        client=mock_client,
        market=mock_market,
        trader=mock_trader,
        strategy=mock_strategy
    )

    # Default contract info for TRUMP_USDT (precision 4, unit 0.0001)
    contract = ContractInfo(
        symbol="TRUMP_USDT",
        base_coin="TRUMP",
        quote_coin="USDT",
        contract_size=1.0,
        price_unit=0.0001,
        volume_unit=1.0,
        price_precision=4,
        volume_precision=0,
        min_volume=1.0,
        max_volume=100000.0,
        min_leverage=1,
        max_leverage=25,
        maintenance_margin_ratio=0.0067,
        initial_margin_ratio=0.0133,
        maker_fee_rate=0.0002,
        taker_fee_rate=0.0006,
        depth_steps=["step0"],
        raw_data={}
    )
    engine.market.get_contract_detail.return_value = contract
    return engine


def test_pre_placed_tp1_order_multi_contract(mock_engine):
    """
    Test multi-contract SMC trade (vol_contracts=2):
    1. Pre-places limit order for 50% (1 contract) at 1:1 TP (2.5200).
    2. When holdVol drops from 2 to 1 (limit filled on exchange book),
       detects fill, updates server-side SL to Breakeven (+1 tick = 2.5001),
       and lets remaining 1 contract run to 1:2 TP (2.5400).
    """
    signal = TradeSignal(
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemandStrategy",
        metadata={
            "strategy_mode": "ORDER_BLOCK_DEMAND",
            "target_1to1_price": 2.5200,
            "target_1to2_price": 2.5400,
            "partial_tp_enabled": True,
            "breakeven_buffer_ticks": 1
        }
    )

    mock_engine.trader.close_position_limit.return_value = {
        "code": 0,
        "data": {"orderId": "LIMIT_TP1_999"}
    }

    # Simulate ticker and open_positions sequence in _monitor_live_position:
    # Call 1: Position has 2 contracts, price is 2.5050
    # Call 2: Position has 1 contract (limit order filled!), price is 2.5210
    # Call 3: Price hits 1:2 TP (2.5400)
    mock_engine.market.get_ticker.side_effect = [
        {"lastPrice": 2.5050, "bid1": 2.5050, "ask1": 2.5051},
        {"lastPrice": 2.5210, "bid1": 2.5210, "ask1": 2.5211},
        {"lastPrice": 2.5400, "bid1": 2.5400, "ask1": 2.5401},
    ]

    mock_engine.trader.get_open_positions.side_effect = [
        [{"positionId": 1001, "holdVol": 2}],
        [{"positionId": 1001, "holdVol": 1}],
        [{"positionId": 1001, "holdVol": 1}],
    ]

    mock_engine.strategy.is_better_than_min_profit.side_effect = [
        False,  # call 1
        False,  # call 2
        True,   # call 3 (reached 1:2 TP)
    ]
    mock_engine.trader.close_position.return_value = {
        "code": 0,
        "data": {"orderId": "FINAL_TP2_CLOSE"}
    }
    mock_engine.trader.get_open_stop_orders.return_value = [
        {"positionId": 1001, "symbol": "TRUMP_USDT", "stopLossPrice": 2.5001, "takeProfitPrice": 2.5400}
    ]

    exit_price, exit_reason, close_oid = mock_engine._monitor_live_position(
        symbol="TRUMP_USDT",
        position_id=1001,
        direction=OrderDirection.LONG,
        vol_contracts=2,
        leverage=10,
        exact_tp=2.5400,
        exact_sl=2.4800,
        precision=4,
        entry_price=2.5000,
        open_time=time.time(),
        signal=signal,
        pre_placed_tp1_order_id="LIMIT_TP1_999",
        tp1_contracts=1
    )

    # Verify server-side SL was updated to Breakeven (+1 tick = 2.5001)
    mock_engine.trader.set_position_tp_sl.assert_called_once_with(
        symbol="TRUMP_USDT",
        position_id=1001,
        take_profit_price=2.5400,
        stop_loss_price=2.5001
    )

    # Verify final exit at 1:2 TP
    assert exit_reason == ExitReason.MIN_PROFIT_TP_HIT
    assert exit_price == 2.5400
    assert close_oid == "FINAL_TP2_CLOSE"


def test_pre_placed_tp1_order_single_contract_full_close(mock_engine):
    """
    Test 1-contract SMC trade:
    When position has only 1 contract, 0.5 cannot be closed on KCEX.
    The bot places 1-contract limit order at 1:1 TP beforehand.
    When it fills on KCEX, position is closed (holdVol drops to 0),
    and the engine exits cleanly at 1:1 with MIN_PROFIT_TP_HIT.
    """
    signal = TradeSignal(
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemandStrategy",
        metadata={
            "strategy_mode": "ORDER_BLOCK_DEMAND",
            "target_1to1_price": 2.5200,
            "target_1to2_price": 2.5400,
            "partial_tp_enabled": True,
            "breakeven_buffer_ticks": 1
        }
    )

    # Call 1: Position has 1 contract open, price is 2.5100
    # Call 2: Position is closed on KCEX (pre-placed limit filled at 2.5200)
    mock_engine.market.get_ticker.side_effect = [
        {"lastPrice": 2.5100, "bid1": 2.5100, "ask1": 2.5101},
        {"lastPrice": 2.5200, "bid1": 2.5200, "ask1": 2.5201},
    ]

    mock_engine.trader.get_open_positions.side_effect = [
        [{"positionId": 1002, "holdVol": 1}],
        [],  # Position closed on exchange
    ]

    exit_price, exit_reason, close_oid = mock_engine._monitor_live_position(
        symbol="TRUMP_USDT",
        position_id=1002,
        direction=OrderDirection.LONG,
        vol_contracts=1,
        leverage=10,
        exact_tp=2.5400,
        exact_sl=2.4800,
        precision=4,
        entry_price=2.5000,
        open_time=time.time(),
        signal=signal,
        pre_placed_tp1_order_id="LIMIT_TP1_SINGLE_123",
        tp1_contracts=1
    )

    assert exit_reason == ExitReason.MIN_PROFIT_TP_HIT
    assert exit_price == 2.5200
    assert close_oid == "LIMIT_TP1_SINGLE_123"


def test_stopout_cancels_pre_placed_tp1_order(mock_engine):
    """
    Test that if position stops out before reaching 1:1,
    the pending pre-placed limit order is automatically cancelled,
    and no false TP is reported.
    """
    signal = TradeSignal(
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemandStrategy",
        metadata={
            "strategy_mode": "ORDER_BLOCK_DEMAND",
            "target_1to1_price": 2.5200,
            "target_1to2_price": 2.5400,
            "partial_tp_enabled": True,
            "breakeven_buffer_ticks": 1
        }
    )

    # Call 1: Position has 2 contracts, price moves towards SL (2.4850)
    # Call 2: Position stopped out on KCEX, price is 2.4790
    mock_engine.market.get_ticker.side_effect = [
        {"lastPrice": 2.4850, "bid1": 2.4850, "ask1": 2.4851},
        {"lastPrice": 2.4790, "bid1": 2.4790, "ask1": 2.4791},
    ]

    mock_engine.trader.get_open_positions.side_effect = [
        [{"positionId": 1003, "holdVol": 2}],
        [],  # Closed via SL on KCEX
    ]

    exit_price, exit_reason, close_oid = mock_engine._monitor_live_position(
        symbol="TRUMP_USDT",
        position_id=1003,
        direction=OrderDirection.LONG,
        vol_contracts=2,
        leverage=10,
        exact_tp=2.5400,
        exact_sl=2.4800,
        precision=4,
        entry_price=2.5000,
        open_time=time.time(),
        signal=signal,
        pre_placed_tp1_order_id="LIMIT_TP1_TO_CANCEL",
        tp1_contracts=1
    )

    # Verify cancel_order was called on the pre-placed limit order
    mock_engine.trader.cancel_order.assert_called_once_with("LIMIT_TP1_TO_CANCEL")
    # Verify exit is not marked as TP
    assert exit_reason != ExitReason.MIN_PROFIT_TP_HIT


def test_shutdown_cancels_pre_placed_tp1_order(mock_engine):
    """
    Test that if shutdown is requested during a live trade,
    the pending pre-placed limit order is cancelled before market closing.
    """
    signal = TradeSignal(
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemandStrategy",
        metadata={
            "strategy_mode": "ORDER_BLOCK_DEMAND",
            "target_1to1_price": 2.5200,
            "target_1to2_price": 2.5400,
            "partial_tp_enabled": True
        }
    )

    mock_engine._shutdown_requested = True
    mock_engine.market.get_ticker.return_value = {"lastPrice": 2.5020, "bid1": 2.5020, "ask1": 2.5021}
    mock_engine.trader.close_position.return_value = {"code": 0, "data": {"orderId": "SHUTDOWN_CLOSE"}}

    exit_price, exit_reason, close_oid = mock_engine._monitor_live_position(
        symbol="TRUMP_USDT",
        position_id=1004,
        direction=OrderDirection.LONG,
        vol_contracts=2,
        leverage=10,
        exact_tp=2.5400,
        exact_sl=2.4800,
        precision=4,
        entry_price=2.5000,
        open_time=time.time(),
        signal=signal,
        pre_placed_tp1_order_id="LIMIT_TP1_SHUTDOWN",
        tp1_contracts=1
    )

    mock_engine.trader.cancel_order.assert_called_once_with("LIMIT_TP1_SHUTDOWN")
    mock_engine.trader.close_position.assert_called_once()
