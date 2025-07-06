from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.conf import config


def get_db_session_maker(DB_URL: str) -> sessionmaker[Session]:
    engine: Engine = create_engine(str(config.DATABASE_URL), pool_pre_ping=True)  # type: ignore
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
