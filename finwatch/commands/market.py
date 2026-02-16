from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from finwatch.models import ExchangeCode
from finwatch.services import stock_service

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
    response = stock_service.get_stocks_by_name(name, exchange)
    table = Table("Name", "Symbol", "Type", title="Symbols found!")
    for symbol in response.symbols:
        table.add_row(symbol.name, symbol.symbol, symbol.type)
    console.print(table)


@app.command()
def watch(symbol: Annotated[str, typer.Argument(help="Name of the symbol to query.")]):
    """
    Look up the price and fundamentals
    """
    pass
