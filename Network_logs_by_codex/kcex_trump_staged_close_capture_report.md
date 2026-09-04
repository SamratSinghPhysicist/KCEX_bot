# KCEX TRUMP/USDT staged-close network report

Capture date: 2026-09-04 (Asia/Kolkata)  
Browser: Microsoft Edge  
Page: `https://www.kcex.com/futures/exchange/TRUMP_USDT?type=linear_swap`  
KCEX web client: `v3.7.91` (`prd - v3.7.91 - fdef20f`)

## Outcome

The controlled sequence completed on the logged-in KCEX account:

1. Opened a minimum-size market long on TRUMP/USDT, isolated 75×, with no TP/SL during creation.
2. Added TP `2.400` and SL `2.335` from the Position tab. KCEX reported success and displayed `Position 2.400 / 2.335`.
3. Attempted a 50% market partial close. KCEX rejected it before sending an order mutation: `Minimum order quantity is 0.24 USDT`.
4. Closed the entire position with a market close. The position is now `CLOSED`.

The position was one contract (UI exposure approximately 0.24 USDT), not a 0.3-USDT fill. KCEX's symbol metadata uses contract-volume units (`minV=1`, `cs=0.1`), so the UI's USDT quantity and the API's `vol` must not be treated as interchangeable.

The open-order route was also `POST /fapi/v1/private/order/create`; its exact body was not retained in the finite CDP ring, while the history response confirms `vol=1`, `leverage=75`, `openType=1`, position `86111367`, and average entry `2.344`.

## Exact final-close request

This is the exact successful 100% close request captured from the browser (secret header values redacted):

```http
POST https://www.kcex.com/fapi/v1/private/order/create
Content-Type: application/json
Authorization: <REDACTED>
Content-Sign: <REDACTED>
Content-time: <REDACTED>
User-Device: <REDACTED>
```

```json
{"symbol":"TRUMP_USDT","openType":1,"positionId":86111367,"leverage":75,"type":1,"vol":1,"side":4,"flashClose":false,"price":"2.341","priceProtect":"0"}
```

Response:

```json
{"success":true,"code":0,"data":{"orderId":"850678462910268416","ts":1788487950408}}
```

`side=4` is the closing side for this long in the captured request. `type=1` is the market-close order type used by this dialog. The `price` field is still populated with the dialog's current/reference price even though the order is a market close; do not assume it is a limit price.

## TP/SL add/modify

The Position-tab action succeeded with:

```text
symbol       TRUMP_USDT
positionId   86111367
take profit  2.400
stop loss    2.335
```

The route family used by KCEX's futures frontend for a position stop placement is:

```http
POST https://www.kcex.com/fapi/v1/private/stoporder/place/v2
```

The exact POST body for this specific action was not retained: KCEX's CDP event ring is finite and it rolled past that earlier request by the time the final-close capture was exported. I have intentionally left the payload `null` in the useful-requests JSON rather than inventing a body. The frontend also contains separate amendment route families (`stoporder/change_plan_order` and `stoporder/change_plan_price`); these should not be conflated with the successful placement route.

For a future sacrificial capture, record the full request immediately after clicking the Position-tab confirm, including the stop-order/plan IDs returned by the response. Those IDs are required for later amendments and differ from `positionId`.

## Partial close

The attempted slider value was 50%, which produced `0.12 USDT` from the 0.24-USDT position. KCEX returned the UI error `Minimum order quantity is 0.24 USDT`; event capture showed no `Network.requestWillBeSent` for a private order and no WebSocket order command. Therefore there is no partial-close URL or JSON payload to report for this run—the order was blocked client-side/validation-side before submission.

To obtain a valid 50% test, a position at least twice the minimum is required (approximately 0.48 USDT if the minimum is 0.24 USDT), then a 0.24-USDT close would be valid. Opening that larger new position was outside this already-confirmed sequence, so it was not performed.

## Reconciliation after close

The history response for `positionId=86111367` was:

```json
{"positionId":86111367,"symbol":"TRUMP_USDT","state":3,"holdVol":0,"closeVol":1,"openAvgPrice":2.344,"closeAvgPrice":2.343,"liquidatePrice":2.328,"leverage":75,"closeProfitLoss":-0.0001,"fee":0,"profitRatio":-0.0319,"positionShowStatus":"CLOSED"}
```

The associated fills were:

```json
{"orderId":"850677236655164416","side":1,"vol":1,"price":2.344,"fee":0}
{"orderId":"850678462910268416","side":4,"vol":1,"price":2.343,"fee":0}
```

## Related realtime/read traffic

The futures page continuously used these data families (full redacted request catalog is in the companion files):

- `GET /fapi/v1/contract/ticker?symbol=TRUMP_USDT` — last, fair/mark/index prices, 24-hour stats and funding rate.
- `GET /fapi/v1/contract/depth_step/TRUMP_USDT?step=0.001` — order book.
- `GET /fapi/v1/contract/deals/TRUMP_USDT` — recent trades.
- `GET /fapi/v1/contract/detailV2?client=web` — contract size, tick, min volume, leverage and margin metadata.
- `GET /fapi/v1/private/account/assets` — futures account balances.
- `GET /fapi/v1/private/position/open_positions?...` — active positions.
- `GET /fapi/v1/private/position/list/history_positions?page_num=1&page_size=20` — closed-position reconciliation.
- `GET /fapi/v1/private/order/list/order_deals?...&symbol=TRUMP_USDT` — fills.
- `GET /fapi/v1/private/order/list/history_orders?...&symbol=TRUMP_USDT` — order records.

WebSockets carried ticker, depth-step, deal, one-minute kline, fair/index price and funding channels; heartbeat frames were `{"method":"ping"}`. The realtime frames are high volume and were not copied verbatim into the deliverable; the raw redacted capture records the useful channel classes and HTTP requests.

## Pair parameters and fees observed earlier in the same INR session

TRUMP metadata: `cs=0.1`, `pu=0.001`, `vu=1`, `minV=1`, `maxV=537040`, `minL=1`, `maxL=75`, `mmr=0.0067`, `imr=0.0133`, `tfr=0`, `mfr=0`. The authenticated tier response showed effective maker and taker fees of 0 for this account at capture time. BTC metadata in the same response showed `maxL=125`, `tfr=0.0001`, `mfr=0`. Query both contract detail and tiered-fee endpoints before each bot order because they can change.

The INR display conversion used `GET /api/platform/common/currency/exchange/rate`; the observed rate was `INR=94.4985` per USD. `GET /api/platform/asset/api/asset/overview/convert/v2` supplied display-converted asset values. These are display/risk inputs, not order quantities.

## Security and files

Authorization, signatures, cookies, WebSocket login material, mhash values and device identifiers are not exported. They are session-bound credentials, and replaying or distributing them would expose the account. The raw file therefore contains redacted header placeholders and exact non-secret request bodies only.

- [Redacted staged-close capture](<C:\Users\Samrat Singh\Documents\Codex\2026-09-04\go-to-kcex-com-in-my-2\outputs\kcex_trump_staged_close_capture.redacted.ndjson>)
- [Useful request catalog](<C:\Users\Samrat Singh\Documents\Codex\2026-09-04\go-to-kcex-com-in-my-2\outputs\kcex_trump_staged_close_useful_requests.json>)
- [Earlier INR/session capture](<C:\Users\Samrat Singh\Documents\Codex\2026-09-04\go-to-kcex-com-in-my-2\outputs\kcex_trump_inr_capture_report.md>)
- [Earlier redacted request catalog](<C:\Users\Samrat Singh\Documents\Codex\2026-09-04\go-to-kcex-com-in-my-2\outputs\kcex_trump_inr_network_capture.redacted.ndjson>)
