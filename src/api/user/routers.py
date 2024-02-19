from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from redis import Redis
from src.database import get_session
from src.database import redis_get_session

from src.api.user import UserServices
from src.api.user import UserSchemas


router = APIRouter(
    tags=['user'],
    prefix='/user',
)


@router.post('/create')
async def create_user(
        data: UserSchemas = None,
        db: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(redis_get_session)
):
    return await UserServices.create_user(data, db, redis_client)


@router.get('/get')
async def get_user(username: str, password: str, db: AsyncSession = Depends(get_session)):
    return await UserServices.get_user_username(username, password, db)
