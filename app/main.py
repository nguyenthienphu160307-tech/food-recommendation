import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import engine, Base, get_db
import app.models  # Nạp các model để SQLAlchemy nhận diện bảng trước khi tạo
from app.routers import auth_router, restaurant_router, user_router, search_router

# Tự động tạo các bảng CSDL (Users, UserProfiles, Roles, UserRoles, OTPStorage, Restaurants, SearchSessions, SearchMessages, SearchCriteria, ...)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[CANH BAO] Khong the tu dong khoi tao database: {e}")

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Smart Dining - Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí",
    description="Backend API phục vụ Hệ thống Smart Dining - Module 1 (Auth), Module 2 (AI Chat) & Module 4 (Restaurants)",
    version="1.0.0"
)

# Đăng ký các Router API
app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(user_router)
app.include_router(search_router)

# Mount thư mục static assets nếu tồn tại
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# Các route phục vụ Giao diện Người dùng (Frontend UI - TSK-12)
@app.get("/", tags=["Frontend UI"], summary="Trang chủ khám phá ẩm thực")
def serve_home_page():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "message": "Chào mừng bạn đến với API Hệ thống Smart Dining!",
        "docs_url": "/docs"
    }


@app.get("/login", tags=["Frontend UI"], summary="Trang Đăng nhập (TSK-12)")
def serve_login_page():
    login_file = os.path.join(FRONTEND_DIR, "login.html")
    if os.path.exists(login_file):
        return FileResponse(login_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang đăng nhập.")


@app.get("/register", tags=["Frontend UI"], summary="Trang Đăng ký & Xác thực OTP (TSK-12)")
def serve_register_page():
    register_file = os.path.join(FRONTEND_DIR, "register.html")
    if os.path.exists(register_file):
        return FileResponse(register_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang đăng ký.")


@app.get("/profile", tags=["Frontend UI"], summary="Trang Cài đặt Hồ sơ cá nhân")
@app.get("/profile.html", tags=["Frontend UI"], include_in_schema=False)
def serve_profile_page():
    profile_file = os.path.join(FRONTEND_DIR, "profile.html")
    if os.path.exists(profile_file):
        return FileResponse(profile_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang hồ sơ.")


@app.get("/index.html", tags=["Frontend UI"], include_in_schema=False)
def serve_index_alias():
    return serve_home_page()



@app.get(
    "/api/test-db",
    tags=["Hệ thống"],
    summary="Kiểm tra kết nối tới Cơ sở dữ liệu MySQL"
)
def test_db_connection(db: Session = Depends(get_db)):
    """
    API kiểm tra trạng thái kết nối Cơ sở dữ liệu:
    1. Thực thi truy vấn SELECT DATABASE(), VERSION() để kiểm tra kết nối sống tới MySQL.
    2. Lấy danh sách toàn bộ các bảng hiện có trong CSDL `food_recomentdation`.
    3. Trả về thông tin chi tiết (Tên DB, phiên bản MySQL, số lượng bảng và tên các bảng).
    """
    try:
        # Thực hiện câu lệnh truy vấn kiểm tra kết nối trực tiếp
        db_info = db.execute(text("SELECT DATABASE(), VERSION()")).fetchone()
        db_name = db_info[0] if db_info else None
        db_version = db_info[1] if db_info else None

        # Lấy danh sách các bảng hiện có trong database
        tables_result = db.execute(text("SHOW TABLES")).fetchall()
        tables = [row[0] for row in tables_result]

        return {
            "status": "success",
            "message": "Kết nối tới cơ sở dữ liệu MySQL thành công!",
            "database_name": db_name,
            "mysql_version": db_version,
            "total_tables": len(tables),
            "tables": tables
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Kết nối tới cơ sở dữ liệu thất bại! Vui lòng kiểm tra lại dịch vụ MySQL.",
                "error": str(e)
            }
        )
