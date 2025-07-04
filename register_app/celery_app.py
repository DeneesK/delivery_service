from celery import Celery  # type: ignore
from core.conf import config  # type: ignore

app = Celery(
    "consumer",
    broker=config.BROKER_URL,
    backend=config.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
    include=["task"],
)
