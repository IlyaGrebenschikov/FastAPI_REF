from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis import Redis

from src.api.v1.user.models import UserModel
from src.api.v1.user.schemas import UserInDBSchema


class RefRepo:
    async def try_create_ref_email(self, ref: str, user: UserInDBSchema, timer: int, redis_client: Redis) -> bytes:
        link = await redis_client.set(ref, user.email, ex=timer)
        return link

    async def try_create_ref_by_link(self, user: UserInDBSchema, ref: str, timer: int, redis_client: Redis) -> bytes:
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

    async def get_all_refferals(self, user: UserInDBSchema, limit: int, db: AsyncSession) -> Optional[UserModel | Any]:
        stmt = (
            select(UserModel).
            filter(UserModel.referred_by == user.email).
            limit(limit)
        )
        referrals = await db.execute(stmt)
        result = referrals.scalars().all()
        return result
