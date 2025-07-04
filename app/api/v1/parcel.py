from api.v1.schemas import NewParcel, ParcelCreated, ParcelOut, Parcels, ParcelTypes
from core.di_container import init_container
from fastapi import APIRouter, Depends
from punq import Container  # type: ignore

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/parcels",
    description="Register the parcel",
    response_model=ParcelCreated,
)
async def new_parcel(
    user: NewParcel,
    container: Container = Depends(init_container),
) -> None:
    pass


@router.get(
    "/parcel-types",
    description="Get all types of parcels",
    response_model=ParcelTypes,
)
async def parcel_types(
    container: Container = Depends(init_container),
) -> None:
    pass


@router.get(
    "/parcels",
    description="Get all parcels",
    response_model=Parcels,
)
async def get_parcels(
    container: Container = Depends(init_container),
) -> None:
    pass


@router.get(
    "/parcels/{parcel_id}",
    description="Get parcel by id",
    response_model=ParcelOut,
)
async def get_parcel_by_id(
    parcel_id: str,
    container: Container = Depends(init_container),
) -> None:
    pass
