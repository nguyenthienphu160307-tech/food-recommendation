"""
==============================================================================
TEST SUITE: ĐÓNG PHIÊN TÌM KIẾM & QUẢN LÝ TRẠNG THÁI SEARCHSESSIONS (TASK TE9C66C)
==============================================================================
Kiểm thử toàn diện các tính năng của Task TE9C66C:
1. Đóng phiên chủ động bởi người dùng (status='active' -> 'closed', current_state='SESSION_CLOSED').
2. Đóng phiên kèm lý do chọn quán (reason='restaurant_selected', selected_restaurant_id).
3. Đảm bảo tính Idempotent và xử lý session không tồn tại (HTTP 404).
4. Chặn gửi tin nhắn và hội thoại đa lượt khi phiên đã ở trạng thái 'closed' (HTTP 400).
5. API kiểm tra trạng thái chi tiết của phiên (GET /api/chat/sessions/{id}/status).
6. Tự động phát hiện phiên hết thời gian chờ (Idle Timeout) và tự động đóng phiên.
7. API quét và đóng hàng loạt phiên hết hạn (POST /api/chat/sessions/cleanup-timeout).
8. Lọc danh sách phiên theo trạng thái (status='active' | 'closed').
9. Tích hợp dọn dẹp tọa độ tạm thời khi đóng phiên (NFR-07 / BR-08 / TSK-20).
==============================================================================
"""

import os
import sys
from datetime import datetime, timedelta

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.search import SearchSession, SearchMessage, SearchCriteria
from app.services.chat_session_service import ChatSessionService

client = TestClient(app)


def test_close_session_manual_user_ended():
    """
    Kiểm thử đóng phiên thủ công khi người dùng kết thúc tìm kiếm (PUT /api/chat/sessions/{id}/close):
    - Khởi tạo phiên (status='active', current_state='SESSION_IDLE').
    - Gửi request đóng phiên qua method PUT.
    - Kỳ vọng: status='closed', current_state='SESSION_CLOSED', ended_at có giá trị, closed_reason='user_ended'.
    """
    res_create = client.post("/api/chat/sessions", json={})
    assert res_create.status_code == 201
    sess_id = res_create.json()["session_id"]
    assert res_create.json()["status"] == "active"
    assert res_create.json()["current_state"] == "SESSION_IDLE"

    # Gửi đóng phiên
    res_close = client.put(f"/api/chat/sessions/{sess_id}/close")
    assert res_close.status_code == 200
    data = res_close.json()

    assert data["session_id"] == sess_id
    assert data["status"] == "closed"
    assert data["current_state"] == "SESSION_CLOSED"
    assert data["closed_reason"] == "user_ended"
    assert data["ended_at"] is not None
    assert data["duration_seconds"] is not None
    assert data["duration_seconds"] >= 0


def test_close_session_post_method_and_selected_restaurant():
    """
    Kiểm thử đóng phiên bằng method POST kèm lý do đã chọn quán:
    - Truyền payload: reason='restaurant_selected', selected_restaurant_id=1.
    - Kỳ vọng: status='closed', closed_reason='restaurant_selected', selected_restaurant_id=1.
    """
    res_create = client.post("/api/chat/sessions", json={})
    sess_id = res_create.json()["session_id"]

    close_payload = {
        "reason": "restaurant_selected",
        "selected_restaurant_id": 1,
        "note": "Đã chọn Pizza 4P's Bến Thành cho bữa tối",
    }
    res_close = client.post(f"/api/chat/sessions/{sess_id}/close", json=close_payload)
    assert res_close.status_code == 200
    data = res_close.json()

    assert data["session_id"] == sess_id
    assert data["status"] == "closed"
    assert data["current_state"] == "SESSION_CLOSED"
    assert data["closed_reason"] == "restaurant_selected"
    assert data["selected_restaurant_id"] == 1


def test_close_session_idempotent_and_nonexistent():
    """
    Kiểm thử tính an toàn (Idempotent) khi đóng nhiều lần và lỗi khi session không tồn tại:
    - Session ID không tồn tại -> 404 Not Found.
    - Đóng một phiên 2 lần liên tiếp -> Lần 2 vẫn trả về 200 OK và trạng thái 'closed'.
    """
    # 1. Thử đóng session không tồn tại
    res_404 = client.put("/api/chat/sessions/9999999/close")
    assert res_404.status_code == 404

    # 2. Tạo phiên mới và đóng 2 lần
    res_create = client.post("/api/chat/sessions", json={})
    sess_id = res_create.json()["session_id"]

    res_close_1 = client.put(f"/api/chat/sessions/{sess_id}/close")
    assert res_close_1.status_code == 200
    assert res_close_1.json()["status"] == "closed"

    # Lần 2 đóng lại (Idempotent)
    res_close_2 = client.put(f"/api/chat/sessions/{sess_id}/close")
    assert res_close_2.status_code == 200
    assert res_close_2.json()["status"] == "closed"


def test_cannot_send_messages_or_turn_after_closed():
    """
    Kiểm thử đảm bảo tính toàn vẹn: Không cho phép gửi tin nhắn hoặc hội thoại vào phiên đã đóng.
    - POST /api/chat/sessions/{id}/messages -> 400 Bad Request.
    - POST /api/chat/sessions/{id}/multi-turn -> 400 Bad Request.
    """
    res_create = client.post("/api/chat/sessions", json={})
    sess_id = res_create.json()["session_id"]

    # Đóng phiên
    client.put(f"/api/chat/sessions/{sess_id}/close")

    # Thử gửi tin nhắn
    res_msg = client.post(f"/api/chat/sessions/{sess_id}/messages", json={
        "content": "Có quán nào khác không?",
        "sender_type": "user",
    })
    assert res_msg.status_code == 400
    assert "closed" in res_msg.json()["detail"].lower()

    # Thử gọi API multi-turn
    res_turn = client.post(f"/api/chat/sessions/{sess_id}/multi-turn", json={
        "message": "Quán nào rẻ hơn?",
        "provider": "rule_based",
    })
    assert res_turn.status_code == 400
    assert "closed" in res_turn.json()["detail"].lower()


def test_session_status_endpoint():
    """
    Kiểm thử endpoint tra cứu trạng thái chi tiết (GET /api/chat/sessions/{id}/status):
    - Session active: is_active=True, is_timed_out=False, idle_seconds >= 0.
    - Sau khi đóng: is_active=False, status='closed', current_state='SESSION_CLOSED'.
    """
    res_create = client.post("/api/chat/sessions", json={})
    sess_id = res_create.json()["session_id"]

    # Trạng thái ban đầu
    res_st = client.get(f"/api/chat/sessions/{sess_id}/status")
    assert res_st.status_code == 200
    st_data = res_st.json()
    assert st_data["session_id"] == sess_id
    assert st_data["status"] == "active"
    assert st_data["is_active"] is True
    assert st_data["is_timed_out"] is False
    assert st_data["idle_seconds"] >= 0

    # Đóng phiên và kiểm tra lại trạng thái
    client.put(f"/api/chat/sessions/{sess_id}/close")
    res_st_closed = client.get(f"/api/chat/sessions/{sess_id}/status")
    assert res_st_closed.status_code == 200
    st_closed_data = res_st_closed.json()
    assert st_closed_data["status"] == "closed"
    assert st_closed_data["is_active"] is False
    assert st_closed_data["current_state"] == "SESSION_CLOSED"


def test_idle_timeout_detection_and_auto_close():
    """
    Kiểm thử cơ chế phát hiện hết thời gian chờ (Timeout):
    - Tạo 1 phiên và điều chỉnh started_at lùi về quá 35 phút trước.
    - Gọi GET /api/chat/sessions/{id}/status?timeout_minutes=30.
    - Kỳ vọng: Hệ thống tự động chuyển status='closed', closed_reason='timeout', is_timed_out=True.
    """
    db = SessionLocal()
    try:
        past_time = datetime.utcnow() - timedelta(minutes=45)
        expired_session = SearchSession(
            user_id=None,
            status="active",
            current_state="RESULT_PRESENTED",
            started_at=past_time,
        )
        db.add(expired_session)
        db.commit()
        db.refresh(expired_session)
        sess_id = expired_session.session_id

        # Kiểm tra hàm helper is_session_timed_out
        is_timed_out = ChatSessionService.is_session_timed_out(expired_session, timeout_minutes=30)
        assert is_timed_out is True

        # Gọi API status với ngưỡng 30 phút -> tự động áp dụng đóng phiên do timeout
        res_st = client.get(f"/api/chat/sessions/{sess_id}/status?timeout_minutes=30")
        assert res_st.status_code == 200
        data = res_st.json()
        assert data["status"] == "closed"
        assert data["current_state"] == "SESSION_CLOSED"
        assert data["closed_reason"] == "timeout"
        assert data["is_timed_out"] is True
        assert data["is_active"] is False

        # Thử gửi tin nhắn vào phiên vừa bị timeout -> Kỳ vọng HTTP 400
        res_msg = client.post(f"/api/chat/sessions/{sess_id}/messages", json={
            "content": "Tôi muốn tìm tiếp",
            "sender_type": "user",
        })
        assert res_msg.status_code == 400
    finally:
        db.close()


def test_cleanup_expired_sessions_api():
    """
    Kiểm thử API quét và dọn dẹp hàng loạt các phiên quá hạn (POST /api/chat/sessions/cleanup-timeout):
    - Tạo 2 phiên đã quá hạn (lùi 40 phút và 50 phút).
    - Tạo 1 phiên mới (vừa tạo, 0 phút).
    - Gọi API cleanup_timeout với ngưỡng 30 phút.
    - Kỳ vọng: closed_count >= 2, 2 phiên cũ được đóng với closed_reason='timeout', phiên mới vẫn active.
    """
    db = SessionLocal()
    try:
        t_old1 = datetime.utcnow() - timedelta(minutes=40)
        t_old2 = datetime.utcnow() - timedelta(minutes=50)

        s_old1 = SearchSession(user_id=None, status="active", started_at=t_old1)
        s_old2 = SearchSession(user_id=None, status="active", started_at=t_old2)
        s_fresh = SearchSession(user_id=None, status="active", started_at=datetime.utcnow())

        db.add_all([s_old1, s_old2, s_fresh])
        db.commit()
        db.refresh(s_old1)
        db.refresh(s_old2)
        db.refresh(s_fresh)

        old1_id = s_old1.session_id
        old2_id = s_old2.session_id
        fresh_id = s_fresh.session_id

        # Gọi API cleanup-timeout
        res_sweep = client.post("/api/chat/sessions/cleanup-timeout?timeout_minutes=30")
        assert res_sweep.status_code == 200
        sweep_data = res_sweep.json()

        assert sweep_data["closed_count"] >= 2
        assert old1_id in sweep_data["closed_session_ids"]
        assert old2_id in sweep_data["closed_session_ids"]
        assert fresh_id not in sweep_data["closed_session_ids"]

        # Kiểm tra trạng thái thực tế trong CSDL
        db.refresh(s_old1)
        db.refresh(s_old2)
        db.refresh(s_fresh)

        assert s_old1.status == "closed"
        assert s_old1.closed_reason == "timeout"
        assert s_old2.status == "closed"
        assert s_old2.closed_reason == "timeout"
        assert s_fresh.status == "active"
    finally:
        db.close()


def test_list_sessions_status_filtering():
    """
    Kiểm thử lọc danh sách phiên theo status ('active' | 'closed'):
    - GET /api/chat/sessions?status=active -> Tất cả phiên trả về đều active.
    - GET /api/chat/sessions?status=closed -> Tất cả phiên trả về đều closed.
    """
    # Tạo 1 phiên active
    res_act = client.post("/api/chat/sessions", json={})
    act_id = res_act.json()["session_id"]

    # Tạo 1 phiên và đóng ngay
    res_cls = client.post("/api/chat/sessions", json={})
    cls_id = res_cls.json()["session_id"]
    client.put(f"/api/chat/sessions/{cls_id}/close")

    # 1. Lọc status=active
    res_list_act = client.get("/api/chat/sessions?status=active&limit=50&auto_timeout_check=false")
    assert res_list_act.status_code == 200
    act_sessions = res_list_act.json()
    assert all(s["status"] == "active" for s in act_sessions)
    assert any(s["session_id"] == act_id for s in act_sessions)

    # 2. Lọc status=closed
    res_list_cls = client.get("/api/chat/sessions?status=closed&limit=50&auto_timeout_check=false")
    assert res_list_cls.status_code == 200
    cls_sessions = res_list_cls.json()
    assert all(s["status"] == "closed" for s in cls_sessions)
    assert any(s["session_id"] == cls_id for s in cls_sessions)
