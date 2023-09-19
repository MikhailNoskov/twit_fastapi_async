from typing import Optional

from fastapi import APIRouter, Header

from schema.users import UserRegister, UserResponse
from schema.positive import PositiveResponse
from database.users import create_user, get_me, get_user, set_follow_user, unfollow_user


user_router = APIRouter(
    tags=["users"]
)


@user_router.post("/signup")
async def sign_new_user(data: UserRegister) -> dict:
    return await create_user(data=data)


@user_router.get('/me', response_model=UserResponse)
async def me(api_key: Optional[str] = Header(...)):
    result = await get_me(api_key)
    return {"result": True, "user": result}


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, api_key: Optional[str] = Header(...)):
    result = await get_user(user_id)
    return {"result": True, "user": result}


@user_router.post('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(user_id: int, api_key: Optional[str] = Header(...)):
    return await set_follow_user(user_id, api_key)


@user_router.delete('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(user_id: int, api_key: Optional[str] = Header(...)):
    return await unfollow_user(user_id, api_key)
