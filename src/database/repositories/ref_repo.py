from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from redis import Redis




from src.api.user import UserModels

from src.api.user import UserSchemasInDB

from src.database.repositories import UserRepo



class RefRepo:

    async def try_create_ref(self, ref: str, user: UserModels, timer: int, redis_client: Redis) -> bytes:
        link = await redis_client.set(ref, user.email, ex=timer)
        return link

    async def try_get_user_by_ref(self, ref: str, redis_client: Redis) -> str:
        data = await redis_client.get(ref)

        return data
