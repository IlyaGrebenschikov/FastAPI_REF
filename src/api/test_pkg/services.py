from src.api.user import UserServices
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from typing import Annotated

from src.security import get_auth_settings
from src.api.auth.schemas import TokenData
from src.database import get_session
from src.security import oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt, JWTError


async def get_current_user(token: str, db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_auth_settings().verify_jwt_token(token)
        email_token: str = payload.get("sub")
        if email_token is None:
            raise credentials_exception
        token_data = TokenData(email=email_token)
    except JWTError:
        raise credentials_exception
    user = await UserServices.get_user_email(token_data.email, db)
    if user is None:
        raise credentials_exception
    return user
