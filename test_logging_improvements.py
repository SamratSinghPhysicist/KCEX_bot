import os
import sys
import json
import pytest
from datetime import datetime, timezone

from kcex.engine.logger import DualCurrencyLogger, TradeOutcomeLogger
from kcex.engine.models import (
    TradeOutcome,
    OrderDirection,
    EngineMode,
    ExitReason
)


def test_dual_currency_logger_status_line_deduplication(tmp_path):
    log_file = tmp_path / "test_engine.log"
    logger = DualCurrencyLogger(log_file=str(log_file))

    # Force non-TTY simulation (like Railway, GitHub Actions)
    logger._is_tty = False
    logger._is_cloud_ci = True

    # 1. First price update should emit a log line
    emitted_1 = logger.update_status_line(
        msg="[DRY-RUN POSITION] LONG @ 2.4500 | Mark: 2.4500",
        price=2.4500,
        tag="POSITION"
    )
    assert emitted_1 is True

    # 2. Second price update with IDENTICAL price should be SUPPRESSED
    emitted_2 = logger.update_status_line(
        msg="[DRY-RUN POSITION] LONG @ 2.4500 | Mark: 2.4500",
        price=2.4500,
        tag="POSITION"
    )
    assert emitted_2 is False, "Same-price message should be suppressed in cloud/CI mode!"

    # 3. Third price update with NEW price should emit
    emitted_3 = logger.update_status_line(
        msg="[DRY-RUN POSITION] LONG @ 2.4500 | Mark: 2.4550",
        price=2.4550,
        tag="POSITION"
    )
    assert emitted_3 is True, "New price update must emit a log line!"

    # 4. Same new price should be suppressed
    emitted_4 = logger.update_status_line(
        msg="[DRY-RUN POSITION] LONG @ 2.4500 | Mark: 2.4550",
        price=2.4550,
        tag="POSITION"
    )
    assert emitted_4 is False


def test_dual_currency_logger_scanning_status_deduplication(tmp_path):
    log_file = tmp_path / "test_scan.log"
    logger = DualCurrencyLogger(log_file=str(log_file))
    logger._is_tty = False
    logger._is_cloud_ci = True

    scan_msg_1 = "[SCANNING] TRUMP_USDT [Min15] | Price: 2.180 USDT | Zones: 6 (4 Demand, 2 Supply) | Active OB: BEARISH_ORDER_BLOCK [2.237-2.278] | Status: Hunting"
    # First emission allowed
    assert logger.update_status_line(scan_msg_1, price=2.180, tag="SCANNING") is True
    # Identical scan message immediately afterwards must be suppressed!
    assert logger.update_status_line(scan_msg_1, price=2.180, tag="SCANNING") is False

    # Price wobbles by 1 tick (2.181) while scanning: structure is identical, MUST be suppressed!
    scan_msg_2 = "[SCANNING] TRUMP_USDT [Min15] | Price: 2.181 USDT | Zones: 6 (4 Demand, 2 Supply) | Active OB: BEARISH_ORDER_BLOCK [2.237-2.278] | Status: Hunting"
    assert logger.update_status_line(scan_msg_2, price=2.181, tag="SCANNING") is False

    # Price wobbles to 2.179 while scanning: structure is identical, MUST be suppressed!
    scan_msg_3 = "[SCANNING] TRUMP_USDT [Min15] | Price: 2.179 USDT | Zones: 6 (4 Demand, 2 Supply) | Active OB: BEARISH_ORDER_BLOCK [2.237-2.278] | Status: Hunting"
    assert logger.update_status_line(scan_msg_3, price=2.179, tag="SCANNING") is False

    # BUT if zones change from 6 to 7 (genuine structural event): MUST be emitted!
    scan_msg_4 = "[SCANNING] TRUMP_USDT [Min15] | Price: 2.179 USDT | Zones: 7 (4 Demand, 3 Supply) | Active OB: BEARISH_ORDER_BLOCK [2.237-2.278] | Status: Hunting"
    assert logger.update_status_line(scan_msg_4, price=2.179, tag="SCANNING") is True


def test_dual_currency_logger_status_line_tty(tmp_path, monkeypatch):
    log_file = tmp_path / "test_tty.log"
    logger = DualCurrencyLogger(log_file=str(log_file))

    # Force interactive TTY simulation (local terminal)
    logger._is_tty = True
    logger._is_cloud_ci = False

    written = []
    monkeypatch.setattr(sys.stdout, "write", lambda s: written.append(s))
    monkeypatch.setattr(sys.stdout, "flush", lambda: None)

    logger.update_status_line(
        msg="[DRY-RUN POSITION] LONG @ 2.4500 | Mark: 2.4500",
        price=2.4500
    )
    assert any("\r" in s for s in written), "Interactive TTY should use carriage return \\r to update in-place"
    assert logger._in_place_active is True

    # Standard log call should flush a newline to keep history intact
    logger.info("Normal order completed")
    assert logger._in_place_active is False


def test_trade_outcome_logger_smc_order_block_details(tmp_path):
    txt_file = tmp_path / "trade_outcomes.txt"
    jsonl_file = tmp_path / "trade_outcomes.jsonl"
    logger = TradeOutcomeLogger(txt_file=str(txt_file), jsonl_file=str(jsonl_file))

    outcome = TradeOutcome(
        trade_id=1,
        symbol="TRUMP_USDT",
        direction=OrderDirection.LONG,
        sub_strategy_name="OrderBlockDemandStrategy(BULLISH_ORDER_BLOCK-LONG)",
        mode=EngineMode.DRY_RUN,
        leverage=10,
        vol_contracts=12,
        contract_size=1.0,
        underlying_quantity=12.0,
        entry_price=2.4320,
        exit_price=2.4460,
        min_profit_tp_price=2.4600,
        stop_loss_price=2.4180,
        price_unit=0.001,
        open_time=1727088300.0,
        close_time=1727088420.0,
        duration_seconds=120.0,
        notional_value_usdt=29.184,
        notional_value_inr=2756.43,
        margin_used_usdt=2.9184,
        margin_used_inr=275.64,
        realized_pnl_usdt=0.1680,
        realized_pnl_inr=15.87,
        pnl_percentage=0.576,
        roe_percentage=5.76,
        base_coin="TRUMP",
        price_precision=4,
        exit_reason=ExitReason.MIN_PROFIT_TP_HIT,
        # SMC Order Block identified fields
        smc_zone_id="OB_LONG_1727092800",
        smc_zone_type="BULLISH_ORDER_BLOCK",
        smc_zone_high=2.4350,
        smc_zone_low=2.4200,
        smc_zone_mid=2.4275,
        smc_zone_creation_bar_idx=142,
        smc_zone_creation_ts=1727088000000,
        smc_zone_creation_time_utc="2026-09-23 10:40:00 UTC",
        smc_bos_bar_idx=145,
        smc_bos_price=2.4450,
        smc_target_1to1=2.4460,
        smc_target_1to2=2.4600,
        smc_partial_tp_hit=True
    )

    card = logger.log_outcome(outcome)

    # Validate formatted text card contains clear levels and candle location
    assert "SMC Identified OB" in card
    assert "BULLISH_ORDER_BLOCK (#OB_LONG_1727092800)" in card
    assert "Bar #142 | 2026-09-23 10:40:00 UTC" in card
    assert "BOS Bar #145" in card
    assert "Low: 2.4200 <---> Mid: 2.4275 <---> High: 2.4350 USDT" in card
    assert "1:1 TP: 2.4460 USDT" in card
    assert "1:2 TP: 2.4600 USDT" in card

    # Validate JSONL contains full fields
    with open(jsonl_file, "r", encoding="utf-8") as f:
        line = f.readline()
        record = json.loads(line)
        assert record["smc_zone_id"] == "OB_LONG_1727092800"
        assert record["smc_zone_type"] == "BULLISH_ORDER_BLOCK"
        assert record["smc_zone_high"] == 2.4350
        assert record["smc_zone_low"] == 2.4200
        assert record["smc_zone_mid"] == 2.4275
        assert record["smc_zone_creation_bar_idx"] == 142
        assert record["smc_zone_creation_time_utc"] == "2026-09-23 10:40:00 UTC"
        assert record["smc_bos_bar_idx"] == 145
        assert record["smc_target_1to1"] == 2.4460
        assert record["smc_target_1to2"] == 2.4600
        assert record["smc_partial_tp_hit"] is True
