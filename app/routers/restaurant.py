import math
from typing import Dict, List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.restaurant import Restaurant, RestaurantAmenity
from app.schemas.restaurant import (
    AmenityResponse,
    AppliedFilterCriteria,
    PaginationMetadata,
    RestaurantFilterItemResponse,
    RestaurantFilterResponse,
    RestaurantListItemResponse,
    RestaurantListResponse,
)
from app.services.geo_service import (
    calculate_bounding_box,
    calculate_haversine_distance,
)

router = APIRouter(prefix="/api/restaurants", tags=["Nhà hàng (Restaurants)"])

VALID_SORT_MODES = {"default", "distance", "rating", "price_asc", "price_desc"}


def _serialize_restaurant(
    r: Restaurant,
    distance_km: Optional[float] = None,
) -> RestaurantFilterItemResponse:
    """Chuyển đổi ORM Restaurant sang schema response kèm ảnh bìa và 5 tiện ích."""
    cover_image_url = None
    if r.images:
        cover_img = next((img for img in r.images if img.is_cover), None)
        cover_image_url = cover_img.image_url if cover_img else r.images[0].image_url

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

    return RestaurantFilterItemResponse(
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
        distance_km=distance_km,
    )


def _validate_filter_params(
    price_min: Optional[float],
    price_max: Optional[float],
    lat: Optional[float],
    lng: Optional[float],
    radius_km: Optional[float],
    sort_by: str,
) -> None:
    """Kiểm tra tính hợp lệ của bộ tham số lọc đa điều kiện."""
    if price_min is not None and price_max is not None and price_min > price_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khoảng giá không hợp lệ: price_min phải nhỏ hơn hoặc bằng price_max.",
        )

    if (lat is None) != (lng is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng cung cấp đầy đủ cả hai tọa độ lat và lng.",
        )

    if radius_km is not None and (lat is None or lng is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng cung cấp tọa độ lat và lng khi lọc theo bán kính radius_km.",
        )

    if sort_by not in VALID_SORT_MODES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Giá trị sort_by='{sort_by}' không hợp lệ. Cho phép: {', '.join(sorted(VALID_SORT_MODES))}.",
        )


def _query_filtered_restaurants(
    db: Session,
    keyword: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = None,
    min_rating: Optional[float] = None,
    has_parking: Optional[bool] = None,
    has_private_room: Optional[bool] = None,
    has_outdoor: Optional[bool] = None,
    pet_friendly: Optional[bool] = None,
    vegetarian_support: Optional[bool] = None,
    status_filter: Optional[str] = "active",
    sort_by: str = "default",
    page: int = 1,
    limit: int = 20,
) -> Tuple[List[RestaurantFilterItemResponse], PaginationMetadata]:
    """
    Thực thi truy vấn lọc nhà hàng đa điều kiện kết hợp (FR-07 / UC-04 / TE9C660):
    - Trạng thái, từ khóa, loại ẩm thực (hỗ trợ đa giá trị phân tách bởi dấu phẩy)
    - Khoảng giá giao nhau (price_min / price_max) tận dụng idx_restaurant_price_range
    - Điểm đánh giá tối thiểu (avg_rating >= min_rating)
    - 5 cờ tiện ích trong RestaurantAmenities qua SQL JOIN
    - Bounding Box SQL (idx_restaurant_coords) + tính chính xác khoảng cách Haversine trong radius_km
    - Sắp xếp & phân trang nhất quán
    """
    _validate_filter_params(price_min, price_max, lat, lng, radius_km, sort_by)

    query = db.query(Restaurant).options(
        joinedload(Restaurant.amenities),
        joinedload(Restaurant.images),
    )

    if status_filter and status_filter != "all":
        query = query.filter(Restaurant.status == status_filter)

    if keyword and keyword.strip():
        kw = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Restaurant.name.ilike(kw),
                Restaurant.address.ilike(kw),
                Restaurant.cuisine_type.ilike(kw),
                Restaurant.description.ilike(kw),
            )
        )

    if cuisine_type and cuisine_type.strip():
        cuisines = [c.strip() for c in cuisine_type.split(",") if c.strip()]
        if cuisines:
            query = query.filter(
                or_(*[Restaurant.cuisine_type.ilike(f"%{c}%") for c in cuisines])
            )

    # Lọc khoảng giá theo nguyên tắc giao nhau (tối ưu với idx_restaurant_price_range)
    if price_min is not None:
        query = query.filter(Restaurant.max_price >= price_min)
    if price_max is not None:
        query = query.filter(Restaurant.min_price <= price_max)

    if min_rating is not None:
        query = query.filter(Restaurant.avg_rating >= min_rating)

    # Lọc kết hợp đồng nhất theo 5 tiện ích trong RestaurantAmenities
    amenity_filters: Dict[str, Optional[bool]] = {
        "has_parking": has_parking,
        "has_private_room": has_private_room,
        "has_outdoor": has_outdoor,
        "pet_friendly": pet_friendly,
        "vegetarian_support": vegetarian_support,
    }
    active_amenity_pairs = [(k, v) for k, v in amenity_filters.items() if v is not None]
    if active_amenity_pairs:
        query = query.join(RestaurantAmenity, Restaurant.id == RestaurantAmenity.restaurant_id)
        for col_name, flag_value in active_amenity_pairs:
            query = query.filter(getattr(RestaurantAmenity, col_name) == flag_value)

    # Sơ lọc Bounding Box trong SQL trước khi tính Haversine chính xác
    has_coords = lat is not None and lng is not None
    if has_coords and radius_km is not None:
        bbox = calculate_bounding_box(lat, lng, radius_km)
        query = query.filter(
            Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
            Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
        )

    candidates = query.all()

    # Tính khoảng cách Haversine chính xác và lọc phần rìa góc Bounding Box
    matched: List[Tuple[Restaurant, Optional[float]]] = []
    for r in candidates:
        dist_km: Optional[float] = None
        if has_coords:
            dist_km = round(calculate_haversine_distance(lat, lng, r.latitude, r.longitude, unit="km"), 2)
            if radius_km is not None and dist_km > radius_km:
                continue
        matched.append((r, dist_km))

    # Sắp xếp kết quả
    if sort_by == "distance":
        matched.sort(key=lambda item: (item[1] if item[1] is not None else float("inf"), -(item[0].avg_rating or 0.0)))
    elif sort_by == "rating":
        matched.sort(key=lambda item: (-(item[0].avg_rating or 0.0), -(item[0].total_reviews or 0), item[0].id))
    elif sort_by == "price_asc":
        matched.sort(key=lambda item: (item[0].min_price or 0.0, item[0].max_price or 0.0))
    elif sort_by == "price_desc":
        matched.sort(key=lambda item: (-(item[0].max_price or 0.0), -(item[0].min_price or 0.0)))
    else:
        if has_coords:
            matched.sort(key=lambda item: (item[1] if item[1] is not None else float("inf"), -(item[0].avg_rating or 0.0)))
        else:
            matched.sort(key=lambda item: -item[0].id)

    total_items = len(matched)
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
    offset = (page - 1) * limit
    paged_items = matched[offset : offset + limit]

    serialized = [_serialize_restaurant(r, dist_km) for r, dist_km in paged_items]
    pagination = PaginationMetadata(
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )
    return serialized, pagination


@router.get(
    "/filter",
    response_model=RestaurantFilterResponse,
    status_code=status.HTTP_200_OK,
    summary="Lọc nhà hàng đa điều kiện kết hợp (FR-07, UC-04 - TE9C660)",
)
def filter_restaurants(
    keyword: Optional[str] = Query(None, description="Từ khóa tìm kiếm theo tên, địa chỉ, mô tả"),
    cuisine_type: Optional[str] = Query(None, description="Loại ẩm thực (VD: 'Món Việt' hoặc 'Món Việt,Món Chay')"),
    price_min: Optional[float] = Query(None, ge=0, description="Mức giá tối thiểu (VNĐ)"),
    price_max: Optional[float] = Query(None, ge=0, description="Mức giá tối đa (VNĐ)"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Vĩ độ người dùng"),
    lng: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Kinh độ người dùng"),
    radius_km: Optional[float] = Query(None, gt=0.0, le=100.0, description="Bán kính khoảng cách tối đa (km)"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Điểm đánh giá tối thiểu (0.0 - 5.0)"),
    has_parking: Optional[bool] = Query(None, description="Tiện ích 1: Có chỗ đậu ô tô"),
    has_private_room: Optional[bool] = Query(None, description="Tiện ích 2: Có phòng riêng"),
    has_outdoor: Optional[bool] = Query(None, description="Tiện ích 3: Có không gian ngoài trời"),
    pet_friendly: Optional[bool] = Query(None, description="Tiện ích 4: Thân thiện với thú cưng"),
    vegetarian_support: Optional[bool] = Query(None, description="Tiện ích 5: Có hỗ trợ món chay"),
    sort_by: str = Query("default", description="Sắp xếp: default, distance, rating, price_asc, price_desc"),
    status_filter: str = Query("active", description="Trạng thái nhà hàng ('active', 'all')"),
    page: int = Query(1, ge=1, description="Số thứ tự trang"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả mỗi trang"),
    db: Session = Depends(get_db),
):
    """
    API Lọc nhà hàng đa điều kiện kết hợp (FR-07 / UC-04 / Task TE9C660):
    - Kết hợp đồng thời `cuisine_type`, khoảng giá (`price_min`/`price_max`), bán kính khoảng cách (`lat`/`lng`/`radius_km`),
      điểm đánh giá tối thiểu (`min_rating`) và 5 tiện ích trong `RestaurantAmenities`.
    - Trả về danh sách nhà hàng khớp điều kiện kèm `distance_km`, `applied_filters` và `pagination`.
    """
    items, pagination = _query_filtered_restaurants(
        db=db,
        keyword=keyword,
        cuisine_type=cuisine_type,
        price_min=price_min,
        price_max=price_max,
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        min_rating=min_rating,
        has_parking=has_parking,
        has_private_room=has_private_room,
        has_outdoor=has_outdoor,
        pet_friendly=pet_friendly,
        vegetarian_support=vegetarian_support,
        status_filter=status_filter,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )

    return RestaurantFilterResponse(
        status="success",
        data=items,
        applied_filters=AppliedFilterCriteria(
            keyword=keyword,
            cuisine_type=cuisine_type,
            price_min=price_min,
            price_max=price_max,
            lat=lat,
            lng=lng,
            radius_km=radius_km,
            min_rating=min_rating,
            has_parking=has_parking,
            has_private_room=has_private_room,
            has_outdoor=has_outdoor,
            pet_friendly=pet_friendly,
            vegetarian_support=vegetarian_support,
            sort_by=sort_by,
            status_filter=status_filter,
        ),
        pagination=pagination,
    )


@router.get(
    "",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách nhà hàng có phân trang & hỗ trợ lọc đa điều kiện (TSK-09 / TE9C660)",
)
def get_restaurants(
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng nhà hàng trên mỗi trang"),
    status_filter: Optional[str] = Query("active", description="Trạng thái nhà hàng ('active', 'all')"),
    keyword: Optional[str] = Query(None, description="Từ khóa tìm kiếm"),
    cuisine_type: Optional[str] = Query(None, description="Loại ẩm thực"),
    price_min: Optional[float] = Query(None, ge=0, description="Mức giá tối thiểu"),
    price_max: Optional[float] = Query(None, ge=0, description="Mức giá tối đa"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Vĩ độ"),
    lng: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Kinh độ"),
    radius_km: Optional[float] = Query(None, gt=0.0, le=100.0, description="Bán kính (km)"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Đánh giá tối thiểu"),
    has_parking: Optional[bool] = Query(None, description="Có chỗ đậu ô tô"),
    has_private_room: Optional[bool] = Query(None, description="Có phòng riêng"),
    has_outdoor: Optional[bool] = Query(None, description="Có không gian ngoài trời"),
    pet_friendly: Optional[bool] = Query(None, description="Thân thiện với thú cưng"),
    vegetarian_support: Optional[bool] = Query(None, description="Có hỗ trợ món chay"),
    sort_by: str = Query("default", description="Kiểu sắp xếp"),
    db: Session = Depends(get_db),
):
    """
    API lấy danh sách nhà hàng hỗ trợ phân trang và lọc đa điều kiện (giữ tương thích ngược TSK-09).
    """
    items, pagination = _query_filtered_restaurants(
        db=db,
        keyword=keyword,
        cuisine_type=cuisine_type,
        price_min=price_min,
        price_max=price_max,
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        min_rating=min_rating,
        has_parking=has_parking,
        has_private_room=has_private_room,
        has_outdoor=has_outdoor,
        pet_friendly=pet_friendly,
        vegetarian_support=vegetarian_support,
        status_filter=status_filter,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )

    list_items: List[RestaurantListItemResponse] = [
        RestaurantListItemResponse(**item.model_dump(exclude={"distance_km"}))
        for item in items
    ]
    return RestaurantListResponse(
        data=list_items,
        pagination=pagination,
    )
