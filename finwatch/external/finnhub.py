from typing import Any

import httpx

from finwatch.config import settings
from finwatch.models import ExchangeCode


def _get_finnhub_request(*, endpoint: str, params: dict[str, Any]) -> Any:
    with httpx.Client(
        base_url=settings.FINNHUB_API_URL,
        timeout=4,
        headers={"X-Finnhub-Token": settings.FINNHUB_API_KEY},
    ) as client:
        response = client.get(url=endpoint, params=params)
    return response.json()


def lookup_for_symbols(query: str, exchange: ExchangeCode) -> Any:
    return _get_finnhub_request(
        endpoint="/search",
        params={"q": query, "exchange": exchange.name},
    )


def get_symbol_quote(symbol_name: str) -> Any:
    return _get_finnhub_request(endpoint="/quote", params={"symbol": symbol_name})
