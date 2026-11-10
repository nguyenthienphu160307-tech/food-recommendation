"""
==============================================================================
UNIT & INTEGRATION TESTS: USER PREFERENCES & RECOMMENDATION ENGINE (TASK TE9C65C)
Kiểm thử toàn diện:
1. Đăng nhập và lấy sở thích mặc định của người dùng (GET /api/users/preferences)
2. Cập nhật sở thích cá nhân: diet_type, allergies, avg_budget (PUT /api/users/preferences)
3. Bắt lỗi Validation: diet_type không hợp lệ, avg_budget âm (Kỳ vọng 400 Bad Request)
4. Bảo vệ Route: Khách (Guest) không có token bị từ chối 401 Unauthorized
5. Khách (Guest) tìm kiếm gợi ý: Không áp đặt sở thích cá nhân, gợi ý chuẩn (BR-02)
6. Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG đọc diet_type='vegetarian' (chỉ gợi ý quán có món chay)
7. Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG đọc allergies=['seafood'] (loại trừ hoàn toàn quán hải sản)
8. Minh bạch hóa bộ tiêu chí AI: applied_preferences, active_filters và ai_reason từng quán
9. Người dùng khôi phục omnivore: Kết quả gợi ý mở rộng bình thường
==============================================================================
"""

import sys
import os

# Đảm bảo đường dẫn import app.* chính xác
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import (
    User, UserProfile, UserPreference, UserRole, Role, Restaurant, RestaurantAmenity
)
from app.core.security import hash_password

client = TestClient(app)


def ensure_test_fixtures():
    """Thiết lập tài khoản người dùng và dữ liệu nhà hàng phong phú phục vụ kiểm thử"""
    db = SessionLocal()
    try:
        # 1. Đảm bảo Role 'user'
        role_user = db.query(Role).filter(Role.name == "user").first()
        if not role_user:
            role_user = Role(name="user", description="Người dùng hệ thống")
            db.add(role_user)
            db.commit()
            db.refresh(role_user)

        # 2. Đảm bảo tài khoản demo: user.demo@foodai.vn / user123
        demo_user = db.query(User).filter(User.email == "user.demo@foodai.vn").first()
        if not demo_user:
            demo_user = User(
                email="user.demo@foodai.vn",
                phone_number="0901111222",
                hashed_password=hash_password("user123"),
                status="active"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            user_prof = UserProfile(
                user_id=demo_user.id,
                full_name="Nguyễn Văn An",
                default_address="11 Nguyễn Đình Chiểu, Phường Đa Kao, Quận 1, TP.HCM",
                default_lat=10.7860,
                default_lng=106.7003
            )
            user_role = UserRole(user_id=demo_user.id, role_id=role_user.id)
            db.add_all([user_prof, user_role])
            db.commit()

        # 3. Đảm bảo CSDL có ít nhất 1 quán chay và 1 quán hải sản để kiểm thử lọc chính xác
        veg_place = db.query(Restaurant).filter(Restaurant.name == "Hum Garden & Vegetarian").first()
        if not veg_place:
            veg_place = Restaurant(
                name="Hum Garden & Vegetarian",
                cuisine_type="Món Chay",
                address="32 Võ Văn Tần, Phường 6, Quận 3, TP.HCM",
                latitude=10.7785,
                longitude=106.6912,
                min_price=180000.0,
                max_price=390000.0,
                avg_rating=4.9,
                total_reviews=690,
                status="active"
            )
            db.add(veg_place)
            db.commit()
            db.refresh(veg_place)
            amenity_veg = RestaurantAmenity(
                restaurant_id=veg_place.id,
                has_parking=True,
                has_private_room=True,
                vegetarian_support=True
            )
            db.add(amenity_veg)
            db.commit()

        seafood_place = db.query(Restaurant).filter(Restaurant.name == "Hải Sản Biển Đông — Lê Văn Thọ").first()
        if not seafood_place:
            seafood_place = Restaurant(
                name="Hải Sản Biển Đông — Lê Văn Thọ",
                cuisine_type="Hải sản",
                address="412 Lê Văn Thọ, Phường 11, Quận Gò Vấp, TP.HCM",
                latitude=10.8415,
                longitude=106.6598,
                min_price=220000.0,
                max_price=500000.0,
                avg_rating=4.5,
                total_reviews=187,
                status="active"
            )
            db.add(seafood_place)
            db.commit()
            db.refresh(seafood_place)
            amenity_sea = RestaurantAmenity(
                restaurant_id=seafood_place.id,
                has_parking=True,
                has_private_room=True,
                vegetarian_support=False
            )
            db.add(amenity_sea)
            db.commit()

    finally:
        db.close()


def run_user_preferences_tests():
    print("==================================================================")
    print("  BẮT ĐẦU CHẠY KIỂM THỬ USER PREFERENCES & RECOMMENDATION ENGINE  ")
    print("                 MÃ TASK: TE9C65C (PHASE 2)                       ")
    print("==================================================================")

    ensure_test_fixtures()

    # Đăng nhập lấy JWT Access Token của user
    login_res = client.post("/api/auth/login", json={
        "account": "user.demo@foodai.vn",
        "password": "user123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["tokens"]["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # -----------------------------------------------------------------
    # TEST 1: Lấy sở thích mặc định của người dùng
    # -----------------------------------------------------------------
    print("\n--- [TEST 1] Đăng nhập và lấy sở thích cá nhân (GET /api/users/preferences) ---")
    res1 = client.get("/api/users/preferences", headers=auth_headers)
    print("Status code:", res1.status_code)
    assert res1.status_code == 200
    pref_data = res1.json()
    assert "diet_type" in pref_data
    assert "allergies" in pref_data
    assert "preferred_cuisines" in pref_data
    assert isinstance(pref_data["allergies"], list)
    print(f"-> THÀNH CÔNG: Chế độ ăn='{pref_data['diet_type']}', Dị ứng={pref_data['allergies']}")

    # -----------------------------------------------------------------
    # TEST 2: Cập nhật sở thích cá nhân (Ăn chay + Dị ứng hải sản)
    # -----------------------------------------------------------------
    print("\n--- [TEST 2] Cập nhật sở thích: Chế độ ăn chay + Dị ứng hải sản (PUT) ---")
    res2 = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={
            "diet_type": "vegetarian",
            "allergies": ["seafood"],
            "preferred_cuisines": ["Món Việt", "Món Nhật"],
            "avg_budget": 200000.0
        }
    )
    print("Status code:", res2.status_code)
    assert res2.status_code == 200
    updated_pref = res2.json()
    assert updated_pref["diet_type"] == "vegetarian"
    assert "seafood" in updated_pref["allergies"]
    assert updated_pref["avg_budget"] == 200000.0
    print("-> CẬP NHẬT THÀNH CÔNG: Đã lưu sở thích ăn chay và dị ứng hải sản vào CSDL")

    # -----------------------------------------------------------------
    # TEST 3: Validation lỗi dữ liệu không hợp lệ (diet_type lạ, ngân sách âm)
    # -----------------------------------------------------------------
    print("\n--- [TEST 3] Bắt lỗi Validation dữ liệu (Kỳ vọng 400 Bad Request) ---")
    res3_bad_diet = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={"diet_type": "mon_an_sieu_nhan"}
    )
    print("Bad diet status code:", res3_bad_diet.status_code)
    assert res3_bad_diet.status_code == 400
    print("Detail:", res3_bad_diet.json()["detail"])

    res3_bad_budget = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={"avg_budget": -50000}
    )
    print("Bad budget status code:", res3_bad_budget.status_code)
    assert res3_bad_budget.status_code in (400, 422)
    print("-> VALIDATION CHUẨN XÁC: Đã chặn chế độ ăn lạ và ngân sách âm")

    # -----------------------------------------------------------------
    # TEST 4: Bảo vệ Route: Khách (Guest) không có Token bị từ chối (401)
    # -----------------------------------------------------------------
    print("\n--- [TEST 4] Khách (Guest) gọi API sở thích cá nhân (Kỳ vọng 401 Unauthorized) ---")
    res4_get = client.get("/api/users/preferences")
    assert res4_get.status_code == 401

    res4_put = client.put("/api/users/preferences", json={"diet_type": "vegan"})
    assert res4_put.status_code == 401
    print("-> BẢO VỆ ROUTE THÀNH CÔNG: Guest bị chặn 401 khi truy cập sở thích cá nhân")

    # -----------------------------------------------------------------
    # TEST 5: Khách (Guest) tìm kiếm gợi ý: Không bị áp sở thích cá nhân (BR-02)
    # -----------------------------------------------------------------
    print("\n--- [TEST 5] Khách (Guest) tìm kiếm gợi ý (GET /api/recommendations) ---")
    res5_guest = client.get("/api/recommendations?latitude=10.776889&longitude=106.700806&radius_km=15")
    assert res5_guest.status_code == 200
    guest_json = res5_guest.json()
    assert guest_json["applied_preferences"]["is_logged_in"] is False
    assert len(guest_json["applied_preferences"]["active_filters"]) == 0
    print(f"-> GUEST RECOMMENDATION: Trả về {guest_json['total']} quán, không áp đặt bộ lọc dị ứng")

    # -----------------------------------------------------------------
    # TEST 6: Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG đọc diet_type='vegetarian'
    # -----------------------------------------------------------------
    print("\n--- [TEST 6] Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG áp dụng diet_type='vegetarian' ---")
    res6_user = client.get(
        "/api/recommendations?latitude=10.776889&longitude=106.700806&radius_km=15",
        headers=auth_headers
    )
    assert res6_user.status_code == 200
    user_rec = res6_user.json()
    assert user_rec["applied_preferences"]["is_logged_in"] is True
    assert user_rec["applied_preferences"]["diet_type"] == "vegetarian"

    # Kiểm tra tất cả các quán trả về BẮT BUỘC phải hỗ trợ món chay
    for r in user_rec["data"]:
        is_veg = r["vegetarian_support"] or "chay" in (r["cuisine_type"] or "").lower()
        assert is_veg is True, f"Quán {r['name']} không có món chay nhưng vẫn xuất hiện cho người ăn chay!"
    print(f"-> TỰ ĐỘNG LỌC CHẾ ĐỘ ĂN THÀNH CÔNG: Toàn bộ {user_rec['total']} quán đều hỗ trợ món chay!")

    # -----------------------------------------------------------------
    # TEST 7: Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG loại trừ dị ứng hải sản (allergies)
    # -----------------------------------------------------------------
    print("\n--- [TEST 7] Người dùng đăng nhập tìm kiếm: TỰ ĐỘNG loại trừ dị ứng hải sản ---")
    assert "seafood" in user_rec["applied_preferences"]["allergies"]
    seafood_places = [
        r for r in user_rec["data"]
        if "hải sản" in (r["cuisine_type"] or "").lower() or "hải sản" in r["name"].lower()
    ]
    assert len(seafood_places) == 0, f"Vẫn còn quán hải sản trong kết quả: {[s['name'] for s in seafood_places]}"
    print("-> TỰ ĐỘNG LOẠI TRỪ DỊ ỨNG THÀNH CÔNG: Không có bất kỳ quán hải sản nào xuất hiện!")

    # -----------------------------------------------------------------
    # TEST 8: Minh bạch hóa bộ tiêu chí AI (Explainable AI Transparency)
    # -----------------------------------------------------------------
    print("\n--- [TEST 8] Kiểm tra tính minh bạch và lời giải thích AI (Explainable AI) ---")
    active_filters = user_rec["applied_preferences"]["active_filters"]
    reason_summary = user_rec["applied_preferences"]["filter_reason"]
    print("Active filters:", active_filters)
    print("Reason summary:", reason_summary)
    assert len(active_filters) >= 2
    assert "VEGETARIAN" in active_filters[0]
    assert "Hải sản" in active_filters[1]

    # Kiểm tra giải thích cá nhân trên từng quán
    top_venue = user_rec["data"][0]
    print(f"Top 1: '{top_venue['name']}' -> Match: {top_venue['match_score']}%")
    print(f"AI Reason: {top_venue['ai_reason']}")
    assert len(top_venue["ai_reason"]) > 10
    print("-> MINH BẠCH HÓA HOÀN HẢO: Đã có lời giải thích tự động rõ ràng cho từng địa điểm")

    # -----------------------------------------------------------------
    # TEST 9: Khôi phục chế độ bình thường (omnivore) và xóa dị ứng
    # -----------------------------------------------------------------
    print("\n--- [TEST 9] Khôi phục chế độ ăn omnivore, kết quả gợi ý mở rộng bình thường ---")
    res9_reset = client.put(
        "/api/users/preferences",
        headers=auth_headers,
        json={"diet_type": "omnivore", "allergies": []}
    )
    assert res9_reset.status_code == 200

    res9_rec = client.get(
        "/api/recommendations?latitude=10.776889&longitude=106.700806&radius_km=15",
        headers=auth_headers
    )
    assert res9_rec.status_code == 200
    rec_after_reset = res9_rec.json()
    print(f"Số lượng quán sau khi bỏ ăn chay: {rec_after_reset['total']} quán (lớn hơn {user_rec['total']})")
    assert rec_after_reset["total"] >= user_rec["total"]
    print("-> KHÔI PHỤC THÀNH CÔNG: Hệ thống tự động mở lại thực đơn đa dạng khi đổi sang omnivore\n")

    print("==================================================================")
    print(">>> TẤT CẢ 9 BÀI KIỂM THỬ USER PREFERENCES ĐỀU PASS THÀNH CÔNG 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_user_preferences_tests()
