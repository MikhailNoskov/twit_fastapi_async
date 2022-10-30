from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(forein_key=User)
    text = Column(String)
    created_at = Column(...)


class MessageImage(Base):
    __tablename__ = "messageimages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(forein_key=User)
    img = (...)


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(forein_key=User)
    message = Column(foreign_key=Message)
    text = Column(String)
    created_at = Column(...)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(forein_key=User)
    folooewd = Column(forein_key=User)
    created_at = Column(...)
    is_active = Column(Boolean, default=False)
