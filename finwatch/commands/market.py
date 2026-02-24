import asyncio
from typing import Annotated

import typer

from finwatch.external import finnhub
from finwatch.models import ExchangeCode
from finwatch.ui import render_lookup_symbols, render_quote, render_status

app = typer.Typer()


@app.command()
def status(
    exchange: Annotated[
        ExchangeCode, typer.Option(help="Exchange to get the status of")
    ] = ExchangeCode.US,
):
    status = finnhub.get_market_status(exchange=exchange)
    render_status(status)


@app.command()
def search(
    name: Annotated[str, typer.Argument(help="Symbol's name to search.")],
    exchange: Annotated[
        ExchangeCode,
        typer.Option(
            "--exchange",
            "-e",
            case_sensitive=False,
            help="Exchange to look for the symbols.",
        ),
    ] = ExchangeCode.US,
):
    """
    Search for symbols by NAME, optionally use --exchange to specify an exchange.
    Support for NYSE, TSX, and BVC.
    """
    symbols = finnhub.lookup_for_symbols(query=name, exchange=exchange)
    render_lookup_symbols(symbols)


@app.command()
def watch(
    ticker_symbol: Annotated[str, typer.Argument(help="Name of the symbol to query.")],
):
    """Look up the latest price of a stock."""
    quote = finnhub.get_symbol_quote(ticker_symbol=ticker_symbol)
    render_quote(ticker_symbol, quote)


@app.command()
def stream(
    symbols: Annotated[
        list[str],
        typer.Argument(help="Ticker symbol of the stock to watch in real-time."),
    ],
):
    """Watch a list of stocks moving in real time."""
    try:
        asyncio.run(finnhub.get_trades_with_ws(symbols=symbols))
    except KeyboardInterrupt:
        print("\nStopped Streaming")
