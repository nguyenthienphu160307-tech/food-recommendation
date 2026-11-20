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
from app.models.restaurant import Restaurant


class GeoRestaurant(Base):
    """Bảng lưu trữ thông tin Nhà hàng & Tọa độ địa lý cho module Geo"""
    __tablename__ = "geo_restaurants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    category = Column(String(100), nullable=True, default="Món Việt")
    price_min = Column(Integer, nullable=True, default=50000)
    price_max = Column(Integer, nullable=True, default=200000)
    rating_avg = Column(Float, nullable=True, default=4.5)
    open_time = Column(String(20), nullable=True, default="08:00")
    close_time = Column(String(20), nullable=True, default="22:00")
    image_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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
