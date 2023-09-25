from typing import Optional
import logging.config

from fastapi import HTTPException, status, Depends, Header
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload, subqueryload, aliased


from models.tweets import Tweet, Like
from models.users import User
from models.media import Media
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from schema.users import UserFollower
from schema.positive import PositiveResponse
from logging_conf import logs_config
from database.services import AbstractService


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_tweets")
logger.setLevel("DEBUG")


class TweetService(AbstractService):
    async def create_new_tweet(self, user: User, data: TweetCreate):
        async with self.session.begin():
            if not user:
                logger.warning(msg='Access denied')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            new_tweet = Tweet(
                content=data.tweet_data,
                author=user
            )
            self.session.add(new_tweet)
            await self.session.flush()
            await self.session.refresh(new_tweet)
            if data.tweet_media_ids:
                await self.session.execute(
                    update(
                        Media
                    ).where(
                        Media.id.in_(
                            data.tweet_media_ids
                        )
                    ).values(tweet_id=new_tweet.id))
            tweet = TweetResponse(tweet_id=new_tweet.id)
            logger.info(msg='Tweet created')
            return tweet

    async def remove_tweet(self, user: User, tweet_id: int):
        async with self.session.begin():
            if not user:
                logger.warning(msg='Access denied')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            tweet = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
            tweet = tweet.scalar_one_or_none()
            if not tweet:
                logger.warning(msg='Tweet not found')
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tweet not found"
                )
            if user.id != tweet.author_id:
                logger.warning(msg='Tweet can not be deleted by this user')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can not delete this tweet"
                )
            await self.session.delete(tweet)
            logger.warning(msg='Tweet has been deleted')
            return PositiveResponse(result=True)

    async def create_like(self, user, tweet_id: int):
        async with self.session.begin():
            if not user:
                logger.warning(msg='Access denied')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            like = await self.session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if like:
                logger.debug(msg='Redirected to dislike tweet')
                await self.session.delete(like)
                logger.debug(msg='Tweet is unliked')
                return PositiveResponse(result=True)
            new_like = Like(user_id=user.id, tweet_id=tweet_id)
            self.session.add(new_like)
            await self.session.flush()
            await self.session.refresh(new_like)
            logger.debug(msg='Tweet is liked')
            return PositiveResponse(result=True)

    async def delete_like(self, user, tweet_id: int):
        async with self.session.begin():
            if not user:
                logger.warning(msg='Access denied')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            like = await self.session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if not like:
                logger.warning(msg='The tweet can not be unliked')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You have not liked this tweet"
                )
            await self.session.delete(like)
            logger.debug(msg='Tweet is unliked')
            return PositiveResponse(result=True)

    async def get_all_tweets(self, user, api_key: Optional[str] = Header(...)):
        async with self.session.begin():
            tweets = await self.session.execute(select(Tweet).options(
                selectinload(Tweet.author),  # Eagerly load Author
                subqueryload(Tweet.likes).options(subqueryload(Like.user)),
                subqueryload(Tweet.attachments)  # Eagerly load Likes
            ))
            tweets = tweets.scalars().all()
            tweets_response = []
            for tweet in tweets:
                tweet_display = TweetDisplay(
                    id=tweet.id,
                    content=tweet.content,
                    author=UserFollower(
                        id=tweet.author.id,
                        name=tweet.author.name
                    ),
                    likes=[],
                    attachments=[]
                )
                for like in tweet.likes:
                    tweet_display.likes.append(
                        UserFollower(id=like.user.id, name=like.user.name)
                    )
                for attachment in tweet.attachments:
                    tweet_display.attachments.append(attachment.media_url)
                tweets_response.append(tweet_display)
            # Optimize with db query
            tweets_response = sorted(tweets_response, key=lambda t: len(t.likes), reverse=True)
            logger.debug(msg='All tweets retrieved')
            return TweetsList(result=True, tweets=tweets_response)
