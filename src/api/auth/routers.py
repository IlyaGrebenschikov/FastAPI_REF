from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas import Token
from src.api.auth import authenticate_user
from src.database import get_session
from src.security import oauth2_scheme


router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@router.post('/token', response_model=Token)
async def create_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_session)
):
    return await authenticate_user(form_data, db)
