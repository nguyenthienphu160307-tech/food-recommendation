"""
==============================================================================
UNIT & INTEGRATION TESTS: TÍCH HỢP LLM/NLP PHÂN TÍCH CHAT SANG SEARCHCRITERIA
MÃ TASK: TE9C668 (MODULE 2 & 3)
==============================================================================
Kiểm thử toàn diện:
1. Kết nối & Bóc tách LLM/NLP:
   - Thử nghiệm Gemini API (Mock HTTP response & fallback)
   - Thử nghiệm OpenAI API (Mock HTTP response & fallback)
   - Bóc tách câu truy vấn tự nhiên tiếng Việt phức tạp (cuisine, location, budget, parking, other_conditions)
2. Lưu trữ vào bảng SearchCriteria & SearchMessages:
   - Tự động Geocoding tọa độ GPS từ location_text
   - Lưu trữ bản ghi SearchCriteria chuẩn xác
   - Lưu tin nhắn người dùng và phản hồi AI vào SearchMessages
   - Bảo vệ quyền riêng tư vị trí GPS (BR-08 / TSK-20)
3. Hỗ trợ Multi-turn Refinement (Kế thừa và cập nhật tiêu chí qua nhiều lượt chat)
4. Kiểm thử các API Endpoints:
   - POST /api/chat/sessions/{session_id}/parse-and-save
   - POST /api/chat/parse-and-save
   - POST /api/search/llm-parse-and-save
   - POST /api/search/extract-criteria (hỗ trợ provider)
   - Xử lý các trường hợp ngoại lệ: 404 (session không tồn tại), 400 (phiên đã đóng), 422 (tin nhắn rỗng)
==============================================================================
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Thêm thư mục gốc dev/food-recommendation vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app
from app.models.search import SearchCriteria, SearchMessage, SearchSession
from app.models.user import User
from app.schemas.ai_search import DiningCriteriaSchema, OtherConditionsSchema
from app.services.chat_session_service import ChatSessionService
from app.services.llm_service import LLMService

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Khởi tạo bảng cơ sở dữ liệu trước khi chạy bài test."""
    Base.metadata.create_all(bind=engine)
    yield


# ==============================================================================
# PHẦN 1: UNIT TEST LLMSERVICE & KẾT NỐI GEMINI / OPENAI / RULE-BASED
# ==============================================================================

def test_llm_service_configured_providers():
    """Kiểm tra hàm phát hiện các API key đã được cấu hình."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSyTest123", "OPENAI_API_KEY": ""}):
        providers = LLMService.get_configured_providers()
        assert providers["gemini"] is True
        assert providers["openai"] is False

    with patch.dict(os.environ, {"GEMINI_API_KEY": "", "OPENAI_API_KEY": "sk-test456"}):
        providers = LLMService.get_configured_providers()
        assert providers["gemini"] is False
        assert providers["openai"] is True


def test_gemini_api_connector_mock():
    """Kiểm tra gọi Gemini API với structured JSON response."""
    mock_gemini_response = MagicMock()
    mock_gemini_response.status_code = 200
    mock_gemini_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps({
                                "location_text": "Quận 1",
                                "cuisine": "BBQ Hàn Quốc",
                                "budget": 350000,
                                "has_parking": True,
                                "other_conditions": {
                                    "has_private_room": True,
                                    "pet_friendly": None,
                                    "vegetarian_support": None,
                                    "has_outdoor": None,
                                    "group_size": 4,
                                },
                            })
                        }
                    ]
                }
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_gemini_response):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "mock_gemini_key"}):
            criteria = LLMService.call_gemini_api(
                prompt="Cần tìm quán nướng ở Quận 1 cho 4 người dưới 350k có phòng riêng",
                api_key="mock_gemini_key",
            )
            assert criteria.location_text == "Quận 1"
            assert criteria.cuisine == "BBQ Hàn Quốc"
            assert criteria.budget == 350000
            assert criteria.has_parking is True
            assert criteria.other_conditions.has_private_room is True
            assert criteria.other_conditions.group_size == 4


def test_openai_api_connector_mock():
    """Kiểm tra gọi OpenAI API với JSON mode response."""
    mock_openai_response = MagicMock()
    mock_openai_response.status_code = 200
    mock_openai_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "location_text": "Gò Vấp",
                        "cuisine": "Món Chay",
                        "budget": 150000,
                        "has_parking": None,
                        "other_conditions": {
                            "has_private_room": None,
                            "pet_friendly": True,
                            "vegetarian_support": True,
                            "has_outdoor": True,
                            "group_size": None,
                        },
                    })
                }
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_openai_response):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "mock_openai_key"}):
            criteria = LLMService.call_openai_api(
                prompt="Quán chay thanh đạm sân vườn ở Gò Vấp tầm 150 ngàn cho thú cưng",
                api_key="mock_openai_key",
            )
            assert criteria.location_text == "Gò Vấp"
            assert criteria.cuisine == "Món Chay"
            assert criteria.budget == 150000
            assert criteria.other_conditions.vegetarian_support is True
            assert criteria.other_conditions.pet_friendly is True
            assert criteria.other_conditions.has_outdoor is True


def test_llm_service_fallback_to_rule_based():
    """Kiểm tra cơ chế tự động Fallback sang Rule-based NLP khi không có API Key."""
    # Khi không có key, tự động fallback an toàn
    with patch.dict(os.environ, {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""}):
        criteria, explanation, engine_used = LLMService.extract_criteria(
            prompt="Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, có phòng riêng",
            provider="auto",
        )
        assert engine_used == "rule_based_nlp"
        assert criteria.location_text == "Quận 1"
        assert criteria.cuisine == "BBQ Hàn Quốc"
        assert criteria.budget == 300000
        assert criteria.has_parking is True
        assert criteria.other_conditions.has_private_room is True
        assert criteria.other_conditions.group_size == 4
        assert "BBQ Hàn Quốc" in explanation


# ==============================================================================
# PHẦN 2: INTEGRATION TEST PARSE & LƯU VÀO BẢNG SEARCHCRITERIA
# ==============================================================================

def test_parse_and_save_to_criteria_flow():
    """Kiểm tra toàn bộ luồng bóc tách và lưu vào bảng SearchCriteria & SearchMessages."""
    db = SessionLocal()
    try:
        # 1. Tạo 1 phiên chat mới
        session_obj = ChatSessionService.create_session(db, user_id=None)
        sess_id = session_obj.session_id

        # 2. Thực hiện bóc tách và lưu
        user_text = "Tôi ở Bình Thạnh, muốn tìm quán lẩu nấm hoặc món việt dưới 250k có chỗ đậu xe"
        result = LLMService.parse_and_save_to_criteria(
            db=db,
            session_id=sess_id,
            user_message=user_text,
            provider="rule_based",
        )

        assert result["session_id"] == sess_id
        assert result["criteria_id"] > 0
        assert result["user_message"] == user_text
        assert result["location_text"] in ("Bình Thạnh", "Quận Bình Thạnh")
        assert result["latitude"] is not None and result["longitude"] is not None
        # Kiểm tra tọa độ Bình Thạnh hợp lý
        assert 10.75 <= result["latitude"] <= 10.85
        assert 106.65 <= result["longitude"] <= 106.75
        assert result["cuisine"] == "Món Việt"
        assert result["budget"] == 250000
        assert result["has_parking"] is True

        # 3. Kiểm tra bản ghi SearchCriteria trong CSDL
        saved_crit = db.query(SearchCriteria).filter(SearchCriteria.criteria_id == result["criteria_id"]).first()
        assert saved_crit is not None
        assert saved_crit.session_id == sess_id
        assert saved_crit.budget == 250000
        assert saved_crit.has_parking is True

        # 4. Kiểm tra tin nhắn trong SearchMessages
        messages = db.query(SearchMessage).filter(SearchMessage.session_id == sess_id).order_by(SearchMessage.message_id.asc()).all()
        assert len(messages) >= 2
        assert messages[0].sender_type == "user"
        assert messages[0].content == user_text
        assert messages[1].sender_type == "ai"
        assert len(messages[1].content) > 0
    finally:
        db.close()


def test_multi_turn_criteria_refinement():
    """Kiểm tra kế thừa ngữ cảnh hội thoại nhiều lượt (Multi-turn Refinement)."""
    db = SessionLocal()
    try:
        # 1. Tạo phiên mới
        session_obj = ChatSessionService.create_session(db, user_id=None)
        sess_id = session_obj.session_id

        # Lượt 1: Chỉ nhắc đến món ăn và địa điểm
        turn1_text = "Muốn ăn đồ nướng quanh Quận 1"
        res1 = LLMService.parse_and_save_to_criteria(
            db=db,
            session_id=sess_id,
            user_message=turn1_text,
            provider="rule_based",
        )
        assert res1["location_text"] == "Quận 1"
        assert res1["cuisine"] == "BBQ Hàn Quốc"
        assert res1["budget"] is None

        # Lượt 2: Bổ sung ngân sách và tiện ích mà không nhắc lại địa điểm
        turn2_text = "Có chỗ đậu ô tô dưới 300k và cần phòng riêng yên tĩnh"
        res2 = LLMService.parse_and_save_to_criteria(
            db=db,
            session_id=sess_id,
            user_message=turn2_text,
            provider="rule_based",
        )
        # Tiêu chí mới phải kế thừa địa điểm và ẩm thực từ lượt 1
        assert res2["location_text"] == "Quận 1"
        assert res2["cuisine"] == "BBQ Hàn Quốc"
        assert res2["budget"] == 300000
        assert res2["has_parking"] is True
        assert res2["other_conditions"]["has_private_room"] is True

        # Xác nhận có 2 bản ghi criteria trong phiên này
        crits = db.query(SearchCriteria).filter(SearchCriteria.session_id == sess_id).all()
        assert len(crits) == 2
    finally:
        db.close()


# ==============================================================================
# PHẦN 3: KIỂM THỬ ROUTER ENDPOINTS (FASTAPI RESTFUL)
# ==============================================================================

def test_api_session_parse_and_save_success():
    """Kiểm tra endpoint POST /api/chat/sessions/{session_id}/parse-and-save."""
    # Khởi tạo session trước
    res_sess = client.post("/api/chat/sessions", json={})
    assert res_sess.status_code == 201
    sess_id = res_sess.json()["session_id"]

    # Gửi câu chat để parse và lưu
    payload = {
        "message": "Tìm quán cơm tấm ở Quận 3 có sân vườn thoáng mát tầm 70 nghìn",
        "provider": "auto"
    }
    res_parse = client.post(f"/api/chat/sessions/{sess_id}/parse-and-save", json=payload)
    assert res_parse.status_code == 201
    data = res_parse.json()

    assert data["session_id"] == sess_id
    assert data["criteria_id"] > 0
    assert data["cuisine"] == "Cơm tấm"
    assert data["budget"] == 70000
    assert data["other_conditions"]["has_outdoor"] is True
    assert "cơm tấm" in data["ai_explanation"].lower()


def test_api_session_parse_and_save_nonexistent_session():
    """Kiểm tra gọi parse-and-save với session_id không tồn tại (Kỳ vọng 404)."""
    payload = {"message": "Tìm quán lẩu ở Quận 1"}
    response = client.post("/api/chat/sessions/9999999/parse-and-save", json=payload)
    assert response.status_code == 404
    assert "Không tìm thấy phiên chat" in response.json()["detail"]


def test_api_session_parse_and_save_closed_session():
    """Kiểm tra gọi parse-and-save vào phiên đã đóng (Kỳ vọng 400)."""
    # Tạo và đóng phiên
    res_sess = client.post("/api/chat/sessions", json={})
    sess_id = res_sess.json()["session_id"]
    client.put(f"/api/chat/sessions/{sess_id}/close")

    # Thử gửi câu chat
    payload = {"message": "Tôi muốn thêm một câu hỏi"}
    res_closed = client.post(f"/api/chat/sessions/{sess_id}/parse-and-save", json=payload)
    assert res_closed.status_code == 400
    assert "đã kết thúc" in res_closed.json()["detail"]


def test_api_session_parse_and_save_empty_message():
    """Kiểm tra gửi tin nhắn rỗng (Kỳ vọng 422)."""
    res_sess = client.post("/api/chat/sessions", json={})
    sess_id = res_sess.json()["session_id"]

    res_empty = client.post(f"/api/chat/sessions/{sess_id}/parse-and-save", json={"message": "   "})
    assert res_empty.status_code == 422


def test_api_chat_parse_and_save_auto_session():
    """Kiểm tra endpoint tiện ích POST /api/chat/parse-and-save tự tạo session mới."""
    payload = {
        "message": "Nhóm bạn muốn tìm quán cà phê hoặc lẩu nướng ở Thủ Đức dưới 200k",
        "provider": "rule_based"
    }
    response = client.post("/api/chat/parse-and-save", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["session_id"] > 0
    assert data["criteria_id"] > 0
    assert data["location_text"] in ("Thủ Đức", "TP. Thủ Đức")
    assert data["budget"] == 200000


def test_api_search_llm_parse_and_save_endpoint():
    """Kiểm tra endpoint POST /api/search/llm-parse-and-save."""
    payload = {
        "message": "Tìm quán chay thanh đạm ở Gò Vấp tầm 150k cho mang thú cưng",
        "provider": "rule_based"
    }
    response = client.post("/api/search/llm-parse-and-save", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["cuisine"] == "Món Chay"
    assert data["budget"] == 150000
    assert data["other_conditions"]["vegetarian_support"] is True
    assert data["other_conditions"]["pet_friendly"] is True


def test_api_extract_criteria_with_provider_parameter():
    """Kiểm tra endpoint POST /api/search/extract-criteria hỗ trợ tham số provider."""
    payload = {
        "prompt": "Quán nướng Quận 1 có chỗ đậu ô tô dưới 300k",
        "provider": "rule_based"
    }
    response = client.post("/api/search/extract-criteria", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["extraction_engine"] == "rule_based_nlp"
    assert data["extracted_criteria"]["cuisine"] == "BBQ Hàn Quốc"
    assert data["extracted_criteria"]["has_parking"] is True


if __name__ == "__main__":
    pytest.main(["-v", __file__])
