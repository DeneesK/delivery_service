from celery import Celery  # type: ignore


def get_client(broker: str) -> Celery:
    celery_client = Celery("delivery_app", broker=broker)  # TODO: name вынести в conf
    return celery_client
