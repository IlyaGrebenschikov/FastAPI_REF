from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from src.database import get_session

from src.api.user import UserServices
from src.api.user import UserSchemas


router = APIRouter(
    tags=['user'],
    prefix='/user',
)


@router.post('/create')
async def create_user(data: UserSchemas = None, db: AsyncSession = Depends(get_session)):
    return await UserServices.create_user(data, db)


@router.get('/get')
@cache(expire=30)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await UserServices.get_user(user_id, db)
