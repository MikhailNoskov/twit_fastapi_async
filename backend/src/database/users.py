import logging.config

from fastapi import HTTPException, status, Depends, Header
from sqlalchemy import select, insert, column, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload


from models.users import User, users_connections
from schema.users import UserRegister, UserFollowing, UserFollower
from schema.positive import PositiveResponse
from logging_conf import logs_config
from database.services import AbstractService


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_users")
logger.setLevel("DEBUG")


class UserService(AbstractService):
    async def create_user(self, data: UserRegister) -> dict:
        async with self.session.begin():
            user = await self.session.execute(select(User).where(User.name == data.username))
            user = user.scalar_one_or_none()
            if user:
                logger.exception(msg="User with supplied username exists")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with supplied username exists"
                )
            user = await self.session.execute(select(User).where(User.api_key == data.api_key))
            user = user.scalar_one_or_none()
            if user:
                logger.exception(msg="User with supplied api_key exists")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with supplied api_key exists"
                )
            user = User(name=data.username, password=data.password, api_key=data.api_key)
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            logger.info(msg="User successfully registered")
            return {
                "message": "User successfully registered!"
            }

    async def get_me(self, user_id: int):
        async with self.session.begin():
            user = await self.session.execute(select(User).where(User.id == user_id).options(
             joinedload(User.followers),
             joinedload(User.following)))
            user = user.scalar()
            if not user:
                logger.error(msg="User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            logger.debug('User retrieved for me endpoint')
            return user

    async def get_user(self, user_id: int):
        # async with self.session.begin():
        user = await self.session.execute(select(User).where(User.id == user_id).options(
         joinedload(User.followers),
         joinedload(User.following)))
        user = user.scalar()
        if not user:
            logger.error(msg="User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        logger.debug('User retrieved for id endpoint')
        return user

    async def set_follow_user(self, user_id: int, me: User):
        async with self.session.begin():
            user = await self.get_user(user_id)
            if not me:
                logger.error(msg="Access denied")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            if not user:
                logger.error(msg="User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            if me.id == user.id:
                logger.error(msg="Trying to follow yourself")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You can not follow yourself"
                )
            try:
                stmt = insert(users_connections).values(
                    follower_id=me.id,
                    followed_id=user.id
                )
                await self.session.execute(stmt)
                await self.session.commit()
                return PositiveResponse(result=True)
            except IntegrityError:
                logger.error(msg="Trying to follow the user which is already being followed")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You are already following this user"
                )

    async def unfollow_user(self, user_id: int, me: User):
        async with self.session.begin():
            if not me:
                logger.error(msg="Access denied")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            stmt = select(users_connections).where(
                (column('follower_id') == me.id) &
                (column('followed_id') == user_id)
                )
            follow = await self.session.execute(stmt)
            follow = follow.scalar_one_or_none()
            if follow:
                stmt = delete(users_connections).where(
                    (column('follower_id') == me.id) &
                    (column('followed_id') == user_id)
                )
                await self.session.execute(stmt)
                return PositiveResponse(result=True)
            logger.error(msg="Trying to unfollow user which is not being followed")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are not following this user"
            )
