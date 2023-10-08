from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/signin")


def authenticate(
        token: str = Depends(oauth2_scheme)) -> Optional[str]:
    """
    Token verification function
    :param token: Provided oauth2 token
    :return: User returned by token
    """
    if not token:
        # raise HTTPException(
        #     status_code=status.HTTP_403_FORBIDDEN,
        #     detail="Sign in for access!"
        # )
        return None
    decoded_token = verify_access_token(token)
    return decoded_token["user"]
