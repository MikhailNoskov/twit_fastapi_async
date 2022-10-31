from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/api/users/me')
async def me(request: Request, db: Session = Depends(get_db)):
    pass


@app.get('/api/users/{user_id}')
async def user(request: Request, db: Session = Depends(get_db)):
    pass


@app.post('/api/tweets')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass


@app.delete('/api/tweets/{tweet_id}')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass


@app.post('/api/medias')
async def post_image(request: Request, db: Session = Depends(get_db)):
    pass


@app.post('/api/tweets/{tweet_id}/likes')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass


@app.delete('/api/tweets/{tweet_id}/likes')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass


@app.post('/api/users/{user_id}/follow')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass


@app.delete('/api/users/{user_id}/follow')
async def send_tweet(request: Request, db: Session = Depends(get_db)):
    pass
# @app.get("/")
# async def home(request: Request, db: Session = Depends(get_db)):
#     todos = db.query(models.Smth).all()
#     return templates.TemplateResponse("base.html",
#                                       {"request": request, "todo_list": todos})
#
#
# @app.post("/add")
# async def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
#     new_todo = models.Smth(title=title)
#     db.add(new_todo)
#     db.commit()
#
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
#
#
# @app.get("/update/{todo_id}")
# async def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
#     smth = db.query(models.Smth).filter(models.Smth.id == todo_id).first()
#     smth.complete = not smth.complete
#     db.commit()
#
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
#
#
# @app.get("/delete/{todo_id}")
# async def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
#     smth = db.query(models.Smth).filter(models.smth.id == todo_id).first()
#     db.delete(smth)
#     db.commit()
#
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)