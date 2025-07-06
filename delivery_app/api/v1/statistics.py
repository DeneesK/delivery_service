import logging
from datetime import datetime

from fastapi import APIRouter, Query, Depends, HTTPException, status
from punq import Container  # type: ignore

from core.di_container import init_container
from api.v1.schemas import DailyStatisticsResponse, ParcelTypeEnum, StatisticsOut
from services.statistics import StatisticsService
from services.cache import CacheService


router = APIRouter(prefix="/daily-statics", tags=["Statics"])

logger = logging.getLogger("app")


@router.get(
    "/",
    response_model=DailyStatisticsResponse,
    description="calculation of the sum of the delivery costs of all parcels by type per day",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful retrieval of costs of all parcels by type per day",
            "model": DailyStatisticsResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_statistics(
    date: datetime = Query(..., description="date exp.: YYYY-MM-DD"),
    parcel_type: ParcelTypeEnum | None = Query(None, description="Parcel type(optional)"),
    container: Container = Depends(init_container),
):
    try:
        cache: CacheService = container.resolve(CacheService)
        key = f"{date}-{parcel_type.value if parcel_type else "all"}"
        cached = await cache.get(key)
        if cached:
            static = DailyStatisticsResponse.model_validate(cached)
        else:
            parcel_service: StatisticsService = container.resolve(StatisticsService)
            result = await parcel_service.get_daily_costs(date, parcel_type)
            static = DailyStatisticsResponse(
                data=[StatisticsOut.model_validate(s) for s in result.data]
            )
            await cache.set(key, static.model_dump_json())
        return static
    except Exception as e:
        logger.error("Error getting statistics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
