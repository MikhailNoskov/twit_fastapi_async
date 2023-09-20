from pydantic import BaseModel


class PositiveResponse(BaseModel):
    result: bool

    class Config:
        orm_mode = True
