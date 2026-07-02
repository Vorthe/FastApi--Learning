```python
router = APIRouter() # برای ماژولار کردن مسیرها و جلوگیری از شلوغی فایل اصلی
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # تنظیم موتور هشینگ؛ بدون این خط هیچ راه امنی برای ذخیره پسورد نداری
class CreateUserRequest(BaseModel): # تعریف ساختار ورودی؛ برای اینکه FastAPI بدونه چه فیلدهایی رو از کلاینت بگیره و ولیدیشن کنه
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
def get_db(): # مدیریت چرخه حیات Session؛ استفاده از yield باعث میشه Connection بعد از اتمام درخواست حتماً بسته بشه
    db = SessionLocal()
    try:
        yield db # خروجی: یک نمونه فعال از Session برای استفاده در Dependencyها
    finally:
        db.close() # تضمین آزادسازی منابع دیتابیس حتی در صورت بروز Error
db_dependency = Annotated[Session, Depends(get_db)] # تعریف یک Type Alias برای تمیزکاری؛ با این کار هر جا از این استفاده کنی، FastAPI خودش Session رو تزریق می‌کنه
def authenticate_user(username: str, password: str, db): # تابع منطق بیزنس؛ ورودی: اعتبارنامه‌ها و دیتابیس | خروجی: Boolean
    user = db.query(Users).filter(Users.username == username).first() # کوئری برای یافتن کاربر؛ اگر نبود None برمی‌گردونه
    if not user:
        return False # اگر کاربر وجود نداشت، ورود متوقف میشه
    if not bcrypt_context.verify(password, user.hashed_password): # مقایسه پسورد خام با هش ذخیره شده در دیتابیس
        return False # اگر هش مطابقت نداشت، ورود رد میشه
    return True # تایید نهایی
@router.post("/auth", status_code=status.HTTP_201_CREATED) # تعریف Endpoint ایجاد کاربر؛ خروجی: وضعیت 201 (Created)
async def create_user(db: db_dependency, create_user_reaquest: CreateUserRequest): # ورودی: Session و مدل Pydantic
    create_user_model = Users( # تبدیل دیتا از مدل Pydantic به مدل SQLAlchemy (ORM)
        email=create_user_reaquest.email,
        username=create_user_reaquest.username,
        first_name=create_user_reaquest.first_name,
        last_name=create_user_reaquest.last_name,
        role=create_user_reaquest.role,
        hashed_password=bcrypt_context.hash(create_user_reaquest.password), # حتماً باید اینجا هش بشه، ذخیره پسورد Plain-text فاجعه است
        is_active=True,
    )
    db.add(create_user_model) # آماده‌سازی برای ذخیره
    db.commit() # اجرای نهایی کوئری و ثبت در دیتابیس
@router.post("/token") # Endpoint استاندارد OAuth2 برای دریافت توکن
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency # استفاده از فرم استاندارد برای دریافت username/password
):
    user=authenticate_user(form_data.username,form_data.password,db) # فراخوانی تابع احراز هویت
    if not user:
        return "Failed Authentication" # ایراد: نباید متن ساده برگردونی؛ باید HTTPException با کد 401 بده
    return "Successful Authentication" # ایراد: اینجا باید JWT تولید و برگردونی، نه فقط یک رشته متنی

