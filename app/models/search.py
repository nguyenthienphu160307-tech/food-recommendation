from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
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

    # Quan hệ 1 - N với SearchCriteria (lưu các tiêu chí trích xuất từ câu chat, sắp xếp mới nhất lên đầu)
    criteria = relationship(
        "SearchCriteria",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="SearchCriteria.created_at.desc()"
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


class SearchCriteria(Base):
    """
    Bảng lưu trữ tiêu chí tìm kiếm trích xuất từ câu chat AI (SearchCriteria - TSK-18):
    - criteria_id: Khóa chính
    - session_id: Khóa ngoại liên kết phiên chat cha
    - location_text: Tên địa danh/khu vực gốc được người dùng nhập (VD: 'Bình Thạnh', 'Quận 1')
    - latitude, longitude: Tọa độ tâm địa lý sau khi qua Geocoding Service
    - cuisine: Loại ẩm thực bóc tách được (lẩu, nướng, cơm, chay,...)
    - budget: Ngân sách tối đa (VND)
    - has_parking: Yêu cầu chỗ đậu ô tô / xe máy
    - other_conditions: Các điều kiện mở rộng (phòng riêng, ngoài trời, thú cưng...) dạng JSON
    """
    __tablename__ = "search_criteria"

    criteria_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("search_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    location_text = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    cuisine = Column(String(100), nullable=True)
    budget = Column(Integer, nullable=True)
    has_parking = Column(Boolean, nullable=True, default=False)
    other_conditions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Quan hệ N - 1 với SearchSessions
    session = relationship("SearchSession", back_populates="criteria")
