import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from functools import lru_cache
from pathlib import Path
from sqlalchemy import URL


class EnvSettings(BaseSettings):
    
    root_dir: DirectoryPath = Path(__file__).parent.parent.parent
    model_config = SettingsConfigDict(
        env_file=f'{root_dir}/.env',
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

    @property
    def get_url(self) -> str:
        return self.REDIS_URL.format(
            REDIS_HOST=self.REDIS_HOST,
            REDIS_PORT=self.REDIS_PORT,
        )


class Settings:
    
    env: EnvSettings = EnvSettings()
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()
    secret: SecretSettings = SecretSettings()


@lru_cache(typed=True)
def get_settings() -> Settings:
    return Settings()
