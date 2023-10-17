import pytest
import asyncio

from database.connection import Base, get_session, engine, async_session_maker
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
