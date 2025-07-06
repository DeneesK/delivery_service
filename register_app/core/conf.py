from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    BROKER_URL: str
    DATABASE_URL: MySQLDsn
    REDIS_URL: str
    CELERY_BACKEND: str
    CURRENCY_RATE_URL: str
    MONGO_URL: str
    MONGO_DB: str
    MONGO_COLLECTION: str
    IS_DEV_MODE: bool = True
