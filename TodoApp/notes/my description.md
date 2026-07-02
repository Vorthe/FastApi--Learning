```python
from typing import Annotated---->"" 
from fastapi import APIRouter, Depends---->""
from pydantic import BaseModel---->""
from sqlalchemy.orm import Session---->""
from database import SessionLocal---->""
from models import Users---->""
from passlib.context import CryptContext---->""
from starlette import status---->""
from fastapi.security import OAuth2PasswordRequestForm---->""

router = APIRouter()---->""

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")---->""


class CreateUserRequest(BaseModel):---->""
    username: str---->""
    email: str---->""
    first_name: str---->""
    last_name: str---->""
    password: str---->""
    role: str---->""


def get_db():---->""
    db = SessionLocal()---->""
    try:---->""
        yield db---->""
    finally:---->""
        db.close()---->""


db_dependency = Annotated[Session, Depends(get_db)]---->""


def authenticate_user(username: str, password: str, db):---->""
    user = db.query(Users).filter(Users.username == username).first()---->""
    if not user:---->""
        return False---->""
    if not bcrypt_context.verify(password, user.hashed_password):---->""
        return False---->""
    return True---->""


@router.post("/auth", status_code=status.HTTP_201_CREATED)---->""
async def create_user(db: db_dependency, create_user_reaquest: CreateUserRequest):---->""
    create_user_model = Users(---->""
        email=create_user_reaquest.email,---->""
        username=create_user_reaquest.username,---->""
        first_name=create_user_reaquest.first_name,---->""
        last_name=create_user_reaquest.last_name,---->""
        role=create_user_reaquest.role,---->""
        hashed_password=bcrypt_context.hash(create_user_reaquest.password),---->""
        is_active=True,---->""
    )
    db.add(create_user_model)---->""
    db.commit()---->""


@router.post("/token")---->""
async def login_for_access_token(---->""
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency---->""
):
    user=authenticate_user(form_data.username,form_data.password,db)---->""
    if not user:---->""
        return "Failed Authentication"---->""
    return "Successful Authentication"---->""









from typing import Annotated---->""
from pydantic import BaseModel, Field---->""
from sqlalchemy.orm import Session---->""
from fastapi import APIRouter, Depends, HTTPException, Path---->""
from models import Todos---->""
from database import SessionLocal---->""
from starlette import status---->""

router = APIRouter()---->""


def get_db():---->""
    db = SessionLocal()---->""
    try:---->""
        yield db---->""
    finally:---->""
        db.close()---->""


db_dependency = Annotated[Session, Depends(get_db)]---->""


class TodoRequest(BaseModel):---->""
    title: str = Field(min_length=3)---->""
    description: str = Field(min_length=3, max_length=100)---->""
    priority: int = Field(gt=0, lt=6)---->""
    complete: bool = Field()---->""


@router.get("/")---->""
async def read_all(db: db_dependency):---->""
    return db.query(Todos).all()---->""


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)---->""
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):---->""
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()---->""
    if todo_model is not None:---->""
        return todo_model---->""
    raise HTTPException(status_code=404, detail="Todo not found.")---->""


@router.post("/todo", status_code=status.HTTP_201_CREATED)---->""
async def create_todo(db: db_dependency, todo_request: TodoRequest):---->""
    todo_model = Todos(**todo_request.model_dump())---->""

    db.add(todo_model)---->""
    db.commit()---->""


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)---->""
async def update_todo(---->""
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)---->""
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()---->""
    if todo_model is None:---->""
        raise HTTPException(status_code=404, detail="Todo not found")---->""

    todo_model.title = todo_request.title---->""
    todo_model.description = todo_request.description---->""
    todo_model.priority = todo_request.priority---->""
    todo_model.complete = todo_request.complete---->""

    db.add(todo_model)---->""
    db.commit()---->""


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)---->""
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):---->""
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()---->""
    if todo_model is None:---->""
        raise HTTPException(status_code=404, detail="Todo id not found")---->""

    db.query(Todos).filter(Todos.id == todo_id).delete()---->""
    db.commit()---->""









from sqlalchemy import create_engine---->""
from sqlalchemy.orm import sessionmaker---->""
from sqlalchemy.ext.declarative import declarative_base---->""

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"---->""
engine = create_engine(---->""
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}---->""
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)---->""
Base = declarative_base()---->""









from database import Base ;----"این همون متغیره بیس هست که توی خودش مادراصلی مدل ها رو داره همون متغیرع دکلرتیو بیس هست"
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean ;----"از سیکیول‌آلچمی ستون فارن کی اینتیجر استرینگ و مقدار صحیح و غلط رو میاره تا بتونیم مقداردهی کنیم و به دیتابیس با زبان پایتون بفرستیم"


class Users(Base): ;----"کلاس یوزر که از بیس که همون میشه دکلرتیو بیس ارث بری میکنه"
    __tablename__ = "users" ;----"با این دستور دبل آندراسکور اسم تیبل کاربرهارو رومیسازیم"
    id = Column(Integer, primary_key=True, index=True) ;----"مشخصات ایدیمون باید عددی باشه ،کلید اصلی باشه تا باهاش بتونیم اطلاعات از دیتابیس بگیریم،ایندکس ترو هنوز برای من جا نیوفتاده چون ما برای دسترسی به اطلاعات کاربر توی دیتابیس با آیدی میتونیم بهشون برسیم ولی بازم ایندکس ترو یا فالس بودنش رو هنوز نمیدونم یعنی چی؟"
    email = Column(String, unique=True) ;----"این ستون باید حروفی باشه و فقط یونیک باشه و ایمیلی تکراری نباید باشه"
    username = Column(String, unique=True) ;----"این ستون باید حروفی باشه و فقط یونیک باشه و ایمیلی تکراری نباید باشه"
    first_name = Column(String) ;----"این ستون باید حروفی باشه"
    last_name = Column(String) ;----"این ستون باید حروفی باشه"
    hashed_password = Column(String) ;----"این ستون باید حروفی باشه"
    is_active = Column(Boolean, default=True) ;----"این ستونمون باید دوحالته باشه یا ترو یا فالس "
    role = Column(String) ;----"این ستون باید حروفی باشه"


class Todos(Base): ;----""
    __tablename__ = "todos" ;----"با این دستور دبل آندراسکور اسم تیبل کارهایی که قراره انجام بدیم رو رومیسازیم"
    id = Column(Integer, primary_key=True, index=True) ;----"مشخصات ایدیمون باید عددی باشه ،کلید اصلی باشه تا باهاش بتونیم اطلاعات از دیتابیس بگیریم"
    title = Column(String) ;----"این ستون باید حروفی باشه"
    description = Column(String) ;----"این ستون باید حروفی باشه"
    priority = Column(Integer) ;----"این ستون باید عددی باشه"
    complete = Column(Boolean, default=False);----"این ستونمون باید دوحالته باشه یا ترو یا فالس"
    owner_id=Column(Integer,ForeignKey("users.id")) ;----"اینجا چون فارن کی زدیم باید تیبل رو که متصل میشیم رو تعیین کنیم و کنارش بگیم به کدوم ستون که اینجا میشه آیدی فارن کی میزنیم یعنی به کلید آیدی کوئری میزنیم تا فقط با یه عدد ایدی به اطلاعات کل اون سطر برسیم"









from fastapi import FastAPI ;----"اصل برنامه همینه که باید ایمپورت کنیم فستای پی ای رو"
import models;----"برای اینکه رنامه اجرا بشه باید مدل هامون رو ایمپورت کنیم"
from database import engine;----"انجین یه متغیره که کریت انجین توش قرار گرفته و واسط بین دیتابیس با برناممون هست که ما در اصل میگیم اسم دیتابیسمون اینه و ترید هم فالس چون دیتابیس اسکیولایت هست"
from routers import auth, todos;----"فایل های آث و تودوس رو از روترز ایمپورت میکنیم زیرا ای پی آی هایی که نوشتیم رو در فایل همشون رو تو پوشه روت ها ای پی آی هاشو مینویسیم و توی پوشه مین ایمپورت میکنیم و بعد برای اجرا توی ترمینال مین رو بعنوان اپ استفاده میکنیم "

app = FastAPI();----"این برای اینه که تو ترمینال میخاییم برنامه راه اندازی کنیم باید اپ بنویسیم دو نقطه بزاریم و پوشه مین رو بنویسیم که ای پی آی هایی که نوشتیم توی روتر هست و اونم به مین ارجاع داده شده"


models.Base.metadata.create_all(bind=engine);----"بر اساس مدلهایی که ساختم و از داخل بیس که در اصلمادر و پایه مدل هایی که میسازیم از اون تابع کریت آل که یعنی تمامی جداول رو میسازیم و من فقط اینجا نقش metadata رو نفهمیدم"

app.include_router(auth.router);----"با این دستور یعنی مسیر آث و تودوس یا بهتره بگم روت های یا ای پی آی های تودوس و آث که ویژگی و براشون شرایط ساختیم شامل پوشه روترمیشه که اونم از برنامه یا اپ که ساختیم همشون میرن اونجا"
app.include_router(todos.router);----"با این دستور یعنی مسیر آث و تودوس یا بهتره بگم روت های یا ای پی آی های تودوس و آث که ویژگی و براشون شرایط ساختیم شامل پوشه روترمیشه که اونم از برنامه یا اپ که ساختیم همشون میرن اونجا"

