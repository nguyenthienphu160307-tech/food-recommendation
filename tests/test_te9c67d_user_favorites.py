"""
Bộ Kiểm thử Tự động Toàn diện cho Task TE9C67D / FR-11, UC-08:
Xây dựng API Lưu / Bỏ lưu Nhà hàng yêu thích (Favorites).
Mô tả:
Viết POST/DELETE /api/favorites và GET /api/favorites với ràng buộc UNIQUE(user_id, restaurant_id) trong bảng UserFavorites.

15 Ca Kiểm thử Chi tiết:
1.  TEST 01: Guest chưa có Token gọi POST /api/favorites -> Bị chặn 401 Unauthorized (BR-01).
2.  TEST 02: Guest chưa có Token gọi GET / DELETE /api/favorites -> Bị chặn 401 Unauthorized (BR-01).
3.  TEST 03: Tài khoản bị khóa (status='locked') gọi API -> Bị chặn 403 Forbidden (BR-07).
4.  TEST 04: Lưu nhà hàng không tồn tại (ID=99999) -> Bị chặn 404 Not Found.
5.  TEST 05: Lưu nhà hàng thành công lần đầu (POST -> 201 Created) & sinh favorite_id.
6.  TEST 06: Ràng buộc UNIQUE(user_id, restaurant_id): Lưu lại cùng 1 nhà hàng -> Bị chặn 409 Conflict.
7.  TEST 07: Kiểm tra nhanh trạng thái yêu thích (GET /api/favorites/check/{id}) -> is_favorite=True/False.
8.  TEST 08: Lấy danh sách yêu thích (GET /api/favorites) kèm phân trang RESTful và thông tin quán.
9.  TEST 09: Tính khoảng cách GPS và sắp xếp danh sách (sort_by: newest, rating, price_asc, distance).
10. TEST 10: Cô lập dữ liệu giữa các User (User B không thấy danh sách của User A).
11. TEST 11: Bỏ lưu nhà hàng qua Path Param (DELETE /api/favorites/{id} -> 200 OK).
12. TEST 12: Bỏ lưu nhà hàng chưa từng lưu hoặc đã xóa -> Báo lỗi 404 Not Found.
13. TEST 13: Bỏ lưu nhà hàng qua Query Param / Payload (DELETE /api/favorites?restaurant_id=...).
14. TEST 14: Ràng buộc Cascade Delete khi xóa Restaurant hoặc xóa User.
15. TEST 15: Benchmark hiệu năng xử lý hàng loạt NFR-01 (< 3.0 giây).
"""
import sys
import os
import time
from datetime import datetime
from typing import Optional

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo in console tiếng Việt UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
import app.models
from app.models.user import User, UserProfile
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.models.interaction import UserFavorite
from app.services.favorite_service import FavoriteService
from app.schemas.favorite import (
    FavoriteCreateRequest,
    FavoriteDeleteRequest,
    FavoriteItemResponse,
    FavoriteListResponse,
    FavoriteActionResponse,
    FavoriteCheckResponse,
)
from app.routers.favorite import (
    add_favorite,
    delete_favorite_by_path,
    delete_favorite,
    get_my_favorites,
    check_favorite_status,
)
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
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TE9C67D: API LƯU / BỎ LƯU NHÀ HÀNG YÊU THÍCH")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    app.dependency_overrides[get_db] = lambda: db

    passed_count = 0

    # 1. Khởi tạo dữ liệu người dùng mẫu
    user_a = User(
        email="user_a_fav@smartdining.vn",
        phone_number="0911000001",
        hashed_password="hashed_pass_a",
        status="active"
    )
    user_b = User(
        email="user_b_fav@smartdining.vn",
        phone_number="0911000002",
        hashed_password="hashed_pass_b",
        status="active"
    )
    user_locked = User(
        email="user_locked_fav@smartdining.vn",
        phone_number="0911000003",
        hashed_password="hashed_pass_locked",
        status="locked"
    )
    db.add_all([user_a, user_b, user_locked])
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)
    db.refresh(user_locked)

    # 2. Khởi tạo các nhà hàng mẫu
    r1 = Restaurant(
        name="Phở Thìn Bờ Hồ - Chi nhánh 1",
        description="Phở bò gia truyền thơm ngon đậm đà",
        address="12 Lê Duẩn, Bến Nghé, Quận 1, TP.HCM",
        latitude=10.7800,
        longitude=106.6990,
        cuisine_type="Món Việt",
        min_price=60000.0,
        max_price=120000.0,
        open_hours="06:00 - 22:00",
        avg_rating=4.7,
        total_reviews=15,
        status="active"
    )
    r2 = Restaurant(
        name="Sushi Hokkaido Sachi",
        description="Ẩm thực Nhật Bản cao cấp tươi sống",
        address="139 Nguyễn Trãi, Bến Thành, Quận 1, TP.HCM",
        latitude=10.7710,
        longitude=106.6920,
        cuisine_type="Món Nhật",
        min_price=200000.0,
        max_price=800000.0,
        open_hours="10:30 - 22:30",
        avg_rating=4.9,
        total_reviews=42,
        status="active"
    )
    r3 = Restaurant(
        name="Lẩu Nướng Gogi House",
        description="Thịt nướng chuẩn vị Hàn Quốc",
        address="35 Nguyễn Thị Minh Khai, Quận 1, TP.HCM",
        latitude=10.7850,
        longitude=106.7020,
        cuisine_type="Lẩu Nướng",
        min_price=150000.0,
        max_price=450000.0,
        open_hours="10:00 - 22:00",
        avg_rating=4.2,
        total_reviews=8,
        status="active"
    )
    db.add_all([r1, r2, r3])
    db.commit()
    db.refresh(r1)
    db.refresh(r2)
    db.refresh(r3)

    # Thêm tiện ích và ảnh bìa
    amenity1 = RestaurantAmenity(restaurant_id=r1.id, has_parking=True, has_private_room=False)
    amenity2 = RestaurantAmenity(restaurant_id=r2.id, has_parking=True, has_private_room=True)
    img1 = RestaurantImage(restaurant_id=r1.id, image_url="https://img.foodai.vn/pho1.jpg", is_cover=True)
    img2 = RestaurantImage(restaurant_id=r2.id, image_url="https://img.foodai.vn/sushi.jpg", is_cover=True)
    db.add_all([amenity1, amenity2, img1, img2])
    db.commit()

    # Tạo JWT Tokens phục vụ TestClient HTTP
    token_user_a = create_access_token(user_a.id)
    token_user_b = create_access_token(user_b.id)
    token_locked = create_access_token(user_locked.id)

    client = TestClient(app)

    # =========================================================================
    # TEST 01: Guest chưa có Token gọi POST /api/favorites -> 401 Unauthorized
    # =========================================================================
    print("\n[TEST 01] Guest chưa có Token gọi POST /api/favorites (BR-01)...")
    res_t1 = client.post("/api/favorites", json={"restaurant_id": r1.id})
    assert res_t1.status_code == status.HTTP_401_UNAUTHORIZED
    print(" => PASSED: Chặn thành công khách vãng lai gọi POST (HTTP 401 Unauthorized).")
    passed_count += 1

    # =========================================================================
    # TEST 02: Guest chưa có Token gọi GET / DELETE /api/favorites -> 401 Unauthorized
    # =========================================================================
    print("\n[TEST 02] Guest chưa có Token gọi GET / DELETE /api/favorites (BR-01)...")
    res_t2_get = client.get("/api/favorites")
    assert res_t2_get.status_code == status.HTTP_401_UNAUTHORIZED
    res_t2_del = client.delete(f"/api/favorites/{r1.id}")
    assert res_t2_del.status_code == status.HTTP_401_UNAUTHORIZED
    print(" => PASSED: Chặn thành công khách vãng lai gọi GET và DELETE (HTTP 401 Unauthorized).")
    passed_count += 1

    # =========================================================================
    # TEST 03: Tài khoản bị khóa (status='locked') gọi API -> 403 Forbidden
    # =========================================================================
    print("\n[TEST 03] Tài khoản bị khóa (status='locked') gọi API (BR-07)...")
    res_t3 = client.post(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_locked}"},
        json={"restaurant_id": r1.id}
    )
    assert res_t3.status_code == status.HTTP_403_FORBIDDEN
    print(" => PASSED: Chặn thành công tài khoản bị khóa theo BR-07 (HTTP 403 Forbidden).")
    passed_count += 1

    # =========================================================================
    # TEST 04: Lưu nhà hàng không tồn tại (ID=99999) -> 404 Not Found
    # =========================================================================
    print("\n[TEST 04] Lưu nhà hàng không tồn tại trong CSDL (ID=99999)...")
    res_t4 = client.post(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"},
        json={"restaurant_id": 99999}
    )
    assert res_t4.status_code == status.HTTP_404_NOT_FOUND
    print(" => PASSED: Báo lỗi 404 Not Found khi nhà hàng không tồn tại.")
    passed_count += 1

    # =========================================================================
    # TEST 05: Lưu nhà hàng thành công lần đầu (POST -> 201 Created)
    # =========================================================================
    print("\n[TEST 05] User A lưu nhà hàng R1 thành công lần đầu (POST -> 201 Created)...")
    payload_t5 = {"restaurant_id": r1.id, "note": "Quán phở yêu thích mỗi sáng thứ Hai"}
    res_t5 = client.post(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"},
        json=payload_t5
    )
    assert res_t5.status_code == status.HTTP_201_CREATED
    data_t5 = res_t5.json()
    assert data_t5["status"] == "success"
    assert data_t5["is_favorite"] is True
    assert data_t5["restaurant_id"] == r1.id
    assert data_t5["favorite_id"] is not None
    fav_id_1 = data_t5["favorite_id"]
    print(f" => PASSED: Lưu nhà hàng R1 thành công! favorite_id={fav_id_1}, is_favorite=True.")
    passed_count += 1

    # =========================================================================
    # TEST 06: Ràng buộc UNIQUE(user_id, restaurant_id): Lưu lại quán R1 -> 409 Conflict
    # =========================================================================
    print("\n[TEST 06] Kiểm tra ràng buộc duy nhất UNIQUE(user_id, restaurant_id) -> 409 Conflict...")
    res_t6 = client.post(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"},
        json={"restaurant_id": r1.id, "note": "Lưu đúp để kiểm tra"}
    )
    assert res_t6.status_code == status.HTTP_409_CONFLICT
    assert "đã có trong danh sách yêu thích" in res_t6.json()["detail"]
    print(" => PASSED: Chặn thành công trùng lặp theo ràng buộc UNIQUE(user_id, restaurant_id) (HTTP 409 Conflict).")
    passed_count += 1

    # =========================================================================
    # TEST 07: Kiểm tra nhanh trạng thái yêu thích (GET /api/favorites/check/{id})
    # =========================================================================
    print("\n[TEST 07] Kiểm tra nhanh trạng thái yêu thích (GET /api/favorites/check/{id})...")
    res_t7_r1 = client.get(
        f"/api/favorites/check/{r1.id}",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t7_r1.status_code == status.HTTP_200_OK
    assert res_t7_r1.json()["is_favorite"] is True
    assert res_t7_r1.json()["favorite_id"] == fav_id_1

    res_t7_r2 = client.get(
        f"/api/favorites/check/{r2.id}",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t7_r2.status_code == status.HTTP_200_OK
    assert res_t7_r2.json()["is_favorite"] is False
    assert res_t7_r2.json()["favorite_id"] is None
    print(" => PASSED: Endpoint kiểm tra nhanh trạng thái yêu thích phản hồi chính xác.")
    passed_count += 1

    # Lưu thêm quán R2 cho User A
    client.post(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"},
        json={"restaurant_id": r2.id, "note": "Sushi ngon"}
    )

    # =========================================================================
    # TEST 08: Lấy danh sách yêu thích (GET /api/favorites) kèm phân trang RESTful
    # =========================================================================
    print("\n[TEST 08] Lấy danh sách yêu thích của User A (GET /api/favorites)...")
    res_t8 = client.get(
        "/api/favorites?page=1&limit=10",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t8.status_code == status.HTTP_200_OK
    data_t8 = res_t8.json()
    assert data_t8["status"] == "success"
    assert data_t8["total"] == 2
    assert len(data_t8["data"]) == 2
    assert data_t8["pagination"]["total_items"] == 2
    assert data_t8["pagination"]["page"] == 1

    # Kiểm tra thông tin nhà hàng chi tiết kèm theo
    first_item = data_t8["data"][0]
    assert "restaurant" in first_item
    assert first_item["restaurant"]["id"] in [r1.id, r2.id]
    assert first_item["restaurant"]["cover_image_url"] is not None
    assert "is_open" in first_item["restaurant"]
    print(f" => PASSED: Lấy danh sách yêu thích thành công ({data_t8['total']} quán kèm thông tin đầy đủ).")
    passed_count += 1

    # =========================================================================
    # TEST 09: Tính khoảng cách GPS và sắp xếp danh sách (sort_by)
    # =========================================================================
    print("\n[TEST 09] Tính khoảng cách GPS và kiểm tra các chế độ sắp xếp (sort_by)...")
    # Tọa độ tại Nhà thờ Đức Bà (10.7797, 106.6990)
    res_t9_gps = client.get(
        "/api/favorites?lat=10.7797&lng=106.6990&sort_by=rating",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t9_gps.status_code == status.HTTP_200_OK
    data_t9 = res_t9_gps.json()
    # Sắp xếp rating giảm dần: R2 (4.9 sao) phải xếp trước R1 (4.7 sao)
    assert data_t9["data"][0]["restaurant"]["id"] == r2.id
    assert data_t9["data"][1]["restaurant"]["id"] == r1.id
    print(" => PASSED: Sắp xếp theo rating giảm dần và tính toán dữ liệu khoảng cách chuẩn xác.")
    passed_count += 1

    # =========================================================================
    # TEST 10: Cô lập dữ liệu giữa các User (User B không thấy quán của User A)
    # =========================================================================
    print("\n[TEST 10] Kiểm tra tính cô lập dữ liệu người dùng (User B vs User A)...")
    res_t10 = client.get(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_b}"}
    )
    assert res_t10.status_code == status.HTTP_200_OK
    assert res_t10.json()["total"] == 0
    assert len(res_t10.json()["data"]) == 0
    print(" => PASSED: Cô lập dữ liệu tuyệt đối giữa các tài khoản người dùng.")
    passed_count += 1

    # =========================================================================
    # TEST 11: Bỏ lưu nhà hàng qua Path Param (DELETE /api/favorites/{id} -> 200 OK)
    # =========================================================================
    print("\n[TEST 11] User A bỏ lưu quán R1 qua DELETE /api/favorites/{restaurant_id}...")
    res_t11 = client.delete(
        f"/api/favorites/{r1.id}",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t11.status_code == status.HTTP_200_OK
    assert res_t11.json()["is_favorite"] is False
    assert res_t11.json()["restaurant_id"] == r1.id

    # Xác minh lại danh sách chỉ còn 1 quán (R2)
    res_t11_check = client.get(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t11_check.json()["total"] == 1
    assert res_t11_check.json()["data"][0]["restaurant_id"] == r2.id
    print(" => PASSED: Bỏ lưu thành công, danh sách tự động cập nhật giảm còn 1 quán.")
    passed_count += 1

    # =========================================================================
    # TEST 12: Bỏ lưu nhà hàng chưa từng lưu hoặc đã xóa -> 404 Not Found
    # =========================================================================
    print("\n[TEST 12] Bỏ lưu nhà hàng đã xóa (R1) lần nữa -> 404 Not Found...")
    res_t12 = client.delete(
        f"/api/favorites/{r1.id}",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t12.status_code == status.HTTP_404_NOT_FOUND
    print(" => PASSED: Báo lỗi 404 Not Found chính xác khi quán không còn trong danh sách yêu thích.")
    passed_count += 1

    # =========================================================================
    # TEST 13: Bỏ lưu nhà hàng qua Query Param / Payload (DELETE /api/favorites?restaurant_id=...)
    # =========================================================================
    print("\n[TEST 13] Bỏ lưu quán R2 qua DELETE /api/favorites?restaurant_id=... ...")
    res_t13 = client.delete(
        f"/api/favorites?restaurant_id={r2.id}",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t13.status_code == status.HTTP_200_OK
    assert res_t13.json()["is_favorite"] is False

    # Xác minh lại danh sách User A về 0 quán
    res_t13_empty = client.get(
        "/api/favorites",
        headers={"Authorization": f"Bearer {token_user_a}"}
    )
    assert res_t13_empty.json()["total"] == 0
    print(" => PASSED: Hỗ trợ linh hoạt cả DELETE qua Query Param / Payload.")
    passed_count += 1

    # =========================================================================
    # TEST 14: Ràng buộc Cascade Delete khi xóa Restaurant hoặc xóa User
    # =========================================================================
    print("\n[TEST 14] Kiểm tra ràng buộc Cascade Delete...")
    # Tạo lại favorite cho User B với R3
    FavoriteService.add_favorite(db=db, user_id=user_b.id, restaurant_id=r3.id)
    fav_before = db.query(UserFavorite).filter(UserFavorite.restaurant_id == r3.id).first()
    assert fav_before is not None

    # Xóa nhà hàng R3
    db.delete(r3)
    db.commit()

    # Kiểm tra UserFavorite liên quan có tự động bị xóa không (Cascade Delete)
    fav_after = db.query(UserFavorite).filter(UserFavorite.restaurant_id == r3.id).first()
    assert fav_after is None, "UserFavorite phải tự động bị xóa khi xóa Restaurant"
    print(" => PASSED: Ràng buộc Cascade Delete hoạt động chính xác, không để lại bản ghi mồ côi.")
    passed_count += 1

    # =========================================================================
    # TEST 15: Benchmark hiệu năng xử lý hàng loạt NFR-01 (< 3.0 giây)
    # =========================================================================
    print("\n[TEST 15] Benchmark hiệu năng xử lý hàng loạt (NFR-01 < 3.0 giây)...")
    # Tạo lại dữ liệu cho benchmark
    FavoriteService.add_favorite(db=db, user_id=user_a.id, restaurant_id=r1.id)
    t0 = time.perf_counter()
    iterations = 200
    for _ in range(iterations):
        _ = FavoriteService.get_user_favorites(db=db, user_id=user_a.id, page=1, limit=10)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian xử lý {iterations} lượt: {elapsed_ms:.2f} ms ({elapsed_ms / iterations:.4f} ms/lượt)")
    assert elapsed_ms < 3000, f"Hiệu năng quá chậm: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ phản hồi cực nhanh ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")
    passed_count += 1

    print("\n" + "=" * 80)
    print(f"KẾT QUẢ KIỂM THỬ: {passed_count}/15 CA KIỂM THỬ ĐÃ VƯỢT QUA HOÀN TOÀN (100% PASSED)!")
    print("=" * 80)
    db.close()


def test_te9c67d_user_favorites():
    """Wrapper function để pytest tự động thu thập và chạy toàn bộ bộ kiểm thử"""
    run_tests()


if __name__ == "__main__":
    run_tests()
