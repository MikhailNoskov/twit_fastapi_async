from typing import Optional
import uvicorn
import sentry_sdk


from fastapi import FastAPI, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.requests import Request

from database.get_user import verify_api_key
from routes.users import user_router
from routes.tweets import tweet_router
from routes.media import media_router
from models.users import User

sentry_sdk.init(
    dsn="https://c699f8e763ecd3e18f34cd56ed3b435c@o1075355.ingest.sentry.io/4505930641309696",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI()

app.include_router(user_router, prefix='/api/users')
app.include_router(tweet_router, prefix='/api/tweets')
app.include_router(media_router, prefix='/api/medias')


@app.middleware("http")
async def add_user(request: Request, call_next):
    if 'api-key' in request.headers.keys():
        api_key = request.headers.get('api-key', None)
        user = await verify_api_key(api_key=api_key)
        request.state.user = user
    else:
        request.state.user = None
    return await call_next(request)


@app.get('/api/userinfo/')
def index():
    return RedirectResponse(url="/api/users/me")


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/images', StaticFiles(directory='images'), name='images')
