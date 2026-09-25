"""
Unit & Integration Tests for MongoDB Logging & Live Analytics (OB + Demand Strategy)
=====================================================================================
Validates:
1. TradeOutcome serialization (to_mongo_dict & to_dict) contains all SMC & MM detailed telemetry.
2. MongoTradeLogger logging (log_executed_trade and log_trade alias) with multiple pairs.
3. MultiAssetExecutionEngine worker wiring, outcome propagation, and MongoDB logging.
4. Live Analytics strategy matching, filtering, and OB + Demand telemetry display.
"""

import time
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from kcex.engine.models import (
    TradeOutcome,
    OrderDirection,
    EngineMode,
    ExitReason,
    ExecutionConfig,
    TradeSignal
)
from kcex.engine.mongo_logger import MongoTradeLogger
from run_live_analytics import (
    matches_strategy,
    filter_trades,
    compute_analytics,
    display_order_block_demand_telemetry
)


def test_trade_outcome_full_smc_serialization():
    """Verify that TradeOutcome contains and serializes all SMC detailed info to MongoDB dict."""
    outcome = TradeOutcome(
        trade_id=101,
        symbol="ETH_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemand(Hour4)",
        mode=EngineMode.LIVE,
        leverage=15,
        vol_contracts=2,
        contract_size=0.01,
        underlying_quantity=0.02,
        base_coin="ETH",
        entry_price=3500.0,
        exit_price=3600.0,
        min_profit_tp_price=3600.0,
        stop_loss_price=3450.0,
        price_unit=0.01,
        price_precision=2,
        open_time=time.time() - 3600,
        close_time=time.time(),
        duration_seconds=3600.0,
        notional_value_usdt=70.0,
        notional_value_inr=6650.0,
        margin_used_usdt=4.67,
        margin_used_inr=443.65,
        realized_pnl_usdt=2.0,
        realized_pnl_inr=190.0,
        pnl_percentage=2.857,
        roe_percentage=42.82,
        inr_rate=95.0,
        exit_reason=ExitReason.MIN_PROFIT_TP_HIT,
        balance_before_trade_usdt=100.0,
        balance_before_trade_inr=9500.0,
        balance_after_trade_usdt=102.0,
        balance_after_trade_inr=9690.0,
        smc_zone_id="OB_BULL_42_1790000000",
        smc_zone_type="BULLISH_ORDER_BLOCK",
        smc_zone_high=3475.0,
        smc_zone_low=3450.0,
        smc_zone_mid=3462.5,
        smc_zone_creation_bar_idx=42,
        smc_zone_creation_ts=1790000000000,
        smc_zone_creation_time_utc="2026-09-24 10:00:00 UTC",
        smc_bos_bar_idx=50,
        smc_bos_price=3510.0,
        smc_trigger_candle_time_utc="2026-09-24 12:00:00 UTC",
        smc_trigger_bar_idx=55,
        smc_fvg_size=5.0,
        smc_target_1to1=3550.0,
        smc_target_1to2=3600.0,
        smc_partial_tp_hit=True
    )

    mongo_doc = outcome.to_mongo_dict()
    assert mongo_doc["trade_id"] == 101
    assert mongo_doc["symbol"] == "ETH_USDT"
    assert mongo_doc["base_coin"] == "ETH"
    assert mongo_doc["smc_zone_id"] == "OB_BULL_42_1790000000"
    assert mongo_doc["smc_zone_type"] == "BULLISH_ORDER_BLOCK"
    assert mongo_doc["smc_zone_high"] == 3475.0
    assert mongo_doc["smc_zone_low"] == 3450.0
    assert mongo_doc["smc_zone_mid"] == 3462.5
    assert mongo_doc["smc_zone_creation_bar_idx"] == 42
    assert mongo_doc["smc_zone_creation_time_utc"] == "2026-09-24 10:00:00 UTC"
    assert mongo_doc["smc_bos_price"] == 3510.0
    assert mongo_doc["smc_trigger_candle_time_utc"] == "2026-09-24 12:00:00 UTC"
    assert mongo_doc["smc_target_1to1"] == 3550.0
    assert mongo_doc["smc_target_1to2"] == 3600.0
    assert mongo_doc["smc_partial_tp_hit"] is True
    assert mongo_doc["balance_before_trade_usdt"] == 100.0
    assert mongo_doc["balance_after_trade_usdt"] == 102.0

    # Test to_dict alias
    std_dict = outcome.to_dict()
    assert std_dict["smc_zone_id"] == "OB_BULL_42_1790000000"
    assert std_dict["smc_zone_mid"] == 3462.5


def test_mongo_logger_mock_insert_all_pairs():
    """Verify MongoTradeLogger logs trades for all pairs and provides log_trade alias."""
    logger = MongoTradeLogger(mongodb_uri="mongodb://localhost:27017")
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.insert_one.return_value.inserted_id = "test_doc_id_999"

    logger._connected = True
    logger._db = mock_db

    pairs_to_test = ["TRUMP_USDT", "ETH_USDT", "BTC_USDT", "DOGE_USDT"]

    for i, symbol in enumerate(pairs_to_test, 1):
        outcome = TradeOutcome(
            trade_id=i,
            symbol=symbol,
            direction=OrderDirection.LONG,
            sub_strategy_name=f"OrderBlockDemand(Min15)",
            mode=EngineMode.LIVE,
            leverage=15,
            vol_contracts=1,
            contract_size=1.0,
            underlying_quantity=1.0,
            entry_price=10.0,
            exit_price=11.0,
            min_profit_tp_price=11.0,
            stop_loss_price=9.5,
            price_unit=0.01,
            open_time=time.time() - 60,
            close_time=time.time(),
            duration_seconds=60.0,
            notional_value_usdt=10.0,
            notional_value_inr=950.0,
            margin_used_usdt=0.67,
            margin_used_inr=63.65,
            realized_pnl_usdt=1.0,
            realized_pnl_inr=95.0,
            pnl_percentage=10.0,
            roe_percentage=150.0,
            exit_reason=ExitReason.MIN_PROFIT_TP_HIT,
            smc_zone_id=f"OB_{symbol}_{i}",
            smc_zone_type="BULLISH_ORDER_BLOCK",
            smc_zone_high=9.8,
            smc_zone_low=9.5,
            smc_target_1to1=10.5,
            smc_target_1to2=11.0,
            smc_partial_tp_hit=True
        )

        cfg = ExecutionConfig(symbol=symbol, leverage=15, strategy_mode="ORDER_BLOCK_DEMAND")

        # Test log_executed_trade
        doc_id = logger.log_executed_trade(outcome, cfg, balance_before_usdt=50.0, balance_before_inr=4750.0)
        assert doc_id == "test_doc_id_999"

        # Test log_trade alias
        alias_doc_id = logger.log_trade(outcome, cfg, balance_before_usdt=50.0, balance_before_inr=4750.0)
        assert alias_doc_id == "test_doc_id_999"


def test_strategy_matching_in_analytics():
    """Verify that matches_strategy recognizes all variants of OB + Demand strategy."""
    doc1 = {"sub_strategy_name": "OrderBlockDemand(Hour4)", "config_snapshot": {"strategy_mode": "ORDER_BLOCK_DEMAND"}}
    doc2 = {"sub_strategy_name": "OrderBlockDemand(BULLISH_ORDER_BLOCK-LONG)", "config_snapshot": {}}
    doc3 = {"sub_strategy_name": "TICK_CONSTRAINED_MM", "smc_zone_id": "OB_123"}
    doc4 = {"sub_strategy_name": "StochasticRSI(FAST_SCALP-LONG)", "config_snapshot": {"strategy_mode": "STOCH_RSI"}}

    assert matches_strategy(doc1, "ORDER_BLOCK_DEMAND") is True
    assert matches_strategy(doc1, "OB") is True
    assert matches_strategy(doc1, "SMC") is True
    assert matches_strategy(doc2, "OB") is True
    assert matches_strategy(doc2, "ORDER_BLOCK") is True
    assert matches_strategy(doc3, "OB") is True
    assert matches_strategy(doc4, "OB") is False
    assert matches_strategy(doc4, "STOCH_RSI") is True


def test_multi_asset_breakdown_analytics(capsys):
    """Verify display_order_block_demand_telemetry aggregates and presents multi-pair analytics."""
    sample_trades = [
        {
            "trade_id": 1,
            "symbol": "TRUMP_USDT",
            "direction": "LONG",
            "sub_strategy_name": "OrderBlockDemand(Min15)",
            "realized_pnl_usdt": 0.05,
            "realized_pnl_inr": 4.75,
            "duration_seconds": 120.0,
            "exit_reason": "MIN_PROFIT_TP_HIT",
            "smc_zone_id": "OB_1",
            "smc_zone_type": "BULLISH_ORDER_BLOCK",
            "smc_zone_high": 2.05,
            "smc_zone_low": 2.00,
            "smc_target_1to1": 2.10,
            "smc_target_1to2": 2.20,
            "smc_partial_tp_hit": True
        },
        {
            "trade_id": 2,
            "symbol": "DOGE_USDT",
            "direction": "SHORT",
            "sub_strategy_name": "OrderBlockDemand(Min15)",
            "realized_pnl_usdt": 0.02,
            "realized_pnl_inr": 1.90,
            "duration_seconds": 60.0,
            "exit_reason": "MIN_PROFIT_TP_HIT",
            "smc_zone_id": "OB_2",
            "smc_zone_type": "BEARISH_ORDER_BLOCK",
            "smc_zone_high": 0.25,
            "smc_zone_low": 0.24,
            "smc_target_1to1": 0.23,
            "smc_target_1to2": 0.22,
            "smc_partial_tp_hit": False
        },
        {
            "trade_id": 3,
            "symbol": "ETH_USDT",
            "direction": "LONG",
            "sub_strategy_name": "OrderBlockDemand(Hour4)",
            "realized_pnl_usdt": -0.03,
            "realized_pnl_inr": -2.85,
            "duration_seconds": 300.0,
            "exit_reason": "STOP_LOSS_HIT",
            "smc_zone_id": "OB_3",
            "smc_zone_type": "DEMAND_BLOCK",
            "smc_zone_high": 3500.0,
            "smc_zone_low": 3480.0,
            "smc_target_1to1": 3550.0,
            "smc_target_1to2": 3600.0,
            "smc_partial_tp_hit": False
        }
    ]

    display_order_block_demand_telemetry(sample_trades, asset_label="ALL")
    captured = capsys.readouterr().out

    assert "ORDER BLOCK + DEMAND BLOCK STRATEGY TELEMETRY [SMC]" in captured
    assert "SMC Multi-Asset Performance Breakdown (By Pair):" in captured
    assert "TRUMP_USDT" in captured
    assert "DOGE_USDT" in captured
    assert "ETH_USDT" in captured
    assert "BULL_OB" in captured
    assert "BEAR_OB" in captured
    assert "DEMAND" in captured
