from pydantic import BaseModel


class MediaResponse(BaseModel):
    """
    MediaResponse schema
    """
    result: bool = True
    media_id: int

    class Config:
        orm_mode = True
