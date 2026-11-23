"""Unit tests for Geospatial Haversine & Bounding Box service (Task TE9C651)."""

import pytest
from app.services.geo_service import (
    calculate_bounding_box,
    calculate_haversine_distance,
    filter_restaurants_by_location,
    validate_coordinates,
)


def test_haversine_same_point():
    assert calculate_haversine_distance(10.7769, 106.7009, 10.7769, 106.7009, "km") == 0.0
    assert calculate_haversine_distance(10.7769, 106.7009, 10.7769, 106.7009, "m") == 0.0


def test_haversine_known_distance_hcm():
    # Khoảng cách từ Chợ Bến Thành (10.7725, 106.6980) đến Dinh Độc Lập (10.7770, 106.6953) ~ 0.58 km
    dist_km = calculate_haversine_distance(10.7725, 106.6980, 10.7770, 106.6953, unit="km")
    dist_m = calculate_haversine_distance(10.7725, 106.6980, 10.7770, 106.6953, unit="m")
    assert 0.5 <= dist_km <= 0.65
    assert 500.0 <= dist_m <= 650.0


def test_bounding_box_bounds():
    bbox = calculate_bounding_box(10.8000, 106.6500, radius_km=5.0)
    assert bbox.min_lat < 10.8000 < bbox.max_lat
    assert bbox.min_lng < 106.6500 < bbox.max_lng


def test_invalid_coordinates():
    with pytest.raises(ValueError):
        validate_coordinates(95.0, 106.0)
    with pytest.raises(ValueError):
        validate_coordinates(10.0, 190.0)


def test_filter_and_sort_restaurants():
    restaurants = [
        {"id": 1, "name": "Quán Xa", "latitude": 10.7000, "longitude": 106.6000},
        {"id": 2, "name": "Quán Gần", "latitude": 10.8360, "longitude": 106.6660},
        {"id": 3, "name": "Quán Vừa", "latitude": 10.8290, "longitude": 106.6710},
    ]
    result = filter_restaurants_by_location(10.8350, 106.6650, restaurants, radius_km=3.0)
    assert result["stats"]["within_radius"] == 2
    assert result["restaurants"][0]["name"] == "Quán Gần"
    assert result["restaurants"][1]["name"] == "Quán Vừa"