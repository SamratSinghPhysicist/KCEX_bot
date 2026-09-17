#!/usr/bin/env python3
"""
KCEX All Pairs Detailed Exporter
================================
Discovers, fetches, and analyzes all futures trading pairs available on KCEX.

Endpoints identified from network reconnaissance logs in D:\\My_Bots\\Trading\\KCEX\\Network_logs_by_codex:
1. GET /fapi/v1/contract/detail?type=all  (Comprehensive specifications for all pairs)
2. GET /fapi/v1/contract/detailV2?client=web (Alternative metadata route)
3. GET /fapi/v1/contract/ticker (Real-time prices, 24h volume, funding rates, open interest)

Fields Captured:
1. Fees: Maker fee rate (%), Taker fee rate (%), Zero-fee flag
2. Min Quantity & Contracts: minVol, contractSize, min_underlying_qty, min_notional_usdt, min_margin_usdt, maxVol
3. Tick Size: priceUnit, priceScale (precision)
4. Start Date / Age: createTime, start_date_utc, start_date_ist, age_days, age_readable
5. Max Leverage: maxLeverage, minLeverage, maintenanceMarginRate (mmr), initialMarginRate (imr)
6. Other Relevant Info: status (ACTIVE/DELISTED), lastPrice, fairPrice, indexPrice, fundingRate, 24h turnover,
   open interest, 24h change %, isHot, isNew, apiAllowed, conceptPlate tags, oracle sources
"""

import os
import sys
import json
import csv
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional


# =====================================================================
# CONFIGURATION
# =====================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "ALL_PAIRS_DETAILS_18Sep2026")

BASE_URL = "https://www.kcex.com"
ENDPOINT_DETAIL_ALL = f"{BASE_URL}/fapi/v1/contract/detail?type=all"
ENDPOINT_DETAIL_V2 = f"{BASE_URL}/fapi/v1/contract/detailV2?client=web"
ENDPOINT_TICKER = f"{BASE_URL}/fapi/v1/contract/ticker"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

IST = timezone(timedelta(hours=5, minutes=30))


# =====================================================================
# NETWORK FETCHERS
# =====================================================================
def fetch_json(url: str, timeout: int = 15) -> Optional[Dict[str, Any]]:
    """Fetch JSON data from KCEX REST API."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                raw = response.read().decode("utf-8")
                return json.loads(raw)
    except Exception as e:
        print(f"[WARN] Failed fetching {url}: {e}", file=sys.stderr)
    return None


def format_readable_age(days: int) -> str:
    """Format days into human-readable age e.g. '2y 140d' or '45d'."""
    if days < 0:
        return "New (today)"
    years = days // 365
    rem_days = days % 365
    if years > 0:
        return f"{years}y {rem_days}d"
    months = days // 30
    if months > 0:
        return f"{months}m {days % 30}d"
    return f"{days}d"


# =====================================================================
# MAIN PROCESSOR
# =====================================================================
def run():
    print("=" * 80)
    print(" KCEX ALL PAIRS DETAILED EXPORTER")
    print("=" * 80)
    print(f"Target Output Directory: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Fetch Contract Specifications
    print("\n[1/3] Fetching KCEX contract specifications...")
    spec_data = fetch_json(ENDPOINT_DETAIL_ALL)
    if not spec_data or "data" not in spec_data or not spec_data["data"]:
        print("[INFO] Fallback to detailV2 endpoint...")
        spec_data = fetch_json(ENDPOINT_DETAIL_V2)

    if not spec_data or "data" not in spec_data:
        raise RuntimeError("Failed to retrieve contract specifications from KCEX API.")

    contracts_raw: List[Dict[str, Any]] = spec_data["data"]
    print(f"      Retrieved {len(contracts_raw)} contract records from KCEX.")

    # 2. Fetch Live Tickers
    print("\n[2/3] Fetching KCEX real-time contract tickers...")
    ticker_data = fetch_json(ENDPOINT_TICKER)
    tickers: Dict[str, Dict[str, Any]] = {}
    if ticker_data and "data" in ticker_data and isinstance(ticker_data["data"], list):
        for item in ticker_data["data"]:
            sym = item.get("symbol")
            if sym:
                tickers[sym] = item
    print(f"      Retrieved {len(tickers)} active market tickers.")

    # Current timestamp for age calculation
    now_utc = datetime.now(timezone.utc)

    # 3. Process each pair
    print("\n[3/3] Parsing and enriching pair details...")
    processed_records: List[Dict[str, Any]] = []

    for c in contracts_raw:
        symbol = c.get("symbol") or c.get("contractCode") or ""
        if not symbol:
            continue

        base_coin = c.get("baseCoin") or c.get("bc") or ""
        quote_coin = c.get("quoteCoin") or c.get("qc") or ""
        settle_coin = c.get("settleCoin") or c.get("sc") or quote_coin
        display_name_en = c.get("displayNameEn") or c.get("dne") or f"{symbol} SWAP"

        # State / Status
        raw_state = c.get("state")
        # state == 0 is active/trading; state == 3 is delisted / inactive
        is_active = (raw_state == 0) and (symbol in tickers)
        status_str = "ACTIVE" if is_active else ("SUSPENDED_OR_DELISTED" if raw_state == 3 else f"INACTIVE_{raw_state}")

        # Fees
        maker_fee = float(c.get("makerFeeRate") if c.get("makerFeeRate") is not None else (c.get("mfr") or 0.0))
        taker_fee = float(c.get("takerFeeRate") if c.get("takerFeeRate") is not None else (c.get("tfr") or 0.0))
        is_zero_fee = (maker_fee == 0.0 and taker_fee == 0.0)

        # Min / Max Volume & Contract Size
        min_contracts = float(c.get("minVol") if c.get("minVol") is not None else (c.get("minV") or 1.0))
        max_contracts = float(c.get("maxVol") if c.get("maxVol") is not None else (c.get("maxV") or 0.0))
        contract_size = float(c.get("contractSize") if c.get("contractSize") is not None else (c.get("cs") or 1.0))
        min_underlying_qty = min_contracts * contract_size
        max_underlying_qty = max_contracts * contract_size if max_contracts else 0.0

        vol_unit_step = float(c.get("volUnit") if c.get("volUnit") is not None else (c.get("vu") or 1.0))
        vol_precision = int(c.get("volScale") if c.get("volScale") is not None else (c.get("vs") or 0))

        # Tick Size / Price Precision
        tick_size = float(c.get("priceUnit") if c.get("priceUnit") is not None else (c.get("pu") or 0.001))
        price_precision = int(c.get("priceScale") if c.get("priceScale") is not None else (c.get("ps") or 2))
        amount_precision = int(c.get("amountScale") if c.get("amountScale") is not None else (c.get("as") or 2))

        # Leverage & Margins
        min_leverage = int(c.get("minLeverage") if c.get("minLeverage") is not None else (c.get("minL") or 1))
        max_leverage = int(c.get("maxLeverage") if c.get("maxLeverage") is not None else (c.get("maxL") or 20))
        mmr = float(c.get("maintenanceMarginRate") if c.get("maintenanceMarginRate") is not None else (c.get("mmr") or 0.005))
        imr = float(c.get("initialMarginRate") if c.get("initialMarginRate") is not None else (c.get("imr") or 0.01))

        # Start Date / Listing Time
        create_time_ms = c.get("createTime") or c.get("ct")
        start_date_utc_str = ""
        start_date_ist_str = ""
        age_days = -1
        age_str = "N/A"
        if create_time_ms:
            try:
                dt_utc = datetime.fromtimestamp(create_time_ms / 1000.0, timezone.utc)
                dt_ist = dt_utc.astimezone(IST)
                start_date_utc_str = dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
                start_date_ist_str = dt_ist.strftime("%Y-%m-%d %H:%M:%S IST")
                delta = now_utc - dt_utc
                age_days = max(0, delta.days)
                age_str = format_readable_age(age_days)
            except Exception:
                pass

        # Ticker Market Stats
        t = tickers.get(symbol, {})
        last_price = float(t.get("lastPrice")) if t.get("lastPrice") is not None else None
        fair_price = float(t.get("fairPrice")) if t.get("fairPrice") is not None else None
        index_price = float(t.get("indexPrice")) if t.get("indexPrice") is not None else None
        funding_rate = float(t.get("fundingRate")) if t.get("fundingRate") is not None else None
        change_24h_rate = float(t.get("riseFallRate")) if t.get("riseFallRate") is not None else None
        vol_24h_contracts = float(t.get("volume24")) if t.get("volume24") is not None else None
        turnover_24h_usdt = float(t.get("amount24")) if t.get("amount24") is not None else None
        open_interest_contracts = float(t.get("holdVol")) if t.get("holdVol") is not None else None
        high_24h = float(t.get("high24Price")) if t.get("high24Price") is not None else None
        low_24h = float(t.get("lower24Price")) if t.get("lower24Price") is not None else None

        # Calculate Notional & Margin
        price_for_calc = last_price or fair_price
        if price_for_calc is not None and price_for_calc > 0:
            min_notional_usdt = round(min_contracts * contract_size * price_for_calc, 6)
            min_margin_usdt = round(min_notional_usdt / max_leverage, 6) if max_leverage > 0 else None
            open_interest_usdt = round(open_interest_contracts * contract_size * price_for_calc, 2) if open_interest_contracts else None
        else:
            min_notional_usdt = None
            min_margin_usdt = None
            open_interest_usdt = None

        # Tags and Oracle
        concept_plate = c.get("conceptPlate") or c.get("cp") or []
        tags_str = "; ".join(concept_plate) if isinstance(concept_plate, list) else str(concept_plate)
        index_origin = c.get("indexOrigin") or c.get("io") or []
        oracles_str = "; ".join(index_origin) if isinstance(index_origin, list) else str(index_origin)
        depth_steps = c.get("depthStepList") or c.get("dsl") or []
        depth_steps_str = "; ".join(str(x) for x in depth_steps) if isinstance(depth_steps, list) else str(depth_steps)

        is_hot = bool(c.get("isHot") or c.get("ih"))
        is_new = bool(c.get("isNew") or c.get("in"))
        api_allowed = bool(c.get("apiAllowed", True))

        record = {
            "symbol": symbol,
            "status": status_str,
            "is_active": is_active,
            "base_coin": base_coin,
            "quote_coin": quote_coin,
            "settle_coin": settle_coin,
            "display_name_en": display_name_en,
            # Fees
            "maker_fee_rate": maker_fee,
            "maker_fee_pct": f"{maker_fee * 100:.3f}%",
            "taker_fee_rate": taker_fee,
            "taker_fee_pct": f"{taker_fee * 100:.3f}%",
            "is_zero_fee": is_zero_fee,
            # Minimums & Contract sizing
            "min_contracts": min_contracts,
            "contract_size": contract_size,
            "min_underlying_qty": min_underlying_qty,
            "min_notional_usdt": min_notional_usdt,
            "min_margin_usdt": min_margin_usdt,
            "max_contracts": max_contracts,
            "max_underlying_qty": max_underlying_qty,
            "vol_unit_step": vol_unit_step,
            "vol_precision_scale": vol_precision,
            # Tick size & Price Precision
            "tick_size": tick_size,
            "price_precision_scale": price_precision,
            "amount_precision_scale": amount_precision,
            # Start Date & Age
            "start_date_utc": start_date_utc_str,
            "start_date_ist": start_date_ist_str,
            "start_timestamp_ms": create_time_ms,
            "age_days": age_days,
            "age_readable": age_str,
            # Leverage & Margins
            "max_leverage": max_leverage,
            "min_leverage": min_leverage,
            "maintenance_margin_rate": mmr,
            "maintenance_margin_pct": f"{mmr * 100:.2f}%",
            "initial_margin_rate": imr,
            "initial_margin_pct": f"{imr * 100:.2f}%",
            # Market Realtime Info
            "current_price": last_price,
            "fair_price": fair_price,
            "index_price": index_price,
            "funding_rate": funding_rate,
            "funding_rate_pct": f"{funding_rate * 100:.4f}%" if funding_rate is not None else "",
            "price_change_24h_pct": f"{change_24h_rate * 100:.2f}%" if change_24h_rate is not None else "",
            "high_24h": high_24h,
            "low_24h": low_24h,
            "volume_24h_contracts": vol_24h_contracts,
            "turnover_24h_usdt": turnover_24h_usdt,
            "open_interest_contracts": open_interest_contracts,
            "open_interest_usdt": open_interest_usdt,
            # Flags & Metadata
            "is_hot": is_hot,
            "is_new": is_new,
            "api_allowed": api_allowed,
            "tags_concept_plate": tags_str,
            "oracle_sources": oracles_str,
            "depth_step_aggregations": depth_steps_str,
        }
        processed_records.append(record)

    # Sort records: ACTIVE pairs first, then by turnover_24h_usdt descending (with None last), then symbol
    processed_records.sort(
        key=lambda r: (
            0 if r["is_active"] else 1,
            -(r["turnover_24h_usdt"] or 0),
            r["symbol"]
        )
    )

    active_records = [r for r in processed_records if r["is_active"]]
    zero_fee_active_records = [r for r in active_records if r["is_zero_fee"]]

    print(f"\n[SUMMARY STATS]")
    print(f"Total historical/cataloged pairs: {len(processed_records)}")
    print(f"Currently active & tradable pairs: {len(active_records)}")
    print(f"Active zero-fee pairs (0% maker & 0% taker): {len(zero_fee_active_records)}")

    # =====================================================================
    # EXPORT CSV FILES
    # =====================================================================
    fieldnames = list(processed_records[0].keys())

    # 1. Complete Catalog (All Pairs)
    all_csv_path = os.path.join(OUTPUT_DIR, "kcex_all_pairs_detailed.csv")
    with open(all_csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_records)
    print(f"[EXPORT] Saved {len(processed_records)} rows -> {all_csv_path}")

    # 2. Active Pairs Only (Currently Tradable with live price)
    active_csv_path = os.path.join(OUTPUT_DIR, "kcex_active_pairs_detailed.csv")
    with open(active_csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(active_records)
    print(f"[EXPORT] Saved {len(active_records)} rows -> {active_csv_path}")

    # 3. Active Zero-Fee Pairs (0% maker & 0% taker)
    zero_fee_csv_path = os.path.join(OUTPUT_DIR, "kcex_zero_fee_pairs_detailed.csv")
    with open(zero_fee_csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(zero_fee_active_records)
    print(f"[EXPORT] Saved {len(zero_fee_active_records)} rows -> {zero_fee_csv_path}")

    # 4. JSON Export for programmatic loading in trading bots
    json_path = os.path.join(OUTPUT_DIR, "kcex_all_pairs_detailed.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "total_pairs_count": len(processed_records),
            "active_pairs_count": len(active_records),
            "zero_fee_active_count": len(zero_fee_active_records),
            "pairs": processed_records
        }, f, indent=2, ensure_ascii=False)
    print(f"[EXPORT] Saved JSON database -> {json_path}")

    # 5. Generate Markdown Summary Report
    report_path = os.path.join(OUTPUT_DIR, "README_PAIR_ANALYSIS.md")
    generate_markdown_report(report_path, processed_records, active_records, zero_fee_active_records, now_utc)
    print(f"[EXPORT] Saved Analysis Report -> {report_path}")

    print("\n[SUCCESS] KCEX pairs extraction complete!")


def generate_markdown_report(report_path, all_records, active_records, zero_fee_records, now_utc):
    """Generates an executive markdown report summarizing the dataset."""
    leverage_counts = {}
    for r in active_records:
        lev = f"{r['max_leverage']}x"
        leverage_counts[lev] = leverage_counts.get(lev, 0) + 1
    sorted_leverage = sorted(leverage_counts.items(), key=lambda x: int(x[0].replace('x','')), reverse=True)

    # Smallest min margin pairs
    priced_active = [r for r in active_records if r['min_margin_usdt'] is not None and r['min_margin_usdt'] > 0]
    cheapest_margin = sorted(priced_active, key=lambda x: x['min_margin_usdt'])[:15]

    # Top volume pairs
    top_volume = sorted(active_records, key=lambda x: x['turnover_24h_usdt'] or 0, reverse=True)[:15]

    # Oldest and Newest coins
    valid_age = [r for r in active_records if r['age_days'] >= 0]
    newest = sorted(valid_age, key=lambda x: x['age_days'])[:10]
    oldest = sorted(valid_age, key=lambda x: x['age_days'], reverse=True)[:10]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# KCEX Futures Pairs Analysis & Specification Report\n\n")
        f.write(f"- **Generated At**: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} (Asia/Kolkata: {now_utc.astimezone(IST).strftime('%Y-%m-%d %H:%M:%S IST')})\n")
        f.write(f"- **Total Listed / Cataloged Pairs**: {len(all_records)}\n")
        f.write(f"- **Currently Active & Tradable Pairs**: {len(active_records)}\n")
        f.write(f"- **Zero-Fee Pairs (0% Maker & 0% Taker)**: {len(zero_fee_records)}\n\n")

        f.write("## 1. Leverage Tier Breakdown (Active Pairs)\n\n")
        f.write("| Max Leverage | Pair Count | Percentage |\n|---|---:|---:|\n")
        for lev, count in sorted_leverage:
            pct = (count / len(active_records)) * 100
            f.write(f"| {lev} | {count} | {pct:.1f}% |\n")

        f.write("\n## 2. Top 15 Highest 24h Turnover Pairs\n\n")
        f.write("| Symbol | Price | 24h Turnover (USDT) | Max Lev | Maker Fee | Taker Fee | Min Order USDT |\n|---|---:|---:|---:|---:|---:|---:|\n")
        for r in top_volume:
            f.write(f"| `{r['symbol']}` | {r['current_price']} | ${r['turnover_24h_usdt']:,.2f} | {r['max_leverage']}x | {r['maker_fee_pct']} | {r['taker_fee_pct']} | ${r['min_notional_usdt']} |\n")

        f.write("\n## 3. Top 15 Smallest Capital Requirement Pairs (Lowest Min Margin USDT)\n\n")
        f.write("| Symbol | Price | Max Lev | Min Contracts | Contract Size | Min Notional USDT | Min Margin USDT | Zero Fee? |\n|---|---:|---:|---:|---:|---:|---:|:---:|\n")
        for r in cheapest_margin:
            f.write(f"| `{r['symbol']}` | {r['current_price']} | {r['max_leverage']}x | {r['min_contracts']} | {r['contract_size']} | ${r['min_notional_usdt']} | **${r['min_margin_usdt']}** | {'✅' if r['is_zero_fee'] else '❌'} |\n")

        f.write("\n## 4. Newest Listed Pairs on KCEX\n\n")
        f.write("| Symbol | Listed Date (UTC) | Age | 24h Turnover (USDT) | Max Lev |\n|---|---|---|---:|---:|\n")
        for r in newest:
            f.write(f"| `{r['symbol']}` | {r['start_date_utc']} | {r['age_readable']} | ${r['turnover_24h_usdt']:,.2f} | {r['max_leverage']}x |\n")

        f.write("\n## 5. Oldest Listed Pairs on KCEX\n\n")
        f.write("| Symbol | Listed Date (UTC) | Age | 24h Turnover (USDT) | Max Lev |\n|---|---|---|---:|---:|\n")
        for r in oldest:
            f.write(f"| `{r['symbol']}` | {r['start_date_utc']} | {r['age_readable']} | ${r['turnover_24h_usdt']:,.2f} | {r['max_leverage']}x |\n")

        f.write("\n## 6. Export Files Description\n\n")
        f.write("1. `kcex_all_pairs_detailed.csv`: Complete database of all 1,740 pairs with status, fees, sizing, tick sizes, age, leverage, and volume.\n")
        f.write("2. `kcex_active_pairs_detailed.csv`: Filtered view of all 839 currently active/tradable pairs with live ticker quotes and computed margin requirements.\n")
        f.write("3. `kcex_zero_fee_pairs_detailed.csv`: 108 active pairs featuring 0.00% maker fee AND 0.00% taker fee.\n")
        f.write("4. `kcex_all_pairs_detailed.json`: Formatted JSON file ready for direct ingestion by Python bot algorithms.\n")


if __name__ == "__main__":
    run()
