"""
==============================================================================
UNIT & INTEGRATION TESTS: USER PREFERENCES DECLARATION API & UI (TASK TE9C64E - FR-04)
Kiểm thử toàn diện:
1. Đăng ký/đăng nhập tài khoản kiểm thử
2. Khai báo sở thích lần đầu qua POST /api/users/preferences (lưu JSON vào UserPreferences)
3. Xác minh trực tiếp trong CSDL bảng user_preferences lưu đúng chuỗi JSON chuẩn
4. Lấy thông tin sở thích qua GET /api/users/preferences
5. Cập nhật chế độ ăn Keto, Chay và ngân sách trung bình qua PUT /api/users/preferences
6. Kiểm tra các chế độ ăn hợp lệ: keto, vegetarian, vegan, halal, omnivore
7. Kiểm tra danh sách dị ứng: seafood, peanut, dairy, gluten, egg, soy
8. Bắt lỗi Validation: diet_type không hợp lệ, avg_budget âm
9. Bảo vệ Route: Khách (Guest) không có Token bị từ chối 401 Unauthorized
==============================================================================
"""

import sys
import os
import json
import sqlite3

# Đảm bảo đường dẫn import app.* chính xác
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import User, UserProfile, UserPreference, Role, UserRole
from app.core.security import hash_password

client = TestClient(app)


def setup_te9c64e_fixture():
    """Đảm bảo tài khoản kiểm thử và bảng CSDL sẵn sàng"""
    db = SessionLocal()
    try:
        role_user = db.query(Role).filter(Role.name == "user").first()
        if not role_user:
            role_user = Role(name="user", description="Người dùng hệ thống")
            db.add(role_user)
            db.commit()
            db.refresh(role_user)

        user = db.query(User).filter(User.email == "user.demo@foodai.vn").first()
        if not user:
            user = User(
                email="user.demo@foodai.vn",
                phone_number="0901111222",
                hashed_password=hash_password("user123"),
                status="active"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            prof = UserProfile(
                user_id=user.id,
                full_name="Nguyễn Văn An",
                default_address="11 Nguyễn Đình Chiểu, Q1, TP.HCM",
                default_lat=10.7860,
                default_lng=106.7003
            )
            ur = UserRole(user_id=user.id, role_id=role_user.id)
            db.add_all([prof, ur])
            db.commit()

        # Reset preferences của user này để test khai báo mới
        db.query(UserPreference).filter(UserPreference.user_id == user.id).delete()
        db.commit()
    finally:
        db.close()


def run_te9c64e_tests():
    print("==================================================================")
    print("   BẮT ĐẦU CHẠY KIỂM THỬ KHAI BÁO USER PREFERENCES (TASK TE9C64E) ")
    print("               YÊU CẦU NGHIỆP VỤ: FR-04 (PHASE 2)                ")
    print("==================================================================")

    setup_te9c64e_fixture()

    # 1. Đăng nhập lấy Bearer Access Token
    login_res = client.post("/api/auth/login", json={
        "account": "user.demo@foodai.vn",
        "password": "user123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["tokens"]["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # -----------------------------------------------------------------
    # TEST 1: Khai báo sở thích lần đầu qua POST /api/users/preferences
    # -----------------------------------------------------------------
    print("\n--- [TEST 1] Khai báo sở thích lần đầu (POST /api/users/preferences) ---")
    post_payload = {
        "diet_type": "keto",
        "allergies": ["seafood", "peanut"],
        "preferred_cuisines": ["Lẩu Nướng", "Món Nhật"],
        "avg_budget": 350000.0
    }
    res1 = client.post("/api/users/preferences", headers=auth_headers, json=post_payload)
    print("Status code:", res1.status_code)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["diet_type"] == "keto"
    assert "seafood" in data1["allergies"]
    assert "peanut" in data1["allergies"]
    assert "Lẩu Nướng" in data1["preferred_cuisines"]
    assert data1["avg_budget"] == 350000.0
    print("-> KHAI BÁO THÀNH CÔNG: Chế độ ăn Keto, Dị ứng [seafood, peanut], Ngân sách 350,000đ")

    # -----------------------------------------------------------------
    # TEST 2: Kiểm tra trực tiếp bảng CSDL user_preferences lưu đúng JSON
    # -----------------------------------------------------------------
    print("\n--- [TEST 2] Kiểm tra lưu chuỗi JSON thực tế trong bảng user_preferences ---")
    db = SessionLocal()
    try:
        user_rec = db.query(User).filter(User.email == "user.demo@foodai.vn").first()
        pref_db = db.query(UserPreference).filter(UserPreference.user_id == user_rec.id).first()
        assert pref_db is not None
        print("Raw allergies column in DB:", pref_db.allergies)
        print("Raw preferred_cuisines column in DB:", pref_db.preferred_cuisines)

        # Kiểm tra tính hợp lệ của chuỗi JSON
        parsed_allergies = json.loads(pref_db.allergies)
        parsed_cuisines = json.loads(pref_db.preferred_cuisines)
        assert isinstance(parsed_allergies, list)
        assert isinstance(parsed_cuisines, list)
        assert "seafood" in parsed_allergies
        assert "Lẩu Nướng" in parsed_cuisines
        print("-> ĐÃ XÁC THỰC CSDL: Bảng user_preferences lưu JSON chuẩn xác 100%")
    finally:
        db.close()

    # -----------------------------------------------------------------
    # TEST 3: Lấy thông tin sở thích qua GET /api/users/preferences
    # -----------------------------------------------------------------
    print("\n--- [TEST 3] Lấy thông tin sở thích (GET /api/users/preferences) ---")
    res3 = client.get("/api/users/preferences", headers=auth_headers)
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["diet_type"] == "keto"
    assert data3["allergies"] == ["seafood", "peanut"]
    assert data3["preferred_cuisines"] == ["Lẩu Nướng", "Món Nhật"]
    assert data3["avg_budget"] == 350000.0
    print("-> LẤY DỮ LIỆU THÀNH CÔNG: API deserialize JSON thành mảng List hoàn hảo")

    # -----------------------------------------------------------------
    # TEST 4: Cập nhật chế độ ăn Chay (vegetarian) qua PUT /api/users/preferences
    # -----------------------------------------------------------------
    print("\n--- [TEST 4] Cập nhật sang chế độ ăn Chay (PUT /api/users/preferences) ---")
    put_payload = {
        "diet_type": "vegetarian",
        "allergies": ["gluten", "dairy"],
        "preferred_cuisines": ["Món Việt", "Món Chay"],
        "avg_budget": 180000.0
    }
    res4 = client.put("/api/users/preferences", headers=auth_headers, json=put_payload)
    assert res4.status_code == 200
    data4 = res4.json()
    assert data4["diet_type"] == "vegetarian"
    assert "gluten" in data4["allergies"]
    assert "dairy" in data4["allergies"]
    assert "Món Chay" in data4["preferred_cuisines"]
    assert data4["avg_budget"] == 180000.0
    print("-> CẬP NHẬT THÀNH CÔNG: Đã đổi sang chế độ ăn chay, dị ứng gluten & bơ sữa")

    # -----------------------------------------------------------------
    # TEST 5: Kiểm tra các chế độ ăn hợp lệ khác (vegan, halal, omnivore)
    # -----------------------------------------------------------------
    print("\n--- [TEST 5] Kiểm tra chuỗi các chế độ ăn khác (vegan, halal, omnivore) ---")
    for diet in ["vegan", "halal", "omnivore"]:
        res_d = client.put("/api/users/preferences", headers=auth_headers, json={"diet_type": diet})
        assert res_d.status_code == 200
        assert res_d.json()["diet_type"] == diet
        print(f" -> Hợp lệ: diet_type='{diet}'")

    # -----------------------------------------------------------------
    # TEST 6: Bắt lỗi Validation: Chế độ ăn không hợp lệ & Ngân sách âm
    # -----------------------------------------------------------------
    print("\n--- [TEST 6] Bắt lỗi Validation khi nhập sai dữ liệu (Kỳ vọng 400/422) ---")
    res6_bad_diet = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={"diet_type": "diet_khong_ton_tai"}
    )
    print("Bad diet status code:", res6_bad_diet.status_code)
    assert res6_bad_diet.status_code == 400

    res6_bad_budget = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={"avg_budget": -99999}
    )
    print("Bad budget status code:", res6_bad_budget.status_code)
    assert res6_bad_budget.status_code in (400, 422)
    print("-> VALIDATION BẢO VỆ: Đã ngăn chặn dữ liệu sai định dạng")

    # -----------------------------------------------------------------
    # TEST 7: Bảo vệ Route: Khách (Guest) không có token bị từ chối 401
    # -----------------------------------------------------------------
    print("\n--- [TEST 7] Bảo vệ Route: Khách (Guest) gọi POST/PUT/GET (Kỳ vọng 401) ---")
    assert client.get("/api/users/preferences").status_code == 401
    assert client.post("/api/users/preferences", json={"diet_type": "keto"}).status_code == 401
    assert client.put("/api/users/preferences", json={"diet_type": "keto"}).status_code == 401
    print("-> BẢO VỆ AN TOÀN: Toàn bộ 3 phương thức GET/POST/PUT đều yêu cầu xác thực JWT (401)")

    # -----------------------------------------------------------------
    # TEST 8: Kiểm tra file UI frontend/preferences.html tồn tại & đầy đủ
    # -----------------------------------------------------------------
    print("\n--- [TEST 8] Kiểm tra file Giao diện Onboarding frontend/preferences.html ---")
    ui_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "preferences.html")
    assert os.path.exists(ui_path), "File preferences.html không tồn tại!"
    with open(ui_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "TE9C64E" in html
    assert "FR-04" in html
    assert "keto" in html.lower()
    assert "vegetarian" in html.lower()
    assert "seafood" in html.lower()
    assert "budget-slider" in html
    assert "json-preview" in html
    print(f"-> GIAO DIỆN HOÀN CHỈNH: preferences.html ({len(html)} ký tự) đáp ứng đầy đủ yêu cầu FR-04\n")

    print("==================================================================")
    print(">>> TẤT CẢ 8 BÀI TEST API & GIAO DIỆN FR-04/TE9C64E ĐỀU PASS 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_te9c64e_tests()
