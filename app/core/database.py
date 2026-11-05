import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Nạp biến môi trường từ file .env
load_dotenv()

# 1. Đọc chuỗi kết nối duy nhất từ file .env (Không còn bất kỳ biến lẻ tẻ nào)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Thiếu biến DATABASE_URL trong file .env! Vui lòng kiểm tra lại file cấu hình.")

# 2. Tự động kiểm tra và khởi tạo Database nếu chưa tồn tại
try:
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)
except Exception as e:
    print(f"[CANH BAO] Khong the tu dong khoi tao database: {e}")

# 3. Khởi tạo engine kết nối trực tiếp
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
