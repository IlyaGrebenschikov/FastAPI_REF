from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.database import get_session
from src.database import redis_get_session
from src.api.v1.user import service_create_user
from src.api.v1.user import UserSchemas


router = APIRouter(
    tags=['user'],
    prefix='/user',
)


@router.post('/create', operation_id='create')
async def create_user(
        data: UserSchemas = None,
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await service_create_user(data, db, redis_client)
