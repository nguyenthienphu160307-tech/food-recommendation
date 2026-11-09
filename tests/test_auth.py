import sys
import os

# Thêm thư mục gốc dự án vào sys.path để import app.* không bị lỗi
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo console Windows in tiếng Việt UTF-8 không bị lỗi charmap
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import User, UserProfile, UserRole, Role, OTPStorage, RevokedToken
from app.core.security import hash_password

client = TestClient(app)


def cleanup_db():
    """Hàm dọn dẹp dữ liệu để test có thể lặp lại nhiều lần độc lập"""
    db = SessionLocal()
    db.query(RevokedToken).delete()
    db.query(UserRole).delete()
    db.query(UserProfile).delete()
    db.query(User).delete()
    db.query(OTPStorage).delete()
    db.commit()
    db.close()


def run_tests():
    print("================================================================")
    print("   BẮT ĐẦU CHẠY TOÀN BỘ BỘ TEST SUITE CHO AUTH & RBAC (BR-07)   ")
    print("================================================================\n")

    cleanup_db()

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 1] KIỂM THỬ GỬI OTP VÀ ĐĂNG KÝ TÀI KHOẢN (TSK-02)
    # -------------------------------------------------------------
    print("--- [TEST 1] Yêu cầu cấp mã OTP cho email sinhvien@example.com ---")
    res1 = client.post("/api/auth/send-otp", json={"email": "sinhvien@example.com"})
    print("Response status:", res1.status_code)
    assert res1.status_code == 200, f"Expected 200, got {res1.status_code}"

    # Lấy mã OTP trong CSDL vừa sinh ra
    db = SessionLocal()
    otp_record = (
        db.query(OTPStorage)
        .filter(OTPStorage.contact == "sinhvien@example.com")
        .order_by(OTPStorage.id.desc())
        .first()
    )
    assert otp_record is not None
    otp_code = otp_record.otp_code
    print(f"-> Đã lấy được mã OTP từ CSDL: {otp_code}")

    print("\n--- [TEST 2] Thử đăng ký với OTP SAI (999999) (Kỳ vọng 400 Bad Request) ---")
    res2 = client.post("/api/auth/register", json={
        "email": "sinhvien@example.com",
        "phone_number": "0912345678",
        "password": "password123",
        "full_name": "Nguyễn Văn A",
        "otp_code": "999999"
    })
    print("Response status:", res2.status_code)
    assert res2.status_code == 400

    print("\n--- [TEST 3] Đăng ký tài khoản với OTP ĐÚNG (Kỳ vọng 201 Created) ---")
    res3 = client.post("/api/auth/register", json={
        "email": "sinhvien@example.com",
        "phone_number": "0912345678",
        "password": "password123",
        "full_name": "Nguyễn Văn A",
        "otp_code": otp_code
    })
    print("Response status:", res3.status_code)
    assert res3.status_code == 201
    db.close()

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 2] KIỂM THỬ API ĐĂNG NHẬP & CẤP TOKEN (POST /api/auth/login)
    # -------------------------------------------------------------
    print("\n--- [TEST 4] Đăng nhập SAI mật khẩu (Kỳ vọng 401 Unauthorized) ---")
    res4 = client.post("/api/auth/login", json={
        "account": "sinhvien@example.com",
        "password": "wrong_password"
    })
    print("Response status:", res4.status_code)
    assert res4.status_code == 401

    print("\n--- [TEST 5] Đăng nhập ĐÚNG qua Email (Kỳ vọng 200 OK + JWT Tokens) ---")
    res5 = client.post("/api/auth/login", json={
        "account": "sinhvien@example.com",
        "password": "password123"
    })
    print("Response status:", res5.status_code)
    login_data = res5.json()
    assert res5.status_code == 200
    assert "tokens" in login_data
    assert "access_token" in login_data["tokens"]
    assert "refresh_token" in login_data["tokens"]
    assert login_data["tokens"]["token_type"] == "bearer"
    assert "user" in login_data
    assert "user" in login_data["user"]["roles"]
    print(f"-> Nhận Access Token: {login_data['tokens']['access_token'][:30]}...")
    print(f"-> Nhận Refresh Token: {login_data['tokens']['refresh_token'][:30]}...")

    user_access_token = login_data["tokens"]["access_token"]
    user_refresh_token = login_data["tokens"]["refresh_token"]

    print("\n--- [TEST 6] Đăng nhập ĐÚNG qua Số điện thoại (Kỳ vọng 200 OK) ---")
    res6 = client.post("/api/auth/login", json={
        "account": "0912345678",
        "password": "password123"
    })
    print("Response status:", res6.status_code)
    assert res6.status_code == 200
    assert res6.json()["user"]["email"] == "sinhvien@example.com"

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 3] KIỂM THỬ QUY TẮC BR-07: CHẶN TÀI KHOẢN BỊ KHÓA ('locked')
    # -------------------------------------------------------------
    print("\n--- [TEST 7] Khóa tài khoản người dùng và thử đăng nhập (Kiểm tra BR-07) ---")
    db = SessionLocal()
    user_record = db.query(User).filter(User.email == "sinhvien@example.com").first()
    assert user_record is not None
    user_record.status = "locked"  # Admin khóa tài khoản theo BR-07
    db.commit()
    db.close()

    res7 = client.post("/api/auth/login", json={
        "account": "sinhvien@example.com",
        "password": "password123"
    })
    print("Response status:", res7.status_code)
    print("Response detail:", res7.json().get("detail"))
    assert res7.status_code == 403, f"Expected 403 Forbidden for locked account, got {res7.status_code}"
    assert "BR-07" in res7.json().get("detail", "")

    # Mở khóa lại tài khoản để tiếp tục các bài kiểm thử sau
    db = SessionLocal()
    user_record = db.query(User).filter(User.email == "sinhvien@example.com").first()
    user_record.status = "active"
    db.commit()
    db.close()

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 4] KIỂM THỬ MIDDLEWARE PHÂN QUYỀN RBAC (Guest, User, Admin)
    # -------------------------------------------------------------
    print("\n--- [TEST 8] Khách (Guest - Không có Token) truy cập Endpoint công khai (BR-02) ---")
    res8 = client.get("/api/auth/public-info")
    print("Response status:", res8.status_code)
    print("Response JSON:", res8.json())
    assert res8.status_code == 200
    assert res8.json().get("role") == "guest"
    assert res8.json().get("access_level") == "limited"

    print("\n--- [TEST 9] Khách (Guest) truy cập Endpoint yêu cầu quyền User (Kỳ vọng 401 Unauthorized) ---")
    res9 = client.get("/api/auth/user-only")
    print("Response status:", res9.status_code)
    assert res9.status_code == 401

    print("\n--- [TEST 10] User có Token hợp lệ truy cập Endpoint thành viên (/user-only) (Kỳ vọng 200 OK) ---")
    headers_user = {"Authorization": f"Bearer {user_access_token}"}
    res10 = client.get("/api/auth/user-only", headers=headers_user)
    print("Response status:", res10.status_code)
    print("Response JSON:", res10.json())
    assert res10.status_code == 200

    print("\n--- [TEST 11] User thường truy cập Endpoint Quản trị viên (/admin-only) (Kỳ vọng 403 Forbidden) ---")
    res11 = client.get("/api/auth/admin-only", headers=headers_user)
    print("Response status:", res11.status_code)
    print("Response detail:", res11.json().get("detail"))
    assert res11.status_code == 403, f"Expected 403 Forbidden, got {res11.status_code}"

    # Tạo một tài khoản Admin thực sự trong CSDL
    print("\n--- [TEST 12] Tạo tài khoản Admin và truy cập Endpoint Quản trị viên (/admin-only) ---")
    db = SessionLocal()
    admin_user = User(
        email="admin@smartdining.vn",
        hashed_password=hash_password("admin_secret_pass"),
        status="active"
    )
    db.add(admin_user)
    db.flush()

    admin_profile = UserProfile(user_id=admin_user.id, full_name="Hệ thống Quản trị viên")
    db.add(admin_profile)

    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Quản trị viên toàn quyền hệ thống")
        db.add(admin_role)
        db.flush()

    user_role_admin = UserRole(user_id=admin_user.id, role_id=admin_role.id)
    db.add(user_role_admin)
    db.commit()
    db.close()

    # Admin đăng nhập
    res12_login = client.post("/api/auth/login", json={
        "account": "admin@smartdining.vn",
        "password": "admin_secret_pass"
    })
    assert res12_login.status_code == 200
    admin_access_token = res12_login.json()["tokens"]["access_token"]
    headers_admin = {"Authorization": f"Bearer {admin_access_token}"}

    # Admin gọi /admin-only -> Kỳ vọng 200 OK
    res12 = client.get("/api/auth/admin-only", headers=headers_admin)
    print("Admin access response status:", res12.status_code)
    print("Admin access response JSON:", res12.json())
    assert res12.status_code == 200

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 5] KIỂM THỬ REFRESH TOKEN (POST /api/auth/refresh-token)
    # -------------------------------------------------------------
    print("\n--- [TEST 13] Cấp mới Access Token bằng Refresh Token (Kỳ vọng 200 OK) ---")
    res13 = client.post("/api/auth/refresh-token", json={
        "refresh_token": user_refresh_token
    })
    print("Response status:", res13.status_code)
    assert res13.status_code == 200
    new_access_token = res13.json()["access_token"]
    print(f"-> Nhận Access Token mới: {new_access_token[:30]}...")

    # Sử dụng Access Token mới vừa cấp
    res13_verify = client.get("/api/auth/user-only", headers={"Authorization": f"Bearer {new_access_token}"})
    assert res13_verify.status_code == 200
    print("-> Xác nhận Access Token mới hoạt động hoàn toàn chính xác!")

    # -------------------------------------------------------------
    # [GIAI ĐOẠN 6] KIỂM THỬ ĐĂNG XUẤT (POST /api/auth/logout) & THU HỒI TOKEN
    # -------------------------------------------------------------
    print("\n--- [TEST 14] Thực hiện Đăng xuất tài khoản (POST /api/auth/logout) ---")
    res14 = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {new_access_token}"},
        json={"refresh_token": user_refresh_token}
    )
    print("Logout response status:", res14.status_code)
    print("Logout response JSON:", res14.json())
    assert res14.status_code == 200

    print("\n--- [TEST 15] Thử dùng lại Token ĐÃ ĐĂNG XUẤT (Kỳ vọng 401 Unauthorized) ---")
    res15 = client.get("/api/auth/user-only", headers={"Authorization": f"Bearer {new_access_token}"})
    print("Response status sau khi logout:", res15.status_code)
    print("Response detail:", res15.json().get("detail"))
    assert res15.status_code == 401
    assert "đăng xuất" in res15.json().get("detail", "").lower() or "kết thúc" in res15.json().get("detail", "").lower()

    print("\n--- [TEST 16] Thử dùng Refresh Token ĐÃ BỊ THU HỒI (Kỳ vọng 401 Unauthorized) ---")
    res16 = client.post("/api/auth/refresh-token", json={"refresh_token": user_refresh_token})
    print("Response status refresh sau khi logout:", res16.status_code)
    assert res16.status_code == 401

    print("\n================================================================")
    print(">>> TẤT CẢ 16 KỊCH BẢN KIỂM THỬ ĐÃ THÀNH CÔNG VƯỢT QUA (ALL 16 TESTS PASSED)! <<<")
    print("================================================================\n")


if __name__ == "__main__":
    run_tests()
