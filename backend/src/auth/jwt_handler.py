import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from database.connection import Settings

settings = Settings()


def create_access_token(user: str) -> str:
    """
    Create access token function
    :param user: User in the form of string
    :return: Access token as a string
    """
    payload = {
        "user": user,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    """
    Access token verification function
    :param token: Access token as a string
    :return: Dict data including User as a string and expires attr as a timestamp
    """
    try:
        data = jwt.decode(token, settings.SECRET_KEY)
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied!"
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token!"
        )
