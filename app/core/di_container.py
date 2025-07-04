from functools import lru_cache

from core.conf import Settings
from db.db import AsyncSessionFactory
from punq import Container, Scope  # type: ignore


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    config: Settings = container.resolve(Settings)  # type: ignore

    container.register(
        AsyncSessionFactory,
        instance=AsyncSessionFactory(
            database_dsn=str(config.DATABASE_URL), echo=config.IS_DEV_MODE
        ),
        scope=Scope.singleton,
    )
    return container
