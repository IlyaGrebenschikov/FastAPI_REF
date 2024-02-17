from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm


from src.security import get_auth_settings
from src.security import verify_password

from src.api.user import UserServices


async def authenticate_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await UserServices.get_user_username(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    is_password_correct = verify_password(form_data.password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = get_auth_settings().create_jwt_token({"sub": user.email, "scopes": form_data.scopes})

    return {"access_token": jwt_token, "token_type": "bearer"}
