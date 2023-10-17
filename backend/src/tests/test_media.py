from io import BytesIO
from PIL import Image
import pytest

from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_post_media(create_data):
    """
    Post new tweet test function
    :param test_app: App instance
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
