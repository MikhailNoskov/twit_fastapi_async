import pytest
import asyncio

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from database.connection import Base, get_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_session():
    db_url = "postgresql+asyncpg://postgres:postgres@localhost/testdb"
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
