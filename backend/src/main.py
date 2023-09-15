import uvicorn
from fastapi import FastAPI
from routes.users import user_router
from routes.tweets import tweet_router
from routes.media import media_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(user_router, prefix='/api/users')
app.include_router(tweet_router, prefix='/api/tweets')
app.include_router(media_router, prefix='/api/medias')


@app.get('/api/userinfo/')
def index():
    return RedirectResponse(url="/api/users/me")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
