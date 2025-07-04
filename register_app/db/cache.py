from redis import Redis


def get_cache():
    return Redis()
