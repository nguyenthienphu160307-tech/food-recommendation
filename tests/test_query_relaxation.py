"""
==============================================================================
TEST SUITE: CƠ CHẾ TỰ ĐỘNG NỚI LỎNG ĐIỀU KIỆN (QUERY RELAXATION - TASK TE9C66F)
==============================================================================
Kiểm thử toàn diện các yêu cầu nghiệp vụ của Task TE9C66F (UC-02 Ngoại lệ):
1. Tự động mở rộng bán kính (+3.0 km) khi 0 kết quả trong bán kính ban đầu.
2. Tự động nới khoảng ngân sách (±25%) khi mức giá ban đầu quá thấp.
3. Không nới lỏng khi truy vấn ban đầu đã có kết quả (Strict match).
4. Kết hợp mở rộng bán kính và nới khoảng ngân sách khi điều kiện kép quá hẹp.
5. Tạm thời nới lỏng các tiện ích phụ (ngoài trời, thú cưng, ăn chay) để ưu tiên vị trí và ẩm thực.
6. API chuyên dụng POST /api/search/relax.
7. Tích hợp cờ auto_relax trên API GET /api/restaurants/filter.
8. Tích hợp trọn vẹn vào State Machine (State 4 QUERY_RELAXATION) và sinh câu giải thích AI.
==============================================================================
"""

import os
import sys

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.restaurant import Restaurant, RestaurantAmenity
from app.services.query_relaxation_service import QueryRelaxationService
from app.services.geo_service import calculate_haversine_distance

client = TestClient(app)


def test_query_relaxation_strict_match_no_relaxation():
    """
    Kiểm thử trường hợp truy vấn gốc đã có kết quả:
    - Không kích hoạt Query Relaxation (relaxation_applied = False, stage = 0).
    """
    db = SessionLocal()
    try:
        # Tìm tại Quận 1 bán kính 3km (có sẵn nhiều quán)
        results, meta = QueryRelaxationService.relax_and_search(
            db=db,
            lat=10.7769,
            lng=106.7009,
            radius_km=3.0,
            limit=5,
        )
        assert len(results) > 0
        assert meta["relaxation_applied"] is False
        assert meta["stage"] == 0
        assert meta["strategy"] == "none"
        assert meta["radius_delta_km"] == 0.0
    finally:
        db.close()


def test_query_relaxation_radius_expansion_plus_3km():
    """
    Kiểm thử tự động mở rộng bán kính (+3.0 km) khi ban đầu 0 kết quả:
    - Chọn bán kính ban đầu cực hẹp (0.01 km) khiến 0 nhà hàng nào thỏa mãn.
    - Cơ chế Query Relaxation tự động kích hoạt: mở rộng bán kính +3.0 km (lên 3.01 km).
    - Kỳ vọng: tìm thấy kết quả, strategy='radius_expansion', stage=1, radius_delta_km=3.0.
    """
    db = SessionLocal()
    try:
        results, meta = QueryRelaxationService.relax_and_search(
            db=db,
            lat=10.7769,
            lng=106.7009,
            radius_km=0.01,  # Bán kính siêu hẹp 10 mét -> 0 quán
            limit=5,
        )
        assert len(results) > 0
        assert meta["relaxation_applied"] is True
        assert meta["strategy"] == "radius_expansion"
        assert meta["stage"] == 1
        assert meta["radius_delta_km"] == 3.0
        assert meta["relaxed_radius_km"] == 3.01
        assert "mở rộng bán kính thêm +3.0 km" in meta["explanation_message"]
    finally:
        db.close()


def test_query_relaxation_budget_expansion_plus_25_percent():
    """
    Kiểm thử tự động nới khoảng ngân sách (±25%) khi ngân sách ban đầu quá thấp:
    - Tìm quán món Âu trong bán kính 3km tại Quận 1.
    - Đặt budget ban đầu = 130.000đ (Pizza 4P's Bến Thành có min_price = 150.000đ nên ban đầu 0 quán).
    - Khi nới ngân sách +25%: budget mới = 130k * 1.25 = 162.500đ (> 150k min_price của Pizza 4P's).
    - Kỳ vọng: tìm thấy quán, strategy='budget_expansion', stage=2, budget_delta_percent=25.0.
    """
    db = SessionLocal()
    try:
        # Ngân sách 130k không đủ cho quán Âu nào (min_price Pizza 4P là 150k)
        results, meta = QueryRelaxationService.relax_and_search(
            db=db,
            lat=10.7725,
            lng=106.698,
            radius_km=1.0,
            cuisine="Món Âu",
            budget=130000,
            limit=5,
        )
        assert len(results) > 0
        assert meta["relaxation_applied"] is True
        assert meta["strategy"] == "budget_expansion"
        assert meta["stage"] == 2
        assert meta["budget_delta_percent"] == 25.0
        assert meta["relaxed_budget"] == int(130000 * 1.25)
        assert "nới khoảng ngân sách ±25%" in meta["explanation_message"]
    finally:
        db.close()


def test_query_relaxation_combined_radius_and_budget():
    """
    Kiểm thử kết hợp mở rộng bán kính (+3km/+6km) VÀ nới khoảng ngân sách (±25%):
    - Đặt vị trí tại khu vực xa trung tâm với ngân sách hạn hẹp.
    - Cả mở rộng bán kính đơn lẻ hay nới ngân sách đơn lẻ đều chưa đủ.
    - Hệ thống chuyển sang Cấp 3: kết hợp cả 2 yếu tố.
    """
    db = SessionLocal()
    try:
        # Tọa độ cách xa trung tâm ~4km, bán kính 0.5km và budget 140k
        results, meta = QueryRelaxationService.relax_and_search(
            db=db,
            lat=10.8000,
            lng=106.7200,
            radius_km=0.5,
            cuisine="Món Âu",
            budget=140000,
            limit=5,
        )
        assert len(results) > 0
        assert meta["relaxation_applied"] is True
        assert meta["stage"] >= 2
        assert meta["relaxed_radius_km"] > 0.5
    finally:
        db.close()


def test_query_relaxation_amenities_relaxed():
    """
    Kiểm thử nới lỏng tiện ích phụ:
    - Đặt điều kiện ẩm thực kèm các tiện ích khó thỏa mãn đồng thời (pet_friendly, has_outdoor, vegetarian_support).
    - Hệ thống nới lỏng các cờ tiện ích phụ để lấy ứng viên thay thế gần đúng nhất.
    """
    db = SessionLocal()
    try:
        results, meta = QueryRelaxationService.relax_and_search(
            db=db,
            lat=10.7769,
            lng=106.7009,
            radius_km=1.0,
            cuisine="Cơm tấm",
            pet_friendly=True,
            has_outdoor=True,
            vegetarian_support=True,
            limit=5,
        )
        assert len(results) > 0
        assert meta["relaxation_applied"] is True
        assert meta["stage"] >= 1
    finally:
        db.close()


def test_api_search_relax_endpoint():
    """
    Kiểm thử API chuyên dụng POST /api/search/relax:
    - Gửi payload tìm kiếm có bán kính 0.01 km (0 quán).
    - Kiểm tra response model QueryRelaxationResponse:
      + status == 'success'
      + task_code == 'TE9C66F'
      + is_relaxed == True
      + relaxation_info chứa chi tiết bước nới lỏng (+3km)
      + results danh sách quán kèm khoảng cách và đánh giá.
    """
    payload = {
        "lat": 10.7769,
        "lng": 106.7009,
        "radius_km": 0.01,
        "limit": 5,
    }
    res = client.post("/api/search/relax", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["task_code"] == "TE9C66F"
    assert data["is_relaxed"] is True
    assert data["results_count"] > 0
    assert len(data["results"]) > 0

    rel_info = data["relaxation_info"]
    assert rel_info["relaxation_applied"] is True
    assert rel_info["strategy"] == "radius_expansion"
    assert rel_info["radius_delta_km"] == 3.0
    assert rel_info["relaxed_radius_km"] == 3.01
    assert "giải thích" in rel_info["explanation_message"].lower() or "mở rộng" in rel_info["explanation_message"].lower()


def test_api_restaurants_filter_auto_relax():
    """
    Kiểm thử cờ auto_relax trên API GET /api/restaurants/filter:
    - Khi auto_relax=false và radius=0.01km -> Trả về 0 quán.
    - Khi auto_relax=true và radius=0.01km -> Tự động nới lỏng bán kính (+3km), trả về quán và trường relaxation.
    """
    # 1. auto_relax = false
    res_strict = client.get("/api/restaurants/filter?lat=10.7769&lng=106.7009&radius_km=0.01&auto_relax=false")
    assert res_strict.status_code == 200
    data_strict = res_strict.json()
    assert len(data_strict["data"]) == 0
    assert data_strict["relaxation"] is None

    # 2. auto_relax = true
    res_relaxed = client.get("/api/restaurants/filter?lat=10.7769&lng=106.7009&radius_km=0.01&auto_relax=true")
    assert res_relaxed.status_code == 200
    data_relaxed = res_relaxed.json()
    assert len(data_relaxed["data"]) > 0
    assert data_relaxed["relaxation"] is not None
    assert data_relaxed["relaxation"]["relaxation_applied"] is True
    assert data_relaxed["relaxation"]["strategy"] == "radius_expansion"
    assert data_relaxed["relaxation"]["radius_delta_km"] == 3.0


def test_multi_turn_state_machine_query_relaxation_flow():
    """
    Kiểm thử luồng State Machine (State 4 QUERY_RELAXATION) qua API Multi-turn Chat:
    - Gửi câu hỏi tìm kiếm tại địa điểm không có nhà hàng thỏa mãn (Cần Giờ, ngân sách 30k).
    - State Machine kích hoạt State 4 và tự động nới lỏng.
    - Kiểm tra: relaxation_applied=True, relaxation_info có thông tin mở rộng (+3km hoặc ±25%).
    - Câu giải thích của AI (ai_message) chứa thông tin giải thích nới lỏng minh bạch.
    """
    res_sess = client.post("/api/chat/sessions", json={})
    assert res_sess.status_code == 201
    sess_id = res_sess.json()["session_id"]

    turn_payload = {
        "message": "Tìm quán lẩu nướng tại Cần Giờ có chỗ đậu xe giá dưới 30k",
        "provider": "rule_based",
    }
    res_turn = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=turn_payload)
    assert res_turn.status_code == 200
    turn_data = res_turn.json()

    assert turn_data["current_state"] == "RESULT_PRESENTED"
    assert turn_data["relaxation_applied"] is True
    assert "relaxation_info" in turn_data
    assert len(turn_data["results"]) > 0

    # Lời giải thích AI phải giải thích rõ ràng việc nới lỏng bán kính hoặc ngân sách
    ai_msg = turn_data["ai_message"].lower()
    assert ("mở rộng" in ai_msg or "nới" in ai_msg or "tự động" in ai_msg)
