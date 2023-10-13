from pydantic import BaseModel
from typing import List


class UserRegister(BaseModel):
    """
    User register schema
    """

    username: str
    password: str
    api_key: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "mike@klike.com",
                "password": "strong!!!",
                "api_key": "test",
            }
        }


class UserFollower(BaseModel):
    """
    User follower schema
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class UserFollowing(BaseModel):
    """
    Followed User schema
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class UserForResponse(BaseModel):
    """
    User response schema
    """

    id: int
    name: str
    followers: List[UserFollower] = []
    following: List[UserFollowing] = []

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    User response with result schema
    """

    result: bool
    user: UserForResponse

    class Config:
        orm_mode = True
