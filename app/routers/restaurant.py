"""
Router quản lý Nhà hàng, Bộ lọc đa điều kiện kết hợp (TSK-23 / FR-07 / UC-04),
Chi tiết Nhà hàng kèm Thực đơn & Hình ảnh (TSK-25 / FR-09) và Quản lý Tiện ích (TSK-26).
"""

import math
from typing import Dict, List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantMenu
from app.schemas.restaurant import (
    AmenityResponse,
    AppliedFilterCriteria,
    MenuCategoryResponse,
    PaginationMetadata,
    RestaurantDetailResponse,
    RestaurantFilterItemResponse,
    RestaurantFilterResponse,
    RestaurantImageResponse,
    RestaurantListItemResponse,
    RestaurantListResponse,
)
from app.services.geo_service import (
    calculate_bounding_box,
    calculate_haversine_distance,
    format_distance_display,
)

router = APIRouter(prefix="/api/restaurants", tags=["Nhà hàng & Bộ lọc đa điều kiện (Restaurants)"])


class AmenityUpdateRequest(BaseModel):
    """Schema cập nhật 5 tiện ích nhà hàng dành cho Admin (TSK-26)."""
    has_parking: bool = Field(False, description="Có bãi đỗ ô tô / xe máy")
    has_private_room: bool = Field(False, description="Có phòng riêng yên tĩnh")
    has_outdoor: bool = Field(False, description="Có không gian ngoài trời / sân vườn")
    pet_friendly: bool = Field(False, description="Thân thiện với thú cưng")
    vegetarian_support: bool = Field(False, description="Có phục vụ món chay")


def _build_list_item(r: Restaurant) -> RestaurantListItemResponse:
    """Chuyển đổi thực thể ORM Restaurant sang DTO trả về cho Frontend."""
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

    now_vn = get_vietnam_now()
    open_info = check_restaurant_open_status(r.open_hours, check_dt=now_vn)

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
        is_open=open_info["is_open"],
        open_status_label=open_info["status_label"],
        open_status_detail=open_info["detail_text"],
        ranking_bonus=open_info["bonus_score"],
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
    Thực thi truy vấn lọc nhà hàng đa điều kiện kết hợp (FR-07 / UC-04 / TE9C660).
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

    if price_min is not None:
        query = query.filter(Restaurant.max_price >= price_min)
    if price_max is not None:
        query = query.filter(Restaurant.min_price <= price_max)

    if min_rating is not None:
        query = query.filter(Restaurant.avg_rating >= min_rating)

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

    has_coords = lat is not None and lng is not None
    if has_coords and radius_km is not None:
        bbox = calculate_bounding_box(lat, lng, radius_km)
        query = query.filter(
            Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
            Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
        )

    candidates = query.all()

    matched: List[Tuple[Restaurant, Optional[float]]] = []
    for r in candidates:
        dist_km: Optional[float] = None
        if has_coords:
            dist_km = round(calculate_haversine_distance(lat, lng, r.latitude, r.longitude, unit="km"), 2)
            if radius_km is not None and dist_km > radius_km:
                continue
        matched.append((r, dist_km))

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
    auto_relax: bool = Query(False, description="Tự động nới lỏng bán kính (+3km) hoặc ngân sách (±25%) khi 0 kết quả (TE9C66F)"),
    page: int = Query(1, ge=1, description="Số thứ tự trang"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả mỗi trang"),
    db: Session = Depends(get_db),
):
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

    if auto_relax and len(items) == 0:
        from app.services.query_relaxation_service import QueryRelaxationService
        rel_results, _ = QueryRelaxationService.relax_and_search(
            db=db,
            lat=lat,
            lng=lng,
            radius_km=radius_km,
            cuisine=cuisine_type,
            price_min=price_min,
            price_max=price_max,
            min_rating=min_rating,
            has_parking=has_parking,
            has_private_room=has_private_room,
            has_outdoor=has_outdoor,
            pet_friendly=pet_friendly,
            vegetarian_support=vegetarian_support,
            limit=limit,
        )
        if rel_results:
            items = [_serialize_restaurant(r, dist) for r, dist in rel_results]
            pagination = PaginationMetadata(
                page=1,
                limit=limit,
                total_items=len(items),
                total_pages=1,
            )

    return RestaurantFilterResponse(
        status="success",
        total=pagination.total_items,
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
    limit: int = Query(10, ge=1, le=500, description="Số lượng nhà hàng trên mỗi trang"),
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
    open_now: Optional[bool] = Query(None, description="Lọc chỉ các nhà hàng đang mở cửa"),
    sort_by_open: Optional[bool] = Query(False, description="Ưu tiên xếp nhà hàng đang mở cửa lên trước"),
    db: Session = Depends(get_db),
):
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

    if open_now is True:
        list_items = [it for it in list_items if it.is_open]
    elif open_now is False:
        list_items = [it for it in list_items if not it.is_open]

    if sort_by_open:
        list_items.sort(key=lambda x: (x.ranking_bonus, x.avg_rating), reverse=True)

    return RestaurantListResponse(
        data=list_items,
        pagination=pagination,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Chi tiết một nhà hàng: thực đơn, thư viện ảnh, tiện ích (TSK-25 / FR-09)"
)
def get_restaurant_detail(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = (
        db.query(Restaurant)
        .options(
            joinedload(Restaurant.amenities),
            joinedload(Restaurant.images),
            joinedload(Restaurant.menus).joinedload(RestaurantMenu.items),
        )
        .filter(Restaurant.id == restaurant_id, Restaurant.status != "hidden")
        .first()
    )
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy nhà hàng.")

    base = _build_list_item(restaurant)
    menus = sorted(restaurant.menus, key=lambda m: (m.display_order, m.id))
    images = sorted(restaurant.images, key=lambda i: (i.display_order, i.id))
    return RestaurantDetailResponse(
        **base.model_dump(),
        menus=[
            MenuCategoryResponse(
                id=m.id, name=m.name, description=m.description, display_order=m.display_order,
                items=[
                    {"id": it.id, "name": it.name, "description": it.description, "price": it.price,
                    "image_url": it.image_url, "is_available": it.is_available}
                    for it in sorted(m.items, key=lambda x: x.id)
                ],
            )
            for m in menus
        ],
        images=[RestaurantImageResponse.model_validate(i) for i in images],
    )


@router.put(
    "/{restaurant_id}/amenities",
    response_model=AmenityResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật 5 cờ tiện ích của nhà hàng (TSK-26)"
)
def update_restaurant_amenities(
    restaurant_id: int,
    payload: AmenityUpdateRequest,
    db: Session = Depends(get_db)
):
    """API quản lý tiện ích nhà hàng dành cho Admin (Task TSK-26)."""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy nhà hàng.")

    amenity = db.query(RestaurantAmenity).filter(RestaurantAmenity.restaurant_id == restaurant_id).first()
    if not amenity:
        amenity = RestaurantAmenity(restaurant_id=restaurant_id)
        db.add(amenity)

    amenity.has_parking = payload.has_parking
    amenity.has_private_room = payload.has_private_room
    amenity.has_outdoor = payload.has_outdoor
    amenity.pet_friendly = payload.pet_friendly
    amenity.vegetarian_support = payload.vegetarian_support

    db.commit()
    db.refresh(amenity)
    return AmenityResponse.model_validate(amenity)