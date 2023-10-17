from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .jwt_handler import verify_access_token
from database.get_user import get_user_by_name

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    """
    Token verification function
    :param token: Provided oauth2 token
    :return: User returned by token
    """
    if not token:
        return None
    decoded_token = verify_access_token(token)
    return await get_user_by_name(decoded_token["user"])
