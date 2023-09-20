# from typing import Optional

from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base


engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/twitter', pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session():
    async with async_session_maker() as session:
        yield session


# class Settings(BaseSettings):
#     SECRET_KEY: Optional[str] = None
#
#     class Config:
#         env_file = ".env"