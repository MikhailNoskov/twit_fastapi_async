from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends
from models.tweets import Tweet, Like
from schema.tweets import TweetDisplay, TweetsList, TweetCreate, TweetResponse
from database.connection import get_session
from sqlalchemy import select
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
        # request: Request, db: Session = Depends(get_db)
):
    pass
#
#
# @app.post('/api/medias')
# async def post_image(request: Request, db: Session = Depends(get_db)):
#     pass
#
#


@tweet_router.post('/{tweet_id}/likes')
async def like_tweet(
        # request: Request, db: Session = Depends(get_db)
                     ):
    pass


@tweet_router.delete('/{tweet_id}/likes')
async def unlike_tweet(
        # request: Request, db: Session = Depends(get_db)
                     ):
    pass

#
#
# @app.delete('/api/tweets/{tweet_id}/likes')
# async def send_tweet(request: Request, db: Session = Depends(get_db)):
#     pass
#
#
# @app.post('/api/users/{user_id}/follow')
# async def send_tweet(request: Request, db: Session = Depends(get_db)):
#     pass
#
#
# @app.delete('/api/users/{user_id}/follow')
# async def send_tweet(request: Request, db: Session = Depends(get_db)):
#     pass
# @app.get("/")
# async def home(request: Request, db: Session = Depends(get_db)):
#     todos = db.query(models.Smth).all()
#     return templates.TemplateResponse("base.html",
#                                       {"request": request, "todo_list": todos})
