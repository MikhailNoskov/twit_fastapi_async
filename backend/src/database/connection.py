import logging.config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from logging_conf import logs_config
from settings import settings

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.data_base")
logger.setLevel("DEBUG")

DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME

engine = create_async_engine(
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_pre_ping=True
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session():
    """
    Async db session generator
    :return: Yields db async connection
    """
    async with async_session_maker() as session:
        logger.debug(msg='Database session yielded')
        yield session
