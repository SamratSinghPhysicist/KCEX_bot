# KCEX TRUMP/USDT futures capture — INR conversion and staged 0.3 USDT order

Capture date: 2026-09-04 (Asia/Kolkata)  
Browser: Microsoft Edge, KCEX web futures client `v3.7.91` (`prd - v3.7.91 - fdef20f`)

## Current state

The KCEX futures page is open on `TRUMP_USDT`. The display currency is INR and the wallet card renders INR equivalents (for example, `≈ 0.00 INR` for a zero unrealised PNL). The order form is staged but no new order has been submitted in this run:

- Side: market **long**
- Quantity/volume: **0.3 USDT** (the UI shows approximately `0.1 TRUMP`; margin displayed as `0.00 USDT` because the account uses high leverage)
- Margin mode/leverage: isolated, **75×**
- TP/SL: enabled, **By ROI** mode, TP `+10%`, SL `−10%`
- Available balance observed: `0.62 USDT` (authenticated asset response was approximately `0.627866298806 USDT`)
- Estimated long liquidation price shown by the UI: `2.332` at the observed market price around `2.346`
- Form fee label: Maker `0%` / Taker `0%`

The order was submitted after confirmation. The server accepted one contract (`vol=1`, displayed by the UI as approximately `0.24 USDT` at the fill), with average entry `2.348`, position id `86111127`, and order id `850675602315250176`. The account's attached ROI TP/SL was converted by the client to absolute prices `takeProfitPrice=2.352` and `stopLossPrice=2.345`.

## INR conversion

Changing the menu currency to INR produced no write request; it behaves as a local/display preference. On a clean reload the page fetched:

`GET https://www.kcex.com/api/platform/common/currency/exchange/rate` → HTTP 200

Observed response (captured at reload time):

```json
{"data":{"USD":"0.9999","INR":"94.4985", "HKD":"7.8406", "EUR":"0.8598", "CNY":"6.7186", "JPY":"155.9791", "GBP":"0.7389"},"code":0,"msg":"success"}
```

The observed USD-to-INR display factor was therefore **94.4985 INR per USD** at capture time. This is a time-varying quote, not a constant to hard-code.

The balance/overview conversion call was:

`GET https://www.kcex.com/api/platform/asset/api/asset/overview/convert/v2` → HTTP 200

Its response included USDT balance objects with `originContract` and a display `contract` value (the observed USDT contract display was approximately `0.71`). This confirms the same conversion mechanism is used for futures/contract balance presentation, not just spot balances. Re-fetch the rate and overview before each display or risk calculation.

## Read requests observed for this pair

Authenticated/private requests (all had dynamic auth/signature headers, redacted in the companion NDJSON):

| Purpose | Request |
|---|---|
| Futures asset balance | `GET /fapi/v1/private/account/assets` |
| Position risk limits | `GET /fapi/v1/private/account/risk_limit?…` |
| Position leverage | `GET /fapi/v1/private/position/leverage?symbol=TRUMP_USDT` |
| Open positions | `GET /fapi/v1/private/position/open_positions?…` |
| Fee tier/effective pair fee | `GET /fapi/v1/private/account/tiered_fee_rate?symbol=TRUMP_USDT` |
| Recent deals | `GET /fapi/v1/private/order/list/order_deals?…&symbol=TRUMP_USDT` |
| History orders | `GET /fapi/v1/private/order/list/history_orders?…&symbol=TRUMP_USDT` |
| History positions | `GET /fapi/v1/private/position/list/history_positions?page_num=1&page_size=20` |

Public market/risk requests:

| Purpose | Request |
|---|---|
| Contract metadata | `GET /fapi/v1/contract/detailV2?client=web` (and the symbol-filtered variant) |
| Ticker | `GET /fapi/v1/contract/ticker?symbol=TRUMP_USDT` |
| Order book | `GET /fapi/v1/contract/depth_step/TRUMP_USDT?step=0.001` |
| Recent trades | `GET /fapi/v1/contract/deals/TRUMP_USDT` |
| Funding | `GET /fapi/v1/contract/funding_rate/TRUMP_USDT` |
| Extreme/last price | `GET /fapi/v1/contract/kline/extreme_price/TRUMP_USDT?type=LAST_PRICE` |
| Platform balances | `GET /api/platform/asset/sys_balances?sys=SWAP` (plus related platform asset routes) |

Realtime WebSocket subscriptions observed on the futures page included ticker, depth-step, deals, 1-minute kline, fair/mark price, index price, and funding-rate channels. Heartbeat was `{"method":"ping"}`. Account-channel login material was observed but not exported.

## Contract, leverage, quantity and fee findings

From the TRUMP contract-detail response:

```text
symbol=TRUMP_USDT, cs=0.1, pu=0.001, vu=1,
minV=1, maxV=537040, minL=1, maxL=75,
mmr=0.0067, imr=0.0133, tfr=0, mfr=0
```

`cs=0.1` is the contract size and `pu=0.001` is the price tick. The metadata minimum volume is `minV=1` in KCEX's contract-volume units; the order form accepts 0.3 USDT and renders the equivalent underlying amount, so bots must use the symbol metadata and UI/API volume convention rather than assuming that `minV` is a USDT notional.

The same detail response showed BTC metadata with `maxL=125`, `tfr=0.0001`, `mfr=0` (BTC base taker 0.01%, maker 0%). For TRUMP, the authenticated tier endpoint returned:

```json
{"success":true,"code":0,"data":{"level":9999,"dealAmount":0,"makerFee":0,"takerFee":0,"makerFeeDiscount":1,"takerFeeDiscount":1,"feeType":1,"makerFeeDeduct":0,"takerFeeDeduct":0,"mxDeduct":false,"mxDiscount":false}}
```

Thus the **effective TRUMP fee for this account at capture time was 0 maker / 0 taker**. Fee tiers/events can change; query this endpoint immediately before fee-sensitive trading. The UI also displayed Maker 0% / Taker 0%.

## TP/SL and risk calculation observations

The order form exposes two ROI fields (`+ 10% By ROI` and `− 10% By ROI`) when TP/SL is enabled. This is percentage mode; switching the selector to an absolute-price mode (where available) should be captured separately after the trade. The UI simultaneously exposes estimated liquidation price and margin, so a bot should snapshot ticker/mark price, leverage, contract size, maintenance/initial margin metadata, and fee tier before calculating pre-trade PNL/liquidation.

For the staged 0.3 USDT quantity, the UI displayed approximately `0.1 TRUMP`, `Buy 0.30 USDT`, `Sell 0.30 USDT`, `Margin 0.00 USDT`, and estimated long liquidation `2.332`. INR presentation should be derived from the fresh exchange-rate endpoint, not from a cached constant.

## Write lifecycle to capture after confirmation

The frontend route families identified during source/route reconnaissance are:

| Operation | Route family |
|---|---|
| Open order | `POST /fapi/v1/private/order/create` (often with `mhash` query parameter) |
| Position TP/SL | `POST /fapi/v1/private/stoporder/place/v2` |
| Amend TP/SL | `POST /fapi/v1/private/stoporder/change_plan_order` or `change_plan_price` |
| Partial close / close trigger | `POST /fapi/v1/private/planorder/place/v2` |
| Amend/cancel close trigger | `POST /fapi/v1/private/planorder/change_stop_order`, `change_price[_v1]`, or `cancel` |
| Close all | `POST /fapi/v1/private/position/close_all` |
| Reverse | `POST /fapi/v1/private/position/reverse` |

These are route-family findings, not claims that a write was sent in this run. After each confirmed write, reconcile with open positions, open orders, plan orders, stop orders, order deals, and account assets, and persist server-side IDs.

## Live execution result and captured write

Immediately before submission the UI sent two authenticated liquidation previews:

`POST /fapi/v1/private/position/order/calc_liquidate_price/v2`  
Payload (non-secret fields): `{"leverage":75,"longSideVol":1,"shortSideVol":1,"longSidePrice":2.349,"shortSidePrice":2.349,"positionOpenType":1,"orderType":"5","symbol":"TRUMP_USDT"}`  
Response: `{"success":true,"code":0,"data":{"shortSideLiquidatePrice":2.364,"longSideLiquidatePrice":2.333}}`

The confirmed create request was:

`POST /fapi/v1/private/order/create`  
Payload (non-secret fields):

```json
{"symbol":"TRUMP_USDT","side":1,"openType":1,"type":"5","vol":1,"leverage":75,"marketCeiling":false,"bboPriceType":0,"stopLossPrice":"2.345","takeProfitPrice":"2.352","lossTrend":"1","profitTrend":"1","priceProtect":"0"}
```

Response: `{"success":true,"code":0,"data":{"orderId":"850675602315250176","ts":1788487268389}}`

The attached stop was hit almost immediately as price reached `2.345`; no separate user TP/SL-amend, partial-close, or manual-close write was sent. The authenticated history response recorded position `86111127` as `CLOSED`, `closeVol=1`, `closeAvgPrice=2.345`, `closeProfitLoss=-0.0003 USDT`, `fee=0`, and `profitRatio=-0.0958` (UI displayed the position briefly as 0.24 USDT). Because the position was already closed by the attached stop, partial-close and final manual-close operations were not possible without opening another live position, which was not performed without a separate confirmation for that new trade.

## Security and capture limitations

The companion file is a redacted NDJSON capture. Authorization, Content-Sign, Content-time, User-Device, cookies, WebSocket login tokens, mhash values, IP/device identifiers, and analytics payloads are intentionally removed. These are session/device/time-bound credentials and must not be copied into a bot or exported as a credential file. The report records header names and request shapes so a bot can implement fresh authentication/session handling.

The browser CDP event buffer is finite, so the artifact contains every request class and exact responses retained during the clean reload, not an archival dump of every third-party pixel or compressed market frame ever emitted by the page. Large analytics/compressed bodies are represented by redacted markers.
