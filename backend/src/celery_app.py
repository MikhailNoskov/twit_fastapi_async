import asyncio
import os

from celery import Celery
from PIL import Image
import io
import logging.config
from logging_conf import logs_config

from database.media import update_media_path
from aws.aws_connection import s3
from settings import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(__name__)
celery_app.conf.broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
celery_app.conf.result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}"


logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.celery")
logger.setLevel("DEBUG")


@celery_app.task
def resize_image(name, path, file_bytes, size_mb=2) -> None:
    """
    Image file resize async task
    :param name: str
    :param path: str
    :param file_bytes: bytes
    :param size_mb: File size threshold
    :return: None
    """
    if len(file_bytes) > 2 * 1024 * 1024:  # 2Mb
        logger.warning(msg="Big file")
        input_stream = io.BytesIO(file_bytes)
        image = Image.open(input_stream)

        # Calculate resize ratio
        ratio = 2 * 1024 * 1024 / len(file_bytes)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)

        image = image.resize((new_width, new_height))

        # Convert to RGB if needed
        if image.mode != "RGB":
            logger.debug(msg="Schema is not RGB")
            image = image.convert("RGB")
        # Convert to lower quality JPEG
        output_stream = io.BytesIO()
        image.save(output_stream, "JPEG", quality=70)
        resized_bytes = output_stream.getvalue()
    else:
        resized_bytes = file_bytes
    with open(path, "wb") as f:
        f.write(resized_bytes)
    s3.upload_file(path, "amigomalay", name)
    logger.info(msg="File saved")
    os.remove(path)
    logger.info(msg="Temporary file removed")


@celery_app.task
def reattach_new_path(image_id: int, path: str) -> None:
    async def wrapped():
        await update_media_path(media_id=image_id, new_path=path)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wrapped())
