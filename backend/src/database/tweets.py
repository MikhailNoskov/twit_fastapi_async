from typing import Optional
import logging.config

from fastapi import status, Header
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, subqueryload


from models.tweets import Tweet, Like
from models.users import User
from models.media import Media
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from schema.users import UserFollower
from schema.positive import PositiveResponse
from logging_conf import logs_config
from database.services import AbstractService
from exceptions.custom_exceptions import CustomException

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_tweets")
logger.setLevel("DEBUG")


class TweetService(AbstractService):
    """
    Service for db connection for Tweet cors
    """

    async def create_new_tweet(self, user: User, data: TweetCreate) -> TweetResponse:
        """
        New tweet create method
        :param user: User instance
        :param data: Tweet data including content, likes and author info
        :return: Tweet response with the id of tweet created
        """
        async with self.session.begin():
            if not user:
                error_message = "Access denied"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            new_tweet = Tweet(content=data.tweet_data, author=user)
            self.session.add(new_tweet)
            await self.session.flush()
            await self.session.refresh(new_tweet)
            if data.tweet_media_ids:
                await self.session.execute(
                    update(Media).where(Media.id.in_(data.tweet_media_ids)).values(tweet_id=new_tweet.id)
                )
            tweet = TweetResponse(tweet_id=new_tweet.id)
            logger.info(msg="Tweet created")
            return tweet

    async def remove_tweet(self, user: User, tweet_id: int) -> PositiveResponse:
        """
        Tweet delete method
        :param user: User instance
        :param tweet_id: ID of the tweet being deleted
        :return: Positive response in case of successful delete
        """
        async with self.session.begin():
            if not user:
                error_message = "Access denied"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            tweet = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
            tweet = tweet.scalar_one_or_none()
            if not tweet:
                error_message = "Tweet not found"
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND,
                )
            if user.id != tweet.author_id:
                error_message = "Tweet can not be deleted by this user"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            await self.session.delete(tweet)
            logger.warning(msg="Tweet has been deleted")
            return PositiveResponse(result=True)

    async def create_like(self, user, tweet_id: int) -> PositiveResponse:
        """
        Like created method
        :param user: User instance
        :param tweet_id: ID of the tweet being liked
        :return: Positive response in case of successful like
        """
        async with self.session.begin():
            if not user:
                error_message = "Access denied"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="likes",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            tweet = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
            tweet = tweet.scalar_one_or_none()
            if not tweet:
                error_message = "Tweet not found"
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND,
                )
            like = await self.session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if like:
                logger.debug(msg="Redirected to dislike tweet")
                await self.session.delete(like)
                logger.debug(msg="Tweet is unliked")
                return PositiveResponse(result=True)
            new_like = Like(user_id=user.id, tweet_id=tweet_id)
            self.session.add(new_like)
            await self.session.flush()
            await self.session.refresh(new_like)
            logger.debug(msg="Tweet is liked")
            return PositiveResponse(result=True)

    async def delete_like(self, user, tweet_id: int) -> PositiveResponse:
        """
        Like delete method
        :param user: User instance
        :param tweet_id: ID of the tweet being unliked
        :return: Positive response in case of successful unlike
        """
        async with self.session.begin():
            if not user:
                error_message = "Access denied"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="likes",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            like = await self.session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if not like:
                error_message = "The tweet can not be unliked"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_404_NOT_FOUND,
                )
            await self.session.delete(like)
            logger.debug(msg="Tweet is unliked")
            return PositiveResponse(result=True)

    async def get_all_tweets(self, user, api_key: Optional[str] = Header(...)):
        """
        Get all the tweets for the current user
        :param user: Instance of current user
        :param api_key: #  Remove it!!!!
        :return: List of the Tweets which can be seen by current User
        """
        async with self.session.begin():
            if not user:
                error_message = "Access denied"
                logger.warning(msg=error_message)
                raise CustomException(
                    error_type="tweets",
                    error_message=error_message,
                    response_status=status.HTTP_403_FORBIDDEN,
                )
            tweets = await self.session.execute(
                select(Tweet).options(
                    selectinload(Tweet.author),  # Eagerly load Author
                    subqueryload(Tweet.likes).options(subqueryload(Like.user)),
                    subqueryload(Tweet.attachments),  # Eagerly load Likes
                )
            )
            tweets = tweets.scalars().all()
            tweets_response = []
            for tweet in tweets:
                tweet_display = TweetDisplay(
                    id=tweet.id,
                    content=tweet.content,
                    author=UserFollower(id=tweet.author.id, name=tweet.author.name),
                    likes=[],
                    attachments=[],
                )
                for like in tweet.likes:
                    tweet_display.likes.append(UserFollower(id=like.user.id, name=like.user.name))
                for attachment in tweet.attachments:
                    tweet_display.attachments.append(attachment.media_url)
                tweets_response.append(tweet_display)
            # Optimize with db query
            tweets_response = sorted(tweets_response, key=lambda t: len(t.likes), reverse=True)
            logger.debug(msg="All tweets retrieved")
            return TweetsList(result=True, tweets=tweets_response)
