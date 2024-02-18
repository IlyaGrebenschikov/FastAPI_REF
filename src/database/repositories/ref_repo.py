from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Optional

from src.api.user import UserModels

from src.api.user import UserSchemasInDB

from src.database.repositories import UserRepo


class RefRepo:

    async def try_create_ref(self, ref: str, user: UserModels, db: AsyncSession) -> Optional[UserModels]:
        user.referrer = ref
        await db.commit()
        await db.refresh(user)

        return user
