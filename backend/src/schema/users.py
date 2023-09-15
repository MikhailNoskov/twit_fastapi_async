from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserRegister(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "mike@klike.com",
                "password": "strong!!!",
            }
        }


class UserFollower(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserFollowing(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserForResponse(BaseModel):
    id: int
    name: str
    followers: List[UserFollower] = None
    following: List[UserFollowing] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    result: bool
    user: UserForResponse

    class Config:
        orm_mode = True
