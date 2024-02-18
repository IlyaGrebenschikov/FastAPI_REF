from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import init_db

from src.api.user import user_router
from src.api.auth import auth_router
from src.api.ref import ref_router
from src.api.test_pkg import test_pkg_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Refferal APP',
    lifespan=lifespan
)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(test_pkg_router)
app.include_router(ref_router)
