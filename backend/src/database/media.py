import logging.config

from fastapi import HTTPException
from models.media import Media
from schema.media import MediaResponse
from logging_conf import logs_config
from database.connection import async_session_maker
from database.services import AbstractService
from sqlalchemy import select

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_media")
logger.setLevel("DEBUG")



class MediaService(AbstractService):
    """
    Service for db connection for Media cors
    """
    async def file_db_record(self, path: str) -> MediaResponse:
        """
        Media instance (image db info) create method
        :param path: Path to the image file
        :return: MediaResponse with info about image file
        """
        async with self.session.begin():
            new_media = Media(media_url=path)
            self.session.add(new_media)
            await self.session.flush()
            await self.session.refresh(new_media)
            image = MediaResponse(media_id=new_media.id)
            logger.debug(msg=f'Image {path} added')
            return image

async def update_media_path(media_id: int, new_path: str) -> None:
    """

    :param media_id:
    :param new_path:
    :return:
    """
    async with async_session_maker() as db:
        async with db.begin():
            media = await db.execute(select(Media).where(Media.id == media_id))
            media = media.scalars().first()
            if not media:
                raise HTTPException(status_code=404, detail="Media not found")
            media.media_url = new_path
            await db.merge(media)
            await db.commit()
            logger.info(msg='New path is saved')
