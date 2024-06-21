from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from src.core.settings import get_db_settings


engine = create_async_engine(url=get_db_settings().create_url())
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
