from fastapi import Depends
from fastapi import APIRouter

from redis import Redis

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from src.api.user import UserSchemasInDB
from src.api.auth import get_current_user
from src.api.ref import create_ref_link
from src.api.ref import delete_ref_link
from src.database import get_session
from src.database import redis_get_session

router = APIRouter(
    prefix='/referral',
    tags=['referral']
)


@router.post('/create_link')
async def create_referral_link(
        referral_link: str,
        current_user: Annotated[UserSchemasInDB, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await create_ref_link(referral_link, current_user, db, redis_client)


@router.patch('/update_link', )
async def update_referral_link(
        referral_link: str,
        current_user: Annotated[UserSchemasInDB, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await create_ref_link(referral_link, current_user, db, redis_client)


@router.delete('/delete_link')
async def delete_referral_link(
        referral_link: str,
        current_user: Annotated[UserSchemasInDB, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await delete_ref_link(referral_link, current_user, db, redis_client)
