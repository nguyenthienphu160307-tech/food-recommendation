from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class SearchSession(Base):
    """
    Bảng quản lý phiên tìm kiếm / Chat AI (SearchSessions):
    - Quản lý vòng đời hội thoại (status: 'active', 'closed').
    - Hỗ trợ cả Người dùng đã đăng nhập (user_id = id) và Khách vãng lai (user_id = NULL) theo quy tắc BR-02.
    """
    __tablename__ = "search_sessions"

    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    status = Column(String(20), default="active", nullable=False)  # 'active', 'closed'
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Quan hệ với bảng Users (1 User có nhiều phiên tìm kiếm)
    user = relationship("User", back_populates="search_sessions")

    # Quan hệ 1 - N với SearchMessages (1 phiên có nhiều tin nhắn, tự động xóa cascade và xếp tăng dần theo thời gian)
    messages = relationship(
        "SearchMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="SearchMessage.created_at.asc()"
    )


class SearchMessage(Base):
    """
    Bảng lưu trữ lịch sử tin nhắn trong phiên tìm kiếm AI (SearchMessages):
    - Lưu trữ theo thời gian thực (created_at).
    - Phân biệt người gửi: sender_type = 'user' (người dùng) hoặc 'ai' (trợ lý ảo).
    """
    __tablename__ = "search_messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("search_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    sender_type = Column(String(10), nullable=False)  # 'user', 'ai'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Quan hệ N - 1 với SearchSessions
    session = relationship("SearchSession", back_populates="messages")
