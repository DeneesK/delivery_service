from functools import lru_cache

from redis.asyncio import Redis
from celery import Celery  # type: ignore
from punq import Container, Scope  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient

from core.conf import Settings, get_config
from db.db import AsyncSessionFactory
from services.parcel import ParcelService, get_parcel_service
from task_producer.producer import get_client
from db.cache.redis_client import get_redis
from db.log_db.mongo_db import get_mongo_client
from services.cache import CacheService, get_cache_service
from services.statistics import StatisticsService, get_static_service


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, factory=get_config, scope=Scope.singleton)  # type: ignore
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
        Redis,
        instance=get_redis(),
        scope=Scope.singleton,
    )

    container.register(
        ParcelService,
        instance=get_parcel_service(session_maker, task_client),
        scope=Scope.singleton,
    )

    cache_client = container.resolve(Redis)

    container.register(
        CacheService,
        instance=get_cache_service(cache_client, config.TTl),
        scope=Scope.singleton,
    )

    container.register(
        AsyncIOMotorClient,
        instance=get_mongo_client(config.MONGO_URL),
        scope=Scope.singleton,
    )

    mongo_client = container.resolve(AsyncIOMotorClient)

    container.register(
        StatisticsService,
        instance=get_static_service(mongo_client, config.MONGO_DB, config.MONGO_COLLECTION),
        scope=Scope.singleton,
    )

    return container
