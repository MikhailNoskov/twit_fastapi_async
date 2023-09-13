from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, column, delete

from models.users import User, users_connections
from schema.users import UserRegister, UserFull, UserFollowing, UserFollower
from database.connection import get_session
from sqlalchemy.orm import joinedload


user_router = APIRouter(
    tags=["users"]
)


@user_router.post("/signup")
async def sign_new_user(data: UserRegister, db: AsyncSession = Depends(get_session)) -> dict:
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


@user_router.get('/me', response_model=UserRegister)
async def me(api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
    async with db.begin():
        user = await db.execute(select(User).where(User.api_key == api_key))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user


@user_router.get('/{user_id}', response_model=UserFull)
async def get_user_by_id(user_id: int, api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
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


@user_router.post('/{user_id}/follow')
async def follow_user(user_id: int, api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
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
            return {"result": True}
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are already following this user"
            )


@user_router.delete('/{user_id}/follow')
async def follow_user(user_id: int, api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
    async with db.begin():
        me = await db.execute(select(User).where(User.api_key == api_key))
        me = me.scalar_one_or_none()
        if not me:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        stmt = select(users_connections).where(
                column('follower_id') == me.id,
                column('followed_id') == user_id
            )
        follow = await db.execute(stmt)
        follow = follow.scalar_one_or_none()
        if follow:
            # await db.delete(follow)
            # return {"result": True}
            stmt = delete(users_connections).where(
                column('follower_id') == me.id,
                column('followed_id') == user_id
            )
            await db.execute(stmt)
            # await db.delete(follow)
            return {"result": True}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user"
        )
# @user_router.post("/signin")
# async def sign_user_in(user: UserSignIn) -> dict:
#     if user.username not in users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist")
#     if users[user.username].password != user.password:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Wrong credentials passed"
#         )
#     return {
#         "message": "User signed in successfully"
#     }
