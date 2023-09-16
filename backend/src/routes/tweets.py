from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from schema.positive import PositiveResponse
from database.tweets import create_new_tweet, remove_tweet, create_like, delete_like, get_all_tweets
from database.users import set_follow_user, unfollow_user

tweet_router = APIRouter(tags=["tweets"])


@tweet_router.post('/', response_model=TweetResponse)
async def post_new_tweet(data: TweetCreate, api_key: Optional[str] = Header(...)):
    return await create_new_tweet(data, api_key)


@tweet_router.delete('/{tweet_id}')
async def delete_tweet(tweet_id: int, api_key: Optional[str] = Header(...)):
    return await remove_tweet(tweet_id, api_key)


@tweet_router.post('/{tweet_id}/likes')
async def like_tweet(tweet_id: int, api_key: Optional[str] = Header(...)):
    return await create_like(tweet_id, api_key)


@tweet_router.delete('/{tweet_id}/likes')
async def unlike_tweet(tweet_id: int, api_key: Optional[str] = Header(...)):
    return await delete_like(tweet_id, api_key)


@tweet_router.get('/', response_model=TweetsList)
# @tweet_router.get('/', response_model=List[TweetDisplay])
async def get_tweets(api_key: Optional[str] = Header(...)):
    return await get_all_tweets(api_key)


@tweet_router.post('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(user_id: int, api_key: Optional[str] = Header(...)):
    return await set_follow_user(user_id, api_key)


@tweet_router.delete('/{user_id}/follow', response_model=PositiveResponse)
async def follow_user(user_id: int, api_key: Optional[str] = Header(...)):
    return await unfollow_user(user_id, api_key)
