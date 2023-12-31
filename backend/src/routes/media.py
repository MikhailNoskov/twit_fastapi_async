import string
import random
import logging.config
from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, Depends, Header
from fastapi.requests import Request

from schema.media import MediaResponse
from database.media import MediaService
from celery_app import resize_image, reattach_new_path
from logging_conf import logs_config
from exceptions.custom_exceptions import CustomException
from .response_info import MEDIA_ERROR_RESPONSES


media_router = APIRouter(tags=["media"])

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.media_routes")
logger.setLevel("DEBUG")


@media_router.post(
    "/",
    response_model=MediaResponse,
    status_code=201,
    responses={
        "403": MEDIA_ERROR_RESPONSES[403]
    }

)
async def post_new_media_file(
    request: Request,
    service: MediaService = Depends(),
    file: UploadFile = File(...),
    api_key: Optional[str] = Header(None),
):
    """
    Image file save endpoint
    ------------------------
    :param api_key: str\n
    :param request: Request\n
    :param service: Media db connect service instance\n
    :param file: Uploaded file\n
    :return: Image file info db create method of Media service\n
    """
    user = request.state.user
    default_path = "images/default_kSGOVr.jpg"
    if not user:
        error_message = "Access denied"
        logger.warning(msg=error_message)
        raise CustomException(
            error_type="medias",
            error_message=error_message,
            response_status=status.HTTP_403_FORBIDDEN,
        )
    filename = file.filename
    logger.debug(msg=f"User {user} tries to load file {filename}")
    letters = string.ascii_letters
    random_str = "".join(random.choice(letters) for i in range(6))
    new = f"_{random_str}."
    filename = new.join(filename.rsplit(".", 1))
    file_bytes = await file.read()
    image = await service.file_db_record(path=default_path)
    resize_image.delay(filename, file_bytes)
    reattach_new_path.delay(image.media_id, filename)
    return image
