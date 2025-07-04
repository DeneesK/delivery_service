from db.db import AsyncSessionFactory
from db.models.parcel import Parcel, ParcelType
from services.common import DBObjectService
from sqlalchemy import select


class ParcelService(DBObjectService):
    async def new_parcel(
        self, name: str, weight: float, parcel_type: str, content_value_usd: float, owner: str
    ) -> Parcel:
        """Create new parcel"""
        async with self.session_maker() as session:
            async with session.begin():
                parcel = Parcel(
                    name=name,
                    parcel_type=parcel_type,
                    content_value_usd=content_value_usd,
                    owner=owner,
                )
                session.add(parcel)
        return parcel

    async def get_by_id(self, parcel_id: str) -> Parcel | None:
        """Get parcel by parcel_id"""
        async with self.session_maker() as session:
            parcel = await session.get(Parcel, parcel_id)
        return parcel

    async def parcel_types(self) -> list[ParcelType]:
        """Get all parcel's types - name and id"""
        async with self.session_maker() as session:
            result = await session.execute(select(ParcelType))
            return list(result.scalars().all())

    async def get_all_parcels(self, owner: str) -> list[Parcel | None]:
        """Get all parcels by owner"""
        async with self.session_maker() as session:
            result = await session.execute(select(Parcel).where(Parcel.owner == owner))
            return list(result.scalars().all())


def get_parcel_service(session_maker: AsyncSessionFactory) -> ParcelService:
    return ParcelService(session_maker)
