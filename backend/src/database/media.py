import logging.config

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.media import Media
from schema.media import MediaResponse
from database.connection import get_session
from logging_conf import logs_config

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_media")
logger.setLevel("DEBUG")


class MediaService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def file_db_record(self, path: str):
        # async with session() as db:
        async with self.session.begin():
            new_media = Media(media_url=path)
            self.session.add(new_media)
            await self.session.flush()
            await self.session.refresh(new_media)
            image = MediaResponse(media_id=new_media.id)
            logger.debug(msg=f'Image {path} added')
            return image
