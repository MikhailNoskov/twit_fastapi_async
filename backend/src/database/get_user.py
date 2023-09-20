from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends, UploadFile, File
from models.users import User
from database.connection import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import async_session_maker as session


media_router = APIRouter(
    tags=["media"]
)


async def verify_api_key(api_key: str):
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.api_key == api_key))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user
