from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class Notification(Base):
    """
    Bảng lưu trữ Thông báo người dùng (Notifications - TSK-48 / PBI-17)
    - Lưu các thông báo hệ thống, phản hồi đánh giá, hoặc thay đổi trạng thái tài khoản.
    - Cung cấp cờ `is_read` để đánh dấu trạng thái đã đọc và đếm thông báo chưa đọc.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(50), default="system", nullable=False)  # 'system', 'review_reply', 'account_status', 'review_moderation'
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Quan hệ N - 1 với bảng Users
    user = relationship("User", back_populates="notifications")

    # Composite Index tối ưu hóa truy vấn lọc thông báo chưa đọc theo người dùng
    __table_args__ = (
        Index("idx_notifications_user_read", "user_id", "is_read"),
    )
