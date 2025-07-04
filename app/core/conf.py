from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: MySQLDsn
    SECRET_KEY: str
    DESCRIPTION: str
    IS_DEV_MODE: bool = True
