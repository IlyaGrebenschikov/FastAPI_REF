from fastapi import APIRouter

from src.api.v1.user import user_router
from src.api.v1.auth import auth_router
from src.api.v1.ref import ref_router


def init_v1_router() -> APIRouter:
    v1_router = APIRouter(
        prefix='/v1',
    )
    v1_router.include_router(user_router)
    v1_router.include_router(auth_router)
    v1_router.include_router(ref_router)

    return v1_router
