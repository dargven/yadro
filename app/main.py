from fastapi import FastAPI

from app.database import Base, engine
from app.services.initial_data import InitialDataService
# from app.majors.router import router as router_majors
# from app.pages.router import router as router_pages
# from app.students.router import router as router_students
from app.users.router import router as router_users

app = FastAPI()


# app.mount('/static', StaticFiles(directory='app/static'), 'static')
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await InitialDataService.load_initial_users()


app.include_router(router_users)
# app.include_router(router_students)
# app.include_router(router_majors)
# app.include_router(router_pages)
