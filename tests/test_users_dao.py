import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import Response, Request
from app.users.dao import UsersDAO
from app.users.models import User


@pytest.mark.asyncio
async def test_load_users_from_api_success(async_session: AsyncSession):
    mock_api_data = {
        "results": [
            {
                "gender": "female",
                "name": {"first": "Alice", "last": "Smith"},
                "email": "alice@example.com",
                "phone": "111-222-333",
                "location": {"city": "Berlin", "country": "Germany"},
                "picture": {"medium": "http://example.com/photo.jpg"}
            },
            {
                "gender": "male",
                "name": {"first": "Bob", "last": "Johnson"},
                "email": "bob@example.com",
                "phone": "444-555-666",
                "location": {"city": "Paris", "country": "France"},
                "picture": {"medium": "http://example.com/photo2.jpg"}
            }
        ]
    }

    async def mock_get(*args, **kwargs):
        return Response(
            status_code=200,
            request=Request("GET", args[0]),
            json=mock_api_data
        )

    with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
        inserted_count = await UsersDAO.load_users_from_api(db=async_session, count=2)

    # Проверяем, что два пользователя были добавлены
    assert inserted_count == 2

    result = await async_session.execute(
        select(User).where(User.email.in_([
            "alice@example.com", "bob@example.com"
        ]))
    )
    users = result.scalars().all()
    assert len(users) == 2

    alice = next((u for u in users if u.first_name == "Alice"), None)
    assert alice is not None
    assert alice.place == "Berlin, Germany"