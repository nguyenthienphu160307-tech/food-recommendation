import math
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.restaurant import Restaurant
from app.schemas.restaurant import (
    RestaurantListResponse,
    RestaurantListItemResponse,
    PaginationMetadata,
    AmenityResponse,
)

router = APIRouter(prefix="/api/restaurants", tags=["Nhà hàng (Restaurants)"])


@router.get(
    "",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách nhà hàng cơ bản có phân trang (TSK-09)"
)
def get_restaurants(
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng nhà hàng trên mỗi trang"),
    status_filter: Optional[str] = Query("active", description="Trạng thái nhà hàng ('active', 'all')"),
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách nhà hàng cơ bản hỗ trợ phân trang (Task TSK-09 / PBI-10):
    1. Nhận tham số phân trang `page` và `limit`.
    2. Truy vấn kết hợp Eager Loading (joinedload) tối ưu hiệu năng không bị lỗi N+1 (< 3s).
    3. Tự động tìm và trả về đường dẫn ảnh bìa (`is_cover=True`) từ bảng `restaurant_images`.
    4. Trả kèm các cờ tiện ích chính từ bảng `restaurant_amenities`.
    5. Trả về metadata phân trang (total_items, total_pages, page, limit).
    """
    # 1. Khởi tạo truy vấn danh sách nhà hàng
    query = db.query(Restaurant)
    if status_filter and status_filter != "all":
        query = query.filter(Restaurant.status == status_filter)

    # 2. Đếm tổng số lượng nhà hàng
    total_items = query.count()

    # 3. Tính toán tổng số trang
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    # 4. Lấy dữ liệu theo phân trang kết hợp Eager Loading
    offset = (page - 1) * limit
    restaurants = (
        query.options(
            joinedload(Restaurant.amenities),
            joinedload(Restaurant.images)
        )
        .order_by(Restaurant.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # 5. Định dạng dữ liệu từng nhà hàng kèm ảnh bìa và tiện ích
    items_response: List[RestaurantListItemResponse] = []
    for r in restaurants:
        # Lấy ảnh bìa: ưu tiên ảnh có is_cover = True, nếu không có thì lấy ảnh đầu tiên
        cover_image_url = None
        if r.images:
            cover_img = next((img for img in r.images if img.is_cover), None)
            cover_image_url = cover_img.image_url if cover_img else r.images[0].image_url

        # Lấy thông tin tiện ích
        if r.amenities:
            amenities_data = AmenityResponse(
                has_parking=r.amenities.has_parking,
                has_private_room=r.amenities.has_private_room,
                has_outdoor=r.amenities.has_outdoor,
                pet_friendly=r.amenities.pet_friendly,
                vegetarian_support=r.amenities.vegetarian_support,
            )
        else:
            amenities_data = AmenityResponse()

        items_response.append(
            RestaurantListItemResponse(
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
            )
        )

    # 6. Trả về phản hồi danh sách kèm thông tin phân trang
    return RestaurantListResponse(
        data=items_response,
        pagination=PaginationMetadata(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=total_pages
        )
    )
