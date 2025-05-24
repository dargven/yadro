import httpx

from app.users.schemas import SUserCreate


class RandomUserAPI:
    BASE_URL = "https://randomuser.me/api/"

    @classmethod
    async def fetch_users(cls, count: int) -> list[SUserCreate]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{cls.BASE_URL}?results={count}&inc=gender,name,email,phone,location,picture"
            )
            response.raise_for_status()

            return [
                cls._parse_user(user_data)
                for user_data in response.json()["results"]

            ]

    @staticmethod
    def _parse_user(user_data: dict) -> SUserCreate:
        return SUserCreate(
            gender=user_data["gender"],
            first_name=user_data["name"]["first"],
            last_name=user_data["name"]["last"],
            email=user_data["email"],
            phone=user_data["phone"],
            place=f"{user_data["location"]['city']}",
            photo=user_data["picture"]["thumbnail"]
        )
