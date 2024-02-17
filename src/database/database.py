from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from redis import asyncio as asyncredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.core import get_settings
from src.database import Base


engine = create_async_engine(url=get_settings().db.create_url())

async_session = async_sessionmaker(engine, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def init_redis():
    redis = await asyncredis.from_url(get_settings().redis.get_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
