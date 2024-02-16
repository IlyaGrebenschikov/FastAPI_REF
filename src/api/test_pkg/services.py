from src.api.user import UserServices
from fastapi import HTTPException
from fastapi import status

from src.security import get_auth_settings
from src.api.auth.models import TokenData

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt, JWTError


async def get_current_user(token: str, password: str, db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_auth_settings().verify_jwt_token(token)
        return payload, token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await UserServices.get_user(token_data.username, password, db)
    if user is None:
        raise credentials_exception
    return user
