import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Restaurant, RestaurantAmenity, SearchSession, SearchMessage, SearchCriteria

client = TestClient(app)


def test_chatbox_ui_html_structure():
    """
    Kiểm tra giao diện frontend/index.html chứa đầy đủ các thành phần
    Chatbox UI, Chip câu hỏi mẫu (NFR-02) và Typing Indicator (TE9C672).
    """
    response = client.get("/frontend/index.html")
    assert response.status_code == 200
    html = response.text

    # 1. Container Chatbox Drawer & Header hiện đại
    assert 'id="ai-drawer"' in html
    assert 'ai-drawer-header' in html
    assert 'Trợ lý Ẩm thực AI' in html
    assert 'ai-status-badge' in html
    assert 'ai-status-dot' in html
    assert 'ai-status-text' in html
    assert 'startNewChatSession()' in html
    assert 'closeCurrentChatSession(' in html

    # 2. Feed tin nhắn & Bong bóng chat
    assert 'id="ai-chat-feed"' in html
    assert 'bubble-ai' in html
    assert 'bubble-user' in html
    assert 'ai-welcome-bubble' in html

    # 3. Hiệu ứng đang phân tích tiêu chí (Typing & Analyzing Indicator)
    assert 'id="ai-typing-indicator"' in html
    assert 'typing-dots' in html
    assert 'typing-status-text' in html
    assert '@keyframes typingBounce' in html

    # 4. Chip gợi ý câu hỏi mẫu cho người mới (NFR-02)
    assert 'id="sample-prompts-bar"' in html
    assert 'id="sample-prompts-scroll"' in html
    assert 'prompt-chip' in html
    assert 'SAMPLE_PROMPTS_INITIAL' in html
    assert 'SAMPLE_PROMPTS_FOLLOW_UP' in html
    assert 'renderSamplePromptChips' in html

    # 5. Thẻ nhà hàng mini card & Huy hiệu nới lỏng
    assert 'chat-card-mini' in html
    assert 'chat-relaxation-badge' in html
    assert 'typewriterEffect' in html

    # 6. Nút nổi Floating Chat Trigger
    assert 'id="floating-chat-trigger"' in html
    assert 'floating-chat-badge' in html


def test_chatbox_api_integration_flow():
    """
    Kiểm tra luồng API tích hợp từ UI Chatbox:
    1. Tạo phiên (initChatSessionIfNeeded -> POST /api/chat/sessions)
    2. Gửi câu hỏi khởi đầu (sendDrawerMessage -> POST /api/chat/sessions/{id}/multi-turn)
    3. Gửi câu hỏi tiếp theo đa lượt (Follow-up multi-turn)
    4. Đóng phiên chat (closeCurrentChatSession -> PUT /api/chat/sessions/{id}/close)
    """
    # 1. Khởi tạo phiên
    create_res = client.post("/api/chat/sessions", json={"user_id": None})
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["session_id"]
    assert session_id is not None
    assert session_data["status"] == "active"

    # 2. Lượt 1: Gửi câu hỏi mẫu NFR-02 "Quán nướng Quận 1 dưới 300k có chỗ đậu ô tô"
    turn1_res = client.post(
        f"/api/chat/sessions/{session_id}/multi-turn",
        json={
            "message": "Quán nướng Quận 1 dưới 300k có chỗ đậu ô tô",
            "provider": "auto",
            "user_id": None
        }
    )
    assert turn1_res.status_code == 200
    turn1_data = turn1_res.json()
    assert turn1_data["session_id"] == session_id
    assert turn1_data["status"] == "active"
    assert "RESULT_PRESENTED" in turn1_data["current_state"]
    assert turn1_data["ai_message"] is not None
    assert len(turn1_data["ai_message"]) > 0

    # 3. Lượt 2: Gửi câu hỏi tiếp theo (Follow-up multi-turn): "Quán nào rẻ hơn nữa không?"
    turn2_res = client.post(
        f"/api/chat/sessions/{session_id}/multi-turn",
        json={
            "message": "Quán nào rẻ hơn nữa không?",
            "provider": "auto",
            "user_id": None
        }
    )
    assert turn2_res.status_code == 200
    turn2_data = turn2_res.json()
    assert turn2_data["session_id"] == session_id
    assert turn2_data["status"] == "active"
    assert "RESULT_PRESENTED" in turn2_data["current_state"]
    assert turn2_data["merged_criteria"] is not None

    # 4. Đóng phiên (closeCurrentChatSession)
    close_res = client.put(
        f"/api/chat/sessions/{session_id}/close",
        json={"reason": "user_ended"}
    )
    assert close_res.status_code == 200
    close_data = close_res.json()
    assert close_data["session_id"] == session_id
    assert close_data["status"] == "closed"
    assert close_data["closed_reason"] == "user_ended"

    # 5. Gửi tiếp khi đã đóng phiên phải trả về lỗi 400
    turn3_after_close = client.post(
        f"/api/chat/sessions/{session_id}/multi-turn",
        json={"message": "Còn quán nào không?"}
    )
    assert turn3_after_close.status_code == 400
    assert "đã kết thúc" in turn3_after_close.json()["detail"].lower()
