from core.conf import config
from redis import Redis


def get_cache():
    return Redis.from_url(config.REDIS_URL, decode_responses=True)
