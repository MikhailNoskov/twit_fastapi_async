from pydantic import BaseModel
from typing import Optional, List
from db import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"{self.username}"
