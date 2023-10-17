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
    expected = {
        "result": True,
        "tweets": [
            {
                "id": 1,
                "content": "Text for the first tweet",
                "author": {"id": 1, "name": "mike@klike.com"},
                "likes": [],
                "attachments": [],
            },
            {
                "id": 2,
                "content": "Text for the second tweet",
                "author": {"id": 2, "name": "jorge@klike.com"},
                "likes": [],
                "attachments": [],
            }
        ],
    }
    headers = {"api-key": "test"}
    response = await client.get("/api/tweets/", headers=headers)
    assert response.json() == expected
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_tweets_not_authenticated(create_data):
    """
    Get all tweets test function by not authenticated_user
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {
        "result": False,
        "error_message": "Access denied",
        "error_type": "tweets"
    }
    headers = {"api-key": "west"}
    response = await client.get("/api/tweets/", headers=headers)
    assert response.json() == expected
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_post_tweet(create_data):
    """
    Post new tweet test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True, "tweet_id": 3}
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


@pytest.mark.asyncio
async def test_delete_tweet_tweet_by_other_user(create_data):
    """
    Other user Tweet delete test function
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {
        "result": False,
        'error_message': 'Tweet can not be deleted by this user',
        'error_type': 'tweets'
    }
    headers = {"api-key": "test"}
    response = await client.delete("/api/tweets/2", headers=headers)
    assert response.json() == expected
    assert response.status_code == 403
