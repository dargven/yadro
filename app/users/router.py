from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from app.dependecies.dependecies import get_db
from app.exceptions import UserNotFound
from app.users.dao import UsersDAO

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Users"])


@router.get("/random")
async def get_random_user(db: AsyncSession = Depends(get_db)):
    if not (user := await UsersDAO.get_random_user(db)):
        raise UserNotFound
    return user.to_dict()


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    user = await UsersDAO.find_one_or_none(db, id=user_id)
    if not user:
        raise UserNotFound
    return user.to_dict()


@router.get("/", response_class=HTMLResponse)
async def get_users_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/api/load-users", response_class=JSONResponse)
async def load_users_api(
        count: int = 20,
        db: AsyncSession = Depends(get_db)
):
    loaded_count = await UsersDAO.load_users_from_api(db, count=count)
    return {"status": "success", "loaded": loaded_count}


@router.get("/api/users", response_class=JSONResponse)
async def get_users_paginated(
        page: int = 1,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    users, pagination = await UsersDAO.find_all_paginated(db=db, page=page, limit=limit)
    return {"users": [user.to_dict() for user in users], "pagination": pagination}
