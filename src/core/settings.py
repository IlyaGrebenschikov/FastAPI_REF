import secrets
from functools import lru_cache
from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import URL


ROOT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{ROOT_DIR}/.env',
        env_file_encoding='utf-8',
    )

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: str


class SecretSettings:
    secret_key: str = secrets.token_hex(32)
    secret_algh: str = 'HS256'
    jwt_expiration: Final[int] = 30


class DbSettings(EnvSettings):
    def create_url(self) -> URL:
        url_obj = URL.create(
            'postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT
        )
        return url_obj

    @property
    def get_url(self) -> str:
        return self.DB_URL.format(
            POSTGRES_USER=self.POSTGRES_USER,
            POSTGRES_PASSWORD=self.POSTGRES_PASSWORD,
            POSTGRES_HOST=self.POSTGRES_HOST,
            POSTGRES_PORT=self.POSTGRES_PORT,
            POSTGRES_DB=self.POSTGRES_DB,
            )


class RedisSettings(EnvSettings):
    def __init__(self, **values: Any):
        super().__init__(**values)
        self.ex_timer: Final[int] = 1800

    @property
    def get_url(self) -> str:
        return self.REDIS_URL.format(
            REDIS_HOST=self.REDIS_HOST,
            REDIS_PORT=self.REDIS_PORT,
        )


@lru_cache(typed=True)
def get_db_settings() -> DbSettings:
    return DbSettings()


@lru_cache(typed=True)
def get_secret_settings() -> SecretSettings:
    return SecretSettings()


@lru_cache(typed=True)
def get_redis_settings() -> RedisSettings:
    return RedisSettings()
