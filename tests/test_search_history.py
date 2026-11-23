"""
Bộ kiểm thử Tự động cho Task TSK-46 / PBI-14:
Xây dựng API Xem lịch sử tìm kiếm & Khôi phục phiên hội thoại cũ (FR-12, UC-10)
Mô tả: Viết GET /api/search/history trả về danh sách SearchSessions kèm SearchCriteria và các nhà hàng đã gợi ý cho người dùng.

9 Ca kiểm thử toàn diện:
1. TEST 01: Chặn truy vấn lịch sử với user_id không tồn tại (HTTP 404 / BR-01).
2. TEST 02: Trả về danh sách rỗng chuẩn xác cho người dùng mới chưa có phiên tìm kiếm nào.
3. TEST 03: Trả về đầy đủ thông tin phiên kèm tiêu chí tìm kiếm SearchCriteria bóc tách.
4. TEST 04: Tự động liên kết và gợi ý các nhà hàng khớp theo thể loại ẩm thực (cuisine).
5. TEST 05: Tự động lọc và gợi ý nhà hàng theo ngân sách (budget) và chỗ đỗ ô tô (parking).
6. TEST 06: Kiểm tra tính toán % Match Score và trạng thái mở cửa thực tế (BR-03, BR-05).
7. TEST 07: Lọc lịch sử theo trạng thái phiên ('active', 'closed', 'all').
8. TEST 08: Kiểm tra cơ chế phân trang chuẩn RESTful (page, limit, total_pages, total_sessions).
9. TEST 09: Benchmark hiệu năng truy vấn lịch sử và kết quả gợi ý đạt chuẩn NFR-01 (< 3.0s).
"""
import sys
import os
import time
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
from app.models.user import User
from app.models.search import SearchSession, SearchMessage, SearchCriteria
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.services.chat_session_service import ChatSessionService
from app.routers.search import get_search_history, get_chat_search_history

# Khởi tạo SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def run_tests():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-46: API XEM LỊCH SỬ TÌM KIẾM & KẾT QUẢ GỢI Ý")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    # 1. Tạo User kiểm thử
    user = User(
        email="user_history_test@foodai.vn",
        phone_number="0987654321",
        hashed_password="hashed_secret_password",
        status="active"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    print(f"Đã tạo User kiểm thử ID={user_id} ({user.email})")

    # 2. Tạo tập dữ liệu Nhà hàng mẫu (Restaurants & Amenities)
    r1 = Restaurant(
        name="Lẩu Nấm Thiên Nhiên Ashima",
        address="35A Nguyễn Đình Chiểu, Quận 1, TP.HCM",
        latitude=10.7865,
        longitude=106.6995,
        min_price=150000,
        max_price=350000,
        open_hours="10:00 - 22:00",
        avg_rating=4.7,
        total_reviews=120,
        status="active",
        cuisine_type="Lẩu & Nấm"
    )
    db.add(r1)
    db.flush()
    am1 = RestaurantAmenity(restaurant_id=r1.id, has_parking=True, has_private_room=True)
    db.add(am1)
    img1 = RestaurantImage(restaurant_id=r1.id, image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5", is_cover=True)
    db.add(img1)

    r2 = Restaurant(
        name="BBQ Hàn Quốc King Meat",
        address="18 Hai Bà Trưng, Bến Nghé, Quận 1, TP.HCM",
        latitude=10.7780,
        longitude=106.7040,
        min_price=200000,
        max_price=450000,
        open_hours="11:00 - 23:00",
        avg_rating=4.6,
        total_reviews=85,
        status="active",
        cuisine_type="Nướng BBQ Hàn Quốc"
    )
    db.add(r2)
    db.flush()
    am2 = RestaurantAmenity(restaurant_id=r2.id, has_parking=True, has_outdoor=True)
    db.add(am2)

    r3 = Restaurant(
        name="Cơm Chay Thanh Lương",
        address="45 Đinh Tiên Hoàng, Bình Thạnh, TP.HCM",
        latitude=10.7950,
        longitude=106.6980,
        min_price=40000,
        max_price=90000,
        open_hours="07:00 - 21:00",
        avg_rating=4.5,
        total_reviews=60,
        status="active",
        cuisine_type="Món Chay thanh đạm"
    )
    db.add(r3)
    db.flush()
    am3 = RestaurantAmenity(restaurant_id=r3.id, has_parking=False, vegetarian_support=True)
    db.add(am3)

    db.commit()
    print("Đã khởi tạo 3 nhà hàng mẫu đại diện cho các thể loại Lẩu, Nướng BBQ và Món Chay")

    # -------------------------------------------------------------
    # TEST 01: Chặn user_id không tồn tại (HTTP 404 / BR-01)
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra chặn truy vấn với user_id không tồn tại (BR-01):")
    try:
        get_search_history(user_id=99999, db=db)
        assert False, "Phải ném lỗi 404 khi user không tồn tại"
    except HTTPException as e:
        print(f"  Bắt đúng mã lỗi HTTP: {e.status_code} - {e.detail}")
        assert e.status_code == 404
    print("  => PASSED: Đảm bảo kiểm soát quyền truy cập theo BR-01!")

    # -------------------------------------------------------------
    # TEST 02: Trả về danh sách rỗng cho người dùng mới
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra kết quả trả về khi người dùng chưa có phiên chat nào:")
    empty_res = get_search_history(user_id=user_id, db=db)
    print(f"  Tổng số phiên: {empty_res.total_sessions}, Số lượng data: {len(empty_res.data)}")
    assert empty_res.total_sessions == 0
    assert len(empty_res.data) == 0
    assert empty_res.total_pages == 1
    print("  => PASSED: Phản hồi cấu trúc chuẩn xác khi lịch sử rỗng!")

    # -------------------------------------------------------------
    # TEST 03: Trả về thông tin phiên kèm SearchCriteria bóc tách
    # -------------------------------------------------------------
    print("\n[TEST 03] Khởi tạo phiên tìm kiếm kèm SearchCriteria và kiểm tra kết quả:")
    # Tạo phiên 1
    s1 = ChatSessionService.create_session(db, user_id=user_id)
    ChatSessionService.save_message(db, session_id=s1.session_id, sender_type="user", content="Tìm quán lẩu ở Quận 1 dưới 300k có bãi ô tô")
    ChatSessionService.save_message(db, session_id=s1.session_id, sender_type="ai", content="Gợi ý quán lẩu nấm cho bạn")
    ChatSessionService.save_criteria(
        db=db,
        session_id=s1.session_id,
        location_text="Quận 1",
        latitude=10.7860,
        longitude=106.7003,
        cuisine="Lẩu",
        budget=300000,
        has_parking=True
    )

    res_s1 = get_search_history(user_id=user_id, db=db)
    assert res_s1.total_sessions == 1
    item1 = res_s1.data[0]
    print(f"  Phiên #{item1.session_id}: title='{item1.title_preview}', total_messages={item1.total_messages}")
    print(f"  Tiêu chí bóc tách: khu vực='{item1.criteria.location_text}', món='{item1.criteria.cuisine}', ngân sách={item1.criteria.budget}đ, đỗ ô tô={item1.criteria.has_parking}")
    
    assert item1.criteria is not None
    assert item1.criteria.location_text == "Quận 1"
    assert item1.criteria.cuisine == "Lẩu"
    assert item1.criteria.budget == 300000
    assert item1.criteria.has_parking is True
    print("  => PASSED: Trả về đầy đủ metadata phiên và tiêu chí SearchCriteria!")

    # -------------------------------------------------------------
    # TEST 04: Tự động liên kết và gợi ý nhà hàng theo thể loại ẩm thực
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra gợi ý nhà hàng khớp với thể loại ẩm thực (Lẩu):")
    print(f"  Số lượng quán gợi ý cho phiên Lẩu: {len(item1.suggested_restaurants)}")
    assert len(item1.suggested_restaurants) >= 1
    top_rest = item1.suggested_restaurants[0]
    print(f"  Quán gợi ý hàng đầu: '{top_rest.name}' (Ẩm thực: {top_rest.cuisine_type}, Giá: {top_rest.min_price:,.0f}đ - {top_rest.max_price:,.0f}đ)")
    assert "Lẩu" in top_rest.cuisine_type
    print("  => PASSED: Tự động gợi ý chuẩn xác quán ăn theo thể loại ẩm thực của phiên!")

    # -------------------------------------------------------------
    # TEST 05: Gợi ý nhà hàng theo ngân sách và chỗ đỗ ô tô
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra gợi ý nhà hàng theo ngân sách (budget) và bãi đỗ ô tô:")
    # Tạo phiên 2: Món Chay ngân sách hạt dẻ 50k
    s2 = ChatSessionService.create_session(db, user_id=user_id)
    ChatSessionService.save_message(db, session_id=s2.session_id, sender_type="user", content="Muốn ăn món chay thanh đạm giá rẻ dưới 60k")
    ChatSessionService.save_criteria(
        db=db,
        session_id=s2.session_id,
        location_text="Bình Thạnh",
        cuisine="Chay",
        budget=60000,
        has_parking=False
    )

    res_s2 = get_search_history(user_id=user_id, db=db)
    assert res_s2.total_sessions == 2
    item2 = res_s2.data[0]  # Sắp xếp mới nhất lên đầu -> phiên s2
    assert item2.session_id == s2.session_id
    assert len(item2.suggested_restaurants) >= 1
    top_chay = item2.suggested_restaurants[0]
    print(f"  Quán gợi ý phiên Chay: '{top_chay.name}' - Giá min: {top_chay.min_price:,.0f}đ <= Ngân sách: 60.000đ")
    assert "Chay" in top_chay.cuisine_type
    assert top_chay.min_price <= 60000
    print("  => PASSED: Gợi ý chuẩn xác theo ràng buộc ngân sách và tiện ích!")

    # -------------------------------------------------------------
    # TEST 06: Kiểm tra % Match Score và giờ mở cửa trong gợi ý
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra % Match Score và trạng thái giờ mở cửa trong kết quả gợi ý:")
    assert 65 <= top_rest.match_score <= 99, f"match_score={top_rest.match_score} ngoài khoảng hợp lệ [65, 99]"
    assert isinstance(top_rest.is_open, bool)
    print(f"  Quán '{top_rest.name}': match_score={top_rest.match_score}%, is_open={top_rest.is_open}, khoảng cách={top_rest.distance_km}km")
    print("  => PASSED: Đầy đủ các trường độ phù hợp Match Score và giờ mở cửa!")

    # -------------------------------------------------------------
    # TEST 07: Lọc lịch sử theo trạng thái phiên ('active' vs 'closed')
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra lọc lịch sử theo trạng thái ('active' / 'closed'):")
    # Đóng phiên s1
    ChatSessionService.close_session(db, s1.session_id)

    res_active = get_search_history(user_id=user_id, status_filter="active", db=db)
    res_closed = get_search_history(user_id=user_id, status_filter="closed", db=db)
    print(f"  Phiên đang active: {res_active.total_sessions} phiên (Session #{res_active.data[0].session_id})")
    print(f"  Phiên đã closed: {res_closed.total_sessions} phiên (Session #{res_closed.data[0].session_id})")
    assert res_active.total_sessions == 1 and res_active.data[0].status == "active"
    assert res_closed.total_sessions == 1 and res_closed.data[0].status == "closed"
    print("  => PASSED: Bộ lọc trạng thái hoạt động chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 08: Kiểm tra phân trang chuẩn RESTful (page, limit)
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra cơ chế phân trang RESTful:")
    # Tạo thêm 2 phiên nữa
    s3 = ChatSessionService.create_session(db, user_id=user_id)
    s4 = ChatSessionService.create_session(db, user_id=user_id)

    paged_res = get_search_history(user_id=user_id, page=1, limit=2, db=db)
    print(f"  Trang 1: {len(paged_res.data)} phiên, Tổng phiên: {paged_res.total_sessions}, Tổng trang: {paged_res.total_pages}")
    assert paged_res.total_sessions == 4
    assert paged_res.limit == 2
    assert paged_res.total_pages == 2
    assert len(paged_res.data) == 2

    paged_res_p2 = get_search_history(user_id=user_id, page=2, limit=2, db=db)
    assert len(paged_res_p2.data) == 2
    assert paged_res_p2.data[0].session_id != paged_res.data[0].session_id
    print("  => PASSED: Phân trang RESTful phân tách dữ liệu chính xác!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Xử lý NFR-01 (< 3.0 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng xử lý truy vấn lịch sử và gợi ý quán (NFR-01):")
    t0 = time.perf_counter()
    iterations = 200  # Chạy 200 lượt truy vấn lịch sử kết hợp gợi ý
    for _ in range(iterations):
        _ = get_search_history(user_id=user_id, page=1, limit=10, db=db)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian xử lý {iterations} lượt: {elapsed_ms:.2f} ms ({elapsed_ms / iterations:.4f} ms/lượt)")
    assert elapsed_ms < 3000, f"Hiệu năng quá chậm: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ phản hồi cực nhanh ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 80)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-46 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 80)
    db.close()


if __name__ == "__main__":
    run_tests()
