import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.interaction import Restaurant

router = APIRouter(prefix="/api/geo", tags=["Geospatial & Restaurants Management"])

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Tính khoảng cách đường chim bay (km) bằng công thức Haversine."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return round(EARTH_RADIUS_KM * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)), 2)


def seed_default_restaurants_if_empty(db: Session) -> None:
    """Tự động thêm 6 quán ăn mẫu vào CSDL nếu bảng restaurants đang trống."""
    if db.query(Restaurant).count() > 0:
        return

    sample_restaurants = [
        Restaurant(
            name="GoGi House — Thịt Nướng Hàn Quốc",
            address="189 Quang Trung, Phường 10, Quận Gò Vấp, TP.HCM",
            latitude=10.8295, longitude=106.6728,
            category="BBQ Hàn Quốc", price_min=199000, price_max=380000,
            rating_avg=4.7, open_time="10:00", close_time="22:00"
        ),
        Restaurant(
            name="Lẩu Nấm Ashima — Phan Văn Trị",
            address="366 Phan Văn Trị, Phường 5, Quận Gò Vấp, TP.HCM",
            latitude=10.8214, longitude=106.6915,
            category="Món Việt", price_min=250000, price_max=450000,
            rating_avg=4.8, open_time="10:30", close_time="22:00"
        ),
        Restaurant(
            name="Quán Nướng Khói Sài Gòn",
            address="122 Nguyễn Gia Trí (D2), Phường 25, Quận Bình Thạnh, TP.HCM",
            latitude=10.8028, longitude=106.7125,
            category="BBQ Hàn Quốc", price_min=140000, price_max=250000,
            rating_avg=4.6, open_time="16:00", close_time="23:30"
        ),
        Restaurant(
            name="Hum Garden & Vegetarian",
            address="32 Võ Văn Tần, Phường 6, Quận 3, TP.HCM",
            latitude=10.7785, longitude=106.6912,
            category="Món Chay", price_min=180000, price_max=390000,
            rating_avg=4.9, open_time="10:00", close_time="22:00"
        ),
        Restaurant(
            name="Cơm Tấm Bụi Sài Gòn — Đa Kao",
            address="100 Nguyễn Văn Thủ, Phường Đa Kao, Quận 1, TP.HCM",
            latitude=10.7882, longitude=106.6985,
            category="Cơm tấm", price_min=55000, price_max=120000,
            rating_avg=4.5, open_time="06:30", close_time="21:30"
        ),
        Restaurant(
            name="Phở Hòa Pasteur",
            address="260C Pasteur, Phường Võ Thị Sáu, Quận 3, TP.HCM",
            latitude=10.7868, longitude=106.6881,
            category="Món Việt", price_min=75000, price_max=150000,
            rating_avg=4.8, open_time="06:00", close_time="22:30"
        ),
    ]
    db.add_all(sample_restaurants)
    db.commit()


@router.get("/nearby-restaurants", summary="Tìm danh sách nhà hàng theo tọa độ GPS và bán kính")
def get_nearby_restaurants(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lng: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(15.0, gt=0.0),
    db: Session = Depends(get_db),
):
    seed_default_restaurants_if_empty(db)

    # Tính Bounding Box sơ bộ
    lat_delta = math.degrees(radius_km / EARTH_RADIUS_KM)
    cos_lat = math.cos(math.radians(lat))
    lng_delta = math.degrees(radius_km / (EARTH_RADIUS_KM * cos_lat)) if abs(cos_lat) > 1e-6 else 180.0

    candidates = (
        db.query(Restaurant)
        .filter(
            Restaurant.latitude.between(lat - lat_delta, lat + lat_delta),
            Restaurant.longitude.between(lng - lng_delta, lng + lng_delta),
        )
        .all()
    )

    results = []
    for r in candidates:
        dist = haversine_km(lat, lng, r.latitude, r.longitude)
        if dist <= radius_km:
            results.append({
                "id": r.id,
                "name": r.name,
                "address": r.address,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "category": r.category,
                "priceMin": r.price_min or 100000,
                "priceMax": r.price_max or 300000,
                "rating": r.rating_avg,
                "distance_km": dist,
                "openHours": f"{r.open_time or '08:00'} - {r.close_time or '22:00'}",
            })

    results.sort(key=lambda x: x["distance_km"])
    return {
        "center": {"lat": lat, "lng": lng},
        "radius_km": radius_km,
        "total": len(results),
        "restaurants": results,
    }
    
class RestaurantPayload(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    address: str = Field(..., min_length=5, max_length=255)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    category: Optional[str] = Field("Món Việt", max_length=100)
    price_min: Optional[int] = Field(50000, ge=0)
    price_max: Optional[int] = Field(200000, ge=0)
    rating_avg: Optional[float] = Field(4.5, ge=0.0, le=5.0)
    open_time: Optional[str] = Field("08:00", max_length=20)
    close_time: Optional[str] = Field("22:00", max_length=20)
    image_url: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field("active", max_length=20)


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Tính khoảng cách đường chim bay (km) bằng công thức Haversine."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return round(EARTH_RADIUS_KM * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)), 2)


def seed_default_restaurants_if_empty(db: Session) -> None:
    """Tự động thêm 6 quán ăn mẫu vào CSDL nếu bảng restaurants đang trống."""
    if db.query(Restaurant).count() > 0:
        return

    sample_restaurants = [
        Restaurant(
            name="GoGi House — Thịt Nướng Hàn Quốc",
            address="189 Quang Trung, Phường 10, Quận Gò Vấp, TP.HCM",
            latitude=10.8295, longitude=106.6728,
            category="BBQ Hàn Quốc", price_min=199000, price_max=380000,
            rating_avg=4.7, open_time="10:00", close_time="22:00",
            image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
        Restaurant(
            name="Lẩu Nấm Ashima — Phan Văn Trị",
            address="366 Phan Văn Trị, Phường 5, Quận Gò Vấp, TP.HCM",
            latitude=10.8214, longitude=106.6915,
            category="Món Việt", price_min=250000, price_max=450000,
            rating_avg=4.8, open_time="10:30", close_time="22:00",
            image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
        Restaurant(
            name="Quán Nướng Khói Sài Gòn",
            address="122 Nguyễn Gia Trí (D2), Phường 25, Quận Bình Thạnh, TP.HCM",
            latitude=10.8028, longitude=106.7125,
            category="BBQ Hàn Quốc", price_min=140000, price_max=250000,
            rating_avg=4.6, open_time="16:00", close_time="23:30",
            image_url="https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
        Restaurant(
            name="Hum Garden & Vegetarian",
            address="32 Võ Văn Tần, Phường 6, Quận 3, TP.HCM",
            latitude=10.7785, longitude=106.6912,
            category="Món Chay", price_min=180000, price_max=390000,
            rating_avg=4.9, open_time="10:00", close_time="22:00",
            image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
        Restaurant(
            name="Cơm Tấm Bụi Sài Gòn — Đa Kao",
            address="100 Nguyễn Văn Thủ, Phường Đa Kao, Quận 1, TP.HCM",
            latitude=10.7882, longitude=106.6985,
            category="Cơm tấm", price_min=55000, price_max=120000,
            rating_avg=4.5, open_time="06:30", close_time="21:30",
            image_url="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
        Restaurant(
            name="Phở Hòa Pasteur",
            address="260C Pasteur, Phường Võ Thị Sáu, Quận 3, TP.HCM",
            latitude=10.7868, longitude=106.6881,
            category="Món Việt", price_min=75000, price_max=150000,
            rating_avg=4.8, open_time="06:00", close_time="22:30",
            image_url="https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=600&q=80",
            status="active"
        ),
    ]
    db.add_all(sample_restaurants)
    db.commit()


def serialize_restaurant(r: Restaurant, dist: Optional[float] = None) -> dict:
    data = {
        "id": r.id,
        "name": r.name,
        "address": r.address,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "category": r.category or "Món Việt",
        "priceMin": r.price_min or 50000,
        "priceMax": r.price_max or 200000,
        "price_min": r.price_min or 50000,
        "price_max": r.price_max or 200000,
        "rating": r.rating_avg or 4.5,
        "rating_avg": r.rating_avg or 4.5,
        "open_time": r.open_time or "08:00",
        "close_time": r.close_time or "22:00",
        "openHours": f"{r.open_time or '08:00'} - {r.close_time or '22:00'}",
        "image_url": r.image_url,
        "status": r.status or "active",
    }
    if dist is not None:
        data["distance_km"] = dist
    return data


@router.get("/nearby-restaurants", summary="Tìm danh sách nhà hàng theo tọa độ GPS và bán kính")
def get_nearby_restaurants(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lng: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(15.0, gt=0.0),
    db: Session = Depends(get_db),
):
    seed_default_restaurants_if_empty(db)

    lat_delta = math.degrees(radius_km / EARTH_RADIUS_KM)
    cos_lat = math.cos(math.radians(lat))
    lng_delta = math.degrees(radius_km / (EARTH_RADIUS_KM * cos_lat)) if abs(cos_lat) > 1e-6 else 180.0

    candidates = (
        db.query(Restaurant)
        .filter(
            Restaurant.latitude.between(lat - lat_delta, lat + lat_delta),
            Restaurant.longitude.between(lng - lng_delta, lng + lng_delta),
        )
        .all()
    )

    results = []
    for r in candidates:
        if r.status == "hidden":
            continue
        dist = haversine_km(lat, lng, r.latitude, r.longitude)
        if dist <= radius_km:
            results.append(serialize_restaurant(r, dist=dist))

    results.sort(key=lambda x: x["distance_km"])
    return {
        "center": {"lat": lat, "lng": lng},
        "radius_km": radius_km,
        "total": len(results),
        "restaurants": results,
    }


@router.get("/restaurants", summary="Lấy danh sách nhà hàng hỗ trợ tìm kiếm nhanh & lọc")
def list_restaurants(
    search: Optional[str] = Query(None, description="Từ khóa tên hoặc địa chỉ"),
    category: Optional[str] = Query(None, description="Danh mục ẩm thực"),
    db: Session = Depends(get_db),
):
    seed_default_restaurants_if_empty(db)
    query = db.query(Restaurant)

    if search and search.strip():
        kw = f"%{search.strip()}%"
        query = query.filter(or_(Restaurant.name.ilike(kw), Restaurant.address.ilike(kw)))

    if category and category != "all":
        query = query.filter(Restaurant.category == category)

    items = query.order_by(Restaurant.id.desc()).all()
    return {
        "total": len(items),
        "restaurants": [serialize_restaurant(r) for r in items],
    }


@router.post("/restaurants", status_code=status.HTTP_201_CREATED, summary="Thêm nhà hàng mới")
def create_restaurant(payload: RestaurantPayload, db: Session = Depends(get_db)):
    new_rest = Restaurant(**payload.model_dump())
    db.add(new_rest)
    db.commit()
    db.refresh(new_rest)
    return {
        "message": "Thêm nhà hàng mới thành công!",
        "restaurant": serialize_restaurant(new_rest),
    }


@router.put("/restaurants/{restaurant_id}", summary="Cập nhật thông tin & tọa độ nhà hàng")
def update_restaurant(restaurant_id: int, payload: RestaurantPayload, db: Session = Depends(get_db)):
    rest = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not rest:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng cần sửa.")

    for key, value in payload.model_dump().items():
        setattr(rest, key, value)

    db.commit()
    db.refresh(rest)
    return {
        "message": "Cập nhật thông tin nhà hàng thành công!",
        "restaurant": serialize_restaurant(rest),
    }


@router.delete("/restaurants/{restaurant_id}", summary="Xóa nhà hàng")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    rest = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not rest:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng cần xóa.")

    db.delete(rest)
    db.commit()
    return {"message": f"Đã xóa nhà hàng #{restaurant_id} thành công!"}