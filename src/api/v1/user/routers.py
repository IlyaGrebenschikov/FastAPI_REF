from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.database.database import get_session
from src.database.redis_connect import redis_get_session
from src.api.v1.user.services import service_create_user
from src.api.v1.user.schemas import UserSchema


user_router = APIRouter(
    tags=['user'],
    prefix='/user',
)


@user_router.post('/create', operation_id='create')
async def create_user(
        data: UserSchema = None,
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await service_create_user(data, db, redis_client)
