from pydantic import BaseModel
from typing import Optional, List
from database.connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    api_key = Column(String(50), nullable=True)
    tweets = relationship('DbUser', back_populates='author')

    def __repr__(self):
        return f"{self.name}"
