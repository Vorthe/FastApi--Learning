from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .database import engine
from .models import Base
from .routers import admin, auth, todos, users
from contextlib import asynccontextmanager

# from TodoApp.redis_client import redis_client

BASE_DIR = Path(__file__).resolve().parent


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await redis_client.ping()
#     print("Redis Connected")

#     yield

#     await redis_client.aclose()


# app = FastAPI(lifespan=lifespan)

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def healthy_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


# templates.TemplateResponse(
# request=request, name="home.html", context={"request": request}) #این چیه؟ این همون کدی هست که توی جینجای جدید باید کانتکست بنویسی و تقریبا شبیه جنگو شده
