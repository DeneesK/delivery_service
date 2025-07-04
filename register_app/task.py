import logging

from celery_app import app
from currency_rate import get_usd_to_rub
from db.db import SessionLocal
from db.models.parcel import Parcel
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@app.task(name="consumer.tasks.register_parcel_task")
def register_parcel_task(parcel_data: dict):
    session: Session = SessionLocal()
    try:
        logger.info("New task got, from %s", parcel_data["owner"])
        usd_rate = get_usd_to_rub()

        weight = parcel_data["weight"]
        content_value_usd = parcel_data["content_value_usd"]
        delivery_cost_rub = round((weight * 0.5 + content_value_usd * 0.01) * usd_rate, 2)

        parcel = Parcel(
            name=parcel_data["name"],
            weight=weight,
            type_id=parcel_data["type_id"],
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
