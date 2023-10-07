import logging.config
from typing import Optional

from sqlalchemy import select

from models.users import User
from database.connection import async_session_maker as session
from logging_conf import logs_config


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_users")
logger.setLevel("DEBUG")


async def verify_api_key(api_key: str) -> Optional[User]:
    """
    Api key verification function
    :param api_key: Received api key as a string
    :return: User instance found by api key
    """
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.api_key == api_key))
            user = user.scalar_one_or_none()
            if not user:
                logging.warning(msg=f"User with {api_key} api key not found")
                return None
            logging.debug(msg='User retrieved')
            return user
