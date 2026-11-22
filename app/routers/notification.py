from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationCreateRequest,
    NotificationBroadcastRequest,
    NotificationResponse,
    NotificationListResponse,
    UnreadCountResponse,
    MarkReadResponse,
    ReviewReplyNotificationRequest,
    AccountStatusNotificationRequest,
)

router = APIRouter(prefix="/api/notifications", tags=["Hệ thống Thông báo (Notifications - TSK-48)"])


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách thông báo của người dùng (TSK-48 / PBI-17)"
)
def get_user_notifications(
    user_id: int = Query(..., description="ID người dùng đã đăng nhập (bắt buộc theo BR-01)"),
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng thông báo trên trang"),
    unread_only: bool = Query(False, description="Chỉ lấy thông báo chưa đọc (True/False)"),
    db: Session = Depends(get_db)
):
    """
    API Lấy danh sách thông báo cá nhân của người dùng:
    - Sắp xếp thông báo mới nhất lên đầu (created_at DESC).
    - Hỗ trợ phân trang chuẩn RESTful (page, limit).
    - Hỗ trợ lọc chỉ xem thông báo chưa đọc (unread_only=True).
    - Trả về tổng số thông báo (`total`) và số lượng chưa đọc (`unread_count`) để cập nhật badge UI.
    """
    # Xử lý tương thích khi hàm được gọi trực tiếp trong Unit Test
    if hasattr(page, "default"):
        page = page.default
    if hasattr(limit, "default"):
        limit = limit.default
    if hasattr(unread_only, "default"):
        unread_only = unread_only.default

    result = NotificationService.get_user_notifications(
        db=db,
        user_id=user_id,
        page=page,
        limit=limit,
        unread_only=unread_only
    )
    return NotificationListResponse(**result)


@router.get(
    "/unread-count",
    response_model=UnreadCountResponse,
    status_code=status.HTTP_200_OK,
    summary="Đếm số lượng thông báo chưa đọc (Badge Counter - TSK-48)"
)
def get_unread_count(
    user_id: int = Query(..., description="ID người dùng đã đăng nhập"),
    db: Session = Depends(get_db)
):
    """
    API lấy nhanh số lượng thông báo chưa đọc của người dùng:
    - Dùng để hiển thị badge số lượng đỏ trên icon quả chuông ở thanh điều hướng.
    """
    count = NotificationService.get_unread_count(db=db, user_id=user_id)
    return UnreadCountResponse(user_id=user_id, unread_count=count)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo thông báo mới cho người dùng (TSK-48)"
)
def create_notification(
    payload: NotificationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    API tạo một bản ghi thông báo mới vào bảng Notifications:
    - Dành cho Admin hoặc các dịch vụ nghiệp vụ nội bộ khi phát sinh sự kiện.
    - Mặc định `is_read = False`.
    """
    notification = NotificationService.create_notification(
        db=db,
        user_id=payload.user_id,
        title=payload.title,
        content=payload.content,
        notification_type=payload.type
    )
    return notification


@router.post(
    "/broadcast",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Gửi thông báo hệ thống hàng loạt (Broadcast - TSK-48)"
)
def broadcast_notification(
    payload: NotificationBroadcastRequest,
    db: Session = Depends(get_db)
):
    """
    API gửi thông báo hệ thống đến nhiều người dùng:
    - Nếu `user_ids` không truyền -> Gửi đến toàn bộ người dùng active.
    - Nếu truyền danh sách `user_ids` -> Gửi đến các người dùng chỉ định.
    """
    notifications = NotificationService.broadcast_notification(
        db=db,
        title=payload.title,
        content=payload.content,
        notification_type=payload.type,
        user_ids=payload.user_ids
    )
    return notifications


@router.post(
    "/trigger/review-reply",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Trigger: Gửi thông báo khi nhận phản hồi đánh giá (TSK-48 / Module 5)"
)
def trigger_review_reply_notification(
    payload: ReviewReplyNotificationRequest,
    db: Session = Depends(get_db)
):
    """
    Sự kiện tự động gửi thông báo khi một bài đánh giá của người dùng nhận được phản hồi.
    """
    return NotificationService.notify_review_reply(
        db=db,
        user_id=payload.user_id,
        restaurant_name=payload.restaurant_name,
        reviewer_name=payload.reviewer_name,
        reply_content=payload.reply_content
    )


@router.post(
    "/trigger/account-status",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Trigger: Gửi thông báo khi trạng thái tài khoản thay đổi (TSK-48 / PBI-17)"
)
def trigger_account_status_notification(
    payload: AccountStatusNotificationRequest,
    db: Session = Depends(get_db)
):
    """
    Sự kiện tự động gửi thông báo khi tài khoản bị khóa hoặc được mở khóa bởi Admin (BR-07).
    """
    return NotificationService.notify_account_status(
        db=db,
        user_id=payload.user_id,
        new_status=payload.new_status,
        reason=payload.reason
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Đánh dấu một thông báo đã đọc (is_read = true - TSK-48)"
)
def mark_notification_as_read(
    notification_id: int,
    user_id: int = Query(..., description="ID người dùng sở hữu thông báo"),
    db: Session = Depends(get_db)
):
    """
    API đánh dấu thông báo cụ thể là đã đọc:
    - Cập nhật `is_read = True`.
    - Kiểm tra bảo mật: từ chối nếu người dùng không phải chủ sở hữu (403 Forbidden).
    """
    return NotificationService.mark_as_read(
        db=db,
        notification_id=notification_id,
        user_id=user_id
    )


@router.put(
    "/read-all",
    response_model=MarkReadResponse,
    status_code=status.HTTP_200_OK,
    summary="Đánh dấu toàn bộ thông báo của người dùng đã đọc (TSK-48)"
)
def mark_all_notifications_as_read(
    user_id: int = Query(..., description="ID người dùng"),
    db: Session = Depends(get_db)
):
    """
    API Đánh dấu tất cả thông báo chưa đọc của người dùng là đã đọc (Mark All as Read).
    """
    updated_count = NotificationService.mark_all_as_read(db=db, user_id=user_id)
    return MarkReadResponse(
        success=True,
        message=f"Đã đánh dấu {updated_count} thông báo là đã đọc thành công.",
        updated_count=updated_count
    )


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa một thông báo (TSK-48)"
)
def delete_notification(
    notification_id: int,
    user_id: int = Query(..., description="ID người dùng sở hữu thông báo"),
    db: Session = Depends(get_db)
):
    """
    API xóa thông báo khỏi danh sách của người dùng:
    - Kiểm tra quyền sở hữu trước khi xóa.
    """
    NotificationService.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=user_id
    )
    return {
        "success": True,
        "message": f"Đã xóa thông báo ID {notification_id} thành công."
    }
