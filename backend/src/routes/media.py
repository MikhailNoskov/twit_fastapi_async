import shutil
import string
import random

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.requests import Request

from schema.media import MediaResponse
from database.media import file_db_record
from celery_app import resize_image

media_router = APIRouter(
    tags=["media"]
)


@media_router.post('/', response_model=MediaResponse)
async def post_new_media_file(request: Request, file: UploadFile = File(...)):
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_str}.'
    filename = new.join(file.filename.rsplit('.', 1))
    path = f'images/{filename}'
    file_bytes = await file.read()
    resize_image.delay(path, file_bytes)
    return await file_db_record(path)
