import string
import random
import logging.config

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from fastapi.requests import Request

from schema.media import MediaResponse
from database.media import MediaService
from celery_app import resize_image, reattach_new_path
from logging_conf import logs_config


media_router = APIRouter(tags=["media"])

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.media_routes")
logger.setLevel("DEBUG")


@media_router.post('/', response_model=MediaResponse)
async def post_new_media_file(request: Request, service: MediaService = Depends(), file: UploadFile = File(...)):
    """
    Image file save endpoint
    :param request: Request
    :param service: Media db connect service instance
    :param file: Uploaded file
    :return: Image file info db create method of Media service
    """
    user = request.state.user
    default_path = 'images/default_kSGOVr.jpg'
    if not user:
        logger.error('Access denied')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    logger.debug(msg=f'User {user} tries to load file {file.filename}')
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_str}.'
    filename = new.join(file.filename.rsplit('.', 1))
    path = f'images/{filename}'
    file_bytes = await file.read()
    image = await service.file_db_record(path=default_path)
    resize_image.delay(filename, path, file_bytes)
    new_path = 'https://amigomalay.s3.eu-north-1.amazonaws.com/' + filename
    reattach_new_path.delay(image.media_id, new_path)
    return image
