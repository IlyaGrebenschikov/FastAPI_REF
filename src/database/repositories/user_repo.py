from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import Optional

from src.api.user import UserModels
from src.api.user import UserSchemas
from src.api.user import UserSchemasInDB
from src.security import get_password_hash


class UserRepo:

    async def try_create_user(self, data: UserSchemas, db: AsyncSession) -> Optional[UserModels]:
        convert = UserSchemasInDB(
            name=data.name,
            email=data.email,
            hashed_password=data.password,
            referred_by=data.referred_by,
        )

        user = UserModels(
            name=convert.name,
            email=convert.email,
            hashed_password=convert.hashed_password,
            referred_by=convert.referred_by,
        )

        user.hashed_password = get_password_hash(user.hashed_password)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        response = {
            'name': user.name,
            'email': user.email,
            'referred_by': user.referred_by,
        }

        return response

    async def try_get_user_by_username(self, username: str, db: AsyncSession) -> Optional[UserModels]:
        stmt = (
            select(UserModels).
            filter(UserModels.name == username)
        )

        result = await db.execute(stmt)
        user = result.scalar()

        return user


    async def try_get_user_by_email(self, email: str, db: AsyncSession) -> Optional[UserModels]:
        stmt = (
            select(UserModels).
            filter(UserModels.email == email)
        )

        result = await db.execute(stmt)
        user = result.scalar()

        return user
