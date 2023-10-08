from pydantic import BaseModel


class PositiveResponse(BaseModel):
    """
    Positive response schema
    """
    result: bool

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
