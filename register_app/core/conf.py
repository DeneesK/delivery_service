from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    BROKER_URL: str
    DATABASE_URL: MySQLDsn
    CELERY_BACKEND: str
    CURRENCY_RATE_URL: str
    IS_DEV_MODE: bool = True


config = Settings()  # type: ignore
