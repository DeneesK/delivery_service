import httpx

from redis import Redis


def get_usd_to_rub(cache: Redis, currency_url: str) -> float:
    cached = cache.get("usd_to_rub")
    if cached:
        return float(cached)  # type: ignore

    with httpx.Client() as client:
        resp = client.get(currency_url)
        data = resp.json()
        rate = data["Valute"]["USD"]["Value"]
        cache.set("usd_to_rub", rate, ex=300)
        return rate
