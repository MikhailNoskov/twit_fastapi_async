import logging.config

from fastapi import status
from sqlalchemy import select, insert, column, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload


from models.users import User, users_connections
from schema.users import UserRegister
from schema.positive import PositiveResponse
from logging_conf import logs_config
from database.services import AbstractService
from exceptions.custom_exceptions import CustomException


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_users")
logger.setLevel("DEBUG")


class UserService(AbstractService):
    """
    Service for db connection for User cors
    """
    async def create_user(self, data: UserRegister) -> dict:
        """
        Create new User method
        :param data: User info received
        :return: User create confirmation
        """
        async with self.session.begin():
            user = await self.session.execute(select(User).where(User.name == data.username))
            user = user.scalar_one_or_none()
            if user:
                error_message = "User with supplied username exists"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_409_CONFLICT
                )
            user = await self.session.execute(select(User).where(User.api_key == data.api_key))
            user = user.scalar_one_or_none()
            if user:
                error_message = "User with supplied api_key exists"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_409_CONFLICT
                )
            user = User(name=data.username, password=data.password, api_key=data.api_key)
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            logger.info(msg="User successfully registered")
            return {
                "message": "User successfully registered!"
            }

    async def get_me(self, me: User) -> User:
        """
        Get current authenticated user method
        :param user_id: int
        :return: User instance
        """
        async with self.session.begin():
            if not me:
                error_message = "User not found"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND
                )
            user = await self.session.execute(select(User).where(User.id == me.id).options(
             joinedload(User.followers),
             joinedload(User.following)))
            user = user.scalar()
            logger.debug('User retrieved for me endpoint')
            return user

    async def get_user(self, user_id: int) -> User:
        """
        Get user by ID method
        :param user_id: int
        :return: User instance
        """
        user = await self.session.execute(select(User).where(User.id == user_id).options(
         joinedload(User.followers),
         joinedload(User.following)))
        user = user.scalar()
        if not user:
            error_message = "User not found"
            logger.exception(msg=error_message)
            raise CustomException(
                error_type='users',
                error_message=error_message,
                response_status=status.HTTP_404_NOT_FOUND
            )
        logger.debug('User retrieved for id endpoint')
        return user

    async def set_follow_user(self, user_id: int, me: User) -> PositiveResponse:
        """
        Follow user method
        :param user_id: int
        :param me: Curent authenticated user
        :return: Positive response in case of successful follow
        """
        async with self.session.begin():
            user = await self.get_user(user_id)
            if not me:
                error_message = 'Access denied'
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN
                )
            if not user:
                error_message = "User not found"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND
                )
            if me.id == user.id:
                error_message = "Trying to follow yourself"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND
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
                error_message = "Trying to follow the user which is already being followed"
                logger.exception(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND
                )

    async def unfollow_user(self, user_id: int, me: User) -> PositiveResponse:
        """
        Unfollow user method
        :param user_id: int
        :param me: Curent authenticated user
        :return: Positive response in case of successful unfollow
        """
        async with self.session.begin():
            if not me:
                error_message = 'Access denied'
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type='users',
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN
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
            error_message = "Trying to unfollow user which is not being followed"
            logger.exception(msg=error_message)
            raise CustomException(
                error_type='users',
                error_message=error_message,
                response_status=status.HTTP_404_NOT_FOUND
            )
