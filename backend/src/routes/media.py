import shutil
import string
import random
import logging.config

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.requests import Request

from schema.media import MediaResponse
from database.media import file_db_record
from celery_app import resize_image
from logging_conf import logs_config


media_router = APIRouter(tags=["media"])

logging.config.dictConfig(logs_config)
logger = logging.getLogger("app.media_routes")
logger.setLevel("DEBUG")


@media_router.post('/', response_model=MediaResponse)
async def post_new_media_file(request: Request, file: UploadFile = File(...)):
    user = request.state.user
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
    resize_image.delay(path, file_bytes)
    return await file_db_record(path)
