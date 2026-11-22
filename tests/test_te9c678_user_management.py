"""
==============================================================================
KIỂM THỬ TOÀN DIỆN TASK TE9C678: QUẢN LÝ NGƯỜI DÙNG & KHÓA/MỞ KHÓA TÀI KHOẢN
Yêu cầu nghiệp vụ: FR-14, BR-07
Các API kiểm tra:
- GET /api/admin/users: Danh sách người dùng, tìm kiếm, lọc status/role, phân trang
- PATCH /api/admin/users/{id}/status: Khóa/mở khóa tài khoản vi phạm và thu hồi phiên
==============================================================================
"""

import os
import sys
from datetime import datetime

# Đảm bảo mã hóa UTF-8 cho console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.core.security import hash_password, create_access_token
from app.models.user import User, UserProfile, Role, UserRole, RevokedToken
from app.models.search import SearchSession

client = TestClient(app)


def setup_te9c678_data():
    """Chuẩn bị dữ liệu tài khoản Admin, User bình thường và User vi phạm phục vụ kiểm thử"""
    db = SessionLocal()
    try:
        # 1. Đảm bảo Roles
        role_user = db.query(Role).filter_by(name="user").first()
        if not role_user:
            role_user = Role(name="user", description="Người dùng chuẩn")
            db.add(role_user)

        role_admin = db.query(Role).filter_by(name="admin").first()
        if not role_admin:
            role_admin = Role(name="admin", description="Quản trị viên hệ thống")
            db.add(role_admin)

        db.commit()
        db.refresh(role_user)
        db.refresh(role_admin)

        # 2. Tạo tài khoản Admin
        admin_user = db.query(User).filter_by(email="admin.te9c678@foodai.vn").first()
        if not admin_user:
            admin_user = User(
                email="admin.te9c678@foodai.vn",
                phone_number="0988776655",
                hashed_password=hash_password("admin_pass_123"),
                status="active"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            db.add(UserProfile(user_id=admin_user.id, full_name="Admin TE9C678"))
            db.add(UserRole(user_id=admin_user.id, role_id=role_admin.id))
            db.commit()

        # 3. Tạo tài khoản User bình thường
        normal_user = db.query(User).filter_by(email="user.te9c678@foodai.vn").first()
        if not normal_user:
            normal_user = User(
                email="user.te9c678@foodai.vn",
                phone_number="0911223344",
                hashed_password=hash_password("user_pass_123"),
                status="active"
            )
            db.add(normal_user)
            db.commit()
            db.refresh(normal_user)
            db.add(UserProfile(user_id=normal_user.id, full_name="Nguyễn Văn Test"))
            db.add(UserRole(user_id=normal_user.id, role_id=role_user.id))
            db.commit()

        # 4. Tạo tài khoản User vi phạm sẽ bị khóa
        violator_user = db.query(User).filter_by(email="violator.te9c678@foodai.vn").first()
        if not violator_user:
            violator_user = User(
                email="violator.te9c678@foodai.vn",
                phone_number="0977665544",
                hashed_password=hash_password("violator_pass_123"),
                status="active"
            )
            db.add(violator_user)
            db.commit()
            db.refresh(violator_user)
            db.add(UserProfile(user_id=violator_user.id, full_name="Spam Bot Vi Phạm"))
            db.add(UserRole(user_id=violator_user.id, role_id=role_user.id))
            db.commit()
        else:
            violator_user.status = "active"
            db.commit()

        # 5. Sinh JWT Token cho từng tài khoản
        admin_token = create_access_token(admin_user.id, claims={"email": admin_user.email, "role": "admin"})
        user_token = create_access_token(normal_user.id, claims={"email": normal_user.email, "role": "user"})
        violator_token = create_access_token(violator_user.id, claims={"email": violator_user.email, "role": "user"})

        return {
            "admin_user_id": admin_user.id,
            "admin_token": admin_token,
            "normal_user_id": normal_user.id,
            "user_token": user_token,
            "violator_user_id": violator_user.id,
            "violator_token": violator_token,
        }
    finally:
        db.close()


def test_te9c678_user_management_suite():
    data = setup_te9c678_data()
    admin_headers = {"Authorization": f"Bearer {data['admin_token']}"}
    user_headers = {"Authorization": f"Bearer {data['user_token']}"}
    violator_id = data["violator_user_id"]
    admin_id = data["admin_user_id"]

    print("\n--- [TEST 1] Khách vãng lai (Guest) gọi GET /api/admin/users (Kỳ vọng 401) ---")
    res1 = client.get("/api/admin/users")
    assert res1.status_code == 401
    print("-> BẢO VỆ ROUTE THÀNH CÔNG: 401 Unauthorized (Chặn khách không có token)")

    print("\n--- [TEST 2] User thường (role='user') gọi GET /api/admin/users (Kỳ vọng 403) ---")
    res2 = client.get("/api/admin/users", headers=user_headers)
    assert res2.status_code == 403
    print("-> PHÂN QUYỀN RBAC THÀNH CÔNG: 403 Forbidden (Chặn người dùng thường)")

    print("\n--- [TEST 3] Admin gọi GET /api/admin/users lấy danh sách và phân trang ---")
    res3 = client.get("/api/admin/users?page=1&limit=10", headers=admin_headers)
    assert res3.status_code == 200
    res3_json = res3.json()
    assert res3_json["status"] == "success"
    assert "data" in res3_json and "total" in res3_json
    assert "pagination" in res3_json
    users = res3_json["data"]
    assert len(users) >= 3
    sample_user = users[0]
    for field in ["id", "email", "status", "role", "roles", "full_name", "active_sessions_count"]:
        assert field in sample_user, f"Thiếu trường {field} trong response người dùng"
    print(f"-> THÀNH CÔNG: Lấy được {len(users)} người dùng kèm metadata đầy đủ (HTTP 200)")

    print("\n--- [TEST 4] Admin lọc danh sách theo status='active' và keyword='violator' ---")
    res4_filter = client.get("/api/admin/users?status=active&keyword=violator", headers=admin_headers)
    assert res4_filter.status_code == 200
    filter_data = res4_filter.json()["data"]
    assert len(filter_data) >= 1
    assert any("violator" in u["email"] for u in filter_data)
    print("-> BỘ LỌC HOẠT ĐỘNG CHUẨN XÁC: Lọc đúng tài khoản theo trạng thái và từ khóa")

    print("\n--- [TEST 5] Admin tự khóa tài khoản chính mình (Kỳ vọng 400 Bad Request) ---")
    res5_self = client.patch(
        f"/api/admin/users/{admin_id}/status",
        headers=admin_headers,
        json={"status": "locked"}
    )
    assert res5_self.status_code == 400
    assert "không thể tự khóa" in res5_self.json()["detail"].lower()
    print("-> AN TOÀN HỆ THỐNG: Ngăn chặn Quản trị viên tự khóa chính mình thành công")

    print("\n--- [TEST 6] Admin gửi trạng thái không hợp lệ (status='deleted') (Kỳ vọng 400) ---")
    res6_bad = client.patch(
        f"/api/admin/users/{violator_id}/status",
        headers=admin_headers,
        json={"status": "deleted"}
    )
    assert res6_bad.status_code == 400
    assert "chỉ chấp nhận" in res6_bad.json()["detail"].lower()
    print("-> VALIDATION BẢO VỆ: Đã chặn trạng thái sai định dạng (400 Bad Request)")

    print("\n--- [TEST 7] Admin khóa ID không tồn tại (ID=999999) (Kỳ vọng 404 Not Found) ---")
    res7_notfound = client.patch(
        "/api/admin/users/999999/status",
        headers=admin_headers,
        json={"status": "locked"}
    )
    assert res7_notfound.status_code == 404
    print("-> BẮT LỖI 404 CHUẨN: Người dùng không tồn tại trả về 404 Not Found")

    print("\n--- [TEST 8] Admin THỰC HIỆN KHÓA TÀI KHOẢN VI PHẠM & THU HỒI PHIÊN (BR-07) ---")
    # Tạo 2 phiên tìm kiếm active giả lập cho violator
    db = SessionLocal()
    s1 = SearchSession(user_id=violator_id, status="active", started_at=datetime.utcnow())
    s2 = SearchSession(user_id=violator_id, status="active", started_at=datetime.utcnow())
    db.add_all([s1, s2])
    db.commit()
    db.close()

    res8_lock = client.patch(
        f"/api/admin/users/{violator_id}/status",
        headers=admin_headers,
        json={"status": "locked", "reason": "Tài khoản spam đánh giá và vi phạm chính sách cộng đồng"}
    )
    assert res8_lock.status_code == 200
    lock_body = res8_lock.json()
    assert lock_body["new_status"] == "locked"
    assert lock_body["revoked_sessions_count"] >= 2
    assert "khóa tài khoản" in lock_body["message"].lower()

    # Kiểm tra CSDL xem 2 phiên SearchSession đã bị đóng (closed) chưa
    db = SessionLocal()
    violator_db = db.query(User).filter_by(id=violator_id).first()
    assert violator_db.status == "locked"

    active_remaining = db.query(SearchSession).filter(
        SearchSession.user_id == violator_id,
        SearchSession.status == "active"
    ).count()
    assert active_remaining == 0, f"Vẫn còn {active_remaining} phiên active chưa bị đóng!"

    revoked_tokens_count = db.query(RevokedToken).filter_by(user_id=violator_id).count()
    assert revoked_tokens_count >= 1, "Chưa lưu bản ghi thu hồi token vào bảng RevokedToken!"
    db.close()
    print("-> BR-07 THÀNH CÔNG: Tài khoản đã bị khóa, toàn bộ phiên tìm kiếm bị đóng, token bị thu hồi!")

    print("\n--- [TEST 9] Tài khoản bị khóa gọi API bảo vệ và Đăng nhập lại (Kỳ vọng 403) ---")
    # Thử gọi API bằng token đã cấp trước khi bị khóa
    violator_headers = {"Authorization": f"Bearer {data['violator_token']}"}
    res9_pref = client.get("/api/users/preferences", headers=violator_headers)
    assert res9_pref.status_code == 403
    assert "bị khóa" in res9_pref.json()["detail"].lower()
    print("-> BẢO VỆ BR-07: Token của tài khoản bị khóa bị từ chối truy cập (403 Forbidden)")

    # Thử đăng nhập lại bằng email và mật khẩu
    res9_login = client.post("/api/auth/login", json={
        "account": "violator.te9c678@foodai.vn",
        "password": "violator_pass_123"
    })
    assert res9_login.status_code == 403
    assert "bị khóa" in res9_login.json()["detail"].lower()
    print("-> BẢO VỆ BR-07: Đăng nhập bị chặn hoàn toàn (HTTP 403 Forbidden)")

    print("\n--- [TEST 10] Admin MỞ KHÓA TÀI KHOẢN (status='active') ---")
    res10_unlock = client.patch(
        f"/api/admin/users/{violator_id}/status",
        headers=admin_headers,
        json={"status": "active", "reason": "Người dùng đã cam kết không tái phạm"}
    )
    assert res10_unlock.status_code == 200
    assert res10_unlock.json()["new_status"] == "active"

    # Người dùng đăng nhập lại thành công
    res10_login = client.post("/api/auth/login", json={
        "account": "violator.te9c678@foodai.vn",
        "password": "violator_pass_123"
    })
    assert res10_login.status_code == 200
    assert "token" in res10_login.json()
    print("-> PHỤC HỒI THÀNH CÔNG: Sau khi mở khóa, người dùng có thể đăng nhập bình thường (HTTP 200)\n")

    print("==================================================================")
    print(">>> TẤT CẢ 10 CA KIỂM THỬ TASK TE9C678 (FR-14, BR-07) ĐỀU PASS 100%! <<<")
    print("==================================================================")


def test_te9c678_user_management():
    test_te9c678_user_management_suite()


if __name__ == "__main__":
    test_te9c678_user_management_suite()
