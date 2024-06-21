import redis.asyncio as aioredis
from redis import Redis

from src.core.settings import get_redis_settings


async def redis_get_session() -> Redis:
    url = get_redis_settings().get_url
    client = aioredis.from_url(url, encoding="utf8", decode_responses=True)

    async with client:
        yield client
