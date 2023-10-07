from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = 'special_key'
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None
    TEST_DB_NAME: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None

    class Config:
        env_file = ".env"


settings = Settings()
