from rich.console import Console
from rich.table import Table

from finwatch.models import LookupSymbol, Quote


def render_lookup_symbols(table: Table, console: Console, symbols: list[LookupSymbol]):
    if len(symbols) == 0:
        console.print(table)
        return

    for symbol in symbols:
        table.add_row(symbol.name, symbol.ticker_symbol, symbol.type)
    console.print(table)


def render_quote(
    table: Table,
    console: Console,
    symbol: str,
    quote: Quote,
) -> None:
    table.add_row(
        symbol,
        str(quote.current_price),
        str(quote.high_price),
        str(quote.low_price),
        str(quote.open_price),
        str(quote.percent_change),
        str(quote.time),
    )
    console.log(table)
