import json
from typing import Any

from websockets import ClientConnection

from finwatch.models import TickerState, Trade


def handle_trades(payload: Any) -> list[Trade] | None:
    if payload.get("type") != "trade":
        return None
    return [Trade.model_validate(trade) for trade in payload.get("data", {})]


async def subscribe_to_symbols(symbols: list[str], *, ws: ClientConnection) -> None:
    for symbol in symbols:
        message = {"type": "subscribe", "symbol": symbol}
        await ws.send(json.dumps(message))


def update_state(state: TickerState, trade: Trade) -> None:
    if state.open_price == 0:
        state.open_price = trade.last_price
    state.last_price = trade.last_price
    state.volume += trade.volume
    state.trade_count += 1
