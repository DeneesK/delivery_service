from celery import Celery  # type: ignore


def get_client(broker: str) -> Celery:
    celery_client = Celery(broker=broker)
    return celery_client
