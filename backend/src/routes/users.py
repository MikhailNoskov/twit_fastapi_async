import logging.config
from typing import Optional

from fastapi import APIRouter, Header, Depends
from fastapi.requests import Request

from schema.users import UserRegister, UserResponse
from schema.positive import PositiveResponse
from database.users import UserService
from logging_conf import logs_config


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.user_routes")
logger.setLevel("DEBUG")


user_router = APIRouter(
    tags=["users"]
)


@user_router.post("/signup")
async def sign_new_user(data: UserRegister, service: UserService = Depends()) -> dict:
    """
    Sign up enpoint
    :param data: User info
    :param service: User db connection service
    :return: New user create method of User service
    """
    logger.debug(msg='Trying register new user')
    return await service.create_user(data=data)


@user_router.get('/me', response_model=UserResponse)
async def me(request: Request, service: UserService = Depends(), api_key: Optional[str] = Header(None)):
    """
    Current user info endpoint
    :param request: Request
    :param service: User db connection service
    :param api_key: str
    :return: Get current authenticated user method of User service
    """
    logger.info(msg='Me endpoint called')
    me = request.state.user
    result = await service.get_me(me)
    return {"result": True, "user": result}


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, service: UserService = Depends(), api_key: Optional[str] = Header(None)):
    """
    Get User by ID endpoint
    :param user_id: int
    :param service: User db connection service
    :param api_key: str
    :return: Get user by ID method of User service
    """
    logger.info(msg=f'Get {user_id} endpoint called')
    result = await service.get_user(user_id)
    return {"result": True, "user": result}


@user_router.post('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(
        request: Request,
        user_id: int,
        service: UserService = Depends(),
        api_key: Optional[str] = Header(None)
):
    """
    Follow User endpoint
    :param request: Request
    :param user_id: int
    :param service: User db connection service
    :param api_key: str
    :return: Follow user by ID method of User service
    """
    logger.info(msg=f'{request.state.user} tries to follow user {user_id}')
    return await service.set_follow_user(user_id, request.state.user)


@user_router.delete('/{user_id}/follow', response_model=PositiveResponse)
async def stop_follow_user(
        request: Request,
        user_id: int,
        service: UserService = Depends(),
        api_key: Optional[str] = Header(None)
):
    """
    Unfollow User endpoint
    :param request: Request
    :param user_id: int
    :param service: User db connection service
    :param api_key: str
    :return: Unfollow user by ID method of User service
    """
    logger.info(msg=f'{request.state.user} tries to unfollow user {user_id}')
    return await service.unfollow_user(user_id, request.state.user)
