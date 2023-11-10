import logging.config
from typing import Optional

from fastapi import APIRouter, Header, Depends
from fastapi.requests import Request

from schema.tweets import TweetsList, TweetCreate, TweetResponse
from schema.positive import PositiveResponse
from database.tweets import TweetService
from logging_conf import logs_config
from utils.response_info import TWEET_ERROR_RESPONSES

tweet_router = APIRouter(tags=["tweets"])

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.tweets_routes")
logger.setLevel("DEBUG")


@tweet_router.post(
    "/",
    response_model=TweetResponse,
    status_code=201,
    responses={
        '403': TWEET_ERROR_RESPONSES[403]
    }
)
async def post_new_tweet(
    request: Request,
    data: TweetCreate,
    service: TweetService = Depends(),
    api_key: Optional[str] = Header(None),
):
    """
    New tweet create endpoint
    -------------------------
    :param\n
    request: Request\n
    data: Tweet info received\n
    service: Tweet db connection service instance\n
    api_key: str\n
    :return\n
    Tweet create method of Tweet service
    """
    user = request.state.user
    logger.info(msg=f"User {user} tries creating a tweet")
    return await service.create_new_tweet(user, data)


@tweet_router.delete(
    "/{tweet_id}",
    response_model=PositiveResponse,
    responses={
        '403': TWEET_ERROR_RESPONSES[403],
        '404': TWEET_ERROR_RESPONSES[404],
    }
)
async def delete_tweet(
    request: Request,
    tweet_id: int,
    service: TweetService = Depends(),
    api_key: Optional[str] = Header(None),
):
    """
    Tweet delete endpoint
    ----------------------
    :param request: Request\n
    :param tweet_id: int\n
    :param service: Tweet db connection service instance\n
    :param api_key: str\n
    :return: Tweet delete method of Tweet service\n
    """
    user = request.state.user
    logger.info(msg=f"User {user} tries deleting a tweet")
    return await service.remove_tweet(user, tweet_id)


@tweet_router.post(
    "/{tweet_id}/likes",
    response_model=PositiveResponse,

    status_code=201,
    responses={
        '403': TWEET_ERROR_RESPONSES[403],
        '404': TWEET_ERROR_RESPONSES[404],
    }
)
async def like_tweet(
    request: Request,
    tweet_id: int,
    service: TweetService = Depends(),
    api_key: Optional[str] = Header(None),
):
    """
    Like tweet enpoint
    --------------------
    :param request: Request\n
    :param tweet_id: int\n
    :param service: Tweet db connection service instance\n
    :param api_key: str\n
    :return: Tweet like create method of Tweet service\n
    """
    user = request.state.user
    logger.info(msg=f"User {user} tries liking a tweet {tweet_id}")
    return await service.create_like(user, tweet_id)


@tweet_router.delete(
    "/{tweet_id}/likes",
    response_model=PositiveResponse,
    responses={
        '403': TWEET_ERROR_RESPONSES[403],
        '404': TWEET_ERROR_RESPONSES[404],
    }
)
async def unlike_tweet(
    request: Request,
    tweet_id: int,
    service: TweetService = Depends(),
    api_key: Optional[str] = Header(None),
):
    """
    Unlike tweet enpoint
    ---------------------
    :param request: Request\n
    :param tweet_id: int\n
    :param service: Tweet db connection service instance\n
    :param api_key: str\n
    :return: Tweet like delete method of Tweet service\n
    """
    user = request.state.user
    logger.info(msg=f"User {user} tries unliking a tweet {tweet_id}")
    return await service.delete_like(user, tweet_id)


@tweet_router.get(
    "/",
    response_model=TweetsList,
    responses={
        "403": TWEET_ERROR_RESPONSES[403]
    }
)
async def get_tweets(
    request: Request,
    service: TweetService = Depends(),
    api_key: Optional[str] = Header(None),
    # authed = Depends(authenticate)
):
    """
    Get all tweets enpoint
    -----------------------
    :param request: Request\n
    :param service: Tweet db connection service instance\n
    :param api_key: str\n
    :return: Get all tweets method of Tweet service\n
    """
    logger.debug(msg="All tweets endpoint called")
    user = request.state.user
    return await service.get_all_tweets(user)
