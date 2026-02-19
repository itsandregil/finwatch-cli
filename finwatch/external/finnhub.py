from typing import Any

from httpx import Client
from tenacity import retry, wait_exponential

from finwatch.config import settings
from finwatch.models import ExchangeCode, LookupSymbol, Quote

# TODO: Handle validation and request errors properly


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def _get_finnhub_request(*, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    with Client(
        base_url=settings.FINNHUB_API_URL,
        timeout=4,
        headers={"X-Finnhub-Token": settings.FINNHUB_API_KEY},
    ) as client:
        response = client.get(url=endpoint, params=params)
    return response.json()


def lookup_for_symbols(*, query: str, exchange: ExchangeCode) -> list[LookupSymbol]:
    result = _get_finnhub_request(
        endpoint="/search",
        params={"q": query, "exchange": exchange.name},
    )
    symbols = result.get("result", [])
    return [LookupSymbol.model_validate(symbol) for symbol in symbols]


def get_symbol_quote(*, ticker_symbol: str) -> Quote:
    result = _get_finnhub_request(endpoint="/quote", params={"symbol": ticker_symbol})
    return Quote.model_validate(result)
