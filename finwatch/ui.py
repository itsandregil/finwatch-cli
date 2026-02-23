from datetime import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from finwatch.models import LookupSymbol, MarketStatus, Quote

ModelDump = dict[str, Any]


def _get_table_header(
    dump: ModelDump,
    title: str | None = None,
) -> Table:
    if title is not None:
        return Table(*dump.keys(), title=title)
    return Table(*dump.keys())


def _print_table(table: Table) -> None:
    console = Console()
    console.print(table)


def _get_renderable_data(dump: ModelDump, keep_time: bool = True):
    renderable_data = {}
    for att, value in dump.items():
        if isinstance(value, datetime) and keep_time:
            renderable_data[att] = str(value.date())
            continue
        renderable_data[att] = str(value)
    return renderable_data.values()


def render_lookup_symbols(symbols: list[LookupSymbol]):
    if len(symbols) == 0:
        print("No symbols found")
        return

    table = _get_table_header(symbols[0].model_dump())
    for symbol in symbols:
        renderables = _get_renderable_data(symbol.model_dump())
        table.add_row(*renderables)
    _print_table(table)


def render_quote(
    symbol: str,
    quote: Quote,
) -> None:
    data = quote.model_dump(exclude={"percent_change"})
    table = _get_table_header(data, title=f"Quote for {symbol}")
    renderables = _get_renderable_data(data)
    table.add_row(*renderables)
    _print_table(table)


def render_status(status: MarketStatus) -> None:
    data = status.model_dump()
    table = _get_table_header(data)
    renderables = _get_renderable_data(data, keep_time=False)
    table.add_row(*renderables)
    _print_table(table)
