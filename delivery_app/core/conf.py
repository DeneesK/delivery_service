from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: MySQLDsn
    BROKER_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    DESCRIPTION: str
    MONGO_URL: str
    TTl: int
    MONGO_DB: str
    MONGO_COLLECTION: str
    IS_DEV_MODE: bool = True


def get_config() -> Settings:
    return Settings()  # type: ignore
