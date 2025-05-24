from app.database import async_session_maker
from app.services.randomuser import RandomUserAPI
from app.users.dao import UsersDAO


# from app.logger import logger


class InitialDataService:
    @classmethod
    async def load_initial_users(cls, count: int = 1000) -> bool:
        """Загружает начальных пользователей в БД"""
        async with async_session_maker() as session:
            try:
                existing_count = await UsersDAO.count()
                if existing_count >= count:
                    return False

                needed = count - existing_count

                users_data = await RandomUserAPI.fetch_users(needed)
                await UsersDAO.bulk_create(
                    [user.model_dump() for user in users_data]
                )

                return True

            except Exception as e:
                raise
