from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    FINNHUB_API_KEY: str
    EXCHANGE_RATE_API_KEY: str


settings = Config()
