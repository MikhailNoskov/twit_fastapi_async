from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserRegister(BaseModel):
    username: str
    password: str

    class Config :
        schema_extra = {
            "example": {
                "username": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


# class NewUser(User):
#     pass
#
#
# class UserSignIn(BaseModel):
#     email: EmailStr
#     password: str
#
#     class Config :
#         schema_extra = {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!",
#                 "events": [],
#             }
#         }
