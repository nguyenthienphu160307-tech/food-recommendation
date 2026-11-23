import os
import sys

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo import được module app từ thư mục gốc
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User

client = TestClient(app)


def test_chat_session_suite():
    # 0. Lấy 1 user mẫu từ CSDL để dùng cho test
    db = SessionLocal()
    sample_user = db.query(User).first()
    sample_user_id = sample_user.id if sample_user else None
    db.close()

    print("\n--- [TEST 1] Khởi tạo phiên chat cho Khách vãng lai (Guest Mode - user_id=None / BR-02) ---")
    res_guest = client.post("/api/chat/sessions", json={})
    assert res_guest.status_code == 201
    guest_session = res_guest.json()
    print("Response Guest Session:", guest_session)
    assert guest_session["user_id"] is None
    assert guest_session["status"] == "active"
    guest_session_id = guest_session["session_id"]
    print(f"-> Tạo thành công phiên Guest session_id={guest_session_id} (HTTP 201)")

    if sample_user_id:
        print(f"\n--- [TEST 2] Khởi tạo phiên chat cho Người dùng đã đăng nhập (user_id={sample_user_id}) ---")
        res_user = client.post("/api/chat/sessions", json={"user_id": sample_user_id})
        assert res_user.status_code == 201
        user_session = res_user.json()
        print("Response User Session:", user_session)
        assert user_session["user_id"] == sample_user_id
        assert user_session["status"] == "active"
        print(f"-> Tạo thành công phiên User session_id={user_session['session_id']} (HTTP 201)")

    print("\n--- [TEST 3] Thử tạo phiên với user_id KHÔNG TỒN TẠI (Kỳ vọng HTTP 404) ---")
    res_invalid_user = client.post("/api/chat/sessions", json={"user_id": 999999})
    assert res_invalid_user.status_code == 404
    print("-> Đã chặn đúng user không tồn tại (HTTP 404)!")

    print(f"\n--- [TEST 4] Gửi tin nhắn câu hỏi của Người dùng (sender_type='user') theo thời gian thực ---")
    res_msg1 = client.post(f"/api/chat/sessions/{guest_session_id}/messages", json={
        "content": "Tôi đang ở Quận 1, muốn tìm quán lẩu nướng có chỗ đậu ô tô dưới 300k/người",
        "sender_type": "user"
    })
    assert res_msg1.status_code == 201
    msg1 = res_msg1.json()
    print("Tin nhắn User đã lưu:", msg1)
    assert msg1["sender_type"] == "user"
    assert "Quận 1" in msg1["content"]

    print(f"\n--- [TEST 5] Gửi câu trả lời của Trợ lý ảo (sender_type='ai') theo thời gian thực ---")
    res_msg2 = client.post(f"/api/chat/sessions/{guest_session_id}/messages", json={
        "content": "Chào bạn, mình đã tìm thấy 3 nhà hàng thỏa mãn yêu cầu của bạn tại Quận 1 gồm Lẩu Nướng Gogi, Cơm Niêu Sài Gòn...",
        "sender_type": "ai"
    })
    assert res_msg2.status_code == 201
    msg2 = res_msg2.json()
    print("Tin nhắn AI đã lưu:", msg2)
    assert msg2["sender_type"] == "ai"

    print(f"\n--- [TEST 6] Truy xuất toàn bộ lịch sử tin nhắn của phiên #{guest_session_id} ---")
    res_history = client.get(f"/api/chat/sessions/{guest_session_id}")
    assert res_history.status_code == 200
    history = res_history.json()
    print("Tổng số tin nhắn:", history["session"]["total_messages"])
    assert history["session"]["total_messages"] >= 2
    assert len(history["messages"]) >= 2
    # Kiểm tra thứ tự tăng dần theo thời gian (created_at ASC)
    assert history["messages"][0]["sender_type"] == "user"
    assert history["messages"][1]["sender_type"] == "ai"
    print("-> Lịch sử tin nhắn được sắp xếp chuẩn xác theo thời gian thực!")

    print(f"\n--- [TEST 7] Đóng phiên hội thoại chat (#{guest_session_id}) ---")
    res_close = client.put(f"/api/chat/sessions/{guest_session_id}/close")
    assert res_close.status_code == 200
    closed_data = res_close.json()
    print("Response Close:", closed_data)
    assert closed_data["status"] == "closed"

    print(f"\n--- [TEST 8] Kiểm tra chặn gửi tin nhắn vào phiên đã đóng (Kỳ vọng HTTP 400) ---")
    res_msg_closed = client.post(f"/api/chat/sessions/{guest_session_id}/messages", json={
        "content": "Thêm một câu hỏi khi phiên đã kết thúc",
        "sender_type": "user"
    })
    assert res_msg_closed.status_code == 400
    print("Response detail:", res_msg_closed.json()["detail"])
    print("-> Đã chặn đúng không cho gửi tin nhắn vào phiên đã đóng (HTTP 400)!")

    print("\n>>> TẤT CẢ 8 CA KIỂM THỬ TASK TSK-16 ĐỀU ĐẠT CHUẨN (ALL TESTS PASSED)! <<<")


if __name__ == "__main__":
    test_chat_session_suite()
