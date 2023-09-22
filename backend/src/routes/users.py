import logging.config
from typing import Optional

from fastapi import APIRouter, Header
from fastapi.requests import Request

from schema.users import UserRegister, UserResponse
from schema.positive import PositiveResponse
from database.users import create_user, get_me, get_user, set_follow_user, unfollow_user
from logging_conf import logs_config


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.user_endpoint")
logger.setLevel("DEBUG")


user_router = APIRouter(
    tags=["users"]
)


@user_router.post("/signup")
async def sign_new_user(data: UserRegister) -> dict:
    logger.debug(msg='New user registered')
    return await create_user(data=data)


@user_router.get('/me', response_model=UserResponse)
async def me(request: Request, api_key: Optional[str] = Header(...)):
    logger.info(msg='Me endpoint called')
    me = request.state.user
    result = await get_me(me.id)
    return {"result": True, "user": result}


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, api_key: Optional[str] = Header(...)):
    result = await get_user(user_id)
    return {"result": True, "user": result}


@user_router.post('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(request: Request, user_id: int, api_key: Optional[str] = Header(...)):
    return await set_follow_user(user_id, request.state.user)


@user_router.delete('/{user_id}/follow', response_model=PositiveResponse)
async def stop_follow_user(request: Request, user_id: int, api_key: Optional[str] = Header(...)):
    return await unfollow_user(user_id, request.state.user)
