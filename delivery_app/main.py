from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio import Redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middleware import SessionIDMiddleware
from starlette.middleware.sessions import SessionMiddleware

import db.cache.redis_client
from api.v1 import main_router as v1_router
from core.conf import get_config
from core.di_container import init_container
from db.db import AsyncSessionFactory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    config = get_config()
    db.cache.redis_client.redis = await Redis.from_url(config.REDIS_URL, decode_responses=True)
    container = init_container()
    app.description = config.DESCRIPTION
    yield
    session_factory: AsyncSessionFactory = container.resolve(AsyncSessionFactory)
    redis: Redis = container.resolve(Redis)
    await redis.close()
    await session_factory.close_all()


def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        title="Delivery Service",
        version="1.0.0",
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.add_middleware(SessionIDMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)
    app.include_router(v1_router)
    return app
