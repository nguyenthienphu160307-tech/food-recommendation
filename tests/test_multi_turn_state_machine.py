"""
==============================================================================
UNIT & INTEGRATION TESTS: BỘ QUẢN LÝ NGỮ CẢNH HỘI THOẠI ĐA LƯỢT (TE9C669)
==============================================================================
Tuân thủ chuẩn State Diagram Vòng đời tìm kiếm (Hình 8.2 SRS):
1. Kiểm tra 8 trạng thái State Machine & Metadata endpoint:
   - SESSION_IDLE, PARSING_INTENT, SPATIAL_FILTERING, QUERY_RELAXATION,
     RANKING_AND_AI, RESULT_PRESENTED, CONTEXT_REFINING, SESSION_CLOSED
2. Kiểm tra nghiệp vụ Hợp nhất Tiêu chí (Multi-turn Criteria Merging):
   - 'Quán nào rẻ hơn?' -> Tự động siết/giảm ngân sách, giữ nguyên vị trí, món, tiện ích.
   - 'Đổi sang Quận 3'   -> Cập nhật địa danh mới, tự động Geocode lại tọa độ GPS, giữ nguyên món và ngân sách.
   - 'Cần thêm phòng riêng' -> Cập nhật other_conditions.has_private_room = True, kế thừa tiêu chí cũ.
   - 'Không cần phòng riêng' -> Cập nhật negative modifier has_private_room = False.
3. Kiểm tra Truy vấn không gian & Nới lỏng điều kiện (Query Relaxation - State 4) khi 0 kết quả.
4. Kiểm tra lưu trữ lịch sử tiêu chí và audit trail trong bảng SearchCriteria.
5. Kiểm tra đóng phiên (SESSION_CLOSED - State 8) và chặn gửi tin nhắn vào phiên đã đóng.
==============================================================================
"""

import json
import os
import sys

# Đảm bảo UTF-8 console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Thêm thư mục dev/food-recommendation vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app
from app.models.search import SearchCriteria, SearchMessage, SearchSession
from app.schemas.ai_search import DiningCriteriaSchema, OtherConditionsSchema
from app.services.chat_session_service import ChatSessionService
from app.services.multi_turn_state_machine import (
    MultiTurnStateMachine,
    SearchSessionState,
    VALID_STATE_TRANSITIONS,
)

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Khởi tạo cơ sở dữ liệu trước khi kiểm thử."""
    Base.metadata.create_all(bind=engine)
    yield


# ==============================================================================
# PHẦN 1: KIỂM THỬ ĐỊNH NGHĨA STATE MACHINE & SƠ ĐỒ CHUYỂN TRẠNG THÁI (HÌNH 8.2)
# ==============================================================================

def test_state_diagram_metadata_api():
    """Kiểm tra API trả về cấu trúc và 8 trạng thái của State Diagram Hình 8.2."""
    response = client.get("/api/search/state-diagram")
    assert response.status_code == 200
    data = response.json()

    assert data["task_code"] == "TE9C669"
    assert "Hình 8.2" in data["diagram_name"]
    states = data["states"]
    assert len(states) == 8, f"Kỳ vọng đúng 8 trạng thái theo Hình 8.2, thực tế có {len(states)}"

    expected_states = [
        "SESSION_IDLE",
        "PARSING_INTENT",
        "SPATIAL_FILTERING",
        "QUERY_RELAXATION",
        "RANKING_AND_AI",
        "RESULT_PRESENTED",
        "CONTEXT_REFINING",
        "SESSION_CLOSED",
    ]
    actual_state_keys = [s["state"] for s in states]
    for exp in expected_states:
        assert exp in actual_state_keys, f"Thiếu trạng thái {exp} trong sơ đồ trạng thái!"

    # Kiểm tra chuyển trạng thái hợp lệ
    transitions = data["valid_transitions"]
    assert "SESSION_IDLE" in transitions
    assert "PARSING_INTENT" in transitions["SESSION_IDLE"]
    assert "CONTEXT_REFINING" in transitions["RESULT_PRESENTED"]


def test_session_initial_state_idle():
    """Kiểm tra phiên chat mới tạo có trạng thái ban đầu là SESSION_IDLE."""
    db = SessionLocal()
    try:
        session = ChatSessionService.create_session(db, user_id=None)
        state = MultiTurnStateMachine.get_current_state(session)
        assert state == SearchSessionState.SESSION_IDLE
        assert session.status == "active"
    finally:
        db.close()


# ==============================================================================
# PHẦN 2: KIỂM THỬ THUẬT TOÁN HỢP NHẤT TIÊU CHÍ (CRITERIA MERGING)
# ==============================================================================

def test_criteria_merging_cheaper_intent():
    """
    Kiểm thử câu hỏi 'Quán nào rẻ hơn?':
    - Giữ nguyên địa điểm ('Quận 1'), ẩm thực ('BBQ Hàn Quốc'), tiện ích ('has_parking=True').
    - Tự động giảm trần ngân sách xuống (-25%).
    """
    db = SessionLocal()
    try:
        sess = ChatSessionService.create_session(db)
        # Giả lập tiêu chí hiện tại ở lượt 1
        initial_crit = SearchCriteria(
            session_id=sess.session_id,
            location_text="Quận 1",
            latitude=10.7769,
            longitude=106.7009,
            cuisine="BBQ Hàn Quốc",
            budget=300000,
            has_parking=True,
            other_conditions=json.dumps({"has_private_room": True}),
        )

        # Lượt 2: Người dùng hỏi "Có quán nào rẻ hơn không?"
        incoming_schema = DiningCriteriaSchema(
            location_text=None,
            cuisine=None,
            budget=None,
            has_parking=None,
            other_conditions=OtherConditionsSchema(),
        )

        merged = MultiTurnStateMachine.merge_criteria(
            current_crit=initial_crit,
            incoming_crit=incoming_schema,
            raw_message="Có quán nào rẻ hơn không bạn?",
        )

        assert merged["location_text"] == "Quận 1"
        assert merged["cuisine"] == "BBQ Hàn Quốc"
        assert merged["has_parking"] is True
        assert merged["other_conditions"]["has_private_room"] is True
        # Ngân sách phải thấp hơn 300.000đ (300k * 0.75 = 220k - 230k)
        assert merged["budget"] is not None
        assert merged["budget"] < 300000
        assert merged["budget"] == 220000
    finally:
        db.close()


def test_criteria_merging_change_location_with_geocoding():
    """
    Kiểm thử câu hỏi 'Đổi sang Quận 3':
    - Cập nhật location_text mới = 'Quận 3'.
    - Tự động Geocode lại tọa độ GPS sang Quận 3 (lat ~ 10.7844, lng ~ 106.6843).
    - Giữ nguyên ẩm thực ('BBQ Hàn Quốc'), ngân sách (300.000đ), chỗ đỗ xe.
    """
    db = SessionLocal()
    try:
        sess = ChatSessionService.create_session(db)
        initial_crit = SearchCriteria(
            session_id=sess.session_id,
            location_text="Quận 1",
            latitude=10.7769,
            longitude=106.7009,
            cuisine="BBQ Hàn Quốc",
            budget=300000,
            has_parking=True,
            other_conditions=json.dumps({"has_private_room": True}),
        )

        incoming_schema = DiningCriteriaSchema(
            location_text="Quận 3",
            cuisine=None,
            budget=None,
            has_parking=None,
            other_conditions=OtherConditionsSchema(),
        )

        merged = MultiTurnStateMachine.merge_criteria(
            current_crit=initial_crit,
            incoming_crit=incoming_schema,
            raw_message="Đổi sang Quận 3 giúp mình",
        )

        assert merged["location_text"] in ("Quận 3", "Quan 3")
        assert merged["latitude"] is not None and merged["longitude"] is not None
        # Kiểm tra tọa độ nằm trong khu vực Quận 3
        assert 10.77 <= merged["latitude"] <= 10.80
        assert 106.67 <= merged["longitude"] <= 106.70
        # Các tiêu chí khác không đổi
        assert merged["cuisine"] == "BBQ Hàn Quốc"
        assert merged["budget"] == 300000
        assert merged["has_parking"] is True
        assert merged["other_conditions"]["has_private_room"] is True
    finally:
        db.close()


def test_criteria_merging_amenity_toggle():
    """
    Kiểm thử bổ sung và hủy bỏ tiện ích (Amenity modification):
    - Lượt thêm: 'Cần thêm phòng riêng và cho mang thú cưng' -> True
    - Lượt bỏ: 'Không cần phòng riêng nữa' -> False
    """
    db = SessionLocal()
    try:
        sess = ChatSessionService.create_session(db)
        initial_crit = SearchCriteria(
            session_id=sess.session_id,
            location_text="Bình Thạnh",
            latitude=10.8016,
            longitude=106.7115,
            cuisine="Món Chay",
            budget=150000,
            has_parking=False,
            other_conditions=json.dumps({
                "has_private_room": False,
                "pet_friendly": False,
                "vegetarian_support": True,
            }),
        )

        # 1. Thêm phòng riêng và thú cưng
        inc1 = DiningCriteriaSchema(
            location_text=None,
            cuisine=None,
            budget=None,
            has_parking=None,
            other_conditions=OtherConditionsSchema(has_private_room=True, pet_friendly=True),
        )
        merged1 = MultiTurnStateMachine.merge_criteria(initial_crit, inc1, "Cần có phòng riêng và cho mang pet")
        assert merged1["other_conditions"]["has_private_room"] is True
        assert merged1["other_conditions"]["pet_friendly"] is True
        assert merged1["other_conditions"]["vegetarian_support"] is True
        assert merged1["cuisine"] == "Món Chay"

        # 2. Hủy phòng riêng
        initial_crit.other_conditions = json.dumps(merged1["other_conditions"])
        inc2 = DiningCriteriaSchema(
            location_text=None,
            cuisine=None,
            budget=None,
            has_parking=None,
            other_conditions=OtherConditionsSchema(has_private_room=False),
        )
        merged2 = MultiTurnStateMachine.merge_criteria(initial_crit, inc2, "Thôi không cần phòng riêng nữa")
        assert merged2["other_conditions"]["has_private_room"] is False
        assert merged2["other_conditions"]["pet_friendly"] is True
    finally:
        db.close()


# ==============================================================================
# PHẦN 3: KIỂM THỬ ĐIỀU HƯỚNG VÒNG ĐỜI TRỌN GÓI (MULTI-TURN LIFECYCLE)
# ==============================================================================

def test_full_multi_turn_lifecycle_api():
    """
    Kiểm tra kịch bản hội thoại đa lượt thực tế từ đầu đến cuối:
    - Turn 1: Khởi tạo phiên & hỏi món nướng ở Quận 1.
    - Turn 2: 'Quán nào rẻ hơn?' -> Hợp nhất budget, giữ Quận 1.
    - Turn 3: 'Đổi sang Quận 3' -> Hợp nhất Quận 3, Geocode lại tọa độ.
    - Turn 4: 'Cảm ơn, tôi đã chọn được quán rồi' -> Đóng phiên (SESSION_CLOSED).
    - Turn 5: Thử gửi thêm tin nhắn khi phiên đã đóng -> Kỳ vọng HTTP 400.
    """
    # 1. Tạo phiên mới (State 1: SESSION_IDLE)
    res_sess = client.post("/api/chat/sessions", json={})
    assert res_sess.status_code == 201
    sess_id = res_sess.json()["session_id"]
    assert res_sess.json()["current_state"] == "SESSION_IDLE"

    # 2. Turn 1: Câu hỏi ban đầu (State 1 -> 2 -> 3 -> 5 -> 6)
    t1_payload = {
        "message": "Tôi đang ở Quận 1 muốn tìm quán đồ nướng lẩu có chỗ đậu ô tô dưới 350k",
        "provider": "rule_based",
    }
    res_t1 = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=t1_payload)
    assert res_t1.status_code == 200
    d1 = res_t1.json()
    assert d1["current_state"] == "RESULT_PRESENTED"
    assert d1["merged_criteria"]["location_text"] == "Quận 1"
    assert d1["merged_criteria"]["cuisine"] == "BBQ Hàn Quốc"
    assert d1["merged_criteria"]["budget"] == 350000
    assert d1["merged_criteria"]["has_parking"] is True
    assert len(d1["results"]) > 0

    # 3. Turn 2: Người dùng hỏi tiếp "Quán nào rẻ hơn?" (State 6 -> 7 -> 2 -> 3 -> 5 -> 6)
    t2_payload = {
        "message": "Quán nào rẻ hơn nữa không bạn?",
        "provider": "rule_based",
    }
    res_t2 = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=t2_payload)
    assert res_t2.status_code == 200
    d2 = res_t2.json()
    assert d2["current_state"] == "RESULT_PRESENTED"
    # Tiêu chí được merge: giữ Quận 1, giảm budget
    assert d2["merged_criteria"]["location_text"] == "Quận 1"
    assert d2["merged_criteria"]["cuisine"] == "BBQ Hàn Quốc"
    assert d2["merged_criteria"]["budget"] < 350000
    assert d2["merged_criteria"]["has_parking"] is True

    # 4. Turn 3: Người dùng đổi địa điểm "Đổi sang Quận 3"
    t3_payload = {
        "message": "Đổi sang Quận 3 giúp mình nhé",
        "provider": "rule_based",
    }
    res_t3 = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=t3_payload)
    assert res_t3.status_code == 200
    d3 = res_t3.json()
    assert d3["current_state"] == "RESULT_PRESENTED"
    assert d3["merged_criteria"]["location_text"] in ("Quận 3", "Quan 3")
    assert d3["merged_criteria"]["cuisine"] == "BBQ Hàn Quốc"
    assert d3["merged_criteria"]["latitude"] is not None

    # 5. Kiểm tra lịch sử trạng thái qua GET /api/chat/sessions/{session_id}/state
    res_st = client.get(f"/api/chat/sessions/{sess_id}/state")
    assert res_st.status_code == 200
    st_info = res_st.json()
    assert st_info["session_id"] == sess_id
    assert st_info["current_state"] == "RESULT_PRESENTED"
    assert st_info["total_criteria_versions"] >= 3
    assert len(st_info["criteria_history"]) >= 3
    # Xác nhận tiêu chí đầu là Quận 1, tiêu chí cuối là Quận 3
    assert st_info["criteria_history"][0]["location_text"] == "Quận 1"
    assert st_info["criteria_history"][-1]["location_text"] in ("Quận 3", "Quan 3")

    # 6. Turn 4: Kết thúc phiên tìm kiếm (State 6 -> 8: SESSION_CLOSED)
    t4_payload = {
        "message": "Cảm ơn bạn nhé, mình đã chọn được quán rồi!",
        "provider": "rule_based",
    }
    res_t4 = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=t4_payload)
    assert res_t4.status_code == 200
    d4 = res_t4.json()
    assert d4["current_state"] == "SESSION_CLOSED"
    assert d4["status"] == "closed"
    assert "Chúc bạn có một bữa ăn ngon miệng" in d4["ai_message"]

    # 7. Turn 5: Thử gửi thêm tin nhắn vào phiên đã đóng (Kỳ vọng HTTP 400)
    res_t5 = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json={"message": "Tìm thêm quán nữa"})
    assert res_t5.status_code == 400
    assert "đã kết thúc" in res_t5.json()["detail"]


# ==============================================================================
# PHẦN 4: KIỂM THỬ NỚI LỎNG ĐIỀU KIỆN (QUERY RELAXATION - STATE 4)
# ==============================================================================

def test_query_relaxation_when_zero_results():
    """
    Kiểm tra khi điều kiện quá hẹp dẫn đến 0 kết quả ban đầu:
    - State Machine kích hoạt State 4: QUERY_RELAXATION.
    - Tự động nới lỏng bán kính hoặc ngân sách trần.
    - Tìm thấy ứng viên thay thế và trả về cờ relaxation_applied = True.
    """
    res_sess = client.post("/api/chat/sessions", json={})
    sess_id = res_sess.json()["session_id"]

    # Đưa ra yêu cầu cực hẹp: Nhà hàng ở Cần Giờ giá dưới 40k có phòng riêng VIP
    payload = {
        "message": "Tìm quán lẩu nướng ở Cần Giờ có phòng riêng VIP giá dưới 40 ngàn",
        "provider": "rule_based",
    }
    res = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["relaxation_applied"] is True
    assert "relaxation_info" in data
    # Câu giải thích của AI phải có nhắc tới việc nới lỏng điều kiện
    assert "nới lỏng" in data["ai_message"].lower() or "mở rộng" in data["ai_message"].lower()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
