import json
import time
from decimal import Decimal, InvalidOperation
from playwright.sync_api import sync_playwright


# ============================================================
# CONFIG
# ============================================================

THRESHOLD_USDT = Decimal("0.5")

KCEX_URL = "https://www.kcex.com/futures/exchange/TRUMP_USDT?type=linear_swap"

DETAIL_ENDPOINTS = [
    "/fapi/v1/contract/detailV2?client=web",
    "/fapi/v1/contract/detail?type=all",
]

TICKER_ENDPOINT = "/fapi/v1/contract/ticker"

# Use your normal Edge browser.
BROWSER_CHANNEL = "msedge"


# ============================================================
# HELPERS
# ============================================================

def D(value):
    try:
        if value is None:
            return None
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def recursive_dicts(obj):
    """
    Recursively yield dictionaries from arbitrary JSON.
    """
    if isinstance(obj, dict):
        yield obj

        for value in obj.values():
            yield from recursive_dicts(value)

    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_dicts(item)


def find_first(obj, keys):
    """
    Search recursively for the first numeric value associated
    with any of the specified keys.
    """
    for d in recursive_dicts(obj):
        for key in keys:
            if key in d:
                value = D(d[key])
                if value is not None:
                    return value

    return None


def extract_symbol(d):
    """
    Extract KCEX symbol from a contract/ticker dictionary.
    """
    for key in (
        "symbol",
        "contractCode",
        "contract",
        "instrument",
        "pair",
    ):
        value = d.get(key)

        if isinstance(value, str):
            value = value.upper()

            if value.endswith("_USDT"):
                return value

    return None


def collect_contract_objects(obj):
    """
    Find dictionaries which look like KCEX contract metadata.
    """
    contracts = []

    for d in recursive_dicts(obj):

        symbol = extract_symbol(d)

        if not symbol:
            continue

        min_v = None
        cs = None

        for key in ("minV", "minVol", "minVolume"):
            if key in d:
                min_v = D(d[key])
                if min_v is not None:
                    break

        for key in ("cs", "contractSize", "contract_size"):
            if key in d:
                cs = D(d[key])
                if cs is not None:
                    break

        if min_v is not None and cs is not None:
            contracts.append({
                "symbol": symbol,
                "minV": min_v,
                "cs": cs,
                "raw": d,
            })

    # Deduplicate
    result = {}

    for c in contracts:
        result[c["symbol"]] = c

    return result


def collect_ticker_objects(obj):
    """
    Extract symbol -> current price from arbitrary ticker JSON.
    """
    prices = {}

    for d in recursive_dicts(obj):

        symbol = extract_symbol(d)

        if not symbol:
            continue

        price = None

        for key in (
            "lastPrice",
            "last",
            "fairPrice",
            "markPrice",
        ):
            if key in d:
                price = D(d[key])

                if price is not None and price > 0:
                    break

        if price is not None and price > 0:
            prices[symbol] = price

    return prices


def browser_fetch(page, endpoint):
    """
    Execute fetch() INSIDE the KCEX webpage.

    This means the request is made by the real browser,
    rather than Python requests, so browser/session/security
    handling is preserved.
    """
    result = page.evaluate(
        """
        async (url) => {
            const response = await fetch(url, {
                method: "GET",
                credentials: "include",
                cache: "no-store"
            });

            const text = await response.text();

            return {
                status: response.status,
                ok: response.ok,
                text: text
            };
        }
        """,
        endpoint,
    )

    if not result["ok"]:
        raise RuntimeError(
            f"HTTP {result['status']} from {endpoint}\\n"
            f"Response: {result['text'][:500]}"
        )

    try:
        return json.loads(result["text"])
    except json.JSONDecodeError:
        raise RuntimeError(
            f"Endpoint did not return JSON:\\n"
            f"{result['text'][:500]}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 90)
    print("KCEX FUTURES MINIMUM ORDER SCANNER")
    print("=" * 90)
    print(f"Requirement: minimum order value < {THRESHOLD_USDT} USDT")
    print()

    with sync_playwright() as p:

        print("[1/4] Launching Microsoft Edge...")

        browser = p.chromium.launch(
            channel=BROWSER_CHANNEL,
            headless=False,
        )

        context = browser.new_context(
            viewport={
                "width": 1440,
                "height": 900,
            },
            locale="en-US",
            timezone_id="Asia/Kolkata",
        )

        page = context.new_page()

        print("[2/4] Opening KCEX...")

        try:
            page.goto(
                KCEX_URL,
                wait_until="domcontentloaded",
                timeout=60_000,
            )
        except Exception as e:
            print(f"[WARN] Initial navigation: {e}")

        # Give KCEX JavaScript / anti-bot layer time to initialize.
        page.wait_for_timeout(7000)

        print("[3/4] Reading KCEX contract metadata from browser...")

        contracts = {}

        last_error = None

        for endpoint in DETAIL_ENDPOINTS:

            try:
                data = browser_fetch(page, endpoint)

                contracts = collect_contract_objects(data)

                if contracts:
                    print(
                        f"      Contract endpoint: {endpoint}"
                    )
                    break

            except Exception as e:
                last_error = e

        if not contracts:

            browser.close()

            raise RuntimeError(
                "Could not obtain KCEX contract metadata.\n"
                f"Last error: {last_error}"
            )

        print(
            f"      Found {len(contracts)} USDT contracts."
        )

        print("[4/4] Reading all KCEX ticker prices...")

        prices = {}

        try:
            ticker_data = browser_fetch(
                page,
                TICKER_ENDPOINT,
            )

            prices = collect_ticker_objects(ticker_data)

        except Exception as e:
            print(
                f"[WARN] All-ticker request failed: {e}"
            )

        print(
            f"      Received {len(prices)} ticker prices."
        )

        # ----------------------------------------------------
        # FALLBACK:
        # Fetch missing ticker symbols individually.
        # ----------------------------------------------------

        missing = [
            symbol
            for symbol in contracts
            if symbol not in prices
        ]

        if missing:

            print(
                f"      Fetching {len(missing)} missing prices..."
            )

            for i, symbol in enumerate(
                missing,
                start=1,
            ):

                try:

                    endpoint = (
                        f"{TICKER_ENDPOINT}"
                        f"?symbol={symbol}"
                    )

                    ticker_data = browser_fetch(
                        page,
                        endpoint,
                    )

                    ticker_prices = (
                        collect_ticker_objects(
                            ticker_data
                        )
                    )

                    if symbol in ticker_prices:
                        prices[symbol] = (
                            ticker_prices[symbol]
                        )

                except Exception:
                    pass

        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        qualifying = []

        for symbol, contract in contracts.items():

            price = prices.get(symbol)

            if price is None:
                continue

            min_v = contract["minV"]
            cs = contract["cs"]

            # KCEX convention observed in your captures:
            #
            # Minimum USDT order =
            #     minV × contract_size × current_price

            minimum_usdt = (
                min_v
                * cs
                * price
            )

            if minimum_usdt < THRESHOLD_USDT:

                qualifying.append({
                    "symbol": symbol,
                    "minV": min_v,
                    "cs": cs,
                    "price": price,
                    "minimum_usdt": minimum_usdt,
                })

        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        qualifying.sort(
            key=lambda x: x["minimum_usdt"]
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        print()
        print("=" * 100)
        print(
            f"KCEX PAIRS WITH MINIMUM ORDER < "
            f"{THRESHOLD_USDT} USDT"
        )
        print("=" * 100)

        if not qualifying:

            print("No pairs satisfy the requirement.")

        else:

            print(
                f"{'PAIR':<28}"
                f"{'MIN V':>12}"
                f"{'CONTRACT SIZE':>18}"
                f"{'PRICE':>20}"
                f"{'MIN ORDER USDT':>20}"
            )

            print("-" * 100)

            for row in qualifying:

                print(
                    f"{row['symbol']:<28}"
                    f"{str(row['minV']):>12}"
                    f"{str(row['cs']):>18}"
                    f"{str(row['price']):>20}"
                    f"{str(row['minimum_usdt']):>20}"
                )

        print()
        print("=" * 100)
        print(
            f"Total contracts discovered : "
            f"{len(contracts)}"
        )
        print(
            f"Ticker prices available    : "
            f"{len(prices)}"
        )
        print(
            f"Qualifying pairs           : "
            f"{len(qualifying)}"
        )
        print("=" * 100)

        # ----------------------------------------------------
        # SAVE CSV
        # ----------------------------------------------------

        with open(
            "kcex_pairs_under_0.5usdt.csv",
            "w",
            encoding="utf-8",
        ) as f:

            f.write(
                "symbol,minV,contract_size,"
                "price,min_order_usdt\n"
            )

            for row in qualifying:

                f.write(
                    f"{row['symbol']},"
                    f"{row['minV']},"
                    f"{row['cs']},"
                    f"{row['price']},"
                    f"{row['minimum_usdt']}\n"
                )

        print()
        print(
            "Saved: kcex_pairs_under_0.5usdt.csv"
        )

        browser.close()


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nStopped.")

    except Exception as e:
        print()
        print("=" * 90)
        print("ERROR")
        print("=" * 90)
        print(e)