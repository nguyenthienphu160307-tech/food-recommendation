import os
import sys

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo import được module app từ thư mục gốc
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ui_and_auth_suite():
    print("\n--- [TEST 1] Kiểm tra tải Trang chủ (GET /) ---")
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "Smart Dining" in res_home.text
    print("-> Trang chủ tải thành công (HTTP 200)")

    print("\n--- [TEST 2] Kiểm tra tải Trang Đăng nhập (GET /login) ---")
    res_login = client.get("/login")
    assert res_login.status_code == 200
    assert "Đăng nhập" in res_login.text
    assert "login-form" in res_login.text
    print("-> Trang Đăng nhập tải thành công (HTTP 200)")

    print("\n--- [TEST 3] Kiểm tra tải Trang Đăng ký (GET /register) ---")
    res_reg = client.get("/register")
    assert res_reg.status_code == 200
    assert "Tạo tài khoản mới" in res_reg.text
    assert "otp-modal" in res_reg.text
    print("-> Trang Đăng ký & OTP Modal tải thành công (HTTP 200)")

    print("\n--- [TEST 4] Kiểm tra tải Static Asset Design System (GET /static/css/design-system.css) ---")
    res_css = client.get("/static/css/design-system.css")
    assert res_css.status_code == 200
    assert "--brand-primary" in res_css.text
    assert ".btn-primary" in res_css.text
    print("-> File CSS Design System tải thành công (HTTP 200)")

    # Đảm bảo tài khoản test sinhvien@example.com tồn tại
    from app.core.database import SessionLocal
    from app.core.security import hash_password
    from app.models.user import User, UserProfile, Role, UserRole

    db = SessionLocal()
    user = db.query(User).filter_by(email="sinhvien@example.com").first()
    if not user:
        user = User(
            email="sinhvien@example.com",
            hashed_password=hash_password("password123"),
            status="active",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        profile = UserProfile(user_id=user.id, full_name="Nguyễn Văn A")
        db.add(profile)
        user_role = db.query(Role).filter_by(name="user").first()
        if not user_role:
            user_role = Role(name="user", description="Người dùng chuẩn")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
        db.add(UserRole(user_id=user.id, role_id=user_role.id))
        db.commit()
    else:
        user.hashed_password = hash_password("password123")
        user.status = "active"
        db.commit()
    db.close()

    print("\n--- [TEST 5] Kiểm tra API Đăng nhập với Mật khẩu SAI (Kỳ vọng HTTP 401) ---")
    res_login_fail = client.post("/api/auth/login", json={
        "email": "sinhvien@example.com",
        "password": "wrong_password_123"
    })
    print("Status code:", res_login_fail.status_code)
    assert res_login_fail.status_code == 401
    assert "chính xác" in res_login_fail.json()["detail"]
    print("-> Đã chặn đúng mật khẩu sai (HTTP 401)!")

    print("\n--- [TEST 6] Kiểm tra API Đăng nhập với Mật khẩu ĐÚNG (Kỳ vọng HTTP 200) ---")
    res_login_ok = client.post("/api/auth/login", json={
        "email": "sinhvien@example.com",
        "password": "password123"
    })
    print("Status code:", res_login_ok.status_code)
    assert res_login_ok.status_code == 200
    data = res_login_ok.json()
    assert data["message"] == "Đăng nhập thành công!"
    assert "token" in data
    assert data["user"]["email"] == "sinhvien@example.com"
    print("-> Đăng nhập thành công, nhận token và thông tin người dùng (HTTP 200)!")

    print("\n>>> TẤT CẢ CÁC CA KIỂM THỬ FRONTEND UI & AUTH (TSK-12) ĐỀU ĐẠT CHUẨN! <<<")


if __name__ == "__main__":
    test_ui_and_auth_suite()
