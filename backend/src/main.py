import sentry_sdk

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin

from models.users import User
from models.tweets import Tweet, Like
from models.media import Media
from database.get_user import verify_api_key
from routes.users import user_router
from routes.tweets import tweet_router
from routes.media import media_router
from exceptions.custom_exceptions import CustomException


sentry_sdk.init(
    dsn="https://c699f8e763ecd3e18f34cd56ed3b435c@o1075355.ingest.sentry.io/4505930641309696",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()

app.include_router(user_router, prefix='/api/users')
app.include_router(tweet_router, prefix='/api/tweets')
app.include_router(media_router, prefix='/api/medias')


@app.middleware("http")
async def add_user(request: Request, call_next):
    """
    Current User middleware
    :param request: Request
    :param call_next: callable
    :return: call_next function returned
    """
    if 'api-key' in request.headers.keys():
        api_key = request.headers.get('api-key', None)
        user = await verify_api_key(api_key=api_key)
        request.state.user = user
    else:
        request.state.user = None
    return await call_next(request)


@app.get('/api/userinfo/')
def index():
    """
    Userinfo endpoint
    :return: Redirect to get current user endpoint
    """
    return RedirectResponse(url="/api/users/me")


@app.get("/sentry-debug")
async def trigger_error():
    """
    Sentry debug endpoint
    :return: ZeroDivisionError
    """
    return 1 / 0


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    exception = exc.to_dict()
    status_code = exception.pop('status', 404)
    return JSONResponse(
        status_code=status_code,
        content=dict(**exception)
    )

app.mount('/images', StaticFiles(directory='images'), name='images')

site = AdminSite(
    settings=Settings(
        version='1.0.0',
        site_title='Twitter',
        language="en_US",
        amis_theme="antd",
        database_url_async='postgresql+asyncpg://postgres:postgres@localhost:5432/twitter'
    )
)


# Admin models added
@site.register_admin
class UserAdmin(admin.ModelAdmin):
    page_schema = 'User'
    model = User


@site.register_admin
class TweetAdmin(admin.ModelAdmin):
    page_schema = 'Tweet'
    model = Tweet


@site.register_admin
class LikeAdmin(admin.ModelAdmin):
    page_schema = 'Like'
    model = Like


@site.register_admin
class ImageAdmin(admin.ModelAdmin):
    page_schema = 'Image'
    model = Media


# Admin site mounted
site.mount_app(app)
