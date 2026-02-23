from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    FINNHUB_API_URL: str = "https://finnhub.io/api/v1"
    FINNHUB_TRADES_WS: str = "wss://ws.finnhub.io"
    FINNHUB_API_KEY: str

    EXCHANGE_RATES_API_URL: str = "https://v6.exchangerate-api.com/v6"
    EXCHANGE_RATES_API_KEY: str


settings = Config()
