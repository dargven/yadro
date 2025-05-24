from fastapi import APIRouter

from app.exceptions import UserNotFound
from app.users.dao import UsersDAO
from app.users.schemas import SUserResponse
from app.users.models import User

router = APIRouter(tags=["Users"])


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not (user := await UsersDAO.find_one_or_none_by_id(user_id)):
        raise UserNotFound
    return user
