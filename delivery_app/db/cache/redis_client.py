import aioredis


redis: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    return redis  # type: ignore
