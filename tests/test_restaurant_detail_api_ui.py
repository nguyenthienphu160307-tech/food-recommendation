"""
==============================================================================
UNIT & INTEGRATION TESTS: API & TRANG CHI TIẾT NHÀ HÀNG, TIỆN ÍCH VÀ THỰC ĐƠN (FR-09)
MÃ TASK: TE9C662
Kiểm thử toàn diện:
1. API GET /api/restaurants/{restaurant_id}:
   - Lấy thông tin chi tiết nhà hàng thành công (200 OK)
   - Tính toán khoảng cách Haversine chính xác khi truyền lat, lng
   - Kiểm tra validation tọa độ (400 khi chỉ truyền 1 trong 2 tọa độ)
   - Trả về mã 404 khi không tìm thấy nhà hàng
   - Cung cấp đầy đủ 5 tiện ích trong RestaurantAmenities
   - Trả về bộ ảnh slide sắp xếp theo display_order (RestaurantImages)
   - Trả về danh mục thực đơn (RestaurantMenus) kèm từng món ăn (MenuItems)
2. UI & Frontend Integration:
   - Route phục vụ trang HTML: GET /restaurant-detail và GET /restaurant-detail.html
   - File frontend/restaurant-detail.html có đầy đủ Slider ảnh, 5 tiện ích, thực đơn phân nhóm, mini map Leaflet
   - Liên kết điều hướng từ frontend/index.html sang restaurant-detail.html?id=...
==============================================================================
"""

import sys
import os
import re

# Thêm thư mục gốc dev/food-recommendation vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.restaurant import (
    Restaurant,
    RestaurantAmenity,
    RestaurantImage,
    RestaurantMenu,
    MenuItem,
)

client = TestClient(app)

# Tọa độ mẫu kiểm thử (Nhà thờ Đức Bà Sài Gòn, Q1)
TEST_USER_LAT = 10.779786
TEST_USER_LNG = 106.699018


@pytest.fixture(scope="module", autouse=True)
def setup_test_restaurant_data():
    """Khởi tạo dữ liệu mẫu cho module test chi tiết nhà hàng."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có dữ liệu mẫu chưa
        sample = db.query(Restaurant).filter(Restaurant.name == "Nhà Hàng Chi Tiết Mẫu TE9C662").first()
        if not sample:
            test_rest = Restaurant(
                name="Nhà Hàng Chi Tiết Mẫu TE9C662",
                description="Nhà hàng phục vụ thử nghiệm tính năng chi tiết FR-09",
                address="123 Đường Test Chi Tiết, Phường Bến Nghé, Quận 1, TP.HCM",
                phone_number="02838999999",
                cuisine_type="Món Việt",
                latitude=10.778000,
                longitude=106.700000,
                min_price=120000.0,
                max_price=450000.0,
                open_hours="09:00 - 22:30",
                avg_rating=4.8,
                total_reviews=350,
                status="active",
            )
            db.add(test_rest)
            db.flush()

            # Thêm 5 tiện ích
            amenity = RestaurantAmenity(
                restaurant_id=test_rest.id,
                has_parking=True,
                has_private_room=True,
                has_outdoor=False,
                pet_friendly=False,
                vegetarian_support=True,
            )
            db.add(amenity)

            # Thêm bộ ảnh slide
            img1 = RestaurantImage(
                restaurant_id=test_rest.id,
                image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
                caption="Không gian phòng ăn chính sang trọng",
                is_cover=True,
                display_order=1,
            )
            img2 = RestaurantImage(
                restaurant_id=test_rest.id,
                image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
                caption="Mặt tiền ấm cúng buổi tối",
                is_cover=False,
                display_order=2,
            )
            db.add_all([img1, img2])

            # Thêm nhóm thực đơn và món ăn
            menu1 = RestaurantMenu(
                restaurant_id=test_rest.id,
                name="Món Khai Vị & Đặc Sản",
                description="Các món khai vị nức tiếng",
                display_order=1,
            )
            menu2 = RestaurantMenu(
                restaurant_id=test_rest.id,
                name="Đồ Uống & Tráng Miệng",
                description="Thức uống thanh mát tự nhiên",
                display_order=2,
            )
            db.add_all([menu1, menu2])
            db.flush()

            item1 = MenuItem(
                menu_id=menu1.id,
                name="Chả Giò Hải Sản Hoàng Kim",
                description="Tôm thịt tươi gói bánh tráng rế giòn rụm",
                price=135000.0,
                image_url="https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
                is_available=True,
            )
            item2 = MenuItem(
                menu_id=menu1.id,
                name="Gỏi Ngó Sen Tôm Thịt",
                description="Ngó sen tươi giòn chua ngọt thanh mát",
                price=115000.0,
                image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400",
                is_available=True,
            )
            item3 = MenuItem(
                menu_id=menu2.id,
                name="Trà Hoa Cúc Mật Ong",
                description="Hoa cúc sấy lạnh kết hợp mật ong rừng",
                price=45000.0,
                image_url="https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400",
                is_available=False,
            )
            db.add_all([item1, item2, item3])
            db.commit()
    finally:
        db.close()


def get_sample_restaurant_id():
    db = SessionLocal()
    try:
        r = db.query(Restaurant).filter(Restaurant.name == "Nhà Hàng Chi Tiết Mẫu TE9C662").first()
        if r:
            return r.id
        first_r = db.query(Restaurant).first()
        return first_r.id if first_r else 1
    finally:
        db.close()


# ==============================================================================
# PHẦN 1: KIỂM THỬ API CHI TIẾT NHÀ HÀNG (GET /api/restaurants/{id})
# ==============================================================================

def test_api_restaurant_detail_success():
    """Kiểm tra gọi API lấy thông tin chi tiết nhà hàng trả về mã 200 và đủ dữ liệu cốt lõi."""
    rest_id = get_sample_restaurant_id()
    response = client.get(f"/api/restaurants/{rest_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data["id"] == rest_id
    assert "name" in data and len(data["name"]) > 0
    assert "address" in data and len(data["address"]) > 0
    assert "phone_number" in data
    assert "open_hours" in data
    assert "min_price" in data and data["min_price"] >= 0
    assert "max_price" in data and data["max_price"] >= data["min_price"]
    assert "avg_rating" in data and 0 <= data["avg_rating"] <= 5.0
    assert "total_reviews" in data and data["total_reviews"] >= 0


def test_api_restaurant_detail_distance_calculation():
    """Kiểm tra tính khoảng cách Haversine chính xác khi người dùng truyền lat, lng."""
    rest_id = get_sample_restaurant_id()
    response = client.get(f"/api/restaurants/{rest_id}?lat={TEST_USER_LAT}&lng={TEST_USER_LNG}")
    assert response.status_code == 200
    data = response.json()
    assert data["distance_km"] is not None
    assert isinstance(data["distance_km"], (int, float))
    assert 0.0 <= data["distance_km"] <= 10.0, f"Khoảng cách không hợp lý: {data['distance_km']} km"


def test_api_restaurant_detail_invalid_gps_coords():
    """Kiểm tra validation: truyền lat mà thiếu lng hoặc ngược lại phải trả về 400 Bad Request."""
    rest_id = get_sample_restaurant_id()
    # Chỉ truyền lat
    res1 = client.get(f"/api/restaurants/{rest_id}?lat={TEST_USER_LAT}")
    assert res1.status_code == 400
    assert "đầy đủ cả hai tọa độ" in res1.json()["detail"]

    # Chỉ truyền lng
    res2 = client.get(f"/api/restaurants/{rest_id}?lng={TEST_USER_LNG}")
    assert res2.status_code == 400
    assert "đầy đủ cả hai tọa độ" in res2.json()["detail"]


def test_api_restaurant_detail_not_found():
    """Kiểm tra trả về mã 404 Not Found khi ID nhà hàng không tồn tại."""
    response = client.get("/api/restaurants/9999999")
    assert response.status_code == 404
    assert "Không tìm thấy" in response.json()["detail"]


def test_api_restaurant_detail_amenities():
    """Kiểm tra trả về đầy đủ 5 tiện ích chính trong RestaurantAmenities."""
    rest_id = get_sample_restaurant_id()
    response = client.get(f"/api/restaurants/{rest_id}")
    assert response.status_code == 200
    data = response.json()

    assert "amenities" in data and data["amenities"] is not None
    amenities = data["amenities"]
    assert "has_parking" in amenities
    assert "has_private_room" in amenities
    assert "has_outdoor" in amenities
    assert "pet_friendly" in amenities
    assert "vegetarian_support" in amenities
    assert isinstance(amenities["has_parking"], bool)


def test_api_restaurant_detail_images_slider():
    """Kiểm tra danh sách ảnh slide RestaurantImages trả về có display_order và is_cover."""
    rest_id = get_sample_restaurant_id()
    response = client.get(f"/api/restaurants/{rest_id}")
    assert response.status_code == 200
    data = response.json()

    assert "images" in data
    assert isinstance(data["images"], list)
    assert len(data["images"]) >= 1, "Nhà hàng mẫu phải có ít nhất 1 ảnh"

    # Kiểm tra cấu trúc của từng ảnh
    for img in data["images"]:
        assert "id" in img
        assert "image_url" in img and img["image_url"].startswith("http")
        assert "caption" in img
        assert "is_cover" in img
        assert "display_order" in img

    # Kiểm tra thứ tự sắp xếp theo display_order tăng dần
    orders = [img["display_order"] for img in data["images"]]
    assert orders == sorted(orders), "Danh sách ảnh chưa được sắp xếp theo display_order!"


def test_api_restaurant_detail_menus_and_items():
    """Kiểm tra cấu trúc thực đơn phân nhóm RestaurantMenus kèm chi tiết từng MenuItem."""
    rest_id = get_sample_restaurant_id()
    response = client.get(f"/api/restaurants/{rest_id}")
    assert response.status_code == 200
    data = response.json()

    assert "menus" in data
    assert isinstance(data["menus"], list)
    assert len(data["menus"]) >= 1, "Nhà hàng mẫu phải có ít nhất 1 nhóm thực đơn"

    total_items = 0
    for menu in data["menus"]:
        assert "id" in menu
        assert "name" in menu and len(menu["name"]) > 0
        assert "display_order" in menu
        assert "items" in menu
        assert isinstance(menu["items"], list)
        
        for item in menu["items"]:
            total_items += 1
            assert "id" in item
            assert "name" in item and len(item["name"]) > 0
            assert "price" in item and item["price"] >= 0
            assert "is_available" in item
            assert isinstance(item["is_available"], bool)

    assert total_items >= 1, "Thực đơn phải chứa ít nhất 1 món ăn chi tiết"


# ==============================================================================
# PHẦN 2: KIỂM THỬ FRONTEND VÀ GIAO DIỆN NGƯỜI DÙNG
# ==============================================================================

def test_frontend_routes_served():
    """Kiểm tra FastAPI router phục vụ đúng file HTML chi tiết nhà hàng."""
    res1 = client.get("/restaurant-detail")
    assert res1.status_code == 200
    assert "text/html" in res1.headers["content-type"]

    res2 = client.get("/restaurant-detail.html")
    assert res2.status_code == 200
    assert "text/html" in res2.headers["content-type"]


def test_frontend_detail_html_components():
    """Kiểm tra nội dung file frontend/restaurant-detail.html chứa đầy đủ các thành phần bắt buộc."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    detail_html_path = os.path.join(project_root, "frontend", "restaurant-detail.html")
    assert os.path.exists(detail_html_path), "File frontend/restaurant-detail.html không tồn tại!"

    with open(detail_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Header & Navigation
    assert 'id="btn-back"' in html or 'nav-back-btn' in html
    assert 'id="btn-favorite"' in html
    assert 'id="btn-share"' in html
    assert 'id="theme-toggle"' in html

    # 2. Hero Image Slider (RestaurantImages)
    assert 'id="main-slide-img"' in html
    assert 'id="slide-prev"' in html
    assert 'id="slide-next"' in html
    assert 'id="slide-thumbs"' in html
    assert 'id="slide-caption"' in html
    assert 'id="slide-counter"' in html

    # 3. Core info
    assert 'id="restaurant-name"' in html
    assert 'id="badge-cuisine"' in html
    assert 'id="badge-rating"' in html
    assert 'id="badge-open-status"' in html
    assert 'id="badge-distance"' in html
    assert 'id="info-address"' in html
    assert 'id="info-hours"' in html
    assert 'id="info-phone"' in html
    assert 'id="info-price"' in html

    # 4. 5 Amenities (RestaurantAmenities)
    assert 'id="status-parking"' in html
    assert 'id="status-private-room"' in html
    assert 'id="status-outdoor"' in html
    assert 'id="status-pet"' in html
    assert 'id="status-vegetarian"' in html

    # 5. Grouped Menus & MenuItems
    assert 'id="menu-tabs"' in html
    assert 'id="menu-search-input"' in html
    assert 'id="menus-container"' in html

    # 6. Mini Map (Leaflet)
    assert 'id="mini-map"' in html
    assert "leaflet.js" in html

    # 7. Offline fallback to SEED_VENUES
    assert "SEED_VENUES" in html
    assert "venues-data.js" in html


def test_frontend_index_integration():
    """Kiểm tra frontend/index.html đã tích hợp liên kết mở trang restaurant-detail.html."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_html_path = os.path.join(project_root, "frontend", "index.html")
    assert os.path.exists(index_html_path)

    with open(index_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Modal có liên kết mở restaurant-detail.html?id=...
    assert "restaurant-detail.html?id=" in html or "restaurant-detail?id=" in html
    assert "Xem thực đơn & chi tiết quán" in html


if __name__ == "__main__":
    pytest.main(["-v", __file__])
