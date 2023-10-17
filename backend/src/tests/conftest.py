import pytest
import asyncio

from sqlalchemy_utils import drop_database, create_database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.connection import Base, get_session, engine, async_session_maker
from settings import settings
from auth.hash_password import HashPassword
from models.users import User


@pytest.fixture(scope="session")
def event_loop():
    """
    Event loop generator
    :return: Yields new async event loop
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def drop_base():
    """
    Test db session connection generator
    :return: Yields async connection to blank db
    """
    # db_user = settings.DB_USER
    # db_password = settings.DB_PASSWORD
    # host = settings.DB_HOST
    # port = settings.DB_PORT
    # db_name = settings.TEST_DB_NAME
    #
    # db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{host}:{port}/{db_name}"
    # engine = create_async_engine(db_url, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    #
    # yield async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
async def create_data(drop_base):
    await drop_base
    async with async_session_maker() as session:
        async with session.begin():
            users = {
                0: ['mike@klike.com', 'pass_1', 'test'],
                1: ['jorge@klike.com', 'pass_2', 'rest'],
                2: ['rob@klike.com', 'pass_3', 'nest'],
            }
            for email, password, api_key in users.values():
                hashed_password = HashPassword.create_hash(password)
                user = User(name=email, password=hashed_password, api_key=api_key)
                session.add(user)
                await session.flush()
                await session.refresh(user)


# @pytest.fixture(scope="session")
# async def test_app(test_session):
#     """
#     Get test application function
#     :param test_session: async db session
#     :return: Test app instance
#     """
#
#     async def get_test_session():
#         session = await test_session
#         return session
#
#     app.dependency_overrides[get_session] = get_test_session
#     return app


# @pytest.fixture(scope="session", autouse=True)
# async def cleanup(test_engine):
#     # Clear tables after each test
#     yield
#     drop_database(test_engine.sync_engine.url)
