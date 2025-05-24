from fastapi import APIRouter

from app.exceptions import UserNotFound
from app.users.dao import UsersDAO

router = APIRouter(tags=["Users"])


@router.get("/random")
async def get_random_user():
    if not (user := await UsersDAO.get_random_user()):
        raise UserNotFound
    return user


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not (user := await UsersDAO.find_one_or_none_by_id(user_id)):
        raise UserNotFound
    return user
