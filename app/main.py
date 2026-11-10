from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import engine, Base, get_db
import app.models  # Nạp các model để SQLAlchemy nhận diện bảng trước khi tạo
from app.routers import auth_router, admin_router, preferences_router

# Tự động tạo các bảng CSDL (Users, UserProfiles, Roles, UserRoles, OTPStorage)
Base.metadata.create_all(bind=engine)

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Smart Dining - Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí",
    description="Backend API phục vụ Hệ thống Smart Dining - Module 1 (Auth & User) - Task TSK-02",
    version="1.0.0"
)

# Đăng ký Router
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(preferences_router)


@app.on_event("startup")
def init_default_data():
    """Khởi tạo tài khoản Quản trị viên (admin@foodai.vn) và User chuẩn (user.demo@foodai.vn)"""
    from app.core.database import SessionLocal
    from app.models import User, UserProfile, UserPreference, Role, UserRole
    from app.core.security import hash_password

    db = SessionLocal()
    try:
        role_user = db.query(Role).filter(Role.name == "user").first()
        if not role_user:
            role_user = Role(name="user", description="Người dùng hệ thống")
            db.add(role_user)

        role_admin = db.query(Role).filter(Role.name == "admin").first()
        if not role_admin:
            role_admin = Role(name="admin", description="Quản trị viên hệ thống")
            db.add(role_admin)

        db.commit()
        if role_user: db.refresh(role_user)
        if role_admin: db.refresh(role_admin)

        # Đảm bảo tài khoản Admin
        admin = db.query(User).filter(User.email == "admin@foodai.vn").first()
        if not admin:
            admin = User(
                email="admin@foodai.vn",
                phone_number="0909999888",
                hashed_password=hash_password("admin123"),
                status="active"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

            prof_admin = UserProfile(
                user_id=admin.id,
                full_name="Quản trị viên FoodAI",
                default_address="11 Nguyễn Đình Chiểu, Phường Đa Kao, Quận 1, TP.HCM",
                default_lat=10.7860,
                default_lng=106.7003
            )
            ur_admin = UserRole(user_id=admin.id, role_id=role_admin.id)
            db.add_all([prof_admin, ur_admin])
            db.commit()

        # Đảm bảo tài khoản Người dùng Demo kèm UserPreferences
        demo = db.query(User).filter(User.email == "user.demo@foodai.vn").first()
        if not demo:
            demo = User(
                email="user.demo@foodai.vn",
                phone_number="0901111222",
                hashed_password=hash_password("user123"),
                status="active"
            )
            db.add(demo)
            db.commit()
            db.refresh(demo)

            prof_demo = UserProfile(
                user_id=demo.id,
                full_name="Nguyễn Văn An",
                default_address="11 Nguyễn Đình Chiểu, Phường Đa Kao, Quận 1, TP.HCM",
                default_lat=10.7860,
                default_lng=106.7003
            )
            ur_demo = UserRole(user_id=demo.id, role_id=role_user.id)
            pref_demo = UserPreference(
                user_id=demo.id,
                diet_type="omnivore",
                allergies="[]",
                preferred_cuisines='["Món Việt", "Lẩu Nướng"]',
                avg_budget=250000.0
            )
            db.add_all([prof_demo, ur_demo, pref_demo])
            db.commit()
    finally:
        db.close()


@app.get("/", tags=["Hệ thống"])
def root():
    return {
        "status": "online",
        "message": "Chào mừng bạn đến với API Hệ thống Smart Dining!",
        "docs_url": "/docs"
    }


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
