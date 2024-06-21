from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.core.settings import get_redis_settings
from src.api.v1.user.schemas import UserInDBSchema
from src.database.repositories.user_repo import UserRepo
from src.database.repositories.ref_repo import RefRepo


async def service_create_ref_link(
        ref: str,
        current_user: UserInDBSchema,
        db: AsyncSession,
        redis_client: Redis
) -> dict:
    timer = get_redis_settings().EX_TIMER
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


async def service_delete_ref_link(
        ref: str,
        current_user: UserInDBSchema,
        db: AsyncSession,
        redis_client: Redis
) -> dict:
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


async def service_get_all_referrals_by_userid(
        user_id: int,
        limit: int,
        current_user: UserInDBSchema,
        db: AsyncSession
):
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
