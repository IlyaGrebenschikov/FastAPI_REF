from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.schemas import TokenSchema
from src.api.v1.auth.services import service_authenticate_user
from src.database.database import get_session


auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@auth_router.post('/token', response_model=TokenSchema, operation_id='token')
async def create_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_session)
):
    return await service_authenticate_user(form_data, db)
