from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=False)
    message = relationship("Message", back_populates="message")
    reaction = relationship("Reaction", back_populates="reaction")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    text = Column(String)
    created_at = Column(...)
    user = relationship("User", back_populates="user")
    message = relationship("MessageImage", back_populates="messageimage")


class MessageImage(Base):
    __tablename__ = "messageimages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('Message.id'))
    img = (...)
    message = relationship("Message", back_populates="message")


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    message_id = Column(Integer, ForeignKey('Message.id'))
    text = Column(String)
    created_at = Column(...)
    user = relationship("User", back_populates="user")
    message = relationship("Message", back_populates="message")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    following_id = Column(Integer, ForeignKey('User.id'))
    created_at = Column(...)
    is_active = Column(Boolean, default=False)
    user = relationship("User", back_populates="user")
    following = relationship("User", back_populates="following")
