from fastapi import APIRouter, HTTPException, status
from models.users import User
from schema.users import UserRegister
from database.connection import get_session
from sqlalchemy import select

user_router = APIRouter(
    tags=["users"]
)


@user_router.post("/signup")
async def sign_new_user(data: UserRegister) -> dict:
    print(data)
    async with get_session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.password == data.password))
            user = user.scalar_one_or_none()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with supplied username exists"
                )
            user = User(username=data.username, password=data.password)
            session.add(user)
            await session.flush()
            return {
                "message": "User successfully registered!"
            }

@user_router.get("/{id}")
async def retrieve_event(id: int):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.id == id))
            user = user.scalar_one_or_none()
            if user:
                return {'yes': 'yes'}
            raise HTTPException(
                status_code=status. HTTP_404_NOT_FOUND,
                detail="Event with supplied ID does not exist"
            )

# @user_router.post("/signin")
# async def sign_user_in(user: UserSignIn) -> dict:
#     if user.username not in users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist")
#     if users[user.username].password != user.password:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Wrong credentials passed"
#         )
#     return {
#         "message": "User signed in successfully"
#     }
#
# @user_router.post("/signup")
# async def sign_new_user(data: User) -> dict:
#     if data.email in users:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with supplied username exists"
#         )
#     users[data.email] = data
#     return {
#         "message": "User successfully registered!"
#     }
#
#
# @user_router.post("/signin")
# async def sign_user_in(user: UserSignIn) -> dict:
#     if user.email not in users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist")
#     if users[user.email].password != user.password:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Wrong credentials passed"
#         )
#     return {
#         "message": "User signed in successfully"
#     }
#
#
# # @app.get('/api/users/me')
# # async def me(request: Request, db: Session = Depends(get_db)):
# #     pass
# #
# #
# # @app.get('/api/users/{user_id}')
# # async def user(request: Request, db: Session = Depends(get_db)):
# #     pass