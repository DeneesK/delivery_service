import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from punq import Container  # type: ignore

from api.v1.schemas import (
    NewParcel,
    ParcelCreated,
    ParcelID,
    ParcelOut,
    Parcels,
    ParcelTypes,
    CompanyAssigned,
    CompanyAssignRequest,
    ParcelTypeEnum,
)
from core.di_container import init_container
from services.parcel import ParcelService
from services.cache import CacheService
from services.company import CompanyService
from core.exceptions import UnauthorizedError

logger = logging.getLogger("app")
router = APIRouter(prefix="/parcels", tags=["Parcel"])


@router.post(
    "/",
    description="Register the parcel",
    response_model=ParcelID,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "description": "Parcel accepted to register",
            "model": ParcelCreated,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized — missing or invalid session"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def new_parcel(
    request: Request,
    new_parcel: NewParcel,
    container: Container = Depends(init_container),
) -> ParcelID:
    owner: str | None = request.session.get("session_id")
    if not owner:
        raise UnauthorizedError
    parcel_service: ParcelService = container.resolve(ParcelService)
    parcel_id = await parcel_service.new_parcel(
        **new_parcel.model_dump(exclude={"parcel_type"}),
        parcel_type=new_parcel.parcel_type.value,
        owner=owner,
    )
    return ParcelID(parcel_id=parcel_id)


@router.get(
    "/types",
    description="Get all types of parcels",
    response_model=ParcelTypes,
    responses={
        status.HTTP_200_OK: {"description": "Successful retrieval of types", "model": ParcelTypes},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def parcel_types(
    container: Container = Depends(init_container),
) -> ParcelTypes:
    cache: CacheService = container.resolve(CacheService)
    parcel_type_key = "parcel_types"
    cached = await cache.get(parcel_type_key)
    if cached:
        p_types = ParcelTypes.model_validate(cached)
    else:
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.parcel_types()
        p_types = ParcelTypes.model_validate(result)
        await cache.set(parcel_type_key, p_types.model_dump_json())
    return p_types


@router.get(
    "/",
    description="Get all parcels by session",
    responses={
        status.HTTP_200_OK: {"description": "Successful retrieval of parcels", "model": Parcels},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized — missing or invalid session"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    response_model=Parcels,
)
async def get_parcels(
    request: Request,
    container: Container = Depends(init_container),
    parcel_type: Optional[ParcelTypeEnum] = Query(None, description="Filter by parcel type "),
    has_delivery_cost: bool = Query(
        False, description="Filter by whether delivery cost is calculated"
    ),
    limit: int = Query(100, ge=1, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> Parcels:
    owner: str = request.session["session_id"]
    key = f"{owner}-{parcel_type}-{has_delivery_cost}-{limit}-{offset}"
    cache: CacheService = container.resolve(CacheService)
    cached = await cache.get(key)

    if cached:
        parcels = Parcels.model_validate(cached)
    else:
        parcel_service: ParcelService = container.resolve(ParcelService)

        result = await parcel_service.get_all_parcels(
            owner=owner,
            parcel_type=parcel_type,
            has_delivery_cost=has_delivery_cost,
            limit=limit,
            offset=offset,
        )
        parcels = Parcels(parcels=[ParcelOut.model_validate(p) for p in result.parcels])
        await cache.set(key, parcels.model_dump_json())

    return parcels


@router.get(
    "/{parcel_id}",
    description="Get parcel by id",
    responses={
        status.HTTP_200_OK: {"description": "Successful retrieval of parcels", "model": Parcels},
        status.HTTP_404_NOT_FOUND: {"description": "Parcel not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    response_model=ParcelOut,
)
async def get_parcel_by_id(
    parcel_id: str,
    container: Container = Depends(init_container),
) -> ParcelOut:
    cache: CacheService = container.resolve(CacheService)
    cached = await cache.get(parcel_id)
    if cached:
        parcel = ParcelOut.model_validate(cached)
    else:
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.get_by_id(parcel_id=parcel_id)  # type: ignore
        parcel = ParcelOut.model_validate(result)
        await cache.set(parcel_id, parcel.model_dump_json())
    return parcel


@router.post(
    "/{parcel_id}/assign-company",
    description="Assign parcel to a delivery company atomically",
    response_model=CompanyAssigned,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Parcel successfully assigned to company"},
        status.HTTP_404_NOT_FOUND: {"description": "Parcel or company not found"},
        status.HTTP_409_CONFLICT: {"description": "Parcel already assigned"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def assign_company_to_parcel(
    parcel_id: str,
    body: CompanyAssignRequest,
    container: Container = Depends(init_container),
):
    parcel_service: CompanyService = container.resolve(CompanyService)

    success = await parcel_service.assign_to_company(parcel_id, body.company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Parcel already assigned to a company",
        )

    return CompanyAssigned(parcel_id=parcel_id, company_id=body.company_id)
