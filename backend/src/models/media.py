from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base
from models.tweets import Tweet


class Media(Base):
    """
    Image file db info model
    """

    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    media_url = Column(String(500), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    tweet = relationship(Tweet, back_populates="attachments", lazy="select")

    def __repr__(self):
        return f"File Nr{self.id}"
