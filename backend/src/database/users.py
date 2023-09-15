from typing import Optional

from fastapi import HTTPException, status, Depends, Header
from sqlalchemy import select, insert, column, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from models.users import User, users_connections
from schema.users import UserRegister, UserFollowing, UserFollower
from schema.positive import PositiveResponse
from database.connection import async_session_maker as session


async def create_user(data: UserRegister) -> dict:
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.name == data.username))
            user = user.scalar_one_or_none()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with supplied username exists"
                )
            user = User(name=data.username, password=data.password)
            db.add(user)
            await db.flush()
            await db.refresh(user)
            return {
                "message": "User successfully registered!"
            }


async def get_me(api_key: Optional[str]):
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.api_key == api_key).options(
             joinedload(User.followers),
             joinedload(User.following)))
            user = user.scalar()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user


async def get_user(user_id: int):
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.id == user_id).options(
             joinedload(User.followers),
             joinedload(User.following)))
            user = user.scalar()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user


async def set_follow_user(user_id: int, api_key: str):
    async with session() as db:
        async with db.begin():
            me = await db.execute(select(User).where(User.api_key == api_key))
            me = me.scalar_one_or_none()
            user = await db.execute(select(User).where(User.id == user_id))
            user = user.scalar_one_or_none()
            if not me:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            if me.id == user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You can not follow yourself"
                )
            try:
                stmt = insert(users_connections).values(
                    follower_id=me.id,
                    followed_id=user.id
                )
                await db.execute(stmt)
                await db.commit()
                return PositiveResponse(result=True)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You are already following this user"
                )


async def unfollow_user(user_id: int, api_key: Optional[str] = Header(None)):
    async with session() as db:
        async with db.begin():
            me = await db.execute(select(User).where(User.api_key == api_key))
            me = me.scalar_one_or_none()
            if not me:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            stmt = select(users_connections).where(
                (column('follower_id') == me.id) &
                (column('followed_id') == user_id)
                )
            follow = await db.execute(stmt)
            follow = follow.scalar_one_or_none()
            if follow:
                stmt = delete(users_connections).where(
                    (column('follower_id') == me.id) &
                    (column('followed_id') == user_id)
                )
                await db.execute(stmt)
                return PositiveResponse(result=True)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are not following this user"
            )
