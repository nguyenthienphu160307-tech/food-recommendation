import sys
import os

# Thêm thư mục gốc dự án vào sys.path để import app.* không bị lỗi
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import User, UserProfile, UserRole, Role, OTPStorage

client = TestClient(app)

def run_tests():
    # Dọn dẹp dữ liệu test cũ để test có thể chạy lặp lại nhiều lần
    clean_db = SessionLocal()
    clean_db.query(UserRole).delete()
    clean_db.query(UserProfile).delete()
    clean_db.query(User).delete()
    clean_db.query(OTPStorage).delete()
    clean_db.commit()
    clean_db.close()

    print("--- [TEST 1] Yêu cầu cấp mã OTP cho email sinhvien@example.com ---")
    res1 = client.post("/api/auth/send-otp", json={"email": "sinhvien@example.com"})
    print("Response status:", res1.status_code)
    print("Response JSON:", res1.json())
    assert res1.status_code == 200, f"Expected 200, got {res1.status_code}"

    # Lấy mã OTP trong database vừa sinh ra
    db = SessionLocal()
    otp_record = db.query(OTPStorage).filter(OTPStorage.contact == "sinhvien@example.com").order_by(OTPStorage.id.desc()).first()
    assert otp_record is not None
    otp_code = otp_record.otp_code
    print(f"-> Đã lấy được mã OTP từ CSDL: {otp_code}")

    print("\n--- [TEST 2] Thử đăng ký với OTP SAI (999999) ---")
    res2 = client.post("/api/auth/register", json={
        "email": "sinhvien@example.com",
        "password": "password123",
        "full_name": "Nguyễn Văn A",
        "otp_code": "999999"
    })
    print("Response status:", res2.status_code)
    print("Response JSON:", res2.json())
    assert res2.status_code == 400, f"Expected 400, got {res2.status_code}"

    print("\n--- [TEST 3] Đăng ký tài khoản với OTP ĐÚNG ---")
    res3 = client.post("/api/auth/register", json={
        "email": "sinhvien@example.com",
        "password": "password123",
        "full_name": "Nguyễn Văn A",
        "otp_code": otp_code
    })
    print("Response status:", res3.status_code)
    print("Response JSON:", res3.json())
    assert res3.status_code == 201, f"Expected 201, got {res3.status_code}"

    # Đóng session cũ và mở session mới để đồng bộ snapshot InnoDB của MySQL
    db.close()
    db = SessionLocal()

    # Kiểm tra CSDL xem 3 bảng đã có dữ liệu chưa
    user = db.query(User).filter(User.email == "sinhvien@example.com").first()
    assert user is not None
    assert user.status == "active"
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    assert profile is not None
    assert profile.full_name == "Nguyễn Văn A"

    user_role = db.query(UserRole).filter(UserRole.user_id == user.id).first()
    assert user_role is not None
    role = db.query(Role).filter(Role.id == user_role.role_id).first()
    assert role.name == "user"

    print("-> Xác nhận dữ liệu đã được lưu chuẩn xác vào cả 3 bảng Users, UserProfiles, UserRoles!")

    print("\n--- [TEST 4] Gửi lại OTP với Email ĐÃ TỒN TẠI (Kỳ vọng 409 Conflict) ---")
    res4 = client.post("/api/auth/send-otp", json={"email": "sinhvien@example.com"})
    print("Response status:", res4.status_code)
    print("Response JSON:", res4.json())
    assert res4.status_code == 409, f"Expected 409, got {res4.status_code}"

    print("\n--- [TEST 5] Thử dùng lại mã OTP cũ (Replay Attack) (Kỳ vọng 400 Bad Request) ---")
    res5 = client.post("/api/auth/register", json={
        "email": "sinhvien@example.com",
        "password": "password123",
        "full_name": "Nguyễn Văn A",
        "otp_code": otp_code
    })
    print("Response status:", res5.status_code)
    print("Response JSON:", res5.json())
    assert res5.status_code == 400, f"Expected 400, got {res5.status_code}"

    db.close()
    print("\n>>> TẤT CẢ 5 KỊCH BẢN KIỂM THỬ ĐÃ THÀNH CÔNG VƯỢT QUA (ALL TESTS PASSED)! <<<")

if __name__ == "__main__":
    run_tests()
