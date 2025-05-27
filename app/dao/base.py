import random
from typing import Optional

from sqlalchemy import func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import async_session_maker
from app.users.models import User


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(
            cls,
            db: AsyncSession,
            **filters
    ) -> Optional[User]:
        result = await db.execute(
            select(User).filter_by(**filters)
        )
        return result.scalar_one_or_none()
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)

            result = result.scalar_one_or_none()
            return result

    @classmethod
    async def find_all(cls, **filter_by):

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        if not cls.model:
            raise NotImplementedError("Model not specified")
        result = await db.execute(select(func.count(cls.model.id)))
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
    async def bulk_create(
            cls,
            db: AsyncSession,
            users_data: list[dict]
    ) -> None:
        stmt = insert(cls.model).values(users_data)
        await db.execute(stmt)
        await db.commit()

    @classmethod
    async def get_random_user(cls) -> Optional[User]:
        async with async_session_maker() as session:
            count = await session.scalar(select(func.count()).select_from(cls.model))

            if not count:
                return None

            random_offset = random.randint(0, count - 1)
            return await session.scalar(
                select(cls.model).offset(random_offset).limit(1))
