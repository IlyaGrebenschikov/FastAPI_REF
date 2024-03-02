from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database import init_db
from src.api.user import user_router
from src.api.auth import auth_router
from src.api.ref import ref_router


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
app.include_router(ref_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='127.0.0.1',
        port=8080
    )
