from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from src.api.user import UserModels
from src.api.user import UserSchemas

from src.security import oauth2_scheme
from src.security import pwd_context
from src.security import verify_password
from src.security import get_password_hash


class UserServices:
    @staticmethod
    async def create_user(data: UserSchemas, db: AsyncSession):
        try:
            user = UserModels(**data.model_dump())
            user.hashed_password = get_password_hash(user.hashed_password)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except Exception:
            raise HTTPException(status_code=400, detail='User already exists')

    @staticmethod
    async def get_user(username: str, password: str, db: AsyncSession):
        stmt = (
            select(UserModels).
            filter(UserModels.name == username)
        )
        result = await db.execute(stmt)
        user = result.scalar()

        is_password_correct = verify_password(password, user.hashed_password)

        if not is_password_correct:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        return user
