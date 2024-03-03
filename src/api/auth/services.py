from typing import Annotated

from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from src.database import get_session
from src.api.auth.schemas import TokenData
from src.api.user import UserModels
from src.security import oauth2_scheme
from src.security import create_jwt_token
from src.security import verify_jwt_token
from src.security import verify_password
from src.api.user import service_get_user_username
from src.api.user import service_get_user_email


async def service_authenticate_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await service_get_user_username(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_password_correct = verify_password(form_data.password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_token = create_jwt_token({"sub": user.email, "scopes": form_data.scopes})

    return {"access_token": jwt_token, "token_type": "bearer"}


async def service_get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_session)
) -> UserModels:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_jwt_token(token)
        email_token: str = payload.get("sub")
        if email_token is None:
            raise credentials_exception
        token_data = TokenData(email=email_token)
    except JWTError:
        raise credentials_exception

    user = await service_get_user_email(token_data.email, db)

    if user is None:
        raise credentials_exception

    return user
