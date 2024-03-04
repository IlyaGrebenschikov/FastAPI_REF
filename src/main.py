import uvicorn
from fastapi import FastAPI

from src.api.v1 import v1_router


app = FastAPI(
    title='Refferal APP',
)
app.include_router(v1_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='127.0.0.1',
        port=8080
    )
