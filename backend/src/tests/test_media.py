from io import BytesIO
from PIL import Image
import pytest

from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_post_media(create_data):
    """
    Post new media test function
    :param create_data: db drop and create fixture function
    :return: None
    """
    await create_data
    fake_img = Image.new("RGB", size=(100, 100))
    img_bytes = BytesIO()
    fake_img.save(img_bytes, format="JPEG")
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True, "media_id": 1}
    file = {"file": ("test_file.jpg", img_bytes.getvalue())}
    headers = {"api-key": "test"}
    response = await client.post("/api/medias/", files=file, headers=headers)
    assert response.json() == expected
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_media_not_authenticated(create_data):
    """
    Post new media by not authenticated user test function
    :param create_data: db drop and create fixture function
    :return: None
    """
    fake_img = Image.new("RGB", size=(100, 100))
    img_bytes = BytesIO()
    fake_img.save(img_bytes, format="JPEG")
    client = AsyncClient(app=app, base_url="http://test")
    expected = {'error_message': 'Access denied', 'error_type': 'medias', 'result': False}
    file = {"file": ("test_file.jpg", img_bytes.getvalue())}
    headers = {"api-key": "west"}
    response = await client.post("/api/medias/", files=file, headers=headers)
    assert response.json() == expected
    assert response.status_code == 403
