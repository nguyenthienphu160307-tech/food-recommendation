import math
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.models.interaction import UserFavorite
from app.schemas.restaurant import (
    RestaurantListItemResponse,
    AmenityResponse,
    PaginationMetadata,
)
from app.schemas.favorite import (
    FavoriteItemResponse,
    FavoriteListResponse,
    FavoriteActionResponse,
    FavoriteCheckResponse,
)
from app.services.open_hours_service import check_restaurant_open_status, get_vietnam_now
from app.services.recommendation_service import calculate_distance_km


class FavoriteService:
    """
    Tầng Service xử lý nghiệp vụ Quản lý Nhà hàng Yêu thích (Favorites - FR-11, UC-08 / Task TE9C67D):
    - Đảm bảo ràng buộc UNIQUE(user_id, restaurant_id) (chặn trùng lặp).
    - Kiểm tra người dùng đăng nhập và trạng thái tài khoản active (BR-01, BR-07).
    - Kiểm tra tính tồn tại của nhà hàng trong bảng Restaurants.
    - Hỗ trợ phân trang chuẩn RESTful và tính toán khoảng cách / giờ mở cửa khi lấy danh sách.
    """

    @staticmethod
    def _verify_user_and_status(db: Session, user_id: int) -> User:
        """Kiểm tra người dùng tồn tại và tài khoản không bị khóa (BR-01, BR-07)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng với ID={user_id}."
            )
        if user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản của bạn đã bị khóa theo chính sách hệ thống (BR-07). Vui lòng liên hệ Quản trị viên."
            )
        return user

    @staticmethod
    def add_favorite(
        db: Session,
        user_id: int,
        restaurant_id: int,
        note: Optional[str] = None
    ) -> UserFavorite:
        """
        Thêm nhà hàng vào danh sách yêu thích (POST /api/favorites - FR-11, UC-08):
        - Kiểm tra tài khoản người dùng (BR-01, BR-07).
        - Kiểm tra nhà hàng có tồn tại và đang hoạt động.
        - Ràng buộc UNIQUE(user_id, restaurant_id): Báo lỗi 409 Conflict nếu đã lưu trước đó.
        """
        # 1. Xác thực tài khoản người dùng
        FavoriteService._verify_user_and_status(db, user_id)

        # 2. Kiểm tra nhà hàng tồn tại
        restaurant = (
            db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id, Restaurant.status != "hidden")
            .first()
        )
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
            )

        # 3. Kiểm tra ràng buộc duy nhất UNIQUE(user_id, restaurant_id)
        existing = (
            db.query(UserFavorite)
            .filter(
                UserFavorite.user_id == user_id,
                UserFavorite.restaurant_id == restaurant_id
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nhà hàng này đã có trong danh sách yêu thích của bạn."
            )

        # 4. Tạo bản ghi UserFavorite mới
        favorite = UserFavorite(
            user_id=user_id,
            restaurant_id=restaurant_id,
            note=note.strip() if note else None,
            created_at=datetime.utcnow()
        )
        db.add(favorite)
        try:
            db.commit()
            db.refresh(favorite)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nhà hàng này đã có trong danh sách yêu thích của bạn."
            )

        return favorite

    @staticmethod
    def remove_favorite(
        db: Session,
        user_id: int,
        restaurant_id: int
    ) -> bool:
        """
        Xóa nhà hàng khỏi danh sách yêu thích (DELETE /api/favorites - FR-11, UC-08):
        - Bắt buộc tài khoản người dùng hợp lệ.
        - Tìm và xóa bản ghi UserFavorite tương ứng.
        - Báo lỗi 404 Not Found nếu quán chưa từng được lưu trong danh sách yêu thích.
        """
        FavoriteService._verify_user_and_status(db, user_id)

        favorite = (
            db.query(UserFavorite)
            .filter(
                UserFavorite.user_id == user_id,
                UserFavorite.restaurant_id == restaurant_id
            )
            .first()
        )
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nhà hàng ID={restaurant_id} không có trong danh sách yêu thích của bạn."
            )

        db.delete(favorite)
        db.commit()
        return True

    @staticmethod
    def get_user_favorites(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "newest",
        lat: Optional[float] = None,
        lng: Optional[float] = None
    ) -> FavoriteListResponse:
        """
        Lấy danh sách nhà hàng yêu thích của người dùng (GET /api/favorites - FR-11, UC-08):
        - Hỗ trợ phân trang RESTful (page, limit, total, total_pages).
        - Eager Loading (joinedload) chống lỗi N+1 truy vấn khi lấy thông tin nhà hàng, ảnh bìa, tiện ích.
        - Tính toán trạng thái giờ mở cửa theo thời gian thực (BR-03) và khoảng cách GPS nếu có tọa độ.
        - Hỗ trợ sắp xếp: 'newest' (mới lưu nhất), 'rating' (đánh giá cao nhất), 'price_asc', 'price_desc', 'distance'.
        """
        FavoriteService._verify_user_and_status(db, user_id)

        # Xử lý tham số an toàn khi gọi trực tiếp trong Unit Test
        if hasattr(page, "default"):
            page = page.default
        if hasattr(limit, "default"):
            limit = limit.default
        if hasattr(sort_by, "default"):
            sort_by = sort_by.default
        if hasattr(lat, "default"):
            lat = lat.default
        if hasattr(lng, "default"):
            lng = lng.default

        page = max(1, page or 1)
        limit = max(1, min(100, limit or 10))
        sort_by = sort_by or "newest"

        # Khởi tạo truy vấn kết hợp Eager Loading
        query = (
            db.query(UserFavorite)
            .join(Restaurant, UserFavorite.restaurant_id == Restaurant.id)
            .options(
                joinedload(UserFavorite.restaurant).joinedload(Restaurant.amenities),
                joinedload(UserFavorite.restaurant).joinedload(Restaurant.images)
            )
            .filter(UserFavorite.user_id == user_id)
            .filter(Restaurant.status != "hidden")
        )

        # Sắp xếp CSDL
        if sort_by == "rating":
            query = query.order_by(Restaurant.avg_rating.desc(), UserFavorite.id.desc())
        elif sort_by == "price_asc":
            query = query.order_by(Restaurant.min_price.asc(), UserFavorite.id.desc())
        elif sort_by == "price_desc":
            query = query.order_by(Restaurant.max_price.desc(), UserFavorite.id.desc())
        else:  # 'newest' hoặc mặc định
            query = query.order_by(UserFavorite.id.desc())

        total_items = query.count()
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
        offset = (page - 1) * limit
        rows = query.offset(offset).limit(limit).all()

        now_vn = get_vietnam_now()
        items: List[FavoriteItemResponse] = []

        for fav in rows:
            r = fav.restaurant
            # 1. Ảnh bìa
            cover_image_url = None
            if r.images:
                c_img = next((img for img in r.images if img.is_cover), None)
                cover_image_url = c_img.image_url if c_img else r.images[0].image_url

            # 2. Tiện ích
            amenities_data = AmenityResponse(
                has_parking=r.amenities.has_parking if r.amenities else False,
                has_private_room=r.amenities.has_private_room if r.amenities else False,
                has_outdoor=r.amenities.has_outdoor if r.amenities else False,
                pet_friendly=r.amenities.pet_friendly if r.amenities else False,
                vegetarian_support=r.amenities.vegetarian_support if r.amenities else False,
            )

            # 3. Trạng thái mở cửa BR-03
            open_info = check_restaurant_open_status(r.open_hours, check_dt=now_vn)

            # 4. Khoảng cách GPS nếu có tọa độ
            dist_km = None
            if lat is not None and lng is not None and r.latitude is not None and r.longitude is not None:
                dist_km = calculate_distance_km(float(lat), float(lng), float(r.latitude), float(r.longitude))

            rest_dto = RestaurantListItemResponse(
                id=r.id,
                name=r.name,
                description=r.description,
                address=r.address,
                phone_number=r.phone_number,
                cuisine_type=r.cuisine_type,
                latitude=r.latitude,
                longitude=r.longitude,
                min_price=r.min_price,
                max_price=r.max_price,
                open_hours=r.open_hours,
                avg_rating=r.avg_rating,
                total_reviews=r.total_reviews,
                status=r.status,
                cover_image_url=cover_image_url,
                amenities=amenities_data,
                is_open=open_info["is_open"],
                open_status_label=open_info["status_label"],
                open_status_detail=open_info["detail_text"],
                ranking_bonus=open_info["bonus_score"],
            )

            items.append(
                FavoriteItemResponse(
                    favorite_id=fav.id,
                    restaurant_id=fav.restaurant_id,
                    user_id=fav.user_id,
                    note=fav.note,
                    created_at=fav.created_at,
                    restaurant=rest_dto,
                )
            )

        # Nếu người dùng muốn sắp xếp theo khoảng cách
        if sort_by == "distance" and lat is not None and lng is not None:
            items.sort(key=lambda x: calculate_distance_km(float(lat), float(lng), x.restaurant.latitude, x.restaurant.longitude))

        return FavoriteListResponse(
            status="success",
            task_code="TE9C67D",
            total=total_items,
            data=items,
            pagination=PaginationMetadata(
                page=page,
                limit=limit,
                total_items=total_items,
                total_pages=total_pages
            )
        )

    @staticmethod
    def check_favorite_status(
        db: Session,
        user_id: int,
        restaurant_id: int
    ) -> FavoriteCheckResponse:
        """Kiểm tra một nhà hàng cụ thể đã được người dùng lưu yêu thích hay chưa"""
        FavoriteService._verify_user_and_status(db, user_id)

        fav = (
            db.query(UserFavorite)
            .filter(
                UserFavorite.user_id == user_id,
                UserFavorite.restaurant_id == restaurant_id
            )
            .first()
        )
        return FavoriteCheckResponse(
            restaurant_id=restaurant_id,
            is_favorite=fav is not None,
            favorite_id=fav.id if fav else None,
            note=fav.note if fav else None,
            created_at=fav.created_at if fav else None
        )
