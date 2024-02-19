from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from redis import Redis

from src.database.repositories import UserRepo
from src.api.user import UserSchemas
from src.database.repositories import RefRepo
from src.security import verify_password



class UserServices:
    @staticmethod
    async def create_user(data: UserSchemas, db: AsyncSession, redis_client: Redis):
        ref_repo = RefRepo()
        user_repo = UserRepo()
        test_data = await ref_repo.try_get_user_by_ref(data.referred_by, redis_client)
        if not test_data:
            raise HTTPException(400, 'referrer link has expired')
        data.referred_by = test_data

        try:
            result = await user_repo.try_create_user(data, db)
            return result
        except Exception:
            raise HTTPException(status_code=400, detail='User already exists')

    @staticmethod
    async def get_user_username(username: str, password: str, db: AsyncSession):
        exc = HTTPException(status_code=400, detail="Incorrect username or password")
        user_repo = UserRepo()
        user = await user_repo.try_get_user_by_username(username, db)
        if not user:
            raise exc
        is_password_correct = verify_password(password, user.hashed_password)
        if not is_password_correct:
            raise exc
        return user

    @staticmethod
    async def get_user_email(email: str, db: AsyncSession):
        exc = HTTPException(status_code=400, detail="Incorrect email or password")
        user_repo = UserRepo()
        user = await user_repo.try_get_user_by_email(email, db)
        if not user:
            raise exc

        return user
