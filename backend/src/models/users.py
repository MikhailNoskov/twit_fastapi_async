from pydantic import BaseModel
from typing import Optional, List
from database.connection import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Index
from sqlalchemy.orm import relationship


users_connections = Table('users_connections', Base.metadata,
                          Column('follower_id', Integer, ForeignKey('users.id')),
                          Column('followed_id', Integer, ForeignKey('users.id')),
                          Index('unique_follow', 'follower_id', 'followed_id', unique=True))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    api_key = Column(String(50), nullable=True)
    tweets = relationship('DbUser', back_populates='author')

    followers = relationship('User',
                             secondary=users_connections,
                             primaryjoin=id == users_connections.c.follower_id,
                             secondaryjoin=id == users_connections.c.followed_id,
                             backref='following')

    following = relationship('User',
                             secondary=users_connections,
                             primaryjoin=id == users_connections.c.followed_id,
                             secondaryjoin=id == users_connections.c.follower_id,
                             backref='followers')

    def __repr__(self):
        return f"{self.name}"
