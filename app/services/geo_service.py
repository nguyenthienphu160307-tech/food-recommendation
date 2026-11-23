"""Geospatial calculation service module (Task TE9C651).

Provides Haversine distance calculations (km/m), Bounding Box pre-filtering
for database index optimization, and Spatial SQL expressions.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional
from sqlalchemy import func, text

EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_M = 6371000.0


@dataclass(frozen=True)
class BoundingBox:
    """Represents a geographic rectangular bounding box for fast SQL filtering."""
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "min_lat": round(self.min_lat, 6),
            "max_lat": round(self.max_lat, 6),
            "min_lng": round(self.min_lng, 6),
            "max_lng": round(self.max_lng, 6),
        }


def validate_coordinates(lat: float, lng: float) -> None:
    """Validate GPS latitude and longitude ranges."""
    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Vĩ độ (lat={lat}) không hợp lệ. Phải nằm trong khoảng [-90, 90].")
    if not (-180.0 <= lng <= 180.0):
        raise ValueError(f"Kinh độ (lng={lng}) không hợp lệ. Phải nằm trong khoảng [-180, 180].")


def calculate_bounding_box(lat: float, lng: float, radius_km: float) -> BoundingBox:
    """Calculate the min/max latitude and longitude bounding box around a point.

    Used in SQL WHERE clauses (latitude BETWEEN min_lat AND max_lat) to leverage
    B-Tree indexes before running expensive trigonometric Haversine calculations.
    """
    validate_coordinates(lat, lng)
    if radius_km <= 0:
        raise ValueError("Bán kính tìm kiếm (radius_km) phải lớn hơn 0.")

    # Độ lệch vĩ độ (radian -> độ)
    lat_delta = math.degrees(radius_km / EARTH_RADIUS_KM)

    # Độ lệch kinh độ phụ thuộc vào cos(vĩ độ hiện tại)
    cos_lat = math.cos(math.radians(lat))
    if abs(cos_lat) < 1e-6:
        lng_delta = 180.0
    else:
        lng_delta = math.degrees(radius_km / (EARTH_RADIUS_KM * cos_lat))

    return BoundingBox(
        min_lat=max(-90.0, lat - lat_delta),
        max_lat=min(90.0, lat + lat_delta),
        min_lng=max(-180.0, lng - lng_delta),
        max_lng=min(180.0, lng + lng_delta),
    )


def calculate_haversine_distance(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
    unit: Literal["km", "m"] = "km",
) -> float:
    """Calculate great-circle distance between two GPS coordinates using Haversine formula."""
    validate_coordinates(lat1, lng1)
    validate_coordinates(lat2, lng2)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2)
    )
    # Clamp 'a' trong đoạn [0, 1] để tránh sai số dấu phẩy động
    a = min(1.0, max(0.0, a))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    if unit == "m":
        return round(EARTH_RADIUS_M * c, 1)
    return round(EARTH_RADIUS_KM * c, 3)


def format_distance_display(distance_km: float) -> str:
    """Format distance for UI display (m if < 1km, otherwise km)."""
    if distance_km < 1.0:
        return f"{int(round(distance_km * 1000))} m"
    return f"{distance_km:.2f} km"


def get_spatial_haversine_sql(
    user_lat: float,
    user_lng: float,
    lat_column: str = "latitude",
    lng_column: str = "longitude",
) -> str:
    """Generate raw Spatial SQL Haversine expression (in kilometers) for MySQL/PostgreSQL."""
    validate_coordinates(user_lat, lng=user_lng)
    return (
        f"({EARTH_RADIUS_KM} * 2 * ASIN(SQRT("
        f"POWER(SIN(RADIANS({lat_column} - {user_lat}) / 2), 2) + "
        f"COS(RADIANS({user_lat})) * COS(RADIANS({lat_column})) * "
        f"POWER(SIN(RADIANS({lng_column} - {user_lng}) / 2), 2)"
        f")))"
    )


def get_sqlalchemy_haversine_expr(user_lat: float, user_lng: float, model_lat_col: Any, model_lng_col: Any):
    """Build a SQLAlchemy expression calculating Haversine distance in kilometers."""
    validate_coordinates(user_lat, user_lng)
    lat1_rad = math.radians(user_lat)
    lng1_rad = math.radians(user_lng)
    lat2_rad = func.radians(model_lat_col)
    lng2_rad = func.radians(model_lng_col)

    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad

    a = func.pow(func.sin(dlat / 2.0), 2) + (
        math.cos(lat1_rad) * func.cos(lat2_rad) * func.pow(func.sin(dlng / 2.0), 2)
    )
    return EARTH_RADIUS_KM * 2.0 * func.asin(func.sqrt(a))


def filter_restaurants_by_location(
    user_lat: float,
    user_lng: float,
    restaurants: List[Dict[str, Any]],
    radius_km: float = 5.0,
    lat_key: str = "latitude",
    lng_key: str = "longitude",
) -> Dict[str, Any]:
    """Filter and sort a list of restaurants using Bounding Box pre-filter + Haversine."""
    bbox = calculate_bounding_box(user_lat, user_lng, radius_km)
    matched_restaurants: List[Dict[str, Any]] = []
    bbox_candidates_count = 0

    for item in restaurants:
        r_lat = item.get(lat_key) if item.get(lat_key) is not None else item.get("lat")
        r_lng = item.get(lng_key) if item.get(lng_key) is not None else item.get("lng")

        if r_lat is None or r_lng is None:
            continue

        r_lat = float(r_lat)
        r_lng = float(r_lng)

        # Bước 1: Lọc nhanh bằng Bounding Box (O(1) phép so sánh số học)
        if not (bbox.min_lat <= r_lat <= bbox.max_lat and bbox.min_lng <= r_lng <= bbox.max_lng):
            continue

        bbox_candidates_count += 1

        # Bước 2: Tính chính xác khoảng cách Haversine cho các ứng viên trong vùng
        dist_km = calculate_haversine_distance(user_lat, user_lng, r_lat, r_lng, unit="km")
        if dist_km <= radius_km:
            dist_m = calculate_haversine_distance(user_lat, user_lng, r_lat, r_lng, unit="m")
            enriched_item = dict(item)
            enriched_item["distance_km"] = dist_km
            enriched_item["distance_m"] = dist_m
            enriched_item["distance_text"] = format_distance_display(dist_km)
            matched_restaurants.append(enriched_item)

    # Sắp xếp nhà hàng từ gần nhất đến xa nhất
    matched_restaurants.sort(key=lambda x: x["distance_km"])

    return {
        "user_location": {"lat": user_lat, "lng": user_lng},
        "radius_km": radius_km,
        "bounding_box": bbox.to_dict(),
        "stats": {
            "total_input": len(restaurants),
            "bbox_candidates": bbox_candidates_count,
            "within_radius": len(matched_restaurants),
        },
        "restaurants": matched_restaurants,
    }