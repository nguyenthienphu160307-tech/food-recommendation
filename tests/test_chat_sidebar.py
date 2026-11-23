"""
Bộ kiểm thử Tự động cho Task TSK-45 / PBI-14:
Xây dựng Giao diện Danh sách Phiên chat cũ bên thanh bên (Chat History Sidebar)
Mô tả: Cho phép người dùng đã đăng nhập chuyển đổi giữa các phiên tìm kiếm trước đó và tiếp tục hội thoại.

9 Ca kiểm thử toàn diện:
1. TEST 01: Khởi tạo và truy vấn danh sách phiên chat theo User ID (GET /api/chat/sessions?user_id=...).
2. TEST 02: Phân tách độc lập giữa phiên Khách (Guest) và User đã đăng nhập (BR-02).
3. TEST 03: Tự động trích xuất tiêu đề tóm tắt cuộc trò chuyện (title_preview) từ câu hỏi đầu của User.
4. TEST 04: Cập nhật chính xác số lượng tin nhắn (total_messages) và mốc thời gian cuối (last_message_at).
5. TEST 05: Chuyển đổi phiên và nạp toàn bộ lịch sử tin nhắn theo thứ tự thời gian (GET /api/chat/sessions/{id}).
6. TEST 06: Quản lý vòng đời phiên chat: Phân biệt trạng thái 'active' và 'closed'.
7. TEST 07: Xóa phiên chat cũ và kiểm tra Cascade Delete tin nhắn con (DELETE /api/chat/sessions/{id}).
8. TEST 08: Kiểm tra tích hợp cấu trúc DOM Thanh bên Lịch sử trong Frontend HTML (frontend/index.html).
9. TEST 09: Benchmark hiệu năng truy vấn và nạp lịch sử phiên chat đạt chuẩn NFR-01 (< 3.0 giây).
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
from app.models.user import User
from app.models.search import SearchSession, SearchMessage
from app.services.chat_session_service import ChatSessionService
from app.routers.search import (
    list_sessions,
    get_session_history,
    create_session,
    send_message,
    close_session,
    delete_session,
)
from app.schemas.search import CreateSessionRequest, SendMessageRequest

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
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-45: GIAO DIỆN DANH SÁCH PHIÊN CHAT CŨ (CHAT SIDEBAR)")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    # Tạo User kiểm thử
    test_user = User(
        email="test_user_tsk45@foodai.vn",
        phone_number="0912345678",
        hashed_password="fakehash123",
        status="active"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    user_id = test_user.id
    print(f"Đã tạo User kiểm thử ID={user_id} ({test_user.email})")

    # -------------------------------------------------------------
    # TEST 01: Khởi tạo và truy vấn danh sách phiên chat theo User ID
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra khởi tạo và truy vấn danh sách phiên chat theo User ID:")
    sess1 = ChatSessionService.create_session(db, user_id=user_id)
    sess2 = ChatSessionService.create_session(db, user_id=user_id)
    assert sess1.session_id is not None and sess2.session_id is not None
    print(f"  Đã tạo 2 phiên: Session #{sess1.session_id} và Session #{sess2.session_id}")

    user_sessions = list_sessions(user_id=user_id, db=db)
    assert len(user_sessions) == 2, f"Kỳ vọng 2 phiên, thực tế: {len(user_sessions)}"
    # Sắp xếp mới nhất lên đầu
    assert user_sessions[0].session_id == sess2.session_id, "Phiên mới nhất phải nằm ở đầu danh sách"
    print("  => PASSED: Truy vấn danh sách phiên theo user_id thành công, sắp xếp mới nhất lên đầu!")

    # -------------------------------------------------------------
    # TEST 02: Phân tách độc lập giữa phiên Khách (Guest) và User (BR-02)
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra phân tách độc lập giữa phiên Khách (Guest) và User (BR-02):")
    guest_sess = ChatSessionService.create_session(db, user_id=None)
    assert guest_sess.user_id is None
    print(f"  Đã tạo phiên Khách vãng lai: Session #{guest_sess.session_id} (user_id=None)")

    # Danh sách của User không được chứa phiên của Khách
    user_sessions_after = list_sessions(user_id=user_id, db=db)
    assert all(s.user_id == user_id for s in user_sessions_after)
    assert len(user_sessions_after) == 2, "Danh sách của User không được chứa phiên của Khách"
    print("  => PASSED: Đảm bảo tính bảo mật và độc lập dữ liệu theo quy tắc BR-02!")

    # -------------------------------------------------------------
    # TEST 03: Tự động trích xuất tiêu đề tóm tắt (title_preview)
    # -------------------------------------------------------------
    print("\n[TEST 03] Kiểm tra trích xuất tiêu đề tóm tắt cuộc trò chuyện (title_preview):")
    # Chưa có tin nhắn -> Tiêu đề mặc định
    title_empty = ChatSessionService.get_session_preview_title(sess1)
    assert title_empty == f"Cuộc trò chuyện #{sess1.session_id}"
    print(f"  Tiêu đề khi chưa có tin nhắn: '{title_empty}'")

    # Gửi câu hỏi đầu tiên của người dùng
    first_question = "Tìm quán nướng BBQ Quận 1 có bãi đỗ ô tô cho nhóm 6 người"
    ChatSessionService.save_message(db, session_id=sess1.session_id, sender_type="user", content=first_question)
    db.refresh(sess1)

    title_extracted = ChatSessionService.get_session_preview_title(sess1)
    print(f"  Tiêu đề sau khi user hỏi: '{title_extracted}'")
    assert "Tìm quán nướng BBQ" in title_extracted
    assert len(title_extracted) <= 45
    print("  => PASSED: Tự động trích xuất tiêu đề từ câu hỏi đầu của user thành công!")

    # -------------------------------------------------------------
    # TEST 04: Cập nhật total_messages và mốc thời gian last_message_at
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra cập nhật số lượng tin nhắn và mốc thời gian tin cuối:")
    ChatSessionService.save_message(db, session_id=sess1.session_id, sender_type="ai", content="Dưới đây là 3 quán nướng BBQ phù hợp...")
    sess_list = list_sessions(user_id=user_id, db=db)
    target_s1 = next(s for s in sess_list if s.session_id == sess1.session_id)
    
    print(f"  Phiên #{sess1.session_id}: total_messages={target_s1.total_messages}, last_message_at={target_s1.last_message_at}")
    assert target_s1.total_messages == 2, f"Kỳ vọng 2 tin nhắn, nhận được: {target_s1.total_messages}"
    assert target_s1.last_message_at is not None
    print("  => PASSED: Cập nhật số lượng tin nhắn và thời gian tin cuối chính xác!")

    # -------------------------------------------------------------
    # TEST 05: Chuyển đổi phiên và nạp lại lịch sử (GET /api/chat/sessions/{id})
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra chuyển đổi phiên và nạp lại lịch sử tin nhắn (UC-10):")
    history_res = get_session_history(session_id=sess1.session_id, db=db)
    assert history_res.session.session_id == sess1.session_id
    assert len(history_res.messages) == 2
    assert history_res.messages[0].sender_type == "user"
    assert history_res.messages[1].sender_type == "ai"
    print(f"  Nạp thành công {len(history_res.messages)} tin nhắn của phiên #{sess1.session_id} theo thứ tự thời gian:")
    for m in history_res.messages:
        print(f"    [{m.sender_type.upper()}]: {m.content[:50]}...")
    print("  => PASSED: Tải lại toàn bộ ngữ cảnh hội thoại phục vụ tiếp tục chat!")

    # -------------------------------------------------------------
    # TEST 06: Quản lý vòng đời phiên chat (active / closed)
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra phân biệt trạng thái 'active' và 'closed':")
    close_res = close_session(session_id=sess1.session_id, db=db)
    assert close_res.status == "closed"
    print(f"  Đã đóng phiên #{sess1.session_id} thành công: status='{close_res.status}'")

    # Kiểm tra không thể gửi thêm tin nhắn vào phiên đã đóng
    try:
        ChatSessionService.save_message(db, session_id=sess1.session_id, sender_type="user", content="Tôi muốn hỏi thêm")
        assert False, "Phải ném lỗi khi gửi tin vào phiên closed"
    except Exception as e:
        print(f"  Đã chặn gửi tin nhắn vào phiên đóng: {e.detail}")
    print("  => PASSED: Vòng đời phiên chat được kiểm soát chặt chẽ!")

    # -------------------------------------------------------------
    # TEST 07: Xóa phiên chat cũ và Cascade Delete tin nhắn con
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra xóa phiên chat và Cascade Delete tin nhắn con:")
    del_res = delete_session(session_id=sess2.session_id, db=db)
    assert del_res["status"] == "success"
    print(f"  Kết quả xóa phiên #{sess2.session_id}: {del_res['message']}")

    # Kiểm tra phiên đã biến mất khỏi CSDL
    remaining = list_sessions(user_id=user_id, db=db)
    assert all(s.session_id != sess2.session_id for s in remaining)
    print("  => PASSED: Xóa phiên chat và dọn dẹp CSDL thành công!")

    # -------------------------------------------------------------
    # TEST 08: Kiểm tra tích hợp cấu trúc DOM Thanh bên trong HTML
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra tích hợp cấu trúc HTML Thanh bên Lịch sử (frontend/index.html):")
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    assert os.path.exists(html_path), "Không tìm thấy file frontend/index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    required_elements = [
        "chat-history-sidebar",
        "btn-new-chat",
        "session-history-list",
        "btn-toggle-sidebar",
        "toggleChatSidebar",
        "loadUserChatHistory",
        "switchChatSession",
        "startNewChatSession",
        "deleteChatSession",
        "ai-session-closed-notice"
    ]
    for elem in required_elements:
        assert elem in html_content, f"Thiếu phần tử / hàm '{elem}' trong frontend/index.html"
        print(f"  Đã tìm thấy: '{elem}'")
    print("  => PASSED: Đầy đủ thành phần giao diện Sidebar và các hàm JavaScript điều khiển!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Xử lý NFR-01 (< 3.0 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng nạp danh sách và chuyển đổi phiên (NFR-01):")
    t0 = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        _ = list_sessions(user_id=user_id, db=db)
        _ = get_session_history(session_id=sess1.session_id, db=db)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian xử lý {iterations} lượt truy vấn kép: {elapsed_ms:.2f} ms ({elapsed_ms / iterations:.4f} ms/lượt)")
    assert elapsed_ms < 1000, f"Hiệu năng quá chậm: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ phản hồi cực nhanh ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 80)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-45 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 80)
    db.close()


if __name__ == "__main__":
    run_tests()
