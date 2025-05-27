import pytest
import respx
import httpx
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
@respx.mock
async def test_load_users():
    mock_users = {
        "results": [{
            "gender": "male",
            "name": {"first": "John", "last": "Doe"},
            "email": "john@example.com",
            "phone": "1234567890",
            "location": {"city": "New York", "country": "USA"},
            "picture": {"medium": "http://example.com/photo.jpg"}
        }] * 5
    }

    respx.get("https://randomuser.me/api/").mock(
        return_value=httpx.Response(200, json=mock_users)
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/load-users?count=5")

    assert response.status_code == 200
    data = response.json()
    assert data["loaded"] == 5


# Тест получения пользователей с пагинацией
@pytest.mark.asyncio
async def test_get_users_paginated():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/users?page=1&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["users"], list)
    assert "pagination" in data
    assert "page" in data["pagination"]
    assert "limit" in data["pagination"]
    assert "total" in data["pagination"]


@pytest.mark.asyncio
async def test_get_user_by_id():
    """Тест получения пользователя по ID"""
    # Сначала получим список, чтобы взять существующий ID
    async with AsyncClient(app=app, base_url="http://test") as client:
        list_response = await client.get("/api/users")
        users = list_response.json()["users"]
        assert users, "Users list is empty, cannot test retrieval by ID"
        user_id = users[0]["id"]

        response = await client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == user_id
