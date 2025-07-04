__all__ = ("main_router",)

from api.v1.parcel import router as parcel_router
from fastapi import APIRouter

main_router = APIRouter(prefix="/v1")
main_router.include_router(parcel_router)
