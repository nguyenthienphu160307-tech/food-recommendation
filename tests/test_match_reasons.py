"""
Bộ kiểm thử Tự động cho Task TSK-40 / PBI-11:
Hiển thị nhãn Độ phù hợp (% Match Score) & Lý do đề xuất trên từng thẻ quán
Mô tả: Sinh các tag trực quan trên giao diện (VD: 'Khớp 95% • Cách 1.2km • Có bãi ô tô • Trong tầm giá 250k') giúp người dùng dễ ra quyết định.

9 Ca kiểm thử toàn diện:
1. TEST 01: Tính khoảng cách GPS bằng công thức Haversine (calculate_distance_km).
2. TEST 02: Thuật toán % Match Score Weighted Scoring (BR-05: 35% Dist + 25% Rating + 25% Amenities + 15% Open).
3. TEST 03: Điểm thưởng ưu thế của quán đang mở cửa (BR-03 & BR-05).
4. TEST 04: Tự động sinh Tag khoảng cách & Tag trạng thái mở cửa thực tế (BR-03).
5. TEST 05: Tự động sinh Tag ngân sách giá & Tiện ích nổi bật (ô tô, phòng riêng, ngoài trời, chay).
6. TEST 06: Tự động sinh Tag đánh giá sao & thể loại món ăn.
7. TEST 07: Định dạng câu tóm tắt đề xuất một dòng (One-line Recommendation Summary).
8. TEST 08: Tích hợp API Backend GET /api/restaurants trả về match_score, match_reasons, recommendation_summary.
9. TEST 09: Benchmark hiệu năng tính toán và sinh tag hàng loạt đạt chuẩn NFR-01 (< 3.0s).
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

from app.core.database import Base
import app.models
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.services.open_hours_service import get_vietnam_now, VIETNAM_TZ
from app.services.recommendation_service import (
    calculate_distance_km,
    calculate_match_score,
    generate_match_reasons,
    generate_recommendation_summary,
    DEFAULT_USER_LAT,
    DEFAULT_USER_LON,
)
from app.routers.restaurant import get_restaurants, get_restaurant_detail

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
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-40: ĐỘ PHÙ HỢP (% MATCH) & LÝ DO ĐỀ XUẤT")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    # -------------------------------------------------------------
    # TEST 01: Tính khoảng cách GPS Haversine
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra độ chính xác của công thức Haversine (calculate_distance_km):")
    # Nhà thờ Đức Bà (10.77978, 106.69901) đến Chợ Bến Thành (10.77254, 106.69803) ~0.8km - 0.9km
    dist = calculate_distance_km(10.77978, 106.69901, 10.77254, 106.69803)
    print(f"  Khoảng cách tính toán giữa Nhà thờ Đức Bà & Chợ Bến Thành: {dist} km")
    assert 0.7 <= dist <= 1.0, f"Khoảng cách {dist} km phải nằm trong khoảng 0.7 - 1.0 km"
    
    # Hai vị trí trùng nhau
    zero_dist = calculate_distance_km(10.8231, 106.6900, 10.8231, 106.6900)
    assert zero_dist == 0.0, f"Khoảng cách trùng nhau phải bằng 0, nhận được: {zero_dist}"
    print("  => PASSED: Công thức Haversine tính toán chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 02: Thuật toán % Match Score Weighted Scoring (BR-05)
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra công thức Weighted Scoring % Match Score (BR-05):")
    class DummyAmenities:
        has_parking = True
        has_private_room = True
        has_outdoor = True
        pet_friendly = True
        vegetarian_support = True

    # Quán lý tưởng: 0.1km, 5 sao, full tiện ích, đang mở
    perfect_score = calculate_match_score(
        distance_km=0.1,
        avg_rating=5.0,
        amenities=DummyAmenities(),
        is_open=True,
    )
    print(f"  Điểm quán lý tưởng: {perfect_score}% (Kỳ vọng: 95% - 99%)")
    assert 95 <= perfect_score <= 99, f"Điểm lý tưởng {perfect_score}% không hợp lệ"

    # Quán xa (20km), rating thấp (1.0), không tiện ích, đóng cửa
    min_score = calculate_match_score(
        distance_km=20.0,
        avg_rating=1.0,
        amenities=None,
        is_open=False,
    )
    print(f"  Điểm sàn tối thiểu: {min_score}% (Kỳ vọng: 65% - 75%)")
    assert 65 <= min_score <= 75, f"Điểm sàn {min_score}% không hợp lệ"
    print("  => PASSED: Thang điểm dao động chuẩn xác trong khoảng 65% - 99% theo BR-05!")

    # -------------------------------------------------------------
    # TEST 03: Điểm thưởng ưu thế của quán đang mở cửa (BR-03 & BR-05)
    # -------------------------------------------------------------
    print("\n[TEST 03] Kiểm tra điểm cộng ưu tiên cho quán đang mở cửa (15% trọng số):")
    score_open = calculate_match_score(distance_km=2.0, avg_rating=4.5, amenities=None, is_open=True)
    score_closed = calculate_match_score(distance_km=2.0, avg_rating=4.5, amenities=None, is_open=False)
    diff = score_open - score_closed
    print(f"  Điểm khi mở cửa: {score_open}% | Điểm khi đóng cửa: {score_closed}% | Chênh lệch: +{diff}%")
    assert diff >= 5, f"Quán mở cửa phải chênh ít nhất 5% điểm, nhận được chênh lệch: {diff}%"
    print("  => PASSED: Quán đang mở cửa được cộng điểm ưu thế xếp hạng rõ rệt!")

    # -------------------------------------------------------------
    # TEST 04: Sinh Tag Khoảng cách & Giờ mở cửa thực tế
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra sinh tag Khoảng cách & Giờ mở cửa thực tế:")
    class MockRestaurantNear:
        latitude = 10.7865
        longitude = 106.7005
        open_hours = "08:00 - 22:00"
        min_price = 50000
        max_price = 150000
        avg_rating = 4.6
        total_reviews = 50
        cuisine_type = "Món Việt"
        amenities = None

    reasons_near = generate_match_reasons(
        MockRestaurantNear(),
        user_lat=10.7860,
        user_lon=106.7003,
        is_open=True,
    )
    print(f"  Tags sinh ra (quán gần): {reasons_near}")
    assert any("Rất gần bạn" in r or "Cách" in r for r in reasons_near), "Thiếu tag khoảng cách"
    assert any("Đang mở cửa" in r for r in reasons_near), "Thiếu tag đang mở cửa"
    print("  => PASSED: Sinh tag khoảng cách và giờ mở cửa thành công!")

    # -------------------------------------------------------------
    # TEST 05: Sinh Tag Mức giá & Tiện ích nổi bật
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra sinh tag Ngân sách & Tiện ích (ô tô, phòng riêng, chay):")
    class MockAmenities:
        has_parking = True
        has_private_room = True
        has_outdoor = False
        pet_friendly = False
        vegetarian_support = True

    class MockRestaurantAmenity:
        latitude = 10.7860
        longitude = 106.7003
        open_hours = "10:00 - 22:00"
        min_price = 100000
        max_price = 250000  # 250k
        avg_rating = 4.3
        total_reviews = 30
        cuisine_type = "Lẩu & Nướng"
        amenities = MockAmenities()

    reasons_am = generate_match_reasons(MockRestaurantAmenity(), is_open=True)
    print(f"  Tags sinh ra: {reasons_am}")
    assert any("250k" in r for r in reasons_am), "Thiếu tag Trong tầm giá 250k"
    assert any("ô tô" in r for r in reasons_am), "Thiếu tag Có chỗ đỗ ô tô"
    assert any("phòng riêng" in r for r in reasons_am), "Thiếu tag Có phòng riêng yên tĩnh"
    print("  => PASSED: Tag ngân sách và tiện ích sinh đúng theo dữ liệu quán!")

    # -------------------------------------------------------------
    # TEST 06: Sinh Tag Đánh giá sao & Thể loại ẩm thực
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra sinh tag Đánh giá sao & Thể loại ẩm thực:")
    class MockRestaurantHighRating:
        latitude = 10.7860
        longitude = 106.7003
        open_hours = "11:00 - 23:00"
        min_price = 200000
        max_price = 450000
        avg_rating = 4.8
        total_reviews = 350
        cuisine_type = "Ẩm thực Nhật Bản"
        amenities = None

    reasons_hr = generate_match_reasons(MockRestaurantHighRating(), is_open=False)
    print(f"  Tags sinh ra: {reasons_hr}")
    assert any("4.8★" in r or "Đánh giá xuất sắc" in r for r in reasons_hr), "Thiếu tag đánh giá xuất sắc"
    assert any("đông khách" in r for r in reasons_hr), "Thiếu tag đông khách"
    print("  => PASSED: Tag đánh giá và ẩm thực sinh chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 07: Định dạng One-line Recommendation Summary
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra dòng tóm tắt đề xuất một dòng (One-line Summary):")
    sample_tags = [
        "📍 Cách 1.2km (~4p đi xe)",
        "🟢 Đang mở cửa đón khách",
        "🚗 Có chỗ đỗ ô tô",
        "💵 Trong tầm giá 250k"
    ]
    summary = generate_recommendation_summary(95, sample_tags)
    print(f"  Câu tóm tắt sinh ra: '{summary}'")
    assert summary.startswith("Khớp 95%"), "Tóm tắt phải bắt đầu bằng 'Khớp 95%'"
    assert "•" in summary, "Tóm tắt phải có dấu chấm phân cách '•'"
    assert "Cách 1.2km" in summary, "Tóm tắt phải chứa khoảng cách"
    assert "Có chỗ đỗ ô tô" in summary, "Tóm tắt phải chứa tiện ích"
    print("  => PASSED: Dòng tóm tắt 1 dòng được sinh gọn gàng, súc tích!")

    # -------------------------------------------------------------
    # TEST 08: Tích hợp API GET /api/restaurants trả về Match Fields
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra tích hợp API RESTful GET /api/restaurants:")
    # Seed dữ liệu nhà hàng
    r1 = Restaurant(
        name="Nhà hàng Gạo Nếp Món Việt",
        address="33 Lê Duẩn, Bến Nghé, Quận 1, TP.HCM",
        latitude=10.7810,
        longitude=106.7005,
        min_price=120000,
        max_price=350000,
        open_hours="08:00 - 22:30",
        avg_rating=4.7,
        total_reviews=210,
        status="active",
        cuisine_type="Ẩm thực Việt Nam"
    )
    db.add(r1)
    db.flush()

    am1 = RestaurantAmenity(
        restaurant_id=r1.id,
        has_parking=True,
        has_private_room=True,
        has_outdoor=True,
        pet_friendly=False,
        vegetarian_support=True
    )
    db.add(am1)

    img1 = RestaurantImage(
        restaurant_id=r1.id,
        image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
        is_cover=True
    )
    db.add(img1)
    db.commit()

    # Gọi hàm router get_restaurants
    res = get_restaurants(
        page=1,
        limit=10,
        status_filter="active",
        user_lat=10.7860,
        user_lon=106.7003,
        db=db
    )
    assert len(res.data) >= 1, "API phải trả về ít nhất 1 nhà hàng"
    item = res.data[0]
    print(f"  Nhà hàng ID={item.id} - '{item.name}':")
    print(f"    % Match Score: {item.match_score}%")
    print(f"    Khoảng cách GPS: {item.distance_km} km")
    print(f"    Lý do đề xuất: {item.match_reasons}")
    print(f"    Tóm tắt đề xuất: {item.recommendation_summary}")

    assert 65 <= item.match_score <= 99, f"match_score={item.match_score} ngoài khoảng hợp lệ"
    assert isinstance(item.match_reasons, list) and len(item.match_reasons) > 0, "match_reasons không được rỗng"
    assert item.recommendation_summary is not None and "Khớp" in item.recommendation_summary
    assert item.distance_km is not None
    print("  => PASSED: API đồng bộ đầy đủ các trường Match Score & Match Reasons!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Xử lý Đề xuất NFR-01 (< 3 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng tính toán và sinh lý do đề xuất (NFR-01):")
    t0 = time.perf_counter()
    iterations = 1000  # Chạy 1.000 lượt tính toán đề xuất
    for i in range(iterations):
        _ = calculate_match_score(distance_km=1.5, avg_rating=4.6, amenities=am1, is_open=True)
        _ = generate_match_reasons(r1, user_lat=10.7860, user_lon=106.7003, is_open=True)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian xử lý {iterations} lượt: {elapsed_ms:.2f} ms ({elapsed_ms / iterations:.4f} ms/lượt)")
    assert elapsed_ms < 1000, f"Hiệu năng tính toán quá chậm: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ siêu tốc ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 80)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-40 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 80)
    db.close()


if __name__ == "__main__":
    run_tests()
