from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.notification import Notification
from app.models.user import User


class NotificationService:
    """
    Dịch vụ quản lý Thông báo người dùng (Notifications Service - TSK-48 / PBI-17)
    - Tạo và lưu trữ thông báo vào bảng `Notifications`.
    - Hỗ trợ các loại thông báo: phản hồi đánh giá (`review_reply`), trạng thái tài khoản (`account_status`), hệ thống (`system`).
    - API đánh dấu đã đọc (`is_read`), đếm số lượng chưa đọc, phân trang danh sách.
    """

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        content: str,
        notification_type: str = "system"
    ) -> Notification:
        """
        Tạo thông báo mới cho người dùng cụ thể:
        - Kiểm tra người dùng có tồn tại hay không.
        - Mặc định `is_read = False`.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng có ID {user_id}."
            )

        notification = Notification(
            user_id=user_id,
            title=title.strip(),
            content=content.strip(),
            type=notification_type,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def broadcast_notification(
        db: Session,
        title: str,
        content: str,
        notification_type: str = "system",
        user_ids: Optional[List[int]] = None
    ) -> List[Notification]:
        """
        Gửi thông báo hàng loạt (Broadcast):
        - Nếu truyền `user_ids`: Gửi đến các người dùng trong danh sách.
        - Nếu không truyền: Gửi đến toàn bộ người dùng có trạng thái 'active'.
        """
        query = db.query(User)
        if user_ids is not None and len(user_ids) > 0:
            users = query.filter(User.id.in_(user_ids)).all()
        else:
            users = query.filter(User.status == "active").all()

        if not users:
            return []

        notifications = [
            Notification(
                user_id=u.id,
                title=title.strip(),
                content=content.strip(),
                type=notification_type,
                is_read=False,
                created_at=datetime.utcnow()
            )
            for u in users
        ]
        db.add_all(notifications)
        db.commit()
        for n in notifications:
            db.refresh(n)
        return notifications

    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 20,
        unread_only: bool = False
    ) -> Dict[str, Any]:
        """
        Lấy danh sách thông báo của người dùng kèm phân trang:
        - Sắp xếp mới nhất trước (created_at DESC, id DESC).
        - Đếm tổng số thông báo và tổng số chưa đọc để hiển thị badge.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng có ID {user_id}."
            )

        base_query = db.query(Notification).filter(Notification.user_id == user_id)
        
        # Đếm số lượng chưa đọc của user
        unread_count = base_query.filter(Notification.is_read == False).count()

        # Áp dụng bộ lọc unread_only nếu được yêu cầu
        filtered_query = base_query
        if unread_only:
            filtered_query = filtered_query.filter(Notification.is_read == False)

        total = filtered_query.count()
        offset = (page - 1) * limit
        items = filtered_query.order_by(
            desc(Notification.created_at),
            desc(Notification.id)
        ).offset(offset).limit(limit).all()

        return {
            "total": total,
            "unread_count": unread_count,
            "page": page,
            "limit": limit,
            "items": items
        }

    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """
        Lấy số lượng thông báo chưa đọc của người dùng để hiển thị badge chuông thông báo.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng có ID {user_id}."
            )

        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> Notification:
        """
        Đánh dấu một thông báo cụ thể là đã đọc:
        - Xác minh quyền sở hữu: chỉ chủ nhân của thông báo mới được đánh dấu.
        """
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy thông báo có ID {notification_id}."
            )

        if notification.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thao tác trên thông báo của người dùng khác."
            )

        if not notification.is_read:
            notification.is_read = True
            db.commit()
            db.refresh(notification)

        return notification

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        """
        Đánh dấu tất cả thông báo của người dùng là đã đọc (Mark all as read):
        - Trả về số lượng bản ghi đã được cập nhật.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng có ID {user_id}."
            )

        updated_count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True}, synchronize_session=False)

        db.commit()
        return updated_count

    @staticmethod
    def delete_notification(db: Session, notification_id: int, user_id: int) -> bool:
        """
        Xóa một thông báo khỏi CSDL:
        - Xác minh quyền sở hữu trước khi xóa.
        """
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy thông báo có ID {notification_id}."
            )

        if notification.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xóa thông báo của người dùng khác."
            )

        db.delete(notification)
        db.commit()
        return True

    @staticmethod
    def notify_review_reply(
        db: Session,
        user_id: int,
        restaurant_name: str,
        reviewer_name: str,
        reply_content: str
    ) -> Notification:
        """
        Tạo thông báo tự động khi người dùng nhận được phản hồi đánh giá (review_reply).
        """
        title = f"Phản hồi mới về đánh giá tại {restaurant_name}"
        content = f"Chủ quán / quản trị viên {reviewer_name} đã phản hồi đánh giá của bạn: \"{reply_content}\""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            content=content,
            notification_type="review_reply"
        )

    @staticmethod
    def notify_account_status(
        db: Session,
        user_id: int,
        new_status: str,
        reason: Optional[str] = None
    ) -> Notification:
        """
        Tạo thông báo tự động khi trạng thái tài khoản thay đổi (account_status).
        """
        if new_status == "locked":
            title = "Cảnh báo: Tài khoản của bạn đã bị khóa tạm thời"
            reason_text = f" Lý do: {reason}." if reason else ""
            content = f"Tài khoản của bạn đã bị khóa bởi Quản trị viên.{reason_text} Vui lòng liên hệ ban quản trị để được hỗ trợ mở khóa."
        else:
            title = "Thông báo: Tài khoản của bạn đã được kích hoạt lại"
            reason_text = f" Ghi chú: {reason}." if reason else ""
            content = f"Tài khoản của bạn đã hoạt động bình thường.{reason_text} Chúc bạn có trải nghiệm tuyệt vời cùng Smart Dining!"

        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            content=content,
            notification_type="account_status"
        )
