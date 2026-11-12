import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers import auth_router, restaurant_router, geo_router, users_router
from app.core.database import engine, Base, get_db
import app.models
from app.routers import auth_router, profile_router, geo_router, ai_search_router
# Tự động tạo bảng CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Dining - Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí",
    description="Backend API phục vụ Hệ thống Smart Dining - Module 1 (Auth), Module 2 (AI Chat) & Module 4 (Restaurants)",
    version="1.0.0"
)

# Đăng ký các Router API
app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(users_router)
app.include_router(ai_search_router)

# Gắn các router API vào hệ thống
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(geo_router)
app.include_router(ai_search_router)

# Mount thư mục frontend để chạy trực tiếp HTML trên cổng 8000
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")


# Các route phục vụ Giao diện Người dùng (Frontend UI - TSK-12)
@app.get("/", tags=["Frontend UI"], summary="Trang chủ khám phá ẩm thực")
def serve_home_page():
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "message": "Chào mừng bạn đến với API Hệ thống Smart Dining!",
        "docs_url": "/docs",
        "home_ui": "/frontend/index.html",
        "admin_restaurants_ui": "/frontend/admin-restaurants.html"
    }


@app.get("/api/test-db", tags=["Hệ thống"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Kết nối CSDL thành công!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "error": str(e)}
        )