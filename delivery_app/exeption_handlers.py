import logging

from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from core.exceptions import (
    NotFoundError,
    UnauthorizedError,
    AlreadyAssignedError,
)

logger = logging.getLogger("app")


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    logger.warning(f"404 Not Found: {exc} | URL: {request.url}")
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def validation_exception_handler(request: Request, exc: ValueError):
    logger.info(f"400 Validation Error: {exc} | URL: {request.url}")
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    logger.warning(f"401 Unauthorized: {exc} | URL: {request.url}")
    return ORJSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


async def already_assigned_exception_handler(request: Request, exc: AlreadyAssignedError):
    logger.info(f"409 Conflict (Already Assigned): {exc} | URL: {request.url}")
    return ORJSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"500 Internal Server Error: {exc} | URL: {request.url}", exc_info=True)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
