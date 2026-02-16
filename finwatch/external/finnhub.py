import httpx

from finwatch.config import settings
from finwatch.models import ExchangeCode


def lookup_for_symbols(query: str, exchange: ExchangeCode):
    with httpx.Client(base_url="https://finnhub.io/api/v1") as client:
        response = client.get(
            "/search",
            params={"q": query, "exchange": exchange.name},
            headers={"X-Finnhub-Token": settings.FINNHUB_API_KEY},
            timeout=3,
        )
    return response.json()
