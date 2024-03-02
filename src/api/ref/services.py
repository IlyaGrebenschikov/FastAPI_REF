from fastapi import status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.core import get_settings
from src.api.user import UserSchemasInDB
from src.database.repositories import UserRepo
from src.database.repositories import RefRepo


async def create_ref_link(ref: str, current_user: UserSchemasInDB, db: AsyncSession, redis_client: Redis) -> dict:
    timer = get_settings().redis.get_timer
    user_repo = UserRepo()
    ref_repo = RefRepo()

    user = await user_repo.try_get_user_by_email(current_user.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email is not auth",
        )

    if await ref_repo.try_get_user_by_ref(ref, redis_client):
        await ref_repo.try_delete_ref_by_link(ref, redis_client)
        await ref_repo.try_delete_ref_by_email(user.email, redis_client)
    await ref_repo.try_create_ref_by_link(user, ref, timer, redis_client)
    await ref_repo.try_create_ref_email(ref, user, timer, redis_client)

    data = await ref_repo.try_get_link(user.email, redis_client)

    return {
        'your_link': data
    }


async def delete_ref_link(ref: str, current_user: UserSchemasInDB, db: AsyncSession, redis_client: Redis) -> dict:
    user_repo = UserRepo()
    ref_repo = RefRepo()

    user = await user_repo.try_get_user_by_email(current_user.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email is not auth",
        )

    await ref_repo.try_delete_ref_by_link(ref, redis_client)
    await ref_repo.try_delete_ref_by_email(user.email, redis_client)

    return {
        'result': 'deleted'
    }


async def get_all_referrals_by_userid(user_id: int, limit: int, current_user: UserSchemasInDB, db: AsyncSession):
    user_repo = UserRepo()
    ref_repo = RefRepo()

    test_user = await user_repo.try_get_user_by_email(current_user.email, db)

    if not test_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email is not auth",
        )
    user = await user_repo.try_get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    referrals = await ref_repo.get_all_refferals(user, limit, db)

    return referrals


# async def add_ref_by_link