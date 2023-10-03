from pydantic import BaseModel


class PositiveResponse(BaseModel):
    """
    Positive response schema
    """
    result: bool

    class Config:
        orm_mode = True
