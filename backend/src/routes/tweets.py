import logging.config
from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends
from fastapi.requests import Request

from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from schema.positive import PositiveResponse
from database.tweets import create_new_tweet, remove_tweet, create_like, delete_like, get_all_tweets
from database.users import set_follow_user, unfollow_user
from logging_conf import logs_config


tweet_router = APIRouter(tags=["tweets"])

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.tweets_routes")
logger.setLevel("DEBUG")


@tweet_router.post('/', response_model=TweetResponse)
async def post_new_tweet(request: Request, data: TweetCreate, api_key: Optional[str] = Header(...)):
    user = request.state.user
    logger.info(msg=f'User {user} tries creating a tweet')
    return await create_new_tweet(user, data)


@tweet_router.delete('/{tweet_id}')
async def delete_tweet(request: Request, tweet_id: int, api_key: Optional[str] = Header(...)):
    user = request.state.user
    logger.info(msg=f'User {user} tries deleting a tweet')
    return await remove_tweet(user, tweet_id)


@tweet_router.post('/{tweet_id}/likes')
async def like_tweet(request: Request, tweet_id: int, api_key: Optional[str] = Header(...)):
    user = request.state.user
    logger.info(msg=f'User {user} tries liking a tweet {tweet_id}')
    return await create_like(user, tweet_id)


@tweet_router.delete('/{tweet_id}/likes')
async def unlike_tweet(request: Request, tweet_id: int, api_key: Optional[str] = Header(...)):
    user = request.state.user
    logger.info(msg=f'User {user} tries unliking a tweet {tweet_id}')
    return await delete_like(user, tweet_id)


@tweet_router.get('/', response_model=TweetsList)
# @tweet_router.get('/', response_model=List[TweetDisplay])
async def get_tweets(request: Request, api_key: Optional[str] = Header(...)):
    logger.debug(msg='All tweets endpoint called')
    user = request.state.user
    return await get_all_tweets(user)
