from typing import Annotated

import typer

from finwatch.external import finnhub
from finwatch.models import ExchangeCode

app = typer.Typer()


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
    print(finnhub.lookup_for_symbols(name, exchange))


@app.command()
def watch(symbol: Annotated[str, typer.Argument(help="Name of the symbol to query.")]):
    """
    Look up the price and fundamentals
    """
    print(finnhub.get_symbol_quote(symbol))
