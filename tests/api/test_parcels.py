import time

import pytest
import httpx
from fastapi import status

BASE_URL = "http://delivery_app_test:8000/v1"


@pytest.mark.asyncio
async def test_register_parcel_success():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/parcels/",
            json={
                "name": "Test Parcel",
                "weight": 1.0,
                "parcel_type": "clothes",
                "content_value_usd": 100.0,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "parcel_id" in response.json()


@pytest.mark.asyncio
async def test_get_parcel_types():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/parcels/types")
        assert response.status_code == status.HTTP_200_OK
        assert "parcel_types" in response.json()


@pytest.mark.asyncio
async def test_get_all_parcels_empty():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/parcels/")
        assert response.status_code == status.HTTP_200_OK
        json_data = response.json()
        assert "parcels" in json_data
        assert isinstance(json_data["parcels"], list)


@pytest.mark.asyncio
async def test_get_all_parcels_with_filter():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/parcels/?parcel_type=clothes&has_delivery_cost=false&limit=10&offset=0",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "parcels" in response.json()


@pytest.mark.asyncio
async def test_get_parcel_by_id_not_found():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/parcels/00000000-0000-0000-0000-000000000000")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_parcel_by_id_success():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        create_response = await client.post(
            "/parcels/",
            json={
                "name": "Test Parcel",
                "weight": 1.0,
                "parcel_type": "clothes",
                "content_value_usd": 100.0,
            },
        )
        assert create_response.status_code == status.HTTP_202_ACCEPTED
        parcel_id = create_response.json()["parcel_id"]
        time.sleep(2)
        get_response = await client.get(f"/parcels/{parcel_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["parcel_id"] == parcel_id
