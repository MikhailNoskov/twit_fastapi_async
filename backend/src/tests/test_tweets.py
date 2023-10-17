import pytest

from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_get_tweets(create_data):
    """
    Get all tweets test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    # expected = {
    #     "result": True,
    #     "tweets": [
    #         {
    #             "id": 0,
    #             "content": "string",
    #             "author": {"id": 0, "name": "string"},
    #             "likes": [{"id": 0, "name": "string"}],
    #             "attachments": [],
    #         }
    #     ],
    # }
    expected = {
        "result": True,
        "tweets": []
    }
    headers = {"api-key": "test"}
    response = await client.get("/api/tweets/", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_post_tweet(create_data):
    """
    Post new tweet test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True, "tweet_id": 1}
    data = {"tweet_data": "Un amigo malay"}
    headers = {"api-key": "test"}
    response = await client.post("/api/tweets/", json=data, headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_like_tweet(create_data):
    """
    Tweet like create test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.post("/api/tweets/1/likes", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_delete_like(create_data):
    """
    Tweet like delete test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.delete("/api/tweets/1/likes", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_delete_tweet(create_data):
    """
    Tweet delete test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.delete("/api/tweets/1", headers=headers)
    assert response.json() == expected
