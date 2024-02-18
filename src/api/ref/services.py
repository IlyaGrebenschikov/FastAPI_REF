from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from email_validator import validate_email, EmailSyntaxError

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated


from src.api.user import UserSchemasInDB
from src.api.auth import get_current_user

from src.database.repositories import UserRepo
from src.database.repositories import RefRepo


async def create_ref_link(ref: str, current_user: UserSchemasInDB, db: AsyncSession) -> dict:
    user_repo = UserRepo()
    ref_repo = RefRepo()

    user = await user_repo.try_get_user_by_email(current_user.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your email is not auth",
        )
    referral_link = await ref_repo.try_create_ref(ref, user, db)

    return {
        'referrer': referral_link.referrer
    }


# async def add_ref_by_link