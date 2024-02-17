from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from src.database.repositories import UserRepo
from src.api.user import UserModels
from src.api.user import UserSchemas
from src.api.user import UserSchemasInDB

from src.security import oauth2_scheme
from src.security import pwd_context
from src.security import verify_password
from src.security import get_password_hash


class UserServices:
    @staticmethod
    async def create_user(data: UserSchemas, db: AsyncSession):
        try:
            user_repo = UserRepo()
            result = await user_repo.try_create_user(data, db)
            return result
        except Exception:
            raise HTTPException(status_code=400, detail='User already exists')

    @staticmethod
    async def get_user(username: str, password: str, db: AsyncSession):
        exc = HTTPException(status_code=400, detail="Incorrect username or password")
        user_repo = UserRepo()
        user = await user_repo.try_get_user_by_username(username, db)
        if not user:
            raise exc
        is_password_correct = verify_password(password, user.hashed_password)
        if not is_password_correct:
            raise exc
        return user
