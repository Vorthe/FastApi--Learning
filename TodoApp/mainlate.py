from typing import Annotated#فکر میکنم ویژگی یرای حاشیه نویسی و گنجاندن میژگی باشه

from pydantic import BaseModel, Field#در این حد میدونم از ولیدیشنی بنام پایدنتیک بیس مدل که همونفکر کنم یکسری ولیدیشن های عمومی باشه و فیلد هم که فکر میکنم مقدارهایی مثل مکس و مین رو آپشنشو میده

from sqlalchemy.orm import Session#از او ار ام مخصوص اسکیول آلچمی ایمپورت میکنیم که سشن ها کانال هایی هستن خودکار برای ارتباط

from fastapi import FastAPI, Depends, HTTPException, Path#از خود فست ای پی ای ایمپورت میکنیم خود فست ای پی ای ،دیپندز که فکر کنم برای وابستگی ایجاد کردن یا راه اتباطی با دیتابیس،اکسپشن برای خطاهایی که باید مدیریت کنیم و در اصل خطاهایی اماده برای سهولت،پتث برای مسیر دهی و گذاشتن قانون برای اون مسیر

import models#ایمپورت مدل هایی که ساختیم

from models import Todos#تیبیل تودوسی که ساختیم رو میاریم اینجا

from database import engine, SessionLocal#انجین یا موتوری که برای برناممون ساختیم و سشن لوکالی که اینهمه فرآیند رو جمع میکنه داخلش و به نوعی شاید یه اکوسیستم رو میاریم این صفحه

from starlette import status#از استارلت وضعیت که مخصوص نمایش وضعیت برای دیدن کدهایی مثل 204 برای آپدیت که تو یوای سواگر نشون میده

  

app = FastAPI()#راه اندازی فست ای پی آیمون

  
  

models.Base.metadata.create_all(bind=engine)#اینو اینهمه بلدم که میدونم میریم از مدلز بیس رو میاریم که همون دیکلریتیو بیس که اشتباه نکنم همون او ار ام پایه و ستون فقراتش ست بعدش میگه کریت آل یعنی همشو بساز  ولی داخل پرانتز که میگه بایند و اونم مساوی انجین هست که همون موتورمون میشه برای مناین رو القا میکنه که ما اینجا استارت رو زدیم و از کاربرها مشخصات رو از طریق تابع های زیر میگیریم و میفرستیم به جایی که میسازه و اونم از طریق سشن ها میرسونه به تیبل و بعدش ثبت میشن توی دیتابیس

  
  

def get_db():#اینو تقریبا یکم درکمیکنم ولی از توضیحدادنش عاجزم

    db = SessionLocal()#شاید سشن لوکالهمون سشن های داخلیمون که به دیتابیس اطلاعات رو میرسونیم

    try:

        yield db#این مبحث ییلد رو اصلابلد نیستم بمن بگو چیه و چه ویژگی داره که الان دقیق چی میگیره و چیکار میکنه و چی تویل میده واقعا برام سواله این ییلد باه و نباشه چی میشه؟

    finally:

        db.close()#اینممیگه تموم شدی دیتابیسمون رو ببند

  
  

db_dependency = Annotated[Session, Depends(get_db)]#تو این انوتیتدمن نمیدونم ویژگی انوتیتد اصلا چیه؟انوتیتد چی میسازه و چیکار میکنه درسته نمیدونم ولی حس میکنم انوتیتد یه نوت پد مدلی هست که میشه چندتا ویژگی براش مثل سشن و دیپندز رو توی خودش جای میده و از طریق این دو تا ایتم ارتباط بین کدهامون و دیتابیس رو برقرار میکنه و با سشن که حس میکنم شبیه کانال هایی هست که وابستگی های کاربر رو میگیره و تحویل میده به دیتابیس یه چیزی تو مایه های رابط یا واسط

  
  

class TodoRequest(BaseModel):#اینم یه کلاسی هست که مااسمشو تو دو ریکوِست گذاشتیم و از بیس مدل که فکر میکنم از پایدنتیک هستش ارث بری میکنه و ویژگی های برای مثال تایتل رو در فرمت استرینگ(حروفی) میگیره و با فیلد محدودیت هایی مثل حداقل و حداکثر طول حروف یا یکسری ویژگی های ترو و فالس رو میشه براش تعریف کرد

    title: str = Field(min_length=3)

    description: str = Field(min_length=3, max_length=100)

    priority: int = Field(gt=0, lt=6)

    complete: bool = Field()

  
  

@app.get("/")

async def read_all(db: db_dependency):

    return db.query(Todos).all()

  
  

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)

async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()#تو این خط به دیتابیس کوءری میزنیم که بره تیبیل تودوس و فیلتر کن و تودوس آیدی داخل تیبل با تودوآیدی کاربری که وارد میکنه درست بود دات فیرست که این فرست یهنی اولین کوردی که بدست میاری

    if todo_model is not None:

        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found.")

  
  

@app.post("/todo", status_code=status.HTTP_201_CREATED)

async def create_todo(db: db_dependency, todo_request: TodoRequest):

    todo_model = Todos(**todo_request.model_dump())

  

    db.add(todo_model)

    db.commit()

  
  

@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)

async def update_todo(

    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)

):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:

        raise HTTPException(status_code=404, detail="Todo not found")

  

    todo_model.title = todo_request.title

    todo_model.description = todo_request.description

    todo_model.priority = todo_request.priority

    todo_model.complete = todo_request.complete

  

    db.add(todo_model)

    db.commit()

  
  

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)

async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:

        raise HTTPException(status_code=404, detail="Todo id not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()

from sqlalchemy import create_engine #از کتابخانه اسکیوالچمی انجین رومیاریم 
from sqlalchemy.orm import sessionmaker#از کتابخانه اسکیوالچمی قسمت او ار ام تولیدکننده سشن رو میاریم 
from sqlalchemy.ext.declarative import declarative_base #ایه های اصلی اوار ام رومیاریم

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"#مسیر اصلی رو تعریف میکنیم
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}#چون از اسکیولایت استفاده میکنیم بهتره بزاریم رو فالس چون مالتی ترد نیست 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#سشن میکر رو میریزیم توی یه متغیری به اسم سشن لوکال و این ویزگی ها رو میدیم هر ثانیه اطلاعات رو خود به خود کامیت نکنه و موتورش از انچینی که درست کردیم استفاده  کنه
Base = declarative_base()#بیس مدلهایی که قراره درست کنیم رو میریزیم توی متغیر بیس و در مدل هایی که و کلاسهایی که درست میکنیم ار این متغیر به ارث میبریم
  
from database import Base#خب از دیتابیسی که ساختیم بیس رو ایمپورت میکنیم

from sqlalchemy import Column, Integer, String, Boolean#از سیکیولآلچمی ایمپورت میکنیم مقدارهایی که قراره یا عددی یا حروفی یا وترو یا فالسی روایمپورت میکنیم



class Todos(Base):#یه کلاس تیبل تعریف میکنیم 

    __tablename__ = "todos" #با این دستور و مجیک اندراسکور تیبیلی که داریم رو اسمگذاری میکنیم

    id = Column(Integer, primary_key=True, index=True)#تو این خط ایدی مشخصاتش باید ستون دارای ویژگی های اینتیجر و آیدی پریماری کی داشته باشه که یعنی فقط یدونه ایتم میتونه پریماری کی یا کلید اصلی باشه برای دسترسی ولی ایندکس ترو رو هم به این معنیه که اگه زیاد کوئری مینیم عین فهرستمیمونه و برامون تو پیدا کردن کمک میکنه

    title = Column(String)#ستون تایتل باید استرینگ(حروفی) باشه 

    description = Column(String)#ستون دیسکریپشن باید استرینگ(حروفی) باشه

    priority = Column(Integer)#ستون پرویاروتی باید اینتیجر(عددی) باشه

    complete = Column(Boolean, default=False)#ستون تایتل باید اینتیجر(عددی) باشه
# من اینارو اینطوری برات توضیحمیدم ببین این مدلی توضیح دادن خوبه برای درک عمیق و یادگیری خوب یا بهترشم میتونی بکنی؟
# و اینکه من یکمم خط کد دارم اونارو برات اینطوری توضیحی بنویسم بفرستمتا دقیق بفهمی من چقدر یاد گرفتم و بررسی کنی و چاله چوله های ذهنیمو درست کنی و در کل فکر میکنم ایده خوبی باشه که من توضیحی اون چیزی که تاالان فهمیدم رو بهت بگم