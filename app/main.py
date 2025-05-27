from fastapi import FastAPI, Request
from fastapi.openapi.models import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.services.initial_data import InitialDataService
from app.users.router import router as router_users

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await InitialDataService.load_initial_users()

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")

    @app.get("/")
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/favicon.ico")
    def favicon():
        return Response(status_code=204)


app.include_router(router_users)
