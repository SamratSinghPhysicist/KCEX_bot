# KCEX futures maker/taker fee capture and screener

## Correction to the first margin calculation

The first pass used `minimum_volume / max_leverage`. That was wrong because KCEX's `minV` is contract volume, not USDT notional. The corrected calculation is:

```text
minimum_notional_usdt = minimum_volume * contract_size * mark_price
minimum_margin_usdt = minimum_notional_usdt / max_leverage
```

This explains the checks you reported:

- `FARTCOIN_USDT`: `1 * 100 * 0.1798 / 75 = 0.2397333 USDT` (about 0.24).
- `PEPE_USDT`: `1 * 100000 * 0.000003624 / 75 = 0.004832 USDT`.

The Python screener and README have been corrected. A ticker response containing mark/fair/last prices is now required for a truthful USDT margin result; rows without a price are left blank instead of being misclassified.

Capture date: 2026-09-07. The Edge tab was on the KCEX TRUMP/USDT futures page. No order was placed or changed during this capture.

## Finding

The fee values shown in the futures right panel are present in the contract metadata response, rather than requiring a separate fee request for each pair:

```text
GET https://www.kcex.com/fapi/v1/contract/detailV2?client=web
```

For each contract record, the useful fields are:

| Field | Meaning |
|---|---|
| `symbol` | Pair, e.g. `TRUMP_USDT` |
| `mfr` | Maker fee rate as a decimal (`0` = 0%) |
| `tfr` | Taker fee rate as a decimal (`0.0001` = 0.01%) |
| `maxL` | Maximum leverage |
| `minV` | Minimum order volume in KCEX's contract-volume unit |
| `cs` | Contract size |
| `pu` | Price tick |
| `mmr`, `imr` | Maintenance/initial margin rates |

Examples captured from the response:

- `TRUMP_USDT`: maker 0%, taker 0%, max leverage 75x, minimum volume 1.
- `DOGE_USDT`: maker 0%, taker 0%, max leverage 75x, minimum volume 1.
- `BTC_USDT`: maker 0%, taker 0.01%, max leverage 125x, minimum volume 1.
- `ETH_USDT`: maker 0%, taker 0.01%, max leverage 125x, minimum volume 1.

The requested screening formula is:

```text
minimum_notional_usdt = minimum_volume * contract_size * mark_price
minimum_margin_usdt = minimum_notional_usdt / max_leverage
```

This preserves KCEX's volume unit. It is not silently converted to notional USDT; use `cs` and a current price if the bot needs notional exposure.

## Counts from the captured response

- USDT-margined contract records inspected: **1,698**.
- Maker = 0 and taker = 0: **371 pairs**.
- The earlier 15-pair result was based on the incorrect formula and should not be used.
- A fresh full browser capture of the contract metadata plus the bulk ticker returned **371 zero-fee pairs** and **9 pairs** meeting the corrected ≤ 0.03 USDT margin filter.
- The corrected result is [zero_fee_75x_margin_le_0.03.json](kcex_fee_screen_corrected_run/zero_fee_75x_margin_le_0.03.json).

The complete zero-fee symbol list is in [kcex_zero_fee_symbols.txt](kcex_zero_fee_symbols.txt). The full-capture corrected qualifying output is [zero_fee_75x_margin_le_0.03.json](kcex_fee_screen_corrected_run/zero_fee_75x_margin_le_0.03.json). The accompanying `all_pairs.csv` is a local fixture run used to verify the corrected formula; the earlier `kcex_fee_screen_run` 15-row file is historical and must not be used for margin decisions.

Corrected validation examples (all have minimum volume 1):

| Pair | Max leverage | Minimum margin |
|---|---:|---:|
| DOGE_USDT | 75x | 0.0120173 |
| TRUMP_USDT | 75x | 0.0030840 |
| PEPE_USDT | 75x | 0.0048227 |
| PENGU_USDT | 75x | 0.0116547 |
| BONK_USDT | 75x | 0.0044947 |
| SHIB_USDT | 75x | 0.0073000 |
| SPX_USDT | 75x | 0.0075613 |
| WIF_USDT | 75x | 0.0028733 |
| MELANIA_USDT | 75x | 0.0001506 |

`FARTCOIN_USDT` remains zero-fee and 75x, but is correctly excluded because its current mark price made the minimum margin approximately **0.2397333 USDT**.

## Requests saved

The new redacted request log is [kcex_fee_network_capture.redacted.ndjson](kcex_fee_network_capture.redacted.ndjson). It records the fee source request, risk-limit cross-check, currency-rate request, and related contract-service requests. Authorization, cookies, `User-Device`, signatures, and other session credentials are deliberately represented as `<redacted>` and were not written to disk.

## Python

The reusable screener is [kcex_pair_screen.py](../kcex_pair_screen.py). It now understands `mfr`/`tfr` embedded in `contract/detailV2`, while still accepting a separate fee response. The local run used the redacted contract fixture [kcex_fee_contract_fixture.json](kcex_fee_contract_fixture.json) and produced [summary.json](kcex_fee_screen_run/summary.json), [all_pairs.csv](kcex_fee_screen_run/all_pairs.csv), and the two JSON lists.

Run it with a saved KCEX contract-detail response and the pasted risk-limit response:

```powershell
python .\kcex_pair_screen.py `
  --risk-limit .\pasted-text.txt `
  --contracts .\contract_detailV2.json `
  --out-dir .\pair_screen_output
```

The script performs no authenticated requests and does not require browser credentials.
