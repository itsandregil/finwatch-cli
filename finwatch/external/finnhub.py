import json
from typing import Any

import websockets
from httpx import Client
from rich.live import Live

from finwatch.config import settings
from finwatch.external.utils import (
    handle_trades,
    subscribe_to_symbols,
    update_state,
)
from finwatch.models import ExchangeCode, LookupSymbol, MarketStatus, Quote, TickerState
from finwatch.ui import render_trade_states

# TODO: Handle validation and request errors properly
# TODO: Cache requests that do not change in result


def _get_finnhub_request(*, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    with Client(
        base_url=settings.FINNHUB_API_URL,
        timeout=4,
        headers={"X-Finnhub-Token": settings.FINNHUB_API_KEY},
    ) as client:
        response = client.get(url=endpoint, params=params)
    return response.json()


def get_market_status(*, exchange: ExchangeCode) -> MarketStatus:
    data = _get_finnhub_request(
        endpoint="/stock/market-status",
        params={"exchange": exchange.name},
    )
    return MarketStatus.model_validate(data)


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


async def get_trades_with_ws(*, symbols: list[str]):
    "Get real-time price changes using websockets"
    states = {symbol: TickerState(symbol=symbol) for symbol in symbols}

    async with websockets.connect(
        f"{settings.FINNHUB_TRADES_WS}?token={settings.FINNHUB_API_KEY}"
    ) as ws:
        await subscribe_to_symbols(symbols, ws=ws)

        try:
            with Live(render_trade_states(states), refresh_per_second=10) as live:
                while True:
                    message = await ws.recv()
                    trades = handle_trades(json.loads(message))
                    if trades is None:
                        continue
                    for trade in trades:
                        update_state(states[trade.symbol], trade)
                live.update(render_trade_states(states))
        except websockets.ConnectionClosed:
            print("Connection closed")
