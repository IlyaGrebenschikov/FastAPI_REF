from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import init_db
from src.database import init_redis

from src.api.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    yield


app = FastAPI(
    title='Refferal APP',
    lifespan=lifespan
)
app.include_router(user_router)
