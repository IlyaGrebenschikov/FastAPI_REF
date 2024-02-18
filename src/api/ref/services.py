import json
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from email_validator import validate_email, EmailSyntaxError

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from redis import Redis

from src.core import get_settings


from src.api.user import UserSchemasInDB
from src.api.auth import get_current_user

from src.database.repositories import UserRepo
from src.database.repositories import RefRepo


async def create_ref_link(ref: str, current_user: UserSchemasInDB, db: AsyncSession, redis_client: Redis) -> str:
    timer = get_settings().redis.get_timer
    user_repo = UserRepo()
    ref_repo = RefRepo()

    user = await user_repo.try_get_user_by_email(current_user.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email is not auth",
        )

    await ref_repo.try_create_ref(ref, user, timer, redis_client)
    data = await ref_repo.try_get_user_by_ref(ref, redis_client)

    return data


# async def add_ref_by_link