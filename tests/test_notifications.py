"""
Bộ kiểm thử Tự động cho Task TSK-48 / PBI-17:
Xây dựng Hệ thống Thông báo người dùng (Notifications Service)
Mô tả: Tạo và gửi thông báo vào bảng Notifications khi người dùng nhận phản hồi đánh giá hoặc thông báo hệ thống; API đánh dấu đã đọc (is_read).

12 Ca kiểm thử toàn diện:
1.  TEST 01: Tạo thông báo đơn lẻ (create_notification) & kiểm tra giá trị mặc định is_read = False.
2.  TEST 02: Chặn tạo hoặc truy vấn thông báo với user_id không tồn tại (HTTP 404 / BR-01).
3.  TEST 03: Tạo thông báo phản hồi đánh giá (notify_review_reply - Module 5 trigger).
4.  TEST 04: Tạo thông báo trạng thái tài khoản (notify_account_status - locked/active).
5.  TEST 05: Gửi thông báo hệ thống hàng loạt (Broadcast notification).
6.  TEST 06: Đếm số lượng thông báo chưa đọc (get_unread_count - Badge UI counter).
7.  TEST 07: Lấy danh sách thông báo có phân trang (page, limit) và sắp xếp mới nhất lên đầu.
8.  TEST 08: Lọc danh sách chỉ lấy thông báo chưa đọc (unread_only = True).
9.  TEST 09: Đánh dấu 1 thông báo cụ thể là đã đọc (mark_as_read) & kiểm tra phân quyền bảo mật (403 Forbidden).
10. TEST 10: Đánh dấu tất cả thông báo của người dùng là đã đọc (mark_all_as_read).
11. TEST 11: Xóa thông báo (delete_notification) & kiểm tra Cascade Delete khi xóa người dùng.
12. TEST 12: Kiểm thử toàn diện qua các Router Handlers của router /api/notifications.
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
from fastapi import HTTPException

from app.core.database import Base
import app.models
from app.models.user import User
from app.models.notification import Notification
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationCreateRequest,
    NotificationBroadcastRequest,
    ReviewReplyNotificationRequest,
    AccountStatusNotificationRequest,
)
from app.routers.notification import (
    get_user_notifications,
    get_unread_count,
    create_notification,
    broadcast_notification,
    trigger_review_reply_notification,
    trigger_account_status_notification,
    mark_notification_as_read,
    mark_all_notifications_as_read,
    delete_notification,
)

# Khởi tạo SQLite in-memory test database độc lập và siêu nhanh
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def run_tests():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-48: HỆ THỐNG THÔNG BÁO NGƯỜI DÙNG (NOTIFICATIONS)")
    print("=" * 80)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    # 1. Khởi tạo dữ liệu người dùng kiểm thử
    user_a = User(
        email="user_a@foodai.vn",
        phone_number="0901111222",
        hashed_password="hashed_pwd_123",
        status="active"
    )
    user_b = User(
        email="user_b@foodai.vn",
        phone_number="0903333444",
        hashed_password="hashed_pwd_456",
        status="active"
    )
    user_locked = User(
        email="user_locked@foodai.vn",
        phone_number="0905555666",
        hashed_password="hashed_pwd_789",
        status="locked"
    )
    db.add_all([user_a, user_b, user_locked])
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)
    db.refresh(user_locked)

    passed_count = 0

    # -------------------------------------------------------------------------
    # TEST 01: Tạo thông báo đơn lẻ
    # -------------------------------------------------------------------------
    print("\n[TEST 01] Tạo thông báo đơn lẻ (create_notification) & kiểm tra is_read = False...")
    notif_1 = NotificationService.create_notification(
        db=db,
        user_id=user_a.id,
        title="Chào mừng bạn đến với Smart Dining!",
        content="Hệ thống giúp bạn tìm kiếm địa điểm ăn uống ngon và phù hợp nhất.",
        notification_type="system"
    )
    assert notif_1.id is not None, "Notification ID phải tự động sinh."
    assert notif_1.user_id == user_a.id, "user_id phải khớp với người nhận."
    assert notif_1.is_read is False, "Thông báo mới phải có is_read = False."
    assert notif_1.type == "system", "Loại thông báo phải là 'system'."
    assert isinstance(notif_1.created_at, datetime), "created_at phải là kiểu datetime."
    print(" => PASSED: Thông báo đơn lẻ được lưu thành công với is_read = False.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 02: Chặn tạo hoặc truy vấn thông báo với user_id không tồn tại
    # -------------------------------------------------------------------------
    print("\n[TEST 02] Chặn thao tác với user_id không tồn tại (HTTP 404)...")
    try:
        NotificationService.create_notification(
            db=db,
            user_id=99999,
            title="Lỗi người dùng",
            content="Nội dung kiểm thử."
        )
        assert False, "Phải ném ngoại lệ HTTPException khi user_id không tồn tại."
    except HTTPException as e:
        assert e.status_code == 404, f"Status code phải là 404, nhận được: {e.status_code}"
    
    try:
        NotificationService.get_unread_count(db=db, user_id=99999)
        assert False, "Phải ném ngoại lệ khi đếm unread với user_id không tồn tại."
    except HTTPException as e:
        assert e.status_code == 404
    print(" => PASSED: Chặn thành công thao tác với user_id không tồn tại (404 Not Found).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 03: Tạo thông báo phản hồi đánh giá (notify_review_reply)
    # -------------------------------------------------------------------------
    print("\n[TEST 03] Tạo thông báo phản hồi đánh giá (notify_review_reply)...")
    reply_notif = NotificationService.notify_review_reply(
        db=db,
        user_id=user_a.id,
        restaurant_name="Quán Bò Nướng Phố",
        reviewer_name="Chủ quán Minh",
        reply_content="Cảm ơn bạn đã ghé quán! Quán rất hân hạnh được phục vụ bạn lần sau."
    )
    assert reply_notif.type == "review_reply", "Loại thông báo phải là 'review_reply'."
    assert "Quán Bò Nướng Phố" in reply_notif.title, "Tiêu đề phải chứa tên quán."
    assert "Chủ quán Minh" in reply_notif.content, "Nội dung phải chứa tên người phản hồi."
    assert reply_notif.is_read is False
    print(" => PASSED: Thông báo phản hồi đánh giá được tạo chuẩn xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 04: Tạo thông báo trạng thái tài khoản (notify_account_status)
    # -------------------------------------------------------------------------
    print("\n[TEST 04] Tạo thông báo thay đổi trạng thái tài khoản (notify_account_status)...")
    lock_notif = NotificationService.notify_account_status(
        db=db,
        user_id=user_a.id,
        new_status="locked",
        reason="Vi phạm quy tắc đăng tải đánh giá spam"
    )
    assert lock_notif.type == "account_status"
    assert "bị khóa" in lock_notif.title.lower()
    assert "spam" in lock_notif.content

    unlock_notif = NotificationService.notify_account_status(
        db=db,
        user_id=user_a.id,
        new_status="active",
        reason="Đã xem xét khiếu nại thành công"
    )
    assert "kích hoạt" in unlock_notif.title.lower()
    print(" => PASSED: Thông báo trạng thái tài khoản (locked & active) sinh chính xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 05: Gửi thông báo hệ thống hàng loạt (Broadcast)
    # -------------------------------------------------------------------------
    print("\n[TEST 05] Gửi thông báo hệ thống hàng loạt (Broadcast)...")
    broadcast_list = NotificationService.broadcast_notification(
        db=db,
        title="Bảo trì hệ thống định kỳ",
        content="Hệ thống sẽ bảo trì từ 01:00 đến 03:00 sáng mai.",
        notification_type="system"
    )
    # Hệ thống có 2 user active (user_a, user_b), user_locked không nhận
    assert len(broadcast_list) == 2, f"Số thông báo broadcast phải là 2, nhận được {len(broadcast_list)}"
    recipient_ids = [n.user_id for n in broadcast_list]
    assert user_a.id in recipient_ids and user_b.id in recipient_ids
    assert user_locked.id not in recipient_ids

    # Broadcast chỉ định danh sách user_ids
    specific_broadcast = NotificationService.broadcast_notification(
        db=db,
        title="Cập nhật chính sách người dùng bị khóa",
        content="Chính sách hỗ trợ tài khoản.",
        notification_type="system",
        user_ids=[user_locked.id]
    )
    assert len(specific_broadcast) == 1
    assert specific_broadcast[0].user_id == user_locked.id
    print(" => PASSED: Broadcast hoạt động chính xác cho cả active users và danh sách chỉ định.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 06: Đếm số lượng thông báo chưa đọc (get_unread_count)
    # -------------------------------------------------------------------------
    print("\n[TEST 06] Đếm số lượng thông báo chưa đọc (get_unread_count)...")
    unread_a = NotificationService.get_unread_count(db=db, user_id=user_a.id)
    # user_a có: notif_1 + reply_notif + lock_notif + unlock_notif + 1 broadcast = 5 thông báo chưa đọc
    assert unread_a == 5, f"Số thông báo chưa đọc của user_a phải là 5, nhận: {unread_a}"
    unread_b = NotificationService.get_unread_count(db=db, user_id=user_b.id)
    assert unread_b == 1, f"user_b chỉ nhận 1 thông báo broadcast, nhận: {unread_b}"
    print(f" => PASSED: Đếm chính xác unread_count (User A: {unread_a}, User B: {unread_b}).")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 07: Lấy danh sách thông báo phân trang và sắp xếp mới nhất lên đầu
    # -------------------------------------------------------------------------
    print("\n[TEST 07] Phân trang danh sách thông báo (page, limit, created_at DESC)...")
    res_page1 = NotificationService.get_user_notifications(db=db, user_id=user_a.id, page=1, limit=3)
    assert res_page1["total"] == 5, f"Tổng số phải là 5, nhận: {res_page1['total']}"
    assert res_page1["unread_count"] == 5
    assert len(res_page1["items"]) == 3, f"Số lượng trang 1 phải là 3, nhận: {len(res_page1['items'])}"
    # Kiểm tra thứ tự sắp xếp giảm dần theo thời gian/ID
    items = res_page1["items"]
    assert items[0].id > items[1].id > items[2].id, "Danh sách phải sắp xếp ID giảm dần (mới nhất trước)."

    res_page2 = NotificationService.get_user_notifications(db=db, user_id=user_a.id, page=2, limit=3)
    assert len(res_page2["items"]) == 2, f"Trang 2 phải có 2 thông báo còn lại, nhận: {len(res_page2['items'])}"
    print(" => PASSED: Phân trang và thứ tự sắp xếp mới nhất hoạt động hoàn hảo.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 08: Lọc danh sách chỉ lấy thông báo chưa đọc (unread_only = True)
    # -------------------------------------------------------------------------
    print("\n[TEST 08] Lọc danh sách theo unread_only = True...")
    # Đánh dấu 1 thông báo là đã đọc
    NotificationService.mark_as_read(db=db, notification_id=notif_1.id, user_id=user_a.id)
    assert notif_1.is_read is True

    filtered_res = NotificationService.get_user_notifications(
        db=db, user_id=user_a.id, page=1, limit=10, unread_only=True
    )
    assert filtered_res["total"] == 4, f"Tổng số thông báo chưa đọc phải còn 4, nhận: {filtered_res['total']}"
    assert filtered_res["unread_count"] == 4
    for item in filtered_res["items"]:
        assert item.is_read is False, "Tất cả các mục trả về khi unread_only=True phải có is_read=False."
    print(" => PASSED: Bộ lọc unread_only hoạt động chính xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 09: Đánh dấu 1 thông báo là đã đọc & kiểm tra bảo mật (403 Forbidden)
    # -------------------------------------------------------------------------
    print("\n[TEST 09] Đánh dấu 1 thông báo đã đọc & kiểm tra phân quyền (403 Forbidden)...")
    # user_b cố tình đánh dấu thông báo của user_a
    try:
        NotificationService.mark_as_read(db=db, notification_id=reply_notif.id, user_id=user_b.id)
        assert False, "Phải ném ngoại lệ 403 Forbidden khi thao tác trên thông báo của người khác."
    except HTTPException as e:
        assert e.status_code == 403, f"Status code phải là 403, nhận: {e.status_code}"
    
    # user_a đánh dấu thông báo của chính mình
    updated_notif = NotificationService.mark_as_read(db=db, notification_id=reply_notif.id, user_id=user_a.id)
    assert updated_notif.is_read is True
    new_unread_a = NotificationService.get_unread_count(db=db, user_id=user_a.id)
    assert new_unread_a == 3, f"Số unread phải giảm còn 3, nhận: {new_unread_a}"
    print(" => PASSED: Kiểm tra phân quyền 403 Forbidden và cập nhật is_read thành công.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 10: Đánh dấu tất cả thông báo của người dùng đã đọc (mark_all_as_read)
    # -------------------------------------------------------------------------
    print("\n[TEST 10] Đánh dấu tất cả thông báo đã đọc (mark_all_as_read)...")
    updated_count = NotificationService.mark_all_as_read(db=db, user_id=user_a.id)
    assert updated_count == 3, f"Số bản ghi cập nhật phải là 3, nhận: {updated_count}"
    
    unread_after_all = NotificationService.get_unread_count(db=db, user_id=user_a.id)
    assert unread_after_all == 0, f"Sau khi mark all, unread phải là 0, nhận: {unread_after_all}"

    # Gọi lại mark_all khi không còn thông báo chưa đọc nào
    updated_zero = NotificationService.mark_all_as_read(db=db, user_id=user_a.id)
    assert updated_zero == 0
    print(" => PASSED: Đánh dấu tất cả đã đọc thành công, unread_count về 0.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 11: Xóa thông báo & Kiểm tra Cascade Delete khi xóa User
    # -------------------------------------------------------------------------
    print("\n[TEST 11] Xóa thông báo (delete_notification) & kiểm tra Cascade Delete...")
    # Thử xóa với user không phải chủ sở hữu
    try:
        NotificationService.delete_notification(db=db, notification_id=notif_1.id, user_id=user_b.id)
        assert False, "Phải ném 403 khi xóa thông báo của người khác."
    except HTTPException as e:
        assert e.status_code == 403

    # Xóa hợp lệ bởi chính user_a
    deleted = NotificationService.delete_notification(db=db, notification_id=notif_1.id, user_id=user_a.id)
    assert deleted is True
    # Kiểm tra không còn trong DB
    check_notif = db.query(Notification).filter(Notification.id == notif_1.id).first()
    assert check_notif is None

    # Kiểm tra Cascade Delete: Tạo 1 user tạm thời kèm thông báo, rồi xóa user đó
    temp_user = User(email="temp@foodai.vn", hashed_password="pwd", status="active")
    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)
    temp_notif = NotificationService.create_notification(
        db=db, user_id=temp_user.id, title="Thông báo tạm", content="Sẽ bị xóa theo user"
    )
    temp_notif_id = temp_notif.id
    # Xóa temp_user
    db.delete(temp_user)
    db.commit()
    # Kiểm tra thông báo tự động bị xóa theo CASCADE
    cascade_check = db.query(Notification).filter(Notification.id == temp_notif_id).first()
    assert cascade_check is None, "Thông báo phải tự động bị xóa khi user bị xóa (CASCADE)."
    print(" => PASSED: Xóa thông báo phân quyền 403 và Cascade Delete hoạt động chính xác.")
    passed_count += 1

    # -------------------------------------------------------------------------
    # TEST 12: Kiểm thử toàn bộ Router Handlers của router /api/notifications
    # -------------------------------------------------------------------------
    print("\n[TEST 12] Kiểm thử toàn bộ Router Handlers của router /api/notifications...")
    
    # 1. create_notification handler
    create_payload = NotificationCreateRequest(
        user_id=user_b.id,
        title="Ưu đãi ẩm thực cuối tuần",
        content="Giảm giá 20% tại các nhà hàng buffet lẩu.",
        type="system"
    )
    r_created = create_notification(payload=create_payload, db=db)
    assert r_created.id is not None
    assert r_created.is_read is False
    created_id = r_created.id

    # 2. get_unread_count handler
    r_unread = get_unread_count(user_id=user_b.id, db=db)
    assert r_unread.unread_count >= 2

    # 3. broadcast_notification handler
    broadcast_payload = NotificationBroadcastRequest(
        title="Tính năng mới: AI Chatbot gợi ý",
        content="Trải nghiệm tính năng tìm kiếm thông minh.",
        type="system"
    )
    r_broadcast = broadcast_notification(payload=broadcast_payload, db=db)
    assert len(r_broadcast) >= 2

    # 4. trigger_review_reply_notification handler
    reply_payload = ReviewReplyNotificationRequest(
        user_id=user_b.id,
        restaurant_name="Lẩu Haidilao Landmark",
        reviewer_name="Quản lý Trần",
        reply_content="Cảm ơn quý khách đã gửi đánh giá!"
    )
    r_reply = trigger_review_reply_notification(payload=reply_payload, db=db)
    assert r_reply.type == "review_reply"

    # 5. trigger_account_status_notification handler
    status_payload = AccountStatusNotificationRequest(
        user_id=user_b.id,
        new_status="locked",
        reason="Kiểm tra bảo mật"
    )
    r_status = trigger_account_status_notification(payload=status_payload, db=db)
    assert r_status.type == "account_status"

    # 6. get_user_notifications handler (kèm phân trang)
    r_list = get_user_notifications(user_id=user_b.id, page=1, limit=5, unread_only=False, db=db)
    assert r_list.total >= 4
    assert len(r_list.items) <= 5

    # 7. mark_notification_as_read handler
    r_marked = mark_notification_as_read(notification_id=created_id, user_id=user_b.id, db=db)
    assert r_marked.is_read is True

    # 8. mark_all_notifications_as_read handler
    r_marked_all = mark_all_notifications_as_read(user_id=user_b.id, db=db)
    assert r_marked_all.success is True
    assert r_marked_all.updated_count > 0

    # Kiểm tra lại unread count sau khi mark all
    r_unread_after = get_unread_count(user_id=user_b.id, db=db)
    assert r_unread_after.unread_count == 0

    # 9. delete_notification handler
    r_del = delete_notification(notification_id=created_id, user_id=user_b.id, db=db)
    assert r_del["success"] is True

    print(" => PASSED: Toàn bộ 9 Router Handlers của router /api/notifications hoạt động chuẩn xác.")
    passed_count += 1

    print("\n" + "=" * 80)
    print(f"KẾT QUẢ KIỂM THỬ: {passed_count}/12 CA KIỂM THỬ ĐÃ VƯỢT QUA HOÀN TOÀN (100% PASSED)!")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
