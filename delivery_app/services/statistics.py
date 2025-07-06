from datetime import datetime, timedelta
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from dto.statics_dto import DailyStatisticsDTO, StatisticsOut


class StatisticsService:
    def __init__(self, client: AsyncIOMotorClient, db_name: str, collection: str):
        self.collection = client[db_name][collection]

    async def ensure_indexes(self):
        """creating indexes"""
        await self.collection.create_index([("timestamp", 1), ("parcel_type", 1)])

    async def get_daily_costs(
        self, date: datetime, parcel_type: Optional[str] = None
    ) -> DailyStatisticsDTO:
        """calculation of the sum of the delivery costs of all parcels by type per day"""
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)

        match_stage = {"timestamp": {"$gte": start, "$lt": end}}

        if parcel_type:
            match_stage["parcel_type"] = parcel_type  # type: ignore

        pipeline = [
            {"$match": match_stage},
            {
                "$group": {
                    "_id": "$parcel_type",
                    "total_cost": {"$sum": "$delivery_cost_usd"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "parcel_type": "$_id",
                    "total_cost": 1,
                    "date": {"$literal": start.strftime("%Y-%m-%d")},
                }
            },
        ]

        result = await self.collection.aggregate(pipeline).to_list(length=None)  # type: ignore

        return DailyStatisticsDTO(data=[StatisticsOut.model_validate(s) for s in result])


def get_static_service(
    client: AsyncIOMotorClient, db_name: str, collection: str
) -> StatisticsService:
    return StatisticsService(client, db_name, collection)
