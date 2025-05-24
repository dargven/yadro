from sqlalchemy import func
from sqlalchemy.future import select

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            # print(query)
            result = await session.execute(query)

            result = result.scalar_one_or_none()
            # print(result)
            return result

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def count(cls) -> int:
        async with async_session_maker() as session:
            result = await session.execute(select(func.count(cls.model.id)))
            return result.scalar()

    @classmethod
    async def create(cls, data: dict) -> model:
        async with async_session_maker() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @classmethod
    async def bulk_create(cls, data_list: list[dict]) -> list[model]:
        async with async_session_maker() as session:
            instances = [cls.model(**data) for data in data_list]
            session.add_all(instances)
            await session.commit()

            # Обновляем instances чтобы получить их ID
            for instance in instances:
                await session.refresh(instance)

            return instances
