from pymongo import MongoClient

from core.conf import config


mongo_client: MongoClient = MongoClient(config.MONGO_URL)  # type: ignore
mongo_collection = mongo_client[config.MONGO_DB][config.MONGO_COLLECTION]
