import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from formula_1.db import create_admin_user
from formula_1.features import (
    companies,
    organizations,
    users,
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before the app starts
    create_admin_user(logger)
    yield
    # after the app ends


app = FastAPI(
    title="Fórmula 1",
    lifespan=lifespan,
)

logger = logging.getLogger(__name__)

app.mount(
    "/static", StaticFiles(directory="formula_1/static"), name="static"
)
app.mount(
    "/fonts",
    StaticFiles(directory="formula_1/static/app/fonts"),
    name="fonts",
)

app.include_router(companies.router)
app.include_router(organizations.router)
app.include_router(users.router)


@app.get("/", response_class=HTMLResponse)
@app.get("/app/{path:path}", response_class=HTMLResponse)
def home():
    return FileResponse("formula_1/templates/index.html")
