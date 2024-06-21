from typing import Annotated

from fastapi import Depends, APIRouter
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.user.schemas import UserInDBSchema
from src.api.v1.auth.services import service_get_current_user
from src.api.v1.ref.services import (
    service_create_ref_link,
    service_delete_ref_link,
    service_get_all_referrals_by_userid
)
from src.database.database import get_session
from src.database.redis_connect import redis_get_session


ref_router = APIRouter(
    prefix='/referral',
    tags=['referral']
)


@ref_router.post('/create_link', operation_id='create_link')
async def create_referral_link(
        referral_link: str,
        current_user: Annotated[UserInDBSchema, Depends(service_get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await service_create_ref_link(referral_link, current_user, db, redis_client)


@ref_router.patch('/update_link', operation_id='update_link')
async def update_referral_link(
        referral_link: str,
        current_user: Annotated[UserInDBSchema, Depends(service_get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await service_create_ref_link(referral_link, current_user, db, redis_client)


@ref_router.delete('/delete_link', operation_id='delete_link')
async def delete_referral_link(
        referral_link: str,
        current_user: Annotated[UserInDBSchema, Depends(service_get_current_user)],
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await service_delete_ref_link(referral_link, current_user, db, redis_client)


@ref_router.get('/get_all_referrals{user_id}', operation_id='get_all_referrals{user_id}')
async def get_all_referrals(
        current_user: Annotated[UserInDBSchema, Depends(service_get_current_user)],
        user_id: int,
        limit: int = 20,
        db: AsyncSession = Depends(get_session)
):
    return await service_get_all_referrals_by_userid(user_id, limit, current_user, db)
