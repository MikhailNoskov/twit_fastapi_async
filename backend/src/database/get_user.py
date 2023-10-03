from typing import Optional, List
import logging.config

from fastapi import APIRouter, HTTPException, status, Header, Depends, UploadFile, File
from models.users import User
from database.connection import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import async_session_maker as session
from logging_conf import logs_config

media_router = APIRouter(
    tags=["media"]
)

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_users")
logger.setLevel("DEBUG")


async def verify_api_key(api_key: str):
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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            logging.debug(msg='User retrieved')
            return user
