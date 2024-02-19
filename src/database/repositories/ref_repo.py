from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from redis import Redis

from typing import TYPE_CHECKING, Optional

from src.api.user import UserModels

from src.api.user import UserSchemasInDB

if TYPE_CHECKING:
    from src.database.repositories import UserRepo



class RefRepo:

    async def try_create_ref_email(self, ref: str, user: UserModels, timer: int, redis_client: Redis) -> bytes:
        link = await redis_client.set(ref, user.email, ex=timer)
        return link

    async def try_create_ref_by_link(self, user: UserModels, ref: str, timer: int, redis_client: Redis) -> bytes:
        link = await redis_client.set(user.email, ref, ex=timer)
        return link

    async def try_get_user_by_ref(self, ref: str, redis_client: Redis) -> str:
        data = await redis_client.get(ref)

        return data

    async def try_get_link(self, email: str, redis_client: Redis) -> str:
        data = await redis_client.get(email)

        return data

    async def try_delete_ref_by_link(self, ref: str, redis_client: Redis) -> bytes:
        data = await redis_client.delete(ref)

        return data

    async def try_delete_ref_by_email(self, email: str, redis_client: Redis) -> bytes:
        data = await redis_client.delete(email)

        return data
