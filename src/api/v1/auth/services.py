from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from src.database.database import get_session
from src.api.v1.auth.schemas import TokenDataSchema
from src.api.v1.user.models import UserModel
from src.api.v1.user.services import service_get_user_username, service_get_user_email
from src.security.auth_security import oauth2_scheme, verify_password
from src.security.jwt_security import create_jwt_token, verify_jwt_token


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
) -> UserModel:
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
        token_data = TokenDataSchema(email=email_token)
    except JWTError:
        raise credentials_exception

    user = await service_get_user_email(token_data.email, db)

    if user is None:
        raise credentials_exception

    return user
