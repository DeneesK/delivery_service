import orjson
from aioredis import Redis


class CacheService:
    def __init__(self, cache_client: Redis, ttl: int):
        self.cache = cache_client
        self.ttl = ttl

    async def get(self, key: str) -> dict | list:
        cached = await self.cache.get(str(key))
        result = orjson.loads(cached)
        return result

    async def set(self, name: str, value: str) -> None:
        await self.cache.set(name, value, ex=self.ttl)


def get_cache_service(cache_client: Redis, ttl: int) -> CacheService:
    return CacheService(cache_client, ttl)
