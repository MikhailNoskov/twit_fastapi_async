from abc import ABC

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session


class AbstractService:
    """
    Abstract service initiated with async db connection
    """
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
