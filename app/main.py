from contextlib import asynccontextmanager
from typing import AsyncGenerator

from api.v1 import main_router as v1_router
from core.conf import Settings
from core.di_container import init_container
from db.db import AsyncSessionFactory
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middleware import SessionIDMiddleware
from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container = init_container()
    config: Settings = container.resolve(Settings)

    app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)
    app.add_middleware(SessionIDMiddleware)

    app.description = config.DESCRIPTION
    yield
    session_factory: AsyncSessionFactory = container.resolve(AsyncSessionFactory)
    await session_factory.close_all()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Delivery Service",
        version="1.0.0",
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    app.include_router(v1_router)
    return app
