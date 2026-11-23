from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
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
# 4. BẢNG RESTAURANT REVIEWS & 6. NOTIFICATIONS (Re-exported from modules)
# =====================================================================
from app.models.review import RestaurantReview
from app.models.notification import Notification


# =====================================================================
# 5. BẢNG USER FAVORITES (Danh sách nhà hàng yêu thích / Bookmark - TE9C67D)
# =====================================================================
class UserFavorite(Base):
    """Bảng lưu danh sách quán ăn yêu thích của người dùng (UserFavorites - FR-11, UC-08)."""
    __tablename__ = "user_favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "restaurant_id", name="uq_favorite_user_restaurant"),
        Index("idx_favorite_user", "user_id"),
        Index("idx_favorite_restaurant", "restaurant_id"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="favorites")
    restaurant = relationship("Restaurant", back_populates="favorites")

