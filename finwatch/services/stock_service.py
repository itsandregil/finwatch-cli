from finwatch.external import finnhub
from finwatch.models import ExchangeCode, SymbolLookupResponse


def get_stocks_by_name(
    symbol_name: str,
    exchange: ExchangeCode,
) -> SymbolLookupResponse:
    result = finnhub.lookup_for_symbols(symbol_name, exchange)
    response = SymbolLookupResponse.model_validate(result, by_alias=True)
    return response


def get_stock_symbol(symbol_name: str):
    pass
