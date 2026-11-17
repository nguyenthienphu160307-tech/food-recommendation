import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.restaurant import Restaurant
from app.schemas.restaurant import (
    RestaurantListResponse,
    RestaurantListItemResponse,
    RestaurantOpenStatusResponse,
    PaginationMetadata,
    AmenityResponse,
)
from app.services.open_hours_service import (
    check_restaurant_open_status,
    get_vietnam_now,
    DEFAULT_OPEN_BONUS_WEIGHT,
)
from app.services.recommendation_service import (
    calculate_distance_km,
    calculate_match_score,
    generate_match_reasons,
    generate_recommendation_summary,
    DEFAULT_USER_LAT,
    DEFAULT_USER_LON,
)

router = APIRouter(prefix="/api/restaurants", tags=["Nhà hàng (Restaurants)"])


@router.get(
    "",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách nhà hàng có phân trang, giờ mở cửa & độ phù hợp Match Score (TSK-09 / TSK-37 / TSK-40 / BR-03 / BR-05)"
)
def get_restaurants(
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng nhà hàng trên mỗi trang"),
    status_filter: Optional[str] = Query("active", description="Trạng thái nhà hàng ('active', 'all')"),
    open_now: Optional[bool] = Query(None, description="Lọc chỉ các nhà hàng đang mở cửa tại thời điểm hiện tại (BR-03)"),
    sort_by_open: Optional[bool] = Query(False, description="Ưu tiên xếp nhà hàng đang mở cửa lên trước (BR-03 Ranking Bonus)"),
    user_lat: Optional[float] = Query(None, description="Vĩ độ GPS của người dùng để tính khoảng cách và độ phù hợp (TSK-40)"),
    user_lon: Optional[float] = Query(None, description="Kinh độ GPS của người dùng để tính khoảng cách và độ phù hợp (TSK-40)"),
    sort_by_match: Optional[bool] = Query(False, description="Ưu tiên sắp xếp theo % Match Score giảm dần (PBI-11 / BR-05)"),
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách nhà hàng cơ bản hỗ trợ phân trang & xếp hạng gợi ý (Task TSK-09, TSK-37 & TSK-40):
    1. Nhận tham số phân trang `page` và `limit`.
    2. Truy vấn kết hợp Eager Loading (joinedload) tối ưu hiệu năng không bị lỗi N+1 (< 3s).
    3. Tự động tìm và trả về đường dẫn ảnh bìa (`is_cover=True`) từ bảng `restaurant_images`.
    4. Trả kèm các cờ tiện ích chính từ bảng `restaurant_amenities`.
    5. Phân tích giờ mở cửa hoạt động thực tế `open_hours` theo múi giờ Việt Nam (BR-03).
    6. Tính toán % Match Score (65% - 99%) & sinh tag trực quan các lý do đề xuất (TSK-40 / BR-05).
    7. Hỗ trợ lọc quán đang mở (`open_now=true`), ưu tiên mở cửa (`sort_by_open=true`), và ưu tiên khớp cao (`sort_by_match=true`).
    """
    now_vn = get_vietnam_now()

    # Xử lý tương thích khi hàm được gọi trực tiếp trong Unit Test
    if hasattr(status_filter, "default"):
        status_filter = status_filter.default
    if hasattr(open_now, "default"):
        open_now = open_now.default
    if hasattr(sort_by_open, "default"):
        sort_by_open = sort_by_open.default
    if hasattr(user_lat, "default"):
        user_lat = user_lat.default
    if hasattr(user_lon, "default"):
        user_lon = user_lon.default
    if hasattr(sort_by_match, "default"):
        sort_by_match = sort_by_match.default

    # Tọa độ tính toán (sử dụng tọa độ người dùng truyền lên hoặc tọa độ trung tâm mặc định)
    effective_lat = user_lat if user_lat is not None else DEFAULT_USER_LAT
    effective_lon = user_lon if user_lon is not None else DEFAULT_USER_LON

    # 1. Khởi tạo truy vấn danh sách nhà hàng
    query = db.query(Restaurant)
    if status_filter and status_filter != "all":
        query = query.filter(Restaurant.status == status_filter)

    # 2. Lấy dữ liệu kết hợp Eager Loading
    all_restaurants = (
        query.options(
            joinedload(Restaurant.amenities),
            joinedload(Restaurant.images)
        )
        .order_by(Restaurant.id.desc())
        .all()
    )

    # 3. Định dạng dữ liệu từng nhà hàng kèm ảnh bìa, tiện ích, giờ mở cửa & độ phù hợp Match Score
    items_response: List[RestaurantListItemResponse] = []
    for r in all_restaurants:
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

        # Kiểm tra trạng thái giờ mở cửa thực tế (BR-03 / TSK-37)
        open_info = check_restaurant_open_status(r.open_hours, check_dt=now_vn)

        # Tính khoảng cách GPS (Haversine)
        dist_km = None
        if r.latitude is not None and r.longitude is not None:
            dist_km = calculate_distance_km(
                effective_lat, effective_lon, float(r.latitude), float(r.longitude)
            )

        # Tính % Match Score (TSK-40 / BR-05)
        match_score = calculate_match_score(
            distance_km=dist_km if dist_km is not None else 3.0,
            avg_rating=r.avg_rating or 4.0,
            amenities=r.amenities,
            is_open=open_info["is_open"],
        )

        # Sinh danh sách các tag lý do đề xuất trực quan (TSK-40)
        match_reasons = generate_match_reasons(
            restaurant=r,
            user_lat=effective_lat,
            user_lon=effective_lon,
            check_dt=now_vn,
            is_open=open_info["is_open"],
        )

        # Sinh câu tóm tắt một dòng
        summary = generate_recommendation_summary(match_score, match_reasons)

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
                is_open=open_info["is_open"],
                open_status_label=open_info["status_label"],
                open_status_detail=open_info["detail_text"],
                ranking_bonus=open_info["bonus_score"],
                match_score=match_score,
                match_reasons=match_reasons,
                recommendation_summary=summary,
                distance_km=dist_km,
            )
        )

    # 4. Lọc theo trạng thái đang mở cửa nếu người dùng yêu cầu (BR-03)
    if open_now is True:
        items_response = [it for it in items_response if it.is_open]
    elif open_now is False:
        items_response = [it for it in items_response if not it.is_open]

    # 5. Sắp xếp ưu tiên:
    # 5.1 Ưu tiên theo % Match Score (PBI-11 / BR-05) nếu bật sort_by_match
    if sort_by_match:
        items_response.sort(key=lambda x: (x.match_score, x.avg_rating), reverse=True)
    # 5.2 Hoặc ưu tiên nhà hàng đang mở cửa lên trước (BR-03 Ranking Bonus)
    elif sort_by_open:
        items_response.sort(key=lambda x: (x.ranking_bonus, x.avg_rating), reverse=True)

    # 6. Thực hiện phân trang trên tập kết quả
    total_items = len(items_response)
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
    offset = (page - 1) * limit
    paged_items = items_response[offset : offset + limit]

    # 7. Trả về phản hồi danh sách kèm thông tin phân trang
    return RestaurantListResponse(
        data=paged_items,
        pagination=PaginationMetadata(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=total_pages
        )
    )


@router.get(
    "/{restaurant_id}/open-status",
    response_model=RestaurantOpenStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Kiểm tra chi tiết trạng thái giờ mở cửa theo thời gian thực (BR-03 / TSK-37)"
)
def get_restaurant_open_status(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    API kiểm tra chi tiết trạng thái đóng/mở cửa của một nhà hàng cụ thể theo thời gian thực:
    - Múi giờ chuẩn: Việt Nam (UTC+7).
    - Phân tích chuỗi `open_hours` (ca thường, ca gãy, qua đêm, 24/7).
    - Trả về nhãn trạng thái và điểm thưởng ưu tiên xếp hạng (BR-03).
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    now_vn = get_vietnam_now()
    open_info = check_restaurant_open_status(restaurant.open_hours, check_dt=now_vn)

    return RestaurantOpenStatusResponse(
        restaurant_id=restaurant.id,
        restaurant_name=restaurant.name,
        open_hours_raw=restaurant.open_hours,
        is_open=open_info["is_open"],
        status_code=open_info["status_code"],
        status_label=open_info["status_label"],
        detail_text=open_info["detail_text"],
        badge_color=open_info["badge_color"],
        bonus_score=open_info["bonus_score"],
        checked_at=now_vn.isoformat()
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantListItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin chi tiết một nhà hàng kèm giờ mở cửa & độ phù hợp (TSK-25 / TSK-37 / TSK-40)"
)
def get_restaurant_detail(
    restaurant_id: int,
    user_lat: Optional[float] = Query(None, description="Vĩ độ GPS của người dùng"),
    user_lon: Optional[float] = Query(None, description="Kinh độ GPS của người dùng"),
    db: Session = Depends(get_db)
):
    """API lấy thông tin chi tiết của một nhà hàng kèm trạng thái mở cửa thực tế & lý do đề xuất"""
    # Xử lý tương thích khi gọi trực tiếp
    if hasattr(user_lat, "default"):
        user_lat = user_lat.default
    if hasattr(user_lon, "default"):
        user_lon = user_lon.default

    effective_lat = user_lat if user_lat is not None else DEFAULT_USER_LAT
    effective_lon = user_lon if user_lon is not None else DEFAULT_USER_LON

    r = (
        db.query(Restaurant)
        .options(
            joinedload(Restaurant.amenities),
            joinedload(Restaurant.images)
        )
        .filter(Restaurant.id == restaurant_id)
        .first()
    )
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    cover_image_url = None
    if r.images:
        cover_img = next((img for img in r.images if img.is_cover), None)
        cover_image_url = cover_img.image_url if cover_img else r.images[0].image_url

    amenities_data = AmenityResponse(
        has_parking=r.amenities.has_parking if r.amenities else False,
        has_private_room=r.amenities.has_private_room if r.amenities else False,
        has_outdoor=r.amenities.has_outdoor if r.amenities else False,
        pet_friendly=r.amenities.pet_friendly if r.amenities else False,
        vegetarian_support=r.amenities.vegetarian_support if r.amenities else False,
    )

    now_vn = get_vietnam_now()
    open_info = check_restaurant_open_status(r.open_hours, check_dt=now_vn)

    dist_km = None
    if r.latitude is not None and r.longitude is not None:
        dist_km = calculate_distance_km(
            effective_lat, effective_lon, float(r.latitude), float(r.longitude)
        )

    match_score = calculate_match_score(
        distance_km=dist_km if dist_km is not None else 3.0,
        avg_rating=r.avg_rating or 4.0,
        amenities=r.amenities,
        is_open=open_info["is_open"],
    )

    match_reasons = generate_match_reasons(
        restaurant=r,
        user_lat=effective_lat,
        user_lon=effective_lon,
        check_dt=now_vn,
        is_open=open_info["is_open"],
    )

    summary = generate_recommendation_summary(match_score, match_reasons)

    return RestaurantListItemResponse(
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
        match_score=match_score,
        match_reasons=match_reasons,
        recommendation_summary=summary,
        distance_km=dist_km,
    )
