import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, Base, get_db
import app.models
from app.routers import (
    auth_router,
    profile_router,
    users_router,
    restaurant_router,
    geo_router,
    ai_search_router,
    search_router,
    admin_router,
    preferences_router,
)

# Tự động tạo bảng CSDL
Base.metadata.create_all(bind=engine)

def _seed_demo_accounts():
    from app.core.database import SessionLocal
    from app.core.security import hash_password
    from app.models.user import User, UserProfile, Role, UserRole
    db = SessionLocal()
    try:
        for r_name, desc in [("user", "Người dùng"), ("admin", "Quản trị viên")]:
            if not db.query(Role).filter_by(name=r_name).first():
                db.add(Role(name=r_name, description=desc))
        db.commit()

        demo_list = [
            ("sinhvien@example.com", "123456", "Nguyễn Văn An", "user"),
            ("admin@smartdining.vn", "123456", "Quản trị viên", "admin"),
        ]
        for email, pwd, full_name, r_name in demo_list:
            if not db.query(User).filter_by(email=email).first():
                u = User(email=email, hashed_password=hash_password(pwd), status="active")
                db.add(u)
                db.flush()
                db.add(UserProfile(user_id=u.id, full_name=full_name))
                role = db.query(Role).filter_by(name=r_name).first()
                db.add(UserRole(user_id=u.id, role_id=role.id))
        db.commit()
    finally:
        db.close()

_seed_demo_accounts()


app = FastAPI(
    title="Smart Dining - Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí",
    description="Backend API phục vụ Hệ thống Smart Dining - Module 1 (Auth), Module 2 (AI Chat) & Module 4 (Restaurants)",
    version="1.0.0",
)

# Cho phép Frontend (Live Server 5500) gọi API sang Backend (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các Router API
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(users_router)
app.include_router(restaurant_router)
app.include_router(geo_router)
app.include_router(ai_search_router)
app.include_router(search_router)
app.include_router(admin_router)
app.include_router(preferences_router)

# Mount thư mục frontend để chạy trực tiếp HTML trên cổng 8000
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
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
        "docs_url": "/docs",
        "home_ui": "/frontend/index.html",
        "admin_restaurants_ui": "/frontend/admin-restaurants.html",
    }


@app.get("/restaurant-detail", tags=["Frontend UI"], summary="Trang Chi tiết Nhà hàng & Thực đơn (FR-09 / TE9C662)")
@app.get("/restaurant-detail.html", tags=["Frontend UI"], summary="Trang Chi tiết Nhà hàng & Thực đơn (FR-09 / TE9C662)")
def serve_restaurant_detail_page():
    detail_file = os.path.join(FRONTEND_DIR, "restaurant-detail.html")
    if os.path.exists(detail_file):
        return FileResponse(detail_file)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Trang chi tiết nhà hàng chưa được khởi tạo.",
    )



@app.get("/api/test-db", tags=["Hệ thống"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Kết nối CSDL thành công!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "error": str(e)},
        )
        
app.get("/", include_in_schema=False)
def serve_home_page():
    return RedirectResponse(url="/frontend/index.html")

@app.get("/login", include_in_schema=False)
def serve_login():
    return RedirectResponse(url="/frontend/login.html")

@app.get("/register", include_in_schema=False)
def serve_register():
    return RedirectResponse(url="/frontend/register.html")

@app.get("/profile", include_in_schema=False)
def serve_profile():
    return RedirectResponse(url="/frontend/profile.html")

@app.get("/admin", include_in_schema=False)
def serve_admin():
    return RedirectResponse(url="/frontend/admin.html")

@app.get("/admin/menu", include_in_schema=False)
def serve_admin_menu():
    return RedirectResponse(url="/frontend/admin-menu.html")

@app.get("/admin/images", include_in_schema=False)
def serve_admin_images():
    return RedirectResponse(url="/frontend/admin-images.html")