import pytest
import httpx
from fastapi import status

BASE_URL = "http://delivery_app_test:8000/v1"


@pytest.mark.asyncio
async def test_get_statistics_all_types():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/daily-statics/", params={"date": "2025-07-06"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        for item in data["data"]:
            assert "parcel_type" in item
            assert "total_cost" in item
            assert "date" in item


@pytest.mark.asyncio
async def test_get_statistics_with_type():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/daily-statics/",
            params={"date": "2025-07-06", "parcel_type": "clothes"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        for item in data["data"]:
            assert item["parcel_type"] == "clothes"
