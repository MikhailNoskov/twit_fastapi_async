import logging.config

from fastapi import status
from sqlalchemy import select

from models.media import Media
from schema.media import MediaResponse
from logging_conf import logs_config
from database.connection import async_session_maker
from database.services import AbstractService
from exceptions.custom_exceptions import CustomException


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
            try:
                new_media = Media(media_url=path)
                self.session.add(new_media)
                await self.session.flush()
                await self.session.refresh(new_media)
                image = MediaResponse(media_id=new_media.id)
                logger.debug(msg=f"Image {path} added")
                return image
            except Exception as err:
                logger.warning(msg=f'Error occurred while saving media record {err}')


async def update_media_path(media_id: int, new_path: str) -> None:
    """

    :param media_id:
    :param new_path:
    :return:
    """
    async with async_session_maker() as db:
        async with db.begin():
            try:
                media = await db.execute(select(Media).where(Media.id == media_id))
                media = media.scalars().first()
                if not media:
                    error_message = "Media not found"
                    logger.warning(msg=error_message)
                    raise CustomException(
                        error_type="media",
                        error_message=error_message,
                        response_status=status.HTTP_404_NOT_FOUND,
                    )
                media.media_url = new_path
                await db.merge(media)
                await db.commit()
                logger.info(msg="New path is saved")
            except Exception as err:
                logger.warning(msg=f'Error occurred while reattaching media to tweet {err}')
