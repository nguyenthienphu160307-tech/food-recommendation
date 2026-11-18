import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.search import SearchSession, SearchCriteria, SearchMessage

client = TestClient(app)


def test_parsed_criteria_chips_html_and_js_elements():
    """
    Kiểm tra frontend/index.html chứa đầy đủ thành phần UI & JavaScript
    cho Thẻ tiêu chí đã bóc tách (Parsed Criteria Chips - Task TE9C673).
    """
    res = client.get("/frontend/index.html")
    assert res.status_code == 200
    html = res.text

    # 1. Thanh Parsed Criteria Bar trên khung chat
    assert 'id="parsed-criteria-bar"' in html
    assert 'id="parsed-chips-scroll"' in html
    assert 'btn-clear-all-chips' in html
    assert 'clearAllCriteria()' in html

    # 2. CSS styles cho Parsed Chips
    assert '.parsed-chip' in html
    assert '.btn-remove-chip' in html
    assert '.chat-parsed-criteria-box' in html
    assert '.chip-location' in html
    assert '.chip-cuisine' in html
    assert '.chip-budget' in html
    assert '.chip-amenity' in html

    # 3. JavaScript logic
    assert 'extractChipsFromCriteria' in html
    assert 'renderParsedCriteriaChips' in html
    assert 'buildInBubbleParsedCriteriaHtml' in html
    assert 'removeCriterion' in html
    assert '/api/chat/sessions/' in html
    assert '/criteria/remove-field' in html


def test_remove_criterion_api_lifecycle():
    """
    Kiểm tra vòng đời API xóa nhanh tiêu chí (Task TE9C673):
    1. Tạo phiên hội thoại
    2. Gửi câu hỏi bóc tách đa tiêu chí: Vị trí, Món, Ngân sách, Đậu ô tô
    3. Xóa tiêu chí 'cuisine' qua POST /criteria/remove-field
    4. Xóa tiêu chí 'has_parking' qua DELETE /criteria/{field}
    5. Xóa tiêu chí 'location' qua DELETE /criteria/{field}
    6. Xóa tất cả qua field 'all'
    7. Chặn xóa tiêu chí khi phiên đã đóng
    """
    # 1. Tạo phiên
    create_res = client.post("/api/chat/sessions", json={"user_id": None})
    assert create_res.status_code == 201
    session_id = create_res.json()["session_id"]

    # 2. Gửi câu hỏi khởi đầu
    turn_res = client.post(
        f"/api/chat/sessions/{session_id}/multi-turn",
        json={
            "message": "Tìm quán nướng Bình Thạnh dưới 300k có chỗ đậu ô tô",
            "provider": "auto",
            "user_id": None
        }
    )
    assert turn_res.status_code == 200
    turn_data = turn_res.json()
    crit = turn_data["merged_criteria"]
    assert crit is not None
    assert crit["cuisine"] is not None
    assert crit["budget"] is not None
    assert crit["has_parking"] is True

    # 3. Xóa tiêu chí 'cuisine' (Món ăn) qua POST /criteria/remove-field
    remove_cui_res = client.post(
        f"/api/chat/sessions/{session_id}/criteria/remove-field",
        json={"field": "cuisine"}
    )
    assert remove_cui_res.status_code == 200
    data_cui = remove_cui_res.json()
    assert data_cui["session_id"] == session_id
    assert data_cui["removed_field"] == "cuisine"
    assert data_cui["status"] == "success"
    assert "Món ăn" in data_cui["ai_message"]
    # Xác nhận cuisine đã về None, các trường khác vẫn giữ nguyên
    updated_cui = data_cui["updated_criteria"]
    assert updated_cui["cuisine"] is None
    assert updated_cui["budget"] is not None
    assert updated_cui["has_parking"] is True

    # 4. Xóa tiêu chí 'has_parking' (Đậu ô tô) qua DELETE /criteria/has_parking
    remove_park_res = client.delete(
        f"/api/chat/sessions/{session_id}/criteria/has_parking"
    )
    assert remove_park_res.status_code == 200
    data_park = remove_park_res.json()
    assert data_park["removed_field"] == "has_parking"
    updated_park = data_park["updated_criteria"]
    assert updated_park["has_parking"] is False

    # 5. Xóa tiêu chí 'location' (Vị trí) qua DELETE /criteria/location
    remove_loc_res = client.delete(
        f"/api/chat/sessions/{session_id}/criteria/location"
    )
    assert remove_loc_res.status_code == 200
    data_loc = remove_loc_res.json()
    updated_loc = data_loc["updated_criteria"]
    assert updated_loc["location_text"] is None
    assert updated_loc["latitude"] is None
    assert updated_loc["longitude"] is None

    # 6. Xóa tất cả qua field 'all'
    remove_all_res = client.post(
        f"/api/chat/sessions/{session_id}/criteria/remove-field",
        json={"field": "all"}
    )
    assert remove_all_res.status_code == 200
    data_all = remove_all_res.json()
    updated_all = data_all["updated_criteria"]
    assert updated_all["location_text"] is None
    assert updated_all["cuisine"] is None
    assert updated_all["budget"] is None
    assert updated_all["has_parking"] is False

    # 7. Đóng phiên và kiểm tra chặn xóa
    client.put(f"/api/chat/sessions/{session_id}/close", json={"reason": "user_ended"})
    blocked_res = client.post(
        f"/api/chat/sessions/{session_id}/criteria/remove-field",
        json={"field": "budget"}
    )
    assert blocked_res.status_code == 400
    assert "kết thúc" in blocked_res.json()["detail"].lower()
