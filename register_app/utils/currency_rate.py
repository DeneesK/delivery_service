import httpx

from core.conf import config  # type: ignore
from db.cache import get_cache  # type: ignore


def get_usd_to_rub() -> float:
    cache = get_cache()
    cached = cache.get("usd_to_rub")
    if cached:
        return float(cached)

    with httpx.Client() as client:
        resp = client.get(config.CURRENCY_RATE_URL)
        data = resp.json()
        rate = data["Valute"]["USD"]["Value"]
        cache.set("usd_to_rub", rate, ex=300)
        return rate
