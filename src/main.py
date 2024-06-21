import uvicorn
from fastapi import FastAPI

from src.api.v1 import init_v1_router


def main() -> None:
    app = FastAPI(
        title='Refferal APP',
    )
    app.include_router(init_v1_router())
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8000
    )


if __name__ == '__main__':
    main()
