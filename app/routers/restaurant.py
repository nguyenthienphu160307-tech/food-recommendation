"""
Router quản lý Nhà hàng, Bộ lọc đa điều kiện kết hợp (TSK-23 / FR-07 / UC-04),
Chi tiết Nhà hàng kèm Thực đơn & Hình ảnh (TSK-25 / FR-09) và Quản lý Tiện ích (TSK-26).
"""

import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantMenu
from app.schemas.restaurant import (
    RestaurantListResponse,
    RestaurantListItemResponse,
    RestaurantDetailResponse,
    MenuCategoryResponse,
    RestaurantImageResponse,
    PaginationMetadata,
    AmenityResponse,
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
    "",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách nhà hàng cơ bản có phân trang (TSK-09)"
)
def get_restaurants(
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    limit: int = Query(10, ge=1, le=500, description="Số lượng nhà hàng trên mỗi trang"),
    status_filter: Optional[str] = Query("active", description="Trạng thái nhà hàng ('active', 'all')"),
    db: Session = Depends(get_db)
):
    query = db.query(Restaurant)
    if status_filter and status_filter != "all":
        query = query.filter(Restaurant.status == status_filter)

    total_items = query.count()
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    offset = (page - 1) * limit
    restaurants = (
        query.options(joinedload(Restaurant.amenities), joinedload(Restaurant.images))
        .order_by(Restaurant.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return RestaurantListResponse(
        data=[_build_list_item(r) for r in restaurants],
        pagination=PaginationMetadata(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=total_pages
        )
    )


@router.get(
    "/filter",
    status_code=status.HTTP_200_OK,
    summary="API Lọc nhà hàng đa điều kiện kết hợp (TSK-23 / FR-07 / UC-04)"
)
def filter_restaurants_multi_criteria(
    keyword: Optional[str] = Query(None, description="Từ khóa tên quán, món ăn hoặc địa chỉ"),
    cuisine_type: Optional[str] = Query(None, description="Loại ẩm thực (VD: Món Việt, Lẩu Nướng, Món Nhật)"),
    price_min: Optional[float] = Query(None, ge=0, description="Ngân sách tối thiểu (VNĐ)"),
    price_max: Optional[float] = Query(None, ge=0, description="Ngân sách tối đa (VNĐ)"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Điểm đánh giá tối thiểu (1.0 - 5.0)"),
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Vĩ độ người dùng"),
    lng: Optional[float] = Query(None, ge=-180, le=180, description="Kinh độ người dùng"),
    radius_km: Optional[float] = Query(None, gt=0, le=50, description="Bán kính tìm kiếm (km)"),
    has_parking: Optional[bool] = Query(None, description="Có bãi đỗ ô tô"),
    has_private_room: Optional[bool] = Query(None, description="Có phòng riêng"),
    has_outdoor: Optional[bool] = Query(None, description="Có không gian ngoài trời"),
    pet_friendly: Optional[bool] = Query(None, description="Cho phép mang thú cưng"),
    vegetarian_support: Optional[bool] = Query(None, description="Hỗ trợ thực đơn chay"),
    sort_by: str = Query("distance", description="Tiêu chí sắp xếp: 'distance' | 'rating' | 'price_asc'"),
    db: Session = Depends(get_db)
):
    """
    Truy vấn lọc nhà hàng kết hợp đa điều kiện (Task TSK-23):
    1. Lọc theo từ khóa, loại hình ẩm thực, mức giá, điểm đánh giá.
    2. Lọc theo 5 cờ tiện ích trong bảng `RestaurantAmenities`.
    3. Khoanh vùng Bounding Box SQL + tính khoảng cách Haversine chính xác theo bán kính `radius_km`.
    """
    query = (
        db.query(Restaurant)
        .outerjoin(RestaurantAmenity, Restaurant.id == RestaurantAmenity.restaurant_id)
        .options(joinedload(Restaurant.amenities), joinedload(Restaurant.images))
        .filter(Restaurant.status == "active")
    )

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

    if cuisine_type and cuisine_type.strip() and cuisine_type.lower() != "all":
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type.strip()}%"))

    if price_min is not None:
        query = query.filter(Restaurant.max_price >= price_min)
    if price_max is not None:
        query = query.filter(Restaurant.min_price <= price_max)
    if min_rating is not None:
        query = query.filter(Restaurant.avg_rating >= min_rating)

    # Bộ lọc 5 tiện ích (RestaurantAmenities)
    if has_parking is True:
        query = query.filter(RestaurantAmenity.has_parking.is_(True))
    if has_private_room is True:
        query = query.filter(RestaurantAmenity.has_private_room.is_(True))
    if has_outdoor is True:
        query = query.filter(RestaurantAmenity.has_outdoor.is_(True))
    if pet_friendly is True:
        query = query.filter(RestaurantAmenity.pet_friendly.is_(True))
    if vegetarian_support is True:
        query = query.filter(RestaurantAmenity.vegetarian_support.is_(True))

    # Lọc thô bằng Bounding Box trên CSDL nếu có tọa độ và bán kính
    if lat is not None and lng is not None and radius_km is not None:
        bbox = calculate_bounding_box(lat, lng, radius_km)
        query = query.filter(
            Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
            Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
        )

    rows = query.all()
    results = []

    for r in rows:
        item_dict = _build_list_item(r).model_dump()
        if lat is not None and lng is not None:
            dist_km = calculate_haversine_distance(lat, lng, r.latitude, r.longitude, unit="km")
            if radius_km is not None and dist_km > radius_km:
                continue
            item_dict["distance_km"] = dist_km
            item_dict["distance_text"] = format_distance_display(dist_km)
        else:
            item_dict["distance_km"] = None
            item_dict["distance_text"] = None
        results.append(item_dict)

    # Sắp xếp kết quả
    if sort_by == "distance" and lat is not None and lng is not None:
        results.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 9999.0)
    elif sort_by == "rating":
        results.sort(key=lambda x: x["avg_rating"], reverse=True)
    elif sort_by == "price_asc":
        results.sort(key=lambda x: x["min_price"])

    return {
        "total": len(results),
        "filters_applied": {
            "keyword": keyword,
            "cuisine_type": cuisine_type,
            "price_min": price_min,
            "price_max": price_max,
            "min_rating": min_rating,
            "radius_km": radius_km,
            "has_parking": has_parking,
            "has_private_room": has_private_room,
            "has_outdoor": has_outdoor,
            "pet_friendly": pet_friendly,
            "vegetarian_support": vegetarian_support,
        },
        "data": results,
    }


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