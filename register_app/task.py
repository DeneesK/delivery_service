import logging

from redis import Redis
from sqlalchemy.orm import Session
from pymongo.collection import Collection

from celery_app import app
from utils.currency_rate import get_usd_to_rub
from db.models.parcel import Parcel
from utils.cost_log import insert_log
from core.di_container import init_container
from core.conf import Settings

logger = logging.getLogger(__name__)


@app.task(name="consumer.tasks.register_parcel_task", acks_late=True)
def register_parcel_task(parcel_data: dict):
    """save new parcel to db with calculated delivery cost"""
    try:
        container = init_container()

        session: Session = container.resolve(Session)
        mongo_collection: Collection = container.resolve(Collection)
        config: Settings = container.resolve(Settings)

        logger.info("New task got, from %s", parcel_data["owner"])

        cache: Redis = container.resolve(Redis)
        usd_rate = get_usd_to_rub(cache, config.CURRENCY_RATE_URL)

        weight = parcel_data["weight"]
        content_value_usd = parcel_data["content_value_usd"]
        delivery_cost_rub = round((weight * 0.5 + content_value_usd * 0.01) * usd_rate, 2)

        insert_log(mongo_collection, parcel_data, delivery_cost_rub)

        parcel = Parcel(
            parcel_id=parcel_data["parcel_id"],
            name=parcel_data["name"],
            weight=weight,
            parcel_type=parcel_data["parcel_type"],
            content_value_usd=content_value_usd,
            delivery_cost_rub=delivery_cost_rub,
            owner=parcel_data["owner"],
        )
        session.add(parcel)
        session.commit()
        logger.info("Task finished, from %s", parcel_data["owner"])
    except Exception as e:
        logger.error("Error during register parcel task %s", e, exc_info=True)
        session.rollback()
        raise
    finally:
        session.close()
