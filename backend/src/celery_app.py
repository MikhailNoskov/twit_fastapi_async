import asyncio

from celery import Celery
from PIL import Image
import io
import logging.config
from logging_conf import logs_config

from database.media import update_media_path

celery_app = Celery(__name__)
celery_app.conf.broker_url = 'redis://localhost:6379'
celery_app.conf.result_backend = 'redis://localhost:6379'


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.celery")
logger.setLevel("DEBUG")


@celery_app.task
def resize_image(path, file_bytes, size_mb=2) -> None:
    """
    Image file resize async task
    :param path: str
    :param file_bytes: bytes
    :param size_mb: File size threshold
    :return: None
    """
    if len(file_bytes) > 2 * 1024 * 1024:  # 2Mb
        logger.warning(msg='Big file')
        input_stream = io.BytesIO(file_bytes)
        image = Image.open(input_stream)

        # Calculate resize ratio
        ratio = 2 * 1024 * 1024 / len(file_bytes)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)

        image = image.resize((new_width, new_height))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            logger.debug(msg='Schema is not RGB')
            image = image.convert('RGB')
        # Convert to lower quality JPEG
        output_stream = io.BytesIO()
        image.save(output_stream, 'JPEG', quality=70)
        resized_bytes = output_stream.getvalue()

    else:
        resized_bytes = file_bytes
    with open(path, "wb") as f:
        f.write(resized_bytes)
    logger.info(msg='File saved')


@celery_app.task
def reattach_new_path(image_id: int, path: str) -> None:
    async def wrapped():
        await update_media_path(media_id=image_id, new_path=path)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wrapped())
