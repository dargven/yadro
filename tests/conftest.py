import pytest
from app.database import async_session_maker


@pytest.fixture
async def async_session():
    async with async_session_maker() as session:
        yield session