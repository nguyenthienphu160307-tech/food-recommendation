from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.review import RestaurantReview
from app.models.restaurant import Restaurant
from app.models.user import User, UserProfile
from app.schemas.review import ReviewResponse, ReviewUserSummary


class ReviewService:
    """
    Dịch vụ quản lý Đánh giá & Nhận xét Nhà hàng (Review Service - TSK-51 / PBI-13)
    - Quản lý tạo, sửa, xóa và truy vấn đánh giá (1-5 sao kèm bình luận).
    - Đảm bảo ràng buộc UNIQUE(restaurant_id, user_id) theo BR-06 (mỗi người 1 review/quán, cho phép sửa).
    - Tự động tính toán lại `avg_rating` và `total_reviews` trong bảng `Restaurants` sau mỗi thao tác.
    """

    @staticmethod
    def recalculate_restaurant_rating(db: Session, restaurant_id: int) -> Tuple[float, int]:
        """
        Tự động tính lại điểm đánh giá trung bình (avg_rating) và tổng số lượt đánh giá:
        - avg_rating = round(sum(ratings) / total_reviews, 1)
        - Nếu không còn đánh giá nào: avg_rating = 0.0, total_reviews = 0
        - Cập nhật trực tiếp vào bảng `Restaurants`
        """
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            return 0.0, 0

        ratings = db.query(RestaurantReview.rating).filter(
            RestaurantReview.restaurant_id == restaurant_id
        ).all()

        total = len(ratings)
        if total > 0:
            avg = round(sum(r[0] for r in ratings) / total, 1)
        else:
            avg = 0.0

        restaurant.avg_rating = avg
        restaurant.total_reviews = total
        db.commit()
        db.refresh(restaurant)

        return avg, total

    @staticmethod
    def create_review(
        db: Session,
        restaurant_id: int,
        user_id: int,
        rating: int,
        comment: Optional[str] = None
    ) -> RestaurantReview:
        """
        Tạo mới đánh giá cho nhà hàng (FR-10, BR-01, BR-06):
        - Kiểm tra nhà hàng và người dùng tồn tại.
        - Kiểm tra tài khoản không bị khóa (BR-07).
        - Kiểm tra điểm rating hợp lệ từ 1 đến 5 sao.
        - Kiểm tra ràng buộc BR-06: nếu người dùng đã đánh giá quán này rồi -> chặn với HTTP 409 Conflict.
        - Tự động kích hoạt tính lại avg_rating trên Restaurant.
        """
        # 1. Kiểm tra nhà hàng tồn tại
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhà hàng có ID {restaurant_id}."
            )

        # 2. Kiểm tra người dùng tồn tại và hợp lệ (BR-01, BR-07)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng có ID {user_id}."
            )
        if user.status == "locked":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản của bạn đang bị khóa, không thể gửi đánh giá."
            )

        # 3. Kiểm tra số sao hợp lệ (1 <= rating <= 5)
        if not (1 <= rating <= 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Điểm đánh giá phải là số nguyên từ 1 đến 5 sao."
            )

        # 4. Kiểm tra ràng buộc BR-06: 1 người dùng chỉ được đánh giá 1 lần / nhà hàng
        existing = db.query(RestaurantReview).filter(
            RestaurantReview.restaurant_id == restaurant_id,
            RestaurantReview.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bạn đã đánh giá nhà hàng này rồi (Quy tắc BR-06). Vui lòng sử dụng tính năng chỉnh sửa đánh giá (PUT)."
            )

        # 5. Lưu đánh giá mới vào bảng RestaurantReviews
        clean_comment = comment.strip() if comment else None
        new_review = RestaurantReview(
            restaurant_id=restaurant_id,
            user_id=user_id,
            rating=rating,
            comment=clean_comment,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        # 6. Tự động tính toán lại avg_rating và total_reviews trong bảng Restaurants
        ReviewService.recalculate_restaurant_rating(db, restaurant_id)

        return new_review

    @staticmethod
    def update_review(
        db: Session,
        review_id: int,
        user_id: int,
        rating: Optional[int] = None,
        comment: Optional[str] = None
    ) -> RestaurantReview:
        """
        Chỉnh sửa đánh giá cũ (PUT /api/reviews/{id} - BR-06 cho phép sửa):
        - Kiểm tra quyền sở hữu: chỉ chính chủ của review mới được sửa (403 Forbidden).
        - Kiểm tra rating hợp lệ nếu có truyền.
        - Cập nhật nội dung và tự động tính lại avg_rating.
        """
        review = db.query(RestaurantReview).filter(RestaurantReview.id == review_id).first()
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy bản ghi đánh giá có ID {review_id}."
            )

        # Phân quyền: Kiểm tra chính chủ
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền chỉnh sửa đánh giá của người dùng khác."
            )

        if rating is not None:
            if not (1 <= rating <= 5):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Điểm đánh giá phải từ 1 đến 5 sao."
                )
            review.rating = rating

        if comment is not None:
            review.comment = comment.strip() if comment.strip() else None

        review.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(review)

        # Tự động tính lại điểm trung bình của nhà hàng
        ReviewService.recalculate_restaurant_rating(db, review.restaurant_id)

        return review

    @staticmethod
    def delete_review(
        db: Session,
        review_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> Tuple[float, int]:
        """
        Xóa đánh giá khỏi CSDL:
        - Người dùng chỉ được xóa đánh giá của chính mình (hoặc Admin có quyền kiểm duyệt).
        - Tự động cập nhật lại avg_rating và total_reviews của nhà hàng sau khi xóa.
        """
        review = db.query(RestaurantReview).filter(RestaurantReview.id == review_id).first()
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy bản ghi đánh giá có ID {review_id}."
            )

        if not is_admin and review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xóa đánh giá của người dùng khác."
            )

        restaurant_id = review.restaurant_id
        db.delete(review)
        db.commit()

        # Tự động tính lại avg_rating và total_reviews
        avg, total = ReviewService.recalculate_restaurant_rating(db, restaurant_id)
        return avg, total

    @staticmethod
    def get_restaurant_reviews(
        db: Session,
        restaurant_id: int,
        page: int = 1,
        limit: int = 10,
        rating_filter: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Lấy danh sách đánh giá của nhà hàng kèm phân trang và thông tin người đánh giá:
        - Sắp xếp mới nhất trước (created_at DESC).
        - Kèm thông tin họ tên, avatar của người đánh giá.
        """
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhà hàng có ID {restaurant_id}."
            )

        base_query = db.query(RestaurantReview).filter(
            RestaurantReview.restaurant_id == restaurant_id
        )

        if rating_filter is not None and 1 <= rating_filter <= 5:
            base_query = base_query.filter(RestaurantReview.rating == rating_filter)

        total_matching = base_query.count()
        offset = (page - 1) * limit
        reviews = base_query.order_by(
            desc(RestaurantReview.created_at),
            desc(RestaurantReview.id)
        ).offset(offset).limit(limit).all()

        # Nạp thông tin user profiles để hiển thị đẹp mắt trên giao diện
        review_items: List[ReviewResponse] = []
        for r in reviews:
            user = db.query(User).filter(User.id == r.user_id).first()
            user_summary = None
            if user:
                profile = user.profile
                user_summary = ReviewUserSummary(
                    user_id=user.id,
                    full_name=profile.full_name if profile else (user.email.split("@")[0] if user.email else "Người dùng"),
                    avatar_url=profile.avatar_url if profile else None
                )

            review_items.append(ReviewResponse(
                id=r.id,
                restaurant_id=r.restaurant_id,
                user_id=r.user_id,
                rating=r.rating,
                comment=r.comment,
                created_at=r.created_at,
                updated_at=r.updated_at,
                user=user_summary
            ))

        return {
            "restaurant_id": restaurant.id,
            "restaurant_name": restaurant.name,
            "avg_rating": restaurant.avg_rating,
            "total_reviews": restaurant.total_reviews,
            "page": page,
            "limit": limit,
            "items": review_items
        }

    @staticmethod
    def get_user_review_for_restaurant(
        db: Session,
        restaurant_id: int,
        user_id: int
    ) -> Optional[RestaurantReview]:
        """
        Lấy đánh giá hiện có của một người dùng đối với một nhà hàng cụ thể (nếu có).
        """
        return db.query(RestaurantReview).filter(
            RestaurantReview.restaurant_id == restaurant_id,
            RestaurantReview.user_id == user_id
        ).first()
