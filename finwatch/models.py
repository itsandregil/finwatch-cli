from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer


class ExchangeCode(str, Enum):
    """Exchange codes supported by Finnhub"""

    US = "NYSE"
    TO = "TSX"
    BC = "BVC"


LowerString = Annotated[str, PlainSerializer(lambda s: s.lower())]


class FinnhubBaseModel(BaseModel):
    model_config = {"validate_by_alias": True}


class LookupSymbol(FinnhubBaseModel):
    name: str = Field(validation_alias="description")
    symbol: str
    type: LowerString


class SymbolLookupResponse(FinnhubBaseModel):
    count: int
    symbols: list[LookupSymbol] = Field(validation_alias="result")


class QuoteResponse(FinnhubBaseModel):
    pass
