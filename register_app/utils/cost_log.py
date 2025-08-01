from datetime import datetime

from pymongo.collection import Collection


def insert_log(mongo_collection: Collection, parcel_data: dict, cost: float) -> None:
    mongo_collection.insert_one(
        {
            "timestamp": datetime.utcnow(),
            "parcel_id": parcel_data["parcel_id"],
            "parcel_type": parcel_data["parcel_type"],
            "delivery_cost_usd": cost,
            "session_id": parcel_data.get("session_id"),
        }
    )
