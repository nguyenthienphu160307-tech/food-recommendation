"""
Bộ kiểm thử Tự động Toàn diện cho Task TSK-51 / PBI-13:
Xây dựng API Chấm điểm (1-5 sao), Nhận xét & Tự động tính lại avg_rating (FR-10)
Mô tả: Viết POST/PUT /api/reviews kiểm tra UNIQUE(restaurant_id, user_id) theo BR-06;
       sau khi lưu tự động cập nhật avg_rating trong bảng Restaurants.

14 Ca kiểm thử bao phủ toàn diện:
1.  TEST 01: Chặn tạo đánh giá với restaurant_id không tồn tại (HTTP 404).
2.  TEST 02: Chặn tạo đánh giá với user_id không tồn tại (HTTP 404 / BR-01).
3.  TEST 03: Chặn tài khoản bị khóa (status='locked') gửi đánh giá (HTTP 403 / BR-07).
4.  TEST 04: Kiểm tra ràng buộc điểm số rating: ngoài khoảng 1-5 sao bị chặn (HTTP 400).
5.  TEST 05: Tạo đánh giá 5 sao hợp lệ đầu tiên và tự động cập nhật avg_rating = 5.0, total_reviews = 1.
6.  TEST 06: Ràng buộc UNIQUE(restaurant_id, user_id) theo BR-06: Chặn gửi review lần 2 (HTTP 409 Conflict).
7.  TEST 07: Cho phép chỉnh sửa đánh giá cũ (PUT) và tự động tính lại avg_rating.
8.  TEST 08: Kiểm tra phân quyền: Chặn người dùng khác sửa review của người khác (HTTP 403 Forbidden).
9.  TEST 09: Tính toán chính xác avg_rating theo công thức làm tròn 1 chữ số thập phân với nhiều đánh giá.
10. TEST 10: Lấy danh sách đánh giá nhà hàng có phân trang, thông tin người dùng và lọc theo số sao.
11. TEST 11: Lấy đánh giá của chính người dùng (/my-review) phục vụ hiển thị form cập nhật.
12. TEST 12: Xóa đánh giá, kiểm tra phân quyền 403, tự động cập nhật avg_rating về 0.0 khi xóa hết.
13. TEST 13: Kiểm tra ràng buộc Cascade Delete khi xóa Restaurant.
14. TEST 14: Kiểm thử toàn diện 5 Router Handlers của router /api/reviews.
"""
import sys
import os
from datetime import datetime

# Thêm thư mục gốc dự án vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo in console tiếng Việt UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import HTTPException

from app.core.database import Base
import app.models
from app.models.user import User, UserProfile
from app.models.restaurant import Restaurant
from app.models.review import RestaurantReview
from app.services.review_service import ReviewService
from app.schemas.review import (
    ReviewCreateRequest,
    ReviewUpdateRequest,
)
from app.routers.review import (
    create_review,
    update_review,
    get_restaurant_reviews,
    get_my_review,
    delete_review,
)

# Khởi tạo SQLite in-memory test database độc lập và siêu tốc
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def run_tests():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-51: API CHẤM ĐIỂM, NHẬN XÉT & TÍNH AVG_RATING")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    # Khởi tạo dữ liệu người dùng & nhà hàng mẫu
    user_1 = User(
        email="reviewer_1@foodai.vn",
        phone_number="0911222333",
        hashed_password="fake_hash_1",
        status="active"
    )
    user_2 = User(
        email="reviewer_2@foodai.vn",
        phone_number="0944555666",
        hashed_password="fake_hash_2",
        status="active"
    )
    user_3 = User(
        email="reviewer_3@foodai.vn",
        phone_number="0977888999",
        hashed_password="fake_hash_3",
        status="active"
    )
    user_locked = User(
        email="locked_user@foodai.vn",
        phone_number="0988777666",
        hashed_password="fake_hash_locked",
        status="locked"
    )
    db.add_all([user_1, user_2, user_3, user_locked])
    db.commit()
    db.refresh(user_1)
    db.refresh(user_2)
    db.refresh(user_3)
    db.refresh(user_locked)

    prof_1 = UserProfile(user_id=user_1.id, full_name="Trần Văn Minh", avatar_url="https://avatar.com/1.jpg")
    prof_2 = UserProfile(user_id=user_2.id, full_name="Lê Thị Hoa", avatar_url="https://avatar.com/2.jpg")
    db.add_all([prof_1, prof_2])
    db.commit()

    restaurant_a = Restaurant(
        name="Lẩu Nướng Phố Cổ",
        address="12 Hàng Buồm, Hoàn Kiếm, Hà Nội",
        cuisine_type="Lẩu Nướng",
        latitude=21.0345,
        longitude=105.8521,
        min_price=150000.0,
        max_price=350000.0,
        avg_rating=0.0,
        total_reviews=0,
        status="active"
    )
    restaurant_b = Restaurant(
        name="Bún Bò Huế O Mai",
        address="45 Quang Trung, Đà Nẵng",
        cuisine_type="Món Huế",
        latitude=16.0678,
        longitude=108.2208,
        min_price=40000.0,
        max_price=70000.0,
        avg_rating=0.0,
        total_reviews=0,
        status="active"
    )
    db.add_all([restaurant_a, restaurant_b])
    db.commit()
    db.refresh(restaurant_a)
    db.refresh(restaurant_b)

    passed_count = 0

    # -------------------------------------------------------------------------
    # TEST 01: Chặn tạo đánh giá với restaurant_id không tồn tại
    # -------------------------------------------------------------------------
    print("\n[TEST 01] Chặn tạo đánh giá với restaurant_id không tồn tại (HTTP 404)...")
    try:
        ReviewService.create_review(
            db=db,
            restaurant_id=99999,
            user_id=user_1.id,
            rating=5,
            comment="Quán ngon tuyệt!"
        )
        assert False, "Phải ném HTTPException 404."
    except HTTPException as e:
        assert e.status_code == 404
    print(" => PASSED: Chặn thành công restaurant_id không tồn tại (404 Not Found).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 02: Chặn tạo đánh giá với user_id không tồn tại
    # -------------------------------------------------------------------------
    print("\n[TEST 02] Chặn tạo đánh giá với user_id không tồn tại (HTTP 404 / BR-01)...")
    try:
        ReviewService.create_review(
            db=db,
            restaurant_id=restaurant_a.id,
            user_id=88888,
            rating=5,
            comment="Ngon xuất sắc"
        )
        assert False, "Phải ném HTTPException 404."
    except HTTPException as e:
        assert e.status_code == 404
    print(" => PASSED: Chặn thành công user_id không tồn tại (404 Not Found).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 03: Chặn tài khoản bị khóa (status='locked') gửi đánh giá
    # -------------------------------------------------------------------------
    print("\n[TEST 03] Chặn tài khoản bị khóa (status='locked') gửi đánh giá (HTTP 403 / BR-07)...")
    try:
        ReviewService.create_review(
            db=db,
            restaurant_id=restaurant_a.id,
            user_id=user_locked.id,
            rating=4,
            comment="Đánh giá từ tài khoản vi phạm"
        )
        assert False, "Phải ném HTTPException 403."
    except HTTPException as e:
        assert e.status_code == 403
    print(" => PASSED: Chặn thành công tài khoản bị khóa gửi đánh giá (403 Forbidden).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 04: Kiểm tra ràng buộc điểm số rating (1 <= rating <= 5)
    # -------------------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra ràng buộc điểm số rating (1-5 sao)...")
    # Thử rating = 0
    try:
        ReviewService.create_review(db=db, restaurant_id=restaurant_a.id, user_id=user_1.id, rating=0)
        assert False, "Rating = 0 phải bị từ chối."
    except HTTPException as e:
        assert e.status_code == 400

    # Thử rating = 6
    try:
        ReviewService.create_review(db=db, restaurant_id=restaurant_a.id, user_id=user_1.id, rating=6)
        assert False, "Rating = 6 phải bị từ chối."
    except HTTPException as e:
        assert e.status_code == 400
    print(" => PASSED: Ràng buộc số sao 1 <= rating <= 5 hoạt động chuẩn xác (400 Bad Request).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 05: Tạo đánh giá 5 sao đầu tiên & tự động cập nhật avg_rating = 5.0
    # -------------------------------------------------------------------------
    print("\n[TEST 05] Tạo đánh giá 5 sao đầu tiên & tự động cập nhật avg_rating, total_reviews...")
    rev_1 = ReviewService.create_review(
        db=db,
        restaurant_id=restaurant_a.id,
        user_id=user_1.id,
        rating=5,
        comment="Nước lẩu thái đậm đà, thịt bò tươi ngon, nhân viên phục vụ rất nhiệt tình!"
    )
    assert rev_1.id is not None
    assert rev_1.rating == 5
    assert rev_1.restaurant_id == restaurant_a.id
    assert rev_1.user_id == user_1.id

    # Kiểm tra CSDL Restaurants đã được tự động cập nhật avg_rating và total_reviews
    db.refresh(restaurant_a)
    assert restaurant_a.total_reviews == 1, f"total_reviews phải là 1, nhận: {restaurant_a.total_reviews}"
    assert restaurant_a.avg_rating == 5.0, f"avg_rating phải là 5.0, nhận: {restaurant_a.avg_rating}"
    print(" => PASSED: Đánh giá đầu tiên lưu thành công, avg_rating tự động cập nhật = 5.0 (total = 1).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 06: Ràng buộc UNIQUE(restaurant_id, user_id) theo BR-06
    # -------------------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra ràng buộc BR-06: Chặn gửi đánh giá lần 2 (HTTP 409 Conflict)...")
    try:
        ReviewService.create_review(
            db=db,
            restaurant_id=restaurant_a.id,
            user_id=user_1.id,
            rating=4,
            comment="Gửi lại đánh giá lần hai"
        )
        assert False, "Phải ném HTTPException 409 Conflict khi đánh giá trùng theo BR-06."
    except HTTPException as e:
        assert e.status_code == 409, f"Status code phải là 409, nhận: {e.status_code}"
        assert "BR-06" in e.detail or "đã đánh giá" in e.detail
    print(" => PASSED: Chặn thành công đánh giá lần 2 theo quy tắc BR-06 (409 Conflict).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 07: Cho phép chỉnh sửa đánh giá cũ (PUT) và tự động tính lại avg_rating
    # -------------------------------------------------------------------------
    print("\n[TEST 07] Chỉnh sửa đánh giá cũ (PUT) từ 5 sao xuống 3 sao & tính lại avg_rating...")
    updated_rev = ReviewService.update_review(
        db=db,
        review_id=rev_1.id,
        user_id=user_1.id,
        rating=3,
        comment="Hôm nay đi lại hơi đông, nước lẩu hơi mặn xíu nên hạ xuống 3 sao."
    )
    assert updated_rev.rating == 3
    assert "3 sao" in updated_rev.comment

    db.refresh(restaurant_a)
    assert restaurant_a.total_reviews == 1
    assert restaurant_a.avg_rating == 3.0, f"avg_rating phải cập nhật thành 3.0, nhận: {restaurant_a.avg_rating}"
    print(" => PASSED: Chỉnh sửa đánh giá thành công (BR-06 cho phép sửa), avg_rating tính lại = 3.0.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 08: Kiểm tra phân quyền: Chặn người khác sửa review của người khác
    # -------------------------------------------------------------------------
    print("\n[TEST 08] Chặn người dùng khác chỉnh sửa review của người khác (HTTP 403 Forbidden)...")
    try:
        ReviewService.update_review(
            db=db,
            review_id=rev_1.id,
            user_id=user_2.id,
            rating=1,
            comment="Cố tình hạ điểm của người khác"
        )
        assert False, "Phải ném 403 Forbidden."
    except HTTPException as e:
        assert e.status_code == 403, f"Status code phải là 403, nhận: {e.status_code}"
    print(" => PASSED: Phân quyền bảo mật 403 Forbidden hoạt động chính xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 09: Tính toán avg_rating với nhiều đánh giá (round 1 chữ số thập phân)
    # -------------------------------------------------------------------------
    print("\n[TEST 09] Thêm nhiều đánh giá từ các người dùng khác nhau và xác minh avg_rating...")
    # User 2 đánh giá 4 sao
    rev_2 = ReviewService.create_review(
        db=db,
        restaurant_id=restaurant_a.id,
        user_id=user_2.id,
        rating=4,
        comment="Quán sạch sẽ, đồ ăn ngon, giá cả hợp lý."
    )
    # User 3 đánh giá 4 sao
    rev_3 = ReviewService.create_review(
        db=db,
        restaurant_id=restaurant_a.id,
        user_id=user_3.id,
        rating=4,
        comment="Khá ổn áp, sẽ quay lại lần sau."
    )
    # Hiện tại có 3 reviews với số sao: 3, 4, 4 -> Tổng = 11 -> avg = 11/3 = 3.6666... -> Làm tròn 3.7
    db.refresh(restaurant_a)
    assert restaurant_a.total_reviews == 3, f"total_reviews phải là 3, nhận: {restaurant_a.total_reviews}"
    assert restaurant_a.avg_rating == 3.7, f"avg_rating làm tròn phải là 3.7, nhận: {restaurant_a.avg_rating}"

    # Cập nhật user_3 từ 4 sao lên 5 sao -> [3, 4, 5] -> Tổng = 12 -> avg = 4.0
    ReviewService.update_review(db=db, review_id=rev_3.id, user_id=user_3.id, rating=5)
    db.refresh(restaurant_a)
    assert restaurant_a.avg_rating == 4.0, f"avg_rating phải là 4.0, nhận: {restaurant_a.avg_rating}"
    print(" => PASSED: Thuật toán tính avg_rating = round(sum/count, 1) hoạt động hoàn hảo (3.7 -> 4.0).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 10: Lấy danh sách đánh giá của nhà hàng (phân trang, lọc theo sao)
    # -------------------------------------------------------------------------
    print("\n[TEST 10] Lấy danh sách đánh giá kèm thông tin user và lọc theo sao...")
    list_res = ReviewService.get_restaurant_reviews(
        db=db,
        restaurant_id=restaurant_a.id,
        page=1,
        limit=2
    )
    assert list_res["total_reviews"] == 3
    assert list_res["avg_rating"] == 4.0
    assert len(list_res["items"]) == 2, "Trang 1 với limit=2 phải trả về 2 mục."
    # Kiểm tra nạp thông tin user
    first_item = list_res["items"][0]
    assert first_item.user is not None
    assert first_item.user.full_name in ["Trần Văn Minh", "Lê Thị Hoa", "reviewer_3"]

    # Lọc chỉ lấy các đánh giá 5 sao (chỉ có user_3)
    filtered_5star = ReviewService.get_restaurant_reviews(
        db=db,
        restaurant_id=restaurant_a.id,
        page=1,
        limit=10,
        rating_filter=5
    )
    assert len(filtered_5star["items"]) == 1
    assert filtered_5star["items"][0].rating == 5
    print(" => PASSED: Lấy danh sách phân trang, thông tin user và lọc theo sao thành công.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 11: Lấy đánh giá của chính người dùng (/my-review)
    # -------------------------------------------------------------------------
    print("\n[TEST 11] Lấy đánh giá hiện có của chính tôi (/my-review)...")
    my_rev = ReviewService.get_user_review_for_restaurant(
        db=db,
        restaurant_id=restaurant_a.id,
        user_id=user_1.id
    )
    assert my_rev is not None
    assert my_rev.user_id == user_1.id
    assert my_rev.rating == 3

    # Kiểm tra với nhà hàng B chưa từng đánh giá
    my_rev_b = ReviewService.get_user_review_for_restaurant(
        db=db,
        restaurant_id=restaurant_b.id,
        user_id=user_1.id
    )
    assert my_rev_b is None
    print(" => PASSED: Lấy thông tin /my-review chính xác phục vụ form chỉnh sửa.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 12: Xóa đánh giá & tự động tính lại avg_rating về 0.0
    # -------------------------------------------------------------------------
    print("\n[TEST 12] Xóa đánh giá, kiểm tra phân quyền 403 & tự động cập nhật avg_rating...")
    # Chặn user_2 xóa review của user_1
    try:
        ReviewService.delete_review(db=db, review_id=rev_1.id, user_id=user_2.id, is_admin=False)
        assert False, "Phải ném 403 Forbidden."
    except HTTPException as e:
        assert e.status_code == 403

    # Xóa review 1 hợp lệ
    avg, total = ReviewService.delete_review(db=db, review_id=rev_1.id, user_id=user_1.id)
    assert total == 2
    # Còn lại rev_2 (4 sao) và rev_3 (5 sao) -> avg = 9/2 = 4.5
    assert avg == 4.5

    # Xóa 2 reviews còn lại
    ReviewService.delete_review(db=db, review_id=rev_2.id, user_id=user_2.id)
    avg_final, total_final = ReviewService.delete_review(db=db, review_id=rev_3.id, user_id=user_3.id)
    assert total_final == 0
    assert avg_final == 0.0
    db.refresh(restaurant_a)
    assert restaurant_a.avg_rating == 0.0
    assert restaurant_a.total_reviews == 0
    print(" => PASSED: Xóa đánh giá phân quyền chuẩn và tự động reset avg_rating = 0.0 khi xóa hết.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 13: Ràng buộc Cascade Delete khi xóa Restaurant
    # -------------------------------------------------------------------------
    print("\n[TEST 13] Kiểm tra Cascade Delete khi xóa Restaurant...")
    # Tạo 1 review trên nhà hàng B
    rev_b = ReviewService.create_review(
        db=db,
        restaurant_id=restaurant_b.id,
        user_id=user_1.id,
        rating=5,
        comment="Bún bò Huế rất ngon!"
    )
    rev_b_id = rev_b.id
    # Xóa nhà hàng B
    db.delete(restaurant_b)
    db.commit()
    # Kiểm tra review tự động bị xóa
    check_rev = db.query(RestaurantReview).filter(RestaurantReview.id == rev_b_id).first()
    assert check_rev is None, "Review phải tự động bị xóa khi Restaurant bị xóa (CASCADE)."
    print(" => PASSED: Ràng buộc Cascade Delete hoạt động chính xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 14: Kiểm thử toàn diện 5 Router Handlers của router /api/reviews
    # -------------------------------------------------------------------------
    print("\n[TEST 14] Kiểm thử toàn bộ 5 Router Handlers của router /api/reviews...")
    # Tạo lại 1 nhà hàng mới để test router handlers
    rest_test = Restaurant(
        name="Quán Chay Thanh Tịnh",
        address="99 Nguyễn Thị Minh Khai, Q.1, TP.HCM",
        cuisine_type="Món Chay",
        latitude=10.7712,
        longitude=106.6901,
        min_price=50000.0,
        max_price=120000.0,
        avg_rating=0.0,
        total_reviews=0,
        status="active"
    )
    db.add(rest_test)
    db.commit()
    db.refresh(rest_test)

    # 1. create_review handler
    create_payload = ReviewCreateRequest(
        restaurant_id=rest_test.id,
        user_id=user_1.id,
        rating=5,
        comment="Đồ ăn chay thanh vị, không dầu mỡ, không gian yên bình!"
    )
    r_created = create_review(payload=create_payload, db=db)
    assert r_created.id is not None
    assert r_created.rating == 5
    assert r_created.user is not None
    assert r_created.user.full_name == "Trần Văn Minh"
    saved_id = r_created.id

    # 2. get_my_review handler
    r_my = get_my_review(restaurant_id=rest_test.id, user_id=user_1.id, db=db)
    assert r_my is not None
    assert r_my.id == saved_id

    # 3. update_review handler
    update_payload = ReviewUpdateRequest(
        user_id=user_1.id,
        rating=4,
        comment="Cập nhật lại: Đồ ăn ngon nhưng gửi xe hơi chật tí."
    )
    r_updated = update_review(review_id=saved_id, payload=update_payload, db=db)
    assert r_updated.rating == 4

    # 4. get_restaurant_reviews handler
    r_list = get_restaurant_reviews(restaurant_id=rest_test.id, page=1, limit=5, rating=None, db=db)
    assert r_list.total_reviews == 1
    assert r_list.avg_rating == 4.0
    assert len(r_list.items) == 1

    # 5. delete_review handler
    r_del = delete_review(review_id=saved_id, user_id=user_1.id, is_admin=False, db=db)
    assert r_del.success is True
    assert r_del.avg_rating == 0.0
    assert r_del.total_reviews == 0

    print(" => PASSED: Toàn bộ 5 Router Handlers của router /api/reviews hoạt động chuẩn xác.")
    passed_count += 1

    print("\n" + "=" * 80)
    print(f"KẾT QUẢ KIỂM THỬ: {passed_count}/14 CA KIỂM THỬ ĐÃ VƯỢT QUA HOÀN TOÀN (100% PASSED)!")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
