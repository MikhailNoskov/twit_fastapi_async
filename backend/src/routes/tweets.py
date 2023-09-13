from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends
from models.tweets import Tweet, Like
from models.media import Media
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from database.connection import get_session
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, subqueryload, aliased
from fastapi.responses import JSONResponse
from models.users import User
from schema.users import UserFollower


tweet_router = APIRouter(
    tags=["tweets"]
)


@tweet_router.post('/', response_model=TweetResponse)
async def post_new_tweet(request: TweetCreate, api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
    async with db.begin():
        #TODO write get user method for all the endpoint
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
        await db.execute(update(Media).where(Media.id.in_(request.attachments)).values(tweet_id=new_tweet.id))
        tweet = TweetResponse(tweet_id=new_tweet.id)
        return tweet


@tweet_router.get('/', response_model=TweetsList)
# @tweet_router.get('/', response_model=List[TweetDisplay])
async def get_all_tweets(api_key: Optional[str] = Header(None), db: AsyncSession = Depends(get_session)):
    async with db.begin():
        # tweets = await db.execute(select(Tweet).options(selectinload(Tweet.author), subqueryload(Tweet.liked)))
        tweets = await db.execute(select(Tweet).options(
            selectinload(Tweet.author),  # Eagerly load Author
            subqueryload(Tweet.likes).options(subqueryload(Like.user))  # Eagerly load Likes
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
                likes=[]
            )
            for like in tweet.likes:
                tweet_display.likes.append(
                    UserFollower(id=like.user.id, name=like.user.name)
                )
            tweets_response.append(tweet_display)
        return TweetsList(result=True, tweets=tweets_response)


@tweet_router.delete('/{tweet_id}')
async def delete_tweet(
        tweet_id: int,
        api_key: Optional[str] = Header(None),
        db: AsyncSession = Depends(get_session)
        # request: Request, db: Session = Depends(get_db)
):
    async with db.begin():
        user = await db.execute(select(User).where(User.api_key == api_key))
        user = user.scalar_one_or_none()
        print('User: ', user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        tweet = await db.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = tweet.scalar_one_or_none()
        print('Tweet: ', tweet.__dict__)

        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tweet not found"
            )
        # print('Ids: ', user.id, tweet.author_id)
        if user.id != tweet.author_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You can not delete this post"
            )
        await db.delete(tweet)
        return {"result": True}


@tweet_router.post('/{tweet_id}/likes')
async def like_tweet(
        tweet_id: int,
        api_key: Optional[str] = Header(None),
        db: AsyncSession = Depends(get_session)
):
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
        return {"result": True}


@tweet_router.delete('/{tweet_id}/likes')
async def unlike_tweet(
        tweet_id: int,
        api_key: Optional[str] = Header(None),
        db: AsyncSession = Depends(get_session)
):
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
        return {"result": True}
