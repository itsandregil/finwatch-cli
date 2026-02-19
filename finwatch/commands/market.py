from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from finwatch.external import finnhub
from finwatch.models import ExchangeCode
from finwatch.ui import render_lookup_symbols, render_quote

app = typer.Typer()
console = Console()


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
    table = Table("Name", "Symbol", "Type")
    render_lookup_symbols(table, console, symbols)


@app.command()
def watch(
    ticker_symbol: Annotated[str, typer.Argument(help="Name of the symbol to query.")],
):
    """
    Look up the latest price of a stock.
    """
    quote = finnhub.get_symbol_quote(ticker_symbol=ticker_symbol)
    table = Table(
        "Ticker Symbol",
        "Current Price",
        "High",
        "Low",
        "Open",
        "% Change",
        "Time",
    )
    render_quote(table, console, ticker_symbol, quote)
