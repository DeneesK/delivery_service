from uuid import uuid4

import anyio
import anyio.to_thread
from celery import Celery  # type: ignore
from sqlalchemy import select

from db.db import AsyncSessionFactory
from db.models.parcel import Parcel, ParcelType
from services.common import DBObjectService
from dto.parcel_dto import ParcelDTO, ParcelsDTO, ParcelTypesDTO, ParcelTypeDTO


class ParcelService(DBObjectService):
    """
    Service for working with parcels.

    Methods allow you to create, receive and update parcel data in the database.
    """

    def __init__(self, session_maker: AsyncSessionFactory, task_client: Celery) -> None:
        super().__init__(session_maker)
        self.task_client = task_client

    async def new_parcel(
        self, name: str, weight: float, parcel_type: str, content_value_usd: float, owner: str
    ) -> str:
        """Send task to register new parcel"""
        parcel_id = str(uuid4())
        parcel_data = {
            "name": name,
            "weight": weight,
            "parcel_type": parcel_type,
            "content_value_usd": content_value_usd,
            "owner": owner,
            "parcel_id": parcel_id,
        }
        await anyio.to_thread.run_sync(
            lambda: self.task_client.send_task("consumer.tasks.register_parcel_task", [parcel_data])
        )
        return parcel_id

    async def get_by_id(self, parcel_id: str) -> ParcelDTO | None:
        """Get parcel by parcel_id"""
        async with self.session_maker() as session:
            parcel = await session.get(Parcel, parcel_id)
            if parcel:
                return ParcelDTO.model_validate(parcel)
            return None

    async def parcel_types(self) -> ParcelTypesDTO:
        """Get all parcel's types - name and id"""
        async with self.session_maker() as session:
            result = await session.execute(select(ParcelType))
            _types = result.scalars().all()
            return ParcelTypesDTO(parcel_types=[ParcelTypeDTO.model_validate(t) for t in _types])

    async def get_all_parcels(
        self,
        owner: str,
        parcel_type: str | None,
        has_delivery_cost: bool,
        limit: int = 100,
        offset: int = 0,
    ) -> ParcelsDTO:
        """Get all parcels by owner, optionally filtered"""
        async with self.session_maker() as session:
            stmt = select(Parcel).where(Parcel.owner == owner)

            if parcel_type:
                stmt = stmt.where(Parcel.parcel_type == parcel_type)

            if has_delivery_cost:
                stmt = stmt.where(Parcel.delivery_cost_rub.is_not(None))
            else:
                stmt = stmt.where(Parcel.delivery_cost_rub.is_(None))

            stmt = stmt.offset(offset).limit(limit)

            result = await session.execute(stmt)
            return ParcelsDTO(parcels=[ParcelDTO.model_validate(p) for p in result.scalars().all()])


def get_parcel_service(session_maker: AsyncSessionFactory, task_client: Celery) -> ParcelService:
    return ParcelService(session_maker, task_client)
