import pytest
from urllib.parse import urlencode

from fastapi.security import OAuth2PasswordRequestForm

from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_signup_correctly(create_data):
    """
    New User sign up test function with correct data
    :param test_app: App instance
    :return: None
    """
    await create_data
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "june@klike.com", "password": "strong!!!", "api_key": "cest"}
    response = await client.post("/api/users/signup", json=data)
    expected = {'message': 'User successfully registered!'}
    assert response.json() == expected
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_signup_email_exists(create_data):
    """
    New User sign up test function with existing email
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "june@klike.com", "password": "strongest", "api_key": "fest"}
    response = await client.post("/api/users/signup", json=data)
    expected = {'result': False, 'error_type': 'users', 'error_message': 'User with supplied username exists'}
    assert response.json() == expected
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_signup_api_key_exists(create_data):
    """
    New User sign up test function with existing api_key
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "junex@klike.com", "password": "strongest", "api_key": "test"}
    response = await client.post("/api/users/signup", json=data)
    expected = {'result': False, 'error_type': 'users', 'error_message': 'User with supplied api_key exists'}
    assert response.json() == expected
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_correctly(create_data):
    """
    User login test function with correct data
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "mike@klike.com", "password": "pass_1"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    response = await client.post("/api/users/signin", data=data, headers=headers)
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_correctly_wrong_email(create_data):
    """
    User login test function with wrong email
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "mikes@klikes.com", "password": "pass_1"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    response = await client.post("/api/users/signin", data=data, headers=headers)
    expected = {"detail": "User does not exist"}
    assert response.json() == expected
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_correctly_wrong_email(create_data):
    """
    User login test function with wrong email
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    data = {"username": "mike@klike.com", "password": "pass_15"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    response = await client.post("/api/users/signin", data=data, headers=headers)
    expected = {"detail": "Wrong credentials passed"}
    assert response.json() == expected
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_me(create_data):
    """
    Get current authenticated User test function with correct data
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {
        "result": True,
        "user": {
            "id": 1,
            "name": "mike@klike.com",
            "followers": [],
            "following": [],
        },
    }
    headers = {"api-key": "test"}
    response = await client.get("/api/users/me", headers=headers)
    assert response.json() == expected
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_me_does_not_exist(create_data):
    """
    Get current authenticated User test function which does not exist
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {'result': False, 'error_type': 'users', 'error_message': 'User not found'}
    headers = {"api-key": "gest"}
    response = await client.get("/api/users/me", headers=headers)
    assert response.json() == expected
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_id(create_data):
    """
    Get user by ID test function with correct data
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True, "user": {"id": 2, "name": "jorge@klike.com", "followers": [], "following": []}}
    headers = {"api-key": "test"}
    response = await client.get("/api/users/2", headers=headers)
    assert response.json() == expected
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id_does_not_exist(create_data):
    """
    Get user by ID test function with correct data
    :param test_app: App instance
    :return: None
    """
    client = AsyncClient(app=app, base_url="http://test")
    expected = {'result': False, 'error_type': 'users', 'error_message': 'User not found'}
    headers = {"api-key": "test"}
    response = await client.get("/api/users/15", headers=headers)
    assert response.json() == expected
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_follow_user(drop_base):
    """
    Follow User test function
    :param test_app: App instance
    :return: None
    """
    # app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.post("/api/users/2/follow", headers=headers)
    assert response.json() == expected
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unfollow_user(create_data):
    """
    Unfollow User test function
    :param test_app: App instance
    :return: None
    """
    # app = await test_app
    client = AsyncClient(app=app, base_url="http://test")
    expected = {"result": True}
    headers = {"api-key": "test"}
    response = await client.delete("/api/users/2/follow", headers=headers)
    assert response.json() == expected
    assert response.status_code == 200
