# KCEX Futures network reconnaissance (DOGE capture + TRUMP execution)

Capture date: 2026-09-04 (Asia/Kolkata). Client build: web-futures v3.7.91, version tag prd - v3.7.91 - fdef20f.

## Outcome

KCEX Futures was opened in Edge. The requested confirmed live action was submitted as a 0.5 USDT TRUMP/USDT market long (isolated, 75x). The UI filled approximately 0.46 USDT at an average entry of 2.342. TP 2.350 / SL 2.330 was entered; KCEX rejected 2.330 while the long's current price was below it, so the stop was temporarily adjusted to 2.327 to satisfy the long-side validation. KCEX displayed a risk warning about the trigger being close to liquidation/current price, which was accepted. The position later disappeared and Position History records it as **Liquidated**: closing quantity 0.46 USDT, average close 2.310, realized PNL 0.00 USDT, yield -100%, open 2026-09-04 06:25:33 and close 06:32:21 (KCEX UI time). Linked Orders shows the liquidation fill and the opening fill; no user-submitted partial close or manual close was sent because liquidation had already closed the position.

The captured artifacts redact Authorization, Content-Sign, Content-time, WebSocket login token, cookies, device identifiers, IP address, and analytics data. Do not hard-code or replay these values; they are session/device/time bound.

## Architecture

Private REST base: https://www.kcex.com/fapi/v1

The client sends Platform: WEB, Language, Accept-Language, Accept-Timezone, Version, Version-tag and User-Device. Private calls use dynamic Authorization, Content-Sign and Content-time headers. The order helper merges the caller payload with priceProtect from local settings and browser fingerprint/mhash fields.

Observed realtime commands:
- {"method":"sub.depth.step","param":{"symbol":"DOGE_USDT","step":"0.00001"}}
- {"method":"sub.deal","param":{"symbol":"DOGE_USDT","compress":true}}
- {"method":"sub.kline","param":{"symbol":"DOGE_USDT","interval":"Min1"}}
- {"method":"sub.funding.rate","param":{"symbol":"DOGE_USDT"}}
- {"method":"sub.fair.price","param":{"symbol":"DOGE_USDT"}}
- {"method":"sub.index.price","param":{"symbol":"DOGE_USDT"}}

The futures socket heartbeat is {"method":"ping"}. A separate market socket uses SUBSCRIPTION with channels including spot@public.miniTickers@24H and spot@public.rateTickers@24H. An account socket uses a login command containing a short-lived token, which is intentionally redacted.

## Read routes

| Need | Route / stream | Notes |
| --- | --- | --- |
| Contract metadata and precision | GET /fapi/v1/contract/detail?type=all | Use for tick, lot, contract size and min amount; never guess these. |
| Ticker | GET /fapi/v1/contract/ticker?symbol=DOGE_USDT | Stream push.ticker includes last/fair/index price, bid1/ask1, 24h stats, funding and OI. |
| Trades | GET /fapi/v1/contract/deals/DOGE_USDT; sub.deal | Stream is push.deal. |
| OHLCV | GET /fapi/v1/contract/kline/DOGE_USDT?interval=Min1&start=...&end=...; sub.kline | Stream push.kline has o,c,h,l,q,a,t. |
| Order book | GET /fapi/v1/contract/depth_step/DOGE_USDT?step=0.00001; sub.depth.step | Stream push.depth.step has asks, bids, version and market-level prices. |
| Funding | GET /fapi/v1/contract/funding_rate/DOGE_USDT; sub.funding.rate | |
| Mark/index | sub.fair.price; sub.index.price | Ticker also carries these. |
| Connectivity | GET /fapi/v1/contract/ping | UI latency probe. |
| Positions | GET /fapi/v1/private/position/open_positions? | Authenticated. |
| Assets | GET /fapi/v1/private/account/assets | Authenticated futures balance. |
| Leverage/mode | GET /private/position/leverage?symbol=DOGE_USDT; GET /private/position/position_mode? | Authenticated. |

## Write lifecycle

| Operation | Method and route | Evidence / payload guidance |
| --- | --- | --- |
| Create order | POST /fapi/v1/private/order/create[?mhash=...] | Direct frontend source. A fast market caller built symbol, side, type:"5", openType, vol, leverage, positionMode and marketCeiling; the helper adds priceProtect/fingerprint data. |
| Amend order price | POST /private/order/change_order_price | Limit alternatives are /private/order/change_limit_order_v1 and /private/order/chase_limit_order. |
| Cancel | POST /private/order/cancel | /private/order/cancel_all also exists. |
| Set position TP/SL | POST /private/stoporder/place/v2[?mhash=...] | Direct frontend helper; priceProtect/fingerprint are added. |
| Edit TP/SL | POST /private/stoporder/change_plan_order or /private/stoporder/change_plan_price | Do not mix stoporder and planorder IDs. |
| Close trigger / partial exit | POST /private/planorder/place/v2[?mhash=...] | Close plan UI constructs triggerPrice, vol, positionMode, price and orderType. |
| Edit/cancel close trigger | POST /private/planorder/change_stop_order, /private/planorder/change_price[_v1], /private/planorder/cancel | |
| Close all positions | POST /private/position/close_all body {} | Global, not a single-pair close. |
| Reverse | POST /private/position/reverse | |

For partial TP/SL, source distinguishes POSITION_VOL from BATCH_VOL and exposes takeProfitPrice, takeProfitVol, stopLossPrice, stopLossVol, volType, takeProfitReverse and stopLossReverse. This is frontend evidence, not a successful write capture; validate on a sacrificial account with a manually confirmed small trade.

## Reconciliation reads

After a write, reconcile using open_positions, order/list/open_orders?page_size=200, planorder/list/orders?page_size=200&states=1, stoporder/open_orders, trackorder/list/orders?pageIndex=1&pageSize=200&states=0,1, order/list/order_deals and account/assets. Persist server IDs and handle reconnect/resubscribe plus book version gaps.

## Fees

The homepage stated 0% futures maker and 0.01% futures taker. One earlier fully rendered futures widget displayed Maker 0% / Taker 0%, which conflicts and may be account-tier/event dependent. Use authenticated GET /fapi/v1/private/account/tiered_fee_rate?... immediately before fee-sensitive logic. No pair-specific fee response was captured.

## Capture scope

The initial general page-load CDP buffer was partly evicted. A later CDP capture on the live TRUMP tab captured the authenticated Position History read (`GET /fapi/v1/private/position/list/history_positions?page_num=1&page_size=20`), REST ping, and live WebSocket ticker/depth/deal/kline/index/fair/funding frames. The companion TRUMP capture file stores request/frame metadata with credentials and large compressed/analytics payloads redacted. The earlier DOGE artifact remains a route/schema reconnaissance file; it is not a claim that a DOGE order was sent.

## Security boundary

Authorization, Content-Sign, Content-time, User-Device, cookies, WebSocket login tokens, mhash values and analytics bodies were observed but are not exported. These are session/device/time-bound credentials; replaying them would be unsafe and brittle. Build a bot around fresh authenticated signing/session handling and the route/payload shapes, not copied browser secrets.
