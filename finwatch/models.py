from datetime import datetime
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
    ticker_symbol: str = Field(validation_alias="symbol")
    type: LowerString


class Quote(FinnhubBaseModel):
    current_price: float = Field(validation_alias="c")
    high_price: float = Field(validation_alias="h")
    low_price: float = Field(validation_alias="l")
    open_price: float = Field(validation_alias="o")
    change: float = Field(validation_alias="d")
    percent_change: float = Field(validation_alias="pc")
    time: datetime = Field(validation_alias="t")
