"""Geospatial API router for distance calculation and nearby restaurant search (TE9C651)."""

from typing import List, Literal, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.geo_service import (
    calculate_bounding_box,
    calculate_haversine_distance,
    filter_restaurants_by_location,
    format_distance_display,
    get_spatial_haversine_sql,
)

router = APIRouter(prefix="/api/geo", tags=["Geospatial & Distance (TE9C651)"])

# Dữ liệu mẫu nhà hàng thực tế tại TP.HCM để test khi chưa ghép chung DB Seeder
SAMPLE_RESTAURANTS = [
    {
        "id": 1,
        "name": "Phở Hòa Pasteur",
        "address": "260C Pasteur, Quận 3, TP.HCM",
        "latitude": 10.7868,
        "longitude": 106.6881,
        "category": "Món Việt",
        "rating": 4.6,
    },
    {
        "id": 2,
        "name": "Cơm Tấm Bụi Sài Gòn",
        "address": "100 Thống Nhất, Quận Gò Vấp, TP.HCM",
        "latitude": 10.8325,
        "longitude": 106.6672,
        "category": "Cơm tấm",
        "rating": 4.5,
    },
    {
        "id": 3,
        "name": "Bếp Chay Thực Dưỡng",
        "address": "45 Lê Lợi, Quận 1, TP.HCM",
        "latitude": 10.7731,
        "longitude": 106.7012,
        "category": "Món Chay",
        "rating": 4.8,
    },
    {
        "id": 4,
        "name": "Gogi House Quang Trung",
        "address": "190 Quang Trung, Quận Gò Vấp, TP.HCM",
        "latitude": 10.8290,
        "longitude": 106.6710,
        "category": "BBQ Hàn Quốc",
        "rating": 4.7,
    },
]


@router.get("/distance")
def compute_distance(
    lat1: float = Query(..., ge=-90, le=90, description="Vĩ độ người dùng"),
    lng1: float = Query(..., ge=-180, le=180, description="Kinh độ người dùng"),
    lat2: float = Query(..., ge=-90, le=90, description="Vĩ độ nhà hàng"),
    lng2: float = Query(..., ge=-180, le=180, description="Kinh độ nhà hàng"),
):
    """Tính khoảng cách Haversine (km và m) giữa 2 tọa độ GPS."""
    try:
        dist_km = calculate_haversine_distance(lat1, lng1, lat2, lng2, unit="km")
        dist_m = calculate_haversine_distance(lat1, lng1, lat2, lng2, unit="m")
        return {
            "from": {"lat": lat1, "lng": lng1},
            "to": {"lat": lat2, "lng": lng2},
            "distance_km": dist_km,
            "distance_m": dist_m,
            "display": format_distance_display(dist_km),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/bounding-box")
def compute_bounding_box(
    lat: float = Query(10.8350, ge=-90, le=90, description="Vĩ độ tâm"),
    lng: float = Query(106.6650, ge=-180, le=180, description="Kinh độ tâm"),
    radius_km: float = Query(5.0, gt=0, le=100, description="Bán kính khoanh vùng (km)"),
):
    """Tính khung giới hạn Bounding Box và sinh câu truy vấn Spatial SQL tối ưu hiệu năng."""
    bbox = calculate_bounding_box(lat, lng, radius_km)
    haversine_sql = get_spatial_haversine_sql(lat, lng)
    return {
        "center": {"lat": lat, "lng": lng},
        "radius_km": radius_km,
        "bounding_box": bbox.to_dict(),
        "optimized_sql_preview": (
            f"SELECT *, {haversine_sql} AS distance_km FROM Restaurants "
            f"WHERE latitude BETWEEN {bbox.min_lat:.6f} AND {bbox.max_lat:.6f} "
            f"AND longitude BETWEEN {bbox.min_lng:.6f} AND {bbox.max_lng:.6f} "
            f"HAVING distance_km <= {radius_km} ORDER BY distance_km ASC;"
        ),
    }


@router.get("/nearby-restaurants")
def get_nearby_restaurants(
    lat: float = Query(10.8350, ge=-90, le=90, description="Vĩ độ người dùng"),
    lng: float = Query(106.6650, ge=-180, le=180, description="Kinh độ người dùng"),
    radius_km: float = Query(5.0, gt=0, le=50, description="Bán kính tìm kiếm (km)"),
):
    """Lọc danh sách nhà hàng trong vùng Bounding Box và sắp xếp theo khoảng cách Haversine."""
    return filter_restaurants_by_location(
        user_lat=lat,
        user_lng=lng,
        restaurants=SAMPLE_RESTAURANTS,
        radius_km=radius_km,
    )