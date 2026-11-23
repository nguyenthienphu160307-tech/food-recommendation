"""
Bộ kiểm thử tự động toàn diện cho Task TE9C67E (FR-15, UC-06e):
Xây dựng API Thống kê & Báo cáo cho Admin Dashboard.
Mô tả:
Thống kê tổng số người dùng, tổng nhà hàng, số lượt tìm kiếm AI theo ngày,
top loại ẩm thực được tìm nhiều nhất và top nhà hàng được yêu thích.

Danh sách 12 Ca Kiểm thử:
1. TEST 01: Guest chưa có Token gọi GET /api/admin/dashboard/stats -> Bị chặn 401 Unauthorized
2. TEST 02: User thường gọi GET /api/admin/dashboard/stats -> Bị chặn 403 Forbidden (RBAC)
3. TEST 03: Admin bị khóa (status='locked') gọi API -> Bị chặn 403 Forbidden (BR-07)
4. TEST 04: Admin hợp lệ gọi GET /api/admin/dashboard/stats -> Trả về 200 OK và đúng cấu trúc Schema
5. TEST 05: Kiểm tra tính tương thích ngược với route GET /api/admin/stats -> 200 OK
6. TEST 06: Kiểm tra số liệu Người dùng (total, active, locked, new_this_week)
7. TEST 07: Kiểm tra số liệu Nhà hàng (total, active, hidden, avg_rating)
8. TEST 08: Kiểm tra số lượt tìm kiếm AI theo ngày mặc định (7 ngày liên tục, đúng định dạng YYYY-MM-DD)
9. TEST 09: Kiểm tra tham số tùy biến `days` (days=3, days=14) và tổng số tìm kiếm trong kỳ
10. TEST 10: Kiểm tra Top loại ẩm thực được tìm nhiều nhất (xếp giảm dần theo lượt tìm, tính đúng tỷ lệ %)
11. TEST 11: Kiểm tra Top nhà hàng được yêu thích nhất từ UserFavorites (xếp theo favorite_count giảm dần)
12. TEST 12: Kiểm tra trường hợp biên (DB rỗng không có lượt tìm kiếm hay yêu thích nào) -> 0 và mảng rỗng []
"""

import sys
import os
from datetime import datetime, timedelta

# Đảm bảo import thư mục gốc
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
import app.models
from app.models.user import User, UserProfile, Role, UserRole
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.models.search import SearchSession, SearchCriteria
from app.models.interaction import UserFavorite
from app.core.security import create_access_token
from app.main import app

# Cấu hình SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def run_tests():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TE9C67E: API THỐNG KÊ & BÁO CÁO ADMIN DASHBOARD")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    app.dependency_overrides[get_db] = lambda: db

    passed_count = 0

    # 1. Khởi tạo Roles
    role_admin = Role(name="admin", description="Quản trị viên")
    role_user = Role(name="user", description="Người dùng thường")
    db.add_all([role_admin, role_user])
    db.commit()
    db.refresh(role_admin)
    db.refresh(role_user)

    # 2. Khởi tạo Users
    admin_user = User(
        email="admin_stats@smartdining.vn",
        phone_number="0909000001",
        hashed_password="hashed_pass_admin",
        status="active"
    )
    regular_user = User(
        email="user_stats@smartdining.vn",
        phone_number="0909000002",
        hashed_password="hashed_pass_user",
        status="active"
    )
    locked_admin = User(
        email="locked_admin_stats@smartdining.vn",
        phone_number="0909000003",
        hashed_password="hashed_pass_locked",
        status="locked"
    )
    locked_user = User(
        email="locked_user_stats@smartdining.vn",
        phone_number="0909000004",
        hashed_password="hashed_pass_locked_user",
        status="locked"
    )
    db.add_all([admin_user, regular_user, locked_admin, locked_user])
    db.commit()

    db.add_all([
        UserRole(user_id=admin_user.id, role_id=role_admin.id),
        UserRole(user_id=regular_user.id, role_id=role_user.id),
        UserRole(user_id=locked_admin.id, role_id=role_admin.id),
        UserRole(user_id=locked_user.id, role_id=role_user.id),
    ])
    db.commit()

    admin_profile = UserProfile(user_id=admin_user.id, full_name="Super Admin Stats")
    db.add(admin_profile)
    db.commit()

    # 3. Khởi tạo Restaurants
    r1 = Restaurant(
        name="Quán Cơm Tấm Sài Gòn 1",
        address="123 Đinh Tiên Hoàng, Quận 1, TP.HCM",
        cuisine_type="Cơm tấm",
        latitude=10.789,
        longitude=106.701,
        avg_rating=4.8,
        status="active"
    )
    r2 = Restaurant(
        name="Nhà hàng BBQ Hàn Quốc Seoul",
        address="456 Lê Thánh Tôn, Quận 1, TP.HCM",
        cuisine_type="BBQ Hàn Quốc",
        latitude=10.778,
        longitude=106.702,
        avg_rating=4.6,
        status="active"
    )
    r3 = Restaurant(
        name="Ẩm Thực Chay Hương Sen",
        address="789 Võ Văn Tần, Quận 3, TP.HCM",
        cuisine_type="Món Chay",
        latitude=10.774,
        longitude=106.689,
        avg_rating=4.9,
        status="active"
    )
    r4 = Restaurant(
        name="Quán Bún Bò Cũ Đã Đóng",
        address="102 Pasteur, Quận 1, TP.HCM",
        cuisine_type="Món Việt",
        latitude=10.776,
        longitude=106.698,
        avg_rating=3.5,
        status="hidden"
    )
    db.add_all([r1, r2, r3, r4])
    db.commit()
    db.refresh(r1)
    db.refresh(r2)
    db.refresh(r3)
    db.refresh(r4)

    # Thêm ảnh bìa cho nhà hàng
    img1 = RestaurantImage(restaurant_id=r1.id, image_url="https://img.foodai.vn/comtam.jpg", is_cover=True)
    img2 = RestaurantImage(restaurant_id=r2.id, image_url="https://img.foodai.vn/bbq.jpg", is_cover=True)
    img3 = RestaurantImage(restaurant_id=r3.id, image_url="https://img.foodai.vn/chay.jpg", is_cover=True)
    db.add_all([img1, img2, img3])
    db.commit()

    # 4. Khởi tạo Lịch sử tìm kiếm AI & Tiêu chí
    now = datetime.utcnow()
    # Hôm nay: 3 lượt
    s1 = SearchSession(started_at=now, status="closed")
    s2 = SearchSession(started_at=now, status="active")
    s3 = SearchSession(started_at=now, status="closed")
    # Hôm qua: 2 lượt
    yesterday = now - timedelta(days=1)
    s4 = SearchSession(started_at=yesterday, status="closed")
    s5 = SearchSession(started_at=yesterday, status="closed")
    # 3 ngày trước: 1 lượt
    three_days_ago = now - timedelta(days=3)
    s6 = SearchSession(started_at=three_days_ago, status="closed")
    db.add_all([s1, s2, s3, s4, s5, s6])
    db.commit()
    db.refresh(s1)
    db.refresh(s2)
    db.refresh(s3)
    db.refresh(s4)
    db.refresh(s5)
    db.refresh(s6)

    # Tiêu chí ẩm thực: BBQ Hàn Quốc (3 lần), Cơm tấm (2 lần), Món Chay (1 lần)
    c1 = SearchCriteria(session_id=s1.session_id, cuisine="BBQ Hàn Quốc")
    c2 = SearchCriteria(session_id=s2.session_id, cuisine="BBQ Hàn Quốc")
    c3 = SearchCriteria(session_id=s3.session_id, cuisine="BBQ Hàn Quốc")
    c4 = SearchCriteria(session_id=s4.session_id, cuisine="Cơm tấm")
    c5 = SearchCriteria(session_id=s5.session_id, cuisine="Cơm tấm")
    c6 = SearchCriteria(session_id=s6.session_id, cuisine="Món Chay")
    db.add_all([c1, c2, c3, c4, c5, c6])
    db.commit()

    # 5. Khởi tạo Bookmark Yêu thích:
    # r2 có 2 lượt yêu thích (admin, regular_user)
    # r1 có 1 lượt yêu thích (admin)
    # r3 có 0 lượt yêu thích
    fav1 = UserFavorite(user_id=admin_user.id, restaurant_id=r2.id)
    fav2 = UserFavorite(user_id=regular_user.id, restaurant_id=r2.id)
    fav3 = UserFavorite(user_id=admin_user.id, restaurant_id=r1.id)
    db.add_all([fav1, fav2, fav3])
    db.commit()

    # Tạo JWT Tokens
    token_admin = create_access_token(admin_user.id)
    token_user = create_access_token(regular_user.id)
    token_locked_admin = create_access_token(locked_admin.id)

    client = TestClient(app)

    # =========================================================================
    # TEST 01: Guest chưa có Token -> 401 Unauthorized
    # =========================================================================
    print("\n[TEST 01] Guest chưa có Token gọi GET /api/admin/dashboard/stats...")
    res = client.get("/api/admin/dashboard/stats")
    assert res.status_code == 401, f"Kỳ vọng 401, nhận: {res.status_code}"
    print("✓ PASS: Bị từ chối 401 Unauthorized đúng quy tắc xác thực.")
    passed_count += 1

    # =========================================================================
    # TEST 02: User thường -> 403 Forbidden (RBAC)
    # =========================================================================
    print("\n[TEST 02] User thường gọi GET /api/admin/dashboard/stats...")
    res = client.get("/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {token_user}"})
    assert res.status_code == 403, f"Kỳ vọng 403, nhận: {res.status_code}"
    assert "Admin" in res.json().get("detail", ""), "Phải có thông báo từ chối quyền Admin"
    print("✓ PASS: User thường bị chặn 403 Forbidden chuẩn xác theo RBAC.")
    passed_count += 1

    # =========================================================================
    # TEST 03: Admin bị khóa -> 403 Forbidden (BR-07)
    # =========================================================================
    print("\n[TEST 03] Admin bị khóa (status='locked') gọi API...")
    res = client.get("/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {token_locked_admin}"})
    assert res.status_code == 403, f"Kỳ vọng 403, nhận: {res.status_code}"
    assert "BR-07" in res.json().get("detail", ""), "Phải báo tài khoản bị khóa theo BR-07"
    print("✓ PASS: Tài khoản Admin bị khóa không được phép truy cập theo BR-07.")
    passed_count += 1

    # =========================================================================
    # TEST 04: Admin hợp lệ gọi GET /api/admin/dashboard/stats -> 200 OK
    # =========================================================================
    print("\n[TEST 04] Admin hợp lệ gọi GET /api/admin/dashboard/stats...")
    res = client.get("/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {token_admin}"})
    assert res.status_code == 200, f"Kỳ vọng 200, nhận: {res.status_code}"
    data = res.json()["data"]
    assert "users" in data
    assert "restaurants" in data
    assert "ai_search_trends" in data
    assert "top_cuisines" in data
    assert "top_favorited_restaurants" in data
    print("✓ PASS: Admin truy cập thành công 200 OK, payload đúng cấu trúc.")
    passed_count += 1

    # =========================================================================
    # TEST 05: Kiểm tra tương thích ngược với route GET /api/admin/stats
    # =========================================================================
    print("\n[TEST 05] Kiểm tra route alias GET /api/admin/stats...")
    res = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {token_admin}"})
    assert res.status_code == 200, f"Kỳ vọng 200, nhận: {res.status_code}"
    data = res.json()["data"]
    assert "top_cuisines" in data
    assert "top_favorited_restaurants" in data
    print("✓ PASS: Route alias /api/admin/stats hoạt động hoàn toàn đồng bộ.")
    passed_count += 1

    # =========================================================================
    # TEST 06: Kiểm tra số liệu Người dùng (Users Stats)
    # =========================================================================
    print("\n[TEST 06] Kiểm tra số liệu Người dùng (total, active, locked, new_this_week)...")
    users = data["users"]
    assert users["total"] == 4, f"Kỳ vọng total=4, nhận: {users['total']}"
    assert users["active"] == 2, f"Kỳ vọng active=2, nhận: {users['active']}"
    assert users["locked"] == 2, f"Kỳ vọng locked=2, nhận: {users['locked']}"
    assert users["new_this_week"] == 4, f"Kỳ vọng new_this_week=4, nhận: {users['new_this_week']}"
    print(f"✓ PASS: Thống kê User chính xác (Total={users['total']}, Active={users['active']}, Locked={users['locked']}).")
    passed_count += 1

    # =========================================================================
    # TEST 07: Kiểm tra số liệu Nhà hàng (Restaurants Stats)
    # =========================================================================
    print("\n[TEST 07] Kiểm tra số liệu Nhà hàng (total, active, hidden, avg_rating)...")
    rests = data["restaurants"]
    assert rests["total"] == 4, f"Kỳ vọng total=4, nhận: {rests['total']}"
    assert rests["active"] == 3, f"Kỳ vọng active=3, nhận: {rests['active']}"
    assert rests["hidden"] == 1, f"Kỳ vọng hidden=1, nhận: {rests['hidden']}"
    assert abs(rests["avg_rating"] - 4.45) <= 0.1, f"Kỳ vọng avg_rating ~ 4.45, nhận: {rests['avg_rating']}"
    print(f"✓ PASS: Thống kê Nhà hàng chính xác (Total={rests['total']}, Active={rests['active']}, Hidden={rests['hidden']}, AvgRating={rests['avg_rating']}).")
    passed_count += 1

    # =========================================================================
    # TEST 08: Kiểm tra số lượt tìm kiếm AI theo ngày mặc định (7 ngày liên tục)
    # =========================================================================
    print("\n[TEST 08] Kiểm tra số lượt tìm kiếm AI theo ngày (mặc định 7 ngày)...")
    trends = data["ai_search_trends"]
    assert len(trends) == 7, f"Kỳ vọng 7 ngày, nhận: {len(trends)}"
    # Kiểm tra tính liên tục của ngày tháng và định dạng YYYY-MM-DD
    today_str = datetime.utcnow().date().strftime("%Y-%m-%d")
    yesterday_str = (datetime.utcnow().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    assert trends[-1]["date"] == today_str, f"Ngày cuối phải là hôm nay: {today_str}"
    assert trends[-1]["search_count"] == 3, f"Hôm nay kỳ vọng 3 tìm kiếm, nhận: {trends[-1]['search_count']}"
    assert trends[-2]["date"] == yesterday_str
    assert trends[-2]["search_count"] == 2, f"Hôm qua kỳ vọng 2 tìm kiếm, nhận: {trends[-2]['search_count']}"
    print(f"✓ PASS: Chuỗi 7 ngày tìm kiếm AI liên tục và chính xác (Hôm nay: {trends[-1]['search_count']}, Hôm qua: {trends[-2]['search_count']}).")
    passed_count += 1

    # =========================================================================
    # TEST 09: Kiểm tra tham số tùy biến `days` (days=3, days=14)
    # =========================================================================
    print("\n[TEST 09] Kiểm tra tham số tùy biến `days=3`...")
    res = client.get("/api/admin/dashboard/stats?days=3", headers={"Authorization": f"Bearer {token_admin}"})
    assert res.status_code == 200
    trends_3 = res.json()["data"]["ai_search_trends"]
    assert len(trends_3) == 3, f"Kỳ vọng 3 ngày, nhận: {len(trends_3)}"
    assert res.json()["data"]["total_ai_searches_in_period"] == 5, "Tổng trong 3 ngày qua là 3 + 2 = 5"
    print("✓ PASS: Tham số days=3 trả về đúng 3 bản ghi và tính chuẩn tổng lượt tìm kiếm.")
    passed_count += 1

    # =========================================================================
    # TEST 10: Kiểm tra Top loại ẩm thực được tìm nhiều nhất
    # =========================================================================
    print("\n[TEST 10] Kiểm tra Top loại ẩm thực được tìm nhiều nhất...")
    top_c = data["top_cuisines"]
    assert len(top_c) == 3, f"Kỳ vọng 3 loại ẩm thực, nhận: {len(top_c)}"
    # #1 phải là BBQ Hàn Quốc (3 lượt, 50.0%)
    assert top_c[0]["cuisine"] == "BBQ Hàn Quốc"
    assert top_c[0]["search_count"] == 3
    assert top_c[0]["percentage"] == 50.0, f"Kỳ vọng 50.0%, nhận: {top_c[0]['percentage']}"
    # #2 là Cơm tấm (2 lượt, 33.3%)
    assert top_c[1]["cuisine"] == "Cơm tấm"
    assert top_c[1]["search_count"] == 2
    assert top_c[1]["percentage"] == 33.3
    # #3 là Món Chay (1 lượt, 16.7%)
    assert top_c[2]["cuisine"] == "Món Chay"
    assert top_c[2]["search_count"] == 1
    assert top_c[2]["percentage"] == 16.7
    print("✓ PASS: Top ẩm thực xếp giảm dần chuẩn xác và tính đúng % tỷ trọng.")
    passed_count += 1

    # =========================================================================
    # TEST 11: Kiểm tra Top nhà hàng được yêu thích nhất
    # =========================================================================
    print("\n[TEST 11] Kiểm tra Top nhà hàng được yêu thích nhất (UserFavorites)...")
    top_fav = data["top_favorited_restaurants"]
    assert len(top_fav) == 2, f"Kỳ vọng 2 nhà hàng có lượt yêu thích, nhận: {len(top_fav)}"
    # #1 phải là r2 (2 lượt yêu thích)
    assert top_fav[0]["id"] == r2.id
    assert top_fav[0]["name"] == r2.name
    assert top_fav[0]["favorite_count"] == 2
    assert top_fav[0]["cover_image_url"] == "https://img.foodai.vn/bbq.jpg"
    # #2 phải là r1 (1 lượt yêu thích)
    assert top_fav[1]["id"] == r1.id
    assert top_fav[1]["name"] == r1.name
    assert top_fav[1]["favorite_count"] == 1
    print(f"✓ PASS: Top nhà hàng yêu thích chính xác (#1: {top_fav[0]['name']} - {top_fav[0]['favorite_count']} bookmarks).")
    passed_count += 1

    # =========================================================================
    # TEST 12: Kiểm tra trường hợp biên (DB rỗng không crash lỗi 500)
    # =========================================================================
    print("\n[TEST 12] Kiểm tra DB rỗng hoàn toàn...")
    # Tạo database rỗng mới
    empty_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=empty_engine)
    empty_db = sessionmaker(autocommit=False, autoflush=False, bind=empty_engine)()
    
    # Tạo duy nhất 1 admin
    role_adm = Role(name="admin")
    empty_db.add(role_adm)
    empty_db.commit()
    adm = User(email="only_admin@smartdining.vn", hashed_password="pwd", status="active")
    empty_db.add(adm)
    empty_db.commit()
    empty_db.add(UserRole(user_id=adm.id, role_id=role_adm.id))
    empty_db.commit()

    token_empty_adm = create_access_token(adm.id)
    app.dependency_overrides[get_db] = lambda: empty_db

    res_empty = client.get("/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {token_empty_adm}"})
    assert res_empty.status_code == 200, f"Kỳ vọng 200, nhận: {res_empty.status_code}"
    empty_data = res_empty.json()["data"]
    assert empty_data["users"]["total"] == 1
    assert empty_data["restaurants"]["total"] == 0
    assert empty_data["restaurants"]["avg_rating"] == 0.0
    assert empty_data["top_cuisines"] == []
    assert empty_data["top_favorited_restaurants"] == []
    assert len(empty_data["ai_search_trends"]) == 7
    for day in empty_data["ai_search_trends"]:
        assert day["search_count"] == 0
    print("✓ PASS: Xử lý an toàn tuyệt đối khi DB rỗng (trả về 0 và mảng rỗng, không phát sinh lỗi 500).")
    passed_count += 1

    print("\n" + "=" * 80)
    print(f"KẾT QUẢ BỘ KIỂM THỬ: {passed_count}/12 TESTS ĐẠT 100% PASS!")
    print("=" * 80)

    # Dọn dẹp dependency overrides
    app.dependency_overrides.clear()
    return passed_count == 12


def test_te9c67e_admin_stats():
    assert run_tests() is True


if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
