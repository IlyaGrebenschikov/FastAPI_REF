from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api.v1.user.models import UserModel
from src.api.v1.user.schemas import UserSchema, UserInDBSchema
from src.security.auth_security import get_password_hash


class UserRepo:
    async def try_create_user(self, data: UserSchema, db: AsyncSession) -> Optional[UserModel]:
        convert = UserInDBSchema(
            name=data.name,
            email=data.email,
            hashed_password=data.password,
            referred_by=data.referred_by,
        )

        user = UserModel(
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

    async def try_get_user_by_username(self, username: str, db: AsyncSession) -> Optional[UserModel]:
        stmt = (
            select(UserModel).
            filter(UserModel.name == username)
        )
        result = await db.execute(stmt)
        user = result.scalar()

        return user

    async def try_get_user_by_email(self, email: str, db: AsyncSession) -> Optional[UserModel]:
        stmt = (
            select(UserModel).
            filter(UserModel.email == email)
        )
        result = await db.execute(stmt)
        user = result.scalar()

        return user

    async def try_get_user_by_id(self, user_id: int, db: AsyncSession) -> Optional[UserModel]:
        stmt = (
            select(UserModel).
            filter(UserModel.id == user_id)
        )
        result = await db.execute(stmt)
        user = result.scalar()

        return user
