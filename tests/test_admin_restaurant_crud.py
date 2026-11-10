"""
==============================================================================
UNIT & INTEGRATION TESTS: ADMIN RESTAURANT CRUD APIS (FR-13)
Kiểm thử toàn diện:
1. POST /api/admin/restaurants: Thêm mới nhà hàng (201 Created)
2. POST /api/admin/restaurants: Bắt lỗi khoảng giá max_price < min_price (400 Bad Request)
3. GET /api/admin/restaurants/{id}: Lấy chi tiết nhà hàng (200 OK)
4. PUT /api/admin/restaurants/{id}: Cập nhật địa chỉ, GPS, giá, giờ mở cửa (200 OK)
5. PUT /api/admin/restaurants/{id}/status: Đổi trạng thái active/inactive (200 OK)
6. DELETE /api/admin/restaurants/{id}: Xóa vĩnh viễn nhà hàng (200 OK)
7. GET /api/admin/restaurants/{id}: Kiểm tra 404 sau khi đã xóa
8. RBAC Guard: Guest gọi CRUD bị từ chối 401 Unauthorized
9. RBAC Guard: User thường gọi CRUD bị từ chối 403 Forbidden
==============================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import (
    User, UserProfile, UserRole, Role, RevokedToken,
    Restaurant, RestaurantAmenity, RestaurantImage
)
from app.core.security import hash_password, create_access_token

client = TestClient(app)


def setup_auth_tokens():
    """Tạo hoặc lấy Token xác thực của Admin và User thường"""
    db = SessionLocal()
    try:
        role_admin = db.query(Role).filter(Role.name == "admin").first()
        if not role_admin:
            role_admin = Role(name="admin", description="Quản trị viên")
            db.add(role_admin)
            db.commit()

        role_user = db.query(Role).filter(Role.name == "user").first()
        if not role_user:
            role_user = Role(name="user", description="Người dùng")
            db.add(role_user)
            db.commit()

        # Admin
        admin = db.query(User).filter(User.email == "admin.crud@foodai.vn").first()
        if not admin:
            admin = User(
                email="admin.crud@foodai.vn",
                phone_number="0901234567",
                hashed_password=hash_password("AdminPass123"),
                status="active"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            db.add(UserProfile(user_id=admin.id, full_name="Admin Test CRUD"))
            db.add(UserRole(user_id=admin.id, role_id=role_admin.id))
            db.commit()

        # User
        user = db.query(User).filter(User.email == "user.normal@foodai.vn").first()
        if not user:
            user = User(
                email="user.normal@foodai.vn",
                phone_number="0907654321",
                hashed_password=hash_password("UserPass123"),
                status="active"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db.add(UserProfile(user_id=user.id, full_name="User Normal"))
            db.add(UserRole(user_id=user.id, role_id=role_user.id))
            db.commit()

        admin_token = create_access_token(admin.id, claims={"email": admin.email, "role": "admin"})
        user_token = create_access_token(user.id, claims={"email": user.email, "role": "user"})

        return admin_token, user_token
    finally:
        db.close()


def run_restaurant_crud_tests():
    print("==================================================================")
    print("   BẮT ĐẦU CHẠY KIỂM THỬ API CRUD NHÀ HÀNG DÀNH CHO ADMIN (FR-13)   ")
    print("==================================================================\n")

    admin_token, user_token = setup_auth_tokens()
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # -----------------------------------------------------------------
    # TEST 1: Thêm mới nhà hàng (POST /api/admin/restaurants)
    # -----------------------------------------------------------------
    print("--- [TEST 1] Admin thêm mới nhà hàng (POST /api/admin/restaurants) ---")
    create_payload = {
        "name": "Bếp Chay Hoa Khai",
        "description": "Không gian thanh tịnh phục vụ các món chay thuần khiết",
        "address": "45 Lê Thánh Tôn, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838221144",
        "cuisine_type": "Món Chay",
        "latitude": 10.7765,
        "longitude": 106.7009,
        "min_price": 60000,
        "max_price": 180000,
        "open_hours": "07:00 - 21:30",
        "status": "active",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True
        }
    }
    res1 = client.post("/api/admin/restaurants", headers=admin_headers, json=create_payload)
    print("Status code:", res1.status_code)
    assert res1.status_code == 201, f"Expected 201 Created, got {res1.status_code}"
    res1_data = res1.json()["data"]
    created_id = res1_data["id"]
    print(f"-> THÊM THÀNH CÔNG: ID={created_id}, Tên='{res1_data['name']}', Tọa độ=({res1_data['latitude']}, {res1_data['longitude']})\n")

    # -----------------------------------------------------------------
    # TEST 2: Bắt lỗi logic giá: max_price < min_price (400 Bad Request)
    # -----------------------------------------------------------------
    print("--- [TEST 2] Bắt lỗi max_price < min_price (Kỳ vọng 400 Bad Request) ---")
    bad_payload = {
        "name": "Quán Sai Giá",
        "address": "123 Đường Số 1, Quận 1, TP.HCM",
        "latitude": 10.77,
        "longitude": 106.70,
        "min_price": 200000,
        "max_price": 50000  # Sai logic
    }
    res2 = client.post("/api/admin/restaurants", headers=admin_headers, json=bad_payload)
    print("Status code:", res2.status_code)
    assert res2.status_code == 400
    print("Detail:", res2.json().get("detail"))
    print("-> VALIDATION CHUẨN XÁC: Đã chặn lỗi giá nghịch đảo\n")

    # -----------------------------------------------------------------
    # TEST 3: Lấy chi tiết nhà hàng vừa tạo (GET /api/admin/restaurants/{id})
    # -----------------------------------------------------------------
    print(f"--- [TEST 3] Admin xem chi tiết nhà hàng ID={created_id} (GET) ---")
    res3 = client.get(f"/api/admin/restaurants/{created_id}", headers=admin_headers)
    print("Status code:", res3.status_code)
    assert res3.status_code == 200
    detail = res3.json()["data"]
    assert detail["name"] == "Bếp Chay Hoa Khai"
    assert detail["amenities"]["vegetarian_support"] is True
    print(f"-> LẤY CHI TIẾT THÀNH CÔNG: Tiện ích món chay={detail['amenities']['vegetarian_support']}\n")

    # -----------------------------------------------------------------
    # TEST 4: Cập nhật thông tin nhà hàng (PUT /api/admin/restaurants/{id})
    # -----------------------------------------------------------------
    print(f"--- [TEST 4] Admin cập nhật địa chỉ, tọa độ GPS và đổi sang 'inactive' (PUT) ---")
    update_payload = {
        "address": "45A Lê Thánh Tôn, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "latitude": 10.7770,
        "longitude": 106.7015,
        "min_price": 70000,
        "max_price": 220000,
        "open_hours": "08:00 - 22:00",
        "status": "inactive"  # Đổi trạng thái sang inactive
    }
    res4 = client.put(f"/api/admin/restaurants/{created_id}", headers=admin_headers, json=update_payload)
    print("Status code:", res4.status_code)
    assert res4.status_code == 200
    updated_data = res4.json()["data"]
    assert updated_data["address"] == "45A Lê Thánh Tôn, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh"
    assert updated_data["latitude"] == 10.7770
    assert updated_data["status"] == "inactive"
    print(f"-> CẬP NHẬT THÀNH CÔNG: Trạng thái mới='{updated_data['status']}', Giá={updated_data['min_price']}-{updated_data['max_price']}\n")

    # -----------------------------------------------------------------
    # TEST 5: Đổi trạng thái active/inactive qua endpoint status (PUT)
    # -----------------------------------------------------------------
    print(f"--- [TEST 5] Đổi trạng thái nhà hàng ID={created_id} về 'active' ---")
    res5 = client.put(
        f"/api/admin/restaurants/{created_id}/status",
        headers=admin_headers,
        json={"status": "active"}
    )
    print("Status code:", res5.status_code)
    assert res5.status_code == 200
    assert res5.json()["new_status"] == "active"
    print("-> ĐỔI TRẠNG THÁI THÀNH CÔNG: Nhà hàng đã hoạt động trở lại\n")

    # -----------------------------------------------------------------
    # TEST 6: Xóa vĩnh viễn nhà hàng (DELETE /api/admin/restaurants/{id})
    # -----------------------------------------------------------------
    print(f"--- [TEST 6] Admin xóa vĩnh viễn nhà hàng ID={created_id} (DELETE) ---")
    res6 = client.delete(f"/api/admin/restaurants/{created_id}", headers=admin_headers)
    print("Status code:", res6.status_code)
    assert res6.status_code == 200
    print("Response message:", res6.json()["message"])
    print("-> XÓA THÀNH CÔNG: Nhà hàng đã được gỡ khỏi CSDL\n")

    # -----------------------------------------------------------------
    # TEST 7: Kiểm tra 404 Not Found sau khi đã xóa
    # -----------------------------------------------------------------
    print(f"--- [TEST 7] Kiểm tra lại nhà hàng ID={created_id} sau khi xóa (Kỳ vọng 404) ---")
    res7 = client.get(f"/api/admin/restaurants/{created_id}", headers=admin_headers)
    print("Status code:", res7.status_code)
    assert res7.status_code == 404
    print("-> XÁC NHẬN CHUẨN XÁC: 404 Not Found (Bản ghi đã không còn tồn tại)\n")

    # -----------------------------------------------------------------
    # TEST 8: Phân quyền - Guest (không có Token) gọi CRUD bị từ chối 401
    # -----------------------------------------------------------------
    print("--- [TEST 8] Guest (không có Token) gọi POST /api/admin/restaurants (Kỳ vọng 401) ---")
    res8 = client.post("/api/admin/restaurants", json=create_payload)
    print("Status code:", res8.status_code)
    assert res8.status_code == 401
    print("-> BẢO VỆ THÀNH CÔNG: 401 Unauthorized\n")

    # -----------------------------------------------------------------
    # TEST 9: Phân quyền - User thường (role='user') gọi CRUD bị từ chối 403
    # -----------------------------------------------------------------
    print("--- [TEST 9] User thường (role='user') gọi DELETE /api/admin/restaurants/1 (Kỳ vọng 403) ---")
    res9 = client.delete("/api/admin/restaurants/1", headers=user_headers)
    print("Status code:", res9.status_code)
    assert res9.status_code == 403
    print("Detail:", res9.json().get("detail"))
    print("-> BẢO VỆ THÀNH CÔNG: 403 Forbidden\n")

    print("==================================================================")
    print(">>> TẤT CẢ 9 BÀI TEST CRUD NHÀ HÀNG DÀNH CHO ADMIN ĐỀU PASS 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_restaurant_crud_tests()
