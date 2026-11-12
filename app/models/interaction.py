"""SQLAlchemy models for Restaurant & 6 interaction/search/notification tables (Task TE9C654)."""

from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Restaurant(Base):
    """Bảng thông tin Nhà hàng cơ bản để liên kết Khóa ngoại (Foreign Key)."""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    price_min = Column(Integer, nullable=True)
    price_max = Column(Integer, nullable=True)
    rating_avg = Column(Float, default=0.0, nullable=False)
    open_time = Column(String(20), nullable=True)
    close_time = Column(String(20), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviews = relationship("RestaurantReview", back_populates="restaurant", cascade="all, delete-orphan")
    favorited_by = relationship("UserFavorite", back_populates="restaurant", cascade="all, delete-orphan")


# =====================================================================
# 1. BẢNG SEARCH SESSIONS (Phiên tìm kiếm / hội thoại gợi ý món ăn AI)
# =====================================================================
class SearchSession(Base):
    """Bảng lưu phiên tìm kiếm của người dùng (SearchSessions)."""
    __tablename__ = "search_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_code = Column(String(64), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=True)
    user_lat = Column(Float, nullable=True)
    user_lng = Column(Float, nullable=True)
    status = Column(String(20), default="active", nullable=False)  # 'active', 'closed'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("SearchMessage", back_populates="session", cascade="all, delete-orphan")
    criteria = relationship("SearchCriteria", back_populates="session", uselist=False, cascade="all, delete-orphan")


# =====================================================================
# 2. BẢNG SEARCH MESSAGES (Lịch sử tin nhắn trong phiên tìm kiếm AI)
# =====================================================================
class SearchMessage(Base):
    """Bảng lưu tin nhắn hỏi đáp trong phiên tìm kiếm (SearchMessages)."""
    __tablename__ = "search_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("search_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_role = Column(String(20), nullable=False, default="user")  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("SearchSession", back_populates="messages")


# =====================================================================
# 3. BẢNG SEARCH CRITERIA (Tiêu chí ăn uống trích xuất từ phiên tìm kiếm)
# =====================================================================
class SearchCriteria(Base):
    """Bảng lưu tiêu chí lọc món ăn/nhà hàng trích xuất từ phiên chat (SearchCriteria)."""
    __tablename__ = "search_criteria"
    __table_args__ = (
        UniqueConstraint("session_id", name="uq_search_criteria_session"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("search_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    cuisine_type = Column(String(100), nullable=True)
    taste_preference = Column(String(255), nullable=True)
    price_min = Column(Integer, nullable=True)
    price_max = Column(Integer, nullable=True)
    radius_km = Column(Float, default=5.0, nullable=False)
    dietary_restrictions = Column(String(255), nullable=True)
    extracted_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("SearchSession", back_populates="criteria")


# =====================================================================
# 4. BẢNG RESTAURANT REVIEWS (Đánh giá & nhận xét nhà hàng)
# =====================================================================
class RestaurantReview(Base):
    """Bảng lưu đánh giá nhà hàng của người dùng (RestaurantReviews)."""
    __tablename__ = "restaurant_reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "restaurant_id", name="uq_review_user_restaurant"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # Điểm từ 1 đến 5 sao
    comment = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="reviews")


# =====================================================================
# 5. BẢNG USER FAVORITES (Danh sách nhà hàng yêu thích / Bookmark)
# =====================================================================
class UserFavorite(Base):
    """Bảng lưu danh sách quán ăn yêu thích của người dùng (UserFavorites)."""
    __tablename__ = "user_favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "restaurant_id", name="uq_favorite_user_restaurant"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    restaurant = relationship("Restaurant", back_populates="favorited_by")


# =====================================================================
# 6. BẢNG NOTIFICATIONS (Thông báo hệ thống cho người dùng)
# =====================================================================
class Notification(Base):
    """Bảng lưu thông báo gửi tới người dùng (Notifications)."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="system", nullable=False)  # 'system', 'review', 'promo'
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)