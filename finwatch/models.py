from enum import Enum


class ExchangeCode(str, Enum):
    """Exchange codes supported by Finnhub"""

    US = "NYSE"
    TO = "TSX"
    BC = "BVC"
