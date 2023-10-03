from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.connection import Base


class Tweet(Base):
    """
    Tweet model
    """
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='tweets')
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Tweet Nr{self.id}"


Tweet.attachments = relationship("Media", back_populates="tweet")


class Like(Base):
    """
    Like model
    """
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    tweet_id = Column(ForeignKey("tweets.id"))
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")
