import logging

from api.v1.schemas import NewParcel, ParcelCreated, ParcelOut, Parcels, ParcelTypes
from core.di_container import init_container
from fastapi import APIRouter, Depends, HTTPException, Request, status
from punq import Container  # type: ignore
from services.parcel import ParcelService

logger = logging.getLogger("app")
router = APIRouter(prefix="/parcels", tags=["Parcel"])


@router.post(
    "/",
    description="Register the parcel",
    response_model=ParcelCreated,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Parcel created successfully",
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
) -> ParcelCreated:
    try:
        owner: str = request.session["session_id"]
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.new_parcel(
            **new_parcel.model_dump(exclude={"parcel_type"}),
            parcel_type=new_parcel.parcel_type.value,
            owner=owner,
        )
        out_parcel = ParcelCreated.model_validate(result)
        return out_parcel
    except KeyError:
        logger.warning("Unauthorized access attempt to create parcel")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except Exception as e:
        logger.error(f"Error creating parcel: {e}", exc_info=True)
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
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.parcel_types()
        parcel_types = ParcelTypes.model_validate(result)
        return parcel_types
    except Exception as e:
        logger.error(f"Error creating parcel: {e}", exc_info=True)
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
) -> Parcels:
    try:
        owner: str = request.session["session_id"]
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.get_all_parcels(owner=owner)
        parcels = Parcels.model_validate(result)
        return parcels
    except KeyError:
        logger.info("Unauthorized access attempt to create parcel")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except Exception as e:
        logger.error(f"Error creating parcel: {e}", exc_info=True)
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
        parcel_service: ParcelService = container.resolve(ParcelService)
        result = await parcel_service.get_by_id(parcel_id=parcel_id)
        if not result:
            logger.info("Parcel %s not found", parcel_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")
        parcel = ParcelOut.model_validate(result)
        return parcel
    except Exception as e:
        logger.error(f"Error creating parcel: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
