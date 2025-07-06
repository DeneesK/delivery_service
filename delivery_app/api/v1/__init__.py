__all__ = ("main_router",)

from fastapi import APIRouter

from api.v1.parcel import router as parcel_router
from delivery_app.api.v1.statistics import router as static_router


main_router = APIRouter(prefix="/v1")
main_router.include_router(parcel_router)
main_router.include_router(static_router)
