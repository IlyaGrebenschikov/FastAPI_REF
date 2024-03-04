from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.schemas import Token
from src.api.v1.auth import service_authenticate_user
from src.database import get_session


router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@router.post('/token', response_model=Token, operation_id='token')
async def create_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_session)
):
    return await service_authenticate_user(form_data, db)
