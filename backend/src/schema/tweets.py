from pydantic import BaseModel
from typing import Optional, List
from schema.users import UserFollower


class TweetDisplay(BaseModel):
    """
    Tweet full info display schema
    """

    id: int
    content: str
    author: UserFollower
    likes: List[UserFollower] = []
    attachments: List[str] = []

    class Config:
        orm_mode = True


class TweetsList(BaseModel):
    """
    List of tweets schema
    """

    result: bool = True
    tweets: List[TweetDisplay]

    class Config:
        orm_mode = True


class TweetCreate(BaseModel):
    """
    Tweet created schema
    """

    tweet_data: str
    tweet_media_ids: Optional[List[int]]


class TweetResponse(BaseModel):
    """
    Tweet response schema
    """

    result: bool = True
    tweet_id: int

    class Config:
        orm_mode = True
