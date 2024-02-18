from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from src.database import get_session
from src.security import oauth2_scheme
from src.api.test_pkg import get_current_user

router = APIRouter(
    prefix='/test',
    tags=['/test']
)


@router.get('/first')
async def first(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_session)):
    return await get_current_user(token, db)
