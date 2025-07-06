from functools import lru_cache
from redis import Redis
from punq import Container, Scope  # type: ignore
from pymongo.collection import Collection
from sqlalchemy.orm import Session, sessionmaker

from core.conf import Settings
from db.cache import get_cache
from db.db import get_db_session_maker
from db.mongo_db import get_mongo_collection


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)  # type: ignore
    config: Settings = container.resolve(Settings)  # type: ignore

    container.register(Redis, instance=get_cache(config.REDIS_URL), scope=Scope.singleton)

    SessionMaker = get_db_session_maker(str(config.DATABASE_URL))
    container.register(sessionmaker, instance=SessionMaker, scope=Scope.singleton)

    container.register(
        Session,
        factory=lambda: container.resolve(sessionmaker)(),
        scope=Scope.transient,
    )

    container.register(
        Collection,
        instance=get_mongo_collection(config.MONGO_URL, config.MONGO_DB, config.MONGO_COLLECTION),
        scope=Scope.singleton,
    )

    return container
