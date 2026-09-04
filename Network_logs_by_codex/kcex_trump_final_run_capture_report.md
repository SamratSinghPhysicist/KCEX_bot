# KCEX TRUMP/USDT final-run capture report

Capture date: 2026-09-04 (Asia/Kolkata)  
Browser: Microsoft Edge  
Page: `https://www.kcex.com/futures/exchange/TRUMP_USDT?type=linear_swap`  
Interface currency: INR

## Final state

The TRUMP/USDT isolated 75x long is closed. KCEX currently shows `Open Position(0)` and `Open Order (0)`.

## Actions observed in this run

1. Market long opened with no TP/SL at creation. The position panel showed approximately `0.48 USDT` exposure (the order-history display rounds the filled amount to `0.47 USDT`).
2. Position TP/SL added: TP `2.400`, SL `2.350`.
3. Position TP/SL amended: TP `2.410`, SL `2.355`. KCEX displayed an order-submission-success message and the row changed to `Position 2.410 / 2.355`.
4. A 50% close was selected (`0.24 USDT`). The request initially remained pending while the browser capture was being released; after release KCEX reported `Order submission successful` and the remaining position became `0.24 USDT`. No separate 75% close was executed.
5. The remaining `0.24 USDT` was closed at 100% market close. The UI now shows no open position.

Current Order History rows for this run:

| Time | Direction | Filled price | Filled quantity | Status |
|---|---|---:|---:|---|
| 07:59:34 | Open Long | 2.363 (Market) | 0.47 USDT | Filled |
| 08:10:18 | Close Long (partial) | 2.365 (Market) | 0.23 USDT | Filled |
| 08:10:56 | Close Long (final) | 2.366 | 0.23 USDT | Filled |

The detail view for the final row reported fill time `08:10:59`, filled quantity `0.23 USDT`, filled price `2.366`, fee `0.00 USDT`, role `Maker`.

## Exact endpoint information

The frontend route used for position TP/SL placement is:

```http
POST https://www.kcex.com/fapi/v1/private/stoporder/place/v2
```

The frontend route used for market open/close orders is:

```http
POST https://www.kcex.com/fapi/v1/private/order/create
```

The exact current-run TP/SL and close POST bodies were not retained by the finite CDP event buffer after the browser released the pending close request. I am not fabricating bodies from UI state. The previously captured exact successful close body (same KCEX market-close schema, from the companion staged-close capture) is:

```json
{"symbol":"TRUMP_USDT","openType":1,"positionId":86111367,"leverage":75,"type":1,"vol":1,"side":4,"flashClose":false,"price":"2.341","priceProtect":"0"}
```

Its response was:

```json
{"success":true,"code":0,"data":{"orderId":"850678462910268416","ts":1788487950408}}
```

For this final run, the UI history confirms two filled close legs of approximately `0.23 USDT` each, but the position/order IDs and raw bodies are not exposed in the UI detail dialog.

## Related read/realtime traffic

The redacted raw catalogs record these read families:

- `GET /fapi/v1/contract/ticker?symbol=TRUMP_USDT` — last, mark/fair/index, 24-hour stats and funding.
- `GET /fapi/v1/contract/depth_step/TRUMP_USDT?step=0.001` — order book.
- `GET /fapi/v1/contract/deals/TRUMP_USDT` — recent trades.
- `GET /fapi/v1/contract/detailV2?client=web` — contract size, tick, minimum volume, leverage and margin metadata.
- `GET /fapi/v1/private/account/assets` — account balances.
- `GET /fapi/v1/private/position/open_positions?...` — active positions.
- `GET /fapi/v1/private/position/list/history_positions?page_num=1&page_size=20` — closed-position history.
- `GET /fapi/v1/private/order/list/order_deals?...&symbol=TRUMP_USDT` — fills.
- `GET /fapi/v1/private/order/list/history_orders?...&symbol=TRUMP_USDT` — order history.
- `GET /api/platform/common/currency/exchange/rate` — display FX rate; earlier INR observation was `94.4985` per USD.

WebSockets carried ticker, depth-step, deal, one-minute kline, fair/index price and funding channels; heartbeat frames used `{"method":"ping"}`.

## Pair constraints and fees previously observed

TRUMP metadata observed in the same INR session: contract size `cs=0.1`, tick `pu=0.001`, minimum volume `minV=1`, maximum leverage `maxL=75`, maintenance margin ratio `mmr=0.0067`, initial margin ratio `imr=0.0133`, maker/taker fee fields `mfr=0`, `tfr=0`. The authenticated tier response showed effective maker and taker fees of 0 for this account at capture time. Re-query contract detail and fee-tier endpoints before relying on these values in a bot.

## Security handling

Authorization, signatures, cookies, WebSocket login payloads, mhash values and device identifiers are deliberately redacted. The raw file preserves non-secret URLs, methods, bodies and UI/reconciliation facts only.

