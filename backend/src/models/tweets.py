from pydantic import BaseModel
from typing import Optional, List
from db import Base
from sqlalchemy import Column, Integer, String


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)

    def __repr__(self):
        return f"{self.text}"
