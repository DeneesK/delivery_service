from redis import Redis

from core.conf import config


def get_cache():
    return Redis.from_url(config.REDIS_URL, decode_responses=True)
