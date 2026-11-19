"""
==============================================================================
UNIT & INTEGRATION TESTS: API LỌC NHÀ HÀNG ĐA ĐIỀU KIỆN (FR-07, UC-04)
MÃ TASK: TE9C660
Kiểm thử toàn diện:
1. Lọc theo cuisine_type (đơn giá trị và đa giá trị)
2. Lọc theo khoảng giá (price_min / price_max)
3. Lọc theo bán kính khoảng cách (lat, lng, radius_km) bằng Bounding Box + Haversine
4. Lọc theo điểm đánh giá tối thiểu (min_rating)
5. Lọc theo cả 5 tiện ích trong RestaurantAmenities (đơn lẻ và kết hợp)
6. Lọc đa điều kiện kết hợp đồng thời tất cả tiêu chí (FR-07 / UC-04)
7. Sắp xếp (distance, rating, price_asc, price_desc) & Phân trang
8. Validation tham số không hợp lệ (400 / 422) & lọc trạng thái active/hidden
==============================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage

client = TestClient(app)

# Tâm kiểm thử: Trung tâm Quận 1, TP.HCM
CENTER_LAT = 10.776889
CENTER_LNG = 106.700806


def seed_diverse_restaurants():
    """Khởi tạo bộ dữ liệu nhà hàng đa dạng phục vụ kiểm thử lọc đa điều kiện TE9C660."""
    db = SessionLocal()
    try:
        db.query(RestaurantImage).delete()
        db.query(RestaurantAmenity).delete()
        db.query(Restaurant).delete()
        db.commit()

        samples = [
            {
                "name": "Cơm Niêu Sài Gòn - Quận 3",
                "description": "Ẩm thực Việt truyền thống, có phòng VIP và món chay",
                "address": "27 Tú Xương, Quận 3, TP.HCM",
                "cuisine_type": "Món Việt",
                "latitude": 10.7783,   # ~1.5 km từ tâm Q1
                "longitude": 106.6872,
                "min_price": 100000.0,
                "max_price": 300000.0,
                "avg_rating": 4.6,
                "total_reviews": 220,
                "status": "active",
                "amenities": dict(has_parking=True, has_private_room=True, has_outdoor=False, pet_friendly=False, vegetarian_support=True),
            },
            {
                "name": "GoGi House - Nướng Hàn Quốc",
                "description": "Thịt nướng BBQ ngoài trời thân thiện thú cưng",
                "address": "189 Quang Trung, Gò Vấp, TP.HCM",
                "cuisine_type": "Lẩu Nướng",
                "latitude": 10.8295,   # ~6.6 km từ tâm Q1
                "longitude": 106.6728,
                "min_price": 200000.0,
                "max_price": 450000.0,
                "avg_rating": 4.8,
                "total_reviews": 510,
                "status": "active",
                "amenities": dict(has_parking=True, has_private_room=False, has_outdoor=True, pet_friendly=True, vegetarian_support=False),
            },
            {
                "name": "Hum Garden & Vegetarian",
                "description": "Nhà hàng chay sân vườn cao cấp tại trung tâm",
                "address": "32 Võ Văn Tần, Quận 3, TP.HCM",
                "cuisine_type": "Món Chay",
                "latitude": 10.7785,   # ~1.06 km từ tâm Q1
                "longitude": 106.6912,
                "min_price": 150000.0,
                "max_price": 380000.0,
                "avg_rating": 4.9,
                "total_reviews": 690,
                "status": "active",
                "amenities": dict(has_parking=True, has_private_room=True, has_outdoor=True, pet_friendly=False, vegetarian_support=True),
            },
            {
                "name": "The Deck Saigon - Thủ Đức",
                "description": "Món Âu ven sông ngoài trời, cho phép thú cưng",
                "address": "38 Nguyễn Ư Dĩ, Thảo Điền, TP. Thủ Đức",
                "cuisine_type": "Món Âu",
                "latitude": 10.8065,   # ~4.7 km từ tâm Q1
                "longitude": 106.7315,
                "min_price": 400000.0,
                "max_price": 1200000.0,
                "avg_rating": 4.7,
                "total_reviews": 430,
                "status": "active",
                "amenities": dict(has_parking=True, has_private_room=True, has_outdoor=True, pet_friendly=True, vegetarian_support=True),
            },
            {
                "name": "Quán Cơm Bình Dân Bến Thành",
                "description": "Quán ăn bình dân giá rẻ gần chợ",
                "address": "12 Lê Thánh Tôn, Quận 1, TP.HCM",
                "cuisine_type": "Món Việt",
                "latitude": 10.7755,   # ~0.3 km từ tâm Q1
                "longitude": 106.6985,
                "min_price": 35000.0,
                "max_price": 80000.0,
                "avg_rating": 3.9,
                "total_reviews": 60,
                "status": "active",
                "amenities": dict(has_parking=False, has_private_room=False, has_outdoor=False, pet_friendly=False, vegetarian_support=False),
            },
            {
                "name": "Nhà hàng Ẩn Tạm Đóng Cửa",
                "description": "Dùng kiểm tra lọc trạng thái hidden",
                "address": "99 Đồng Khởi, Quận 1, TP.HCM",
                "cuisine_type": "Món Việt",
                "latitude": 10.7760,
                "longitude": 106.7010,
                "min_price": 100000.0,
                "max_price": 200000.0,
                "avg_rating": 5.0,
                "total_reviews": 999,
                "status": "hidden",
                "amenities": dict(has_parking=True, has_private_room=True, has_outdoor=True, pet_friendly=True, vegetarian_support=True),
            },
        ]

        for item in samples:
            am_kwargs = item.pop("amenities")
            rest = Restaurant(**item)
            db.add(rest)
            db.flush()
            db.add(RestaurantAmenity(restaurant_id=rest.id, **am_kwargs))
            db.add(RestaurantImage(restaurant_id=rest.id, image_url="https://example.com/cover.jpg", is_cover=True))

        db.commit()
    finally:
        db.close()


def run_multi_filter_tests():
    print("==================================================================")
    print("  KIỂM THỬ API LỌC NHÀ HÀNG ĐA ĐIỀU KIỆN KẾT HỢP (TASK TE9C660)  ")
    print("               YÊU CẦU NGHIỆP VỤ: FR-07, UC-04                    ")
    print("==================================================================")

    seed_diverse_restaurants()

    # TEST 1: Lọc theo cuisine_type (đơn và đa giá trị)
    print("\n--- [TEST 1] Lọc theo cuisine_type (đơn & nhiều loại) ---")
    r1 = client.get("/api/restaurants/filter", params={"cuisine_type": "Món Việt"})
    assert r1.status_code == 200
    d1 = r1.json()
    names1 = [x["name"] for x in d1["data"]]
    print("Kết quả Món Việt:", names1)
    assert len(names1) == 2  # Không bao gồm quán hidden
    assert all("Món Việt" in x["cuisine_type"] for x in d1["data"])

    r1_multi = client.get("/api/restaurants/filter", params={"cuisine_type": "Món Việt, Món Chay"})
    assert r1_multi.status_code == 200
    assert r1_multi.json()["pagination"]["total_items"] == 3
    print("-> PASS: Lọc cuisine_type đơn & đa giá trị chính xác")

    # TEST 2: Lọc theo khoảng giá (price_min / price_max)
    print("\n--- [TEST 2] Lọc theo khoảng giá (price_min & price_max) ---")
    r2 = client.get("/api/restaurants/filter", params={"price_min": 120000, "price_max": 350000})
    assert r2.status_code == 200
    names2 = [x["name"] for x in r2.json()["data"]]
    print("Quán trong khoảng giá 120k-350k:", names2)
    assert "Cơm Niêu Sài Gòn - Quận 3" in names2
    assert "Hum Garden & Vegetarian" in names2
    assert "GoGi House - Nướng Hàn Quốc" in names2
    assert "Quán Cơm Bình Dân Bến Thành" not in names2  # max_price=80k < 120k
    assert "The Deck Saigon - Thủ Đức" not in names2    # min_price=400k > 350k
    print("-> PASS: Khoảng giá giao nhau lọc chuẩn xác")

    # TEST 3: Lọc theo bán kính khoảng cách (lat, lng, radius_km)
    print("\n--- [TEST 3] Lọc theo bán kính khoảng cách (1km, 2km, 5km, 10km) ---")
    r3_1km = client.get("/api/restaurants/filter", params={"lat": CENTER_LAT, "lng": CENTER_LNG, "radius_km": 1.0})
    assert r3_1km.status_code == 200
    names_1km = [x["name"] for x in r3_1km.json()["data"]]
    print("Bán kính 1 km:", names_1km)
    assert names_1km == ["Quán Cơm Bình Dân Bến Thành"]
    assert r3_1km.json()["data"][0]["distance_km"] <= 1.0

    r3_5km = client.get("/api/restaurants/filter", params={"lat": CENTER_LAT, "lng": CENTER_LNG, "radius_km": 5.0, "sort_by": "distance"})
    assert r3_5km.status_code == 200
    items_5km = r3_5km.json()["data"]
    print("Bán kính 5 km (sắp xếp distance):", [(x["name"], x["distance_km"]) for x in items_5km])
    assert len(items_5km) == 4
    dists = [x["distance_km"] for x in items_5km]
    assert dists == sorted(dists), "Kết quả phải được sắp xếp tăng dần theo distance_km"
    assert all(d <= 5.0 for d in dists)
    print("-> PASS: Bounding Box + Haversine tính và lọc bán kính chính xác")

    # TEST 4: Lọc theo điểm đánh giá tối thiểu (min_rating)
    print("\n--- [TEST 4] Lọc theo điểm đánh giá tối thiểu (min_rating >= 4.7) ---")
    r4 = client.get("/api/restaurants/filter", params={"min_rating": 4.7, "sort_by": "rating"})
    assert r4.status_code == 200
    items4 = r4.json()["data"]
    print("Quán rating >= 4.7:", [(x["name"], x["avg_rating"]) for x in items4])
    assert len(items4) == 3
    assert all(x["avg_rating"] >= 4.7 for x in items4)
    assert [x["avg_rating"] for x in items4] == [4.9, 4.8, 4.7]
    print("-> PASS: Lọc điểm đánh giá tối thiểu và sắp xếp rating chuẩn")

    # TEST 5: Lọc theo cả 5 tiện ích trong RestaurantAmenities
    print("\n--- [TEST 5] Kiểm tra lọc từng tiện ích trong 5 tiện ích RestaurantAmenities ---")
    amenity_expectations = {
        "has_parking": 4,
        "has_private_room": 3,
        "has_outdoor": 3,
        "pet_friendly": 2,
        "vegetarian_support": 3,
    }
    for flag, expected_count in amenity_expectations.items():
        res_am = client.get("/api/restaurants/filter", params={flag: True})
        assert res_am.status_code == 200
        got = res_am.json()["data"]
        print(f" -> {flag}=True: {len(got)} quán (kỳ vọng {expected_count})")
        assert len(got) == expected_count
        assert all(x["amenities"][flag] is True for x in got)
    print("-> PASS: Cả 5 tiện ích RestaurantAmenities lọc chính xác 100%")

    # TEST 6: Lọc kết hợp toàn diện tất cả tiêu chí (FR-07, UC-04)
    print("\n--- [TEST 6] Lọc ĐA ĐIỀU KIỆN KẾT HỢP tất cả tiêu chí cùng lúc ---")
    combo_params = {
        "cuisine_type": "Món Chay",
        "price_min": 100000,
        "price_max": 400000,
        "lat": CENTER_LAT,
        "lng": CENTER_LNG,
        "radius_km": 3.0,
        "min_rating": 4.8,
        "has_parking": True,
        "has_private_room": True,
        "has_outdoor": True,
        "pet_friendly": False,
        "vegetarian_support": True,
        "sort_by": "rating",
    }
    r6 = client.get("/api/restaurants/filter", params=combo_params)
    assert r6.status_code == 200
    d6 = r6.json()
    assert d6["pagination"]["total_items"] == 1
    match = d6["data"][0]
    print(f"Quán khớp 100% đa điều kiện: '{match['name']}' | distance={match['distance_km']} km | rating={match['avg_rating']}")
    assert match["name"] == "Hum Garden & Vegetarian"
    assert d6["applied_filters"]["cuisine_type"] == "Món Chay"
    assert d6["applied_filters"]["has_outdoor"] is True
    assert d6["applied_filters"]["pet_friendly"] is False
    print("-> PASS: Truy vấn kết hợp đa điều kiện trả về kết quả duy nhất chính xác tuyệt đối")

    # TEST 7: Sắp xếp giá & Phân trang trên /api/restaurants/filter và /api/restaurants
    print("\n--- [TEST 7] Kiểm tra sắp xếp giá, phân trang & tương thích GET /api/restaurants ---")
    r7_asc = client.get("/api/restaurants/filter", params={"sort_by": "price_asc", "page": 1, "limit": 2})
    assert r7_asc.status_code == 200
    d7 = r7_asc.json()
    assert len(d7["data"]) == 2
    assert d7["pagination"]["total_items"] == 5
    assert d7["pagination"]["total_pages"] == 3
    assert d7["data"][0]["min_price"] <= d7["data"][1]["min_price"]

    # Tương thích ngược endpoint GET /api/restaurants kèm filter
    r7_compat = client.get("/api/restaurants", params={"has_parking": True, "vegetarian_support": True})
    assert r7_compat.status_code == 200
    assert r7_compat.json()["pagination"]["total_items"] == 3
    print("-> PASS: Sắp xếp, phân trang và tương thích ngược hoạt động hoàn hảo")

    # TEST 8: Validation lỗi tham số đầu vào
    print("\n--- [TEST 8] Kiểm tra Validation các tham số sai (400 / 422) ---")
    err_price = client.get("/api/restaurants/filter", params={"price_min": 500000, "price_max": 100000})
    assert err_price.status_code == 400

    err_radius_no_coords = client.get("/api/restaurants/filter", params={"radius_km": 5.0})
    assert err_radius_no_coords.status_code == 400

    err_half_coords = client.get("/api/restaurants/filter", params={"lat": CENTER_LAT})
    assert err_half_coords.status_code == 400

    err_sort = client.get("/api/restaurants/filter", params={"sort_by": "invalid_mode"})
    assert err_sort.status_code == 400

    err_rating = client.get("/api/restaurants/filter", params={"min_rating": 6.5})
    assert err_rating.status_code == 422
    print("-> PASS: Đã chặn đúng toàn bộ tham số không hợp lệ (400 / 422)\n")

    print("==================================================================")
    print(">>> TẤT CẢ 8 BÀI TEST LỌC ĐA ĐIỀU KIỆN TE9C660 ĐỀU PASS 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_multi_filter_tests()
