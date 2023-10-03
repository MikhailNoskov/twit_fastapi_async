import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup(test_app):
    """
    New User sign up test function
    :param test_app: App instance
    :return: None
    """
    app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "mike@klike.com", "password": "strong!!!", "api_key": "test"}
    response = await client.post("/api/users/signup", json=data)
    assert response.json() == {'message': 'User successfully registered!'}


@pytest.mark.asyncio
async def test_get_me(test_app):
    """
    Get current authenticated User test function
    :param test_app: App instance
    :return: None
    """
    app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True,
                "user": {"id": 1, "name": "mike@klike.com", "followers": [], "following": [
                    {
                        "id": 2,
                        "name": "jorge@klike.com"
                    }
                ]
                         }
                }
    headers = {"api-key": "test"}
    response = await client.get("/api/users/me", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_get_user_by_id(test_app):
    """
    Get user by ID test function
    :param test_app: App instance
    :return: None
    """
    app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True,
                "user": {"id": 1, "name": "mike@klike.com", "followers": [], "following": [
                    {
                        "id": 2,
                        "name": "jorge@klike.com"
                    }
                ]
                         }
                }
    headers = {"api-key": "test"}
    response = await client.get("/api/users/1", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_follow_user(test_app):
    """
    Follow User test function
    :param test_app: App instance
    :return: None
    """
    app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.post("/api/users/2/follow", headers=headers)
    assert response.json() == expected


@pytest.mark.asyncio
async def test_unfollow_user(test_app):
    """
    Unfollow User test function
    :param test_app: App instance
    :return: None
    """
    app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.delete("/api/users/2/follow", headers=headers)
    assert response.json() == expected
