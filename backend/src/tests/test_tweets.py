# import pytest
#
# from httpx import AsyncClient
#
#
# @pytest.mark.asyncio
# async def test_get_tweets(test_app):
#     """
#     Get all tweets test function
#     :param test_app: App instance
#     :return: None
#     """
#     app = await test_app
#     client = AsyncClient(app=app, base_url="http://test")
#     expected = {
#         "result": True,
#         "tweets": [
#             {
#                 "id": 0,
#                 "content": "string",
#                 "author": {"id": 0, "name": "string"},
#                 "likes": [{"id": 0, "name": "string"}],
#                 "attachments": [],
#             }
#         ],
#     }
#     headers = {"api-key": "test"}
#     response = await client.get("/api/tweets", headers=headers)
#     assert response.json() == expected
#
#
# @pytest.mark.asyncio
# async def test_post_tweet(test_app):
#     """
#     Post new tweet test function
#     :param test_app: App instance
#     :return: None
#     """
#     app = await test_app
#     client = AsyncClient(app=app, base_url="http://test")
#     expected = {"tweet_data": "string", "tweet_media_ids": [0]}
#     headers = {"api-key": "test"}
#     response = await client.get("/api/tweets", headers=headers)
#     assert response.json() == expected
#
#
# @pytest.mark.asyncio
# async def test_delete_tweet(test_app):
#     """
#     Tweet delete test function
#     :param test_app: App instance
#     :return: None
#     """
#     app = await test_app
#     client = AsyncClient(app=app, base_url="http://test")
#     expected = {"result": True}
#     headers = {"api-key": "test"}
#     response = await client.get("/api/tweets/1", headers=headers)
#     assert response.json() == expected
#
#
# @pytest.mark.asyncio
# async def test_like_tweet(test_app):
#     """
#     Tweet like create test function
#     :param test_app: App instance
#     :return: None
#     """
#     app = await test_app
#     client = AsyncClient(app=app, base_url="http://test")
#     expected = {"result": True}
#     headers = {"api-key": "test"}
#     response = await client.post("/api/tweets/2/likes", headers=headers)
#     assert response.json() == expected
#
#
# @pytest.mark.asyncio
# async def test_delete_like(test_app):
#     """
#     Tweet like delete test function
#     :param test_app: App instance
#     :return: None
#     """
#     app = await test_app
#     client = AsyncClient(app=app, base_url="http://test")
#     expected = {"result": True}
#     headers = {"api-key": "test"}
#     response = await client.delete("/api/tweets/2/likes", headers=headers)
#     assert response.json() == expected
