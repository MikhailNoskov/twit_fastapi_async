from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from database.tweets import create_new_tweet, remove_tweet, create_like, delete_like, get_all_tweets


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