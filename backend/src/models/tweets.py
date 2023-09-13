from pydantic import BaseModel
from typing import Optional, List
from database.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from .users import tweet_connections


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='tweets')

    # liked = relationship('User',
    #                      secondary=tweet_connections,
    #                      primaryjoin=id == tweet_connections.c.tweet_id,
    #                      secondaryjoin=id == tweet_connections.c.liker_id,
    #                      backref='liked_by',
    #                      lazy='select')
    likes = relationship("Like", back_populates="tweet")


    def __repr__(self):
        return f"Tweet Nr{self.id}"


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    tweet_id = Column(ForeignKey("tweets.id"))
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")