import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_DIR = os.path.join(BASE_DIR, "delivery_app")

sys.path.insert(0, APP_DIR)
sys.path.insert(0, BASE_DIR)

import pytest  # noqa
from fastapi import FastAPI  # noqa
from fastapi.testclient import TestClient  # noqa
from unittest.mock import AsyncMock, MagicMock  # noqa

from delivery_app.services.parcel import ParcelService  # noqa
from delivery_app.services.cache import CacheService  # noqa


@pytest.fixture
def app(monkeypatch):
    def mock_init_container():
        pass

    import delivery_app.core.di_container as container

    monkeypatch.setattr(container, "init_container", mock_init_container)
    app = FastAPI()

    from delivery_app.api.v1 import main_router

    monkeypatch.setattr(container, "init_container", mock_init_container)
    app.include_router(main_router)
    monkeypatch.setattr(container, "init_container", mock_init_container)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_session():
    mock_result = MagicMock()
    mock_result.parcel_id = "1234"
    mock_result.scalars.all = MagicMock(return_value=[])

    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_result)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session


@pytest.fixture
def mock_task_client():
    mock_task_client = AsyncMock()
    mock_task_client.send_task = AsyncMock()
    return mock_task_client


@pytest.fixture
def mock_parcel_service(mock_session, mock_task_client):
    mock_session_context_manager = MagicMock()
    mock_session_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_context_manager.__aexit__ = AsyncMock(return_value=None)

    service = ParcelService(
        session_maker=MagicMock(return_value=mock_session_context_manager),
        task_client=mock_task_client,
    )
    return service


@pytest.fixture
def redis_mock():
    return AsyncMock()


@pytest.fixture
def cache_service(redis_mock):
    return CacheService(cache_client=redis_mock, ttl=60)
