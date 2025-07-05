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
    ParcelType,
    ParcelTypes,
)
from core.di_container import init_container
from services.parcel import ParcelService
from services.cache import CacheService

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
    try:
        print(request.session)
        owner: str = request.session["session_id"]
        parcel_service: ParcelService = container.resolve(ParcelService)
        parcel_id = await parcel_service.new_parcel(
            **new_parcel.model_dump(exclude={"parcel_type"}),
            parcel_type=new_parcel.parcel_type.value,
            owner=owner,
        )
        return ParcelID(parcel_id=parcel_id)
    except KeyError:
        logger.error("Unauthorized access attempt to create parcel")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except Exception as e:
        logger.error("Error creating parcel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get(
    "/types",
    description="Get all types of parcels",
    response_model=ParcelTypes,
)
async def parcel_types(
    container: Container = Depends(init_container),
) -> ParcelTypes:
    try:
        cache: CacheService = container.resolve(CacheService)
        parcel_type_key = "parcel_types"
        cached = await cache.get(parcel_type_key)
        if cached:
            result = cached
        else:
            parcel_service: ParcelService = container.resolve(ParcelService)
            result = await parcel_service.parcel_types()
        p_types = ParcelTypes(parcel_types=[ParcelType.model_validate(pt) for pt in result])
        await cache.set(parcel_type_key, p_types.model_dump_json())
        return p_types
    except Exception as e:
        logger.error("Error creating parcel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


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
    parcel_type: Optional[str] = Query(None, description="Filter by parcel type "),
    has_delivery_cost: bool = Query(
        False, description="Filter by whether delivery cost is calculated"
    ),
    limit: int = Query(100, ge=1, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> Parcels:
    try:
        owner: str = request.session["session_id"]
        key = f"{owner}-{parcel_type}-{has_delivery_cost}-{limit}-{offset}"
        cache: CacheService = container.resolve(CacheService)
        cached = await cache.get(key)

        if cached:
            result = cached
        else:
            parcel_service: ParcelService = container.resolve(ParcelService)

            result = await parcel_service.get_all_parcels(
                owner=owner,
                parcel_type=parcel_type,
                has_delivery_cost=has_delivery_cost,
                limit=limit,
                offset=offset,
            )

        if result:
            parcels = Parcels(parcels=[ParcelOut.model_validate(p) for p in result])
            await cache.set(key, parcels.model_dump_json())
            return parcels

        return Parcels(parcels=[None])
    except HTTPException as e:
        raise e
    except KeyError:
        logger.info("Unauthorized access attempt to create parcel")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except Exception as e:
        logger.error("Error creating parcel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


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
    try:
        cache: CacheService = container.resolve(CacheService)
        cached = await cache.get(parcel_id)

        if cached:
            result = cached
        else:
            parcel_service: ParcelService = container.resolve(ParcelService)
            result = await parcel_service.get_by_id(parcel_id=parcel_id)  # type: ignore

        if not result:
            logger.info("Parcel %s not found", parcel_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")
        parcel = ParcelOut.model_validate(result)
        return parcel
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error creating parcel: : %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
