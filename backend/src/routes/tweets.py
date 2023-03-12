# @app.get('/api/tweets/{api_key}')
# async def send_tweet(api_key: str):
#     print(api_key)
#     # print(request.__dict__)
#     # print(request.__dict__['scope']['_query_params'])
#     if api_key == 'test':
#         return {
#             "result": "true",
#             "tweets": [
#                 {
#                     "id": 1,
#                     "content": "Hello Hi!",
#                     "attachments": [],
#                     "author":
#                         {
#                             "id": 1,
#                             "name": "Mike"
#                         },
#                     "likes": [
#                         {
#                             "user_id": 2,
#                             "name": "Alla"
#                         }
#                     ]
#                 }
#             ]
#         }
#     return False


# @app.delete('/api/tweets/{tweet_id}')
# async def send_tweet(request: Request, db: Session = Depends(get_db)):
#     pass
#
#
# @app.post('/api/medias')
# async def post_image(request: Request, db: Session = Depends(get_db)):
#     pass
#
#
# @app.post('/api/tweets/{tweet_id}/likes')
# async def send_tweet(request: Request, db: Session = Depends(get_db)):
#     pass
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
