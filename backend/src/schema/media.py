from pydantic import BaseModel, EmailStr
from typing import Optional, List


class MediaResponse(BaseModel):
    result: bool = True
    media_id: int

    class Config:
        orm_mode = True
