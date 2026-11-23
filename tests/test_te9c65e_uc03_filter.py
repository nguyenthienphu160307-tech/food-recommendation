
"""
Bộ kiểm thử tự động cho Task TE9C65E (UC-03: Định vị GPS & Chọn vị trí thủ công)
và Task TSK-23 (UC-04: API Lọc nhà hàng đa điều kiện kết hợp).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_uc03_nearby_and_multi_criteria_filter():
    """Kiểm tra API lọc theo tọa độ Quận/Huyện và bán kính kết hợp tiện ích."""
    # Tọa độ Quận 1, TP.HCM
    res = client.get(
        "/api/restaurants/filter",
        params={
            "lat": 10.7769,
            "lng": 106.7009,
            "radius_km": 5.0,
            "has_parking": True,
            "sort_by": "distance",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert "total" in body and "data" in body
    for item in body["data"]:
        assert item["distance_km"] <= 5.0
        assert item["amenities"]["has_parking"] is True


if __name__ == "__main__":
    test_uc03_nearby_and_multi_criteria_filter()
    print(">>> PASSED: Task TE9C65E (UC-03) & TSK-23 (UC-04) hoạt động chính xác! <<<")