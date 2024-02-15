from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from typing import Optional

from src.api.user import UserModels
from src.api.user import UserSchemas

from src.security import oauth2_scheme
from src.security import pwd_context


class UserServices:
    @staticmethod
    async def create_user(data: UserSchemas, db: AsyncSession):
        user = UserModels(**data.model_dump())
        user.hashed_password = pwd_context.hash(user.hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user(user_id: int, db: AsyncSession):
        user = await db.get(UserModels, user_id)
        return user
