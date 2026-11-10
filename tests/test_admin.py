"""
==============================================================================
UNIT & INTEGRATION TESTS: ADMIN PORTAL & ROUTE PROTECTION (TASK TE9C656)
Kiểm thử toàn diện:
1. Bảo vệ Route Admin: Guest truy cập bị từ chối (401 Unauthorized)
2. Bảo vệ Route Admin: User thường truy cập bị từ chối (403 Forbidden)
3. Bảo vệ Route Admin: Admin truy cập thành công (200 OK)
4. Admin lấy thống kê Dashboard KPI (GET /api/admin/stats)
5. Admin quản lý người dùng (GET /api/admin/users)
6. Admin thực hiện nghiệp vụ BR-07: Khóa tài khoản người dùng vi phạm
7. Kiểm tra người dùng bị khóa không thể đăng nhập (BR-07)
8. Admin mở khóa tài khoản người dùng (BR-07)
9. Admin quản lý nhà hàng: Thay đổi trạng thái hiển thị (PUT /api/admin/restaurants/{id}/status)
10. Admin quản lý & xử lý báo cáo vi phạm (GET & PUT /api/admin/reports)
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
    User, UserProfile, UserRole, Role, OTPStorage, RevokedToken,
    Restaurant, RestaurantAmenity
)
from app.core.security import hash_password, create_access_token

client = TestClient(app)


def setup_test_users_and_data():
    """Tạo dữ liệu người dùng User thường, Admin và Nhà hàng mẫu để kiểm thử"""
    db = SessionLocal()
    try:
        # Dọn dẹp dữ liệu cũ nếu có
        db.query(RevokedToken).delete()
        db.query(UserRole).delete()
        db.query(UserProfile).delete()
        db.query(User).delete()
        db.query(Role).delete()
        db.commit()

        # Tạo 2 Role: 'user' và 'admin'
        role_user = Role(name="user", description="Người dùng thông thường")
        role_admin = Role(name="admin", description="Quản trị viên hệ thống")
        db.add_all([role_user, role_admin])
        db.commit()

        # 1. Tạo tài khoản User thường
        normal_user = User(
            email="user.test@foodai.vn",
            phone_number="0901111222",
            hashed_password=hash_password("UserPass123"),
            status="active"
        )
        db.add(normal_user)
        db.commit()
        db.refresh(normal_user)

        user_prof = UserProfile(
            user_id=normal_user.id,
            full_name="Nguyễn Văn User",
            default_address="Quận 1, TP.HCM"
        )
        user_role = UserRole(user_id=normal_user.id, role_id=role_user.id)
        db.add_all([user_prof, user_role])

        # 2. Tạo tài khoản Quản trị viên (Admin)
        admin_user = User(
            email="admin.master@foodai.vn",
            phone_number="0909999888",
            hashed_password=hash_password("AdminPass123"),
            status="active"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        admin_prof = UserProfile(
            user_id=admin_user.id,
            full_name="Lê Quản Trị Viên",
            default_address="TP. Hồ Chí Minh"
        )
        admin_role = UserRole(user_id=admin_user.id, role_id=role_admin.id)
        db.add_all([admin_prof, admin_role])

        # 3. Đảm bảo có ít nhất 1 nhà hàng trong CSDL
        restaurant = db.query(Restaurant).first()
        if not restaurant:
            restaurant = Restaurant(
                name="Pizza 4Ps Ben Thanh",
                address="8 Thu Khoa Huan, Q1, TP.HCM",
                latitude=10.7725,
                longitude=106.6980,
                min_price=150000,
                max_price=450000,
                status="active"
            )
            db.add(restaurant)

        db.commit()

        # Tạo Access Tokens
        user_token = create_access_token(normal_user.id, claims={"email": normal_user.email, "role": "user"})
        admin_token = create_access_token(admin_user.id, claims={"email": admin_user.email, "role": "admin"})

        return {
            "normal_user_id": normal_user.id,
            "admin_user_id": admin_user.id,
            "user_token": user_token,
            "admin_token": admin_token,
            "restaurant_id": restaurant.id
        }
    finally:
        db.close()


def run_admin_portal_tests():
    print("==================================================================")
    print("  BẮT ĐẦU CHẠY KIỂM THỬ ROUTE ADMIN PORTAL & RBAC GUARD (TE9C656)  ")
    print("==================================================================\n")

    data = setup_test_users_and_data()
    user_token = data["user_token"]
    admin_token = data["admin_token"]
    normal_user_id = data["normal_user_id"]
    restaurant_id = data["restaurant_id"]

    # -----------------------------------------------------------------
    # TEST 1: Khách (Guest) không có token truy cập route Admin
    # -----------------------------------------------------------------
    print("--- [TEST 1] Guest (không có Token) truy cập GET /api/admin/stats ---")
    res1 = client.get("/api/admin/stats")
    print("Status code:", res1.status_code)
    assert res1.status_code == 401, f"Expected 401 Unauthorized, got {res1.status_code}"
    print("-> ĐÃ CHẶN THÀNH CÔNG: 401 Unauthorized (Chặn truy cập khách trái phép)\n")

    # -----------------------------------------------------------------
    # TEST 2: User thông thường (role='user') cố truy cập route Admin
    # -----------------------------------------------------------------
    print("--- [TEST 2] User thường (role='user') truy cập GET /api/admin/stats ---")
    res2 = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    print("Status code:", res2.status_code)
    assert res2.status_code == 403, f"Expected 403 Forbidden, got {res2.status_code}"
    print("Detail:", res2.json().get("detail"))
    print("-> ĐÃ CHẶN THÀNH CÔNG: 403 Forbidden (Người dùng không đủ thẩm quyền Admin)\n")

    # -----------------------------------------------------------------
    # TEST 3: Admin hợp lệ truy cập Dashboard Stats
    # -----------------------------------------------------------------
    print("--- [TEST 3] Admin hợp lệ truy cập GET /api/admin/stats ---")
    res3 = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print("Status code:", res3.status_code)
    assert res3.status_code == 200, f"Expected 200 OK, got {res3.status_code}"
    stats_data = res3.json()["data"]
    print("KPIs:", stats_data["users"], stats_data["restaurants"])
    assert "users" in stats_data
    assert "restaurants" in stats_data
    print("-> TRUY CẬP THÀNH CÔNG: Đã nạp số liệu KPI Dashboard\n")

    # -----------------------------------------------------------------
    # TEST 4: Admin lấy danh sách người dùng
    # -----------------------------------------------------------------
    print("--- [TEST 4] Admin lấy danh sách người dùng GET /api/admin/users ---")
    res4 = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print("Status code:", res4.status_code)
    assert res4.status_code == 200
    users_list = res4.json()["data"]
    print(f"Tổng số người dùng nạp được: {len(users_list)}")
    assert len(users_list) >= 2
    print("-> THÀNH CÔNG: Danh sách người dùng hiển thị đầy đủ thông tin profile & role\n")

    # -----------------------------------------------------------------
    # TEST 5: Admin thực hiện BR-07: Khóa tài khoản người dùng vi phạm
    # -----------------------------------------------------------------
    print(f"--- [TEST 5] Admin khóa tài khoản user #{normal_user_id} (BR-07) ---")
    res5 = client.put(
        f"/api/admin/users/{normal_user_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "locked"}
    )
    print("Status code:", res5.status_code)
    assert res5.status_code == 200
    print("Response message:", res5.json()["message"])
    assert res5.json()["new_status"] == "locked"
    print("-> THÀNH CÔNG: Tài khoản người dùng đã được chuyển sang trạng thái 'locked' (BR-07)\n")

    # -----------------------------------------------------------------
    # TEST 6: Tài khoản vừa bị khóa thử đăng nhập (Kiểm tra BR-07)
    # -----------------------------------------------------------------
    print("--- [TEST 6] Người dùng bị khóa thử đăng nhập POST /api/auth/login ---")
    res6 = client.post(
        "/api/auth/login",
        json={"account": "user.test@foodai.vn", "password": "UserPass123"}
    )
    print("Status code:", res6.status_code)
    assert res6.status_code == 403
    print("Detail:", res6.json().get("detail"))
    print("-> BR-07 HOẠT ĐỘNG CHUẨN XÁC: Tài khoản bị khóa bị từ chối đăng nhập ngay lập tức\n")

    # -----------------------------------------------------------------
    # TEST 7: Admin mở khóa tài khoản người dùng (status = 'active')
    # -----------------------------------------------------------------
    print(f"--- [TEST 7] Admin mở khóa tài khoản user #{normal_user_id} ---")
    res7 = client.put(
        f"/api/admin/users/{normal_user_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "active"}
    )
    print("Status code:", res7.status_code)
    assert res7.status_code == 200
    assert res7.json()["new_status"] == "active"
    print("-> THÀNH CÔNG: Tài khoản đã được phục hồi trạng thái 'active'\n")

    # -----------------------------------------------------------------
    # TEST 8: Admin không được phép tự khóa tài khoản của chính mình
    # -----------------------------------------------------------------
    print(f"--- [TEST 8] Admin tự khóa tài khoản của chính mình (Kỳ vọng 400 Bad Request) ---")
    admin_id = data["admin_user_id"]
    res8 = client.put(
        f"/api/admin/users/{admin_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "locked"}
    )
    print("Status code:", res8.status_code)
    assert res8.status_code == 400
    print("Detail:", res8.json().get("detail"))
    print("-> BẢO VỆ AN TOÀN: Hệ thống ngăn chặn Quản trị viên tự khóa chính mình\n")

    # -----------------------------------------------------------------
    # TEST 9: Admin quản lý nhà hàng: Thay đổi trạng thái hiển thị
    # -----------------------------------------------------------------
    print(f"--- [TEST 9] Admin cập nhật trạng thái nhà hàng #{restaurant_id} sang 'hidden' ---")
    res9 = client.put(
        f"/api/admin/restaurants/{restaurant_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "hidden"}
    )
    print("Status code:", res9.status_code)
    assert res9.status_code == 200
    assert res9.json()["new_status"] == "hidden"
    print("-> THÀNH CÔNG: Đã ẩn nhà hàng khỏi giao diện công khai\n")

    # -----------------------------------------------------------------
    # TEST 10: Admin xem và xử lý danh sách Báo cáo & Khiếu nại
    # -----------------------------------------------------------------
    print("--- [TEST 10] Admin xem và xử lý báo cáo vi phạm ---")
    res10_get = client.get(
        "/api/admin/reports",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res10_get.status_code == 200
    reports = res10_get.json()["data"]
    print(f"Tổng số báo cáo đang có: {len(reports)}")

    res10_put = client.put(
        "/api/admin/reports/1/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "resolved", "admin_note": "Đã cập nhật lại bảng giá chính xác"}
    )
    assert res10_put.status_code == 200
    assert res10_put.json()["data"]["status"] == "resolved"
    print("-> THÀNH CÔNG: Đã xử lý và cập nhật ghi chú giải quyết báo cáo\n")

    print("==================================================================")
    print(">>> TẤT CẢ 10 BÀI KIỂM THỬ ROUTE ADMIN ĐỀU PASS THÀNH CÔNG 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_admin_portal_tests()
