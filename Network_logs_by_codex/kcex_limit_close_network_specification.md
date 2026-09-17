# KCEX Close Long / Close Short Limit Order Specification & Log Reference

**Capture Date**: 2026-09-18 (Asia/Kolkata)  
**Platform**: WEB (`prd - v3.8.10 - 4420ec7`)  
**Target Tested Pair**: `MOG_USDT` (linear_swap)

---

## 1. Executive Summary & Verification

The endpoint used by KCEX to close both Long and Short positions (via Market or Limit Orders) is:

```http
POST https://www.kcex.com/fapi/v1/private/order/create
```

This endpoint handles both opening new positions and closing existing positions. The action is differentiated exclusively by the **`side`**, **`type`**, and **`positionId`** payload parameters:

| Action | `side` Value | `type` Value | Role |
|---|:---:|:---:|---|
| **Open Long** | `1` | `1` (Limit) / `5` (Market) | Open new long position |
| **Close Short** (Buy to Cover) | `2` | `1` (Limit) / `5` (Market) | Closes active short position |
| **Open Short** | `3` | `1` (Limit) / `5` (Market) | Open new short position |
| **Close Long** (Sell to Exit) | `4` | `1` (Limit) / `5` (Market) | Closes active long position |

---

## 2. Limit Close Payload Schemas

### A. Close Short Limit Order (`side: 2`, `type: 1`)

Used when you are holding an open **SHORT** position and wish to set a Limit Order to buy back contracts at an exact price.

```json
{
  "symbol": "MOG_USDT",
  "openType": 1,
  "positionId": 86111367,
  "leverage": 25,
  "type": 1,
  "vol": 1,
  "side": 2,
  "price": "0.00000345",
  "flashClose": false,
  "priceProtect": "0"
}
```

### B. Close Long Limit Order (`side: 4`, `type: 1`)

Used when you are holding an open **LONG** position and wish to set a Limit Order to sell contracts at an exact price.

```json
{
  "symbol": "MOG_USDT",
  "openType": 1,
  "positionId": 86111367,
  "leverage": 25,
  "type": 1,
  "vol": 1,
  "side": 4,
  "price": "0.00000410",
  "flashClose": false,
  "priceProtect": "0"
}
```

---

## 3. Parameter Breakdown

| Field | Type | Description |
|---|---|---|
| `symbol` | `string` | The futures contract ticker (e.g. `"MOG_USDT"`, `"TRUMP_USDT"`). |
| `openType` | `integer` | Margin mode: `1` = Isolated Margin, `2` = Cross Margin. |
| `positionId` | `integer` | ID of the active position returned by `GET /fapi/v1/private/position/open_positions`. |
| `leverage` | `integer` | Position leverage multiplier (e.g. `25`, `75`). |
| `type` | `integer` | Order Type: **`1` = Limit Order**, `5` = Market Order. |
| `side` | `integer` | Order Direction: **`2` = Close Short**, **`4` = Close Long**. |
| `vol` | `integer` | Number of contract units to close (must satisfy `minVol <= vol <= holdVol`). |
| `price` | `string` | Target limit price. Must be formatted strictly to contract `priceScale` without scientific notation (e.g. `"0.00000345"`). |
| `flashClose` | `boolean` | Must be `false` for limit orders. |
| `priceProtect` | `string` | Price protection setting (`"0"` by default). |

---

## 4. Required Headers

Private orders must include KCEX's dynamic session authentication headers:

```http
Authorization: <REDACTED_SESSION_TOKEN>
Content-Sign: <DYNAMIC_HMAC_SHA256>
Content-time: <EPOCH_MS>
User-Device: eyJ2aXNpdG9ySWQiOiJwMWw4STBBbWJNNHI3OXpsdkR3RiIsInJlcXVlc3RJZCI6IjE3ODk2NTMyOTM4ODIuaWxPc2VqIn0
Platform: WEB
Version-tag: prd - v3.8.10 - 4420ec7
Content-Type: application/json;charset=UTF-8
Language: en-US
```

---

## 5. Successful Response

```json
{
  "success": true,
  "code": 0,
  "data": {
    "orderId": "850678462910268416",
    "ts": 1788487950408
  }
}
```

Once submitted, the order appears under active open orders:
`GET /fapi/v1/private/order/list/open_orders?page_size=200`
and can be canceled via:
`POST /fapi/v1/private/order/cancel` with payload `{"orderId": "<orderId>", "symbol": "<symbol>"}`.

---

## 6. Python SDK Integration in Bot

In `kcex/trade.py`, dedicated functions are implemented:

```python
# To close Short position using Limit Order:
trader.close_short_limit(
    symbol="MOG_USDT",
    price=0.00000345,
    vol_contracts=5   # optional: auto-detects entire position if omitted
)

# To close Long position using Limit Order:
trader.close_long_limit(
    symbol="MOG_USDT",
    price=0.00000410,
    vol_contracts=10  # optional: auto-detects entire position if omitted
)
```
