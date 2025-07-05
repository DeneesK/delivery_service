import pytest
import orjson


@pytest.mark.asyncio
async def test_set_stores_data_correctly(cache_service, redis_mock):
    await cache_service.set("key", "value")
    redis_mock.set.assert_awaited_once_with("key", "value", ex=60)


@pytest.mark.asyncio
async def test_get_returns_parsed_json(cache_service, redis_mock):
    data = {"a": 1}
    redis_mock.get.return_value = orjson.dumps(data)

    result = await cache_service.get("my-key")

    redis_mock.get.assert_awaited_once_with("my-key")
    assert result == data


@pytest.mark.asyncio
async def test_get_returns_none_for_empty_cache(cache_service, redis_mock):
    redis_mock.get.return_value = orjson.dumps(None)

    result = await cache_service.get("unknown")
    assert result is None


@pytest.mark.asyncio
async def test_get_raises_on_invalid_json(cache_service, redis_mock):
    redis_mock.get.return_value = b"not-json"

    with pytest.raises(orjson.JSONDecodeError):
        await cache_service.get("bad-json")
