import pytest
import asyncio

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from database.connection import Base, get_session
from settings import settings


@pytest.fixture(scope="session")
def event_loop():
    """
    Event loop generator
    :return: Yields new async event loop
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_session():
    """
    Test db session connection generator
    :return: Yields async connection to blank db
    """
    db_user = settings.DB_USER
    db_password = settings.DB_PASSWORD
    host = settings.DB_HOST
    port = settings.DB_PORT
    db_name = settings.TEST_DB_NAME

    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{host}:{port}/{db_name}"
    engine = create_async_engine(db_url, echo=True)
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def init_db() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    await init_db()
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope='session')
async def test_app(test_session):
    """
    Get test application function
    :param test_session: async db session
    :return: Test app instance
    """
    async def get_test_session():
        session = await test_session.__anext__()
        return session

    app.dependency_overrides[get_session] = get_test_session
    return app


# @pytest.fixture(scope='session', autouse=True)
# async def cleanup(test_engine):
#     # Clear tables after each test
#     yield
#     drop_database(test_engine.sync_engine.url)
