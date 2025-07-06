from sqlalchemy import update

from services.common import DBObjectService
from db.models.parcel import Parcel
from db.db import AsyncSessionFactory


class CompanyService(DBObjectService):

    async def assign_to_company(self, parcel_id: str, company_id: int) -> bool:
        """Try to assign parcel to a delivery company atomically"""
        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Parcel)
                    .where(Parcel.parcel_id == parcel_id, Parcel.company_id.is_(None))
                    .values(company_id=company_id)
                )
                result = await session.execute(stmt)
                return result.rowcount > 0


def get_parcel_service(session_maker: AsyncSessionFactory) -> CompanyService:
    return CompanyService(session_maker)
