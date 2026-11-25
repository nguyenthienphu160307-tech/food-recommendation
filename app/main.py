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
    users_router,
    restaurant_router,
    geo_router,
    ai_search_router,
    search_router,
    search_history_router,
    admin_router,
    preferences_router,
    notification_router,
    review_router,
    image_router,
    menu_router,
    favorite_router,
)

# Tự động tạo bảng CSDL và seed tài khoản demo
Base.metadata.create_all(bind=engine)

def seed_demo_accounts():
    try:
        from app.models.user import User, UserProfile, Role, UserRole
        from app.core.security import hash_password
        db = Session(bind=engine)

        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Quản trị viên hệ thống")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            user_role = Role(name="user", description="Người dùng thông thường")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)

        admin_user = db.query(User).filter(User.email == "admin@smartdining.vn").first()
        if not admin_user:
            admin_user = User(
                email="admin@smartdining.vn",
                phone_number="0909999888",
                hashed_password=hash_password("123456"),
                status="active"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            db.add(UserProfile(user_id=admin_user.id, full_name="Quản trị viên Hệ thống"))
            db.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
            db.commit()
        else:
            admin_user.status = "active"
            db.commit()

        student_user = db.query(User).filter(User.email == "sinhvien@example.com").first()
        if not student_user:
            student_user = User(
                email="sinhvien@example.com",
                phone_number="0901234567",
                hashed_password=hash_password("123456"),
                status="active"
            )
            db.add(student_user)
            db.commit()
            db.refresh(student_user)
            db.add(UserProfile(user_id=student_user.id, full_name="Nguyễn Văn A"))
            db.add(UserRole(user_id=student_user.id, role_id=user_role.id))
            db.commit()
        elif student_user.profile and student_user.profile.full_name == "Quản trị viên Hệ thống":
            student_user.profile.full_name = "Nguyễn Văn A"
            db.commit()

        db.close()
    except Exception as e:
        print(f"[Seed] Khong the seed tai khoan demo: {e}")

_seed_demo_accounts = seed_demo_accounts
seed_demo_accounts()

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
app.include_router(users_router)
app.include_router(restaurant_router)
app.include_router(geo_router)
app.include_router(ai_search_router)
app.include_router(search_router)
app.include_router(search_history_router)
app.include_router(admin_router)
app.include_router(preferences_router)
app.include_router(notification_router)
app.include_router(review_router)
app.include_router(image_router)
app.include_router(menu_router)
app.include_router(favorite_router)

# Mount thư mục frontend để chạy trực tiếp HTML trên cổng 8000
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    js_dir = os.path.join(FRONTEND_DIR, "js")
    if os.path.isdir(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
    css_dir = os.path.join(FRONTEND_DIR, "css")
    if os.path.isdir(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")


@app.get("/venues-data.js", include_in_schema=False)
def serve_venues_data_js():
    file_path = os.path.join(FRONTEND_DIR, "js", "venues-data.js")
    if not os.path.exists(file_path):
        file_path = os.path.join(FRONTEND_DIR, "venues-data.js")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/javascript")
    raise HTTPException(status_code=404)


@app.get("/map-component.js", include_in_schema=False)
def serve_map_component_js():
    file_path = os.path.join(FRONTEND_DIR, "js", "map-component.js")
    if not os.path.exists(file_path):
        file_path = os.path.join(FRONTEND_DIR, "map-component.js")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/javascript")
    raise HTTPException(status_code=404)


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



@app.get("/login", tags=["Frontend UI"], summary="Trang Đăng nhập (TSK-12)")
@app.get("/login.html", tags=["Frontend UI"], include_in_schema=False)
def serve_login_page():
    login_file = os.path.join(FRONTEND_DIR, "login.html")
    if os.path.exists(login_file):
        return FileResponse(login_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang đăng nhập.")


@app.get("/register", tags=["Frontend UI"], summary="Trang Đăng ký & Xác thực OTP (TSK-12)")
@app.get("/register.html", tags=["Frontend UI"], include_in_schema=False)
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


@app.get("/preferences", tags=["Frontend UI"], summary="Trang Sở thích cá nhân")
@app.get("/preferences.html", tags=["Frontend UI"], include_in_schema=False)
def serve_preferences_page():
    pref_file = os.path.join(FRONTEND_DIR, "preferences.html")
    if os.path.exists(pref_file):
        return FileResponse(pref_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang sở thích.")


@app.get("/admin", tags=["Frontend UI"], summary="Trang Quản trị hệ thống")
@app.get("/admin.html", tags=["Frontend UI"], include_in_schema=False)
def serve_admin_page():
    admin_file = os.path.join(FRONTEND_DIR, "admin.html")
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang quản trị.")


@app.get("/admin-restaurants", tags=["Frontend UI"], summary="Trang Quản trị nhà hàng")
@app.get("/admin-restaurants.html", tags=["Frontend UI"], include_in_schema=False)
def serve_admin_restaurants_page():
    admin_rest_file = os.path.join(FRONTEND_DIR, "admin-restaurants.html")
    if os.path.exists(admin_rest_file):
        return FileResponse(admin_rest_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang quản trị nhà hàng.")


@app.get("/admin/menu", tags=["Frontend UI"], summary="Trang Quản trị thực đơn nhà hàng")
@app.get("/admin-menu", tags=["Frontend UI"], include_in_schema=False)
@app.get("/admin-menu.html", tags=["Frontend UI"], include_in_schema=False)
def serve_admin_menu_page():
    admin_menu_file = os.path.join(FRONTEND_DIR, "admin-menu.html")
    if os.path.exists(admin_menu_file):
        return FileResponse(admin_menu_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang quản trị thực đơn.")


@app.get("/admin/images", tags=["Frontend UI"], summary="Trang Quản lý thư viện ảnh nhà hàng")
@app.get("/admin-images", tags=["Frontend UI"], include_in_schema=False)
@app.get("/admin-images.html", tags=["Frontend UI"], include_in_schema=False)
def serve_admin_images_page():
    admin_images_file = os.path.join(FRONTEND_DIR, "admin-images.html")
    if os.path.exists(admin_images_file):
        return FileResponse(admin_images_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang quản trị thư viện ảnh.")


@app.get("/index.html", tags=["Frontend UI"], include_in_schema=False)
def serve_index_alias():
    return serve_home_page()


@app.get("/favorites-history", tags=["Frontend UI"], summary="Trang Quán ăn Yêu thích & Lịch sử Tìm kiếm AI")
@app.get("/favorites-history.html", tags=["Frontend UI"], include_in_schema=False)
def serve_favorites_history_page():
    fav_file = os.path.join(FRONTEND_DIR, "favorites-history.html")
    if os.path.exists(fav_file):
        return FileResponse(fav_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang yêu thích & lịch sử.")


@app.get("/admin-users-reviews", tags=["Frontend UI"], summary="Trang Quản lý Người dùng & Kiểm duyệt Đánh giá")
@app.get("/admin-users-reviews.html", tags=["Frontend UI"], include_in_schema=False)
def serve_admin_users_reviews_page():
    aur_file = os.path.join(FRONTEND_DIR, "admin-users-reviews.html")
    if os.path.exists(aur_file):
        return FileResponse(aur_file)
    raise HTTPException(status_code=404, detail="Không tìm thấy trang quản lý người dùng & kiểm duyệt.")


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
