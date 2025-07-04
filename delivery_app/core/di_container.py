from functools import lru_cache

from celery import Celery  # type: ignore
from core.conf import Settings
from db.db import AsyncSessionFactory
from punq import Container, Scope  # type: ignore
from services.parcel import ParcelService, get_parcel_service
from task_producer.producer import get_client


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)  # type: ignore
    config: Settings = container.resolve(Settings)  # type: ignore

    container.register(
        AsyncSessionFactory,
        instance=AsyncSessionFactory(
            database_dsn=str(config.DATABASE_URL), echo=config.IS_DEV_MODE
        ),
        scope=Scope.singleton,
    )

    container.register(Celery, instance=get_client(config.BROKER_URL), scope=Scope.singleton)

    session_maker = container.resolve(AsyncSessionFactory)
    task_client = container.resolve(Celery)

    container.register(
        ParcelService,
        instance=get_parcel_service(session_maker, task_client),
        scope=Scope.singleton,
    )

    return container
