from typing import Optional

from fastapi import HTTPException, status, Depends, Header
from sqlalchemy import select, insert, update, column, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, subqueryload, aliased


from models.tweets import Tweet, Like
from models.users import User
from models.media import Media
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from schema.users import UserFollower
from schema.positive import PositiveResponse
from database.connection import async_session_maker as session


async def create_new_tweet(request: TweetCreate, api_key: str):
    async with session() as db:
        async with db.begin():
            #  TODO write get user method for all the endpoint
            user = await db.execute(select(User).where(User.api_key == api_key))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            new_tweet = Tweet(
                content=request.text,
                author=user
            )
            db.add(new_tweet)
            await db.flush()
            await db.refresh(new_tweet)
            if request.attachments:
                await db.execute(update(Media).where(Media.id.in_(request.attachments)).values(tweet_id=new_tweet.id))
            tweet = TweetResponse(tweet_id=new_tweet.id)
            return tweet


async def remove_tweet(tweet_id: int, api_key: str):
    async with session() as db:
        async with db.begin():
            user = await db.execute(select(User).where(User.api_key == api_key))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            tweet = await db.execute(select(Tweet).where(Tweet.id == tweet_id))
            tweet = tweet.scalar_one_or_none()
            if not tweet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tweet not found"
                )
            if user.id != tweet.author_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You can not delete this tweet"
                )
            await db.delete(tweet)
            return PositiveResponse(result=True)


async def create_like(tweet_id: int, api_key: str):
    async with session() as db:
        async with db.begin():
            me = await db.execute(select(User).where(User.api_key == api_key))
            me = me.scalar_one_or_none()
            if not me:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            like = await db.execute(select(Like).where(Like.user_id == me.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if like:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You have already liked this tweet"
                )
            new_like = Like(user_id=me.id, tweet_id=tweet_id)
            db.add(new_like)
            await db.flush()
            await db.refresh(new_like)
            return PositiveResponse(result=True)


async def delete_like(tweet_id: int, api_key: str):
    async with session() as db:
        async with db.begin():
            me = await db.execute(select(User).where(User.api_key == api_key))
            me = me.scalar_one_or_none()
            if not me:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            like = await db.execute(select(Like).where(Like.user_id == me.id, Like.tweet_id == tweet_id))
            like = like.scalar_one_or_none()
            if not like:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You have not liked this tweet"
                )
            await db.delete(like)
            return PositiveResponse(result=True)


# @tweet_router.get('/', response_model=List[TweetDisplay])
async def get_all_tweets(api_key: Optional[str] = Header(...)):
    async with session() as db:
        async with db.begin():
            # tweets = await db.execute(select(Tweet).options(selectinload(Tweet.author), subqueryload(Tweet.liked)))
            tweets = await db.execute(select(Tweet).options(
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
            return TweetsList(result=True, tweets=tweets_response)
            # return TweetsList(result=True, tweets=[TweetDisplay.from_orm(tweet) for tweet in tweets])
