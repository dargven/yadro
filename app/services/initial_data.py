from sqlalchemy import insert

from app.database import async_session_maker
from app.users.dao import UsersDAO
from app.services.randomuser import RandomUserAPI
from app.users.models import User


class InitialDataService:
    @classmethod
    async def load_initial_users(cls, count: int = 1000) -> bool:
        async with async_session_maker() as session:
            try:
                existing_count = await UsersDAO.count(session)
                if existing_count >= count:
                    return False

                needed = count - existing_count
                users_data = await RandomUserAPI.fetch_users(needed)

                await session.execute(
                    insert(User).values([user.model_dump() for user in users_data])
                )
                await session.commit()

                return True
            except Exception:
                await session.rollback()
                raise