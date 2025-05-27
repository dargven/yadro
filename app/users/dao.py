from typing import Optional, Sequence

import httpx
from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.users.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all_paginated(
            cls,
            db: AsyncSession,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            default_limit: int = 10
    ) -> tuple[Sequence[User], dict[str, int]]:
        page = page or 1
        limit = limit or default_limit

        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = default_limit

        total = await db.scalar(select(func.count()).select_from(User))
        offset = (page - 1) * limit

        result = await db.execute(
            select(User).offset(offset).limit(limit)
        )

        return result.scalars().all(), {
            "page": page,
            "limit": limit,
            "total": total,
        }

    @classmethod
    async def load_users_from_api(
            cls,
            db: AsyncSession,
            count: int = 20
    ) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://randomuser.me/api/?results={count}&inc=gender,name,email,phone,location,picture"
            )
            data = response.json()

        users_data = []
        for user in data["results"]:
            users_data.append({
                "gender": user["gender"],
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
                "email": user["email"],
                "phone": user["phone"],
                "place": f"{user['location']['city']}, {user['location']['country']}",
                "photo": user["picture"]["medium"]
            })

        await db.execute(insert(User).values(users_data))
        await db.commit()
        return len(users_data)

    @classmethod
    async def get_users(
            cls,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            default_limit: int = 10
    ) -> tuple[Sequence[User], dict[str, int | None]]:
        """Получение пользователей с пагинацией"""
        # Устанавливаем значения по умолчанию
        page = page or 1
        limit = limit or default_limit

        # Валидация
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = default_limit

        users = await cls.get_paginated(page=page, limit=limit)
        pagination = {
            "page": page,
            "limit": limit,
            "total": await cls.count()
        }
        return users, pagination
