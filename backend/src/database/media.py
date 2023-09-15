from models.media import Media
from schema.media import MediaResponse
from database.connection import async_session_maker as session


async def file_db_record(path: str):
    async with session() as db:
        async with db.begin():
            new_media = Media(media_url=path)
            db.add(new_media)
            await db.flush()
            await db.refresh(new_media)
            image = MediaResponse(media_id=new_media.id)
            return image
