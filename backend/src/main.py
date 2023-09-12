from fastapi import FastAPI
from routes.users import user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router, prefix="/user")


# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session() as session:
#         async with session.begin():
#             session.add_all(
#                 [
#                     User(username='Mike', password='mike_pass'),
#                     User(username='Alla', password='alla_pass'),
#                     Tweet(text='Hey', comment='Haya')
#                 ]
#             )



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=7202, reload=True)