from redis import Redis


def get_cache(url: str):
    return Redis.from_url(url, decode_responses=True)
