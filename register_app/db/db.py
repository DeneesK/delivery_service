from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.conf import config

engine: Engine = create_engine(str(config.DATABASE_URL), pool_pre_ping=True)  # type: ignore

SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=False, autocommit=False)
