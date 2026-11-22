"""
Bộ kiểm thử tự động cho Task TSK-37:
Xây dựng Bộ kiểm tra Giờ mở cửa hoạt động thực tế (BR-03 / PBI-11)
Module 4: Lọc, gợi ý và xếp hạng nhà hàng

Kiểm tra toàn diện:
1. Khung giờ tiêu chuẩn trong ngày (Standard shift)
2. Khung giờ mở xuyên đêm (Cross-midnight / Overnight)
3. Khung giờ ca gãy / nghỉ trưa (Split shifts)
4. Quán mở cửa cả ngày (24/7 / All day)
5. Xử lý an toàn khi không có giờ mở cửa (None / Empty)
6. Quy chuẩn múi giờ Việt Nam (Asia/Ho_Chi_Minh GMT+7)
7. Cơ chế cộng điểm thưởng ưu tiên xếp hạng (Ranking Bonus - BR-03 & BR-05)
8. Tích hợp API Endpoint GET /api/restaurants/{id}/open-status
9. Benchmark hiệu năng bóc tách thời gian (< 3s - NFR-01)
"""
import sys
import os
import time
from datetime import datetime, time as dtime, timezone, timedelta

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
from app.models.restaurant import Restaurant, RestaurantAmenity
from app.services.open_hours_service import (
    normalize_time_str,
    parse_open_hours_intervals,
    check_restaurant_open_status,
    calculate_open_hours_bonus,
    get_vietnam_now,
    VIETNAM_TZ,
    DEFAULT_OPEN_BONUS_WEIGHT,
)
from app.routers.restaurant import get_restaurants, get_restaurant_open_status

# Khởi tạo SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def seed_test_data(db):
    """Khởi tạo các nhà hàng mẫu với nhiều định dạng giờ mở cửa đa dạng"""
    db.query(RestaurantAmenity).delete()
    db.query(Restaurant).delete()
    db.commit()

    # Quán 1: Giờ tiêu chuẩn (08:00 - 22:00)
    r1 = Restaurant(
        id=1,
        name="Cơm Niêu Sài Gòn Xưa",
        address="27 Tú Xương, Quận 3, TP.HCM",
        latitude=10.7760,
        longitude=106.6910,
        min_price=80000.0,
        max_price=250000.0,
        open_hours="08:00 - 22:00",
        avg_rating=4.7,
        total_reviews=180,
        status="active"
    )

    # Quán 2: Giờ mở xuyên đêm (18:00 - 02:00)
    r2 = Restaurant(
        id=2,
        name="Quán Nướng & Beer Về Đêm",
        address="150 Bùi Viện, Quận 1, TP.HCM",
        latitude=10.7675,
        longitude=106.6930,
        min_price=120000.0,
        max_price=350000.0,
        open_hours="18:00 - 02:00",
        avg_rating=4.5,
        total_reviews=95,
        status="active"
    )

    # Quán 3: Ca gãy nghỉ trưa (10:00 - 14:00, 17:00 - 22:00)
    r3 = Restaurant(
        id=3,
        name="Ẩm Thực Chay Thanh Tịnh",
        address="45 Đinh Tiên Hoàng, Quận 1, TP.HCM",
        latitude=10.7890,
        longitude=106.6990,
        min_price=60000.0,
        max_price=180000.0,
        open_hours="10:00 - 14:00, 17:00 - 22:00",
        avg_rating=4.9,
        total_reviews=320,
        status="active"
    )

    # Quán 4: Mở cửa 24/7
    r4 = Restaurant(
        id=4,
        name="Phở Đêm 24/7 Chợ Bến Thành",
        address="12 Lê Lai, Quận 1, TP.HCM",
        latitude=10.7720,
        longitude=106.6980,
        min_price=55000.0,
        max_price=95000.0,
        open_hours="24/7",
        avg_rating=4.4,
        total_reviews=410,
        status="active"
    )

    # Quán 5: Không có giờ mở cửa (None)
    r5 = Restaurant(
        id=5,
        name="Quán Ăn Gia Đình Vỉa Hè",
        address="99 Nguyễn Trãi, Quận 5, TP.HCM",
        latitude=10.7550,
        longitude=106.6750,
        min_price=40000.0,
        max_price=90000.0,
        open_hours=None,
        avg_rating=4.2,
        total_reviews=50,
        status="active"
    )

    db.add_all([r1, r2, r3, r4, r5])
    db.commit()


def run_tests():
    print("=" * 75)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ GIỜ MỞ CỬA HOẠT ĐỘNG THỰC TẾ (BR-03 / TSK-37)")
    print("=" * 75)

    db = TestingSessionLocal()
    seed_test_data(db)

    # -------------------------------------------------------------
    # TEST 01: Khung giờ tiêu chuẩn trong ngày (Standard Shift: 08:00 - 22:00)
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra khung giờ tiêu chuẩn trong ngày (08:00 - 22:00):")
    h_str = "08:00 - 22:00"
    
    # 1. Lúc 11:30 trưa -> Đang mở cửa
    st_noon = check_restaurant_open_status(h_str, datetime(2026, 11, 17, 11, 30, tzinfo=VIETNAM_TZ))
    assert st_noon["is_open"] is True, "11:30 phải đang mở cửa"
    assert st_noon["status_code"] == "OPEN"
    assert "22:00" in st_noon["detail_text"]
    
    # 2. Lúc 07:15 sáng -> Chưa mở cửa
    st_morning = check_restaurant_open_status(h_str, datetime(2026, 11, 17, 7, 15, tzinfo=VIETNAM_TZ))
    assert st_morning["is_open"] is False, "07:15 phải là đã đóng cửa"
    assert "08:00" in st_morning["detail_text"]

    # 3. Lúc 23:00 đêm -> Đã đóng cửa
    st_night = check_restaurant_open_status(h_str, datetime(2026, 11, 17, 23, 0, tzinfo=VIETNAM_TZ))
    assert st_night["is_open"] is False, "23:00 phải là đã đóng cửa"

    print("  Đã kiểm tra: 11:30 (Mở cửa) | 07:15 (Đóng, mở lúc 08:00) | 23:00 (Đã đóng cửa)")
    print("  => PASSED: Khung giờ tiêu chuẩn trong ngày hoạt động chuẩn xác 100%!")

    # -------------------------------------------------------------
    # TEST 02: Khung giờ mở xuyên đêm (Cross-midnight: 18:00 - 02:00)
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra khung giờ mở xuyên đêm (18:00 - 02:00 sáng hôm sau):")
    night_str = "18:00 - 02:00"
    
    # Lúc 23:45 đêm hôm trước -> Mở cửa
    st_pre_midnight = check_restaurant_open_status(night_str, datetime(2026, 11, 17, 23, 45, tzinfo=VIETNAM_TZ))
    assert st_pre_midnight["is_open"] is True, "23:45 phải đang mở cửa"
    
    # Lúc 01:15 sáng hôm sau -> Vẫn mở cửa
    st_post_midnight = check_restaurant_open_status(night_str, datetime(2026, 11, 18, 1, 15, tzinfo=VIETNAM_TZ))
    assert st_post_midnight["is_open"] is True, "01:15 sáng phải đang mở cửa"

    # Lúc 03:00 sáng -> Đã đóng cửa
    st_late = check_restaurant_open_status(night_str, datetime(2026, 11, 18, 3, 0, tzinfo=VIETNAM_TZ))
    assert st_late["is_open"] is False, "03:00 sáng phải đã đóng cửa"

    # Lúc 14:00 chiều -> Đã đóng cửa
    st_afternoon = check_restaurant_open_status(night_str, datetime(2026, 11, 18, 14, 0, tzinfo=VIETNAM_TZ))
    assert st_afternoon["is_open"] is False, "14:00 chiều phải đã đóng cửa"

    print("  Đã kiểm tra: 23:45 (Mở) | 01:15 (Mở) | 03:00 (Đóng) | 14:00 (Đóng)")
    print("  => PASSED: Khung giờ mở xuyên đêm qua 00:00 được xử lý hoàn hảo!")

    # -------------------------------------------------------------
    # TEST 03: Khung giờ ca gãy / nghỉ trưa (10:00 - 14:00, 17:00 - 22:00)
    # -------------------------------------------------------------
    print("\n[TEST 03] Kiểm tra khung giờ nhiều ca gãy (10:00 - 14:00, 17:00 - 22:00):")
    split_str = "10:00 - 14:00, 17:00 - 22:00"
    
    # 1. Ca trưa lúc 12:00 -> Mở cửa
    st_lunch = check_restaurant_open_status(split_str, datetime(2026, 11, 17, 12, 0, tzinfo=VIETNAM_TZ))
    assert st_lunch["is_open"] is True, "12:00 phải đang mở cửa ca trưa"

    # 2. Giờ nghỉ trưa lúc 15:30 -> Đã đóng cửa, thông báo mở lại lúc 17:00
    st_break = check_restaurant_open_status(split_str, datetime(2026, 11, 17, 15, 30, tzinfo=VIETNAM_TZ))
    assert st_break["is_open"] is False, "15:30 phải là giờ nghỉ trưa"
    assert "17:00" in st_break["detail_text"], "Phải thông báo mở lại lúc 17:00"

    # 3. Ca tối lúc 19:30 -> Mở cửa
    st_dinner = check_restaurant_open_status(split_str, datetime(2026, 11, 17, 19, 30, tzinfo=VIETNAM_TZ))
    assert st_dinner["is_open"] is True, "19:30 phải đang mở cửa ca tối"

    print("  Đã kiểm tra: 12:00 (Mở ca trưa) | 15:30 (Nghỉ trưa, mở lại 17:00) | 19:30 (Mở ca tối)")
    print("  => PASSED: Ca gãy nghỉ trưa được bóc tách và thông báo giờ mở lại chính xác!")

    # -------------------------------------------------------------
    # TEST 04: Quán mở cửa 24/7 hoặc mở cả ngày
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra quán mở cửa 24/7 / Cả ngày:")
    all_day_cases = ["24/7", "24/24", "Mở cả ngày", "00:00 - 24:00", "cả ngày"]
    for case in all_day_cases:
        res = check_restaurant_open_status(case, datetime(2026, 11, 17, 3, 30, tzinfo=VIETNAM_TZ))
        assert res["is_open"] is True, f"Trường hợp '{case}' phải luôn mở cửa"
        assert res["status_code"] in ["OPEN", "OPEN_24_7"]
    print(f"  Đã kiểm tra thành công các định dạng: {all_day_cases}")
    print("  => PASSED: Quán mở cửa 24/7 luôn trả về trạng thái mở cửa tại mọi khung giờ!")

    # -------------------------------------------------------------
    # TEST 05: Dữ liệu giờ trống, None hoặc chuỗi không hợp lệ
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra xử lý an toàn dữ liệu rỗng / None (Fault-tolerant):")
    invalid_cases = [None, "", "   ", "Chưa cập nhật", "Liên hệ quán"]
    for inv in invalid_cases:
        res = check_restaurant_open_status(inv, datetime(2026, 11, 17, 12, 0, tzinfo=VIETNAM_TZ))
        assert res["is_open"] is False
        assert res["status_code"] == "UNKNOWN"
        assert res["bonus_score"] == 0.0
    print("  Đã kiểm tra an toàn với: None, chuỗi rỗng và chuỗi không có số")
    print("  => PASSED: Hệ thống xử lý an toàn tuyệt đối, không gây crash server!")

    # -------------------------------------------------------------
    # TEST 06: Kiểm tra Quy chuẩn Múi giờ Việt Nam (Asia/Ho_Chi_Minh UTC+7)
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra múi giờ chuẩn Việt Nam (UTC+7):")
    vn_now = get_vietnam_now()
    assert vn_now.tzinfo is not None, "Thời gian trả về phải có thông tin timezone"
    utc_offset = vn_now.utcoffset()
    assert utc_offset == timedelta(hours=7), f"Offset phải là +7:00, thực tế: {utc_offset}"
    print(f"  Thời gian hiện tại tại Việt Nam: {vn_now.strftime('%Y-%m-%d %H:%M:%S %Z')} (Offset: +07:00)")
    print("  => PASSED: Múi giờ luôn khớp chuẩn giờ sinh hoạt tại Việt Nam!")

    # -------------------------------------------------------------
    # TEST 07: Quy tắc Điểm thưởng Ưu tiên Xếp hạng (Ranking Bonus - BR-03 & BR-05)
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra cơ chế tính điểm thưởng xếp hạng BR-03:")
    bonus_open = calculate_open_hours_bonus("08:00 - 22:00", datetime(2026, 11, 17, 12, 0, tzinfo=VIETNAM_TZ))
    bonus_closed = calculate_open_hours_bonus("08:00 - 22:00", datetime(2026, 11, 17, 23, 0, tzinfo=VIETNAM_TZ))
    assert bonus_open == DEFAULT_OPEN_BONUS_WEIGHT, f"Kỳ vọng {DEFAULT_OPEN_BONUS_WEIGHT}, thực tế: {bonus_open}"
    assert bonus_closed == 0.0, f"Quán đóng cửa phải có điểm thưởng = 0, thực tế: {bonus_closed}"
    print(f"  Quán đang mở cửa: Bonus = +{bonus_open} điểm (BR-03)")
    print(f"  Quán đang đóng cửa: Bonus = {bonus_closed} điểm")
    print("  => PASSED: Thuật toán cộng điểm ưu tiên xếp hạng BR-03 hoạt động chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 08: Kiểm tra Tích hợp API Endpoint (GET /api/restaurants & open-status)
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra tích hợp API Endpoint trả về thông tin giờ mở cửa:")
    # 1. Kiểm tra API chi tiết trạng thái giờ mở cửa
    status_r4 = get_restaurant_open_status(restaurant_id=4, db=db)
    assert status_r4.is_open is True, "Quán 24/7 (ID=4) phải có is_open=True"
    assert status_r4.bonus_score > 0
    assert status_r4.restaurant_name == "Phở Đêm 24/7 Chợ Bến Thành"
    print(f"  API /open-status Quán 4: {status_r4.restaurant_name} => {status_r4.status_label} ({status_r4.detail_text})")

    # 2. Kiểm tra API danh sách quán có trả về is_open và lọc open_now
    list_all = get_restaurants(page=1, limit=10, db=db)
    assert len(list_all.data) == 5
    for item in list_all.data:
        assert hasattr(item, "is_open")
        assert hasattr(item, "open_status_label")
        assert hasattr(item, "open_status_detail")
        assert hasattr(item, "ranking_bonus")

    # 3. Kiểm tra lọc open_now=True
    list_open = get_restaurants(page=1, limit=10, open_now=True, db=db)
    assert all(item.is_open is True for item in list_open.data), "Tất cả quán trong list_open phải có is_open=True"
    print(f"  API GET /api/restaurants: Đã nạp {len(list_all.data)} quán kèm is_open; Lọc open_now=True: {len(list_open.data)} quán")
    print("  => PASSED: API đồng bộ đầy đủ các trường dữ liệu và hỗ trợ lọc theo giờ mở cửa!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Xử lý Giờ mở cửa NFR-01 (< 3 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng xử lý hàng loạt giờ mở cửa (NFR-01):")
    sample_hours = [
        "08:00 - 22:00",
        "18:00 - 02:00",
        "10:00 - 14:00, 17:00 - 22:00",
        "24/7",
        None,
        "09:30 - 23:00",
        "8h - 22h",
        "7:00 AM - 10:00 PM"
    ]
    t0 = time.perf_counter()
    iterations = 2000  # Chạy 2.000 lượt kiểm tra
    now_test = get_vietnam_now()
    for i in range(iterations):
        _ = check_restaurant_open_status(sample_hours[i % len(sample_hours)], now_test)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian bóc tách {iterations} lượt: {elapsed_ms:.2f} ms ({elapsed_ms / iterations:.4f} ms/lượt)")
    assert elapsed_ms < 1000, f"Hiệu năng quá chậm: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ siêu tốc ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 75)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-37 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 75)
    db.close()


if __name__ == "__main__":
    run_tests()
