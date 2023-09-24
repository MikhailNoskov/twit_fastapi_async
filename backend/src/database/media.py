import logging.config

from models.media import Media
from schema.media import MediaResponse
from database.connection import async_session_maker as session

from logging_conf import logs_config

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.db_media")
logger.setLevel("DEBUG")


async def file_db_record(path: str):
    async with session() as db:
        async with db.begin():
            new_media = Media(media_url=path)
            db.add(new_media)
            await db.flush()
            await db.refresh(new_media)
            image = MediaResponse(media_id=new_media.id)
            logger.debug(msg=f'Image {path} added')
            return image
