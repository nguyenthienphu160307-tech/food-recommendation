import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Nạp biến môi trường từ file .env
load_dotenv()

# 1. Đọc chuỗi kết nối duy nhất từ file .env (Mặc định dùng SQLite nếu chưa cấu hình để dễ dàng phát triển & kiểm thử)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./food_recommendation.db"

# 2. Tự động kiểm tra và khởi tạo Database nếu chưa tồn tại
try:
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)
except Exception as e:
    print(f"[CANH BAO] Khong the tu dong khoi tao database: {e}")

# 3. Khởi tạo engine kết nối
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# 4. Quản lý Session phiên làm việc
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 5. Base Model kế thừa
Base = declarative_base()


# 6. Dependency cấp phát kết nối DB cho từng request API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
