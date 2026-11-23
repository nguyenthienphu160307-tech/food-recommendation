from datetime import datetime
from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class RestaurantReview(Base):
    """
    Bảng lưu trữ Đánh giá & Nhận xét của người dùng cho Nhà hàng (RestaurantReviews - TSK-51 / PBI-13)
    - Ràng buộc BR-06: Mỗi người dùng chỉ được đánh giá duy nhất 1 lần trên mỗi nhà hàng UNIQUE(restaurant_id, user_id)
    - Thang điểm 1 - 5 sao (CheckConstraint)
    - Tự động liên kết để tính toán lại điểm trung bình `avg_rating` trong bảng `Restaurants`
    """
    __tablename__ = "restaurant_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1 đến 5 sao
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Các mối quan hệ (Relationships)
    restaurant = relationship("Restaurant", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    # Các ràng buộc nghiệp vụ (Constraints & Indexes - BR-06)
    __table_args__ = (
        UniqueConstraint("restaurant_id", "user_id", name="uq_restaurant_user_review"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
        Index("idx_review_restaurant", "restaurant_id"),
        Index("idx_review_user", "user_id"),
    )
