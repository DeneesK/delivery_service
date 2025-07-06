from pymongo import MongoClient
from pymongo.collection import Collection


def get_mongo_collection(url: str, dbname: str, collectionname: str) -> Collection:
    mongo_client: MongoClient = MongoClient(url)  # type: ignore
    return mongo_client[dbname][collectionname]
