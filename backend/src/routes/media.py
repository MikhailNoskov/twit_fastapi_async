import shutil
import string
import random
from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Header, Depends, UploadFile, File
from models.media import Media
from models.users import User
from schema.media import MediaResponse
from database.connection import get_session
from database.media import file_db_record
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, subqueryload, aliased
from fastapi.responses import JSONResponse


media_router = APIRouter(
    tags=["media"]
)


async def verify_api_key(api_key: Optional[str] = Header(), db: AsyncSession = Depends(get_session)):
    async with db.begin():
        user = await db.execute(select(User).where(User.api_key == api_key))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return True


@media_router.post('/', dependencies=[Depends(verify_api_key)], response_model=MediaResponse)
async def post_new_media_file(image: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return await file_db_record(path)
